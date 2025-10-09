# LEAP - Livefront Engineering Automated Principles

Modular system for encoding engineering principles through AI-assisted code detection and generation. MCP server provides real-time access to principles, detection patterns, and enforcement specs for AI agents.

**Experimental.** Open questions: How to translate human principles into patterns LLMs can reliably apply? What makes valid evals? Balance between hard-coded rules vs LLM analysis?

> "Livefront Engineers are craftspeople who give a damn about building software that is reliable, performant, maintainable, and remarkably fun to use."

---

## Quick Start

### Installation

```bash
./install.sh
# Or with uv:
uv tool install .
```

This creates isolated environment and makes `leap`, `leap-mcp-server`, `leap-eval` globally available. Requires Python 3.11+.

**Install uv separately (one-time):**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### MCP Server Setup

After installation, add to Claude Desktop config:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "leap": {
      "command": "leap-mcp-server"
    }
  }
}
```

**Claude Code:** `~/.config/claude-code/mcp.json`

```json
{
  "$import": "~/Library/Application Support/Claude/claude_desktop_config.json"
}
```

Restart Claude Desktop. AI agents can now query LEAP directly for principles, patterns, and enforcement specs.

### Basic Usage

**Generate code review prompt:**

```bash
leap review --platform web --focus security

# With LLM enhancement (experimental, requires OPENAI_API_KEY)
leap review --platform web --focus security --enhanced
```

**Generate code writing prompt:**

```bash
leap generate --platform android --component ui
```

**Test prompt effectiveness:**

```bash
leap-eval --prompt-file my_prompt.txt
```

---

## What It Enforces

### The 15 Principles

**Priority:** Security > Accessibility > Testing > Performance > Code Style

1. **Security** - HTTPS everywhere, no secrets in source
2. **Accessibility** - Equal access for all abilities
3. **Testing** - 80% minimum coverage on business logic
4. **Code Reviews** - Every line peer-reviewed
5. **Zero TODOs** - Track work via tickets, not comments
6. **Zero Build Warnings** - Clean build output
7. **Design Integrity** - Match designs exactly
8. **Code Consistency** - Uniform style across platforms
9. **Unidirectional Data Flow** - Predictable state management
10. **Flexible Layout** - All screen sizes and orientations
11. **Localization** - Support any locale
12. **Minimal Dependencies** - Reduce third-party risk
13. **Compatibility** - Document required versions
14. **Documentation** - README with setup/build/test info
15. **Continuous Integration** - Automated quality checks

### Severity System

- **Critical**: Security/accessibility blocking merge → Immediate fix required
- **Blocking**: Test gaps, warnings, TODOs → Must fix before merge
- **Required**: Design deviations, missing docs → Should fix before merge
- **Recommended**: Style issues, best practices → Improve when possible
- **Informational**: Suggestions and tips → Consider for future

---

## Usage

### MCP Server (Primary Use Case)

AI agents automatically access LEAP:

- Code review → calls `get_detection_patterns`
- Code generation → calls `get_generation_guidance`
- Dependency check → calls `validate_dependency`

**Available Tools:**

1. `get_principles` - Engineering principles filtered by platform/focus
2. `get_detection_patterns` - Regex patterns for violations
3. `get_generation_guidance` - Code writing guidance
4. `get_platform_requirements` - Platform-specific requirements
5. `get_enforcement_specs` - CI implementation guidance
6. `validate_dependency` - Dependency approval check
7. `get_severity_guidance` - Severity classification rules

**Manual queries:**

```
"What are security principles for web?"
→ calls get_principles(platform=web, focus_areas=["security"])

"Is lodash approved for web?"
→ calls validate_dependency(package=lodash, platform=web)
```

### CLI Commands

**Code Review:**

```bash
leap review --platform web --focus security,accessibility
leap review --platform android --focus testing
leap review --platform ios --focus security --enhanced
```

**Code Generation:**

```bash
leap generate --platform web --component ui
leap generate --platform android --component business-logic
leap generate --platform ios --component data-layer
```

**Architecture Guidance:**

```bash
leap architecture --platform web
```

**Dependency Evaluation:**

```bash
leap dependencies --platform web lodash axios
```

For detailed CLI reference, see [docs/CLI_REFERENCE.md](docs/CLI_REFERENCE.md).

---

## Validation

Test prompt effectiveness with evaluation framework:

```bash
# Auto-detect platform/focus from prompt metadata
leap review --platform web --focus security > prompt.txt
leap-eval --prompt-file prompt.txt

# Test specific principles
leap-eval --principles security,accessibility

# Compare models
leap-eval --provider openai --output gpt4.md
leap-eval --provider anthropic --output claude.md
diff gpt4.md claude.md
```

**Performance Metrics:**

| Mode | Accuracy | Precision | Recall | F1 Score |
|------|----------|-----------|--------|----------|
| Rule-Based (Default) | 85% | 84% | 100% | 91% |
| LLM Enhanced (`--enhanced`) | 80% | 88% | 88% | 88% |

Rule-based provides +25% accuracy improvement with 100% recall. Enhanced mode (`--enhanced` flag) adds LLM-generated patterns for latest OWASP/WCAG standards but is experimental and may introduce false positives.

For detailed metrics, see [docs/EVALUATION_METRICS.md](docs/EVALUATION_METRICS.md).

---

## Platform-Specific

**Android:**

- SDK 24+, Target 28
- Approved: Dagger, RxJava2, Retrofit
- Tools: ktlint, detekt, lint
- Security: EncryptedSharedPreferences

**iOS:**

- iOS 12+, iPhone only
- First-party dependencies only
- Tools: SwiftLint, Slather
- Security: Keychain

**Web:**

- Chrome, Safari, Firefox, Edge, IE 11
- Stack: React, Redux, TypeScript, Jest
- Tools: eslint, stylelint, tsc
- Standards: Semantic HTML, WCAG 2.1

---

## Additional Resources

**Documentation:**

- [CLI Reference](docs/CLI_REFERENCE.md) - Complete command documentation
- [Integration Guide](docs/INTEGRATIONS.md) - Git hooks, VS Code, CI/CD
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Installation and runtime issues
- [Contributing](docs/CONTRIBUTING.md) - Development setup and standards
- [Architecture](docs/ARCHITECTURE.md) - System design and data flow
- [Evaluation Metrics](docs/EVALUATION_METRICS.md) - Testing and performance

**Quick Links:**

- [Installation Issues](docs/TROUBLESHOOTING.md#installation-issues)
- [MCP Server Setup](docs/TROUBLESHOOTING.md#mcp-server-issues)
- [Git Hooks](docs/INTEGRATIONS.md#git-hooks)
- [VS Code Tasks](docs/INTEGRATIONS.md#vs-code-integration)
- [CI/CD Examples](docs/INTEGRATIONS.md#cicd-integration)
- [Development Setup](docs/CONTRIBUTING.md#development-setup)

---

## System Architecture

Modular design separating core knowledge from implementation:

```text
leap/
├── core/                # Knowledge base (principles, platforms, philosophy)
├── modules/
│   ├── detection/      # Rules and patterns for code review
│   └── generation/     # Guidance and examples for code writing
└── evals/              # Test cases for validation
```

**Features:**

- Platform-aware (Android, iOS, Web)
- Focus-driven (security, accessibility, testing, etc.)
- Severity-based (Critical → Informational)
- Pattern-based detection (70-85% coverage)
- Cultural context (Livefront mantras and values)
- Real-time MCP access (no copy/paste)

For detailed architecture, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## Examples

### Code Review Workflow

```bash
# Generate review prompt
leap review --platform web --focus security,accessibility > review.txt

# Use with AI assistant
cat review.txt | your-ai-tool --input code.tsx

# Validate effectiveness
leap-eval --prompt-file review.txt
```

### Feature Development Workflow

```bash
# 1. Generate code
leap generate --platform web --component ui > feature_prompt.txt
cat feature_prompt.txt | your-ai-tool

# 2. Review generated code
leap review --platform web --focus security,accessibility > review.txt
cat review.txt | your-ai-tool --input generated_code.tsx

# 3. Test effectiveness
leap-eval --prompt-file review.txt
```

### Integration Patterns

**Git Hook:**

```bash
#!/bin/bash
# .git/hooks/pre-commit
leap review --platform web --focus security,accessibility
```

**VS Code Task:**
See [docs/INTEGRATIONS.md#vs-code-integration](docs/INTEGRATIONS.md#vs-code-integration)

**GitHub Actions:**
See [docs/INTEGRATIONS.md#github-actions](docs/INTEGRATIONS.md#github-actions)

---

## Troubleshooting

### Common Issues

**"leap-mcp-server: command not found"**

```bash
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
uv tool install --force .
```

**"API key required"**

```bash
cp .env.example .env
# Edit .env and add your API keys
```

**MCP server won't start**

```bash
# Check logs
tail -50 ~/Library/Logs/Claude/mcp-server-leap.log

# Test manually
leap-mcp-server

# Reinstall
uv tool install --force .
```

For complete troubleshooting guide, see [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

---

## Contributing

Contributions welcome! See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for:

- Development setup
- Code quality standards
- Testing requirements
- Pull request process

**Quick dev setup:**

```bash
git clone git@github.com:james-livefront/engineering_principles.git
cd engineering_principles
uv sync                    # Install dependencies
uv run pytest              # Run tests
uv run pre-commit install  # Install quality hooks
```
