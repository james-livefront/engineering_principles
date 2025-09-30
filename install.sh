#!/bin/bash
# LEAP MCP Server Installation Script
# Makes it easy for anyone to install LEAP, even with minimal Python experience

set -e  # Exit on error

echo "🐸 LEAP MCP Server Installation"
echo "================================"
echo ""

# Check if Python 3.11+ is installed
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    echo "Please install Python 3.11 or later from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.11"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $PYTHON_VERSION found, but Python 3.11+ is required."
    echo "Please install Python 3.11 or later from https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION found"
echo ""

# Check if pipx is installed
echo "Checking for pipx..."
if ! command -v pipx &> /dev/null; then
    echo "📦 Installing pipx..."
    python3 -m pip install --user pipx
    python3 -m pipx ensurepath

    # Reload PATH
    export PATH="$HOME/.local/bin:$PATH"

    if ! command -v pipx &> /dev/null; then
        echo "❌ pipx installation failed. Please run: python3 -m pip install --user pipx"
        exit 1
    fi
fi

echo "✅ pipx is installed"
echo ""

# Install LEAP
echo "📦 Installing LEAP..."
pipx install --force .

if [ $? -eq 0 ]; then
    echo ""
    echo "✨ Installation complete! ✨"
    echo ""
    echo "Available commands:"
    echo "  • leap-mcp-server  - MCP server for AI integration"
    echo "  • leap-review      - Generate code review prompts"
    echo "  • leap-eval        - Run evaluation tests"
    echo ""
    echo "Next steps:"
    echo "1. Add LEAP to Claude Desktop configuration:"
    echo "   File: ~/Library/Application Support/Claude/claude_desktop_config.json"
    echo ""
    echo "   Add this to the 'mcpServers' section:"
    echo '   "leap": {'
    echo '     "command": "leap-mcp-server"'
    echo '   }'
    echo ""
    echo "2. Restart Claude Desktop"
    echo ""
    echo "For help, see: README.md"
else
    echo ""
    echo "❌ Installation failed"
    echo "Please check the error messages above"
    exit 1
fi
