"""
HTTP client driver for GHL API.

Provides a singleton httpx.AsyncClient and ghl_request() helper that handles
authentication headers, versioning, and error mapping.
"""

import logging
from typing import Any, Dict, Optional

import httpx

from ghl_mcp_server.config import get_config
from ghl_mcp_server.exceptions import GHLApiError, GHLAuthenticationError, GHLRateLimitError

logger = logging.getLogger(__name__)

_client: Optional[httpx.AsyncClient] = None


def get_client() -> httpx.AsyncClient:
    """Get or create the singleton httpx AsyncClient."""
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(timeout=30.0)
        logger.debug("GHL HTTP client created")
    return _client


async def close_client() -> None:
    """Close the HTTP client."""
    global _client
    if _client and not _client.is_closed:
        await _client.aclose()
        _client = None
        logger.debug("GHL HTTP client closed")


async def ghl_request(
    method: str,
    path: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Make an authenticated request to the GHL API.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        path: API path (e.g., "/contacts/")
        params: Query parameters
        json: Request body for POST/PUT

    Returns:
        Parsed JSON response dict

    Raises:
        GHLAuthenticationError: On 401 response
        GHLRateLimitError: On 429 response
        GHLApiError: On other non-2xx responses
    """
    config = get_config()
    url = f"{config.api.base_url}{path}"
    headers = {
        "Authorization": f"Bearer {config.api.api_token}",
        "Version": config.api.api_version,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    client = get_client()
    logger.debug(f"GHL {method} {path} params={params}")

    response = await client.request(
        method=method,
        url=url,
        headers=headers,
        params=params,
        json=json,
    )

    if response.status_code == 401:
        raise GHLAuthenticationError(
            f"GHL API authentication failed (401). Check GHL_API_TOKEN."
        )

    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 60))
        raise GHLRateLimitError(retry_after=retry_after)

    if not response.is_success:
        try:
            body = response.json()
            msg = body.get("message", response.text)
        except Exception:
            msg = response.text
        raise GHLApiError(
            f"GHL API error {response.status_code}: {msg}",
            status_code=response.status_code,
        )

    # 204 No Content
    if response.status_code == 204 or not response.content:
        return {"status": "success"}

    return response.json()
