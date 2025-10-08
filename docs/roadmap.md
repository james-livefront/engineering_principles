# Roadmap

## Completed Features

- [x] Code review prompt generation
- [x] Platform-specific standards (Android, iOS, Web)
- [x] Security and accessibility detection rules
- [x] Evaluation framework for measuring prompt effectiveness
- [x] CLI tool for generating targeted prompts
- [x] YAML detection rules integration (70%+ test coverage)
- [x] LLM enhancement mode
- [x] Streamlined prompt formatting (50% size reduction)
- [x] Multi-layered detection architecture (base + enhanced)
- [x] Documentation and examples
- [x] Evaluation metrics documentation (accuracy, precision, recall, F1 score)
- [x] MCP Server Integration - Real-time agent integration with Claude Desktop/Code
- [x] pipx Installation - Global commands (leap-mcp-server, leap-review, leap-eval)
- [x] Testing - 97% MCP server coverage (40/40 tests passing)
- [x] Setup - One-command installation via install.sh
- [x] Code Quality - De-AIification and duplication cleanup (15 improvements across 5 files)
- [x] Documentation - README, CLI Reference, Evaluation Metrics, Contributing Guide (2,335+ lines)
- [x] Detection Rules - Security, Accessibility, Testing, Architecture patterns with platform filtering

## TODO

### Missing Detection Rules Integration
- [ ] Dependencies - Enhanced approval workflow integration
- [ ] Performance - Bundle size, optimization opportunities

### Unused YAML Sections Integration

- [x] **`escalation_path`** - Integrated into severity guidance and review prompts
- [x] **`code_reviews`** - Code review principles integrated into review prompts
- [ ] **`preflight_checklist`** - Generate release readiness checklists and QA prompts
- [ ] **`cultural_expectations`** - Create onboarding and team culture prompts

### Code Quality & Maintenance

- [x] **De-AIification** - Removed AI marketing language from codebase
  - [x] Removed "comprehensive", "AI-powered", "sophisticated", "cutting-edge" buzzwords
  - [x] Simplified verbose docstrings with links to documentation
  - [x] Cleaned up 4 files: README.md, principles_cli.py, eval_runner.py, leap_mcp_server.py
- [x] **Duplication Cleanup** - Fixed contradictions and redundancy
  - [x] Removed duplicate Performance Metrics section in README
  - [x] Deduplicated evaluation metrics documentation
  - [x] Consolidated installation instructions

### Evaluation Improvements

- [x] Expand test cases for edge scenarios - 56 test cases across 5 files (security, accessibility, testing, architecture, generation)
- [x] Add regression tests for new principles - Detection and generation test suites in place
- [x] Improve evaluation metrics (precision/recall per severity) - See `docs/evaluation-metrics.md`
- [x] Multi-config comparison and auto-merge functionality - Parallel evaluation with statistical analysis
- [ ] Automated output comparison for generated prompts

### Test Suite Enhancements

#### MCP Server Testing (Completed)

- [x] MCP server API tests (40 test cases)
- [x] All 7 MCP tools tested (get_principles, get_detection_patterns, get_generation_guidance, get_platform_requirements, get_enforcement_specs, validate_dependency, get_severity_guidance)
- [x] Routing and tool registration tests
- [x] Mock-based testing for fast, reliable tests
- [x] 97% coverage on leap_mcp_server.py

#### Integration Testing

- [x] End-to-end prompt generation workflow tests - CLI commands tested and functional
- [x] Smart Context Detection metadata integration validation - PROMPT_METADATA in all prompts
- [x] Cross-platform prompt consistency verification - Platform filtering working correctly
- [x] YAML rule integration with CLI command testing - 56 test cases validating YAML rules

#### File I/O Testing

- [ ] Edge case handling for malformed YAML files
- [ ] Permission error scenarios and graceful degradation
- [ ] Large file handling and performance validation
- [ ] Directory traversal and file discovery testing

#### Platform Coverage Testing

- [x] All platform combinations (iOS/Android/Web) with all principle types - Complete coverage
- [x] Platform-specific rule application verification - Detection rules filter by platform
- [x] Cross-platform metadata inheritance testing - PROMPT_METADATA system working
- [x] Platform filtering accuracy in evaluation framework - Smart Context Detection implemented

## Future Enhancements

### Integration Opportunities

- [x] **MCP Server for AI Assistants** - Claude Desktop & Claude Code integration
- [ ] IDE assistants (VS Code extension)
- [ ] CI bot integration (GitHub Actions, Jenkins)
- [ ] Pre-commit hooks automation
- [ ] Slack/Teams notifications for violations


### Community & Extensibility

- [ ] Template for other organizations to adapt
- [ ] Plugin system for custom rules
- [ ] Rule pack marketplace/sharing
- [x] Documentation for contributing new principles - See CONTRIBUTING.md

### Advanced Features

- [ ] Machine learning for violation pattern detection
- [ ] Historical trend analysis
- [ ] Team compliance dashboards
- [ ] Automated severity escalation
