# CLI Reference

Reference for the engineering principles CLI.

## Installation

**End users:**

```bash
pipx install .
```

**Developers:**

```bash
uv sync
```

---

## Commands

All commands are available in two forms:

- **Global** (after `pipx install .`): `leap-review`, `leap-eval`
- **Local** (for development): `uv run python principles_cli.py`, `uv run python eval_runner.py`

### `review` - Code Review Prompts

**Global:**

```bash
leap-review review --platform <android|ios|web> [--focus <areas>] [--enhanced]
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
leap-review review --platform web --focus security,accessibility
leap-review review --platform android --focus security
leap-review review --platform ios  # uses default focus
leap-review review --platform web --enhanced  # AI-enhanced with latest patterns

# Using local command (development)
uv run python principles_cli.py review --platform web --focus security,accessibility
uv run python principles_cli.py review --platform android --focus security --enhanced
```

### `generate` - Code Writing Prompts

**Global:**

```bash
leap-review generate --platform <android|ios|web> [--component <type>] [--enhanced]
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
leap-review generate --platform web --component ui
leap-review generate --platform android --component business-logic
leap-review generate --platform ios  # defaults to ui component
leap-review generate --platform web --enhanced  # AI-enhanced code generation prompt

# Using local command (development)
uv run python principles_cli.py generate --platform web --component ui --enhanced
```

### `architecture` - Architecture Guidance

**Global:**

```bash
leap-review architecture --platform <android|ios|web> [--layer <layer>]
```

**Local:**

```bash
uv run python principles_cli.py architecture --platform <android|ios|web> [--layer <layer>]
```

**Layer types**: `presentation`, `business`, `data`

**Examples:**

```bash
# Using global command
leap-review architecture --platform web --layer data
leap-review architecture --platform ios --layer presentation

# Using local command (development)
uv run python principles_cli.py architecture --platform web --layer data
```

### `dependencies` - Dependency Evaluation

**Global:**

```bash
leap-review dependencies --platform <android|ios|web> --check <deps>
```

**Local:**

```bash
uv run python principles_cli.py dependencies --platform <android|ios|web> --check <deps>
```

**Examples:**

```bash
# Using global command
leap-review dependencies --platform web --check react,lodash
leap-review dependencies --platform android --check rxjava,retrofit,gson

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
leap-eval --mode <detection|generation|both> [options]
```

**Local:**

```bash
uv run python eval_runner.py --mode <detection|generation|both> [options]
```

**Options:**

- `--mode`: `detection`, `generation`, or `both`
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
leap-eval --mode detection
leap-eval --mode detection --principles security accessibility
leap-eval --prompt-file my_prompt.txt --output report.md
leap-eval --mode generation --categories ui_component

# Compare multiple prompts
leap-eval --compare-prompts prompt1.md prompt2.md prompt3.md
leap-eval --compare-prompts *.md --prompt-names Security Accessibility General --output comparison.json

# Using local command (development)
uv run python eval_runner.py --mode detection
uv run python eval_runner.py --mode detection --principles security accessibility
uv run python eval_runner.py --prompt-file my_prompt.txt --output report.md

# Compare multiple prompts (local)
uv run python eval_runner.py --compare-prompts prompt1.md prompt2.md
```

## Common Patterns

### Using Global Commands (After pipx install)

```bash
# Daily code review
leap-review review --platform web --focus security,accessibility

# Before starting new feature
leap-review generate --platform android --component ui

# Architecture decisions
leap-review architecture --platform ios --layer business

# Dependency evaluation
leap-review dependencies --platform web --check new-library

# Test prompt effectiveness
leap-eval --mode detection --principles security
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
uv run python eval_runner.py --mode detection --principles security
```

## Shell Aliases

### For Global Commands

```bash
alias pr='leap-review'
alias pr-web='leap-review review --platform web'
alias pr-android='leap-review review --platform android'
alias pr-ios='leap-review review --platform ios'
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
