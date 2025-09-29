# Contributing to LEAP

Thank you for your interest in contributing to LEAP (Livefront Engineering Automated Principles)! This guide will help you extend the system effectively.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Architecture Overview](#architecture-overview)
3. [Adding Detection Patterns](#adding-detection-patterns)
4. [Adding Platform Support](#adding-platform-support)
5. [Adding Evaluation Cases](#adding-evaluation-cases)
6. [Code Style Guidelines](#code-style-guidelines)
7. [Submission Process](#submission-process)

---

## Getting Started

### Prerequisites

- Python 3.8+
- Git
- Familiarity with YAML
- Understanding of regex patterns (for detection rules)

### Setup

```bash
# Clone the repository
git clone https://github.com/livefront/engineering_principles.git
cd engineering_principles

# Install dependencies
pip install -r requirements.txt

# Run tests to ensure everything works
python eval_runner.py
```

### Project Structure

```
engineering_principles/
├── core/                  # Foundational YAML files
│   ├── philosophy.yaml    # Core mantras and values
│   ├── principles.yaml    # 15 engineering principles
│   ├── platforms.yaml     # Platform-specific requirements
│   └── enforcement.yaml   # CI/CD enforcement mechanisms
├── modules/
│   ├── detection/         # Pattern-based violation detection
│   │   ├── rules/         # Regex patterns organized by principle
│   │   ├── severity.yaml  # Severity classification
│   │   └── context.yaml   # Context-aware rule application
│   └── generation/        # Code generation guidance
│       └── guidance.yaml  # Implementation patterns
├── eval/                  # Evaluation test cases
│   ├── test_cases/        # Violation scenarios by platform
│   └── metrics/           # Performance tracking
├── principles_cli.py      # Main CLI implementation
└── eval_runner.py         # Evaluation framework
```

---

## Architecture Overview

### YAML-Based Configuration

LEAP uses YAML files for all configuration to enable:

- **Version control**: Track principle changes over time
- **Human readability**: Non-developers can contribute patterns
- **Machine actionability**: Easy parsing and prompt generation
- **Modularity**: Edit one principle without affecting others

### Two-Layer Detection

1. **Base Patterns (regex)**: Fast, consistent, no false positives
2. **Enhanced Mode (LLM)**: Optional, catches nuanced violations

### Key Design Principles

- **Conservative detection**: High precision > high recall
- **Context awareness**: Same code, different contexts, different rules
- **Cultural integration**: Philosophy and mantras matter as much as rules
- **Measurable outcomes**: All changes validated through evaluation framework

---

## Adding Detection Patterns

Detection patterns are the core of LEAP's violation detection. Here's how to add effective patterns.

### Step 1: Choose the Right Principle Category

Patterns are organized under principles in `modules/detection/rules/`:

```yaml
principles:
  security:
    patterns: [...]
  accessibility:
    patterns: [...]
  testing:
    patterns: [...]
  code_quality:
    patterns: [...]
  architecture:
    patterns: [...]
  design_integrity:
    patterns: [...]
```

### Step 2: Write Your Pattern

Pattern structure:

```yaml
- name: "descriptive_pattern_name"
  regex: "your_regex_pattern_here"
  message: "Clear, actionable error message"
  severity: "critical|required|recommended"
  platform: "all|android|ios|web"
  context_exclude: ["test_code"]  # Optional: skip in certain contexts
  example: "bad_code → good_code"  # Optional but recommended
```

### Example: Adding a New Security Pattern

**Scenario**: Detect hardcoded database passwords

```yaml
# modules/detection/rules/security.yaml
principles:
  security:
    patterns:
      - name: "hardcoded_database_password"
        regex: '(db_password|database_password|DB_PASS)\s*[:=]\s*["\'][^"\']{8,}["\']'
        message: "Database password should be stored in environment variables or secure vault"
        severity: "critical"
        platform: "all"
        context_exclude: ["test_code"]
        example: 'DB_PASS = "secret123" → DB_PASS = os.getenv("DB_PASSWORD")'
```

### Step 3: Add Test Cases

Create test cases in `eval/test_cases/`:

```yaml
# eval/test_cases/security_test_cases.yaml
- id: "SEC-DB-001"
  name: "Hardcoded Database Password"
  platform: "all"
  code: |
    import os
    db_password = "my_secret_password_123"
    connection = connect(host="localhost", password=db_password)
  expected:
    detected: true
    severity: "critical"
    principle: "security"
    pattern: "hardcoded_database_password"
    message_contains: "environment variables"

- id: "SEC-DB-002"
  name: "Database Password from Environment (should pass)"
  platform: "all"
  code: |
    import os
    db_password = os.getenv("DB_PASSWORD")
    connection = connect(host="localhost", password=db_password)
  expected:
    detected: false
```

### Step 4: Run Evaluation

```bash
# Test your new pattern
python eval_runner.py --category security

# Expected output:
# ✅ SEC-DB-001: Hardcoded Database Password - PASS
# ✅ SEC-DB-002: Database Password from Environment - PASS
#
# Security Metrics:
# Accuracy: 96%
# Precision: 95%
# Recall: 100%
```

### Pattern Best Practices

**DO**:

- ✅ Write specific, targeted patterns
- ✅ Include clear, actionable messages
- ✅ Add test cases for both violations and valid code
- ✅ Consider context (exclude test code when appropriate)
- ✅ Provide examples of bad → good code
- ✅ Test against false positives

**DON'T**:

- ❌ Write overly broad patterns that match too much
- ❌ Use vague messages like "Fix this code"
- ❌ Assume your pattern will work without testing
- ❌ Ignore context (test code often needs different rules)
- ❌ Create patterns with high false positive rates

---

## Adding Platform Support

LEAP currently supports Android, iOS, and Web. Here's how to add a new platform.

### Step 1: Define Platform Requirements

Add your platform to `core/platforms.yaml`:

```yaml
react_native:
  name: "React Native"
  description: "Cross-platform mobile development with React"
  languages: ["javascript", "typescript"]
  approved_dependencies:
    - name: "react-navigation"
      purpose: "Navigation library"
      license: "MIT"
    - name: "react-native-reanimated"
      purpose: "Animation library"
      license: "MIT"
  required_tools:
    - tool: "metro"
      purpose: "JavaScript bundler"
    - tool: "eslint"
      purpose: "Code linting"
  file_patterns:
    source: ["*.tsx", "*.jsx", "*.ts", "*.js"]
    test: ["*.test.tsx", "*.test.ts", "*.spec.tsx"]
```

### Step 2: Add Platform-Specific Patterns

Update detection rules with platform-specific patterns:

```yaml
# modules/detection/rules/code_quality.yaml
principles:
  code_quality:
    patterns:
      - name: "react_native_inline_styles"
        regex: 'style=\{\{[^}]+\}\}'
        message: "Avoid inline styles, use StyleSheet.create for performance"
        severity: "recommended"
        platform: "react_native"
        example: 'style={{margin: 10}} → style={styles.container}'
```

### Step 3: Update Context Detection

Add file patterns to `modules/detection/context.yaml`:

```yaml
context_types:
  ui_code:
    detection:
      file_patterns:
        react_native: ["*Screen.tsx", "*Screen.js", "components/*.tsx"]

  business_logic:
    detection:
      file_patterns:
        react_native: ["services/*.ts", "hooks/*.ts"]
```

### Step 4: Add Test Cases

Create platform-specific test cases:

```yaml
# eval/test_cases/react_native_test_cases.yaml
- id: "RN-STYLE-001"
  name: "Inline Styles Detected"
  platform: "react_native"
  code: |
    <View style={{margin: 10, padding: 5}}>
      <Text>Hello</Text>
    </View>
  expected:
    detected: true
    severity: "recommended"
    principle: "code_quality"
```

---

## Adding Evaluation Cases

Strong evaluation cases improve LEAP's accuracy. Here's how to contribute test cases.

### Test Case Structure

```yaml
- id: "CATEGORY-TYPE-NNN"
  name: "Descriptive Test Name"
  platform: "all|android|ios|web|react_native"
  code: |
    # Your test code here
    # Can be multiple lines
  expected:
    detected: true|false
    severity: "critical|required|recommended"
    principle: "security|accessibility|testing|..."
    pattern: "pattern_name"  # Optional: specific pattern to match
    message_contains: "keyword"  # Optional: message validation
```

### Types of Test Cases

**1. True Positive (should detect violation)**

```yaml
- id: "SEC-001"
  name: "Hardcoded API Key"
  code: |
    const API_KEY = "sk-1234567890abcdef";
  expected:
    detected: true
    severity: "critical"
```

**2. True Negative (should NOT detect violation)**

```yaml
- id: "SEC-002"
  name: "API Key from Environment"
  code: |
    const API_KEY = process.env.API_KEY;
  expected:
    detected: false
```

**3. Edge Cases (boundary conditions)**

```yaml
- id: "SEC-003"
  name: "API Key Comment (not a violation)"
  code: |
    // API_KEY should be set in environment variables
    const apiKey = getApiKey();
  expected:
    detected: false
```

**4. Context-Specific Cases**

```yaml
- id: "TEST-001"
  name: "Hardcoded Values in Tests (acceptable)"
  platform: "all"
  code: |
    // In test file: user.test.ts
    const mockUser = { id: 123, name: "Test User" };
  context: "test_code"
  expected:
    detected: false
```

### Contributing Test Cases

1. **Identify gaps**: Run `python eval_runner.py --verbose` to see which categories need coverage
2. **Create test file**: Add to appropriate file in `eval/test_cases/`
3. **Run evaluation**: `python eval_runner.py --category your_category`
4. **Verify results**: Ensure your cases pass and improve metrics
5. **Submit PR**: Include before/after metrics showing improvement

---

## Code Style Guidelines

### Python Code

- Follow PEP 8
- Use type hints
- Write docstrings for public methods
- Keep functions focused and under 50 lines

Example:

```python
def _detect_code_context(self, file_path: str | None, platform: str) -> str:
    """Detect code context (ui_code, business_logic, data_layer) from file path.

    Args:
        file_path: Path to the file being analyzed
        platform: Platform identifier (android, ios, web, etc.)

    Returns:
        Context type string (ui_code, business_logic, etc.) or "unknown"
    """
    if not file_path:
        return "unknown"
    # Implementation...
```

### YAML Files

- Use 2-space indentation
- Keep lines under 100 characters
- Add comments for complex patterns
- Organize alphabetically within sections

Example:

```yaml
# Security patterns for credential detection
patterns:
  - name: "api_key_detection"
    regex: '(api[_-]?key|apikey)\s*[:=]\s*["\'][^"\']{16,}["\']'
    message: "API keys should be stored in environment variables"
    severity: "critical"
    platform: "all"
```

---

## Submission Process

### 1. Fork and Branch

```bash
git checkout -b feature/add-flutter-support
```

### 2. Make Your Changes

- Follow the appropriate guide above
- Add tests for your changes
- Update documentation if needed

### 3. Run Full Test Suite

```bash
# Run evaluation framework
python eval_runner.py

# Check code quality
python -m py_compile principles_cli.py
python -m py_compile eval_runner.py

# Verify CLI works
python principles_cli.py generate --platform web
python principles_cli.py review --platform android --focus security
```

### 4. Commit with Clear Messages

```bash
git commit -m "feat: add Flutter platform support with 15 detection patterns"
```

Commit message format:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `test:` Test additions or modifications
- `refactor:` Code refactoring

### 5. Create Pull Request

**PR Title**: Clear, descriptive summary

**PR Description Template**:

```markdown
## Description
Brief description of what this PR adds/fixes.

## Type of Change
- [ ] New detection patterns
- [ ] Platform support
- [ ] Evaluation cases
- [ ] Bug fix
- [ ] Documentation

## Testing
- [ ] Added test cases
- [ ] All tests pass
- [ ] Evaluation metrics improved or maintained

## Metrics Impact (if applicable)
Before:
- Accuracy: 82%
- Precision: 80%

After:
- Accuracy: 85%
- Precision: 83%

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] Evaluation framework passes
```

### 6. Review Process

- Maintainers will review within 3-5 business days
- Address feedback and update PR
- Once approved, changes will be merged

---

## Common Contribution Scenarios

### Scenario 1: Adding a Security Pattern

```yaml
# 1. Add pattern to modules/detection/rules/security.yaml
- name: "exposed_jwt_secret"
  regex: 'jwt[_-]?secret\s*[:=]\s*["\'][^"\']{16,}["\']'
  message: "JWT secret must be stored in environment variables"
  severity: "critical"

# 2. Add test cases to eval/test_cases/security_test_cases.yaml
- id: "SEC-JWT-001"
  code: |
    const JWT_SECRET = "my-secret-key-12345";
  expected:
    detected: true

# 3. Run tests
python eval_runner.py --category security
```

### Scenario 2: Adding Accessibility Pattern for Web

```yaml
# 1. Add pattern to modules/detection/rules/accessibility.yaml
- name: "missing_aria_label_button"
  regex: '<button(?![^>]*aria-label)[^>]*><(svg|img|i|span)(?![^>]*aria-hidden)'
  message: "Icon-only buttons need aria-label for screen readers"
  severity: "required"
  platform: "web"

# 2. Add test case
- id: "A11Y-BTN-001"
  platform: "web"
  code: |
    <button><svg>...</svg></button>
  expected:
    detected: true

# 3. Test
python eval_runner.py --category accessibility --platform web
```

### Scenario 3: Improving False Positive Rate

```yaml
# 1. Identify false positive from evaluation
# Pattern: hardcoded_url matches "http://localhost" in tests

# 2. Add context exclusion
- name: "hardcoded_url"
  regex: 'http://(?!localhost|127\\.0\\.0\\.1)'
  context_exclude: ["test_code"]  # Added this line

# 3. Add test case for the fix
- id: "SEC-URL-002"
  name: "Localhost in Tests (should pass)"
  code: |
    const testUrl = "http://localhost:3000";
  context: "test_code"
  expected:
    detected: false

# 4. Verify improvement
python eval_runner.py --category security --verbose
```

---

## Questions and Support

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and ideas
- **Email**: <engineering@livefront.com> for private inquiries

---

## License

By contributing to LEAP, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

Thank you for helping make LEAP better! Your contributions help the entire community codify engineering excellence.
