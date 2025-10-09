# CLI Reference

Reference for the engineering principles CLI.

## Installation

**End users:**

```bash
uv tool install .
```

**Developers:**

```bash
uv sync
```

---

## Commands

All commands are available in two forms:

- **Global** (after `uv tool install .`): `leap`, `leap-eval`, `leap-mcp-server`
- **Local** (for development): `uv run python principles_cli.py`, `uv run python eval_runner.py`

### `review` - Code Review Prompts

**Global:**

```bash
leap review --platform <android|ios|web> [--focus <areas>] [--enhanced]
```

**Local:**

```bash
uv run python principles_cli.py review --platform <android|ios|web> [--focus <areas>] [--enhanced]
```

**Default focus**: `security,accessibility,testing`

**Options:**
- `--enhanced`: Enhance prompt with latest 2024/2025 practices using OpenAI (requires `OPENAI_API_KEY`)

**Examples:**

```bash
# Using global command
leap review --platform web --focus security,accessibility
leap review --platform android --focus security
leap review --platform ios  # uses default focus
leap review --platform web --enhanced  # AI-enhanced with latest patterns

# Using local command (development)
uv run python principles_cli.py review --platform web --focus security,accessibility
uv run python principles_cli.py review --platform android --focus security --enhanced
```

### `generate` - Code Writing Prompts

**Global:**

```bash
leap generate --platform <android|ios|web> [--component <type>] [--enhanced]
```

**Local:**

```bash
uv run python principles_cli.py generate --platform <android|ios|web> [--component <type>] [--enhanced]
```

**Component types**: `ui` (default), `business-logic`, `data-layer`

**Options:**
- `--enhanced`: Enhance prompt with latest 2024/2025 practices using OpenAI (requires `OPENAI_API_KEY`)

**Examples:**

```bash
# Using global command
leap generate --platform web --component ui
leap generate --platform android --component business-logic
leap generate --platform ios  # defaults to ui component
leap generate --platform web --enhanced  # AI-enhanced code generation prompt

# Using local command (development)
uv run python principles_cli.py generate --platform web --component ui --enhanced
```

### `architecture` - Architecture Guidance

**Global:**

```bash
leap architecture --platform <android|ios|web> [--layer <layer>]
```

**Local:**

```bash
uv run python principles_cli.py architecture --platform <android|ios|web> [--layer <layer>]
```

**Layer types**: `presentation`, `business`, `data`

**Examples:**

```bash
# Using global command
leap architecture --platform web --layer data
leap architecture --platform ios --layer presentation

# Using local command (development)
uv run python principles_cli.py architecture --platform web --layer data
```

### `dependencies` - Dependency Evaluation

**Global:**

```bash
leap dependencies --platform <android|ios|web> --check <deps>
```

**Local:**

```bash
uv run python principles_cli.py dependencies --platform <android|ios|web> --check <deps>
```

**Examples:**

```bash
# Using global command
leap dependencies --platform web --check react,lodash
leap dependencies --platform android --check rxjava,retrofit,gson

# Using local command (development)
uv run python principles_cli.py dependencies --platform web --check react,lodash
```

## Focus Areas

- `security` - HTTPS, secrets, encryption
- `accessibility` - Screen readers, WCAG compliance
- `testing` - Unit tests, coverage, quality
- `design` - Design matching, responsive layouts
- `documentation` - README, API docs, comments
- `architecture` - Data flow, separation of concerns
- `performance` - Optimization, caching
- `localization` - Internationalization
- `compatibility` - Version support

### `eval` - Test Prompt Effectiveness

**Global:**

```bash
leap-eval [options]
```

**Local:**

```bash
uv run python eval_runner.py  [options]
```

**Options:**

- `--principles`: Specific principles to test (detection mode)
- `--categories`: Specific categories to test (generation mode)
- `--output`: Output file for report
- `--prompt-file`: File containing prompt to test
- `--compare-prompts`: Compare multiple prompt files (.txt, .md)
- `--prompt-names`: Custom names for prompts (optional, used with --compare-prompts)
- `--no-parallel`: Disable parallel evaluation (enabled by default)

**Examples:**

```bash
# Using global command
leap-eval
leap-eval --principles security accessibility
leap-eval --prompt-file my_prompt.txt --output report.md
leap-eval --categories ui_component

# Compare multiple prompts
leap-eval --compare-prompts prompt1.md prompt2.md prompt3.md
leap-eval --compare-prompts *.md --prompt-names Security Accessibility General --output comparison.json

# Using local command (development)
uv run python eval_runner.py
uv run python eval_runner.py --principles security accessibility
uv run python eval_runner.py --prompt-file my_prompt.txt --output report.md

# Compare multiple prompts (local)
uv run python eval_runner.py --compare-prompts prompt1.md prompt2.md
```

## Common Patterns

### Using Global Commands (After pipx install)

```bash
# Daily code review
leap review --platform web --focus security,accessibility

# Before starting new feature
leap generate --platform android --component ui

# Architecture decisions
leap architecture --platform ios --layer business

# Dependency evaluation
leap dependencies --platform web --check new-library

# Test prompt effectiveness
leap-eval --principles security
```

### Using Local Commands (Development)

```bash
# Daily code review
uv run python principles_cli.py review --platform web --focus security,accessibility

# Before starting new feature
uv run python principles_cli.py generate --platform android --component ui

# Architecture decisions
uv run python principles_cli.py architecture --platform ios --layer business

# Dependency evaluation
uv run python principles_cli.py dependencies --platform web --check new-library

# Test prompt effectiveness
uv run python eval_runner.py --principles security
```

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

For complete documentation, see [README.md](README.md).
