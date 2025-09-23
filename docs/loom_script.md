# Loom Recording Script: Engineering Principles Tool

## Opening (0:00-0:30)

**Say:** "Hey team, I want to show you this engineering principles tool we've built. It generates AI prompts that enforce our code standards across Android, iOS, and Web platforms. Instead of hoping developers remember all our standards, we're experimenting with encoding them into prompts that AI assistants will follow automatically."

**Command:**

```bash
ls -la
bat README.md
```

---

## The Problem We're Solving (0:30-1:00)

**Say:** "We have 15 core engineering principles at Livefront, from security to accessibility to testing requirements. Different platforms have different rules. Android uses Dagger and RxJava, iOS is first-party only, Web has its own stack. Trying to cram all this into a monolithic prompt wastes context and confuses the AI. This tool attempts to solve that by generating right-sized prompts tailored to the platform and focus area."

**Command:**

```bash
# Show the core principles
grep "Core Principles" -A 17 README.md | mdcat
```

---

## Basic Code Review Example (1:00-2:00)

**Say:** "Let me show you the simplest use case. Say I'm reviewing a web application and I want to focus on security and accessibility. Watch what happens when I generate a review prompt."

**Command:**

```bash
uv run python principles_cli.py review --platform web --focus security,accessibility | mdless
```

**Say:** "Look at this output - it's a complete prompt I can paste into Claude or ChatGPT. It includes our specific security requirements like HTTPS everywhere, no secrets in source control, and our accessibility standards like WCAG 2.1 compliance. The AI will now review code using OUR standards, not generic best practices."

---

## Platform-Specific Standards (2:00-3:00)

**Say:** "What's really powerful is how it adapts to each platform. Let me show you Android versus iOS."

**Command:**

```bash
# First Android
uv run python principles_cli.py review --platform android --focus architecture | mdless
```

**Say:** "Notice it mentions Dagger, RxJava2, specific Android patterns. Now watch iOS:"

**Command:**

```bash
# Now iOS
uv run python principles_cli.py review --platform ios --focus architecture | mdless
```

**Say:** "Completely different - first-party only, no third-party dependencies, SwiftLint, code-based layouts. The tool knows the rules for each platform."

---

## Code Generation (3:00-4:00)

**Say:** "But it's not just for reviews. We can generate prompts for WRITING code that follows our standards from the start. This is huge for onboarding or when using AI assistants for development."

**Command:**

```bash
uv run python principles_cli.py generate --platform android --component ui | mdless
```

**Say:** "This prompt tells the AI exactly how to write Android UI code for us - responsive layouts, accessibility attributes, our specific architecture patterns. The generated code will already follow our standards."

---

## Real-World Scenario (4:00-5:00)

**Say:** "Let me show you a real scenario. Say we're building a new feature and want to make sure it's secure, accessible, and well-tested."

**Command:**

```bash
# Generate a comprehensive review prompt
uv run python principles_cli.py review --platform web --focus security,accessibility,testing,architecture | mdless
```

**Say:** "This gives us a comprehensive checklist. See how it prioritizes Security over Accessibility over Testing? And look - it catches things like hard-coded strings for localization, missing ARIA labels, test coverage requirements."

---

## Dependency Checking (5:00-5:30)

**Say:** "We even have dependency validation. Remember, all dependencies need VP Technology and client approval."

**Command:**

```bash
# Check if a library is approved
uv run python principles_cli.py dependencies --platform android --check rxjava2 | mdless
```

**Say:** "RxJava2 is approved for Android. But watch what happens with something else:"

**Command:**

```bash
uv run python principles_cli.py dependencies --platform ios --check react-native | mdless
```

**Say:** "It'll tell us React Native isn't in our approved iOS stack."

---

## The Philosophy (5:30-6:00)

**Say:** "This all comes back to our philosophy - 'Livefront Engineers are craftspeople.' We don't defer work with TODOs, we treat the design as the spec, and every line gets peer-reviewed."

**Command:**

```bash
# Show the philosophy
head -15 README.md | tail -10 | mdless
```

**Say:** "By encoding these principles into AI prompts, we're scaling our craftsmanship. Every AI-assisted code review or generation follows the same high standards."

---

## Evaluation Framework (6:00-7:00)

**Say:** "And here's the really cool part - we can actually measure how effective these prompts are. We have an evaluation framework that tests against real code samples."

**Command:**

```bash
# Show the test cases we use
ls evals/detection/
bat evals/detection/security_test_cases.yaml
```

**Say:** "See those test cases? Real code samples with known violations. Now let me generate a web security prompt. Notice it includes metadata that tells the evaluator exactly what platform and focus areas to test:"

**Command:**

```bash
# Generate platform-specific prompt with metadata
uv run python principles_cli.py review --platform web --focus security,accessibility > web_security_prompt.txt

# Show the metadata header
head -6 web_security_prompt.txt

# Test the prompt - it auto-detects platform and focus from metadata
uv run python eval_runner.py --mode detection --prompt-file web_security_prompt.txt --output demo_results.md

# Show results
bat demo_results.md
```

**Say:** "The evaluation automatically detected this is a web prompt with security and accessibility focus. It only tested against relevant violations - no Android SharedPreferences or iOS-specific tests. Now watch what happens with LLM enhancement - it adds specific implementation details like exact contrast ratios, ARIA patterns, and current security vulnerabilities:"

**Command:**

```bash
# Test with LLM enhancement for better results
uv run python eval_runner.py --mode detection --enhanced --prompt-file web_security_prompt.txt --output enhanced_results.md

# Compare baseline vs enhanced accuracy
diff demo_results.md enhanced_results.md | head -30
```

---

## Integration Points (7:00-7:30)

**Say:** "This integrates everywhere in our workflow. You can use it in CI/CD pipelines, as a pre-commit hook, in VS Code, or just run it manually before submitting PRs. For example, you could add this to your git hooks to automatically generate and use the right prompt for your platform:"

**Command:**

```bash
# Example git hook usage
cat > .git/hooks/pre-push.example <<'EOF'
#!/bin/bash
PROMPT=$(uv run python principles_cli.py review --platform web --focus security,accessibility)
# Pass $PROMPT to your AI code reviewer
EOF

cat .git/hooks/pre-push.example
```

---

## Closing & Impact (7:30-8:00)

**Say:** "The impact here is huge. We're not just documenting standards - we're operationalizing them. Every piece of AI-generated or AI-reviewed code follows Livefront's specific engineering principles. This means consistent quality, fewer security issues, better accessibility, and it scales across all our teams and projects."

**Command:**

```bash
# Show the quick start one more time
grep "Quick Start" -A 10 README.md
```

**Say:** "To get started, just clone the repo, run uv sync, and you're ready to generate prompts. The entire setup takes less than a minute, and the impact on code quality is immediate."

---

## Q&A Setup (8:00-8:30)

**Say:** "Let me show you a few more quick examples before we wrap up..."

**Commands to have ready:**

```bash
# Different focus combinations
uv run python principles_cli.py review --platform web --focus security
uv run python principles_cli.py review --platform android --focus testing,performance
uv run python principles_cli.py generate --platform ios --component business-logic

# Show available options
uv run python principles_cli.py --help
uv run python principles_cli.py review --help
```

**Say:** "And that's the engineering principles tool. Questions?"

---

## Key Stats to Mention

- 15 core principles
- 85% accuracy in violation detection
- 3 platforms supported (Android, iOS, Web)
- Priority order: Security > Accessibility > Testing > Performance > Code Style
- Zero TODOs policy
- 80% test coverage requirement
- Every line peer-reviewed
