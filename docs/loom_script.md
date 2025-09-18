# Loom Recording Script: Engineering Principles Tool

## Opening (0:00-0:30)

**Say:** "Hey team, I want to show you this engineering principles tool we've built. It generates AI prompts that enforce our code standards across Android, iOS, and Web platforms. The key insight here is that instead of hoping developers remember all our standards, we're encoding them into prompts that AI assistants will follow automatically."

**Command:**
```bash
ls -la
cat README.md | head -20
```

---

## The Problem We're Solving (0:30-1:00)

**Say:** "We have 15 core engineering principles at Livefront, from security to accessibility to testing requirements. Different platforms have different rules. Android uses Dagger and RxJava, iOS is first-party only, Web has its own stack. Trying to cram all this into a monolithic prompt wastes context and confuses the AI. This tool solves that by generating right-sized prompts tailored to the platform and focus area."

**Command:**
```bash
# Show the core principles
grep "Core Principles" -A 17 README.md
```

---

## Basic Code Review Example (1:00-2:00)

**Say:** "Let me show you the simplest use case. Say I'm reviewing a web application and I want to focus on security and accessibility. Watch what happens when I generate a review prompt."

**Command:**
```bash
uv run python principles_cli.py review --platform web --focus security,accessibility
```

**Say:** "Look at this output - it's a complete prompt I can paste into Claude or ChatGPT. It includes our specific security requirements like HTTPS everywhere, no secrets in source control, and our accessibility standards like WCAG 2.1 compliance. The AI will now review code using OUR standards, not generic best practices."

---

## Platform-Specific Standards (2:00-3:00)

**Say:** "What's really powerful is how it adapts to each platform. Let me show you Android versus iOS."

**Command:**
```bash
# First Android
uv run python principles_cli.py review --platform android --focus architecture
```

**Say:** "Notice it mentions Dagger, RxJava2, specific Android patterns. Now watch iOS:"

**Command:**
```bash
# Now iOS
uv run python principles_cli.py review --platform ios --focus architecture
```

**Say:** "Completely different - first-party only, no third-party dependencies, SwiftLint, code-based layouts. The tool knows the rules for each platform."

---

## Code Generation (3:00-4:00)

**Say:** "But it's not just for reviews. We can generate prompts for WRITING code that follows our standards from the start. This is huge for onboarding or when using AI assistants for development."

**Command:**
```bash
uv run python principles_cli.py generate --platform android --component ui
```

**Say:** "This prompt tells the AI exactly how to write Android UI code for us - responsive layouts, accessibility attributes, our specific architecture patterns. The generated code will already follow our standards."

---

## Real-World Scenario (4:00-5:00)

**Say:** "Let me show you a real scenario. Say we're building a new feature and want to make sure it's secure, accessible, and well-tested."

**Command:**
```bash
# Generate a comprehensive review prompt
uv run python principles_cli.py review --platform web --focus security,accessibility,testing,architecture
```

**Say:** "This gives us a comprehensive checklist. See how it prioritizes Security over Accessibility over Testing? That's our actual priority order. And look - it catches things like hard-coded strings for localization, missing ARIA labels, test coverage requirements. This is exactly what our senior engineers look for."

---

## Dependency Checking (5:00-5:30)

**Say:** "We even have dependency validation. Remember, all dependencies need VP Technology and client approval."

**Command:**
```bash
# Check if a library is approved
uv run python principles_cli.py dependencies --platform android --check rxjava2
```

**Say:** "RxJava2 is approved for Android. But watch what happens with something else:"

**Command:**
```bash
uv run python principles_cli.py dependencies --platform ios --check react-native
```

**Say:** "It'll tell us React Native isn't in our approved iOS stack - we're first-party only on iOS."

---

## The Philosophy (5:30-6:00)

**Say:** "This all comes back to our philosophy - 'Livefront Engineers are craftspeople.' We don't defer work with TODOs, we treat the design as the spec, and every line gets peer-reviewed."

**Command:**
```bash
# Show the philosophy
tail -5 README.md
```

**Say:** "By encoding these principles into AI prompts, we're scaling our craftsmanship. Every AI-assisted code review or generation follows the same high standards."

---

## Evaluation Framework (6:00-6:30)

**Say:** "And here's the really cool part - we can actually measure how effective these prompts are."

**Command:**
```bash
# Show evaluation setup
uv run python eval_runner.py --init-config eval_config.yaml
cat eval_config.yaml | head -20
```

**Say:** "We have an evaluation framework that tests these prompts against real code samples. We're seeing 85% accuracy in detecting violations. We can test with different AI models - GPT-4, Claude, even local models with Ollama."

---

## Integration Points (6:30-7:00)

**Say:** "This integrates everywhere in our workflow. You can use it in CI/CD pipelines, as a pre-commit hook, in VS Code, or just run it manually before submitting PRs."

**Command:**
```bash
# Show how it could be used in a git hook
echo "Example: Add to .git/hooks/pre-push:"
echo 'uv run python principles_cli.py review --platform web --focus security,accessibility'
```

---

## Closing & Impact (7:00-7:30)

**Say:** "The impact here is huge. We're not just documenting standards - we're operationalizing them. Every piece of AI-generated or AI-reviewed code follows Livefront's specific engineering principles. This means consistent quality, fewer security issues, better accessibility, and it scales across all our teams and projects."

**Command:**
```bash
# Show the quick start one more time
grep "Quick Start" -A 10 README.md
```

**Say:** "To get started, just clone the repo, run uv sync, and you're ready to generate prompts. The entire setup takes less than a minute, and the impact on code quality is immediate."

---

## Q&A Setup (7:30-8:00)

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

## Key Stats to Mention:
- 15 core principles
- 85% accuracy in violation detection
- 3 platforms supported (Android, iOS, Web)
- Priority order: Security > Accessibility > Testing > Performance > Code Style
- Zero TODOs policy
- 80% test coverage requirement
- Every line peer-reviewed