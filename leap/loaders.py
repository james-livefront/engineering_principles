"""
YAML loading and data access for LEAP engineering principles.
"""

import sys
from pathlib import Path
from typing import Any

import yaml


class LeapLoader:
    """Loads YAML configuration and engineering principles data"""

    def __init__(self, base_path: Path | None = None):
        """Initialize loader with base path"""
        if base_path is None:
            base_path = Path(__file__).parent.parent

        self.base_path = base_path
        self.core_path = self.base_path / "core"
        self.modules_path = self.base_path / "modules"

    def load_yaml(self, file_path: Path) -> dict[str, Any]:
        """Load YAML safely"""
        try:
            with open(file_path) as f:
                data = yaml.safe_load(f)
                return dict(data) if data is not None else {}
        except FileNotFoundError:
            print(f"Error: File not found: {file_path}")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {e}")
            sys.exit(1)

    def load_principles(self) -> dict[str, Any]:
        """Load principles.yaml"""
        data = self.load_yaml(self.core_path / "principles.yaml")
        principles = data.get("principles", data)
        return principles if isinstance(principles, dict) else {}

    def load_platforms(self) -> dict[str, Any]:
        """Load platforms.yaml"""
        data = self.load_yaml(self.core_path / "platforms.yaml")
        platforms = data.get("platforms", data)
        return platforms if isinstance(platforms, dict) else {}

    def load_philosophy(self) -> dict[str, Any]:
        """Load philosophy.yaml"""
        return self.load_yaml(self.core_path / "philosophy.yaml")

    def load_enforcement(self) -> dict[str, Any]:
        """Load enforcement.yaml"""
        return self.load_yaml(self.core_path / "enforcement.yaml")

    def load_severity_levels(self) -> dict[str, Any]:
        """Load severity.yaml"""
        return self.load_yaml(self.modules_path / "detection" / "severity.yaml")

    def load_detection_rules(self, focus_area: str | None = None) -> dict[str, Any]:
        """Load detection rules, optionally filtered by focus area"""
        rules_path = self.modules_path / "detection" / "rules"

        if focus_area:
            # Load specific rules file
            file_path = rules_path / f"{focus_area}_rules.yaml"
            if file_path.exists():
                return self.load_yaml(file_path)

        # Load all rules files and combine
        all_rules = {}
        if rules_path.exists():
            for rule_file in rules_path.glob("*_rules.yaml"):
                rule_name = rule_file.stem.replace("_rules", "")
                all_rules[rule_name] = self.load_yaml(rule_file)

        return all_rules

    def load_generation_guidance(self) -> dict[str, Any]:
        """Load generation guidance"""
        guidance_path = self.modules_path / "generation" / "guidance.yaml"
        if guidance_path.exists():
            return self.load_yaml(guidance_path)
        return {}

    def get_common_prompt_data(self, platform: str) -> tuple[dict[str, Any], str, dict[str, Any]]:
        """Get common data needed by most prompt generation methods"""
        principles = self.load_principles()
        platform_title = self.get_platform_title(platform)
        platforms = self.load_platforms()
        platform_config = platforms.get(platform, {})
        return principles, platform_title, platform_config

    def get_platform_title(self, platform: str) -> str:
        """Get display title for platform"""
        return {"ios": "iOS", "android": "Android", "web": "Web"}.get(
            platform.lower(), platform.title()
        )
