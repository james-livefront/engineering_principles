# CLI Reference

Complete command reference for LEAP CLI tools.

## Overview

LEAP provides three global commands after installation:

- `leap` - Main CLI for generating prompts and evaluating dependencies
- `leap-eval` - Evaluation framework for testing prompt effectiveness
- `leap-mcp-server` - MCP server for AI agent integration

## Installation

**End users:**

```bash
./install.sh
# Or with uv:
uv tool install .
```

**Developers:**

```bash
uv sync
```

---

## `leap` Command

All commands are available in two forms:

- **Global** (after installation): `leap <subcommand>`
- **Local** (for development): `uv run python principles_cli.py <subcommand>`

### `review` - Code Review Prompts

Generate prompts for reviewing existing code against engineering principles.

```bash
leap review --platform <platform> --focus <areas>
```

**Options:**

- `--platform`: `android`, `ios`, or `web` (required)
- `--focus`: Comma-separated focus areas (default: `security,accessibility,testing`)
- `--enhanced`: Enable LLM-enhanced patterns (experimental, requires OPENAI_API_KEY)

**Available Focus Areas:**

- `security` - HTTPS, secrets, encryption, input validation
- `accessibility` - Screen readers, WCAG compliance, keyboard navigation
- `testing` - Unit tests, coverage, test quality
- `design` - Design matching, responsive layouts
- `documentation` - README, API docs, inline comments
- `architecture` - Data flow, separation of concerns
- `performance` - Optimization, caching, lazy loading
- `localization` - Internationalization support
- `compatibility` - Version support, browser compatibility

**Examples:**

```bash
# Focus on security and accessibility for web
leap review --platform web --focus security,accessibility

# Review Android code with focus on UI concerns
leap review --platform android --focus accessibility,testing

# Review backend service with focus on security and architecture
leap review --platform web --focus security,architecture

# Just security for iOS
leap review --platform ios --focus security

# Enhanced mode with LLM patterns (requires API key)
leap review --platform web --focus security --enhanced

# Development usage
uv run python principles_cli.py review --platform web --focus security,accessibility
```

### `generate` - Code Writing Prompts

Generate prompts for writing new code that follows principles.

```bash
leap generate --platform <platform> --component <type>
```

**Options:**

- `--platform`: `android`, `ios`, or `web` (required)
- `--component`: `ui`, `business-logic`, or `data-layer` (default: `ui`)

**What's Included:**

- Engineering culture: Livefront mantras and core values
- Focused principles: Relevant for component type
- Platform requirements: Approved dependencies, tools, version requirements
- Component guidance: Platform-specific "always" and "never" rules
- Common mistakes: Top pitfalls to avoid

**Examples:**

```bash
# Generate UI component prompt for web (includes accessibility guidance)
leap generate --platform web --component ui

# Generate business logic prompt for Android (includes testing guidance)
leap generate --platform android --component business-logic

# Generate data layer prompt (includes security guidance)
leap generate --platform ios --component data-layer

# Development usage
uv run python principles_cli.py generate --platform web --component ui
```

### `architecture` - Architecture Guidance

Generate architectural guidance for specific layers.

```bash
leap architecture --platform <platform> --layer <layer>
```

**Options:**

- `--platform`: `android`, `ios`, or `web` (required)
- `--layer`: Architecture layer to focus on

**Examples:**

```bash
# Get architecture guidance for Android
leap architecture --platform android --layer business-logic

# Get web architecture patterns
leap architecture --platform web

# Development usage
uv run python principles_cli.py architecture --platform web
```

### `dependencies` - Dependency Evaluation

Generate prompts for evaluating third-party dependencies.

```bash
leap dependencies --platform <platform> <dependency1> <dependency2> ...
```

**Options:**

- `--platform`: `android`, `ios`, or `web` (required)
- List of dependency names to evaluate

**Output Includes:**

- Approval status (✅ APPROVED or ❌ NOT APPROVED)
- Build vs buy analysis
- Security considerations
- Maintenance burden assessment
- Alternative suggestions

**Examples:**

```bash
# Evaluate web dependencies
leap dependencies --platform web lodash axios

# Evaluate Android dependencies
leap dependencies --platform android rxjava3 retrofit

# Check if a new dependency aligns with principles
leap dependencies --platform web some-new-library

# Development usage
uv run python principles_cli.py dependencies --platform web lodash axios
```

---

## `leap-eval` Command

Test prompt effectiveness using evaluation test cases with AI models.

### Basic Usage

```bash
leap-eval [options]

# Or in development:
uv run python eval_runner.py [options]
```

### Common Options

- `--prompt-file <file>` - Test a specific prompt file (auto-detects platform/focus from metadata)
- `--platform <platform>` - Override platform detection (android, ios, web)
- `--focus <areas>` - Override focus areas (comma-separated)
- `--principles <list>` - Test specific principles only (comma-separated)
- `--categories <list>` - Test specific categories (e.g., ui_component)
- `--output <file>` - Save results to file (default: stdout)
- `--provider <name>` - AI provider (openai, anthropic, groq, together, ollama)
- `--model <name>` - Specific model to use
- `--no-parallel` - Disable parallel execution
- `--list-providers` - Show available providers and models
- `--compare-prompts` - Compare multiple prompt files
- `--prompt-names` - Custom names for prompts (used with --compare-prompts)

### Examples

**Auto-detect from prompt metadata:**

```bash
# Generate prompt with metadata
leap review --platform web --focus security > prompt.txt

# Test it (auto-detects platform=web, focus=security)
leap-eval --prompt-file prompt.txt
```

**Manual platform and focus:**

```bash
# Override metadata detection
leap-eval --prompt-file prompt.txt --platform android --focus testing
```

**Test specific principles:**

```bash
# Test only security and accessibility
leap-eval --principles security,accessibility

# Test architecture principles
leap-eval --principles architecture
```

**Custom output:**

```bash
# Save results to file
leap-eval --output results.md

# Test with specific provider/model
leap-eval --provider anthropic --output claude_results.md
```

**Model comparison:**

```bash
# Compare different models
leap-eval --provider openai --model gpt-4o --output gpt4.md
leap-eval --provider anthropic --output claude.md
leap-eval --provider groq --output groq.md

# Compare results
diff gpt4.md claude.md
```

**Prompt comparison:**

```bash
# Compare multiple prompts
leap-eval --compare-prompts prompt1.md prompt2.md prompt3.md

# With custom names
leap-eval --compare-prompts *.md --prompt-names Security Accessibility General --output comparison.json
```

**Generation tests:**

```bash
# Test generation prompts
leap-eval --categories ui_component

# Test both detection and generation
leap-eval --output full_report.md
```

### Available Test Cases

**Detection Tests** (`evals/detection/`):

- `security_test_cases.yaml` - 10 security violation scenarios
- `accessibility_test_cases.yaml` - 10 accessibility compliance tests
- `testing_test_cases.yaml` - 8 testing principle violations
- `architecture_test_cases.yaml` - 7 architecture pattern violations

**Generation Tests** (`evals/generation/`):

- `ui_component_challenges.yaml` - 6 UI component creation challenges

### Understanding Evaluation Results

Example output:

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

For detailed metric explanations, see [EVALUATION_METRICS.md](EVALUATION_METRICS.md).

### AI Provider Setup

**Supported Providers:**

- OpenAI - <https://platform.openai.com/api-keys> (starts with `sk-`)
- Anthropic - <https://console.anthropic.com/> (starts with `sk-ant-`)
- Groq - <https://console.groq.com/> (starts with `gsk-`)
- Together AI - <https://api.together.xyz/>
- Ollama - <https://ollama.ai/> (local, no key needed)

**Set up API keys:**

```bash
# Create .env file
cp .env.example .env
# Edit .env and add your API keys

# Or use environment variables
export OPENAI_API_KEY=sk-your-api-key-here
export ANTHROPIC_API_KEY=sk-ant-your-api-key-here
```

**Configuration priority:**

1. Command line args (`--provider`, `--model`)
2. Config file (`eval_config.yaml`)
3. Environment variables
4. Built-in defaults

### Local Development (No API Costs)

```bash
# Install and use Ollama for free local testing
curl https://ollama.ai/install.sh | sh
ollama pull llama3.1
leap-eval --provider ollama
```

---

## Platform-Specific Considerations

### Android

- **Minimum SDK**: 24
- **Target SDK**: 28
- **Approved dependencies**: Dagger, RxJava2, RxBinding, RxPermissions, RxLocation, Retrofit
- **Tools**: lint, ktlint, detekt, danger-shroud
- **Layouts**: Responsive, portrait/landscape, phone only
- **Security**: EncryptedSharedPreferences for private data

### iOS

- **Minimum version**: iOS 12+
- **Device support**: iPhone only (SE to XS Max)
- **Dependencies**: First-party only (no third-party libraries)
- **Tools**: SwiftLint, Slather
- **Layouts**: Code-based (no nibs/storyboards)
- **Security**: Keychain for private data

### Web

- **Browser support**: Chrome, Safari, Firefox, Edge, IE 11
- **Screen support**: Mobile, Tablet, Desktop
- **Dependencies**: React, Redux, TypeScript, Jest, Yarn, Webpack, Gatsby
- **Tools**: eslint, stylelint, tsc
- **Layouts**: Responsive, mobile-first
- **Markup**: Semantic HTML, WCAG 2.1 compliance

---

## Advanced Usage

### Focus Area Combinations

**UI Code:**

```bash
leap review --platform web --focus accessibility,design,code_quality
```

**Business Logic:**

```bash
leap review --platform android --focus testing,architecture,minimal_dependencies
```

**Data Layer:**

```bash
leap review --platform web --focus security,testing,unidirectional_data_flow
```

### Real-World Workflow

```bash
# 1. Generate code for the new feature
leap generate --platform web --component ui > feature_prompt.txt

# 2. Use prompt with your AI assistant to write initial code
cat feature_prompt.txt | your-ai-tool

# 3. Review the generated code
leap review --platform web --focus security,accessibility > review_prompt.txt

# 4. Use review prompt to check compliance
cat review_prompt.txt | your-ai-tool --input generated_code.tsx

# 5. Test prompt effectiveness
leap-eval --prompt-file review_prompt.txt
```

### Testing Prompt Effectiveness

```bash
# Test default improved prompts (85% accuracy)
leap-eval --principles security,accessibility --output baseline.md

# Test with enhanced mode
leap review --platform web --focus security --enhanced > enhanced.txt
leap-eval --prompt-file enhanced.txt --output enhanced_results.md

# Compare detection modes
diff baseline.md enhanced_results.md

# Test generation prompts create compliant code
leap-eval --categories ui_component --output generation_report.md
```

---

## Shell Aliases

### For Global Commands

```bash
alias pr='leap'
alias pr-web='leap review --platform web'
alias pr-android='leap review --platform android'
alias pr-ios='leap review --platform ios'
alias pr-eval='leap-eval'
```

### For Local Development

```bash
alias pr='uv run python principles_cli.py'
alias pr-web='pr review --platform web'
alias pr-android='pr review --platform android'
alias pr-ios='pr review --platform ios'
alias pr-eval='uv run python eval_runner.py'
```

---

## Help Commands

```bash
# Get help for main CLI
leap --help

# Get help for specific commands
leap review --help
leap generate --help
leap architecture --help
leap dependencies --help

# Get help for evaluation runner
leap-eval --help

# List available providers
leap-eval --list-providers
```
