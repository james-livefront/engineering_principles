"""
Filtering and processing logic for LEAP data.
"""

from typing import Any


def filter_principles_by_focus(
    principles: dict[str, Any], focus_areas: list[str]
) -> dict[str, Any]:
    """Filter principles by focus areas"""
    if not focus_areas:
        return principles

    focus_to_principles = {
        "security": ["security"],
        "accessibility": ["accessibility"],
        "testing": ["testing"],
        "design": ["design_integrity", "flexible_layout"],
        "documentation": ["documentation"],
        "architecture": ["unidirectional_data_flow", "minimal_dependencies"],
        "performance": ["zero_build_warnings"],
        "localization": ["localization"],
        "compatibility": ["compatibility"],
        "code_quality": ["code_consistency", "zero_todos"],
    }

    relevant_principles = set()
    for area in focus_areas:
        if area in focus_to_principles:
            relevant_principles.update(focus_to_principles[area])

    if not relevant_principles:
        return principles

    filtered = {}
    for principle_key, principle_data in principles.items():
        if principle_key in relevant_principles:
            filtered[principle_key] = principle_data

    return filtered


def filter_detection_rules_by_platform(rules: dict[str, Any], platform: str) -> dict[str, Any]:
    """Filter detection rules by platform"""
    filtered_rules = {}

    for category, category_rules in rules.items():
        if not isinstance(category_rules, dict):
            continue

        filtered_category = {}
        for rule_name, rule_data in category_rules.items():
            if not isinstance(rule_data, dict):
                continue

            platforms = rule_data.get("platforms", [])
            if not platforms or platform in platforms:
                filtered_category[rule_name] = rule_data

        if filtered_category:
            filtered_rules[category] = filtered_category

    return filtered_rules


def map_focus_areas_to_enforcement_stages(focus_areas: list[str]) -> set[str]:
    """Map focus areas to relevant CI stages"""
    focus_to_stages = {
        "security": ["security"],
        "testing": ["test"],
        "code_quality": ["lint"],
        "accessibility": ["lint"],
        "architecture": ["build", "lint"],
    }

    relevant_stages = set()
    for area in focus_areas:
        relevant_stages.update(focus_to_stages.get(area, []))

    if not relevant_stages:
        relevant_stages = {"lint", "test", "security"}  # Defaults

    return relevant_stages


def get_component_type_principles(component_type: str) -> dict[str, list[str]]:
    """Get principles relevant to component type"""
    component_mappings = {
        "ui": {
            "always": ["accessibility", "flexible_layout", "design_integrity"],
            "usually": ["localization", "zero_build_warnings"],
            "sometimes": ["testing"],
        },
        "business-logic": {
            "always": ["testing", "unidirectional_data_flow", "zero_build_warnings"],
            "usually": ["minimal_dependencies", "documentation"],
            "sometimes": ["security"],
        },
        "data-layer": {
            "always": ["security", "testing", "unidirectional_data_flow"],
            "usually": ["minimal_dependencies", "zero_build_warnings"],
            "sometimes": ["documentation"],
        },
    }

    return component_mappings.get(component_type, component_mappings["ui"])
