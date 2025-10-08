"""
Unit tests for principles_cli module.
"""

from typing import Any
from unittest.mock import patch

import pytest

# Import the module to test
from principles_cli import PrinciplesCLI


class TestFormatPrinciples:
    """Test cases for format_principles method."""

    def test_format_principles_no_focus(self) -> None:
        """Test formatting principles without focus areas."""
        cli = PrinciplesCLI()
        principles = {
            "security": {
                "why": "Test why",
                "how": ["Step 1", "Step 2"],
                "enforcement": {"automated": ["tool1"], "manual": ["review1"]},
            }
        }

        result = cli.format_principles(principles)
        assert (
            "**Priority Order:** Security > Accessibility > Testing > Performance > Code Style"
            in result
        )
        assert "### Security" in result
        assert "**Why:** Test why" in result
        assert "- Step 1" in result
        assert "- Step 2" in result

    def test_format_principles_with_focus(self) -> None:
        """Test formatting principles with specific focus areas."""
        cli = PrinciplesCLI()
        principles = {
            "security": {"why": "Security matters", "how": ["Use HTTPS"]},
            "accessibility": {"why": "Access matters", "how": ["Use ARIA"]},
            "testing": {"why": "Quality matters", "how": ["Write tests"]},
        }
        focus_areas = ["security", "accessibility"]

        result = cli.format_principles(principles, focus_areas)
        assert "### Security" in result
        assert "### Accessibility" in result
        assert "### Testing" not in result

    def test_format_principles_with_component_filter(self) -> None:
        """Test formatting principles with component-based filtering (e.g., UI components)."""
        cli = PrinciplesCLI()
        principles = {
            "accessibility": {"why": "Access matters", "how": ["Use ARIA"]},
            "flexible_layout": {"why": "Layout matters", "how": ["Use flexbox"]},
            "design_integrity": {"why": "Design matters", "how": ["Follow specs"]},
            "localization": {"why": "L10n matters", "how": ["Externalize strings"]},
            "security": {"why": "Security matters", "how": ["Use HTTPS"]},
            "testing": {"why": "Testing matters", "how": ["Write tests"]},
            "unidirectional_data_flow": {"why": "Data flow matters", "how": ["One-way"]},
        }
        # UI component principles (like what generate_code_prompt passes)
        ui_principles = [
            "accessibility",
            "flexible_layout",
            "design_integrity",
            "localization",
            "security",
        ]

        result = cli.format_principles(principles, ui_principles)
        assert "### Accessibility" in result
        assert "### Flexible_Layout" in result
        assert "### Design_Integrity" in result
        assert "### Localization" in result
        assert "### Security" in result
        # These shouldn't be included for UI components
        assert "### Testing" not in result
        assert "### Unidirectional_Data_Flow" not in result

    def test_format_principles_missing_fields(self) -> None:
        """Test formatting principles with missing fields."""
        cli = PrinciplesCLI()
        principles = {
            "security": {
                "why": "Test why"
                # Missing 'how' and 'enforcement'
            }
        }

        result = cli.format_principles(principles)
        assert "### Security" in result
        assert "**Why:** Test why" in result
        # Should handle missing fields gracefully


class TestFormatPlatformRequirements:
    """Test cases for format_platform_requirements method."""

    def test_format_platform_requirements_ios(self) -> None:
        """Test formatting iOS platform requirements."""
        cli = PrinciplesCLI()
        platform_config = {
            "approved_dependencies": {"frameworks": ["UIKit", "Foundation", "Core Data"]},
            "tools": {"linting": ["SwiftLint"], "testing": ["XCTest", "Quick/Nimble"]},
        }

        result = cli.format_platform_requirements(platform_config)
        assert "**Approved Dependencies:**" in result
        assert "- UIKit (frameworks)" in result
        assert "- Foundation (frameworks)" in result
        assert "**Required Tools:**" in result
        assert "- SwiftLint (linting)" in result
        assert "- XCTest (testing)" in result

    def test_format_platform_requirements_android(self) -> None:
        """Test formatting Android platform requirements with detailed dependencies."""
        cli = PrinciplesCLI()
        platform_config = {
            "approved_dependencies": {
                "architecture": [
                    {
                        "name": "Dagger/Hilt",
                        "purpose": "Dependency injection",
                        "version": "2.x",
                    }
                ],
                "reactive": [
                    {
                        "name": "RxJava2",
                        "purpose": "Reactive programming",
                        "version": "2.x",
                    }
                ],
            },
            "tools": {"linting": ["ktlint", "detekt"]},
        }

        result = cli.format_platform_requirements(platform_config)
        assert "- Dagger/Hilt v2.x - Dependency injection (architecture)" in result
        assert "- RxJava2 v2.x - Reactive programming (reactive)" in result
        assert "- ktlint (linting)" in result

    def test_format_platform_requirements_empty(self) -> None:
        """Test formatting empty platform requirements."""
        cli = PrinciplesCLI()
        result = cli.format_platform_requirements({})
        assert result == ""


class TestFormatDetectionRules:
    """Test cases for format_detection_rules method."""

    def test_format_detection_rules_basic(self) -> None:
        """Test formatting basic detection rules."""
        cli = PrinciplesCLI()
        rules = {
            "security": {
                "hardcoded_secrets": {
                    "description": "Detect API keys in code",
                    "severity": "critical",
                    "patterns": [
                        {
                            "regex": "api_key.*=.*['\"][^'\"]+['\"]",
                            "message": "API key found",
                        }
                    ],
                }
            }
        }

        result = cli.format_detection_rules(rules)
        assert "### Security Rules" in result
        assert "**Hardcoded Secrets** (Severity: critical)" in result
        assert "- Detect API keys in code" in result
        assert "- Detection patterns:" in result
        assert "api_key.*=.*['\"][^'\"]+['\"]" in result
        assert "API key found" in result

    def test_format_detection_rules_nested_patterns(self) -> None:
        """Test formatting rules with nested pattern structures."""
        cli = PrinciplesCLI()
        rules = {
            "security": {
                "insecure_storage": {
                    "description": "Detect insecure storage",
                    "severity": "critical",
                    "patterns": [
                        {
                            "regex": "SharedPreferences.*password",
                            "message": "Insecure storage",
                        }
                    ],
                }
            }
        }

        result = cli.format_detection_rules(rules)
        assert "### Security Rules" in result
        assert "**Insecure Storage** (Severity: critical)" in result
        assert "- Detection patterns:" in result
        assert "SharedPreferences.*password" in result

    def test_format_detection_rules_empty(self) -> None:
        """Test formatting empty detection rules."""
        cli = PrinciplesCLI()
        result = cli.format_detection_rules({})
        assert result == ""


class TestFormatSeverityLevels:
    """Test cases for format_severity_levels method."""

    def test_format_severity_levels_complete(self) -> None:
        """Test formatting complete severity levels."""
        cli = PrinciplesCLI()
        severity = {
            "critical": {
                "description": "Immediate harm to users",
                "action": "Block merge immediately",
                "examples": ["Hardcoded secrets", "Missing accessibility"],
            },
            "blocking": {
                "description": "Break engineering standards",
                "action": "Block merge until resolved",
                "examples": ["Test coverage below 80%", "Build warnings"],
            },
        }

        result = cli.format_severity_levels(severity)
        assert "- **Critical**: Immediate harm to users" in result
        assert "  - Action: Block merge immediately" in result
        assert "    - Hardcoded secrets" in result
        assert "- **Blocking**: Break engineering standards" in result
        assert "    - Test coverage below 80%" in result

    def test_format_severity_levels_minimal(self) -> None:
        """Test formatting minimal severity levels."""
        cli = PrinciplesCLI()
        severity = {"critical": {"description": "Critical issues"}}

        result = cli.format_severity_levels(severity)
        assert "- **Critical**: Critical issues" in result
        assert "Action: See documentation" in result

    def test_format_severity_levels_empty(self) -> None:
        """Test formatting empty severity levels."""
        cli = PrinciplesCLI()
        result = cli.format_severity_levels({})
        assert result == ""


class TestGenerateReviewPrompt:
    """Test cases for generate_review_prompt method."""

    @patch("principles_cli.LeapLoader")
    def test_generate_review_prompt_basic(self, mock_loader_class: Any) -> None:
        """Test generating basic review prompt."""
        # Setup mock loader instance
        mock_loader = mock_loader_class.return_value
        mock_loader.load_principles.return_value = {
            "security": {"why": "Security matters", "how": ["Use HTTPS"]}
        }
        mock_loader.load_platforms.return_value = {
            "web": {"approved_dependencies": {"framework": ["React"]}}
        }
        mock_loader.load_severity_levels.return_value = {
            "critical": {"description": "Critical issues", "action": "Block"}
        }
        mock_loader.load_detection_rules.return_value = {
            "hardcoded_secrets": {
                "description": "Find secrets",
                "severity": "critical",
            }
        }
        mock_loader.get_platform_title.return_value = "Web"

        cli = PrinciplesCLI()
        result = cli.generate_review_prompt("web", ["security"])

        # Check for metadata header
        assert "<!-- PROMPT_METADATA" in result
        assert "platform: web" in result
        assert "focus: security" in result

        # Check for main content
        assert "# Code Review Assistant for Web" in result

    @patch("principles_cli.LeapLoader")
    def test_generate_review_prompt_missing_rule_file(self, mock_loader_class: Any) -> None:
        """Test generating prompt when rule file doesn't exist."""
        # Setup mock loader instance
        mock_loader = mock_loader_class.return_value
        mock_loader.load_principles.return_value = {"security": {"why": "Security matters"}}
        mock_loader.load_platforms.return_value = {"ios": {"tools": {"linting": ["SwiftLint"]}}}
        mock_loader.load_severity_levels.return_value = {"critical": {"description": "Critical"}}
        mock_loader.load_detection_rules.return_value = {}
        mock_loader.get_platform_title.return_value = "iOS"

        cli = PrinciplesCLI()
        result = cli.generate_review_prompt("ios", ["nonexistent"])

        # Check for metadata header
        assert "<!-- PROMPT_METADATA" in result
        assert "platform: ios" in result
        assert "focus: nonexistent" in result

        # Check for main content
        assert "# Code Review Assistant for iOS" in result


class TestGenerateCodePrompt:
    """Test cases for generate_code_prompt method."""

    @patch("principles_cli.LeapLoader")
    def test_generate_code_prompt_basic(self, mock_loader_class: Any) -> None:
        """Test generating basic code generation prompt."""
        # Setup mock loader instance
        mock_loader = mock_loader_class.return_value
        mock_loader.load_principles.return_value = {"security": {"why": "Security matters"}}
        mock_loader.load_platforms.return_value = {"android": {"tools": {"linting": ["ktlint"]}}}
        mock_loader.load_philosophy.return_value = {"description": "Build excellent software"}
        mock_loader.get_platform_title.return_value = "Android"
        mock_loader.get_common_prompt_data.return_value = (
            {"security": {"why": "Security matters"}},
            "Android",
            {"tools": {"linting": ["ktlint"]}},
        )

        cli = PrinciplesCLI()
        result = cli.generate_code_prompt("android", "ui")

        # Check for metadata header
        assert "<!-- PROMPT_METADATA" in result
        assert "platform: android" in result
        assert "component: ui" in result

        # Check for main content
        assert "# Code Generation for Android" in result

    @patch("principles_cli.LeapLoader")
    def test_generate_code_prompt_ui_filtering(self, mock_loader_class: Any) -> None:
        """Test that UI component generation only includes relevant principles."""
        # Setup mock loader instance
        mock_loader = mock_loader_class.return_value
        principles = {
            "accessibility": {"why": "Access for all", "how": ["Use ARIA"]},
            "flexible_layout": {"why": "Responsive design", "how": ["Flexbox"]},
            "design_integrity": {"why": "Match designs", "how": ["Follow specs"]},
            "localization": {"why": "Global reach", "how": ["Externalize strings"]},
            "security": {"why": "Protect users", "how": ["HTTPS only"]},
            "testing": {"why": "Quality code", "how": ["80% coverage"]},
            "unidirectional_data_flow": {"why": "Data flow", "how": ["One-way"]},
        }
        mock_loader.load_principles.return_value = principles
        mock_loader.load_philosophy.return_value = {"description": "Build excellent software"}
        mock_loader.load_platforms.return_value = {"android": {"tools": {"linting": ["ktlint"]}}}
        mock_loader.get_platform_title.return_value = "Android"
        mock_loader.get_common_prompt_data.return_value = (
            principles,
            "Android",
            {"tools": {"linting": ["ktlint"]}},
        )

        cli = PrinciplesCLI()
        result = cli.generate_code_prompt("android", "ui")

        # Check for metadata header
        assert "<!-- PROMPT_METADATA" in result
        assert "platform: android" in result
        assert "component: ui" in result

        # Check for main content
        assert "# Code Generation for Android Ui" in result
        assert "## Engineering Principles" in result

    @patch("principles_cli.LeapLoader")
    def test_generate_code_prompt_business_logic_filtering(self, mock_loader_class: Any) -> None:
        """Test that business logic component generation only includes relevant principles."""
        # Setup mock loader instance
        mock_loader = mock_loader_class.return_value
        principles = {
            "accessibility": {"why": "Access for all", "how": ["Use ARIA"]},
            "testing": {"why": "Quality code", "how": ["80% coverage"]},
            "unidirectional_data_flow": {"why": "Data flow", "how": ["One-way"]},
            "minimal_dependencies": {"why": "Simplicity", "how": ["Avoid bloat"]},
            "security": {"why": "Protect users", "how": ["HTTPS only"]},
            "flexible_layout": {"why": "Responsive design", "how": ["Flexbox"]},
        }
        mock_loader.load_principles.return_value = principles
        mock_loader.load_philosophy.return_value = {"description": "Build excellent software"}
        mock_loader.load_platforms.return_value = {"android": {"tools": {"testing": ["JUnit"]}}}
        mock_loader.get_platform_title.return_value = "Android"
        mock_loader.get_common_prompt_data.return_value = (
            principles,
            "Android",
            {"tools": {"testing": ["JUnit"]}},
        )

        cli = PrinciplesCLI()
        result = cli.generate_code_prompt("android", "business-logic")

        # Check for metadata header
        assert "<!-- PROMPT_METADATA" in result
        assert "platform: android" in result
        assert "component: business-logic" in result

        # Check for main content
        assert "# Code Generation for Android Business-Logic" in result
        assert "## Engineering Principles" in result


class TestArchitecturePrompt:
    """Test cases for generate_architecture_prompt method."""

    @patch("principles_cli.LeapLoader")
    def test_generate_architecture_prompt_basic(self, mock_loader_class: Any) -> None:
        """Test generating basic architecture prompt."""
        # Setup mock loader instance
        mock_loader = mock_loader_class.return_value
        principles = {"architecture": {"why": "Good structure matters"}}
        platform_config = {"approved_dependencies": {"framework": ["React"]}}
        mock_loader.load_principles.return_value = principles
        mock_loader.load_platforms.return_value = {"web": platform_config}
        mock_loader.get_platform_title.return_value = "Web"
        mock_loader.get_common_prompt_data.return_value = (
            principles,
            "Web",
            platform_config,
        )

        cli = PrinciplesCLI()
        result = cli.generate_architecture_prompt("web", "data")

        # Check for metadata header
        assert "<!-- PROMPT_METADATA" in result
        assert "platform: web" in result
        assert "layer: data" in result

        # Check for main content
        assert "# Architecture Assistant for Web" in result


class TestDependencyPrompt:
    """Test cases for generate_dependency_prompt method."""

    @patch("principles_cli.LeapLoader")
    def test_generate_dependency_prompt_approved(self, mock_loader_class: Any) -> None:
        """Test generating dependency prompt for libraries."""
        # Setup mock loader instance
        mock_loader = mock_loader_class.return_value
        principles = {"dependencies": {"why": "Minimize dependencies"}}
        platform_config = {
            "approved_dependencies": {
                "reactive": [
                    {
                        "name": "RxJava2",
                        "purpose": "Reactive programming",
                        "version": "2.x",
                    }
                ]
            }
        }
        mock_loader.load_principles.return_value = principles
        mock_loader.load_platforms.return_value = {"android": platform_config}
        mock_loader.get_platform_title.return_value = "Android"
        mock_loader.get_common_prompt_data.return_value = (
            principles,
            "Android",
            platform_config,
        )

        cli = PrinciplesCLI()
        result = cli.generate_dependency_prompt("android", ["rxjava2"])

        assert "# Dependency Evaluation for Android" in result
        assert "## Dependency Status Check" in result
        assert "rxjava2" in result

    @patch("principles_cli.LeapLoader")
    def test_generate_dependency_prompt_multiple(self, mock_loader_class: Any) -> None:
        """Test generating dependency prompt for multiple libraries."""
        # Setup mock loader instance
        mock_loader = mock_loader_class.return_value
        principles = {"dependencies": {"why": "Minimize dependencies"}}
        platform_config = {"approved_dependencies": {"frameworks": ["UIKit"]}}
        mock_loader.load_principles.return_value = principles
        mock_loader.load_platforms.return_value = {"ios": platform_config}
        mock_loader.get_platform_title.return_value = "iOS"
        mock_loader.get_common_prompt_data.return_value = (
            principles,
            "iOS",
            platform_config,
        )

        cli = PrinciplesCLI()
        result = cli.generate_dependency_prompt("ios", ["react-native", "lodash"])

        assert "# Dependency Evaluation for iOS" in result
        assert "## Dependency Status Check" in result
        assert "react-native" in result
        assert "lodash" in result


if __name__ == "__main__":
    pytest.main([__file__])
