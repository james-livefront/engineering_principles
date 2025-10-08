"""Prompt enhancement utilities using LLM"""

import hashlib
import os
import sys
from pathlib import Path
from typing import Protocol


class LLMClient(Protocol):
    """Protocol for LLM clients that can enhance prompts"""

    def generate(self, prompt: str) -> str: ...


def enhance_prompt_with_llm(prompt: str, llm_client: LLMClient, show_diff: bool = False) -> str:
    """Enhance prompt with latest security/accessibility practices using LLM

    Args:
        prompt: Base prompt to enhance
        llm_client: LLM client that implements generate method
        show_diff: Whether to show difference between original and enhanced

    Returns:
        Enhanced prompt with additional patterns and practices
    """
    cache_dir = Path(".cache")
    cache_dir.mkdir(exist_ok=True)

    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
    cache_file = cache_dir / f"enhanced_{prompt_hash}.txt"

    if cache_file.exists():
        print("✓ Using cached enhanced prompt", file=sys.stderr)
        with open(cache_file) as f:
            enhanced = f.read()
    else:
        print("Enhancing prompt with latest practices using LLM...", file=sys.stderr)

        # Request ONLY additional content from LLM (not full prompt replacement)
        enhancement_request = f"""You are an expert in engineering standards across \
security and accessibility.

Generate ADDITIONAL detection patterns to complement the existing prompt below.
Output ONLY the new patterns you want to add - do NOT rewrite or repeat the original prompt.

The additional patterns should include:

1. **Latest OWASP Patterns** (2023-2024):
   - Specific regex patterns for recent vulnerabilities
   - Real vulnerability patterns (not localhost/test code)

2. **Modern Framework Antipatterns**:
   - React 18+, Angular 15+, Vue 3+, Svelte 4+
   - Specific code examples with detection patterns

3. **WCAG 2.2 Violations** (2023):
   - Latest accessibility requirements
   - Specific HTML/ARIA patterns that violate standards

4. **Advanced Detection Techniques**:
   - Multi-line vulnerability patterns
   - Semantic issues beyond simple regex
   - Context-aware detection patterns

5. **False Positive Prevention**:
   - Explicit patterns to avoid flagging localhost/dev URLs
   - How to distinguish test files from production code
   - Context-based exception handling

Format your output as additional detection rules that can be appended to the existing prompt.
Be specific with regex patterns and code examples.

Original prompt to complement:
---
{prompt}
---

Generate ONLY additional patterns (do not repeat the original prompt):"""

        try:
            additional_content = llm_client.generate(enhancement_request)

            # Programmatically append LLM content to original prompt
            enhanced = f"""{prompt}

---

## Enhanced Patterns (LLM-Generated)

{additional_content}"""

            # Cache the enhanced prompt
            with open(cache_file, "w") as f:
                f.write(enhanced)

            print("✓ Enhancement complete (original + LLM additions)", file=sys.stderr)

        except Exception as e:
            print(f"Enhancement failed: {e}", file=sys.stderr)
            print("→ Using original prompt", file=sys.stderr)
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


def get_openai_client() -> LLMClient | None:
    """Get OpenAI LLM client if available

    Returns:
        LLMClient instance or None if OpenAI not available
    """
    try:
        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None

        class OpenAIClient:
            def __init__(self) -> None:
                self.client = OpenAI(api_key=api_key)

            def generate(self, prompt: str) -> str:
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                )
                return response.choices[0].message.content or ""

        return OpenAIClient()

    except ImportError:
        return None
