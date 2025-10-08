# Evaluation Metrics Guide

Interpret prompt evaluation results and optimize detection performance.

## Core Metrics

### Accuracy

Overall correctness - how many predictions were right out of all predictions

**Formula**: `(True Positives + True Negatives) / Total Predictions`

**Example**: 85% accuracy = 85 out of 100 correct predictions

**Note**: Can be misleading with imbalanced datasets

### Precision

When we predict a violation, how often are we right?

**Formula**: `True Positives / (True Positives + False Positives)`

**Example**: 90% precision = 9 out of 10 flagged violations are actual violations

**Impact**: High precision = fewer false alarms

### Recall (Sensitivity)

Of all actual violations, how many did we catch?

**Formula**: `True Positives / (True Positives + False Negatives)`

**Example**: 75% recall = caught 3 out of 4 real violations

**Impact**: High recall = fewer missed violations

### F1 Score

Harmonic mean of precision and recall

**Formula**: `2 × (Precision × Recall) / (Precision + Recall)`

**Use**: Single metric for balancing precision and recall

## Code Review Context

### The Trade-off

| Scenario | Precision | Recall | Impact |
|----------|-----------|--------|--------|
| Conservative | High (90%+) | Low (60%) | Few false alarms, misses violations |
| Aggressive | Low (70%) | High (95%) | Catches most issues, many false positives |
| Balanced | Medium (80%) | Medium (80%) | Reasonable compromise |

### Priority by Domain

**Security Detection**:

- **Recall Priority**: Missing a security vulnerability is worse than a false positive
- **Target**: Recall > 90%, Precision > 70%

**Accessibility Detection**:

- **Precision Priority**: False accessibility violations frustrate developers
- **Target**: Precision > 85%, Recall > 75%

**Code Style**:

- **Precision Priority**: Style false positives create noise
- **Target**: Precision > 95%, Recall > 60%

**Testing Coverage**:

- **Balanced**: Both missed tests and false test complaints are problematic
- **Target**: F1 Score > 0.80

## Practical Examples

### Security Violation Detection

```text
Test Cases: 100 code samples
- Actual vulnerabilities: 20
- Predicted vulnerabilities: 25
- Correct predictions: 18 (True Positives)
- False alarms: 7 (False Positives)
- Missed vulnerabilities: 2 (False Negatives)

Accuracy = (18 + 73) / 100 = 91%
Precision = 18 / (18 + 7) = 72%
Recall = 18 / (18 + 2) = 90%
F1 Score = 2 × (0.72 × 0.90) / (0.72 + 0.90) = 80%
```

**Interpretation**: Good recall (90% caught) but moderate precision (28% false alarm rate). Tighten detection patterns to reduce false positives.

### Accessibility Detection

```text
Test Cases: 150 UI components
- Actual violations: 30
- Predicted violations: 22
- Correct predictions: 20 (True Positives)
- False alarms: 2 (False Positives)
- Missed violations: 10 (False Negatives)

Accuracy = (20 + 118) / 150 = 92%
Precision = 20 / (20 + 2) = 91%
Recall = 20 / (20 + 10) = 67%
F1 Score = 2 × (0.91 × 0.67) / (0.91 + 0.67) = 77%
```

**Interpretation**: Excellent precision (few false alarms) but concerning recall (missing 1/3 violations). Expand detection patterns or lower thresholds.

## Optimization Strategies

### Improving Precision

- **Tighten patterns**: More specific regex/detection rules
- **Add context**: Consider surrounding code, not just isolated patterns
- **Platform filtering**: Different rules for different platforms
- **Severity thresholds**: Only flag higher-confidence violations

### Improving Recall

- **Expand patterns**: More comprehensive detection rules
- **Lower thresholds**: Catch edge cases and variations
- **Multiple approaches**: Regex + semantic analysis + heuristics
- **Test case analysis**: Study missed violations for pattern gaps

### Balancing Both

- **Ensemble methods**: Combine multiple detection approaches
- **Confidence scoring**: Flag high-confidence violations immediately, review medium-confidence
- **Iterative refinement**: Use evaluation results to tune detection rules
- **Domain-specific tuning**: Different thresholds per violation type

## Evaluation Workflow

1. **Baseline Measurement**: Run evaluation on current prompt/rules
2. **Identify Weaknesses**: Low precision? High false positives. Low recall? Missing violations.
3. **Targeted Improvements**: Adjust detection patterns based on failure analysis
4. **Re-evaluate**: Measure impact of changes
5. **A/B Testing**: Compare multiple approaches systematically

## Multi-Model Comparison

When comparing multiple detection approaches:

```bash
# Global (after pipx install)
leap-eval --compare-prompts config1.yaml config2.yaml

# Local (development)
uv run python eval_runner.py --compare-prompts config1.yaml config2.yaml
```

**Key Comparisons**:

- **Coverage Complementarity**: Do configs catch different violation types?
- **Consistency**: Do configs agree on clear cases?
- **Failure Patterns**: Where do configs systematically struggle?
- **Performance Trade-offs**: Speed vs accuracy implications

## Red Flags

**Accuracy Paradox**: High accuracy with low precision/recall indicates class imbalance - predicting "no violation" everywhere gives high accuracy but useless detection.

**Perfect Metrics**: 100% precision and recall indicates overfitting to test cases or insufficient test diversity.

**Extreme Trade-offs**: >95% precision with <50% recall (or vice versa) suggests detection rules too narrow/broad.

## Implementation Notes

Current evaluation framework (`eval_runner.py`) provides all these metrics. Use `--output report.json` to get detailed breakdown by violation type and platform.

For custom analysis:

- `EvaluationReport.results_by_category`: Per-category metrics
- `EvaluationReport.failed_tests`: Detailed failure analysis
- `TestResult.confidence`: Individual prediction confidence scores
