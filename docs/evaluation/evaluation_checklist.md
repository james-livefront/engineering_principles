# Loom Script Evaluation Checklist

Based on testing all commands from the loom script, here are the improvements needed to make the YAML configuration more effective for LLM prompts:

## ✅ Major Issues Found

### 1. **Empty Detection Rules for Non-Security Focus Areas**

- [X] **Problem**: When focusing on `architecture`, `testing`, or other areas, Detection Rules section is completely empty
- [X] **Fix**: Add detection patterns for architecture violations, testing gaps, code quality issues
- [X] **Impact**: LLMs get no specific patterns to look for beyond security

### 2. **Missing Core Principles in Focus-Specific Outputs**

- [X] **Problem**: Android/iOS architecture prompts show no principles, just empty sections
- [X] **Fix**: Ensure focused prompts still include relevant principles (unidirectional data flow, testing for architecture)
- [X] **Impact**: LLMs lose context about what to enforce

### 3. **Inconsistent Platform Naming**

- [X] **Problem**: iOS shows as "Ios" instead of "iOS" in headers
- [X] **Fix**: Standardize capitalization across all platform references
- [X] **Impact**: Minor but unprofessional appearance

### 4. **Dependency Check Command Issues**

- [X] **Problem**: Dependency checking doesn't actually validate against approved lists
- [X] **Fix**: Implement logic to check if dependency exists in approved platform dependencies
- [X] **Impact**: Feature doesn't work as advertised in demo

### 5. **Missing Accessibility Detection Patterns**

- [X] **Problem**: Accessibility rules show empty detection patterns
- [X] **Fix**: Add regex patterns for missing ARIA labels, contrast issues, semantic HTML
- [X] **Impact**: LLMs can't actually detect accessibility violations

## ✅ Moderate Issues

### 6. **Code Generation Prompts Too Verbose**

- [X] **Problem**: Generate command includes ALL 15 principles, making prompt extremely long
- [X] **Fix**: Filter to only include principles relevant to the component type (UI vs business logic)
- [X] **Impact**: Wastes token context, confuses focus

### 7. **Missing Context-Specific Instructions**

- [X] **Problem**: UI vs business-logic vs data-layer components get same generic guidance
- [X] **Fix**: Add component-specific detection rules and guidelines
- [X] **Impact**: Less targeted, actionable advice

### 8. **Vague Enforcement Instructions**

- [X] **Problem**: Some enforcement sections still too generic (e.g., "Compare implementation screenshots")
- [X] **Fix**: Add more specific tools and commands to run
- [X] **Impact**: LLMs need more concrete actions

## ✅ Minor Issues

### 9. **Philosophy Section Missing Values**

- [X] **Problem**: Code generation shows "Values:" with empty list
- [X] **Fix**: Either populate values or remove empty section
- [X] **Impact**: Looks unfinished

### 10. **Architecture Command Lacks Layer-Specific Guidance**

- [X] **Problem**: Data layer architecture prompt is generic for all layers
- [X] **Fix**: Add specific patterns and anti-patterns for data vs presentation vs business layers
- [X] **Impact**: Less useful architectural guidance

### 11. **Missing Performance and Code Style Detection Rules**

- [ ] **Problem**: No detection patterns for performance or code style issues
- [ ] **Fix**: Add patterns for performance bottlenecks, style violations
- [ ] **Impact**: Incomplete coverage of priority order

### 12. **Dependency Command Should Show Examples**

- [ ] **Problem**: Dependency evaluation doesn't show examples of good/bad dependencies
- [ ] **Fix**: Include examples of approved/rejected dependencies with reasoning
- [ ] **Impact**: Less educational for developers

## ✅ Priority Order for Fixes

### High Priority (Demo-Breaking Issues)

1. Empty Detection Rules for Non-Security Areas
2. Missing Core Principles in Focus Outputs
3. Dependency Check Logic
4. Platform Name Capitalization

### Medium Priority (User Experience)

5. Accessibility Detection Patterns
6. Verbose Code Generation Prompts
7. Context-Specific Instructions

### Low Priority (Polish)

8. Philosophy Values Section
9. Architecture Layer Guidance
10. Performance/Style Detection Rules
11. Dependency Examples

## ✅ Success Criteria

After fixes, the loom script should demonstrate:

- ✅ **Specific, actionable detection patterns** for all focus areas
- ✅ **Platform-appropriate principles** in every output
- ✅ **Working dependency validation** that actually checks approved lists
- ✅ **Consistent, professional formatting** across all platforms
- ✅ **Focused, relevant content** for each command type
- ✅ **Clear enforcement instructions** that LLMs can follow

## ✅ Testing Plan

For each fix:

1. Run the exact command from loom script
2. Verify output includes expected improvements
3. Test with multiple platforms/focus areas
4. Ensure backward compatibility with existing functionality
