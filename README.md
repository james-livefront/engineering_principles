# Livefront Engineering Principles

A modular system for encoding and enforcing Livefront's engineering principles through AI-powered code detection and generation.

## Philosophy

> "Livefront Engineers are craftspeople."

We give a damn about building software that is reliable, performant, maintainable, and remarkably fun to use.

**Core Mantras:**

- **We don't defer work**: If it can be done now, do it now. Otherwise, create a ticket.
- **The design is the spec**: We deliver working software that fulfills the vision laid out in the designs.

## Quick Start

```bash
# Clone and navigate to the repository
git clone <repo-url>
cd engineering_principles

# Generate a code review prompt for web platform focusing on security
python principles_cli.py review --platform web --focus security

# Generate a code writing prompt for Android UI components
python principles_cli.py generate --platform android --component ui

# Generate architecture guidance for iOS data layer
python principles_cli.py architecture --platform ios --layer data

# Evaluate dependencies for web platform
python principles_cli.py dependencies --platform web --check react,lodash
```

## System Architecture

This modular system separates core knowledge from implementation details:

```
engineering_principles/
├── core/                    # Shared knowledge base
│   ├── philosophy.yaml      # Core values and mantras
│   ├── principles.yaml      # All 15 engineering principles
│   ├── platforms.yaml       # Platform-specific configurations
│   └── enforcement.yaml     # How principles are enforced
│
├── modules/
│   ├── detection/          # For code review and analysis
│   │   ├── rules/          # Detection patterns by principle
│   │   ├── severity.yaml   # Issue severity mappings
│   │   └── context.yaml    # Context identification rules
│   │
│   └── generation/         # For code creation
│       ├── examples/       # Positive pattern examples
│       └── guidance.yaml   # Implementation guidance
│
├── evals/                  # Evaluation datasets
│   ├── detection/          # Test cases for detection
│   └── generation/         # Test cases for generation
│
├── principles_cli.py       # Command-line interface
├── eval_runner.py          # Evaluation framework for testing prompts
└── CLI_REFERENCE.md        # Quick command reference
```

**Key Features:**

- **Modular Design**: Core philosophy separate from implementation
- **Platform-Aware**: Android, iOS, and Web-specific guidance
- **Context-Sensitive**: Different rules for UI vs business logic vs data layer
- **Severity-Based**: Critical, Blocking, Required, Recommended, Informational
- **AI-Powered**: Generates prompts for AI code review and generation

## Engineering Principles

**Priority Order:** Security > Accessibility > Testing > Performance > Code Style

### The 15 Core Principles

1. **Accessibility** - Equal access regardless of ability or disability
2. **Code Consistency** - Consistent style across platforms and teams
3. **Zero TODOs** - Track work outside source code via tickets
4. **Security** - HTTPS everywhere, no secrets in source control
5. **Unidirectional Data Flow** - Predictable state management patterns
6. **Testing** - 80% minimum coverage on business logic
7. **Flexible Layout** - Support all screen sizes and orientations
8. **Continuous Integration** - Automated quality checks and deployment
9. **Code Reviews** - Every line peer-reviewed before merge
10. **Zero Build Warnings** - Clean build output with no warnings
11. **Design Integrity** - Match designs exactly as specified
12. **Localization** - Support any locale and language
13. **Minimal Dependencies** - Reduce third-party risk and complexity
14. **Compatibility** - Document and support required versions
15. **Documentation** - README with setup, build, test, and release info

### Enforcement Levels

- **Critical**: Security and accessibility violations - *Blocks merge immediately*
- **Blocking**: Test coverage, build warnings, TODOs - *Must fix before merge*
- **Required**: Design integrity, documentation - *Should fix before merge*
- **Recommended**: Code style, best practices - *Improve when possible*
- **Informational**: Suggestions and tips - *Consider for future improvements*

## CLI Usage

The `principles_cli.py` script generates custom AI prompts by combining modular YAML data.

### Commands

#### `review` - Code Review Prompts

Generate prompts for reviewing existing code against engineering principles.

```bash
python principles_cli.py review --platform <platform> --focus <areas>
```

**Options:**

- `--platform`: `android`, `ios`, or `web`
- `--focus`: Comma-separated focus areas (default: `security,accessibility,testing`)

**Examples:**

```bash
# Focus on security and accessibility for web
python principles_cli.py review --platform web --focus security,accessibility

# All principles for Android
python principles_cli.py review --platform android --focus security,accessibility,testing,design,documentation

# Just security for iOS
python principles_cli.py review --platform ios --focus security
```

#### `generate` - Code Writing Prompts

Generate prompts for writing new code that follows principles.

```bash
python principles_cli.py generate --platform <platform> --component <type>
```

**Options:**

- `--platform`: `android`, `ios`, or `web`
- `--component`: `ui`, `business-logic`, or `data-layer` (default: `ui`)

**Examples:**

```bash
# Generate UI component prompt for web
python principles_cli.py generate --platform web --component ui

# Generate business logic prompt for Android
python principles_cli.py generate --platform android --component business-logic
```

#### `architecture` - Architecture Guidance

Generate architectural guidance for specific layers.

```bash
python principles_cli.py architecture --platform <platform> --layer <layer>
```

**Examples:**

```bash
# Web data layer architecture
python principles_cli.py architecture --platform web --layer data

# iOS presentation layer patterns
python principles_cli.py architecture --platform ios --layer presentation
```

#### `dependencies` - Dependency Evaluation

Generate prompts for evaluating third-party dependencies.

```bash
python principles_cli.py dependencies --platform <platform> --check <deps>
```

**Examples:**

```bash
# Evaluate React and Lodash for web
python principles_cli.py dependencies --platform web --check react,lodash

# Evaluate RxJava for Android
python principles_cli.py dependencies --platform android --check rxjava,retrofit
```

## Integration & Workflows

### Git Hooks Integration

Enforce principles before commits:

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Checking engineering principles..."
python principles_cli.py review --platform web --focus security,accessibility

# Optional: Use with an AI tool to review staged changes
# git diff --staged | your-ai-tool --prompt "$(python principles_cli.py review)"
```

Make executable: `chmod +x .git/hooks/pre-commit`

### VS Code Tasks Integration

Create `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Review with Principles",
      "type": "shell",
      "command": "python",
      "args": [
        "principles_cli.py",
        "review",
        "--platform", "${input:platform}",
        "--focus", "${input:focus}"
      ]
    }
  ],
  "inputs": [
    {
      "id": "platform",
      "type": "pickString",
      "description": "Select platform",
      "options": ["android", "ios", "web"]
    },
    {
      "id": "focus",
      "type": "promptString",
      "description": "Focus areas (comma-separated)",
      "default": "security,accessibility"
    }
  ]
}
```

**Usage:**

1. Command Palette: `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Type "Tasks: Run Task" and select "Review with Principles"
3. Choose platform and focus areas
4. View results in integrated terminal

### Shell Aliases

Add to `.bashrc` or `.zshrc`:

```bash
# Quick principle checks
alias lvf-review='python ~/path/to/principles_cli.py review'
alias lvf-generate='python ~/path/to/principles_cli.py generate'
alias lvf-deps='python ~/path/to/principles_cli.py dependencies'

# Platform-specific shortcuts
alias lvf-android='lvf-review --platform android'
alias lvf-ios='lvf-review --platform ios'
alias lvf-web='lvf-review --platform web'
```

### CI/CD Integration

```yaml
# .github/workflows/pr-review.yml
name: Engineering Principles Check
on: pull_request

jobs:
  principles-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check Engineering Principles
        run: |
          python principles_cli.py review --platform web --focus security,accessibility
          # Use output with your AI tool for automated review
```

## Advanced Usage

### Custom Focus Areas

Available focus areas for the `--focus` parameter:

- `security` - HTTPS, secrets, encryption, input validation
- `accessibility` - Screen readers, WCAG compliance, keyboard navigation
- `testing` - Unit tests, coverage, test quality
- `design` - Design matching, responsive layouts
- `documentation` - README, API docs, inline comments
- `architecture` - Data flow, separation of concerns
- `performance` - Optimization, caching, lazy loading
- `localization` - Internationalization support
- `compatibility` - Version support, browser compatibility

### Platform-Specific Considerations

**Android:**

- Minimum SDK 24, Target SDK 28
- Approved dependencies: Dagger, RxJava2, Retrofit
- Tools: lint, ktlint, detekt
- Layouts: Responsive, portrait/landscape
- Security: EncryptedSharedPreferences

**iOS:**

- iOS 12+, iPhone only (SE to XS Max)
- First-party dependencies only
- Tools: SwiftLint, Slather
- Layouts: Code-based (no nibs)
- Security: Keychain for private data

**Web:**

- Browsers: Chrome, Safari, Firefox, Edge, IE 11
- Dependencies: React, Redux, TypeScript, Jest
- Tools: eslint, stylelint, tsc
- Layouts: Responsive, mobile-first
- Markup: Semantic HTML, WCAG 2.1

### Evaluation Framework

Test the effectiveness of generated prompts using comprehensive test cases:

#### Available Test Cases

**Detection Tests** (`evals/detection/`):

- `security_test_cases.yaml` - 10 security violation scenarios
- `accessibility_test_cases.yaml` - 10 accessibility compliance tests
- `testing_test_cases.yaml` - 8 testing principle violations
- `architecture_test_cases.yaml` - 7 architecture pattern violations

**Generation Tests** (`evals/generation/`):

- `ui_component_challenges.yaml` - 6 UI component creation challenges

#### Running Evaluations

Use the evaluation runner to test prompt effectiveness:

```bash
# Test detection prompts against all principles
python eval_runner.py --mode detection

# Test specific principles only
python eval_runner.py --mode detection --principles security accessibility

# Test generation prompts
python eval_runner.py --mode generation --categories ui_component

# Test a specific prompt file (defaults to all detection tests)
python eval_runner.py --prompt-file my_custom_prompt.txt --output results.md

# Test specific prompt with only security and accessibility
python eval_runner.py --prompt-file my_custom_prompt.txt --principles security accessibility
```

#### Integration with AI Tools

The evaluator expects two functions for AI integration:

```python
def ai_evaluator(prompt: str) -> str:
    """Send prompt to your AI service, return response"""
    # Replace with actual AI API calls
    return your_ai_service.complete(prompt)

def ai_generator(prompt: str) -> str:
    """Generate code using AI service"""
    return your_ai_service.generate_code(prompt)

# Run evaluation with your AI functions
evaluator = PromptEvaluator()
report = evaluator.evaluate_detection_prompt(
    test_prompt,
    ai_evaluator,
    ['security', 'accessibility']
)
```

#### Evaluation Metrics

- **Accuracy**: Percentage of correct detections
- **Precision**: True positives / (True positives + False positives)
- **Recall**: True positives / (True positives + False negatives)
- **F1 Score**: Harmonic mean of precision and recall
- **Per-Category Performance**: Breakdown by principle type

#### Example Evaluation Report

```
# Engineering Principles Evaluation Report

## Overall Results
- Total Tests: 35
- Correct Predictions: 28
- **Accuracy: 80.00%**
- **Precision: 85.71%**
- **Recall: 75.00%**
- **F1 Score: 80.00%**

## Results by Category
- **Security**: 8/10 (80.00%)
- **Accessibility**: 9/10 (90.00%)
- **Testing**: 6/8 (75.00%)
- **Architecture**: 5/7 (71.43%)
```

## Examples

### Real-World Workflow: Adding a New Feature

```bash
# 1. Generate code for the new feature
python principles_cli.py generate --platform web --component ui > feature_prompt.txt

# 2. Use prompt with your AI assistant to write initial code
cat feature_prompt.txt | your-ai-tool

# 3. Review the generated code
python principles_cli.py review --platform web --focus security,accessibility > review_prompt.txt

# 4. Use review prompt to check compliance
cat review_prompt.txt | your-ai-tool --input generated_code.tsx

# 5. Fix any violations and repeat review as needed
```

### Testing Prompt Effectiveness

```bash
# Test how well your prompts detect violations
python principles_cli.py review --platform web > test_prompt.txt
python eval_runner.py --prompt-file test_prompt.txt --mode detection

# Compare different prompt approaches
python eval_runner.py --mode detection --principles security,accessibility --output baseline.md

# Test generation prompts create compliant code
python eval_runner.py --mode generation --categories ui_component --output generation_report.md
```

### Dependency Evaluation Example

```bash
# Check if a new dependency aligns with principles
python principles_cli.py dependencies --platform web --check some-new-library

# Output includes:
# - Build vs buy analysis
# - Security considerations
# - Maintenance burden assessment
# - Alternative suggestions
```

## Maintenance & Evolution

### Adding New Principles

1. Add to `core/principles.yaml` with rationale
2. Create detection rules in `modules/detection/rules/`
3. Add generation guidance in `modules/generation/guidance.yaml`
4. Create test cases in `evals/`
5. Update this README

### Updating Platform Requirements

1. Modify `core/platforms.yaml`
2. Update platform-specific rules
3. Test with representative codebases
4. Update documentation

### Contributing

1. Follow the modular structure
2. Add test cases for new rules
3. Update documentation
4. Ensure backward compatibility

## Troubleshooting

**Common Issues:**

- **File not found errors**: Ensure you're running from the repository root
- **Invalid platform**: Use `android`, `ios`, or `web` (lowercase)
- **Empty output**: Check that YAML files aren't corrupted
- **Missing dependencies**: System requires Python 3.7+ with PyYAML

**Validation Commands:**

```bash
# Check YAML syntax
python -c "import yaml; yaml.safe_load(open('core/principles.yaml'))"

# Verify CLI functionality
python principles_cli.py --help
```

For more detailed command syntax, see [CLI_REFERENCE.md](CLI_REFERENCE.md).
