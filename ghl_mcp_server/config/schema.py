"""
Configuration schema definitions for GHL MCP Server.

Defines the dataclass schemas for GHL API configuration.
"""

from dataclasses import dataclass, field


class ConfigurationError(Exception):
    """Raised when configuration validation fails."""


@dataclass
class GHLApiConfig:
    """GoHighLevel API configuration."""

    base_url: str = "https://services.leadconnectorhq.com"
    api_token: str = ""
    api_version: str = "2021-07-28"
    location_id: str = ""

    def validate(self) -> None:
        """Validate API configuration."""
        if not self.api_token:
            raise ConfigurationError(
                "GHL_API_TOKEN is required. Set it in your .env file or environment."
            )
        if not self.location_id:
            raise ConfigurationError(
                "GHL_LOCATION_ID is required. Set it in your .env file or environment."
            )


@dataclass
class ServerConfig:
    """MCP server configuration."""

    transport: str = "stdio"
    host: str = "127.0.0.1"
    port: int = 8000
    path: str = "/mcp"
    log_level: str = "WARNING"


@dataclass
class AppConfig:
    """Main application configuration."""

    api: GHLApiConfig = field(default_factory=GHLApiConfig)
    server: ServerConfig = field(default_factory=ServerConfig)

    def validate(self) -> None:
        """Validate all configuration values."""
        self.api.validate()
