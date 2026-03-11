"""
STDIO-to-HTTP proxy for Calendesk MCP.

Reads CALENDESK_API_KEY + CALENDESK_TENANT from env,
proxies all MCP tool calls to the Calendesk AI Gateway.
"""

import os
import sys
import json
import asyncio
from typing import Optional

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

GATEWAY_URL = os.getenv("CALENDESK_GATEWAY_URL", "https://mcp.calendesk.com").rstrip("/")

mcp = FastMCP("calendesk")


def _get_credentials() -> tuple[str, str]:
    api_key = os.getenv("CALENDESK_API_KEY", "")
    tenant = os.getenv("CALENDESK_TENANT", "")
    if not api_key or not tenant:
        print(
            "Error: CALENDESK_API_KEY and CALENDESK_TENANT environment variables are required.",
            file=sys.stderr,
        )
        sys.exit(1)
    return api_key, tenant


def _get_headers(api_key: str, tenant: str) -> dict[str, str]:
    return {
        "X-Api-Key": api_key,
        "X-Tenant": tenant,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


async def _discover_and_register_tools():
    """Fetch tools from gateway via MCP protocol and register locally."""
    api_key, tenant = _get_credentials()
    headers = _get_headers(api_key, tenant)

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Step 1: Initialize MCP session
        init_resp = await client.post(
            GATEWAY_URL,
            headers=headers,
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "calendesk-mcp-server", "version": "0.1.0"},
                },
            },
        )
        init_resp.raise_for_status()
        session_id = init_resp.headers.get("mcp-session-id")

        if session_id:
            headers["mcp-session-id"] = session_id

        # Step 2: Send initialized notification
        await client.post(
            GATEWAY_URL,
            headers=headers,
            json={"jsonrpc": "2.0", "method": "notifications/initialized"},
        )

        # Step 3: List tools
        list_resp = await client.post(
            GATEWAY_URL,
            headers=headers,
            json={"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        )
        list_resp.raise_for_status()
        result = list_resp.json()

    tools = result.get("result", {}).get("tools", [])
    for tool in tools:
        _register_proxy_tool(tool, session_id)

    print(f"Registered {len(tools)} tools from Calendesk", file=sys.stderr)


def _register_proxy_tool(tool_def: dict, session_id: Optional[str]):
    """Register a tool that proxies calls to the gateway."""
    name = tool_def["name"]
    description = tool_def.get("description", "")
    schema = tool_def.get("inputSchema", {})
    properties = schema.get("properties", {})

    type_map = {"integer": int, "boolean": bool, "number": float, "array": list, "object": dict}
    annotations = {p: type_map.get(s.get("type", "string"), str) for p, s in properties.items()}

    async def tool_handler(**kwargs) -> str:
        api_key, tenant = _get_credentials()
        hdrs = _get_headers(api_key, tenant)
        if session_id:
            hdrs["mcp-session-id"] = session_id

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                GATEWAY_URL,
                headers=hdrs,
                json={
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {"name": name, "arguments": kwargs},
                },
            )
            resp.raise_for_status()
            result = resp.json()

        content = result.get("result", {}).get("content", [])
        texts = [c.get("text", "") for c in content if c.get("type") == "text"]
        return "\n".join(texts) if texts else json.dumps(result)

    tool_handler.__name__ = name
    tool_handler.__doc__ = description
    tool_handler.__annotations__ = {**annotations, "return": str}
    mcp.tool(name=name, description=description)(tool_handler)


# Discover tools at import time
try:
    asyncio.run(_discover_and_register_tools())
except httpx.ConnectError:
    print(f"Error: Cannot connect to Calendesk gateway at {GATEWAY_URL}", file=sys.stderr)
    sys.exit(1)
except httpx.HTTPStatusError as e:
    print(f"Error: Gateway returned {e.response.status_code}. Check your CALENDESK_API_KEY and CALENDESK_TENANT.", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Error: Failed to initialize: {e}", file=sys.stderr)
    sys.exit(1)


def main():
    """Entry point for the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
