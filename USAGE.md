# LEAP Usage Guide

Practical guide to using LEAP for AI-powered code review and generation.

## Table of Contents

- [Quick Start](#quick-start)
- [Common Workflows](#common-workflows)
- [Command Reference](#command-reference)
- [Advanced Features](#advanced-features)
- [Tips & Best Practices](#tips--best-practices)
- [Troubleshooting](#troubleshooting)

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd engineering_principles

# Install dependencies using uv
pip install uv
uv sync

# Verify installation
uv run python principles_cli.py --help
```

### Your First Prompt

```bash
# Generate a code review prompt for web security
uv run python principles_cli.py review --platform web --focus security

# Use with your favorite AI tool
uv run python principles_cli.py review --platform web --focus security | pbcopy
# Paste into Claude, ChatGPT, etc.
```

### Test It Out

```bash
# Evaluate how well the prompt works
cp .env.example .env  # Add your API keys
uv run python eval_runner.py --mode detection --platform web --focus security
```

## Common Workflows

### Workflow 1: Reviewing a Pull Request

**Scenario**: You want AI to review a PR for security and accessibility issues.

```bash
# Step 1: Generate review prompt for your platform
uv run python principles_cli.py review \
  --platform web \
  --focus security,accessibility \
  > review_prompt.txt

# Step 2: Use with AI (choose one method)

# Option A: Copy to clipboard
cat review_prompt.txt | pbcopy  # Mac
cat review_prompt.txt | xclip   # Linux

# Option B: Pipe to AI tool directly (if supported)
git diff main...feature-branch | your-ai-tool --prompt "$(cat review_prompt.txt)"

# Option C: Use with GitHub CLI + AI
gh pr diff 123 | your-ai-tool --prompt "$(cat review_prompt.txt)"
```

**Pro tip**: Choose focus areas that match your code type - UI components benefit from accessibility focus, data layers from security focus, business logic from testing focus.

### Workflow 2: Writing New Code with AI

**Scenario**: You're using AI to generate a new React component.

```bash
# Step 1: Generate code creation prompt
uv run python principles_cli.py generate \
  --platform web \
  --component ui \
  > generation_prompt.txt

# Step 2: Use as system prompt with AI
# This sets up the AI with Livefront principles, mantras, and guidance

# Step 3: Make specific requests
# Now the AI knows about accessibility requirements, design integrity,
# platform requirements, etc.
```

**What the AI receives**:
- Livefront engineering culture and mantras
- Platform-specific requirements (React, TypeScript, etc.)
- Component-specific guidance (accessibility for UI, testing for business logic)
- Common mistakes to avoid

### Workflow 3: Evaluating a New Dependency

**Scenario**: A developer wants to add a new npm package.

```bash
# Generate dependency evaluation prompt
uv run python principles_cli.py dependencies \
  --platform web \
  lodash moment

# The AI will evaluate:
# - Is it approved? (checks against platforms.yaml)
# - Security considerations
# - Maintenance burden
# - Build vs buy analysis
```

### Workflow 4: Architecture Review

**Scenario**: Reviewing the data layer architecture for an iOS app.

```bash
# Generate architecture guidance prompt
uv run python principles_cli.py architecture \
  --platform ios \
  --layer data

# Focus areas:
# - Unidirectional data flow
# - Testing requirements
# - Platform-specific patterns
```

### Workflow 5: Testing Prompt Effectiveness

**Scenario**: You updated detection rules and want to measure improvement.

```bash
# Test baseline performance
uv run python eval_runner.py \
  --mode detection \
  --platform web \
  --focus security \
  --output baseline_results.md

# Test with enhanced mode
uv run python eval_runner.py \
  --mode detection \
  --platform web \
  --focus security \
  --enhanced \
  --output enhanced_results.md

# Compare results
diff baseline_results.md enhanced_results.md

# Or show the enhancement diff directly
uv run python eval_runner.py \
  --mode detection \
  --platform web \
  --focus security \
  --enhanced \
```

## Command Reference

### Default Values Summary

**principles_cli.py defaults:**
- `review --focus`: `security,accessibility,testing`
- `generate --component`: `ui`
- `architecture --layer`: `data`

**eval_runner.py defaults:**
- `--mode`: `detection` (not `generation` or `both`)
- `--parallel`: Enabled (use `--no-parallel` to disable)

This means these commands are equivalent:
```bash
# These are the same:
uv run python principles_cli.py review --platform web
uv run python principles_cli.py review --platform web --focus security,accessibility,testing

# These are the same:
uv run python eval_runner.py --prompt-file prompt.txt
uv run python eval_runner.py --mode detection --prompt-file prompt.txt
```

### `review` - Code Review Prompts

Generate prompts for reviewing existing code.

**Basic Usage:**
```bash
python principles_cli.py review --platform <platform> --focus <areas>
```

**Parameters:**
- `--platform` (required): `android`, `ios`, or `web`
- `--focus` (optional): Comma-separated focus areas
  - Default: `security,accessibility,testing`
  - Available: `security`, `accessibility`, `testing`, `architecture`, `code_quality`, `design`, `documentation`

**Examples:**

```bash
# Security-focused review for web
uv run python principles_cli.py review --platform web --focus security

# Multiple focus areas
uv run python principles_cli.py review --platform android --focus security,accessibility,testing

# UI code - focus on accessibility and code quality
uv run python principles_cli.py review --platform ios --focus accessibility,architecture

# Data layer - focus on security and testing
uv run python principles_cli.py review --platform web --focus security,testing
```

**What You Get:**
- Detection patterns for each focus area
- Platform-specific rules
- Severity classifications
- "What Happens Next" - CI checks that should be implemented according to standards
- Specific regex patterns for automated detection

### `generate` - Code Generation Prompts

Generate prompts for writing new code with AI assistance.

**Basic Usage:**
```bash
python principles_cli.py generate --platform <platform> --component <type>
```

**Parameters:**
- `--platform` (required): `android`, `ios`, or `web`
- `--component` (optional): `ui`, `business-logic`, or `data-layer`
  - Default: `ui`

**Examples:**

```bash
# Generate UI component with accessibility guidance
uv run python principles_cli.py generate --platform web --component ui

# Generate business logic with testing guidance
uv run python principles_cli.py generate --platform android --component business-logic

# Generate data layer with security guidance
uv run python principles_cli.py generate --platform ios --component data-layer
```

**What You Get:**
- Livefront engineering culture and mantras
- Focused principles relevant to component type
- Platform-specific requirements and approved dependencies
- Component-specific guidance (always/never rules)
- Common mistakes to avoid
- Platform tools and linting requirements

### `architecture` - Architecture Guidance

Generate architectural guidance for specific layers.

**Basic Usage:**
```bash
python principles_cli.py architecture --platform <platform> --layer <layer>
```

**Parameters:**
- `--platform` (required): `android`, `ios`, or `web`
- `--layer` (optional): `data`, `ui`, or `business-logic`
  - Default: `data`

**Examples:**

```bash
# Data layer architecture
uv run python principles_cli.py architecture --platform web --layer data

# UI layer patterns
uv run python principles_cli.py architecture --platform android --layer ui

# Business logic patterns
uv run python principles_cli.py architecture --platform ios --layer business-logic
```

**What You Get:**
- Unidirectional data flow guidance
- Layer-specific responsibilities
- Platform architecture patterns
- Testing strategies
- State management principles

### `dependencies` - Dependency Evaluation

Evaluate third-party dependencies against principles.

**Basic Usage:**
```bash
python principles_cli.py dependencies --platform <platform> <dependency1> [<dependency2> ...]
```

**Parameters:**
- `--platform` (required): `android`, `ios`, or `web`
- `dependencies` (required): One or more dependency names

**Examples:**

```bash
# Check web dependencies
uv run python principles_cli.py dependencies --platform web lodash moment axios

# Check Android dependencies
uv run python principles_cli.py dependencies --platform android retrofit rxjava3

# Check iOS dependencies (remember: first-party only policy!)
uv run python principles_cli.py dependencies --platform ios alamofire
```

**What You Get:**
- Approval status (approved/not approved)
- List of approved dependencies for platform
- Evaluation criteria (security, maintenance, alignment, impact)
- Minimal dependencies principle
- Instructions for AI to assess each dependency

## Advanced Features

### Focus Area Selection

Choose the right focus areas based on your code type for more effective reviews:

**For UI Components (Recommended: accessibility, architecture):**
```bash
# Android UI review
uv run python principles_cli.py review --platform android --focus accessibility,architecture

# iOS UI review
uv run python principles_cli.py review --platform ios --focus accessibility,architecture

# Web UI review
uv run python principles_cli.py review --platform web --focus accessibility,architecture
```

**For Business Logic (Recommended: testing, architecture):**
```bash
# Web business logic review
uv run python principles_cli.py review --platform web --focus testing,architecture

# Android business logic review
uv run python principles_cli.py review --platform android --focus testing,architecture

# iOS business logic review
uv run python principles_cli.py review --platform ios --focus testing,architecture
```

**For Data/API Layers (Recommended: security, testing):**
```bash
# Web data layer review
uv run python principles_cli.py review --platform web --focus security,testing

# Android data layer review
uv run python principles_cli.py review --platform android --focus security,testing

# iOS data layer review
uv run python principles_cli.py review --platform ios --focus security,testing
```

**Best Practices:**
- UI code: Prioritize `accessibility` and `architecture`
- Business logic: Emphasize `testing` and `architecture`
- Data layers: Focus on `security` and `testing`
- Infrastructure: Consider `security` and `performance`
- You can combine multiple focus areas with commas: `--focus security,accessibility,testing`

### Enhanced Detection Mode

Add LLM-powered intelligence to base pattern detection:

```bash
# Standard detection (recommended)
uv run python eval_runner.py --mode detection --platform web

# With LLM enhancement (experimental)
uv run python eval_runner.py --mode detection --platform web --enhanced

# Show what enhancement adds
uv run python eval_runner.py --mode detection --platform web --enhanced
```

**When to use enhanced mode:**
- Testing for edge cases beyond base patterns
- Exploring latest security/accessibility practices
- Research and experimentation
- When base mode recall is insufficient

**When NOT to use enhanced mode:**
- Production CI/CD (risk of false positives)
- Daily code review (base mode is faster and more consistent)
- When precision matters more than recall

### Evaluation Framework

Test prompt effectiveness with real AI models.

**Default Settings:**
- `--mode`: `detection` (default, no need to specify)
- `--parallel`: Enabled by default (use `--no-parallel` to disable)

```bash
# Basic evaluation (detection mode is default)
uv run python eval_runner.py --platform web

# Specific focus areas
uv run python eval_runner.py --focus security,accessibility

# With specific prompt file
uv run python eval_runner.py --prompt-file my_prompt.txt

# Different AI providers
uv run python eval_runner.py --provider openai --model gpt-4o
uv run python eval_runner.py --provider anthropic --model claude-3-5-sonnet-20241022
uv run python eval_runner.py --provider groq --model llama-3.1-70b-versatile

# Save results
uv run python eval_runner.py --mode detection --output results.md

# Test generation prompts
uv run python eval_runner.py --mode generation --categories ui_component
```

**Metrics Explained:**
- **Accuracy**: % of correct predictions (detected or not detected)
- **Precision**: Of violations flagged, how many were real? (True Positives / (TP + False Positives))
- **Recall**: Of real violations, how many did we catch? (True Positives / (TP + False Negatives))
- **F1 Score**: Balance of precision and recall (harmonic mean)

**Target Metrics:**
- Accuracy: >80%
- Precision: >85% (avoid false positives)
- Recall: >75% (catch most violations)
- F1 Score: >80% (balanced performance)

## Severity System Guide

LEAP includes a comprehensive severity classification system that provides structured guidance to AI assistants for consistent code review feedback. Understanding this system helps you interpret and act on AI-generated review results.

### Severity Levels Explained

**Critical (🚨)**
- **Definition**: Security vulnerabilities, accessibility barriers that prevent users from accessing content
- **Examples**: Hardcoded secrets, missing alt text, insecure HTTP URLs in production
- **AI Behavior**: Flags immediately with security/accessibility impact explanation, provides before/after examples
- **Action Required**: Block merge immediately, notify security team if applicable
- **Detection**: `API_KEY = "sk-1234567890"` → Critical security violation

**Blocking (⛔)**
- **Definition**: Issues that break CI/CD or violate core engineering standards
- **Examples**: Test coverage below 80%, build warnings, TODO comments without tickets
- **AI Behavior**: Requires immediate resolution or detailed justification, shows CI pipeline impact
- **Action Required**: Must fix before merge, no exceptions
- **Detection**: `// TODO: implement this later` → Blocking violation

**Required (⚠️)**
- **Definition**: Deviations from design specs or missing important documentation
- **Examples**: Design mismatches, missing README sections, localization gaps
- **AI Behavior**: Requests fix or explanation of trade-offs, allows documented exceptions
- **Action Required**: Should fix before merge or provide justification
- **Detection**: Button size 40px instead of specified 48px → Required fix

**Recommended (💡)**
- **Definition**: Code quality improvements and best practices
- **Examples**: Complex methods, missing edge case tests, inefficient algorithms
- **AI Behavior**: Suggests improvements without blocking, focuses on maintainability
- **Action Required**: Improve when possible, not merge-blocking
- **Detection**: Method with 50+ lines → Recommended refactoring

**Informational (ℹ️)**
- **Definition**: Suggestions, tips, and educational guidance
- **Examples**: Alternative approaches, performance tips, modern patterns
- **AI Behavior**: Provides educational context and suggestions
- **Action Required**: Consider for future improvements
- **Detection**: Using `.forEach()` instead of `.map()` → Informational suggestion

### Working with Severity Levels

**Understanding AI Output:**
```
🚨 CRITICAL: Hardcoded API key detected at line 15
⛔ BLOCKING: Test coverage is 65%, minimum required is 80%
⚠️ REQUIRED: Button touch target is 40px, should be 48px per design
💡 RECOMMENDED: Consider extracting this 45-line method
ℹ️ INFORMATIONAL: Modern React pattern would use hooks instead of classes
```

**Escalation Guidelines:**
- **Critical/Blocking**: Address immediately, may require team discussion
- **Required**: Fix during current PR cycle or document decision
- **Recommended/Informational**: Address in future iterations

**Focus Area Mapping:**
- **Security focus**: Emphasizes Critical and Blocking security violations
- **Accessibility focus**: Emphasizes Critical accessibility barriers
- **Testing focus**: Emphasizes Blocking test coverage and quality issues
- **Architecture focus**: Emphasizes Required and Recommended structural improvements

## Tips & Best Practices

### For Code Review

**DO:**
- ✅ Choose appropriate focus areas for your code type (UI→accessibility, data→security, business→testing)
- ✅ Combine multiple focus areas when needed: `--focus security,accessibility,testing`
- ✅ Review the generated prompt before using (understand what AI is checking)
- ✅ Start with base detection, only use `--enhanced` for edge cases

**DON'T:**
- ❌ Use `--enhanced` mode in CI/CD (false positive risk)
- ❌ Ignore context - different code needs different checks
- ❌ Skip the "What Happens Next" section - it helps AI understand what CI checks should be implemented
- ❌ Forget to specify platform (Android/iOS/Web have different rules)

### For Code Generation

**DO:**
- ✅ Use `generate` prompts as system prompts (set AI context once)
- ✅ Choose correct component type (ui/business-logic/data-layer)
- ✅ Reference the cultural context - it helps AI make better judgment calls
- ✅ Follow platform-specific guidance (approved dependencies, tools)

**DON'T:**
- ❌ Mix component types (don't use UI prompt for data layer code)
- ❌ Ignore the "never" rules in component guidance
- ❌ Skip platform requirements (they exist for good reasons)
- ❌ Forget about the mantras - they encode important cultural values

### For Evaluation

**DO:**
- ✅ Measure before and after changes (track improvements)
- ✅ Test across multiple platforms if making cross-platform changes
- ✅ Use `--enhanced` flag to improve detection with LLM augmentation
- ✅ Track false positives carefully (they erode trust)

**DON'T:**
- ❌ Optimize for 100% recall at expense of precision
- ❌ Ignore per-category performance (security vs accessibility, etc.)
- ❌ Test with only one AI model (different models behave differently)
- ❌ Forget to update test cases as principles evolve

### Integration Patterns

**Pre-commit Hook:**
```bash
#!/bin/bash
# .git/hooks/pre-commit
echo "Checking engineering principles..."

# Get changed files
CHANGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

for FILE in $CHANGED_FILES; do
  if [[ $FILE == *.kt ]]; then
    PLATFORM="android"
  elif [[ $FILE == *.swift ]]; then
    PLATFORM="ios"
  elif [[ $FILE == *.tsx ]] || [[ $FILE == *.jsx ]]; then
    PLATFORM="web"
  else
    continue
  fi

  # Generate focused review based on file type
  python principles_cli.py review --platform $PLATFORM --focus security,testing > /tmp/review_prompt.txt
  echo "Generated review prompt for: $FILE"
done
```

**VS Code Task:**
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "LEAP: Review Current File",
      "type": "shell",
      "command": "python",
      "args": [
        "${workspaceFolder}/../engineering_principles/principles_cli.py",
        "review",
        "--platform", "web",
        "--focus", "security,accessibility"
      ],
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    }
  ]
}
```

**CI/CD (GitHub Actions):**
```yaml
name: Engineering Principles Check
on: pull_request

jobs:
  leap-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install LEAP
        run: |
          pip install uv
          cd engineering_principles
          uv sync

      - name: Run Evaluation
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          cd engineering_principles
          uv run python eval_runner.py \
            --mode detection \
            --platform web \
            --output $GITHUB_STEP_SUMMARY
```

## Troubleshooting

### "Module not found" errors

**Problem**: `ModuleNotFoundError: No module named 'yaml'`

**Solution**:
```bash
# Reinstall dependencies
uv sync

# Or install production dependencies only
uv install
```

### "API key required" errors

**Problem**: `Error: API key required for evaluation`

**Solutions**:
```bash
# Option 1: Create .env file
cp .env.example .env
# Edit .env and add your API keys

# Option 2: Export environment variables
export OPENAI_API_KEY=sk-your-key-here
export ANTHROPIC_API_KEY=sk-ant-your-key-here

# Option 3: Use config file
# Edit eval_config.yaml with your keys
```

### Empty or missing prompts

**Problem**: Prompt generation produces empty or minimal output

**Check**:
```bash
# Verify YAML files exist and are valid
python -c "import yaml; print(yaml.safe_load(open('core/principles.yaml')))"

# Run from repository root
cd /path/to/engineering_principles
python principles_cli.py review --platform web

# Check CLI help
python principles_cli.py --help
python principles_cli.py review --help
```

### Low evaluation scores

**Problem**: Accuracy below 70%

**Debugging steps**:
1. **Check prompt file**: Is it complete? `cat prompt.txt | head -50`
2. **Verify test cases**: Are they appropriate? `cat evals/detection/security_test_cases.yaml`
3. **Test enhanced mode**: Does it help? `--enhanced`
4. **Check AI provider**: Try different model `--provider anthropic`
5. **Review false positives**: Are patterns too aggressive?

### Focus areas not emphasized in output

**Problem**: The generated prompt doesn't properly emphasize your chosen focus areas

**Check**:
```bash
# Verify valid focus areas
uv run python principles_cli.py review --help
# Available focus areas: security, accessibility, testing, performance, architecture

# Test with specific focus areas
uv run python principles_cli.py review --platform android --focus accessibility,architecture
# Should generate prompt with accessibility and architecture sections prominent

# Verify the prompt includes focus-specific patterns
uv run python principles_cli.py review --platform web --focus security | grep -i "security"
# Should see security-related patterns and instructions
```

### Permission errors

**Problem**: Cannot write to directories

**Solution**:
```bash
# Check permissions
ls -la

# Run from correct directory
cd engineering_principles

# Don't run with sudo (uses wrong Python environment)
```

## Getting Help

- **Documentation**: Check [README.md](README.md) and [docs/](docs/)
- **Examples**: See [docs/evolution.md](docs/evolution.md) for background
- **Issues**: Report bugs at [GitHub Issues](https://github.com/yourorg/leap/issues)
- **Article**: Read the full story in [docs/article.md](docs/article.md)

## Understanding Enforcement Specifications

**Important Distinction**: LEAP's "What Happens Next" section shows **enforcement specifications**, not live CI status.

### What This Means

**Enforcement Specifications** (what LEAP provides):
- Detailed descriptions of CI checks that **should** be implemented
- Sourced from `core/enforcement.yaml` configuration
- Based on Livefront's engineering standards and best practices
- Maps focus areas (security, testing, etc.) to relevant check categories

**Actual CI Implementation** (what teams must build):
- Real `.github/workflows/` files or equivalent CI configuration
- Live running checks that block/approve PRs
- Integration with your specific tooling and infrastructure
- Custom implementation based on your project needs

### How to Use This

1. **For AI Code Review**: The enforcement specifications help AI understand what automated checks should follow manual review
2. **For CI Planning**: Use the specifications as a template for implementing your own CI pipeline
3. **For Standards Communication**: Share what checks your team should implement according to engineering standards

### Example Implementation

When LEAP shows:
```markdown
## What Happens Next: Automated CI Checks

**Security Stage**:
- Scan for secrets using patterns: API keys ≥16 chars, passwords, tokens
- Run dependency vulnerability scanner
- Verify all HTTP URLs use HTTPS
```

Your team should implement:
```yaml
# .github/workflows/security.yml
- name: Secret Scanning
  run: |
    # Implement the patterns LEAP specified
    grep -r "api[_-]?key.*=.*['\"][^'\"]{16,}['\"]" src/
```

This design allows LEAP to provide consistent engineering guidance while giving teams flexibility in CI implementation.

## Next Steps

- **Customize for your team**: Edit YAML files to match your principles
- **Add test cases**: Create `evals/` test cases for your violations
- **Integrate with workflow**: Set up pre-commit hooks or CI/CD
- **Measure effectiveness**: Run evaluations regularly
- **Contribute back**: Share improvements via pull requests
