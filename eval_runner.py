#!/usr/bin/env python3
"""Test engineering principle prompts against real cases"""

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, TypedDict

import yaml


def load_dotenv() -> None:
    """Load .env file"""
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()


load_dotenv()


class ExpectedResult(TypedDict):
    detected: bool
    rule: str | None
    severity: str | None
    message_contains: str | None
    suggestion_contains: str | None
    reason: str | None


class TestCase(TypedDict):
    id: str
    name: str
    category: str
    code: str
    language: str
    file_path: str | None
    expected: ExpectedResult


class DetectionResponse(TypedDict):
    found: bool
    confidence: float
    message: str



@dataclass
class TestResult:
    test_id: str
    name: str
    expected: bool
    detected: bool
    confidence: float
    message: str
    correct: bool
    details: dict[str, Any]


# Detection configuration constants
VIOLATION_INDICATORS = [
    "violation", "issue", "problem", "error", "warning",
    "fix", "should", "must", "missing", "incorrect"
]
CONFIDENCE_THRESHOLD = 3
MIN_INDICATORS_FOR_DETECTION = 2


class AIEvaluator(Protocol):
    """Protocol for AI evaluators"""
    def evaluate_code(self, prompt: str) -> str:
        ...


@dataclass
class EvaluationReport:
    total_tests: int
    correct_predictions: int
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    results_by_category: dict[str, dict[str, float]]
    failed_tests: list[TestResult]


class PromptEvaluator:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.detection_tests = self._load_detection_tests()
        self.generation_tests = self._load_generation_tests()

    def _load_detection_tests(self) -> dict[str, list[dict]]:
        """Load detection test cases"""
        tests = {}
        detection_dir = self.base_path / "evals" / "detection"

        if detection_dir.exists():
            for test_file in detection_dir.glob("*_test_cases.yaml"):
                principle = test_file.stem.replace("_test_cases", "")
                try:
                    with open(test_file) as f:
                        data = yaml.safe_load(f)
                        if isinstance(data, dict) and "test_cases" in data:
                            tests[principle] = data["test_cases"]
                except Exception as e:
                    print(f"Error loading {test_file}: {e}")

        return tests

    def _load_generation_tests(self) -> dict[str, list[dict]]:
        """Load generation test cases"""
        tests = {}
        generation_dir = self.base_path / "evals" / "generation"

        if generation_dir.exists():
            for test_file in generation_dir.glob("*_challenges.yaml"):
                category = test_file.stem.replace("_challenges", "")
                try:
                    with open(test_file) as f:
                        data = yaml.safe_load(f)
                        if isinstance(data, dict) and "test_cases" in data:
                            tests[category] = data["test_cases"]
                except Exception as e:
                    print(f"Error loading {test_file}: {e}")

        return tests
    def evaluate_detection_prompt(
        self,
        prompt: str,
        ai_evaluator: AIEvaluator,
        principles: list[str] | None = None,
    ) -> EvaluationReport:
        """Evaluate detection prompt against test cases with Smart Context Detection"""
        all_results: list[TestResult] = []
        category_stats: dict[str, dict[str, float]] = {}

        # Parse prompt metadata for Smart Context Detection
        metadata = parse_prompt_metadata(prompt)
        prompt_platform = metadata.get("platform")
        prompt_focus = metadata.get("focus", "").split(",") if metadata.get("focus") else []

        # Clean up focus areas (remove empty strings and whitespace)
        prompt_focus = [f.strip() for f in prompt_focus if f.strip()]

        # Log Smart Context Detection activation
        if metadata:
            print(f"🎯 Smart Context Detection activated:")
            if prompt_platform:
                print(f"   Platform: {prompt_platform}")
            if prompt_focus:
                print(f"   Focus areas: {', '.join(prompt_focus)}")
            print()

        tests_to_run = self.detection_tests
        if principles:
            tests_to_run = {k: v for k, v in tests_to_run.items() if k in principles}
        elif prompt_focus:
            # If no explicit principles but prompt has focus metadata, use that
            tests_to_run = {k: v for k, v in tests_to_run.items() if k in prompt_focus}

        for principle, test_cases in tests_to_run.items():
            print(f"\nTesting {principle} detection...")

            # Filter test cases by platform if specified in prompt metadata
            filtered_test_cases = test_cases
            if prompt_platform:
                filtered_test_cases = [
                    tc for tc in test_cases
                    if tc.get("category", "").lower() == prompt_platform.lower() or
                       "platform" not in tc or
                       tc.get("platform", "").lower() == prompt_platform.lower()
                ]
                if filtered_test_cases != test_cases:
                    print(f"  Filtered to {len(filtered_test_cases)}/{len(test_cases)} test cases for platform '{prompt_platform}'")

            principle_results: list[TestResult] = []
            for test_case in filtered_test_cases:
                result = self._run_detection_test(prompt, test_case, ai_evaluator)
                all_results.append(result)
                principle_results.append(result)

                status = "✓" if result.correct else "✗"
                print(f"  {status} {result.name}")

            correct = sum(1 for r in principle_results if r.correct)
            total = len(principle_results)
            category_stats[principle] = {
                "accuracy": correct / total if total > 0 else 0,
                "total": total,
                "correct": correct,
            }

        return self._calculate_evaluation_report(all_results, category_stats)
    def _run_detection_test(
        self, prompt: str, test_case: dict, ai_evaluator: AIEvaluator
    ) -> TestResult:
        """Run single detection test"""
        try:
            full_prompt = (
                f"{prompt}\n\nCode to review:\n\n"
                f"```{test_case['language']}\n{test_case['code']}\n```"
            )

            ai_response = ai_evaluator.evaluate_code(full_prompt)
            detected = self._parse_detection_response(ai_response, test_case)
            expected = test_case["expected"]["detected"]

            return TestResult(
                test_id=test_case["id"],
                name=test_case["name"],
                expected=expected,
                detected=detected["found"],
                confidence=detected.get("confidence", 1.0),
                message=detected.get("message", ""),
                correct=expected == detected["found"],
                details={
                    "category": test_case["category"],
                    "language": test_case["language"],
                    "ai_response": ai_response,
                },
            )

        except Exception as e:
            return TestResult(
                test_id=test_case.get("id", "unknown"),
                name=test_case.get("name", "unknown"),
                expected=False,
                detected=False,
                confidence=0.0,
                message=f"Error: {str(e)}",
                correct=False,
                details={"error": str(e)},
            )
    def _parse_detection_response(self, ai_response: str, test_case: dict) -> dict:
        """Parse AI response for violations using detection constants"""
        response_lower = ai_response.lower()

        found_indicators = sum(
            1 for indicator in VIOLATION_INDICATORS
            if indicator in response_lower
        )

        detected = found_indicators >= MIN_INDICATORS_FOR_DETECTION
        confidence = min(found_indicators / CONFIDENCE_THRESHOLD, 1.0)

        return {
            "found": detected,
            "confidence": confidence,
            "message": (ai_response[:200] + "..." if len(ai_response) > 200 else ai_response),
        }

    def _calculate_evaluation_report(
        self, results: list[TestResult], category_stats: dict[str, dict[str, Any]]
    ) -> EvaluationReport:
        """Calculate evaluation metrics"""
        if not results:
            return EvaluationReport(0, 0, 0, 0, 0, 0, {}, [])

        total_tests = len(results)
        correct_predictions = sum(1 for r in results if r.correct)
        accuracy = correct_predictions / total_tests

        true_positives = sum(1 for r in results if r.expected and r.detected)
        false_positives = sum(1 for r in results if not r.expected and r.detected)
        false_negatives = sum(1 for r in results if r.expected and not r.detected)

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0
        )
        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0
        )
        f1_score = (
            2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        )

        failed_tests = [r for r in results if not r.correct]

        return EvaluationReport(
            total_tests=total_tests,
            correct_predictions=correct_predictions,
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1_score,
            results_by_category=category_stats,
            failed_tests=failed_tests,
        )

class APIEvaluator:
    """API-based code evaluator implementing AIEvaluator protocol"""

    def __init__(self, provider: str, model: str, base_url: str) -> None:
        self.provider = provider
        self.model = model
        self.base_url = base_url

        try:
            import openai  # noqa: F401
        except ImportError:
            raise ImportError("OpenAI package is required for API-based evaluation") from None

        if provider == "openai" and not os.getenv("OPENAI_API_KEY"):
            raise ValueError(f"API key required for provider: {provider}")

    def evaluate_code(self, prompt: str) -> str:
        """Evaluate code using API"""
        import openai

        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Code reviewer for engineering principles."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
                max_tokens=4000,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            return f"API Error: {e}"


def load_config(config_path: str) -> dict[str, Any]:
    """Load configuration from YAML or JSON file"""
    path = Path(config_path)

    if not path.exists():
        return {}

    try:
        with open(path) as f:
            if path.suffix.lower() in [".yaml", ".yml"]:
                data = yaml.safe_load(f)
                return dict(data) if data is not None else {}
            elif path.suffix.lower() == ".json":
                data = json.load(f)
                return dict(data) if isinstance(data, dict) else {}
            else:
                return {}
    except Exception:
        return {}


def mock_ai_evaluator(prompt: str) -> str:
    """Mock AI evaluator function for testing"""
    # This would be replaced with actual AI API calls
    return (
        "I found several issues in this code including security "
        "vulnerabilities and missing accessibility attributes."
    )


def parse_prompt_metadata(prompt: str) -> dict[str, str]:
    """Parse metadata from prompt header"""
    import re

    metadata = {}
    match = re.search(r"<!-- PROMPT_METADATA\n(.*?)\n-->", prompt, re.DOTALL)

    if match:
        metadata_text = match.group(1)
        for line in metadata_text.strip().split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()

    return metadata


def enhance_prompt_with_llm(
    prompt: str, api_evaluator: APIEvaluator, show_diff: bool = False
) -> str:
    """Enhance a prompt with latest security/accessibility practices using LLM"""

    # Check cache first
    import hashlib

    cache_dir = Path(".cache")
    cache_dir.mkdir(exist_ok=True)

    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
    cache_file = cache_dir / f"enhanced_{prompt_hash}.txt"

    if cache_file.exists():
        print("Using cached enhanced prompt...")
        with open(cache_file) as f:
            enhanced = f.read()
    else:
        print("Enhancing prompt with latest practices using LLM...")

        enhancement_prompt = f"""Expert in engineering standards across security and accessibility.

Enhance this prompt with additional specific detection patterns while MAINTAINING ACCURACY.

**ADD these enhancement layers (preserve ALL original content):**

1. **Specific Modern Patterns** (2024/2025):
   - Latest OWASP patterns for REAL vulnerabilities (not localhost/test code)
   - Modern framework antipatterns (React 18+, TypeScript 5+)
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

        except Exception as e:
            print(f"Enhancement failed: {e}")
            print("Using original prompt...")
            enhanced = prompt

    if show_diff:
        print("\n" + "=" * 50)
        print("PROMPT ENHANCEMENT DIFF")
        print("=" * 50)

        # Simple diff - show first 500 chars of each
        print("\nOriginal (first 500 chars):")
        print(prompt[:500] + "...")
        print("\nEnhanced (first 500 chars):")
        print(enhanced[:500] + "...")
        print("=" * 50 + "\n")

    return enhanced


def mock_ai_generator(prompt: str) -> str:
    """Mock AI generator function for testing"""
    # This would be replaced with actual AI API calls
    return "// Generated code would appear here"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Test prompt effectiveness against test cases",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n  %(prog)s --mode detection --platform web --focus accessibility\n  %(prog)s --enhanced --platform android --focus security"
    )
    
    parser.add_argument("--mode", choices=["detection", "generation", "both"], default="detection")
    parser.add_argument("--principles", nargs="*", help="Principles to test")
    parser.add_argument("--platform", choices=["android", "ios", "web"])
    parser.add_argument("--focus", help="Comma-separated focus areas")
    parser.add_argument("--enhanced", action="store_true", help="Enhance with LLM")
    parser.add_argument("--output", help="Output file for report")
    parser.add_argument("--prompt-file", help="Prompt file to test")

    args = parser.parse_args()

    # Parse comma-separated values
    if args.principles:
        principles = []
        for p in args.principles:
            principles.extend([x.strip() for x in p.split(",")])
        args.principles = principles

    evaluator = PromptEvaluator()

    if args.prompt_file:
        with open(args.prompt_file) as f:
            test_prompt = f.read()
    else:
        test_prompt = "You are a code reviewer. Find violations of engineering principles."

    effective_principles = args.principles
    if args.focus:
        effective_principles = [x.strip() for x in args.focus.split(",")]

    print(f"Mode: {args.mode}")
    if args.platform:
        print(f"Platform: {args.platform}")
    if effective_principles:
        print(f"Focus: {', '.join(effective_principles)}")

    if args.mode in ["detection", "both"]:
        api_evaluator = APIEvaluator("openai", "gpt-4o", "https://api.openai.com/v1")

        report = evaluator.evaluate_detection_prompt(test_prompt, api_evaluator, effective_principles)
        
        # Simple report output
        print(f"\nResults: {report.accuracy:.2%} accuracy")
        print(f"Precision: {report.precision:.2%}")
        print(f"Recall: {report.recall:.2%}")
        print(f"F1 Score: {report.f1_score:.2%}")
        
        if args.output:
            with open(args.output, "w") as f:
                f.write(f"Accuracy: {report.accuracy:.2%}\n")
                f.write(f"Precision: {report.precision:.2%}\n")
                f.write(f"Recall: {report.recall:.2%}\n")
                f.write(f"F1 Score: {report.f1_score:.2%}\n")


if __name__ == "__main__":
    main()