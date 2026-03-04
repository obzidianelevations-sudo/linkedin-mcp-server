"""
FastMCP server implementation for GHL integration.

Creates and configures the MCP server with all GHL tool registrations.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastmcp import FastMCP

from ghl_mcp_server.drivers.http_client import close_client
from ghl_mcp_server.tools.contacts import register_contact_tools
from ghl_mcp_server.tools.conversations import register_conversation_tools
from ghl_mcp_server.tools.notes import register_note_tools
from ghl_mcp_server.tools.tasks import register_task_tools

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastMCP) -> AsyncIterator[None]:
    """Manage server lifecycle — close HTTP client on shutdown."""
    logger.info("GHL MCP Server starting...")
    yield
    logger.info("GHL MCP Server shutting down...")
    await close_client()


def create_mcp_server() -> FastMCP:
    """Create and configure the MCP server with all GHL tools."""
    mcp = FastMCP("ghl_mcp_server", lifespan=lifespan)

    register_contact_tools(mcp)
    register_note_tools(mcp)
    register_task_tools(mcp)
    register_conversation_tools(mcp)

    return mcp
