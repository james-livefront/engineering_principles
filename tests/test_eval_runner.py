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


class TestProviderConfiguration:
    """Test cases for API provider configuration."""

    def test_api_providers_constants(self) -> None:
        """Test API_PROVIDERS constant has expected structure."""
        assert "openai" in eval_runner.API_PROVIDERS
        openai_config = eval_runner.API_PROVIDERS["openai"]
        assert openai_config["base_url"] == "https://api.openai.com/v1"
        assert openai_config["requires_key"] is True
        assert openai_config["default_model"] == "gpt-4o"


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


if __name__ == "__main__":
    pytest.main([__file__])
