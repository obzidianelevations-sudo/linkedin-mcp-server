"""
GHL MCP Server — CLI entry point.

Loads config, validates API credentials, then runs the MCP server.
"""

import logging
import sys

from ghl_mcp_server.config import get_config
from ghl_mcp_server.config.schema import ConfigurationError
from ghl_mcp_server.server import create_mcp_server

logger = logging.getLogger(__name__)


def main() -> None:
    """Main entry point for the GHL MCP Server."""
    # Basic logging setup — defer to env/config for level
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    try:
        config = get_config()
    except ConfigurationError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)

    # Set log level from config
    logging.getLogger().setLevel(config.server.log_level)

    # Validate API credentials before starting
    try:
        config.validate()
    except ConfigurationError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        print(
            "Set GHL_API_TOKEN and GHL_LOCATION_ID in your .env file or environment.",
            file=sys.stderr,
        )
        sys.exit(1)

    logger.info("GHL MCP Server starting with stdio transport")

    mcp = create_mcp_server()
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
