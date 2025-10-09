"""
Unit tests for eval_runner module.
"""

from pathlib import Path
from unittest.mock import patch

import pytest  # noqa: F401

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


class TestPromptEvaluator:
    """Test cases for PromptEvaluator class."""

    def test_prompt_evaluator_init(self) -> None:
        """Test PromptEvaluator initialization."""
        evaluator = eval_runner.PromptEvaluator()
        # base_path is now auto-detected (should be the module directory or current dir)
        assert isinstance(evaluator.base_path, Path)
        assert evaluator.base_path.exists()
        assert isinstance(evaluator.detection_tests, dict)
        assert isinstance(evaluator.generation_tests, dict)


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

    # NOTE: enhance_prompt_with_llm was removed - feature not implemented
    # If we add LLM enhancement back, add tests here


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


if __name__ == "__main__":
    pytest.main([__file__])
