#!/usr/bin/env python3
"""
Engineering Principles CLI - Generate custom prompts for AI workflows

Usage examples:
    python principles_cli.py review --platform web --focus security,accessibility
    python principles_cli.py generate --platform android --component ui
    python principles_cli.py architecture --platform web --layer data
    python principles_cli.py dependencies --platform ios --check react-native
"""

import argparse
import yaml
import sys
from pathlib import Path
from typing import Dict, List, Any

class PrinciplesCLI:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.core_path = self.base_path / "core"
        self.modules_path = self.base_path / "modules"
        
    def load_yaml(self, file_path: Path) -> Dict[str, Any]:
        """Load YAML file safely"""
        try:
            with open(file_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Error: File not found: {file_path}")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {e}")
            sys.exit(1)
    
    def format_principles(self, principles: Dict[str, Any], focus_areas: List[str] = None) -> str:
        """Format principles for prompt inclusion"""
        output = []
        
        # Add priority order
        output.append("**Priority Order:** Security > Accessibility > Testing > Performance > Code Style\n")
        
        # Handle case where principles might be a list or different structure
        if not isinstance(principles, dict):
            output.append("**Principles:** Unable to parse principles structure")
            return "\n".join(output)
        
        # Filter principles if focus areas specified
        if focus_areas:
            filtered_principles = {k: v for k, v in principles.items() if k in focus_areas}
        else:
            filtered_principles = principles
        
        for name, principle in filtered_principles.items():
            if not isinstance(principle, dict):
                continue
                
            output.append(f"### {name.title()}")
            output.append(f"**Why:** {principle.get('why', 'No description')}")
            
            if 'how' in principle:
                output.append("**How:**")
                how_items = principle['how']
                if isinstance(how_items, list):
                    for item in how_items:
                        output.append(f"- {item}")
                else:
                    output.append(f"- {how_items}")
            
            if 'enforcement' in principle:
                enforcement = principle['enforcement']
                if isinstance(enforcement, dict):
                    output.append("**Enforcement:**")
                    for key, value in enforcement.items():
                        output.append(f"- {key}: {value}")
                else:
                    output.append(f"**Enforcement:** {enforcement}")
            
            output.append("")
        
        return "\n".join(output)
    
    def format_platform_requirements(self, platform_config: Dict[str, Any]) -> str:
        """Format platform-specific requirements"""
        output = []
        
        if 'requirements' in platform_config:
            output.append("**Requirements:**")
            for req in platform_config['requirements']:
                output.append(f"- {req}")
            output.append("")
        
        if 'approved_dependencies' in platform_config:
            output.append("**Approved Dependencies:**")
            for dep in platform_config['approved_dependencies']:
                output.append(f"- {dep}")
            output.append("")
        
        if 'tools' in platform_config:
            output.append("**Required Tools:**")
            for tool in platform_config['tools']:
                output.append(f"- {tool}")
            output.append("")
        
        return "\n".join(output)
    
    def format_detection_rules(self, rules: Dict[str, Any]) -> str:
        """Format detection rules for prompt inclusion"""
        output = []
        
        for category, category_rules in rules.items():
            output.append(f"### {category.title()} Rules")
            
            if 'rules' in category_rules:
                for rule in category_rules['rules']:
                    output.append(f"**{rule['name']}** (Severity: {rule['severity']})")
                    output.append(f"- {rule['description']}")
                    
                    if 'patterns' in rule:
                        output.append("- Detection patterns:")
                        for pattern in rule['patterns'][:3]:  # Show first 3 patterns
                            output.append(f"  - `{pattern}`")
                    
                    if 'fix_suggestions' in rule:
                        output.append(f"- Fix: {rule['fix_suggestions'].get('description', 'No fix info')}")
                    
                    output.append("")
            
            output.append("")
        
        return "\n".join(output)
    
    def generate_review_prompt(self, platform: str, focus_areas: List[str]) -> str:
        """Generate code review prompt"""
        # Load data
        principles_data = self.load_yaml(self.core_path / "principles.yaml")
        principles = principles_data.get('principles', principles_data)  # Handle nested structure
        platforms_data = self.load_yaml(self.core_path / "platforms.yaml")
        platforms = platforms_data.get('platforms', platforms_data)  # Handle nested structure
        severity_data = self.load_yaml(self.modules_path / "detection" / "severity.yaml")
        severity = severity_data.get('severity_levels', severity_data)  # Handle nested structure
        
        # Load detection rules for focus areas
        rules = {}
        for area in focus_areas:
            rule_file = self.modules_path / "detection" / "rules" / f"{area}.yaml"
            if rule_file.exists():
                rule_data = self.load_yaml(rule_file)
                rules[area] = rule_data.get('rules', rule_data)  # Handle nested structure
        
        # Generate prompt
        prompt = f"""# Code Review Assistant for {platform.title()}

You are an expert code reviewer for Livefront's engineering standards. Review code against these principles and provide actionable feedback.

## Core Principles

{self.format_principles(principles, focus_areas)}

## Platform Requirements ({platform.title()})

{self.format_platform_requirements(platforms.get(platform, {}))}

## Detection Rules

{self.format_detection_rules(rules)}

## Severity Levels

- **Critical**: {', '.join(severity.get('critical', []))} - Blocks merge immediately
- **Blocking**: {', '.join(severity.get('blocking', []))} - Must fix before merge
- **Required**: {', '.join(severity.get('required', []))} - Should fix before merge
- **Recommended**: {', '.join(severity.get('recommended', []))} - Improve when possible

## Instructions

When reviewing code:

1. **Identify violations** of the above principles
2. **Classify severity** using the levels above
3. **Provide specific fixes** with before/after examples
4. **Explain the reasoning** behind each principle
5. **Focus especially on**: {', '.join(focus_areas)}

Be constructive and educational in your feedback. Help developers understand not just what to fix, but why it matters for code quality and user experience.
"""
        
        return prompt
    
    def generate_code_prompt(self, platform: str, component_type: str) -> str:
        """Generate code writing prompt"""
        # Load data
        principles_data = self.load_yaml(self.core_path / "principles.yaml")
        principles = principles_data.get('principles', principles_data)  # Handle nested structure
        philosophy = self.load_yaml(self.core_path / "philosophy.yaml")
        platforms_data = self.load_yaml(self.core_path / "platforms.yaml")
        platforms = platforms_data.get('platforms', platforms_data)  # Handle nested structure
        
        # Load generation guidance
        guidance_file = self.modules_path / "generation" / "guidance.yaml"
        if guidance_file.exists():
            guidance = self.load_yaml(guidance_file)
        else:
            guidance = {}
        
        prompt = f"""# Code Generation Assistant for {platform.title()} {component_type.title()}

You are an expert developer creating high-quality code that follows Livefront's engineering principles.

## Core Philosophy

{philosophy.get('description', 'Build excellent software that users love.')}

**Values:**
{chr(10).join(f"- {value}" for value in philosophy.get('values', []))}

## Engineering Principles

{self.format_principles(principles)}

## Platform Requirements ({platform.title()})

{self.format_platform_requirements(platforms.get(platform, {}))}

## Code Generation Guidelines

When writing {component_type} code:

1. **Security First**: Use HTTPS, encrypt sensitive data, no secrets in code
2. **Accessibility**: Include ARIA labels, proper contrast, keyboard navigation
3. **Testing**: Write testable code, aim for 80% coverage on business logic
4. **Performance**: Optimize for the target platform and device capabilities
5. **Documentation**: Comment complex logic, document public APIs

## Component-Specific Guidance

### {component_type.title()} Components

- Follow unidirectional data flow patterns
- Handle loading, error, and success states
- Include proper TypeScript/type annotations
- Use approved dependencies only
- Follow platform naming conventions

## Instructions

Generate code that:
- Follows all engineering principles above
- Is production-ready and maintainable
- Includes appropriate tests
- Has proper error handling
- Follows platform conventions
- Is accessible to all users

Always explain your architectural decisions and how they align with the principles.
"""
        
        return prompt
    
    def generate_architecture_prompt(self, platform: str, layer: str) -> str:
        """Generate architecture guidance prompt"""
        principles_data = self.load_yaml(self.core_path / "principles.yaml")
        principles = principles_data.get('principles', principles_data)  # Handle nested structure
        platforms_data = self.load_yaml(self.core_path / "platforms.yaml")
        platforms = platforms_data.get('platforms', platforms_data)  # Handle nested structure
        
        prompt = f"""# Architecture Assistant for {platform.title()} {layer.title()} Layer

You are an expert software architect helping design systems that follow Livefront's engineering principles.

## Architectural Principles

{self.format_principles(principles, ['unidirectional_data_flow', 'minimal_dependencies', 'testing'])}

## Platform Requirements ({platform.title()})

{self.format_platform_requirements(platforms.get(platform, {}))}

## {layer.title()} Layer Guidelines

### Key Responsibilities
- Data flow management
- State consistency
- Error handling
- Performance optimization

### Design Patterns
- Use unidirectional data flow
- Implement proper separation of concerns
- Ensure testability at every level
- Plan for scalability and maintainability

## Instructions

When designing {layer} layer architecture:

1. **Follow unidirectional data flow** - Data flows down, events flow up
2. **Minimize dependencies** - Use approved libraries only
3. **Design for testing** - Every component should be testable
4. **Plan for errors** - Handle all failure modes gracefully
5. **Document decisions** - Explain architectural choices

Provide specific recommendations for structure, patterns, and implementation approaches.
"""
        
        return prompt
    
    def generate_dependency_prompt(self, platform: str, dependencies: List[str]) -> str:
        """Generate dependency evaluation prompt"""
        principles_data = self.load_yaml(self.core_path / "principles.yaml")
        principles = principles_data.get('principles', principles_data)  # Handle nested structure
        platforms_data = self.load_yaml(self.core_path / "platforms.yaml")
        platforms = platforms_data.get('platforms', platforms_data)  # Handle nested structure
        
        platform_config = platforms.get(platform, {})
        approved_deps = platform_config.get('approved_dependencies', [])
        
        prompt = f"""# Dependency Evaluation for {platform.title()}

You are evaluating whether these dependencies should be approved for use in {platform} projects.

## Dependencies to Evaluate
{chr(10).join(f"- {dep}" for dep in dependencies)}

## Current Approved Dependencies
{chr(10).join(f"- {dep}" for dep in approved_deps)}

## Evaluation Criteria

### Security
- No known vulnerabilities
- Regular security updates
- Trustworthy maintainers

### Maintenance
- Active development
- Regular releases
- Responsive to issues

### Alignment
- Fits our architecture patterns
- Compatible with existing stack
- Doesn't duplicate functionality

### Impact
- Bundle size impact
- Performance implications
- Learning curve for team

## Minimal Dependencies Principle

{principles.get('minimal_dependencies', {}).get('description', 'Minimize external dependencies')}

## Instructions

For each dependency, provide:

1. **Recommendation**: Approve, Reject, or Conditional
2. **Justification**: Why this decision aligns with our principles
3. **Alternatives**: Could we build this ourselves or use existing approved deps?
4. **Implementation**: If approved, how should it be integrated?
5. **Documentation**: What needs to be documented in our README?

Remember: We prefer building ourselves over external dependencies when reasonable.
"""
        
        return prompt

def main():
    cli = PrinciplesCLI()
    
    parser = argparse.ArgumentParser(
        description="Generate custom AI prompts for engineering principles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s review --platform web --focus security,accessibility
  %(prog)s generate --platform android --component ui
  %(prog)s architecture --platform web --layer data
  %(prog)s dependencies --platform ios --check react-native,lodash
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Review command
    review_parser = subparsers.add_parser('review', help='Generate code review prompt')
    review_parser.add_argument('--platform', choices=['android', 'ios', 'web'], required=True)
    review_parser.add_argument('--focus', default='security,accessibility,testing', 
                              help='Comma-separated focus areas')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate code writing prompt')
    generate_parser.add_argument('--platform', choices=['android', 'ios', 'web'], required=True)
    generate_parser.add_argument('--component', default='ui', 
                               help='Component type (ui, business, data)')
    
    # Architecture command
    arch_parser = subparsers.add_parser('architecture', help='Generate architecture guidance prompt')
    arch_parser.add_argument('--platform', choices=['android', 'ios', 'web'], required=True)
    arch_parser.add_argument('--layer', default='data', 
                           help='Architecture layer (ui, business, data)')
    
    # Dependencies command
    deps_parser = subparsers.add_parser('dependencies', help='Generate dependency evaluation prompt')
    deps_parser.add_argument('--platform', choices=['android', 'ios', 'web'], required=True)
    deps_parser.add_argument('--check', required=True, 
                           help='Comma-separated list of dependencies to evaluate')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'review':
            focus_areas = args.focus.split(',')
            prompt = cli.generate_review_prompt(args.platform, focus_areas)
        elif args.command == 'generate':
            prompt = cli.generate_code_prompt(args.platform, args.component)
        elif args.command == 'architecture':
            prompt = cli.generate_architecture_prompt(args.platform, args.layer)
        elif args.command == 'dependencies':
            dependencies = args.check.split(',')
            prompt = cli.generate_dependency_prompt(args.platform, dependencies)
        
        print(prompt)
        
    except Exception as e:
        print(f"Error generating prompt: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()