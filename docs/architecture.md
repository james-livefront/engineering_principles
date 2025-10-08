# System Architecture

This document provides architectural diagrams for the engineering principles tooling.

## CLI Tool Architecture

```mermaid
graph TB
    subgraph "CLI Tool Architecture"
        CLI[principles_cli.py<br/>Main Entry Point]

        subgraph "Core Components"
            Loader[PrinciplesLoader<br/>YAML/JSON Loading]
            Filter[PrinciplesFilter<br/>Query & Filtering]
            Formatter[Output Formatting<br/>Table/JSON/YAML]
        end

        subgraph "Data Sources"
            Android[android.yaml<br/>Android Principles]
            iOS[ios.yaml<br/>iOS Principles]
            Web[web.yaml<br/>Web Principles]
            Patterns[detection_patterns.yaml<br/>Regex Patterns]
            Guidance[generation_guidance.yaml<br/>Code Generation]
        end

        subgraph "Commands"
            List[list<br/>Show Principles]
            Detect[detect<br/>Find Violations]
            Generate[generate<br/>Code Guidance]
            Validate[validate<br/>Check Dependencies]
        end

        CLI --> Loader
        CLI --> Filter
        CLI --> Formatter

        Loader --> Android
        Loader --> iOS
        Loader --> Web
        Loader --> Patterns
        Loader --> Guidance

        Filter --> List
        Filter --> Detect
        Filter --> Generate
        Filter --> Validate

        List --> Formatter
        Detect --> Formatter
        Generate --> Formatter
        Validate --> Formatter
    end

    style CLI fill:#4a90e2,stroke:#2c5aa0,color:#fff
    style Loader fill:#50c878,stroke:#2d8659,color:#fff
    style Filter fill:#50c878,stroke:#2d8659,color:#fff
    style Formatter fill:#50c878,stroke:#2d8659,color:#fff
```

## MCP Server Architecture

```mermaid
graph TB
    subgraph "MCP Server Architecture"
        Server[leap_mcp_server.py<br/>FastMCP Server]

        subgraph "MCP Tools"
            GetPrinciples[get_principles<br/>Filter & Return Principles]
            GetPatterns[get_detection_patterns<br/>Regex Violations]
            GetGuidance[get_generation_guidance<br/>Code Generation Help]
            GetRequirements[get_platform_requirements<br/>Platform Specs]
            GetEnforcement[get_enforcement_specs<br/>CI Implementation]
            ValidateDep[validate_dependency<br/>Package Approval]
            GetSeverity[get_severity_guidance<br/>Severity Classification]
        end

        subgraph "Backend Components"
            Loader2[PrinciplesLoader<br/>YAML Loading]
            Filter2[PrinciplesFilter<br/>Query Logic]
        end

        subgraph "Data Files"
            Android2[android.yaml]
            iOS2[ios.yaml]
            Web2[web.yaml]
            Patterns2[detection_patterns.yaml]
            Guidance2[generation_guidance.yaml]
        end

        subgraph "MCP Clients"
            Claude[Claude Desktop/Code]
            Other[Other MCP Clients]
        end

        Claude --> Server
        Other --> Server

        Server --> GetPrinciples
        Server --> GetPatterns
        Server --> GetGuidance
        Server --> GetRequirements
        Server --> GetEnforcement
        Server --> ValidateDep
        Server --> GetSeverity

        GetPrinciples --> Loader2
        GetPatterns --> Loader2
        GetGuidance --> Loader2
        GetRequirements --> Loader2
        GetEnforcement --> Loader2
        ValidateDep --> Loader2

        Loader2 --> Filter2

        Loader2 --> Android2
        Loader2 --> iOS2
        Loader2 --> Web2
        Loader2 --> Patterns2
        Loader2 --> Guidance2
    end

    style Server fill:#e74c3c,stroke:#c0392b,color:#fff
    style GetPrinciples fill:#9b59b6,stroke:#8e44ad,color:#fff
    style GetPatterns fill:#9b59b6,stroke:#8e44ad,color:#fff
    style GetGuidance fill:#9b59b6,stroke:#8e44ad,color:#fff
    style GetRequirements fill:#9b59b6,stroke:#8e44ad,color:#fff
    style GetEnforcement fill:#9b59b6,stroke:#8e44ad,color:#fff
    style ValidateDep fill:#9b59b6,stroke:#8e44ad,color:#fff
    style GetSeverity fill:#9b59b6,stroke:#8e44ad,color:#fff
    style Loader2 fill:#3498db,stroke:#2980b9,color:#fff
    style Filter2 fill:#3498db,stroke:#2980b9,color:#fff
```

## Component Descriptions

### CLI Tool Components

- **PrinciplesLoader**: Loads and parses YAML/JSON principle files
- **PrinciplesFilter**: Provides query and filtering capabilities for principles
- **Output Formatting**: Formats results as tables, JSON, or YAML

### MCP Server Tools

- **get_principles**: Returns filtered engineering principles by platform/focus
- **get_detection_patterns**: Provides regex patterns for detecting violations
- **get_generation_guidance**: Returns guidance for writing compliant code
- **get_platform_requirements**: Returns platform-specific requirements and constraints
- **get_enforcement_specs**: Provides CI implementation guidance
- **validate_dependency**: Checks if a dependency is approved for a platform
- **get_severity_guidance**: Returns severity classification guidance

### Data Sources

All tools share the same YAML-based principle definitions:
- `android.yaml`: Android platform principles
- `ios.yaml`: iOS platform principles
- `web.yaml`: Web platform principles
- `detection_patterns.yaml`: Regex patterns for violation detection
- `generation_guidance.yaml`: Code generation guidance and templates
