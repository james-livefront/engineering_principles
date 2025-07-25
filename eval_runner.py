#!/usr/bin/env python3
"""
Engineering Principles Evaluation Runner

Tests the effectiveness of generated prompts by running them against test cases
and measuring how well AI systems detect violations and generate compliant code.
"""

import yaml
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Callable, TypedDict, Union
from dataclasses import dataclass
from datetime import datetime

# Type definitions for YAML data structures
class ExpectedResult(TypedDict):
    detected: bool
    rule: Optional[str]
    severity: Optional[str]
    message_contains: Optional[str]
    suggestion_contains: Optional[str]
    reason: Optional[str]

class TestCase(TypedDict):
    id: str
    name: str
    category: str
    code: str
    language: str
    file_path: Optional[str]
    expected: ExpectedResult

class GenerationChallenge(TypedDict):
    id: str
    name: str
    platform: str
    challenge: str
    requirements: Dict[str, str]
    expected_features: Dict[str, List[str]]

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
    details: Dict[str, Any]

@dataclass
class EvaluationReport:
    total_tests: int
    correct_predictions: int
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    results_by_category: Dict[str, Dict[str, float]]
    failed_tests: List[TestResult]

class PromptEvaluator:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.detection_tests = self._load_detection_tests()
        self.generation_tests = self._load_generation_tests()
    
    def _load_detection_tests(self) -> Dict[str, List[TestCase]]:
        """Load all detection test cases"""
        tests: Dict[str, List[TestCase]] = {}
        detection_dir = self.base_path / "evals" / "detection"
        
        if detection_dir.exists():
            for test_file in detection_dir.glob("*_test_cases.yaml"):
                principle = test_file.stem.replace("_test_cases", "")
                try:
                    with open(test_file, 'r') as f:
                        data = yaml.safe_load(f)
                        if isinstance(data, dict) and 'test_cases' in data:
                            tests[principle] = data['test_cases']
                except Exception as e:
                    print(f"Error loading {test_file}: {e}")
        
        return tests
    
    def _load_generation_tests(self) -> Dict[str, List[GenerationChallenge]]:
        """Load all generation test cases"""
        tests: Dict[str, List[GenerationChallenge]] = {}
        generation_dir = self.base_path / "evals" / "generation"
        
        if generation_dir.exists():
            for test_file in generation_dir.glob("*_challenges.yaml"):
                category = test_file.stem.replace("_challenges", "")
                try:
                    with open(test_file, 'r') as f:
                        data = yaml.safe_load(f)
                        if isinstance(data, dict) and 'test_cases' in data:
                            tests[category] = data['test_cases']
                except Exception as e:
                    print(f"Error loading {test_file}: {e}")
        
        return tests
    
    def evaluate_detection_prompt(
        self, 
        prompt: str, 
        ai_evaluator_func: Callable[[str], str], 
        principles: Optional[List[str]] = None
    ) -> EvaluationReport:
        """
        Evaluate how well a detection prompt identifies violations
        
        Args:
            prompt: The generated detection prompt to test
            ai_evaluator_func: Function that takes (prompt, code) and returns detection results
            principles: List of principles to test (None = all)
        """
        all_results: List[TestResult] = []
        category_stats: Dict[str, Dict[str, float]] = {}
        
        # Filter tests by requested principles
        tests_to_run = self.detection_tests
        if principles:
            tests_to_run = {k: v for k, v in tests_to_run.items() if k in principles}
        
        for principle, test_cases in tests_to_run.items():
            print(f"\\nTesting {principle} detection...")
            
            principle_results: List[TestResult] = []
            for test_case in test_cases:
                result = self._run_detection_test(prompt, test_case, ai_evaluator_func)
                all_results.append(result)
                principle_results.append(result)
                
                # Print progress
                status = "✓" if result.correct else "✗"
                print(f"  {status} {result.name}")
            
            # Calculate per-principle stats
            correct = sum(1 for r in principle_results if r.correct)
            total = len(principle_results)
            category_stats[principle] = {
                'accuracy': correct / total if total > 0 else 0,
                'total': total,
                'correct': correct
            }
        
        return self._calculate_evaluation_report(all_results, category_stats)
    
    def evaluate_generation_prompt(
        self,
        prompt: str,
        ai_generator_func: Callable[[str], str],
        ai_evaluator_func: Callable[[str], str],
        categories: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate how well a generation prompt creates compliant code
        
        Args:
            prompt: The generated code writing prompt to test
            ai_generator_func: Function that takes (prompt, challenge) and returns generated code
            ai_evaluator_func: Function that evaluates generated code for compliance
            categories: Categories to test (None = all)
        """
        all_results: List[Dict[str, Any]] = []
        
        # Filter tests by requested categories
        tests_to_run = self.generation_tests
        if categories:
            tests_to_run = {k: v for k, v in tests_to_run.items() if k in categories}
        
        for category, challenges in tests_to_run.items():
            print(f"\\nTesting {category} generation...")
            
            for challenge in challenges:
                result = self._run_generation_test(
                    prompt, challenge, ai_generator_func, ai_evaluator_func
                )
                all_results.append(result)
                
                # Print progress
                score = result.get('compliance_score', 0)
                status = "✓" if score >= 0.8 else "⚠" if score >= 0.6 else "✗"
                print(f"  {status} {challenge['name']} (Score: {score:.2f})")
        
        return {
            'total_challenges': len(all_results),
            'average_compliance': sum(r.get('compliance_score', 0) for r in all_results) / len(all_results),
            'results': all_results
        }
    
    def _run_detection_test(
        self, 
        prompt: str, 
        test_case: TestCase, 
        ai_evaluator_func: Callable[[str], str]
    ) -> TestResult:
        """Run a single detection test case"""
        try:
            # Combine prompt with test code
            full_prompt = f"{prompt}\\n\\nCode to review:\\n\\n```{test_case['language']}\\n{test_case['code']}\\n```"
            
            # Get AI evaluation
            ai_response = ai_evaluator_func(full_prompt)
            
            # Parse AI response to determine if violation was detected
            detected = self._parse_detection_response(ai_response, test_case)
            expected = test_case['expected']['detected']
            
            return TestResult(
                test_id=test_case['id'],
                name=test_case['name'],
                expected=expected,
                detected=detected['found'],
                confidence=detected.get('confidence', 1.0),
                message=detected.get('message', ''),
                correct=expected == detected['found'],
                details={
                    'category': test_case['category'],
                    'language': test_case['language'],
                    'ai_response': ai_response,
                    'expected_rule': test_case['expected'].get('rule'),
                    'expected_severity': test_case['expected'].get('severity')
                }
            )
            
        except Exception as e:
            return TestResult(
                test_id=test_case.get('id', 'unknown'),
                name=test_case.get('name', 'unknown'),
                expected=False,
                detected=False,
                confidence=0.0,
                message=f"Error: {str(e)}",
                correct=False,
                details={'error': str(e)}
            )
    
    def _run_generation_test(
        self,
        prompt: str,
        challenge: GenerationChallenge,
        ai_generator_func: Callable[[str], str],
        ai_evaluator_func: Callable[[str], str]
    ) -> Dict[str, Any]:
        """Run a single generation challenge"""
        try:
            # Generate code using the challenge
            full_prompt = f"{prompt}\\n\\nChallenge:\\n{challenge['challenge']}"
            generated_code = ai_generator_func(full_prompt)
            
            # Evaluate the generated code for compliance
            evaluation = self._evaluate_generated_code(
                generated_code, challenge, ai_evaluator_func
            )
            
            return {
                'challenge_id': challenge['id'],
                'name': challenge['name'],
                'platform': challenge['platform'],
                'generated_code': generated_code,
                'compliance_score': evaluation['score'],
                'feature_compliance': evaluation['features'],
                'missing_features': evaluation['missing'],
                'suggestions': evaluation['suggestions']
            }
            
        except Exception as e:
            return {
                'challenge_id': challenge.get('id', 'unknown'),
                'name': challenge.get('name', 'unknown'),
                'error': str(e),
                'compliance_score': 0.0
            }
    
    def _parse_detection_response(self, ai_response: str, test_case: TestCase) -> DetectionResponse:
        """Parse AI response to determine if violation was detected"""
        response_lower = ai_response.lower()
        
        # Look for indicators that a violation was found
        violation_indicators = [
            'violation', 'issue', 'problem', 'error', 'warning',
            'fix', 'should', 'must', 'missing', 'incorrect'
        ]
        
        found_indicators = sum(1 for indicator in violation_indicators 
                              if indicator in response_lower)
        
        # Simple heuristic: if multiple violation indicators, probably detected
        detected = found_indicators >= 2
        confidence = min(found_indicators / 3, 1.0)
        
        return {
            'found': detected,
            'confidence': confidence,
            'message': ai_response[:200] + "..." if len(ai_response) > 200 else ai_response
        }
    
    def _evaluate_generated_code(
        self, 
        generated_code: str, 
        challenge: Dict[str, Any],
        ai_evaluator_func
    ) -> Dict[str, Any]:
        """Evaluate generated code against challenge requirements"""
        expected_features = challenge.get('expected_features', {})
        evaluation_criteria = challenge.get('evaluation_criteria', {})
        
        # Use AI evaluator to check compliance
        eval_prompt = f"""
        Evaluate this generated code against these requirements:
        
        Challenge: {challenge['challenge']}
        Expected Features: {json.dumps(expected_features, indent=2)}
        
        Generated Code:
        ```{challenge.get('platform', 'typescript')}
        {generated_code}
        ```
        
        Score each category 0-1 and explain what's missing:
        """
        
        ai_evaluation = ai_evaluator_func(eval_prompt)
        
        # Parse the evaluation (simplified for demo)
        # In practice, you'd want more sophisticated parsing
        score = 0.7  # Placeholder - would parse from AI response
        
        return {
            'score': score,
            'features': expected_features,
            'missing': [],  # Would extract from AI response
            'suggestions': ai_evaluation
        }
    
    def _calculate_evaluation_report(
        self, 
        results: List[TestResult], 
        category_stats: Dict[str, Dict]
    ) -> EvaluationReport:
        """Calculate comprehensive evaluation metrics"""
        if not results:
            return EvaluationReport(0, 0, 0, 0, 0, 0, {}, [])
        
        total_tests = len(results)
        correct_predictions = sum(1 for r in results if r.correct)
        accuracy = correct_predictions / total_tests
        
        # Calculate precision, recall, F1
        true_positives = sum(1 for r in results if r.expected and r.detected)
        false_positives = sum(1 for r in results if not r.expected and r.detected)
        false_negatives = sum(1 for r in results if r.expected and not r.detected)
        
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        failed_tests = [r for r in results if not r.correct]
        
        return EvaluationReport(
            total_tests=total_tests,
            correct_predictions=correct_predictions,
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1_score,
            results_by_category=category_stats,
            failed_tests=failed_tests
        )
    
    def generate_report(self, report: EvaluationReport, output_file: Optional[str] = None) -> str:
        """Generate a formatted evaluation report"""
        report_text = f"""
# Engineering Principles Evaluation Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overall Results
- Total Tests: {report.total_tests}
- Correct Predictions: {report.correct_predictions}
- **Accuracy: {report.accuracy:.2%}**
- **Precision: {report.precision:.2%}**
- **Recall: {report.recall:.2%}**
- **F1 Score: {report.f1_score:.2%}**

## Results by Category
"""
        
        for category, stats in report.results_by_category.items():
            report_text += f"- **{category.title()}**: {stats['correct']}/{stats['total']} ({stats['accuracy']:.2%})\\n"
        
        if report.failed_tests:
            report_text += f"\\n## Failed Tests ({len(report.failed_tests)})\\n"
            for test in report.failed_tests[:10]:  # Limit to first 10
                report_text += f"- {test.test_id}: {test.name} (Expected: {test.expected}, Got: {test.detected})\\n"
        
        report_text += """
## Recommendations
- Focus on categories with accuracy < 80%
- Review failed test cases to improve detection rules
- Consider additional test cases for edge cases
"""
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_text)
        
        return report_text


def mock_ai_evaluator(prompt: str) -> str:
    """Mock AI evaluator function for testing"""
    # This would be replaced with actual AI API calls
    return "I found several issues in this code including security vulnerabilities and missing accessibility attributes."

def mock_ai_generator(prompt: str) -> str:
    """Mock AI generator function for testing"""
    # This would be replaced with actual AI API calls
    return "// Generated code would appear here"


def main():
    parser = argparse.ArgumentParser(description="Evaluate engineering principles prompts")
    parser.add_argument('--mode', choices=['detection', 'generation', 'both'], 
                       default='detection', help='Evaluation mode')
    parser.add_argument('--principles', nargs='*', 
                       help='Specific principles to test (detection mode)')
    parser.add_argument('--categories', nargs='*',
                       help='Specific categories to test (generation mode)')
    parser.add_argument('--output', help='Output file for report')
    parser.add_argument('--prompt-file', help='File containing prompt to test')
    
    args = parser.parse_args()
    
    evaluator = PromptEvaluator()
    
    # Load prompt to test
    if args.prompt_file:
        with open(args.prompt_file, 'r') as f:
            test_prompt = f.read()
    else:
        test_prompt = "You are a code reviewer. Find violations of engineering principles."
    
    print(f"Evaluating prompt effectiveness...")
    print(f"Mode: {args.mode}")
    
    if args.mode in ['detection', 'both']:
        print("\\nRunning detection evaluation...")
        report = evaluator.evaluate_detection_prompt(
            test_prompt, 
            mock_ai_evaluator, 
            args.principles
        )
        
        report_text = evaluator.generate_report(report, args.output)
        print(report_text)
    
    if args.mode in ['generation', 'both']:
        print("\\nRunning generation evaluation...")
        results = evaluator.evaluate_generation_prompt(
            test_prompt,
            mock_ai_generator,
            mock_ai_evaluator,
            args.categories
        )
        
        print(f"Generation Results: {results['average_compliance']:.2%} average compliance")


if __name__ == "__main__":
    main()