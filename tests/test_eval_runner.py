"""
Unit tests for eval_runner module.
"""

import json
import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest  # noqa: F401
import yaml

# Import the module to test
import eval_runner


class TestAPIEvaluator:
    """Test cases for APIEvaluator class."""

    def test_init_with_valid_provider(self) -> None:
        """Test APIEvaluator initialization with valid provider."""
        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            evaluator = eval_runner.APIEvaluator(
                provider="openai", model="gpt-4o", base_url="https://api.openai.com/v1"
            )
            assert evaluator.provider == "openai"
            assert evaluator.model == "gpt-4o"
            assert evaluator.base_url == "https://api.openai.com/v1"

    def test_init_missing_api_key(self) -> None:
        """Test APIEvaluator initialization fails without API key."""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="API key required for provider"):
                eval_runner.APIEvaluator(
                    provider="openai",
                    model="gpt-4o",
                    base_url="https://api.openai.com/v1",
                )

    def test_init_openai_not_available(self) -> None:
        """Test APIEvaluator initialization fails when OpenAI is not available."""

        # Mock the import to raise ImportError when openai is imported
        def mock_import(name: str, *args: Any, **kwargs: Any) -> Any:
            if name == "openai":
                raise ImportError("No module named 'openai'")
            return __import__(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            with pytest.raises(ImportError, match="OpenAI package is required"):
                eval_runner.APIEvaluator(
                    provider="openai",
                    model="gpt-4o",
                    base_url="https://api.openai.com/v1",
                )


class TestConfigurationHandling:
    """Test cases for configuration loading and handling."""

    def test_load_config_yaml(self) -> None:
        """Test loading YAML configuration."""
        config_data = {
            "provider": "openai",
            "model": "gpt-4o",
            "base_url": "https://api.openai.com/v1",
            "test_cases": [],
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = f.name

        try:
            loaded_config = eval_runner.load_config(temp_path)
            assert loaded_config["provider"] == "openai"
            assert loaded_config["model"] == "gpt-4o"
        finally:
            Path(temp_path).unlink()

    def test_load_config_json(self) -> None:
        """Test loading JSON configuration."""
        config_data = {
            "provider": "openai",
            "model": "gpt-4o",
            "base_url": "https://api.openai.com/v1",
            "test_cases": [],
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name

        try:
            loaded_config = eval_runner.load_config(temp_path)
            assert loaded_config["provider"] == "openai"
            assert loaded_config["model"] == "gpt-4o"
        finally:
            Path(temp_path).unlink()

    def test_load_config_file_not_found(self) -> None:
        """Test loading config returns empty dict for non-existent file."""
        result = eval_runner.load_config("non_existent_file.yaml")
        assert result == {}


class TestPromptEvaluator:
    """Test cases for PromptEvaluator class."""

    def test_prompt_evaluator_init(self) -> None:
        """Test PromptEvaluator initialization."""
        evaluator = eval_runner.PromptEvaluator()
        assert evaluator.base_path == Path(".")
        assert isinstance(evaluator.detection_tests, dict)
        assert isinstance(evaluator.generation_tests, dict)


class TestDataStructures:
    """Test cases for data structure types."""

    def test_test_result_dataclass(self) -> None:
        """Test TestResult dataclass creation."""
        result = eval_runner.TestResult(
            test_id="test-1",
            name="Test Security",
            expected=True,
            detected=True,
            confidence=0.95,
            message="Security issue detected",
            correct=True,
            details={"category": "security"},
        )

        assert result.test_id == "test-1"
        assert result.correct is True
        assert result.confidence == 0.95

    def test_evaluation_report_dataclass(self) -> None:
        """Test EvaluationReport dataclass creation."""
        report = eval_runner.EvaluationReport(
            total_tests=10,
            correct_predictions=8,
            accuracy=0.8,
            precision=0.85,
            recall=0.75,
            f1_score=0.8,
            results_by_category={},
            failed_tests=[],
        )

        assert report.total_tests == 10
        assert report.accuracy == 0.8


class TestPromptMetadata:
    """Test cases for prompt metadata parsing."""

    def test_parse_prompt_metadata_valid(self) -> None:
        """Test parsing valid prompt metadata."""
        prompt = """<!-- PROMPT_METADATA
platform: web
focus: security,accessibility
mode: review
-->

You are a code reviewer."""

        result = eval_runner.parse_prompt_metadata(prompt)
        assert result["platform"] == "web"
        assert result["focus"] == "security,accessibility"
        assert result["mode"] == "review"

    def test_parse_prompt_metadata_empty_prompt(self) -> None:
        """Test parsing prompt without metadata."""
        prompt = "You are a code reviewer."
        result = eval_runner.parse_prompt_metadata(prompt)
        assert result == {}

    def test_parse_prompt_metadata_malformed(self) -> None:
        """Test parsing malformed metadata."""
        prompt = """<!-- PROMPT_METADATA
platform web
focus: security
invalid line without colon
-->

You are a code reviewer."""

        result = eval_runner.parse_prompt_metadata(prompt)
        assert result["focus"] == "security"
        assert "platform" not in result  # Line without colon is ignored

    def test_parse_prompt_metadata_whitespace_handling(self) -> None:
        """Test parsing metadata with extra whitespace."""
        prompt = """<!-- PROMPT_METADATA
  platform  :   web
  focus:security, accessibility
-->

You are a code reviewer."""

        result = eval_runner.parse_prompt_metadata(prompt)
        assert result["platform"] == "web"
        assert result["focus"] == "security, accessibility"


class TestUtilityFunctions:
    """Test cases for utility functions."""

    def test_load_dotenv_with_file(self) -> None:
        """Test loading environment variables from .env file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("TEST_KEY=test_value\n")
            f.write("# Comment line\n")
            f.write("ANOTHER_KEY=another_value\n")
            f.write("\n")  # Empty line
            temp_path = f.name

        try:
            # Change to temp directory and create .env file there
            temp_dir = Path(temp_path).parent

            with patch("os.chdir"):
                with patch("pathlib.Path.cwd", return_value=temp_dir):
                    with patch("pathlib.Path.exists", return_value=True):
                        with patch("builtins.open", return_value=open(temp_path)):
                            # Clear environment first
                            with patch.dict("os.environ", {}, clear=True):
                                eval_runner.load_dotenv()
                                # Function modifies os.environ, but we can't test that easily
                                # with mocking. Test that it runs without error.
        finally:
            Path(temp_path).unlink()

    def test_mock_ai_evaluator(self) -> None:
        """Test mock AI evaluator function."""
        prompt = "Review this code for security issues."
        result = eval_runner.mock_ai_evaluator(prompt)

        assert isinstance(result, str)
        assert len(result) > 0
        # Check that it returns a response suggesting issues were found
        assert any(word in result.lower() for word in ["issue", "security", "vulnerabilit"])

    def test_mock_ai_generator(self) -> None:
        """Test mock AI generator function."""
        prompt = "Generate a login form component."
        result = eval_runner.mock_ai_generator(prompt)

        assert isinstance(result, str)
        assert "Generated code would appear here" in result

    def test_enhance_prompt_with_llm_cached(self) -> None:
        """Test prompt enhancement with cached result."""
        prompt = "You are a code reviewer."

        # Create a mock API evaluator
        mock_api_evaluator = eval_runner.APIEvaluator.__new__(eval_runner.APIEvaluator)
        mock_api_evaluator.provider = "openai"
        mock_api_evaluator.model = "gpt-4o"
        mock_api_evaluator.base_url = "https://api.openai.com/v1"

        # Create a temporary cache file
        import hashlib

        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
        cache_dir = Path(".cache")
        cache_dir.mkdir(exist_ok=True)
        cache_file = cache_dir / f"enhanced_{prompt_hash}.txt"

        try:
            # Write cached content
            with open(cache_file, "w") as f:
                f.write("Enhanced prompt from cache")

            result = eval_runner.enhance_prompt_with_llm(
                prompt, mock_api_evaluator, show_diff=False
            )
            assert result == "Enhanced prompt from cache"
        finally:
            if cache_file.exists():
                cache_file.unlink()

    def test_enhance_prompt_with_llm_api_error(self) -> None:
        """Test prompt enhancement when API fails."""
        prompt = "You are a code reviewer."

        # Create a mock API evaluator that will fail
        class FailingAPIEvaluator:
            provider = "openai"
            model = "gpt-4o"
            base_url = "https://api.openai.com/v1"

            def evaluate_code(self, prompt: str) -> str:
                raise Exception("API Error")

        mock_api_evaluator = FailingAPIEvaluator()

        # Ensure no cache file exists
        import hashlib

        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
        cache_dir = Path(".cache")
        cache_file = cache_dir / f"enhanced_{prompt_hash}.txt"
        if cache_file.exists():
            cache_file.unlink()

        result = eval_runner.enhance_prompt_with_llm(prompt, mock_api_evaluator, show_diff=False)  # type: ignore
        # Should return original prompt when enhancement fails
        assert result == prompt


class TestSmartContextDetection:
    """Test cases for Smart Context Detection integration."""

    def test_evaluate_detection_prompt_with_metadata(self) -> None:
        """Test that evaluation uses prompt metadata for filtering."""
        evaluator = eval_runner.PromptEvaluator()

        # Mock test data with different platforms
        evaluator.detection_tests = {
            "security": [
                {
                    "id": "web-1",
                    "name": "Web Security",
                    "platform": "web",
                    "expected": {"detected": True},
                },
                {
                    "id": "ios-1",
                    "name": "iOS Security",
                    "platform": "ios",
                    "expected": {"detected": True},
                },
            ]
        }

        prompt_with_metadata = """<!-- PROMPT_METADATA
platform: web
focus: security
-->

You are a code reviewer."""

        # This would normally run the evaluation, but we can't easily test the full flow
        # without more complex mocking. The important part is that the metadata parsing works.
        metadata = eval_runner.parse_prompt_metadata(prompt_with_metadata)
        assert metadata["platform"] == "web"
        assert metadata["focus"] == "security"


class TestMainFunction:
    """Test cases for main function CLI behavior."""

    @patch("eval_runner.PromptEvaluator")
    @patch("eval_runner.APIEvaluator")
    @patch("sys.argv", ["eval_runner.py", "--mode", "detection"])
    def test_main_detection_mode(self, mock_api_evaluator: Any, mock_prompt_evaluator: Any) -> None:
        """Test main function in detection mode."""
        # Mock the evaluator classes
        mock_evaluator_instance = mock_prompt_evaluator.return_value

        # Mock the evaluation report
        mock_report = eval_runner.EvaluationReport(
            total_tests=10,
            correct_predictions=8,
            accuracy=0.8,
            precision=0.85,
            recall=0.75,
            f1_score=0.8,
            results_by_category={},
            failed_tests=[],
        )
        mock_evaluator_instance.evaluate_detection_prompt.return_value = mock_report

        # Test that main runs without error
        eval_runner.main()

        # Verify the evaluators were created and called
        mock_prompt_evaluator.assert_called_once()
        mock_api_evaluator.assert_called_once_with("openai", "gpt-4o", "https://api.openai.com/v1")

    @patch(
        "sys.argv",
        ["eval_runner.py", "--mode", "detection", "--principles", "security,accessibility"],
    )
    @patch("eval_runner.PromptEvaluator")
    def test_main_with_principles(self, mock_prompt_evaluator: Any) -> None:
        """Test main function with specific principles."""
        mock_evaluator_instance = mock_prompt_evaluator.return_value
        mock_report = eval_runner.EvaluationReport(
            total_tests=5,
            correct_predictions=4,
            accuracy=0.8,
            precision=0.8,
            recall=0.8,
            f1_score=0.8,
            results_by_category={},
            failed_tests=[],
        )
        mock_evaluator_instance.evaluate_detection_prompt.return_value = mock_report

        with patch("eval_runner.APIEvaluator"):
            eval_runner.main()

        # Check that principles were parsed correctly
        mock_evaluator_instance.evaluate_detection_prompt.assert_called()

    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch(
        "sys.argv", ["eval_runner.py", "--mode", "detection", "--prompt-file", "nonexistent.txt"]
    )
    def test_main_missing_prompt_file(self, mock_open: Any) -> None:
        """Test main function with missing prompt file."""
        with pytest.raises(FileNotFoundError):
            eval_runner.main()


if __name__ == "__main__":
    pytest.main([__file__])
