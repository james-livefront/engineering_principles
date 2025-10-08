#!/usr/bin/env python3
"""Generate prompts for engineering standards"""

import argparse
import sys
from typing import Any

from leap import LeapLoader
from leap.filters import filter_principles_by_focus, map_focus_areas_to_enforcement_stages


class PrinciplesCLI:
    def __init__(self) -> None:
        self.loader = LeapLoader()

    def format_principles(
        self, principles: dict[str, Any], focus_areas: list[str] | None = None
    ) -> str:
        """Format principles for prompt"""
        output = []
        priority_text = "Security > Accessibility > Testing > Performance > Code Style"
        output.append(f"**Priority Order:** {priority_text}\n")

        if not isinstance(principles, dict):
            output.append("**Principles:** Unable to parse principles structure")
            return "\n".join(output)

        if focus_areas:
            if all(area in principles for area in focus_areas):
                filtered_principles = {k: v for k, v in principles.items() if k in focus_areas}
            else:
                filtered_principles = filter_principles_by_focus(principles, focus_areas)
        else:
            filtered_principles = principles

        for name, principle in filtered_principles.items():
            if not isinstance(principle, dict):
                continue

            output.append(f"### {name.title()}")
            output.append(f"**Why:** {principle.get('why', 'No description')}")

            if "how" in principle:
                output.append("**How:**")
                how_items = principle["how"]
                if isinstance(how_items, list):
                    for item in how_items:
                        output.append(f"- {item}")
                else:
                    output.append(f"- {how_items}")

            output.append("")

        return "\n".join(output)

    def format_platform_requirements(self, platform_config: dict[str, Any]) -> str:
        """Format platform-specific requirements"""
        output = []

        if "requirements" in platform_config:
            output.append("**Requirements:**")
            for req in platform_config["requirements"]:
                output.append(f"- {req}")
            output.append("")

        if "approved_dependencies" in platform_config:
            output.append("**Approved Dependencies:**")
            for category, deps in platform_config["approved_dependencies"].items():
                if isinstance(deps, list):
                    for dep_info in deps:
                        if isinstance(dep_info, dict) and "name" in dep_info:
                            purpose = dep_info.get("purpose", "")
                            version = dep_info.get("version", "")
                            desc = f" - {purpose}" if purpose else ""
                            ver = f" v{version}" if version else ""
                            output.append(f"- {dep_info['name']}{ver}{desc} ({category})")
                        else:
                            output.append(f"- {dep_info} ({category})")
            output.append("")

        if "tools" in platform_config:
            output.append("**Required Tools:**")
            for category, tools in platform_config["tools"].items():
                if isinstance(tools, list):
                    for tool in tools:
                        output.append(f"- {tool} ({category})")
                else:
                    output.append(f"- {tools} ({category})")

        return "\n".join(output)

    def format_detection_rules(self, rules: dict[str, Any]) -> str:
        """Format detection rules for prompt inclusion"""
        output = []

        for category, category_rules in rules.items():
            output.append(f"### {category.title()} Rules")

            if isinstance(category_rules, dict) and "rules" in category_rules:
                actual_rules = category_rules["rules"]
            else:
                actual_rules = category_rules

            if isinstance(actual_rules, dict):
                for rule_name, rule_data in actual_rules.items():
                    if isinstance(rule_data, dict):
                        severity = rule_data.get("severity", "unknown")
                        description = rule_data.get("description", "No description")

                        output.append(
                            f"**{rule_name.replace('_', ' ').title()}** (Severity: {severity})"
                        )
                        output.append(f"- {description}")

                        patterns_to_show = []

                        if "patterns" in rule_data:
                            patterns = rule_data["patterns"]
                            if isinstance(patterns, list):
                                patterns_to_show.extend(patterns)
                            elif isinstance(patterns, dict):
                                for _pattern_name, pattern_data in patterns.items():
                                    if isinstance(pattern_data, dict) and "regex" in pattern_data:
                                        patterns_to_show.append(pattern_data)

                        for platform_key in [
                            "android_patterns",
                            "ios_patterns",
                            "web_patterns",
                            "patterns",
                        ]:
                            if platform_key in rule_data and isinstance(
                                rule_data[platform_key], dict
                            ):
                                for _pattern_name, pattern_data in rule_data[platform_key].items():
                                    if isinstance(pattern_data, dict) and "regex" in pattern_data:
                                        patterns_to_show.append(pattern_data)

                        if patterns_to_show:
                            output.append("- Detection patterns:")
                            for pattern in patterns_to_show[:3]:
                                if isinstance(pattern, dict) and "regex" in pattern:
                                    output.append(f"  - `{pattern['regex']}`")
                                    if "message" in pattern:
                                        output.append(f"    - {pattern['message']}")
                                else:
                                    output.append(f"  - `{pattern}`")

                        output.append("")

            output.append("")

        return "\n".join(output)

    def format_severity_levels(self, severity: dict[str, Any]) -> str:
        """Format severity levels for prompt inclusion"""
        output = []

        severity_order = ["critical", "blocking", "required", "recommended"]

        for level in severity_order:
            if level in severity:
                level_data = severity[level]
                if isinstance(level_data, dict):
                    description = level_data.get("description", f"{level.title()} violations")
                    action = level_data.get("action", "See documentation")
                    llm_instructions = level_data.get("llm_instructions", "")
                    examples = level_data.get("examples", [])

                    output.append(f"- **{level.title()}**: {description}")
                    output.append(f"  - Action: {action}")

                    if llm_instructions:
                        output.append(f"  - AI Guidance: {llm_instructions}")

                    if examples:
                        output.append("  - Examples:")
                        for example in examples[:3]:
                            output.append(f"    - {example}")
                else:
                    output.append(f"- **{level.title()}**: {level_data}")

        return "\n".join(output)

    def generate_review_prompt(self, platform: str, focus_areas: list[str]) -> str:
        """Generate code review prompt"""

        platform_title = self.loader.get_platform_title(platform)

        severity_file = self.loader.modules_path / "detection" / "severity.yaml"
        severity_data = self.loader.load_yaml(severity_file)
        severity_levels = severity_data.get("severity_levels", severity_data)

        detection_sections = []
        for area in focus_areas:
            rules = self._load_detection_rules(area, platform)
            if rules:
                detection_sections.append(self._format_focused_detection(area, rules))

        enforcement_section = self._format_enforcement_context(focus_areas)

        severity_section = self.format_severity_levels(severity_levels)

        prompt = f"""<!-- PROMPT_METADATA
platform: {platform}
focus: {",".join(focus_areas)}
mode: review
-->

# Code Review Assistant for {platform_title}

Review code against standards. **Priority**: Security > Accessibility > Testing.

{chr(10).join(detection_sections)}

## Severity Levels

{severity_section}

## What Happens Next: Automated CI Checks

After your review, the following automated checks will run:

{enforcement_section}

## Instructions

1. **Start by identifying violations** using the patterns above, then find others
2. **Classify severity**: Critical → Blocking → Required → Recommended
3. **Provide specific fixes** with before/after examples
4. **Focus on**: {", ".join(focus_areas)}
"""
        return prompt

    def _format_philosophy(self, philosophy: dict[str, Any]) -> str:
        """Format philosophy for prompt inclusion"""
        output = []

        if "mantras" in philosophy:
            output.append("**Mantras**:")
            for mantra in philosophy["mantras"]:
                principle = mantra.get("principle", "")
                explanation = mantra.get("explanation", "")
                if principle:
                    output.append(f"- *{principle}* - {explanation}")
            output.append("")

        if "core_values" in philosophy:
            values_list = []
            for category, values in philosophy["core_values"].items():
                if isinstance(values, list) and values:
                    values_list.append(f"{category.title()}: {values[0]}")
            if values_list:
                output.append(f"**Values**: {', '.join(values_list)}")
                output.append("")

        return "\n".join(output)

    def _format_enforcement_context(self, focus_areas: list[str]) -> str:
        """Format enforcement context showing what CI will check"""
        output = []

        enforcement = self.loader.load_enforcement()
        ci_pipeline = enforcement.get("enforcement_tools", {}).get("ci_pipeline", {})
        stages = ci_pipeline.get("stages", [])

        relevant_stages = map_focus_areas_to_enforcement_stages(focus_areas)

        for stage in stages:
            stage_name = stage.get("name", "")
            if stage_name in relevant_stages:
                checks = stage.get("checks", [])
                if checks:
                    output.append(f"**{stage_name.title()} Stage**:")
                    for check in checks[:3]:
                        output.append(f"- {check}")
                    output.append("")

        return "\n".join(output)

    def _format_generation_guidance(
        self, guidance: dict[str, Any], component_type: str, platform: str
    ) -> str:
        """Format generation guidance from YAML"""
        output = []

        component_map = {
            "ui": ["accessibility", "architecture"],
            "business-logic": ["testing", "architecture"],
            "data-layer": ["security", "architecture"],
        }

        focus_areas = component_map.get(component_type, ["architecture"])

        principle_guidance = guidance.get("principle_guidance", {})
        for area in focus_areas:
            if area in principle_guidance:
                area_data = principle_guidance[area]
                output.append(f"### {area.title()}")

                if "approach" in area_data:
                    output.append(f"**Approach**: {area_data['approach']}")
                    output.append("")

                if platform in area_data:
                    platform_data = area_data[platform]
                    if "always" in platform_data:
                        output.append("**Always**:")
                        for item in platform_data["always"]:
                            output.append(f"- {item}")
                        output.append("")

                    if "never" in platform_data:
                        output.append("**Never**:")
                        for item in platform_data["never"]:
                            output.append(f"- {item}")
                        output.append("")

        common_mistakes = guidance.get("common_mistakes", {})
        if focus_areas and common_mistakes:
            output.append("### Common Mistakes to Avoid")
            for area in focus_areas:
                if area in common_mistakes:
                    for mistake in common_mistakes[area][:3]:  # Top 3
                        output.append(f"- {mistake}")
            output.append("")

        return "\n".join(output)

    def generate_code_prompt(self, platform: str, component_type: str) -> str:
        """Generate code writing prompt"""
        principles, platform_title, platform_config = self.loader.get_common_prompt_data(platform)
        philosophy_data = self.loader.load_philosophy()

        guidance_file = self.loader.modules_path / "generation" / "guidance.yaml"
        guidance = {}
        if guidance_file.exists():
            guidance = self.loader.load_yaml(guidance_file)

        component_to_principles = {
            "ui": ["accessibility", "code_consistency"],
            "business-logic": ["testing", "unidirectional_data_flow"],
            "data-layer": ["security", "minimal_dependencies"],
        }

        focus_principles = component_to_principles.get(component_type, ["code_consistency"])

        philosophy_section = self._format_philosophy(philosophy_data)
        principles_section = self.format_principles(principles, focus_principles)
        platform_section = self.format_platform_requirements(platform_config)
        guidance_section = self._format_generation_guidance(guidance, component_type, platform)

        prompt = f"""<!-- PROMPT_METADATA
platform: {platform}
component: {component_type}
mode: generate
-->

# Code Generation for {platform_title} {component_type.title()}

Generate production-ready code following Livefront engineering standards.

## Livefront Engineering Culture

{philosophy_section}

## Engineering Principles

{principles_section}

## Platform Requirements ({platform_title})

{platform_section}

## {component_type.title()} Guidance

{guidance_section}

## Instructions

1. Follow platform conventions and patterns shown above
2. Apply security, accessibility, and testing standards from principles
3. Include error handling, loading states, and edge cases
4. Write testable, maintainable code with clear separation of concerns
5. Match existing code style and architecture patterns
"""
        return prompt

    def generate_dependency_prompt(self, platform: str, dependencies: list[str]) -> str:
        """Generate dependency evaluation prompt"""
        principles, platform_title, platform_config = self.loader.get_common_prompt_data(platform)
        approved_deps_config = platform_config.get("approved_dependencies", {})

        approved_deps = []
        dependency_details = {}
        for _category, deps in approved_deps_config.items():
            if isinstance(deps, list):
                for dep_info in deps:
                    if isinstance(dep_info, dict) and "name" in dep_info:
                        dep_name = dep_info["name"]
                        approved_deps.append(dep_name)
                        dependency_details[dep_name.lower()] = dep_info

        dependency_status = []
        for dep in dependencies:
            dep_lower = dep.lower()
            is_approved = any(dep_lower in approved_name.lower() for approved_name in approved_deps)
            status = "✅ APPROVED" if is_approved else "❌ NOT APPROVED"
            dependency_status.append(f"- {dep} - {status}")

            if is_approved:
                for approved_name, details in dependency_details.items():
                    if dep_lower in approved_name.lower():
                        dependency_status.append(
                            f"  - Purpose: {details.get('purpose', 'Not specified')}"
                        )
                        dependency_status.append(
                            f"  - Version: {details.get('version', 'Not specified')}"
                        )
                        break

        minimal_deps_principle = principles.get("minimal_dependencies", {})
        minimal_deps_why = minimal_deps_principle.get(
            "why", "We're responsible for maintaining every single line of code we ship"
        )

        prompt = f"""<!-- PROMPT_METADATA
platform: {platform}
dependencies: {",".join(dependencies)}
mode: dependencies
-->

# Dependency Evaluation for {platform_title}

Evaluate dependencies against Livefront's standards. **Principle**: {minimal_deps_why}

## Dependency Status Check
{chr(10).join(dependency_status)}

## Approved Dependencies for {platform_title}
{chr(10).join(f"- {dep}" for dep in approved_deps)}

## Evaluation Criteria
- **Security**: No vulnerabilities, regular updates, trustworthy maintainers
- **Maintenance**: Active development, responsive to issues
- **Alignment**: Fits architecture, compatible with stack, no duplication
- **Impact**: Bundle size, performance, team learning curve

## Instructions

For each dependency, provide:
1. **Security Assessment**: Known vulnerabilities, maintenance status
2. **Alignment Analysis**: Architectural fit, duplication with existing code
3. **Recommendation**: ✅ APPROVE, 🤔 REVIEW, or ❌ REJECT with rationale
"""
        return prompt

    def generate_architecture_prompt(self, platform: str, layer: str) -> str:
        """Generate architecture guidance prompt"""
        principles, platform_title, platform_config = self.loader.get_common_prompt_data(platform)

        arch_principles = self._format_focused_architecture(
            principles, ["unidirectional_data_flow", "minimal_dependencies", "testing"]
        )

        platform_reqs = self._format_concise_platform(platform_config, platform_title)

        prompt = f"""<!-- PROMPT_METADATA
platform: {platform}
layer: {layer}
mode: architecture
-->

# Architecture Assistant for {platform_title} {layer.title()} Layer

Design systems following Livefront's architecture standards. **Priority**: Security > Testing.

{arch_principles}

{platform_reqs}

## {layer.title()} Layer Guidelines
- **Data Flow**: Unidirectional (data down, events up)
- **State**: Views display state, never modify it
- **Testing**: 80% coverage on business logic, testable architecture
- **Dependencies**: Approved libraries only, document purpose/license

## Instructions

Design architecture that:
1. **Follows unidirectional data flow**
2. **Minimizes and justifies dependencies**
3. **Enables comprehensive testing**
4. **Handles all error states gracefully**

Ask clarifying questions if you need more context to make a thorough evaluation.

Provide specific structure and implementation recommendations.
"""

        return prompt

    def _format_focused_detection(self, area: str, rules: dict[str, Any]) -> str:
        """Format focused detection patterns for a specific area"""
        output = [f"## {area.title()} Detection"]

        severity_order = {"critical": 0, "blocking": 1, "required": 2, "recommended": 3}

        try:
            if isinstance(rules, dict):
                sorted_rules = sorted(
                    rules.items(),
                    key=lambda x: (
                        severity_order.get(x[1].get("severity", "unknown"), 999)
                        if isinstance(x[1], dict)
                        else 999
                    ),
                )
            elif isinstance(rules, list):
                sorted_rules = [(f"rule_{i}", rule) for i, rule in enumerate(rules)]
            else:
                sorted_rules = []
        except Exception as e:
            print(f"ERROR in _format_focused_detection: {e}")
            print(f"area={area}, rules type={type(rules)}")
            raise

        for rule_name, rule_data in sorted_rules:
            if not isinstance(rule_data, dict):
                continue

            severity = rule_data.get("severity", "unknown")
            description = rule_data.get("description", "")

            output.append(
                f"- **{rule_name.replace('_', ' ').title()}** ({severity.title()}): {description}"
            )

            patterns = rule_data.get("patterns", [])
            if isinstance(patterns, list):
                for pattern_data in patterns:
                    if isinstance(pattern_data, dict) and "regex" in pattern_data:
                        regex = pattern_data["regex"]
                        message = pattern_data.get("message", "")
                        output.append(f"  - `{regex}` → {message}")
            elif isinstance(patterns, dict):
                for pattern_name, pattern_data in patterns.items():
                    if isinstance(pattern_data, dict) and "regex" in pattern_data:
                        regex = pattern_data["regex"]
                        message = pattern_data.get("message", "")
                        output.append(f"  - `{regex}` → {message}")
                    elif isinstance(pattern_data, dict) and "message" in pattern_data:
                        # Handle patterns that don't have regex but have message
                        message = pattern_data.get("message", "")
                        output.append(f"  - {pattern_name.replace('_', ' ').title()}: {message}")

        return "\n".join(output)

    def _load_detection_rules(self, area: str, platform: str | None = None) -> dict[str, Any]:
        """Load detection rules from YAML files"""
        detection_file = self.loader.modules_path / "detection" / "rules" / f"{area}.yaml"

        if not detection_file.exists():
            return {}

        detection_data = self.loader.load_yaml(detection_file)
        rules = detection_data.get("rules", {})

        if platform:
            filtered_rules = {}
            for rule_name, rule_data in rules.items():
                if not isinstance(rule_data, dict):
                    continue

                filtered_rule = rule_data.copy()

                platform_patterns = rule_data.get(f"{platform}_patterns", [])
                if platform_patterns:
                    if "patterns" not in filtered_rule:
                        filtered_rule["patterns"] = []
                    elif not isinstance(filtered_rule["patterns"], list):
                        filtered_rule["patterns"] = []

                    if isinstance(platform_patterns, list):
                        for pattern_data in platform_patterns:
                            if isinstance(pattern_data, dict):
                                filtered_rule["patterns"].append(pattern_data)
                    elif isinstance(platform_patterns, dict):
                        for _pattern_name, pattern_data in platform_patterns.items():
                            if isinstance(pattern_data, dict):
                                filtered_rule["patterns"].append(pattern_data)

                filtered_rules[rule_name] = filtered_rule

            return filtered_rules

        return dict(rules)

    def _format_concise_platform(self, platform_config: dict[str, Any], platform_title: str) -> str:
        """Format concise platform requirements"""
        output = [f"## Platform Requirements ({platform_title})"]

        if "approved_dependencies" in platform_config:
            deps_by_category = {}
            for category, dep_list in platform_config["approved_dependencies"].items():
                if isinstance(dep_list, list):
                    category_deps = []
                    for dep in dep_list:
                        if isinstance(dep, dict) and "name" in dep:
                            category_deps.append(dep["name"])
                        else:
                            category_deps.append(str(dep))
                    if category_deps:
                        deps_by_category[category] = category_deps

            for category, deps in deps_by_category.items():
                output.append(f"- **{category.title()}**: {', '.join(deps)}")

        if "tools" in platform_config:
            tools_by_category = {}
            for category, tool_list in platform_config["tools"].items():
                if isinstance(tool_list, list):
                    tools_by_category[category] = tool_list
                else:
                    tools_by_category[category] = [tool_list]

            for category, tools in tools_by_category.items():
                output.append(f"- **{category.title()}**: {', '.join(tools)}")

        return "\n".join(output)

    def _format_focused_architecture(
        self, principles: dict[str, Any], focus_principles: list[str]
    ) -> str:
        """Format focused architecture principles"""
        output = ["## Architecture Principles"]

        for principle_name in focus_principles:
            if principle_name not in principles:
                continue

            principle = principles[principle_name]
            if not isinstance(principle, dict):
                continue

            why = principle.get("why", "")
            how = principle.get("how", "")

            display_name = (
                principle_name.replace("_", " ").title().replace("Data Flow", "Data_Flow")
            )
            output.append(f"- **{display_name}**: {why}")

            if isinstance(how, list):
                key_points = [point.strip("- ") for point in how if point.strip()]
                if key_points:
                    if len(key_points) <= 3:
                        output.append(f"  - {' • '.join(key_points)}")
                    else:
                        output.append(f"  - {' • '.join(key_points[:3])}")
            elif isinstance(how, str) and how:
                first_sentence = how.split(".")[0]
                if first_sentence:
                    output.append(f"  - {first_sentence}")

        return "\n".join(output)


def main() -> None:
    cli = PrinciplesCLI()

    parser = argparse.ArgumentParser(
        description="Generate prompts for engineering standards",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    review_parser = subparsers.add_parser("review", help="Generate review prompt")
    review_parser.add_argument("--platform", choices=["android", "ios", "web"], required=True)
    review_parser.add_argument("--focus", default="security,accessibility,testing")
    review_parser.add_argument(
        "--enhanced", action="store_true", help="Enhance with LLM (requires OPENAI_API_KEY)"
    )

    generate_parser = subparsers.add_parser("generate", help="Generate code prompt")
    generate_parser.add_argument("--platform", choices=["android", "ios", "web"], required=True)
    generate_parser.add_argument("--component", default="ui")
    generate_parser.add_argument(
        "--enhanced", action="store_true", help="Enhance with LLM (requires OPENAI_API_KEY)"
    )

    architecture_parser = subparsers.add_parser("architecture", help="Generate architecture prompt")
    architecture_parser.add_argument("--platform", choices=["android", "ios", "web"], required=True)
    architecture_parser.add_argument(
        "--layer", choices=["data", "ui", "business-logic"], default="data"
    )

    dependency_parser = subparsers.add_parser("dependencies", help="Evaluate dependencies")
    dependency_parser.add_argument("--platform", choices=["android", "ios", "web"], required=True)
    dependency_parser.add_argument("dependencies", nargs="+", help="Dependencies to evaluate")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == "review":
            focus_areas = args.focus.split(",")
            prompt = cli.generate_review_prompt(args.platform, focus_areas)
        elif args.command == "generate":
            prompt = cli.generate_code_prompt(args.platform, args.component)
        elif args.command == "architecture":
            prompt = cli.generate_architecture_prompt(args.platform, args.layer)
        elif args.command == "dependencies":
            prompt = cli.generate_dependency_prompt(args.platform, args.dependencies)
        else:
            parser.print_help()
            return

        # Apply enhancement if requested
        if hasattr(args, "enhanced") and args.enhanced:
            from leap.prompt_enhancer import enhance_prompt_with_llm, get_openai_evaluator

            evaluator = get_openai_evaluator()
            if evaluator is not None:
                prompt = enhance_prompt_with_llm(prompt, evaluator)  # type: ignore[arg-type]
            else:
                print(
                    "⚠️ Enhancement skipped: OPENAI_API_KEY not set or openai package not installed",
                    file=sys.stderr,
                )
                print("   Set API key: export OPENAI_API_KEY='sk-...'", file=sys.stderr)
                print("   Install package: uv add openai", file=sys.stderr)

        print(prompt)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
