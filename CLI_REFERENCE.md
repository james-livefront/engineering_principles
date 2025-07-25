# CLI Reference

Quick reference for daily usage of the engineering principles CLI.

## Commands

### `review` - Code Review Prompts

```bash
python principles_cli.py review --platform <android|ios|web> [--focus <areas>]
```

**Default focus**: `security,accessibility,testing`

**Examples:**

```bash
python principles_cli.py review --platform web --focus security,accessibility
python principles_cli.py review --platform android --focus security
python principles_cli.py review --platform ios  # uses default focus
```

### `generate` - Code Writing Prompts

```bash
python principles_cli.py generate --platform <android|ios|web> [--component <type>]
```

**Component types**: `ui` (default), `business-logic`, `data-layer`

**Examples:**

```bash
python principles_cli.py generate --platform web --component ui
python principles_cli.py generate --platform android --component business-logic
python principles_cli.py generate --platform ios  # defaults to ui component
```

### `architecture` - Architecture Guidance

```bash
python principles_cli.py architecture --platform <android|ios|web> [--layer <layer>]
```

**Layer types**: `presentation`, `business`, `data`

**Examples:**

```bash
python principles_cli.py architecture --platform web --layer data
python principles_cli.py architecture --platform ios --layer presentation
```

### `dependencies` - Dependency Evaluation

```bash
python principles_cli.py dependencies --platform <android|ios|web> --check <deps>
```

**Examples:**

```bash
python principles_cli.py dependencies --platform web --check react,lodash
python principles_cli.py dependencies --platform android --check rxjava,retrofit,gson
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

### `eval_runner` - Test Prompt Effectiveness

```bash
python eval_runner.py --mode <detection|generation|both> [options]
```

**Options:**

- `--mode`: `detection`, `generation`, or `both`
- `--principles`: Specific principles to test (detection mode)
- `--categories`: Specific categories to test (generation mode)
- `--output`: Output file for report
- `--prompt-file`: File containing prompt to test

**Examples:**

```bash
# Test detection across all principles
python eval_runner.py --mode detection

# Test specific principles only
python eval_runner.py --mode detection --principles security accessibility

# Test custom prompt file (defaults to detection mode, all principles)
python eval_runner.py --prompt-file my_prompt.txt --output report.md

# Test custom prompt with specific principles
python eval_runner.py --prompt-file my_prompt.txt --principles security accessibility

# Test generation challenges
python eval_runner.py --mode generation --categories ui_component
```

## Common Patterns

```bash
# Daily code review
python principles_cli.py review --platform web --focus security,accessibility

# Before starting new feature
python principles_cli.py generate --platform android --component ui

# Architecture decisions
python principles_cli.py architecture --platform ios --layer business

# Dependency evaluation
python principles_cli.py dependencies --platform web --check new-library

# Test prompt effectiveness
python eval_runner.py --mode detection --principles security
```

## Shell Aliases

```bash
alias pr='python path/to/principles_cli.py'
alias pr-web='pr review --platform web'
alias pr-android='pr review --platform android'
alias pr-ios='pr review --platform ios'
```

For complete documentation, see [README.md](README.md).
