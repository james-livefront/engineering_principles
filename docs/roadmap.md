# Roadmap

## Completed Features

- [x] AI-powered code review prompt generation
- [x] Platform-specific standards (Android, iOS, Web)
- [x] Security and accessibility detection rules
- [x] Evaluation framework for measuring prompt effectiveness
- [x] CLI tool for generating targeted prompts
- [x] YAML detection rules integration (70%+ test coverage)
- [x] LLM enhancement mode for cutting-edge intelligence
- [x] Streamlined prompt formatting (50% size reduction)
- [x] Multi-layered detection architecture (base + enhanced)
- [x] Comprehensive documentation and examples
- [x] Evaluation metrics documentation (accuracy, precision, recall, F1 score)

## TODO

### Missing Detection Rules Integration

- [x] **Security** - Comprehensive patterns with platform filtering
- [x] **Accessibility** - WCAG patterns, ARIA, semantic HTML
- [x] **Testing** - Coverage requirements, test quality, flaky patterns
- [x] **Architecture** - Data flow violations, coupling detection
- [ ] **Documentation** - Missing README sections, API docs, inline comments
- [ ] **Dependencies** - Enhanced approval workflow integration
- [ ] **Performance** - Bundle size, optimization opportunities

### Unused YAML Sections Integration (NEW)

- [ ] **`preflight_checklist`** - Generate release readiness checklists and QA prompts
- [ ] **`escalation_path`** - Integrate severity guidance into review prompts
- [ ] **`cultural_expectations`** - Create onboarding and team culture prompts
- [ ] **`code_reviews`** - Generate prompts for conducting effective code reviews

### Evaluation Improvements

- [ ] Expand test cases for edge scenarios
- [ ] Add regression tests for new principles
- [x] Improve evaluation metrics (precision/recall per severity) - See `docs/evaluation-metrics.md`
- [x] Multi-config comparison and auto-merge functionality - Parallel evaluation with statistical analysis
- [ ] Automated output comparison for generated prompts

### Test Suite Enhancements

#### Integration Testing

- [ ] End-to-end prompt generation workflow tests
- [ ] Smart Context Detection metadata integration validation
- [ ] Cross-platform prompt consistency verification
- [ ] YAML rule integration with CLI command testing

#### File I/O Testing

- [ ] Edge case handling for malformed YAML files
- [ ] Permission error scenarios and graceful degradation
- [ ] Large file handling and performance validation
- [ ] Directory traversal and file discovery testing

#### Platform Coverage Testing

- [ ] All platform combinations (iOS/Android/Web) with all principle types
- [ ] Platform-specific rule application verification
- [ ] Cross-platform metadata inheritance testing
- [ ] Platform filtering accuracy in evaluation framework

## Future Enhancements

### Integration Opportunities

- [ ] IDE assistants (VS Code extension)
- [ ] CI bot integration (GitHub Actions, Jenkins)
- [ ] Pre-commit hooks automation
- [ ] Slack/Teams notifications for violations

### Community & Extensibility

- [ ] Template for other organizations to adapt
- [ ] Plugin system for custom rules
- [ ] Rule pack marketplace/sharing
- [ ] Documentation for contributing new principles

### Advanced Features

- [ ] Machine learning for violation pattern detection
- [ ] Historical trend analysis
- [ ] Team compliance dashboards
- [ ] Automated severity escalation
