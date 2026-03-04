"""
GHL contact tools.

Provides MCP tools for searching, reading, and updating GHL contacts,
including tag management for the Operator agent's state machine.
"""

import logging
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP
from mcp.types import ToolAnnotations

from ghl_mcp_server.config import get_config
from ghl_mcp_server.drivers.http_client import ghl_request
from ghl_mcp_server.error_handler import handle_tool_error

logger = logging.getLogger(__name__)


def register_contact_tools(mcp: FastMCP) -> None:
    """Register all contact-related tools with the MCP server."""

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Search GHL Contacts",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    async def ghl_search_contacts(
        query: Optional[str] = None,
        tag: Optional[str] = None,
        limit: int = 20,
        skip: int = 0,
    ) -> Dict[str, Any]:
        """
        Search contacts in GoHighLevel CRM.

        Args:
            query: Text search across name, email, phone, company
            tag: Filter by tag (e.g., "new-lead", "operator-processed")
            limit: Max contacts to return (default: 20, max: 100)
            skip: Offset for pagination (default: 0)

        Returns:
            Dict with 'contacts' list and 'total' count. Each contact includes:
            id, name, email, phone, company, tags, customFields, dateAdded
        """
        try:
            config = get_config()
            params: Dict[str, Any] = {
                "locationId": config.api.location_id,
                "limit": min(limit, 100),
                "skip": skip,
            }
            if query:
                params["query"] = query
            if tag:
                params["tags"] = tag

            result = await ghl_request("GET", "/contacts/", params=params)
            return result

        except Exception as e:
            return handle_tool_error(e, "ghl_search_contacts")

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get GHL Contact",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    async def ghl_get_contact(contact_id: str) -> Dict[str, Any]:
        """
        Get full details for a specific GHL contact.

        Args:
            contact_id: GHL contact ID

        Returns:
            Full contact record including id, name, email, phone, company,
            tags, customFields, source, dateAdded, assignedTo
        """
        try:
            result = await ghl_request("GET", f"/contacts/{contact_id}")
            return result

        except Exception as e:
            return handle_tool_error(e, "ghl_get_contact")

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update GHL Contact",
            readOnlyHint=False,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    async def ghl_update_contact(
        contact_id: str,
        fields: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Update fields on a GHL contact.

        Args:
            contact_id: GHL contact ID
            fields: Dict of fields to update, e.g.:
                {"firstName": "Jane", "email": "jane@co.com",
                 "customFields": [{"id": "field_id", "value": "val"}]}

        Returns:
            Updated contact record
        """
        try:
            result = await ghl_request("PUT", f"/contacts/{contact_id}", json=fields)
            return result

        except Exception as e:
            return handle_tool_error(e, "ghl_update_contact")

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Add Tag to GHL Contact",
            readOnlyHint=False,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    async def ghl_add_tag(contact_id: str, tag: str) -> Dict[str, Any]:
        """
        Add a tag to a GHL contact (read-modify-write to preserve existing tags).

        Args:
            contact_id: GHL contact ID
            tag: Tag to add (e.g., "operator-processed")

        Returns:
            Updated contact record showing new tags list
        """
        try:
            # Read existing tags first
            contact = await ghl_request("GET", f"/contacts/{contact_id}")
            contact_data = contact.get("contact", contact)
            existing_tags: List[str] = contact_data.get("tags", [])

            if tag not in existing_tags:
                new_tags = existing_tags + [tag]
                result = await ghl_request(
                    "PUT",
                    f"/contacts/{contact_id}",
                    json={"tags": new_tags},
                )
                return result
            else:
                return {"status": "already_tagged", "contact": contact_data}

        except Exception as e:
            return handle_tool_error(e, "ghl_add_tag")

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Remove Tag from GHL Contact",
            readOnlyHint=False,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    async def ghl_remove_tag(contact_id: str, tag: str) -> Dict[str, Any]:
        """
        Remove a tag from a GHL contact (read-modify-write to preserve other tags).

        Args:
            contact_id: GHL contact ID
            tag: Tag to remove (e.g., "new-lead")

        Returns:
            Updated contact record showing new tags list
        """
        try:
            # Read existing tags first
            contact = await ghl_request("GET", f"/contacts/{contact_id}")
            contact_data = contact.get("contact", contact)
            existing_tags: List[str] = contact_data.get("tags", [])

            new_tags = [t for t in existing_tags if t != tag]
            result = await ghl_request(
                "PUT",
                f"/contacts/{contact_id}",
                json={"tags": new_tags},
            )
            return result

        except Exception as e:
            return handle_tool_error(e, "ghl_remove_tag")
