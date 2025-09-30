#!/usr/bin/env python3
"""
LEAP MCP Server - Livefront Engineering Automated Principles

MCP server that exposes LEAP engineering principles, detection patterns,
enforcement specifications, and platform requirements for AI integration.
"""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.server.lowlevel.server import NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    TextContent,
    Tool,
)

from leap import LeapLoader
from leap.filters import (
    filter_detection_rules_by_platform,
    filter_principles_by_focus,
    get_component_type_principles,
    map_focus_areas_to_enforcement_stages,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("leap-mcp-server")

# Initialize LEAP loader
loader = LeapLoader()

# Create MCP server
server = Server("leap-engineering-principles")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available LEAP tools"""
    return [
        Tool(
            name="get_principles",
            description="Get engineering principles, optionally filtered by platform and focus",
            inputSchema={
                "type": "object",
                "properties": {
                    "platform": {
                        "type": "string",
                        "enum": ["android", "ios", "web"],
                        "description": "Platform to filter for (optional)",
                    },
                    "focus_areas": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Focus areas to filter principles (e.g., security)",
                    },
                },
                "additionalProperties": False,
            },
        ),
        Tool(
            name="get_detection_patterns",
            description="Get regex patterns for detecting violations of engineering principles",
            inputSchema={
                "type": "object",
                "properties": {
                    "principle": {
                        "type": "string",
                        "description": "Specific principle to get patterns for (e.g., security)",
                    },
                    "platform": {
                        "type": "string",
                        "enum": ["android", "ios", "web"],
                        "description": "Platform to filter patterns for (optional)",
                    },
                },
                "additionalProperties": False,
            },
        ),
        Tool(
            name="get_generation_guidance",
            description="Get guidance for writing new code following engineering principles",
            inputSchema={
                "type": "object",
                "properties": {
                    "platform": {
                        "type": "string",
                        "enum": ["android", "ios", "web"],
                        "description": "Platform to generate code for",
                    },
                    "component_type": {
                        "type": "string",
                        "enum": ["ui", "business-logic", "data-layer"],
                        "description": "Type of component being generated (optional)",
                    },
                },
                "required": ["platform"],
                "additionalProperties": False,
            },
        ),
        Tool(
            name="get_platform_requirements",
            description="Get platform-specific requirements, tools, and constraints",
            inputSchema={
                "type": "object",
                "properties": {
                    "platform": {
                        "type": "string",
                        "enum": ["android", "ios", "web"],
                        "description": "Platform to get requirements for",
                    },
                },
                "required": ["platform"],
                "additionalProperties": False,
            },
        ),
        Tool(
            name="get_enforcement_specs",
            description="Get CI implementation guidance showing what checks should be implemented",
            inputSchema={
                "type": "object",
                "properties": {
                    "focus_areas": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Focus areas to get enforcement specs for (optional)",
                    },
                },
                "additionalProperties": False,
            },
        ),
        Tool(
            name="validate_dependency",
            description="Check if a dependency is approved for a specific platform",
            inputSchema={
                "type": "object",
                "properties": {
                    "package": {
                        "type": "string",
                        "description": "Package/dependency name to validate",
                    },
                    "platform": {
                        "type": "string",
                        "enum": ["android", "ios", "web"],
                        "description": "Platform to validate dependency for",
                    },
                },
                "required": ["package", "platform"],
                "additionalProperties": False,
            },
        ),
        Tool(
            name="get_severity_guidance",
            description="Get guidance on how to classify violation severity levels",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
    """Handle tool calls"""
    if arguments is None:
        arguments = {}

    try:
        if name == "get_principles":
            return await get_principles_tool(arguments)
        elif name == "get_detection_patterns":
            return await get_detection_patterns_tool(arguments)
        elif name == "get_generation_guidance":
            return await get_generation_guidance_tool(arguments)
        elif name == "get_platform_requirements":
            return await get_platform_requirements_tool(arguments)
        elif name == "get_enforcement_specs":
            return await get_enforcement_specs_tool(arguments)
        elif name == "validate_dependency":
            return await validate_dependency_tool(arguments)
        elif name == "get_severity_guidance":
            return await get_severity_guidance_tool(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        logger.error(f"Error in tool {name}: {e}")
        raise ValueError(str(e)) from e


async def get_principles_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Get engineering principles"""
    platform = arguments.get("platform")
    focus_areas = arguments.get("focus_areas", [])

    principles = loader.load_principles()

    if focus_areas:
        principles = filter_principles_by_focus(principles, focus_areas)

    # Add platform context if specified
    result = {"principles": principles}
    if platform:
        result["platform"] = platform

    return [TextContent(type="text", text=str(result))]


async def get_detection_patterns_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Get detection patterns for engineering principles"""
    principle = arguments.get("principle")
    platform = arguments.get("platform")

    rules = loader.load_detection_rules(principle)

    if platform:
        rules = filter_detection_rules_by_platform(rules, platform)

    return [TextContent(type="text", text=str(rules))]


async def get_generation_guidance_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Get code generation guidance"""
    platform = arguments["platform"]
    component_type = arguments.get("component_type", "ui")

    # Get platform requirements
    platforms = loader.load_platforms()
    platform_config = platforms.get(platform, {})

    # Get component-specific principles
    component_principles = get_component_type_principles(component_type)

    # Get philosophy for cultural context
    philosophy = loader.load_philosophy()

    result = {
        "platform": platform,
        "component_type": component_type,
        "platform_requirements": platform_config,
        "component_principles": component_principles,
        "philosophy": philosophy,
    }

    return [TextContent(type="text", text=str(result))]


async def get_platform_requirements_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Get platform-specific requirements"""
    platform = arguments["platform"]

    platforms = loader.load_platforms()
    platform_config = platforms.get(platform, {})

    result = {"platform": platform, "requirements": platform_config}

    return [TextContent(type="text", text=str(result))]


async def get_enforcement_specs_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Get CI enforcement specifications"""
    focus_areas = arguments.get("focus_areas", [])

    enforcement = loader.load_enforcement()
    ci_pipeline = enforcement.get("enforcement_tools", {}).get("ci_pipeline", {})
    stages = ci_pipeline.get("stages", [])

    # Filter stages by focus areas if provided
    if focus_areas:
        relevant_stages = map_focus_areas_to_enforcement_stages(focus_areas)
        filtered_stages = [stage for stage in stages if stage.get("name", "") in relevant_stages]
    else:
        filtered_stages = stages

    result = {"focus_areas": focus_areas, "ci_stages": filtered_stages}

    return [TextContent(type="text", text=str(result))]


async def validate_dependency_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Validate if dependency is approved"""
    package = arguments["package"]
    platform = arguments["platform"]

    platforms = loader.load_platforms()
    platform_config = platforms.get(platform, {})
    approved_deps = platform_config.get("dependencies", {}).get("approved", [])

    is_approved = any(dep.get("name") == package for dep in approved_deps if isinstance(dep, dict))

    # Get alternatives if not approved
    alternatives = []
    if not is_approved:
        # Simple logic to suggest alternatives based on purpose
        all_approved = [
            dep.get("name") for dep in approved_deps if isinstance(dep, dict) and dep.get("name")
        ]
        alternatives = all_approved[:3]  # Show first 3 as examples

    result = {
        "package": package,
        "platform": platform,
        "approved": is_approved,
        "alternatives": alternatives,
        "approved_dependencies": approved_deps,
    }

    return [TextContent(type="text", text=str(result))]


async def get_severity_guidance_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Get severity classification guidance"""
    severity_levels = loader.load_severity_levels()

    result = {"severity_levels": severity_levels}

    return [TextContent(type="text", text=str(result))]


async def main() -> None:
    """Main server function"""
    # Initialize the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="leap-engineering-principles",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(), experimental_capabilities={}
                ),
            ),
        )


def main_cli() -> None:
    """CLI entry point for pipx installation."""
    asyncio.run(main())


if __name__ == "__main__":
    main_cli()
