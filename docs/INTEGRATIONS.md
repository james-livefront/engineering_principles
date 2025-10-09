# Integration Guide

How to integrate LEAP into your development workflow.

## Git Hooks

Enforce principles before commits using git hooks.

### Pre-Commit Hook

Check engineering principles before allowing commits:

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Checking engineering principles..."
leap review --platform web --focus security,accessibility

# Optional: Use with an AI tool to review staged changes
# git diff --staged | your-ai-tool --prompt "$(leap review --platform web)"
```

**Setup:**

```bash
# Create the hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
echo "Checking engineering principles..."
leap review --platform web --focus security,accessibility
EOF

# Make it executable
chmod +x .git/hooks/pre-commit
```

### Pre-Push Hook

Review code before pushing to remote:

```bash
#!/bin/bash
# .git/hooks/pre-push

echo "Running engineering principles check..."
leap review --platform web --focus security,accessibility,testing > /tmp/review_prompt.txt

# Optional: Run evaluation
leap-eval --prompt-file /tmp/review_prompt.txt
```

**Setup:**

```bash
# Create the hook
cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash
echo "Running engineering principles check..."
leap review --platform web --focus security,accessibility,testing
EOF

# Make it executable
chmod +x .git/hooks/pre-push
```

---

## VS Code Integration

### Per-Project Tasks (Recommended)

Add a `.vscode/tasks.json` file to each project:

**For a Web Project:**

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Review with Engineering Principles",
      "type": "shell",
      "command": "leap",
      "args": [
        "review",
        "--platform", "web",
        "--focus", "${input:focus}"
      ],
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Generate Code Prompt",
      "type": "shell",
      "command": "leap",
      "args": [
        "generate",
        "--platform", "web",
        "--component", "${input:component}"
      ],
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "panel": "new"
      }
    }
  ],
  "inputs": [
    {
      "id": "focus",
      "type": "pickString",
      "description": "Focus areas for review",
      "options": [
        "security,accessibility",
        "security,accessibility,testing",
        "design,accessibility",
        "performance,security"
      ],
      "default": "security,accessibility"
    },
    {
      "id": "component",
      "type": "pickString",
      "description": "Component type to generate",
      "options": [
        "ui",
        "business-logic",
        "data-layer"
      ],
      "default": "ui"
    }
  ]
}
```

**For an Android Project:**

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Review with Engineering Principles",
      "type": "shell",
      "command": "leap",
      "args": [
        "review",
        "--platform", "android",
        "--focus", "${input:focus}"
      ],
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "panel": "new"
      }
    }
  ],
  "inputs": [
    {
      "id": "focus",
      "type": "pickString",
      "description": "Focus areas for review",
      "options": [
        "security,accessibility",
        "security,testing",
        "accessibility,testing"
      ],
      "default": "security,accessibility"
    }
  ]
}
```

**For an iOS Project:**

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Review with Engineering Principles",
      "type": "shell",
      "command": "leap",
      "args": [
        "review",
        "--platform", "ios",
        "--focus", "${input:focus}"
      ],
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "panel": "new"
      }
    }
  ],
  "inputs": [
    {
      "id": "focus",
      "type": "pickString",
      "description": "Focus areas for review",
      "options": [
        "security,accessibility",
        "security,testing",
        "accessibility,design"
      ],
      "default": "security,accessibility"
    }
  ]
}
```

### Usage

1. Open Command Palette: `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Type "Tasks: Run Task"
3. Select "Review with Engineering Principles" or "Generate Code Prompt"
4. Choose focus areas or component type from predefined options
5. Copy generated prompt to use with AI tools

---

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/pr-review.yml
name: Engineering Principles Check
on: pull_request

jobs:
  principles-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Install LEAP
        run: |
          git clone https://github.com/james-livefront/engineering_principles.git /tmp/leap
          cd /tmp/leap
          uv tool install .

      - name: Run evaluations
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          leap-eval --output eval_results.md
          cat eval_results.md >> $GITHUB_STEP_SUMMARY

      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: evaluation-results
          path: eval_results.md
```

### GitLab CI

```yaml
# .gitlab-ci.yml
engineering_principles:
  image: python:3.11
  stage: test
  script:
    - curl -LsSf https://astral.sh/uv/install.sh | sh
    - export PATH="$HOME/.local/bin:$PATH"
    - git clone https://github.com/james-livefront/engineering_principles.git /tmp/leap
    - cd /tmp/leap && uv tool install .
    - cd $CI_PROJECT_DIR
    - leap-eval --output eval_results.md
  artifacts:
    reports:
      junit: eval_results.md
  only:
    - merge_requests
```

### CircleCI

```yaml
# .circleci/config.yml
version: 2.1

jobs:
  principles-check:
    docker:
      - image: python:3.11
    steps:
      - checkout
      - run:
          name: Install uv
          command: curl -LsSf https://astral.sh/uv/install.sh | sh
      - run:
          name: Install LEAP
          command: |
            export PATH="$HOME/.local/bin:$PATH"
            git clone https://github.com/james-livefront/engineering_principles.git /tmp/leap
            cd /tmp/leap
            uv tool install .
      - run:
          name: Run evaluations
          command: |
            export PATH="$HOME/.local/bin:$PATH"
            leap-eval --output eval_results.md
      - store_artifacts:
          path: eval_results.md

workflows:
  version: 2
  pr-check:
    jobs:
      - principles-check
```

---

## Real-World Workflows

### Feature Development Workflow

```bash
# 1. Generate code for the new feature
leap generate --platform web --component ui > feature_prompt.txt

# 2. Use prompt with your AI assistant to write initial code
cat feature_prompt.txt | your-ai-tool

# 3. Review the generated code
leap review --platform web --focus security,accessibility > review_prompt.txt

# 4. Use review prompt to check compliance
cat review_prompt.txt | your-ai-tool --input generated_code.tsx

# 5. Test prompt effectiveness
leap-eval --prompt-file review_prompt.txt
```

### Code Review Workflow

```bash
# 1. Generate review prompt for platform
leap review --platform android --focus security,accessibility > review_prompt.txt

# 2. Review PR changes
git diff main...feature-branch | your-ai-tool --prompt "$(cat review_prompt.txt)"

# 3. Validate findings
leap-eval --prompt-file review_prompt.txt --output validation.md
```

### Dependency Evaluation Workflow

```bash
# 1. Evaluate new dependency
leap dependencies --platform web lodash > dep_analysis.txt

# 2. Review the analysis
cat dep_analysis.txt

# 3. Make decision based on approval status
# ✅ APPROVED - proceed with installation
# ❌ NOT APPROVED - find alternatives or discuss with team
```

---

## IDE Integrations

### JetBrains IDEs (IntelliJ, WebStorm, Android Studio)

**External Tools Setup:**

1. Go to **Settings** → **Tools** → **External Tools**
2. Click **+** to add a new tool
3. Configure:
   - **Name**: Review with LEAP
   - **Program**: `leap`
   - **Arguments**: `review --platform web --focus security,accessibility`
   - **Working directory**: `$ProjectFileDir$`

4. Run via **Tools** → **External Tools** → **Review with LEAP**

### Vim/Neovim

Add to your `.vimrc` or `init.vim`:

```vim
" Generate review prompt
nnoremap <leader>lr :!leap review --platform web --focus security,accessibility<CR>

" Generate code prompt
nnoremap <leader>lg :!leap generate --platform web --component ui<CR>

" Run evaluation
nnoremap <leader>le :!leap-eval<CR>
```

### Emacs

Add to your `.emacs` or `init.el`:

```elisp
;; LEAP integration
(defun leap-review ()
  "Generate engineering principles review prompt."
  (interactive)
  (shell-command "leap review --platform web --focus security,accessibility"))

(defun leap-generate ()
  "Generate code writing prompt."
  (interactive)
  (shell-command "leap generate --platform web --component ui"))

(global-set-key (kbd "C-c l r") 'leap-review)
(global-set-key (kbd "C-c l g") 'leap-generate)
```

---

## Docker Integration

### Dockerfile

```dockerfile
FROM python:3.11-slim

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Install LEAP
RUN git clone https://github.com/james-livefront/engineering_principles.git /opt/leap
WORKDIR /opt/leap
RUN uv tool install .

# Set up working directory
WORKDIR /workspace

# Entry point
ENTRYPOINT ["leap"]
```

**Build and use:**

```bash
# Build image
docker build -t leap:latest .

# Use for review
docker run --rm -v $(pwd):/workspace leap:latest review --platform web --focus security

# Use for evaluation
docker run --rm -v $(pwd):/workspace -e OPENAI_API_KEY=$OPENAI_API_KEY leap:latest-eval
```

---

## Pre-Commit Framework Integration

For teams using the [pre-commit](https://pre-commit.com/) framework:

**.pre-commit-config.yaml:**

```yaml
repos:
  - repo: local
    hooks:
      - id: leap-review
        name: LEAP Engineering Principles Review
        entry: leap review --platform web --focus security,accessibility
        language: system
        pass_filenames: false
        always_run: true
```

**Setup:**

```bash
# Install pre-commit
pip install pre-commit

# Install the hooks
pre-commit install

# Run manually
pre-commit run leap-review --all-files
```

---

## Continuous Monitoring

### Daily Principle Checks

```bash
#!/bin/bash
# daily-principles-check.sh

# Run comprehensive evaluation
leap-eval --output daily-report-$(date +%Y-%m-%d).md

# Send results to team (example with email)
cat daily-report-$(date +%Y-%m-%d).md | mail -s "Daily Principles Report" team@company.com
```

**Cron job:**

```cron
# Run every day at 9 AM
0 9 * * * /path/to/daily-principles-check.sh
```

---

## Team Workflows

### Pull Request Template

Add to `.github/pull_request_template.md`:

```markdown
## Engineering Principles Checklist

- [ ] Ran `leap review --platform <platform> --focus security,accessibility`
- [ ] All critical and blocking violations addressed
- [ ] Evaluation scores acceptable (`leap-eval --prompt-file review_prompt.txt`)
- [ ] Dependencies approved (if any added)

## Principle Compliance

<!-- Paste relevant sections from LEAP review here -->
```

### Code Review Guidelines

**For Reviewers:**

1. Run platform-specific review prompt: `leap review --platform <platform>`
2. Use output to guide code review focus
3. Verify critical/blocking violations are addressed
4. Check dependency approvals if applicable

**For Authors:**

1. Generate review prompt before PR: `leap review --platform <platform> > review.txt`
2. Self-review using the prompt
3. Address critical and blocking issues
4. Include compliance notes in PR description
