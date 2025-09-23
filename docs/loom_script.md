# Loom Recording Script: LEAP (Livefront Engineering Automated Principles)

## Opening (0:00-0:30)

**Say:** "Hey team, I want to show you LEAP - Livefront Engineering Automated Principles. This is very much an ongoing experiment - we're exploring how to codify human principles into patterns that AI can reliably work with. LEAP generates prompts that attempt to enforce our code standards across Android, iOS, and Web platforms. Instead of hoping developers remember all our standards, we're experimenting with encoding them into prompts that AI assistants will follow automatically."

**Command:**

```bash
ls -la
cat README.md
```

---

## The Problem We're Solving (0:30-1:00)

**Say:** "We have 15 core engineering principles at Livefront, from security to accessibility to testing requirements.

command

Different platforms then have different rules to support these principles. Android uses Dagger and RxJava, iOS is first-party only, Web has its own stack. Trying to cram all this into a monolithic prompt wastes context and confuses the AI. This tool attempts to solve that by generating right-sized prompts tailored to the platform and focus area."

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

**Say:** "Watch how it adapts to each platform. Let me show you Android versus iOS."

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

## System Prompts for Code Generation (3:00-4:00)

**Say:** "But it's not just for reviews. We can generate system prompts that set up AI assistants to write code following our standards from the start. Notice this creates a different type of prompt - a system prompt that defines the AI's role and constraints."

**Command:**

```bash
uv run python principles_cli.py generate --platform android --component ui | mdless
```

**Say:** "See the difference? This isn't a request to review code - it's setting up the AI as a 'Code Generation Assistant for Android UI' with all our platform requirements built in. You'd use this as the system prompt, then ask it to generate specific components. The generated code will already follow our standards."

---

## Two-Prompt Pattern (4:00-5:00)

**Say:** "Here's the key insight - we generate two different types of prompts for different purposes. Let me show you the pattern."

**Command:**

```bash
# Generate system prompt for AI assistant setup
uv run python principles_cli.py generate --platform web --component ui > system_prompt.txt

# Generate user prompt for reviewing code
uv run python principles_cli.py review --platform web --focus security,accessibility > review_prompt.txt

# Show the difference
echo "=== SYSTEM PROMPT ==="
head -10 system_prompt.txt
echo "=== USER PROMPT ==="
head -10 review_prompt.txt
```

**Say:** "See the difference? The system prompt sets up the AI as a 'Code Generation Assistant' with persistent constraints. The user prompt makes a specific request to review code. This pattern gives us maximum flexibility - we can set up domain-specific AI assistants, then use targeted review prompts for specific tasks."

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
head -15 README.md | tail -10 | mdcat
```

**Say:** "By encoding these principles into AI prompts, we're scaling our craftsmanship. Every AI-assisted code review or generation follows the same high standards."

---

## System Architecture & Philosophy (6:00-7:30)

**Say:** "Let me show you how this is organized. The key to avoid tight coupling is separating what we believe from how we enforce it. This modular architecture makes the system maintainable and evolvable."

**Command:**

```bash
# Show the modular architecture
tree -L 2 -d
```

**Say:** "Notice the clear separation - core beliefs versus implementation modules. This decomposition is intentional. Let me explain the philosophy:"

**Command:**

```bash
# Show core philosophy - what we believe
ls -la core/
head -20 core/philosophy.yaml | mdcat
```

**Say:** "The core directory contains our immutable beliefs - our philosophy, the 15 principles, platform configurations. This is the 'what' and 'why' of our engineering culture. These rarely change."

**Command:**

```bash
# Show the principles - universal truths
head -30 core/principles.yaml | mdcat
```

**Say:** "These principles apply regardless of implementation details. Testing at 80% coverage, zero TODOs, accessibility - these are universal."

**Command:**

```bash
# Show modules - how we enforce
ls -la modules/detection/rules/
head -25 modules/detection/rules/security.yaml | mdcat
```

**Say:** "Now the modules directory - this is 'how' we enforce those principles. Detection rules for finding violations, generation patterns for writing compliant code. See these regex patterns? They catch hardcoded secrets, insecure URLs, weak crypto. This separation is crucial - we can evolve our detection techniques, add new patterns, improve accuracy, all without touching our core beliefs. The 'what' stays constant while the 'how' improves."

**Command:**

```bash
# Show the evaluation framework
ls evals/detection/
head -30 evals/detection/security_test_cases.yaml | mdcat
```

**Say:** "And the evals directory validates that our detection actually works. Real code samples with known violations to test our patterns against. This modular architecture means each piece has a single responsibility - core defines beliefs, modules implement enforcement, evals validate effectiveness. Clean separation of concerns."

---

## Evaluation in Action (7:30-8:30)

**Say:** "Now let me show you how this all comes together in practice. I'll generate a web security prompt and test its effectiveness."

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

## Integration Points (8:30-9:00)

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

## Future Opportunities (9:00-9:30)

**Say:** "What's exciting is we've only scratched the surface. We have rich YAML data that we haven't even tapped into yet."

**Command:**

```bash
# Show unused but valuable YAML sections
grep -A 5 "preflight_checklist:" core/principles.yaml | mdcat
grep -A 3 "escalation_path:" core/enforcement.yaml | mdcat
```

**Say:** "See these sections? Preflight checklists for release readiness, escalation paths for severity handling, cultural expectations for onboarding, code review processes. Imagine generating release checklists tailored to each platform, or onboarding prompts that teach new engineers our culture. The foundation is there - we just need to wire it up."

**Command:**

```bash
# Show the roadmap for what's next
grep -A 4 "Unused YAML" docs/roadmap.md | mdcat
```

**Say:** "These could become new CLI commands - 'release-checklist' for QA, 'onboard' for new hires, 'review-guide' for teaching effective code reviews. The modular architecture makes this easy to add."

---

## Closing & Impact (9:30-10:00)

**Say:** "The potential impact here is big. We're not just documenting standards - we're operationalizing them. Every piece of AI-generated or AI-reviewed code follows Livefront's specific engineering principles. This means consistent quality, fewer security issues, better accessibility, and it scales across all our teams and projects. Hopefully!

But remember, this is an experiment. We're learning about the balance between hard-coded rules and LLM intelligence, what makes good evals for our prompts, and how to codify human judgment. The tool will evolve as we learn more."

**Command:**

```bash
# Show the quick start one more time
grep "Quick Start" -A 10 README.md
```

**Say:** "To get started, just clone the repo, run uv sync, and you're ready to generate prompts. The entire setup takes less than a minute."

---

## Q&A Setup (10:00-10:30)

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

**Say:** "And that's LEAP - our experiment in automated engineering principles. Questions?"

---

## Key Stats to Mention

- 15 core principles
- 85% accuracy in violation detection
- 3 platforms supported (Android, iOS, Web)
- Priority order: Security > Accessibility > Testing > Performance > Code Style
- Zero TODOs policy
- 80% test coverage requirement
- Every line peer-reviewed
