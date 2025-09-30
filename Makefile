# Engineering Principles Development Makefile

.PHONY: help install test test-cov lint lint-fix format format-check typecheck clean pre-commit all ci watch install-hooks mcp-server mcp-test

# Default target
help:
	@echo "Available commands:"
	@echo "  install     Install project dependencies"
	@echo "  test        Run all tests"
	@echo "  test-cov    Run tests with coverage report"
	@echo "  lint        Run linting (ruff)"
	@echo "  lint-fix    Run linting with auto-fix"
	@echo "  format      Format code (black + ruff)"
	@echo "  format-check Check code formatting"
	@echo "  typecheck   Run type checking (mypy)"
	@echo "  pre-commit  Run all quality checks (lint + format + typecheck + test)"
	@echo "  clean       Clean up generated files"
	@echo "  all         Run full pipeline (install + pre-commit)"
	@echo ""
	@echo "MCP Server:"
	@echo "  mcp-server  Start the LEAP MCP server for AI agent integration"
	@echo "  mcp-test    Test MCP server startup (checks for errors)"
	@echo ""
	@echo "CI/CD:"
	@echo "  ci          CI pipeline (install + pre-commit)"
	@echo ""
	@echo "Development helpers:"
	@echo "  watch       Watch files and run tests on changes"
	@echo "  install-hooks Install pre-commit hooks"

# Setup targets
install:
	@echo "Installing dependencies..."
	uv sync

# Quality assurance targets
test:
	@echo "Running tests..."
	uv run pytest

test-cov:
	@echo "Running tests with coverage..."
	uv run pytest --cov-report=term-missing --cov-report=html

lint:
	@echo "Running linter..."
	uv run ruff check .

lint-fix:
	@echo "Running linter with auto-fix..."
	uv run ruff check . --fix

format:
	@echo "Formatting code..."
	uv run black .
	uv run ruff format .

format-check:
	@echo "Checking code formatting..."
	uv run black --check .
	uv run ruff format --check .

typecheck:
	@echo "Running type checker..."
	uv run mypy .

pre-commit: lint format typecheck test
	@echo "All quality checks passed!"

# Maintenance targets
clean:
	@echo "Cleaning up..."
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

all: install pre-commit
	@echo "Full pipeline completed!"

# CI/CD target
ci: install pre-commit
	@echo "CI pipeline completed!"

# Development helpers
watch:
	@echo "👀 Watching for changes and running tests..."
	@command -v fswatch >/dev/null 2>&1 || (echo "❌ fswatch not installed. Install with: brew install fswatch" && exit 1)
	fswatch -o . --exclude='.git' --exclude='htmlcov' --exclude='.pytest_cache' | xargs -n1 -I{} make test

install-hooks:
	@echo "🪝 Installing pre-commit hooks..."
	uv run pre-commit install

# MCP Server targets
mcp-server:
	@echo "🚀 Starting LEAP MCP server..."
	@echo "📖 Server will run on stdio for AI agent integration"
	@echo "🛑 Press Ctrl+C to stop"
	uv run python leap_mcp_server.py

mcp-test:
	@echo "🧪 Testing MCP server startup..."
	@echo "Checking dependencies and server initialization..."
	@uv run python -c "from leap_mcp_server import server; print('✅ MCP server imports successfully')" 2>&1 || echo "❌ MCP server import failed"
	@echo "Verifying LEAP data loading..."
	@uv run python -c "from leap import LeapLoader; loader = LeapLoader(); loader.load_principles(); print('✅ LEAP data loads successfully')" 2>&1 || echo "❌ LEAP data loading failed"
