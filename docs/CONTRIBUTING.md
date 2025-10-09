# Contributing to LEAP

Guide for developers working on the LEAP project.

## Development Setup

### Prerequisites

- Python 3.11+
- Git
- uv package manager

### Quick Setup

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

---

## Project Structure

```text
engineering_principles/
├── leap/                       # Main package
│   ├── core/                   # Shared knowledge base
│   │   ├── philosophy.yaml     # Core values and mantras
│   │   ├── principles.yaml     # All 15 engineering principles
│   │   ├── platforms.yaml      # Platform-specific configurations
│   │   └── enforcement.yaml    # How principles are enforced
│   │
│   ├── modules/
│   │   ├── detection/          # For code review and analysis
│   │   │   ├── rules/          # Detection patterns by principle
│   │   │   ├── severity.yaml   # Issue severity mappings
│   │   │   └── context.yaml    # Context identification rules
│   │   │
│   │   └── generation/         # For code creation
│   │       ├── examples/       # Positive pattern examples
│   │       └── guidance.yaml   # Implementation guidance
│   │
│   ├── loaders.py              # YAML data loading
│   ├── prompt_builder.py       # Prompt generation
│   └── prompt_enhancer.py      # LLM enhancement (experimental)
│
├── evals/                      # Evaluation datasets
│   ├── detection/              # Test cases for detection
│   └── generation/             # Test cases for generation
│
├── tests/                      # Unit tests
├── docs/                       # Documentation
├── principles_cli.py           # Command-line interface
├── eval_runner.py              # Evaluation framework
└── leap_mcp_server.py          # MCP server implementation
```

---

## Development Tools

This project uses modern Python tooling:

- **uv** - Fast Python package manager and virtual environment manager
- **pytest** - Testing framework with coverage reporting
- **ruff** - Fast Python linter (replaces flake8, isort, etc.)
- **black** - Code formatting
- **mypy** - Static type checking
- **pre-commit** - Git hooks for code quality

---

## Running Tests

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

### Writing Tests

```python
# tests/test_my_feature.py
import pytest
from leap.loaders import LeapLoader

def test_principle_loading():
    """Test that principles load correctly"""
    loader = LeapLoader()
    principles = loader.load_principles()

    assert len(principles) == 15
    assert "security" in principles
    assert principles["security"]["priority"] == "critical"

@pytest.fixture
def sample_prompt():
    """Fixture for test prompts"""
    return "Test prompt content"

def test_enhancement(sample_prompt):
    """Test prompt enhancement"""
    # Test implementation
    pass
```

---

## Code Quality

### Linting and Formatting

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

### Code Style Standards

- **Line length**: 88 characters (Black default)
- **Type hints**: All public functions must have type hints
- **Docstrings**: All modules, classes, and public functions
- **Import order**: Sorted by ruff/isort rules
- **Naming**: PEP 8 conventions

**Example:**

```python
from pathlib import Path
from typing import Dict, List

def load_principles(path: Path) -> Dict[str, List[str]]:
    """Load engineering principles from YAML file.

    Args:
        path: Path to principles YAML file

    Returns:
        Dictionary mapping principle names to their rules

    Raises:
        FileNotFoundError: If YAML file doesn't exist
    """
    # Implementation
    pass
```

---

## Development Helpers

```bash
make help          # Show all available commands
make install       # Install project dependencies
make clean         # Clean up generated files
make watch         # Watch files and run tests on changes (requires fswatch)
make install-hooks # Install pre-commit git hooks
make ci           # Full CI pipeline (for GitHub Actions)
```

---

## Adding Dependencies

```bash
# Add production dependency
uv add <package-name>

# Add development dependency
uv add --dev <package-name>

# Update all dependencies
uv sync

# Example:
uv add pyyaml
uv add --dev pytest-cov
```

---

## Project Standards

### Test Coverage

- **Minimum**: 25% overall coverage
- **Target**: 80% on business logic
- **Excluded**: Generated code, vendored code
- **CI**: Coverage must not decrease

### Type Coverage

- All public functions must have type hints
- Use `mypy` for static type checking
- Prefer explicit types over `Any`

### Documentation

- All modules must have module-level docstrings
- All classes must have class-level docstrings
- All public functions must have docstrings with:
  - Description
  - Args
  - Returns
  - Raises (if applicable)

**Example:**

```python
"""Module for loading LEAP configuration data.

This module provides the LeapLoader class for loading and
validating YAML configuration files containing engineering
principles, platforms, and detection rules.
"""

class LeapLoader:
    """Loads and validates LEAP configuration data from YAML files.

    The loader reads YAML files from the leap/core directory and
    provides structured access to principles, platforms, and rules.
    """

    def load_principles(self, path: Path | None = None) -> dict:
        """Load engineering principles from YAML file.

        Args:
            path: Optional path to principles file. If None, uses default.

        Returns:
            Dictionary containing principles organized by category.

        Raises:
            FileNotFoundError: If YAML file doesn't exist.
            yaml.YAMLError: If YAML syntax is invalid.
        """
        pass
```

---

## Adding New Features

### Adding a New Principle

1. Add to `leap/core/principles.yaml` with rationale
2. Create detection rules in `leap/modules/detection/rules/`
3. Add generation guidance in `leap/modules/generation/guidance.yaml`
4. Create test cases in `evals/detection/` or `evals/generation/`
5. Update documentation in README.md and relevant docs

**Example:**

```yaml
# leap/core/principles.yaml
performance:
  description: "Optimize for speed and resource efficiency"
  priority: "recommended"
  rationale: "Fast applications provide better user experience"
  applies_to: ["all"]
```

```yaml
# leap/modules/detection/rules/performance.yaml
patterns:
  - name: "Inefficient Loop"
    severity: "recommended"
    pattern: 'for.*in.*range\(len\('
    message: "Consider using enumerate() or direct iteration"
```

### Updating Platform Requirements

1. Modify `leap/core/platforms.yaml`
2. Update platform-specific detection rules
3. Test with representative codebases
4. Update documentation in docs/CLI_REFERENCE.md

### Adding a New Command

1. Add subcommand to `principles_cli.py`
2. Implement command logic
3. Add tests in `tests/`
4. Update CLI_REFERENCE.md
5. Update help text

**Example:**

```python
# principles_cli.py
@click.command()
@click.option('--platform', required=True)
def my_command(platform: str) -> None:
    """Description of what this command does."""
    # Implementation
    pass

cli.add_command(my_command)
```

---

## Testing Your Changes

### Local Testing

```bash
# Run all tests
uv run pytest

# Run specific test
uv run pytest tests/test_loaders.py -v

# Run with coverage
uv run pytest --cov=leap --cov-report=html

# Test CLI commands
uv run python principles_cli.py review --platform web
uv run python eval_runner.py --help
```

### Testing MCP Server

```bash
# Start server manually
uv run python leap_mcp_server.py

# Test with Claude Desktop (development mode)
# Edit ~/Library/Application Support/Claude/claude_desktop_config.json:
{
  "mcpServers": {
    "leap": {
      "command": "/absolute/path/to/.venv/bin/python",
      "args": ["/absolute/path/to/leap_mcp_server.py"],
      "cwd": "/absolute/path/to/engineering_principles"
    }
  }
}

# Restart Claude Desktop to test
```

### Integration Testing

```bash
# Test full workflow
leap review --platform web > review.txt
leap-eval --prompt-file review.txt

# Test all platforms
for platform in android ios web; do
  leap review --platform $platform --focus security > ${platform}_review.txt
  leap-eval --prompt-file ${platform}_review.txt
done
```

---

## Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make your changes**
   - Follow code style standards
   - Add tests for new functionality
   - Update documentation

3. **Run quality checks**
   ```bash
   make pre-commit
   # Or:
   uv run pre-commit run --all-files
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add my feature"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/my-feature
   # Create PR on GitHub
   ```

6. **Address review feedback**
   - Make requested changes
   - Push updates to same branch
   - PR will update automatically

---

## Commit Message Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring
- `style:` - Formatting changes
- `chore:` - Build/tooling changes

**Examples:**

```bash
git commit -m "feat: add support for Kotlin detection rules"
git commit -m "fix: correct YAML parsing for nested structures"
git commit -m "docs: update CLI reference with new commands"
git commit -m "test: add coverage for prompt enhancement"
```

---

## Release Process

1. Update version in `pyproject.toml`
2. Update documentation if needed
3. Run full test suite: `make ci`
4. Create git tag: `git tag v1.2.3`
5. Push tag: `git push origin v1.2.3`
6. CI will handle the rest

---

## Debugging Tips

### Enable verbose logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Debug MCP server

```bash
# Run with Python debugger
uv run python -m pdb leap_mcp_server.py

# Add breakpoints in code
import pdb; pdb.set_trace()
```

### Debug CLI

```bash
# Run with verbose output
uv run python -v principles_cli.py review --platform web

# Check Python path
uv run python -c "import sys; print(sys.path)"

# Verify imports
uv run python -c "from leap.loaders import LeapLoader; print('OK')"
```

### Debug tests

```bash
# Run tests with debugging
uv run pytest --pdb

# Run single test with verbose
uv run pytest tests/test_loaders.py::test_load_principles -vv

# Print output
uv run pytest -s
```

---

## Getting Help

- **Questions**: Open a GitHub discussion
- **Bugs**: Create a GitHub issue
- **Features**: Create a GitHub issue with [Feature Request] tag
- **Security**: Email security@livefront.com

---

## Code Review Checklist

Before requesting review, ensure:

- [ ] Tests pass (`make test`)
- [ ] Code style follows standards (`make lint`)
- [ ] Type checking passes (`make typecheck`)
- [ ] Documentation is updated
- [ ] YAML files are valid
- [ ] Commit messages follow conventions
- [ ] PR description explains changes clearly
- [ ] Breaking changes are documented
