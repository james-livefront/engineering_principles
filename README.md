# Livefront Engineering Principles

AI-powered code review and generation that enforces consistent engineering standards across Android, iOS, and Web platforms. Generates prompts with 85% accuracy for detecting security, accessibility, and architecture violations.

## Quick Start

```bash
# Install
git clone <repo-url> && cd engineering_principles
uv sync

# Generate a code review prompt for your platform
uv run python principles_cli.py review --platform web --focus security,accessibility

# Generate a code writing prompt
uv run python principles_cli.py generate --platform android --component ui

# Test prompt effectiveness (optional)
uv run python eval_runner.py --init-config eval_config.yaml
# Add API keys to eval_config.yaml, then:
uv run python eval_runner.py --mode detection
```

## The 15 Core Principles

1. **Security** - HTTPS everywhere, no secrets in source
2. **Accessibility** - WCAG 2.1, screen reader support  
3. **Testing** - 80% coverage on business logic
4. **Zero TODOs** - Track work in tickets, not code
5. **Code Reviews** - Every line peer-reviewed
6. **Zero Warnings** - Clean build output
7. **Design Integrity** - Match designs exactly
8. **Unidirectional Data Flow** - Predictable state management
9. **Code Consistency** - Platform linters and style guides
10. **Flexible Layout** - All screen sizes and orientations
11. **Localization** - No hard-coded strings
12. **Minimal Dependencies** - Reduce third-party risk
13. **Documentation** - README with setup/build/test
14. **Compatibility** - Support required versions
15. **Continuous Integration** - Automated quality checks

**Priority:** Security > Accessibility > Testing > Performance > Code Style

## CLI Commands

### `review` - Generate code review prompts

```bash
uv run python principles_cli.py review --platform <android|ios|web> --focus <areas>

# Examples
uv run python principles_cli.py review --platform web --focus security
uv run python principles_cli.py review --platform ios --focus security,accessibility,testing
```

### `generate` - Generate code writing prompts

```bash
uv run python principles_cli.py generate --platform <android|ios|web> --component <ui|business-logic|data-layer>

# Examples  
uv run python principles_cli.py generate --platform android --component ui
uv run python principles_cli.py generate --platform web --component business-logic
```

## Platform Requirements

**Android:** SDK 24+, Dagger, RxJava2, Retrofit, lint/ktlint/detekt  
**iOS:** iOS 12+, first-party only, SwiftLint, code-based layouts  
**Web:** React, TypeScript, Jest, eslint/stylelint, IE 11+

## Documentation

- [Evaluation Framework](docs/evaluation.md) - Test prompts with AI models
- [Integration Guide](docs/integration.md) - CI/CD, VS Code, Git hooks  
- [API Providers](docs/api-providers.md) - OpenAI, Anthropic, Ollama setup
- [Development](docs/development.md) - Contributing and architecture

## Philosophy

> "Livefront Engineers are craftspeople."

We don't defer work. The design is the spec.
