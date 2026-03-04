"""
GHL notes tools.

Provides MCP tools for creating notes on GHL contacts.
Used by Operator to stage drafted outreach messages for human review.
"""

import logging
from typing import Any, Dict

from fastmcp import FastMCP
from mcp.types import ToolAnnotations

from ghl_mcp_server.drivers.http_client import ghl_request
from ghl_mcp_server.error_handler import handle_tool_error

logger = logging.getLogger(__name__)


def register_note_tools(mcp: FastMCP) -> None:
    """Register all note-related tools with the MCP server."""

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create GHL Note",
            readOnlyHint=False,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    async def ghl_create_note(
        contact_id: str,
        body: str,
        user_id: str = "",
    ) -> Dict[str, Any]:
        """
        Create a note on a GHL contact.

        Used by Operator to stage all 4 drafted outreach messages plus
        research summary for human review before sending.

        Args:
            contact_id: GHL contact ID
            body: Note body — supports markdown formatting.
                  Operator uses this to include research summary + all 4 messages.
            user_id: Optional GHL user ID to assign the note to

        Returns:
            Created note record with id, body, dateAdded, userId
        """
        try:
            payload: Dict[str, Any] = {"body": body}
            if user_id:
                payload["userId"] = user_id

            result = await ghl_request(
                "POST",
                f"/contacts/{contact_id}/notes",
                json=payload,
            )
            return result

        except Exception as e:
            return handle_tool_error(e, "ghl_create_note")
