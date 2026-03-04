"""
GHL tasks tools.

Provides MCP tools for creating tasks on GHL contacts.
Used by Operator to queue human review actions.
"""

import logging
from typing import Any, Dict, Optional

from fastmcp import FastMCP
from mcp.types import ToolAnnotations

from ghl_mcp_server.drivers.http_client import ghl_request
from ghl_mcp_server.error_handler import handle_tool_error

logger = logging.getLogger(__name__)


def register_task_tools(mcp: FastMCP) -> None:
    """Register all task-related tools with the MCP server."""

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create GHL Task",
            readOnlyHint=False,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    async def ghl_create_task(
        contact_id: str,
        title: str,
        due_date: Optional[str] = None,
        description: str = "",
        assigned_to: str = "",
    ) -> Dict[str, Any]:
        """
        Create a task on a GHL contact.

        Used by Operator to create "Review & Send Outreach — [Name]" tasks
        for human review before sending drafted messages.

        Args:
            contact_id: GHL contact ID
            title: Task title (e.g., "Review & Send Outreach — Jane Smith")
            due_date: ISO 8601 due date string (e.g., "2026-03-04T17:00:00Z").
                      Defaults to end of current day if not provided.
            description: Optional task description / additional context
            assigned_to: Optional GHL user ID to assign the task to

        Returns:
            Created task record with id, title, dueDate, status, assignedTo
        """
        try:
            payload: Dict[str, Any] = {
                "title": title,
                "completed": False,
            }
            if due_date:
                payload["dueDate"] = due_date
            if description:
                payload["description"] = description
            if assigned_to:
                payload["assignedTo"] = assigned_to

            result = await ghl_request(
                "POST",
                f"/contacts/{contact_id}/tasks",
                json=payload,
            )
            return result

        except Exception as e:
            return handle_tool_error(e, "ghl_create_task")
