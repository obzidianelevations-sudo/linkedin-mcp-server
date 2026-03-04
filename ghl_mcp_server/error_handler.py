"""
Centralized error handling for GHL MCP Server with structured responses.

Provides consistent MCP response format across all tools.
"""

import logging
from typing import Any, Dict

from ghl_mcp_server.exceptions import (
    GHLApiError,
    GHLAuthenticationError,
    GHLMCPError,
    GHLRateLimitError,
)

logger = logging.getLogger(__name__)


def handle_tool_error(exception: Exception, context: str = "") -> Dict[str, Any]:
    """
    Handle errors from GHL tool functions and return structured responses.

    Args:
        exception: The exception that occurred
        context: Context about which tool failed

    Returns:
        Structured error response dictionary
    """
    if isinstance(exception, GHLAuthenticationError):
        return {
            "error": "authentication_failed",
            "message": str(exception),
            "resolution": "Check GHL_API_TOKEN in your .env file. Generate a new Private Integration Token in GHL.",
        }

    elif isinstance(exception, GHLRateLimitError):
        return {
            "error": "rate_limit",
            "message": str(exception),
            "retry_after_seconds": exception.retry_after,
            "resolution": f"GHL API rate limit hit. Wait {exception.retry_after} seconds before retrying.",
        }

    elif isinstance(exception, GHLApiError):
        return {
            "error": "api_error",
            "message": str(exception),
            "status_code": exception.status_code,
            "resolution": "Check GHL API documentation or verify your location ID and permissions.",
        }

    elif isinstance(exception, GHLMCPError):
        return {
            "error": "ghl_mcp_error",
            "message": str(exception),
        }

    else:
        logger.error(
            f"Unexpected error in {context}: {exception}",
            extra={
                "context": context,
                "exception_type": type(exception).__name__,
                "exception_message": str(exception),
            },
        )
        return {
            "error": "unknown_error",
            "message": f"Failed to execute {context}: {str(exception)}",
        }
