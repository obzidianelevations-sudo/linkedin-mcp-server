"""
Configuration loading for GHL MCP Server.

Loads settings from environment variables via python-dotenv.
"""

import os

from dotenv import load_dotenv

from .schema import AppConfig, ConfigurationError

# Load .env file if present
load_dotenv()


def load_config() -> AppConfig:
    """
    Load configuration from environment variables.

    Required:
        GHL_API_TOKEN   - GoHighLevel Private Integration Token (pit-...)
        GHL_LOCATION_ID - GHL Location / Sub-account ID

    Optional:
        GHL_BASE_URL    - Override API base URL (default: https://services.leadconnectorhq.com)
        GHL_LOG_LEVEL   - Logging level (default: WARNING)
    """
    config = AppConfig()

    # Required
    api_token = os.environ.get("GHL_API_TOKEN", "")
    location_id = os.environ.get("GHL_LOCATION_ID", "")

    config.api.api_token = api_token
    config.api.location_id = location_id

    # Optional overrides
    if base_url := os.environ.get("GHL_BASE_URL"):
        config.api.base_url = base_url

    if log_level := os.environ.get("GHL_LOG_LEVEL", "").upper():
        if log_level in ("DEBUG", "INFO", "WARNING", "ERROR"):
            config.server.log_level = log_level

    return config
