"""
Custom exceptions for GHL MCP Server.

Defines hierarchical exception types for GHL API error scenarios.
"""


class GHLMCPError(Exception):
    """Base exception for GHL MCP Server."""


class GHLAuthenticationError(GHLMCPError):
    """API token is invalid or missing (HTTP 401)."""


class GHLRateLimitError(GHLMCPError):
    """GHL API rate limit exceeded (HTTP 429)."""

    def __init__(self, message: str = "GHL API rate limit exceeded.", retry_after: int = 60):
        self.retry_after = retry_after
        super().__init__(message)


class GHLApiError(GHLMCPError):
    """General GHL API error (non-2xx response)."""

    def __init__(self, message: str, status_code: int = 0):
        self.status_code = status_code
        super().__init__(message)
