"""Prompt enhancement utilities using LLM"""

import hashlib
import os
from pathlib import Path
from typing import Protocol


class APIEvaluator(Protocol):
    """Protocol for AI evaluators that can enhance prompts"""

    def evaluate_code(self, prompt: str) -> str: ...


def enhance_prompt_with_llm(
    prompt: str, api_evaluator: APIEvaluator, show_diff: bool = False
) -> str:
    """Enhance prompt with latest security/accessibility practices using LLM

    Args:
        prompt: Base prompt to enhance
        api_evaluator: API client that implements evaluate_code method
        show_diff: Whether to show difference between original and enhanced

    Returns:
        Enhanced prompt with additional patterns and practices
    """
    # Check cache first
    cache_dir = Path(".cache")
    cache_dir.mkdir(exist_ok=True)

    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
    cache_file = cache_dir / f"enhanced_{prompt_hash}.txt"

    if cache_file.exists():
        print("✓ Using cached enhanced prompt")
        with open(cache_file) as f:
            enhanced = f.read()
    else:
        print("🔄 Enhancing prompt with latest practices using LLM...")

        enhancement_prompt = f"""Expert in engineering standards across security and accessibility.

Enhance this prompt with additional specific detection patterns while MAINTAINING ACCURACY.

**ADD these enhancement layers (preserve ALL original content):**

1. **Specific Modern Patterns**:
   - Latest OWASP patterns for REAL vulnerabilities (not localhost/test code)
   - Modern framework antipatterns (React, Angular, Vue, Svelte)
   - Current WCAG 2.2 VIOLATIONS (not compliant code)
   - Contemporary testing gaps, not all missing tests

2. **Precision-Focused Analysis**:
   - AVOID FALSE POSITIVES - localhost/dev URLs are NOT violations
   - Test files and examples are NOT production violations
   - Good accessibility (proper ARIA, good contrast) should PASS
   - Context matters - be specific about ACTUAL problems

3. **Advanced Pattern Detection**:
   - Multi-line vulnerabilities that span code blocks
   - Semantic issues beyond regex patterns
   - Compound violations that require understanding context

4. **Real-Time Intelligence**:
   - Current industry standards and best practices
   - Tool-specific guidance (ESLint, TypeScript, testing frameworks)
   - Platform evolution awareness (latest iOS, Android, Web APIs)

**Focus on actionable, specific enhancements like:**
- Exact regex patterns for latest vulnerabilities
- Specific code examples with before/after
- Framework-specific detection rules
- Cross-cutting analysis techniques
- Specific HTML attributes for accessibility
- Concrete code smells with examples

Original prompt:
{prompt}

Enhanced prompt (keep ALL original content and ADD specifics):"""

        try:
            enhanced = api_evaluator.evaluate_code(enhancement_prompt)

            # Cache the enhanced prompt
            with open(cache_file, "w") as f:
                f.write(enhanced)

            print("✓ Enhancement complete")

        except Exception as e:
            print(f"⚠️ Enhancement failed: {e}")
            print("→ Using original prompt")
            enhanced = prompt

    if show_diff:
        print("\n" + "=" * 50)
        print("PROMPT ENHANCEMENT DIFF")
        print("=" * 50)

        # Simple diff - show first 500 chars of each
        print("\nOriginal (first 500 chars):")
        print(prompt[:500])
        print("\n" + "-" * 50)
        print("\nEnhanced (first 500 chars):")
        print(enhanced[:500])
        print("\n" + "=" * 50)

    return enhanced


def get_openai_evaluator() -> APIEvaluator | None:
    """Get OpenAI API evaluator if available

    Returns:
        APIEvaluator instance or None if OpenAI not available
    """
    try:
        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None

        class OpenAIEvaluator:
            def __init__(self) -> None:
                self.client = OpenAI(api_key=api_key)

            def evaluate_code(self, prompt: str) -> str:
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                )
                return response.choices[0].message.content or ""

        return OpenAIEvaluator()

    except ImportError:
        return None
