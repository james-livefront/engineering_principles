# Troubleshooting Guide

Solutions for common LEAP installation and runtime issues.

## Installation Issues

### "Python not found" or version too old

**Problem:** Python 3.11+ is required but not found or version is too old.

**Solution:**

```bash
# Check Python version (need 3.11+)
python3 --version

# Install Python 3.11+ from https://www.python.org/downloads/
# Or use homebrew on macOS:
brew install python@3.11

# Or use pyenv:
pyenv install 3.11
pyenv global 3.11
```

### "leap-mcp-server: command not found"

**Problem:** LEAP commands not available after installation.

**Solution:**

```bash
# Ensure uv tool bin directory is in your PATH
export PATH="$HOME/.local/bin:$PATH"

# Add to your shell profile (~/.zshrc or ~/.bash_profile):
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Reinstall LEAP
cd /path/to/engineering_principles
uv tool install --force .

# Verify installation
which leap-mcp-server
leap --help
```

### "uv: command not found"

**Problem:** uv package manager is not installed.

**Solution:**

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH (usually automatic, but if needed):
export PATH="$HOME/.local/bin:$PATH"

# Verify installation
uv --version
```

### Permission denied during installation

**Problem:** Installation fails with permission errors.

**Solution:**

```bash
# Don't use sudo with uv tool install
# Instead, ensure your user has write access to ~/.local

# Fix permissions if needed:
chmod -R u+w ~/.local

# Try installation again
uv tool install .
```

---

## MCP Server Issues

### Server won't start in Claude Desktop

**Problem:** MCP server fails to start or Claude can't connect.

**Diagnostic Steps:**

1. **Check the MCP server log:**

   ```bash
   tail -50 ~/Library/Logs/Claude/mcp-server-leap.log
   ```

2. **Verify LEAP is installed:**

   ```bash
   leap-mcp-server --help
   # Should show help text, not "command not found"
   ```

3. **Test server startup manually:**

   ```bash
   leap-mcp-server
   # Should start without errors
   # Press Ctrl+C to stop
   ```

4. **Reinstall if needed:**

   ```bash
   cd /path/to/engineering_principles
   uv tool install --force .
   ```

5. **Restart Claude Desktop** after fixing issues

### "spawn leap-mcp-server ENOENT" error

**Problem:** Claude Desktop can't find the `leap-mcp-server` command.

**Solution:**

```bash
# The leap-mcp-server command isn't in Claude's PATH

# Option 1: Use absolute path in config
which leap-mcp-server
# Copy the full path (e.g., /Users/you/.local/bin/leap-mcp-server)

# Edit ~/Library/Application Support/Claude/claude_desktop_config.json:
{
  "mcpServers": {
    "leap": {
      "command": "/Users/you/.local/bin/leap-mcp-server"
    }
  }
}

# Option 2: Reinstall with uv tool
cd /path/to/engineering_principles
uv tool install --force .

# Restart Claude Desktop
```

### MCP server starts but tools don't work

**Problem:** Server runs but tools return errors or empty results.

**Diagnostic Steps:**

1. **Check YAML files exist and are valid:**

   ```bash
   cd /path/to/engineering_principles
   ls -la leap/core/*.yaml
   python3 -c "import yaml; yaml.safe_load(open('leap/core/principles.yaml'))"
   ```

2. **Test tools directly:**

   ```bash
   # For development testing
   cd /path/to/engineering_principles
   uv run python leap_mcp_server.py
   # Then test with MCP client
   ```

3. **Check for import errors:**

   ```bash
   python3 -c "from leap.loaders import LeapLoader; print('OK')"
   ```

---

## CLI Issues

### "OpenAI package not found" / "Anthropic package not found"

**Problem:** Evaluation runner can't find AI provider packages.

**Solution:**

```bash
# Install all dependencies
cd /path/to/engineering_principles
uv sync

# Or install specific provider:
uv add openai
uv add anthropic
```

### "API key required" or "No API key found"

**Problem:** Evaluation needs API keys but can't find them.

**Solution:**

```bash
# Option 1: Use .env file
cp .env.example .env
# Edit .env and add your API keys

# Option 2: Use environment variables
export OPENAI_API_KEY='sk-your-key-here'
export ANTHROPIC_API_KEY='sk-ant-your-key-here'

# Option 3: Use config file
# Edit eval_config.yaml and add keys

# Verify it works
leap-eval --list-providers
```

### "Error calling API" or "Rate limit exceeded"

**Problem:** API calls fail due to network, quota, or rate limits.

**Solutions:**

```bash
# Check internet connection
curl https://api.openai.com

# Check API key validity
# OpenAI: https://platform.openai.com/api-keys
# Anthropic: https://console.anthropic.com/

# Check usage/credits:
# OpenAI: https://platform.openai.com/usage
# Anthropic: https://console.anthropic.com/settings/billing

# Try with different provider
leap-eval --provider anthropic  # if OpenAI fails
leap-eval --provider ollama      # for local/free

# Reduce parallel execution if rate limited
leap-eval --no-parallel
```

### "Model not found" error

**Problem:** Specified model doesn't exist or isn't accessible.

**Solution:**

```bash
# List available providers and models
leap-eval --list-providers

# Use a valid model
leap-eval --provider openai --model gpt-4o
leap-eval --provider anthropic --model claude-3-5-sonnet-20241022

# Or let it use defaults
leap-eval  # uses recommended model for available provider
```

### Low accuracy scores

**Problem:** Evaluation results show unexpectedly low accuracy.

**Possible Causes & Solutions:**

1. **Wrong platform/focus for prompt:**
   ```bash
   # Make sure prompt matches test cases
   leap review --platform web --focus security > prompt.txt
   leap-eval --prompt-file prompt.txt  # auto-detects web/security
   ```

2. **Using basic prompt instead of rule-based:**
   ```bash
   # Use default (rule-based) for best results
   leap review --platform web  # includes detection rules
   ```

3. **API issues causing bad responses:**
   ```bash
   # Try different provider
   leap-eval --provider anthropic
   ```

4. **Try enhanced mode (experimental):**
   ```bash
   export OPENAI_API_KEY='your-key'
   leap review --platform web --focus security --enhanced > enhanced.txt
   leap-eval --prompt-file enhanced.txt
   ```

### Empty output from CLI commands

**Problem:** Commands run but produce no output.

**Solution:**

```bash
# Check that YAML files aren't corrupted
cd /path/to/engineering_principles
python3 -c "import yaml; yaml.safe_load(open('leap/core/principles.yaml'))"

# Ensure you're running from the repository root or LEAP is installed
cd /path/to/engineering_principles
uv run python principles_cli.py review --platform web

# Or use globally installed version
leap review --platform web

# Check for errors
leap review --platform web 2>&1 | tee output.log
```

### "Invalid platform" error

**Problem:** Platform parameter not recognized.

**Solution:**

```bash
# Use exact platform names (lowercase):
leap review --platform android  # ✓
leap review --platform ios      # ✓
leap review --platform web      # ✓

# Not:
leap review --platform Android  # ✗
leap review --platform iPhone   # ✗
leap review --platform react    # ✗
```

---

## Development Issues

### "Module not found" errors

**Problem:** Import errors when running locally.

**Solution:**

```bash
# Install dependencies
cd /path/to/engineering_principles
uv sync

# Verify installation
uv run python -c "from leap.loaders import LeapLoader; print('OK')"

# If still failing, check Python path
uv run python -c "import sys; print(sys.path)"
```

### Changes not reflected after editing code

**Problem:** Code changes don't appear when running commands.

**Solution:**

```bash
# For local development, use uv run:
uv run python principles_cli.py review --platform web

# If using global install, reinstall after changes:
uv tool install --force .

# Or use development mode in Claude Desktop config:
{
  "mcpServers": {
    "leap": {
      "command": "/path/to/.venv/bin/python",
      "args": ["/path/to/leap_mcp_server.py"]
    }
  }
}
```

### Tests failing

**Problem:** pytest tests fail unexpectedly.

**Solution:**

```bash
# Install all dependencies including dev dependencies
uv sync

# Run tests with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_eval_runner.py -v

# Clear pytest cache
uv run pytest --cache-clear

# Check for import issues
uv run python -c "import pytest; print('OK')"
```

---

## Validation Commands

Quick commands to verify LEAP is working correctly:

```bash
# Test LEAP installation
leap --help
leap-eval --help
leap-mcp-server --version 2>&1 | head -5

# Test config loading (for developers)
cd /path/to/engineering_principles
uv run python -c "from eval_runner import load_config; print(load_config('eval_config.yaml'))"

# Test provider setup
leap-eval --list-providers

# Check YAML syntax
cd /path/to/engineering_principles
uv run python -c "import yaml; yaml.safe_load(open('leap/core/principles.yaml'))"

# Test MCP server startup
leap-mcp-server &
sleep 2
pkill -f leap-mcp-server
```

---

## Getting Help

If you're still having issues:

### 1. Check the logs

**Claude Desktop logs:**
```bash
tail -50 ~/Library/Logs/Claude/mcp-server-leap.log
tail -50 ~/Library/Logs/Claude/main.log
```

**System logs:**
```bash
# Check for Python errors
tail -f /var/log/system.log | grep python  # macOS
journalctl -f | grep python  # Linux
```

### 2. Try the install script

```bash
cd /path/to/engineering_principles
./install.sh
```

### 3. Start fresh

```bash
# Uninstall completely
uv tool uninstall engineering_principles

# Remove any cached files
rm -rf ~/.cache/leap
rm -rf .cache/

# Reinstall
cd /path/to/engineering_principles
./install.sh

# Restart Claude Desktop
```

### 4. Verify system requirements

```bash
# Python version
python3 --version  # Should be 3.11+

# uv version
uv --version  # Should be recent

# Disk space
df -h  # Ensure sufficient space

# Internet connection
curl -I https://api.openai.com
```

### 5. Create a minimal test case

```bash
# Test basic functionality
cd /tmp
cat > test_leap.sh << 'EOF'
#!/bin/bash
leap review --platform web --focus security | head -20
EOF

chmod +x test_leap.sh
./test_leap.sh
```

### 6. Report an issue

If nothing works, please report the issue with:

- LEAP version: `leap --version` or git commit hash
- Python version: `python3 --version`
- OS and version: `uname -a`
- Error messages and logs
- Steps to reproduce

---

## Common Error Messages

### "FileNotFoundError: [Errno 2] No such file or directory: 'leap/core/principles.yaml'"

**Cause:** Running from wrong directory or LEAP not properly installed.

**Solution:**
```bash
# Option 1: Run from repo root
cd /path/to/engineering_principles
uv run python principles_cli.py review --platform web

# Option 2: Use globally installed version
leap review --platform web
```

### "ImportError: No module named 'leap'"

**Cause:** LEAP package not installed in Python environment.

**Solution:**
```bash
cd /path/to/engineering_principles
uv sync
uv run python principles_cli.py review --platform web
```

### "yaml.scanner.ScannerError"

**Cause:** YAML file syntax error.

**Solution:**
```bash
# Validate YAML files
cd /path/to/engineering_principles
uv run python -c "
import yaml
from pathlib import Path
for f in Path('leap/core').glob('*.yaml'):
    try:
        yaml.safe_load(open(f))
        print(f'✓ {f}')
    except Exception as e:
        print(f'✗ {f}: {e}')
"
```

### "requests.exceptions.ConnectionError"

**Cause:** Network connectivity issue or API endpoint unavailable.

**Solution:**
```bash
# Check internet connection
curl https://api.openai.com

# Try with different provider
leap-eval --provider ollama  # local, no internet needed

# Check firewall/proxy settings
env | grep -i proxy
```
