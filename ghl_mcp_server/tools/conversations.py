"""
GHL conversation tools.

Provides MCP tools for searching conversations, reading messages,
and sending emails via GHL.
"""

import logging
from typing import Any, Dict, Optional

from fastmcp import FastMCP
from mcp.types import ToolAnnotations

from ghl_mcp_server.config import get_config
from ghl_mcp_server.drivers.http_client import ghl_request
from ghl_mcp_server.error_handler import handle_tool_error

logger = logging.getLogger(__name__)


def register_conversation_tools(mcp: FastMCP) -> None:
    """Register all conversation-related tools with the MCP server."""

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Search GHL Conversations",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    async def ghl_search_conversations(
        contact_id: Optional[str] = None,
        query: Optional[str] = None,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """
        Search conversations in GHL.

        Used by Operator to find conversations for contacts tagged "outreach-sent"
        to check for positive replies.

        Args:
            contact_id: Filter conversations by contact ID
            query: Text search within conversations
            limit: Max conversations to return (default: 20)

        Returns:
            Dict with 'conversations' list. Each entry includes:
            id, contactId, lastMessage, lastMessageDate, unreadCount, type
        """
        try:
            config = get_config()
            params: Dict[str, Any] = {
                "locationId": config.api.location_id,
                "limit": min(limit, 100),
            }
            if contact_id:
                params["contactId"] = contact_id
            if query:
                params["query"] = query

            result = await ghl_request("GET", "/conversations/search", params=params)
            return result

        except Exception as e:
            return handle_tool_error(e, "ghl_search_conversations")

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get GHL Messages",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    async def ghl_get_messages(
        conversation_id: str,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """
        Get messages from a GHL conversation.

        Used by Operator to read inbound replies from leads and determine
        if they are positive (warrant calendar booking response).

        Args:
            conversation_id: GHL conversation ID
            limit: Max messages to return (default: 20)

        Returns:
            Dict with 'messages' list. Each message includes:
            id, type, direction (inbound/outbound), body, dateAdded, status
        """
        try:
            params: Dict[str, Any] = {"limit": min(limit, 100)}
            result = await ghl_request(
                "GET",
                f"/conversations/{conversation_id}/messages",
                params=params,
            )
            return result

        except Exception as e:
            return handle_tool_error(e, "ghl_get_messages")

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Send GHL Email",
            readOnlyHint=False,
            destructiveHint=False,
            openWorldHint=True,
        )
    )
    async def ghl_send_email(
        contact_id: str,
        subject: str,
        html_body: str,
        from_name: str = "",
        from_email: str = "",
    ) -> Dict[str, Any]:
        """
        Send an email via GHL conversations API.

        Note: Staged for future use. Operator currently drafts messages as Notes
        for human review — this tool is available when human approves send.

        Args:
            contact_id: GHL contact ID (recipient)
            subject: Email subject line
            html_body: Email body in HTML format
            from_name: Sender display name (uses GHL default if empty)
            from_email: Sender email address (uses GHL default if empty)

        Returns:
            Sent message record with id, status, dateAdded
        """
        try:
            config = get_config()
            payload: Dict[str, Any] = {
                "type": "Email",
                "contactId": contact_id,
                "locationId": config.api.location_id,
                "subject": subject,
                "html": html_body,
            }
            if from_name:
                payload["fromName"] = from_name
            if from_email:
                payload["fromEmail"] = from_email

            result = await ghl_request("POST", "/conversations/messages", json=payload)
            return result

        except Exception as e:
            return handle_tool_error(e, "ghl_send_email")
