# LEAP - Livefront Engineering Automated Principles

Modular system for encoding and enforcing engineering principles through AI-assisted code detection and generation.

## Status

Experimental. Open questions remain:

- **Codification**: How to translate human principles into patterns LLMs can reliably apply?
- **Evaluation**: What constitutes a valid eval for engineering principles?
- **Balance**: Hard-coded rules (YAML patterns) vs LLM analysis?

## Recent Changes

- Philosophy integration: Livefront mantras/values in code generation prompts
- Simplified architecture: Consolidated data loading, streamlined prompt generation
- Enforcement context: Shows CI checks that should be implemented per standards
- Focus area filtering: Target specific principles (security, accessibility, testing)
- YAML utilization: 542 lines of guidance data integrated

## Philosophy

> "Livefront Engineers are craftspeople."

We give a damn about building software that is reliable, performant, maintainable, and remarkably fun to use.

**Core Mantras:**

- **We don't defer work**: If it can be done now, do it now. Otherwise, create a ticket.
- **The design is the spec**: We deliver working software that fulfills the vision laid out in the designs.

## Quick Start

### For End Users

```bash
git clone git@github.com:james-livefront/engineering_principles.git
cd engineering_principles
./install.sh
```

The script:
- Checks Python version (3.11+ required)
- Installs pipx if needed
- Installs LEAP globally
- Shows Claude Desktop config instructions

### For Developers

```bash
# Clone and navigate to the repository
git clone git@github.com:james-livefront/engineering_principles.git
cd engineering_principles

# Install dependencies for local development
uv sync

# » Generate code review prompts
uv run python principles_cli.py review --platform web --focus security
uv run python principles_cli.py review --platform android --focus accessibility,testing
uv run python principles_cli.py review --platform ios --focus architecture

# » Generate system prompts for AI assistant setup
uv run python principles_cli.py generate --platform web --component ui
uv run python principles_cli.py generate --platform android --component business-logic

# » Generate architecture guidance prompts
uv run python principles_cli.py architecture --platform web

# » Evaluate dependency approval
uv run python principles_cli.py dependencies --platform web react typescript

# » Test prompt effectiveness (requires API keys in .env)
cp .env.example .env  # Edit with your API keys
uv run python eval_runner.py --mode detection --platform web --focus accessibility

# » Improved mode attempts to increase detection with LLM analysis
uv run python eval_runner.py --mode detection --platform web --focus security --enhanced

# » Install MCP server globally for AI agent integration
pipx install .

# » Or start MCP server manually for testing
make mcp-server
# Or run directly:
uv run python leap_mcp_server.py
```

## System Architecture

Modular architecture separating core knowledge from implementation:

```text
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

**Features:**

- Modular design: Core philosophy separate from implementation
- Platform-aware: Android, iOS, Web-specific guidance
- Focus-driven: Target specific principles for efficient reviews
- Severity-based: Critical, Blocking, Required, Recommended, Informational
- Pattern-based detection: 70%+ coverage with YAML regex patterns
- Cultural context: Integrates Livefront mantras and values
- Enforcement awareness: Shows CI checks per standards
- LLM layer: Rules + AI analysis (experimental)

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

### Severity System

- **Critical**: Security vulnerabilities, accessibility barriers → Blocks merge
- **Blocking**: Test coverage gaps, build warnings, TODO comments → Must fix before merge
- **Required**: Design deviations, missing documentation → Should fix before merge
- **Recommended**: Code style issues, best practices → Improve when possible
- **Informational**: Suggestions and tips → Consider for future

AI assistants receive structured guidance per severity level for consistent code review feedback aligned with engineering standards.

## Detection Architecture

Two-layer system: objective pattern matching + optional AI analysis.

### Base Detection (70% Coverage)

YAML regex patterns:
- Security: Hardcoded secrets, insecure URLs, weak crypto, storage issues
- Accessibility: Missing alt text, ARIA labels, touch targets, semantic HTML
- Testing: Missing tests, flaky patterns, coverage issues
- Architecture: Data flow violations, tight coupling, error handling

### Enhanced Detection (Experimental)

LLM analysis attempts:
- Latest standards: OWASP 2024, WCAG 2.2, framework-specific patterns
- Cross-file dependencies and contextual severity
- Advanced patterns: Multi-line detection, semantic code analysis

Note: YAML patterns provide consistent detection. LLM enhancement experimental, may not improve accuracy.

## CLI Usage

Two prompt types with integrated YAML detection rules:

1. **System Prompts** (`generate`): Set up AI assistants with persistent role and constraints
2. **User Prompts** (`review`): Make specific requests within established context

```bash
# Set up AI assistant with system prompt
python principles_cli.py generate --platform web --component ui > system.txt

# Use for specific review tasks
python principles_cli.py review --platform web --focus security > review.txt
```

**Enhancement Layers:**

Base (always active):
- Detection patterns from `modules/detection/rules/`
- Platform-specific filtering
- Severity-ordered rules
- ~70% test case coverage

AI Analysis (`--enhanced`):
- Latest OWASP, WCAG 2.2 intelligence
- Cross-file and contextual analysis
- Note: Experimental, may introduce false positives

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

# Review Android code with focus on UI concerns
uv run python principles_cli.py review --platform android --focus accessibility,testing

# Review backend service with focus on security and architecture
uv run python principles_cli.py review --platform web --focus security,architecture

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

**Includes:**
- Engineering culture: Livefront mantras and core values
- Focused principles: Relevant for component type
- Platform requirements: Approved dependencies, tools, version requirements
- Component guidance: Platform-specific "always" and "never" rules
- Common mistakes: Top pitfalls to avoid

**Examples:**

```bash
# Generate UI component prompt for web (includes accessibility guidance)
uv run python principles_cli.py generate --platform web --component ui

# Generate business logic prompt for Android (includes testing guidance)
uv run python principles_cli.py generate --platform android --component business-logic

# Generate data layer prompt (includes security guidance)
uv run python principles_cli.py generate --platform ios --component data-layer
```

#### `architecture` - Architecture Guidance

Generate architectural guidance for specific layers.

```bash
uv run python principles_cli.py architecture --platform <platform> --layer <layer>
```

#### `dependencies` - Dependency Evaluation

Generate prompts for evaluating third-party dependencies.

```bash
uv run python principles_cli.py dependencies --platform <platform> <dependency1> <dependency2> ...
```

**Examples:**

```bash
# Evaluate web dependencies
uv run python principles_cli.py dependencies --platform web lodash axios

# Evaluate Android dependencies
uv run python principles_cli.py dependencies --platform android rxjava3 retrofit
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

## MCP Server Integration

MCP server provides real-time access to engineering principles, detection patterns, and enforcement specs for AI agents.


### Installation

```bash
pip install pipx
cd /path/to/engineering_principles
pipx install .
```

Global commands:
- `leap-mcp-server` - MCP server for AI agents
- `leap-review` - Code review prompts
- `leap-eval` - Evaluation tests

For development: Use `uv run python principles_cli.py` for immediate code changes.

### Starting the Server Manually

```bash
leap-mcp-server                  # pipx installation
make mcp-server                  # local development
uv run python leap_mcp_server.py # direct execution
```

Server runs on stdio for MCP-compatible AI agents.

### Available Tools

7 tools for AI agents:

#### 1. `get_principles`
Get engineering principles, optionally filtered by platform and focus areas.

```python
# Example call
{
  "platform": "web",
  "focus_areas": ["security", "accessibility"]
}
```

#### 2. `get_detection_patterns`
Get regex patterns for detecting violations of engineering principles.

```python
# Example call
{
  "principle": "security",
  "platform": "web"
}
```

#### 3. `get_generation_guidance`
Get guidance for writing new code following engineering principles.

```python
# Example call
{
  "platform": "android",
  "component_type": "ui"
}
```

#### 4. `get_platform_requirements`
Get platform-specific requirements, tools, and constraints.

```python
# Example call
{
  "platform": "ios"
}
```

#### 5. `get_enforcement_specs`
Get CI implementation guidance showing what checks should be implemented.

```python
# Example call
{
  "focus_areas": ["security", "testing"]
}
```

#### 6. `validate_dependency`
Check if a dependency is approved for a specific platform.

```python
# Example call
{
  "package": "lodash",
  "platform": "web"
}
```

#### 7. `get_severity_guidance`
Get guidance on how to classify violation severity levels.

```python
# Example call
{}
```

### Adding to Claude Desktop

After `pipx install .`, add to config:

**Location:** `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

```json
{
  "mcpServers": {
    "leap": {
      "command": "leap-mcp-server"
    }
  }
}
```

**For development** (immediate code changes):

```json
{
  "mcpServers": {
    "leap": {
      "command": "/absolute/path/to/engineering_principles/.venv/bin/python",
      "args": [
        "/absolute/path/to/engineering_principles/leap_mcp_server.py"
      ],
      "cwd": "/absolute/path/to/engineering_principles"
    }
  }
}
```

Replace `/absolute/path/to/engineering_principles` with actual path. Run `uv sync` first.

### Adding to Claude Code

Import Claude Desktop config:

**Location:** `~/.config/claude-code/mcp.json`

```json
{
  "$import": "~/Library/Application Support/Claude/claude_desktop_config.json"
}
```

Shares MCP servers between Claude Desktop and Claude Code. Updates to Desktop config reflected in Code.

Alternative: Configure Claude Code separately using same format as Desktop.

### Usage in AI Agents

Agents automatically access LEAP data:
- Code review task → calls `get_detection_patterns`
- New code generation → calls `get_generation_guidance`
- Dependency evaluation → calls `validate_dependency`

Manual queries:
```
"What are the security principles for web?"
→ calls get_principles with platform=web, focus_areas=["security"]

"Is react-query approved for web?"
→ calls validate_dependency with package=react-query, platform=web

"What CI checks for accessibility?"
→ calls get_enforcement_specs with focus_areas=["accessibility"]
```

Benefits:
- Real-time access: No copy/paste, agents query directly
- Context-aware: Platform-specific, focused guidance
- Always current: YAML changes immediately available
- Structured data: Not just text prompts
- Dependency validation: Instant approval checks
- Enforcement specs: CI check guidance

## Evaluation Framework

Test prompt effectiveness using test cases with AI models.

### Focus Area Targeting

Target specific principles based on review needs:

```bash
# Focus on UI concerns for frontend code
$ python principles_cli.py review --platform web --focus accessibility,design_integrity

# Focus on backend concerns for services
$ python principles_cli.py review --platform android --focus security,testing,architecture

# Focus on specific principle for targeted review
$ python principles_cli.py review --platform ios --focus security
```

Common combinations:
- UI Code: `accessibility,design_integrity,code_quality`
- Business Logic: `testing,architecture,minimal_dependencies`
- Data Layer: `security,testing,unidirectional_data_flow`

Generated prompts include metadata headers for automatic eval configuration:

```yaml
<!-- PROMPT_METADATA
platform: web
focus: security,accessibility
mode: review
-->
```

Evaluation framework:
- Detects platform and focus from metadata
- Filters test cases to match context
- Fair evaluation (web prompts tested against web violations only)

### Performance Metrics

Rule-based prompt generation results:

| Mode | Accuracy | Precision | Recall | F1 Score |
|------|----------|-----------|--------|----------|
| Basic Principles | 60% | 75% | 75% | 75% |
| Rule-Based (Default) | 85% | 84% | 100% | 91% |
| LLM Enhanced | 80% | 88% | 88% | 88% |

Key improvements:
- +25% accuracy with rule-based (default)
- 100% recall: catches all violations
- 91% F1 score: balanced precision/recall
- Category specific: 80% security, 90% accessibility

### Setup & Configuration

#### 1. Install Dependencies

Uses `uv` for dependency management:

```bash
pip install uv
uv sync      # production + development
uv install   # production only
```

#### 2. Set Up API Keys

Create a `.env` file with your API keys:

```bash
cp .env.example .env
# Edit .env and add your actual API keys (OPENAI_API_KEY, etc.)
```

Or use environment variables directly:

```bash
export OPENAI_API_KEY=sk-your-api-key-here
export ANTHROPIC_API_KEY=sk-ant-your-api-key-here
```

### AI Provider Integration

Supported: OpenAI, Anthropic, Together AI, Groq, Ollama (local), Custom

API keys:
- OpenAI: <https://platform.openai.com/api-keys> (starts with `sk-`)
- Anthropic: <https://console.anthropic.com/> (starts with `sk-ant-`)
- Groq: <https://console.groq.com/> (starts with `gsk-`)
- Together AI: <https://api.together.xyz/>
- Ollama: <https://ollama.ai/> (no key needed)

Configuration priority:
1. Command line args (`--provider`, `--model`)
2. Config file (`eval_config.yaml`)
3. Environment variables
4. Built-in defaults

### Running Tests

**Basic Detection Tests:**

```bash
# Auto-detect platform and focus from prompt metadata
uv run python principles_cli.py review --platform web --focus security > prompt.txt
uv run python eval_runner.py --prompt-file prompt.txt  # Note: --mode detection is the default

# Or manually specify platform and focus (overrides metadata)
uv run python eval_runner.py --prompt-file prompt.txt --platform android --focus testing

# Test with LLM enhancement for better accuracy
uv run python eval_runner.py --prompt-file prompt.txt --enhanced

# Explicitly specify generation mode (detection is default)
uv run python eval_runner.py --mode generation --categories ui_component
```

**Specific Principles:**

```bash
# Test only security and accessibility (default improved)
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

### Evaluation Runner Defaults

Defaults:
- Mode: `detection` (use `--mode generation` or `--mode both` to change)
- Parallel execution: Enabled (use `--no-parallel` to disable)
- Provider: Auto-detect from available API keys
- Model: Provider's recommended model unless specified

### Available Test Cases

**Detection Tests** (`evals/detection/`):

- `security_test_cases.yaml` - 10 security violation scenarios
- `accessibility_test_cases.yaml` - 10 accessibility compliance tests
- `testing_test_cases.yaml` - 8 testing principle violations
- `architecture_test_cases.yaml` - 7 architecture pattern violations

**Generation Tests** (`evals/generation/`):

- `ui_component_challenges.yaml` - 6 UI component creation challenges

### Understanding Results

For detailed metric explanations and optimization strategies, see [docs/EVALUATION_METRICS.md](docs/EVALUATION_METRICS.md).

Example report:

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
# Test default improved prompts (85% accuracy)
uv run python eval_runner.py --mode detection --principles security,accessibility --output baseline.md

# Test with latest security/accessibility practices
uv run python eval_runner.py --mode detection --principles security,accessibility --enhanced --output llm_analysis.md

# Compare detection modes
diff baseline.md llm_analysis.md

# Test generation prompts create compliant code
uv run python eval_runner.py --mode generation --categories ui_component --output generation_report.md
```

### Dependency Evaluation Example

```bash
# Check if a new dependency aligns with principles
uv run python principles_cli.py dependencies --platform web some-new-library

# Output includes:
# - Approval status (✅ APPROVED or ❌ NOT APPROVED)
# - Build vs buy analysis
# - Security considerations
# - Maintenance burden assessment
# - Alternative suggestions
```

## Troubleshooting

### Installation Issues

**"Python not found" or version too old:**
```bash
# Check Python version (need 3.11+)
python3 --version

# Install Python 3.11+ from https://www.python.org/downloads/
# Or use homebrew on macOS:
brew install python@3.11
```

**"pipx: command not found" after installation:**
```bash
# Ensure ~/.local/bin is in your PATH
export PATH="$HOME/.local/bin:$PATH"

# Add to your shell profile (~/.zshrc or ~/.bash_profile):
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**"leap-mcp-server: command not found":**
```bash
# Reinstall LEAP
cd /path/to/engineering_principles
pipx install --force .

# Check installation
which leap-mcp-server
```

### MCP Server Issues

**Server won't start in Claude Desktop:**

1. Check the MCP server log:
   ```bash
   tail -50 ~/Library/Logs/Claude/mcp-server-leap.log
   ```

2. Verify LEAP is installed:
   ```bash
   leap-mcp-server --help
   ```

3. Test server startup manually:
   ```bash
   leap-mcp-server
   # Press Ctrl+C to stop
   ```

4. Reinstall if needed:
   ```bash
   cd /path/to/engineering_principles
   pipx reinstall engineering_principles
   ```

**"spawn leap-mcp-server ENOENT" error:**
- The `leap-mcp-server` command isn't in Claude's PATH
- Make sure you used `pipx install .` (not just `pip install`)
- Restart Claude Desktop after installation

### Common CLI Issues

**Evaluation Runner:**

- **"OpenAI package not found"**: Run `uv sync` to install dependencies
- **"API key required"**: Check config file, environment variables, or use `--api-key`
- **"Error calling API"**: Verify API key, check credits/rate limits, test internet connection
- **"Model not found"**: Use `--list-providers` to see available models
- **Low accuracy scores**: Try `--enhanced` flag for LLM-improved prompts with latest practices

**CLI Commands:**

- **File not found errors**: Ensure you're running from the repository root
- **Invalid platform**: Use `android`, `ios`, or `web` (lowercase)
- **Empty output**: Check that YAML files aren't corrupted
- **Missing dependencies**: Run `uv sync` to install all required packages

### Validation Commands

```bash
# Test LEAP installation
leap-review --help
leap-eval --help
leap-mcp-server --version 2>&1 | head -5

# Test config loading (for developers)
uv run python -c "from eval_runner import load_config; print(load_config('eval_config.yaml'))"

# Test provider setup (for developers)
uv run python eval_runner.py --list-providers

# Check YAML syntax (for developers)
uv run python -c "import yaml; yaml.safe_load(open('core/principles.yaml'))"
```

### Getting Help

If you're still having issues:

1. **Check the logs:**
   - Claude Desktop: `~/Library/Logs/Claude/mcp-server-leap.log`
   - Claude Desktop main: `~/Library/Logs/Claude/main.log`

2. **Try the install script:**
   ```bash
   ./install.sh
   ```

3. **Start fresh:**
   ```bash
   pipx uninstall engineering_principles
   ./install.sh
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
git clone git@github.com:james-livefront/engineering_principles.git
cd engineering_principles

# Quick setup using Makefile
make install       # Install dependencies
make install-hooks # Install pre-commit hooks (optional)
make all          # Install + run all quality checks

# Or use uv directly
uv sync                          # Install all dependencies
uv run pre-commit install       # Install pre-commit hooks (optional)
```

### Running Tests

```bash
# Using Makefile (recommended)
make test          # Run all tests
make test-cov      # Run tests with coverage report
make pre-commit    # Run all quality checks

# Or use uv directly
uv run pytest                              # Run all tests
uv run pytest -v                          # Verbose mode
uv run pytest tests/test_eval_runner.py   # Specific test file
uv run pytest --cov-report=html          # Coverage report
```

### Code Quality

```bash
# Using Makefile (recommended)
make lint          # Check code style
make lint-fix      # Auto-fix linting issues
make format        # Format code with black + ruff
make format-check  # Check formatting without changes
make typecheck     # Run mypy type checking
make pre-commit    # Run all quality checks
make all          # Install deps + run all checks

# Or use uv directly
uv run black .                        # Format code
uv run ruff check . --fix            # Lint with auto-fix
uv run mypy .                         # Type checking
uv run pre-commit run --all-files    # All quality checks
```

### Development Helpers

```bash
make help          # Show all available commands
make install       # Install project dependencies
make clean         # Clean up generated files
make watch         # Watch files and run tests on changes (requires fswatch)
make install-hooks # Install pre-commit git hooks
make ci           # Full CI pipeline (for GitHub Actions)
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

- Test coverage: 25% minimum, target 80% on business logic
- Type hints: All public functions
- Documentation: All modules and classes
- Code style: Black, 88-character line length
- Linting: Ruff with strict settings

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

## Advanced Usage

### Multi-Focus Area Detection

```bash
# Comprehensive security + accessibility review
uv run python principles_cli.py review --platform web --focus security,accessibility,testing

# Generate cross-cutting architecture guidance
uv run python principles_cli.py review --platform android --focus architecture,testing
```

### Enhanced Mode Examples

```bash
# Enhanced security review with latest OWASP patterns
uv run python eval_runner.py --mode detection --platform web --focus security --enhanced

# Test enhanced accessibility prompt
uv run python eval_runner.py --platform web --focus accessibility --enhanced

# Test comprehensive coverage across all areas
uv run python eval_runner.py --mode detection --enhanced --platform web
```

### Integration Workflows

```bash
# 1. Generate prompts for your platform
uv run python principles_cli.py review --platform web --focus security > security_prompt.md

# 2. Test effectiveness against your codebase
uv run python eval_runner.py --prompt-file security_prompt.md --mode detection

# 3. Use improved mode for latest coverage
uv run python eval_runner.py --prompt-file security_prompt.md --enhanced --mode detection
```

### Custom Evaluation

```bash
# Test specific principles only
uv run python eval_runner.py --mode detection --principles security,accessibility

# Generate code compliance testing
uv run python eval_runner.py --mode generation --platform android --categories ui

# Export detailed reports
uv run python eval_runner.py --mode detection --enhanced --output results.json
```

### Contributing

1. Follow the modular structure
2. Add test cases for new rules
3. Update documentation
4. Ensure backward compatibility
