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

# Install dependencies
uv sync

# Generate enhanced code review prompt (includes technical detection patterns)
uv run python principles_cli.py review --platform web --focus security

# Generate a code writing prompt for Android UI components
uv run python principles_cli.py generate --platform android --component ui

# Evaluate prompt effectiveness with AI models (85% accuracy by default)
uv run python eval_runner.py --init-config eval_config.yaml  # Create initial config
# Edit config with API keys, then:
uv run python eval_runner.py --mode detection  # Uses eval_config.yaml by default

# Try LLM-enhanced mode for latest practices
uv run python eval_runner.py --mode detection --enhanced
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
└── eval_config.yaml        # Sample configuration file
```

**Key Features:**

- **Modular Design**: Core philosophy separate from implementation
- **Platform-Aware**: Android, iOS, and Web-specific guidance
- **Context-Sensitive**: Different rules for UI vs business logic vs data layer
- **Severity-Based**: Critical, Blocking, Required, Recommended, Informational
- **AI-Powered**: Generates prompts for AI code review and generation
- **Enhanced by Default**: Automatically includes technical detection patterns for 85% accuracy
- **LLM Enhancement**: Optional mode for latest security/accessibility best practices

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

The `principles_cli.py` script generates custom AI prompts by combining modular YAML data. **All prompts are automatically enhanced with technical detection rules** from the `modules/detection/rules/` directory for maximum effectiveness.

### **Enhancement Modes**

**Default Enhancement** (Always Active):

- Includes specific technical detection patterns
- 85% accuracy on evaluation tests
- No additional flags required

**LLM Enhancement** (Optional):

- Uses AI to add latest OWASP Top 10, WCAG 2.2 practices
- Includes 2024-2025 security/accessibility updates
- Perfect for staying current with emerging threats
- Adaptive to new vulnerability patterns and attack vectors

### **How Enhancement Works**

**Rule-Based Enhancement** (Default):

- Automatically loads detection patterns from `modules/detection/rules/`
- Includes specific regex patterns, platform checks, and technical guidance
- Maps engineering principles to concrete, actionable detection rules
- Example: "HTTPS everywhere" becomes specific HTTP URL pattern detection

**LLM Enhancement** (--enhanced):

- Takes the rule-enhanced prompt as input
- Uses AI to add cutting-edge security/accessibility knowledge
- Updates with latest CVEs, framework vulnerabilities, and accessibility APIs
- Contextual for your specific platform and focus areas

### Basic Commands

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
uv run python principles_cli.py review --platform web --focus security,accessibility

# All principles for Android
uv run python principles_cli.py review --platform android --focus security,accessibility,testing,design,documentation

# Just security for iOS
uv run python principles_cli.py review --platform ios --focus security
```

#### `generate` - Code Writing Prompts

Generate prompts for writing new code that follows principles.

```bash
uv run python principles_cli.py generate --platform <platform> --component <type>
```

**Options:**

- `--platform`: `android`, `ios`, or `web`
- `--component`: `ui`, `business-logic`, or `data-layer` (default: `ui`)

**Examples:**

```bash
# Generate UI component prompt for web
uv run python principles_cli.py generate --platform web --component ui

# Generate business logic prompt for Android
uv run python principles_cli.py generate --platform android --component business-logic
```

#### `architecture` - Architecture Guidance

Generate architectural guidance for specific layers.

```bash
uv run python principles_cli.py architecture --platform <platform> --layer <layer>
```

#### `dependencies` - Dependency Evaluation

Generate prompts for evaluating third-party dependencies.

```bash
uv run python principles_cli.py dependencies --platform <platform> --check <deps>
```

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

### Advanced Focus Areas

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

## Evaluation Framework

Test the effectiveness of generated prompts using comprehensive test cases with real AI models.

### **Performance Metrics**

The evaluation framework shows **significant improvements** with our enhanced prompt generation:

| Mode | Accuracy | Precision | Recall | F1 Score |
|------|----------|-----------|--------|----------|
| **Basic Principles** | 60% | 75% | 75% | 75% |
| **Enhanced (Default)** | **85%** | **84%** | **100%** | **91%** |
| **LLM Enhanced** | 80% | 88% | 88% | 88% |

**Key Improvements:**

- **+25% accuracy** with rule-based enhancement (now default)
- **Perfect recall** - catches all actual violations
- **Excellent F1 scores** - balanced precision and recall
- **Category specific**: 80% security detection, 90% accessibility detection

### Setup & Configuration

**1. Install Dependencies**

This project uses `uv` for modern Python dependency management and virtual environments.

```bash
# Install uv if you haven't already
pip install uv

# Install all dependencies (production + development)
uv sync

# Or install only production dependencies
uv install
```

**2. Create Config File**

```bash
uv run python eval_runner.py --init-config eval_config.yaml
```

This creates `eval_config.yaml` which is automatically used by all subsequent runs.

**3. Add API Keys**
Edit `eval_config.yaml` with your actual API keys:

```yaml
defaults:
  provider: openai
  temperature: 0.1
  max_tokens: 1000

providers:
  openai:
    api_key: sk-your-actual-openai-key-here
    default_model: gpt-4o

  anthropic:
    api_key: sk-ant-your-actual-anthropic-key-here
    default_model: claude-3-5-sonnet-20241022

  groq:
    api_key: gsk-your-actual-groq-key-here
    default_model: llama-3.1-70b-versatile

  together:
    api_key: your-actual-together-key-here
    default_model: meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo

  # Local models - no API key needed
  ollama:
    base_url: http://localhost:11434/v1
    default_model: llama3.1
```

### AI Provider Integration

**Supported Providers:**

- **OpenAI**: GPT-4, GPT-4o, GPT-3.5-turbo
- **Anthropic**: Claude 3.5 Sonnet, Claude 3 Opus
- **Together AI**: Llama 3.1, Mixtral, CodeLlama
- **Groq**: Ultra-fast Llama inference
- **Ollama**: Local models (no API key needed)
- **Custom**: Your own API endpoints

**Getting API Keys:**

**OpenAI:**

1. Go to <https://platform.openai.com/api-keys>
2. Create new secret key (starts with `sk-`)

**Anthropic (Claude):**

1. Go to <https://console.anthropic.com/>
2. Create API key (starts with `sk-ant-`)

**Groq:**

1. Go to <https://console.groq.com/>
2. Get API key (starts with `gsk-`)

**Together AI:**

1. Go to <https://api.together.xyz/>
2. Get API key from dashboard

**Ollama (Local - No Key Needed):**

1. Install: <https://ollama.ai/>
2. Run: `ollama run llama3.1`

**Configuration Priority:**

Settings are applied in this order (highest to lowest):

1. **Command line args** (`--provider`, `--model`)
2. **Config file** (`eval_config.yaml`)
3. **Environment variables** (`OPENAI_API_KEY`, etc.)
4. **Built-in defaults**

### Running Tests

**Basic Detection Tests:**

```bash
# Test with default enhanced prompts (85% accuracy)
uv run python eval_runner.py --mode detection

# Test with LLM-enhanced prompts (latest practices)
uv run python eval_runner.py --mode detection --enhanced

# Test with different providers
uv run python eval_runner.py --provider anthropic --mode detection
uv run python eval_runner.py --provider groq --mode detection --enhanced
uv run python eval_runner.py --provider ollama --mode detection

# List all available providers
uv run python eval_runner.py --list-providers
```

**Specific Principles:**

```bash
# Test only security and accessibility (default enhanced)
uv run python eval_runner.py --mode detection --principles security,accessibility

# Test with LLM enhancement for latest practices
uv run python eval_runner.py --mode detection --principles security,accessibility --enhanced

# Test only architecture principles
uv run python eval_runner.py --mode detection --principles architecture
```

**Custom Prompts:**

```bash
# Test your own prompt file
uv run python principles_cli.py review --platform web > my_prompt.txt
uv run python eval_runner.py --prompt-file my_prompt.txt --mode detection

# Save results to file
uv run python eval_runner.py --mode detection --output results.md
```

**Model Comparison:**

```bash
# Compare different models on same test
uv run python eval_runner.py --provider openai --model gpt-4o --output gpt4_results.md
uv run python eval_runner.py --provider anthropic --output claude_results.md
uv run python eval_runner.py --provider groq --output groq_results.md

# Compare results
diff gpt4_results.md claude_results.md
```

**Generation Tests:**

```bash
# Test generation prompts
uv run python eval_runner.py --mode generation --categories ui_component

# Test both detection and generation
uv run python eval_runner.py --mode both --output full_report.md
```

### Available Test Cases

**Detection Tests** (`evals/detection/`):

- `security_test_cases.yaml` - 10 security violation scenarios
- `accessibility_test_cases.yaml` - 10 accessibility compliance tests
- `testing_test_cases.yaml` - 8 testing principle violations
- `architecture_test_cases.yaml` - 7 architecture pattern violations

**Generation Tests** (`evals/generation/`):

- `ui_component_challenges.yaml` - 6 UI component creation challenges

### Understanding Results

**Evaluation Metrics:**

- **Accuracy**: Percentage of correct detections
- **Precision**: True positives / (True positives + False positives)
- **Recall**: True positives / (True positives + False negatives)
- **F1 Score**: Harmonic mean of precision and recall
- **Per-Category Performance**: Breakdown by principle type

**Example Evaluation Report:**

```markdown
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

## Integration & Workflows

### Git Hooks Integration

Enforce principles before commits:

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Checking engineering principles..."
uv run python principles_cli.py review --platform web --focus security,accessibility

# Optional: Use with an AI tool to review staged changes
# git diff --staged | your-ai-tool --prompt "$(uv run python principles_cli.py review)"
```

Make executable: `chmod +x .git/hooks/pre-commit`

### VS Code Tasks Integration

#### Per-Project Integration (Recommended)

Add a `.vscode/tasks.json` file to each project:

**For a Web Project:**

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Review with Engineering Principles",
      "type": "shell",
      "command": "python",
      "args": [
        "/path/to/engineering_principles/principles_cli.py",
        "review",
        "--platform", "web",
        "--focus", "${input:focus}"
      ],
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "panel": "new"
      }
    }
  ],
  "inputs": [
    {
      "id": "focus",
      "type": "pickString",
      "description": "Focus areas for review",
      "options": [
        "security,accessibility",
        "security,accessibility,testing",
        "design,accessibility",
        "performance,security"
      ],
      "default": "security,accessibility"
    }
  ]
}
```

#### Usage

1. Open Command Palette: `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Type "Tasks: Run Task"
3. Select "Review with Engineering Principles"
4. Choose focus areas from predefined options
5. Copy generated prompt to use with AI tools

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
      - name: Install dependencies
        run: pip install openai pyyaml
      - name: Run evaluations
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python eval_runner.py --mode detection --output eval_results.md
          cat eval_results.md >> $GITHUB_STEP_SUMMARY
```

### Shell Aliases

Add to `.bashrc` or `.zshrc`:

```bash
# Quick principle checks
alias lvf-review='python ~/path/to/principles_cli.py review'
alias lvf-generate='python ~/path/to/principles_cli.py generate'
alias lvf-eval='python ~/path/to/eval_runner.py'

# Platform-specific shortcuts
alias lvf-android='lvf-review --platform android'
alias lvf-ios='lvf-review --platform ios'
alias lvf-web='lvf-review --platform web'
```

## Examples

### Real-World Workflow: Adding a New Feature

```bash
# 1. Generate code for the new feature
uv run python principles_cli.py generate --platform web --component ui > feature_prompt.txt

# 2. Use prompt with your AI assistant to write initial code
cat feature_prompt.txt | your-ai-tool

# 3. Review the generated code
uv run python principles_cli.py review --platform web --focus security,accessibility > review_prompt.txt

# 4. Use review prompt to check compliance
cat review_prompt.txt | your-ai-tool --input generated_code.tsx

# 5. Test prompt effectiveness
uv run python eval_runner.py --prompt-file review_prompt.txt --mode detection
```

### Testing Prompt Effectiveness

```bash
# Test default enhanced prompts (85% accuracy)
uv run python eval_runner.py --mode detection --principles security,accessibility --output baseline.md

# Test with latest security/accessibility practices
uv run python eval_runner.py --mode detection --principles security,accessibility --enhanced --output llm_enhanced.md

# Compare enhancement modes
diff baseline.md llm_enhanced.md

# Test generation prompts create compliant code
uv run python eval_runner.py --mode generation --categories ui_component --output generation_report.md
```

### Dependency Evaluation Example

```bash
# Check if a new dependency aligns with principles
uv run python principles_cli.py dependencies --platform web --check some-new-library

# Output includes:
# - Build vs buy analysis
# - Security considerations
# - Maintenance burden assessment
# - Alternative suggestions
```

## Troubleshooting

### Common Issues

**Evaluation Runner:**

- **"OpenAI package not found"**: Run `uv sync` to install dependencies
- **"API key required"**: Check config file, environment variables, or use `--api-key`
- **"Error calling API"**: Verify API key, check credits/rate limits, test internet connection
- **"Model not found"**: Use `--list-providers` to see available models
- **Low accuracy scores**: Try `--enhanced` flag for LLM-enhanced prompts with latest practices

**CLI Issues:**

- **File not found errors**: Ensure you're running from the repository root
- **Invalid platform**: Use `android`, `ios`, or `web` (lowercase)
- **Empty output**: Check that YAML files aren't corrupted
- **Missing dependencies**: Run `uv sync` to install all required packages

### Validation Commands

```bash
# Test config loading
uv run python -c "from eval_runner import load_config; print(load_config('eval_config.yaml'))"

# Test provider setup
uv run python eval_runner.py --list-providers

# Check YAML syntax
uv run python -c "import yaml; yaml.safe_load(open('core/principles.yaml'))"

# Verify CLI functionality
uv run python principles_cli.py --help
uv run python eval_runner.py --help
```

### Local Development (No API Costs)

```bash
# Install and use Ollama for free local testing
curl https://ollama.ai/install.sh | sh
ollama pull llama3.1
uv run python eval_runner.py --provider ollama --mode detection
```

## Development

### Project Structure

This project uses modern Python tooling for development:

- **uv** - Fast Python package manager and virtual environment manager
- **pytest** - Testing framework with coverage reporting
- **ruff** - Fast Python linter (replaces flake8, isort, etc.)
- **black** - Code formatting
- **mypy** - Static type checking
- **pre-commit** - Git hooks for code quality

### Development Setup

```bash
# Clone the repository
git clone <repo-url>
cd engineering_principles

# Install all dependencies (production + development)
uv sync

# Install pre-commit hooks (optional but recommended)
uv run pre-commit install
```

### Running Tests

```bash
# Run all tests with coverage
uv run pytest

# Run tests in verbose mode
uv run pytest -v

# Run specific test file
uv run pytest tests/test_eval_runner.py

# Run with coverage report
uv run pytest --cov-report=html
```

### Code Quality

```bash
# Format code with black
uv run black .

# Lint with ruff (auto-fix issues)
uv run ruff check . --fix

# Type checking with mypy
uv run mypy . --ignore-missing-imports

# Run all quality checks
uv run pre-commit run --all-files
```

### Adding Dependencies

```bash
# Add production dependency
uv add <package-name>

# Add development dependency
uv add --dev <package-name>

# Update all dependencies
uv sync
```

### Project Standards

- **Test Coverage**: Minimum 25% overall, aiming for 80% on business logic
- **Type Hints**: All public functions should have type annotations
- **Documentation**: All modules and classes should have docstrings
- **Code Style**: Black formatting with 88-character line length
- **Linting**: Ruff with strict settings for imports, code quality

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

