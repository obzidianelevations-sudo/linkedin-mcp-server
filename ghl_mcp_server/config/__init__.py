"""
Configuration system for GHL MCP Server.

Provides a singleton pattern for configuration management.
"""

import logging

from .loaders import load_config
from .schema import AppConfig, ConfigurationError, GHLApiConfig, ServerConfig

logger = logging.getLogger(__name__)

_config: AppConfig | None = None


def get_config() -> AppConfig:
    """Get the application configuration, initializing it if needed."""
    global _config
    if _config is None:
        _config = load_config()
        logger.debug("GHL configuration loaded")
    return _config


def reset_config() -> None:
    """Reset the configuration to force reloading."""
    global _config
    _config = None
    logger.debug("GHL configuration reset")


__all__ = [
    "AppConfig",
    "GHLApiConfig",
    "ServerConfig",
    "ConfigurationError",
    "get_config",
    "reset_config",
]
