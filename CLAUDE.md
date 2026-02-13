# LinkedIn MCP Server

A Model Context Protocol (MCP) server that enables AI assistants to interact with LinkedIn through web scraping.

## Quick Start

### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd linkedin-mcp-server
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Install the browser:**
   ```bash
   uv run patchright install chromium
   ```

4. **Authenticate with LinkedIn:**

   Run the server with `--get-session` to authenticate:
   ```bash
   uv run -m linkedin_mcp_server --get-session --no-headless
   ```

   This will:
   - Open a browser window
   - Navigate to LinkedIn login
   - Save your authenticated session to `~/.linkedin-mcp/profile/`

   **Note:** Your credentials are stored locally in the browser profile. The server never has direct access to your password.

5. **Run the server:**
   ```bash
   uv run -m linkedin_mcp_server
   ```

### Running with Docker

```bash
docker run -it --rm \
  -v ~/.linkedin-mcp:/home/pwuser/.linkedin-mcp \
  stickerdaniel/linkedin-mcp-server:latest
```

To get a session in Docker, first authenticate locally:
```bash
uvx linkedin-scraper-mcp --get-session
```

## Configuration

The server supports the following command-line options:

- `--no-headless` - Run browser in visible mode (useful for debugging)
- `--get-session` - Authenticate and save LinkedIn session
- `--transport stdio|streamable-http` - Choose transport mode (default: stdio)
- `--port PORT` - Port for HTTP transport (default: 8000)

Environment variables can also be used:
- `LINKEDIN_MCP_HEADLESS=false`
- `LINKEDIN_MCP_TRANSPORT=streamable-http`
- `LINKEDIN_MCP_PORT=8080`

## Available Tools

Once connected, the MCP server provides tools for:

- **Person profiles** - Search and retrieve LinkedIn profile data
- **Company information** - Get company details and insights
- **Job listings** - Search and analyze job postings
- **Network data** - Access connections and relationships

## Development

### Setup Development Environment

```bash
# Install all dependencies including dev tools
uv sync --group dev

# Install pre-commit hooks
uv run pre-commit install
```

### Code Quality

- **Lint:** `uv run ruff check .` (auto-fix with `--fix`)
- **Format:** `uv run ruff format .`
- **Type check:** `uv run ty check`
- **Tests:** `uv run pytest` (with coverage: `uv run pytest --cov`)

### Testing

```bash
# Run all tests
uv run pytest

# Run specific test
uv run pytest tests/test_file.py::test_name

# Run with coverage
uv run pytest --cov
```

Tests use `pytest` with async support and automatic browser/config reset between tests.

### Making Changes

1. Create a feature branch from `main`
2. Make your changes
3. Run tests and code quality checks
4. Commit with conventional commit messages: `type(scope): subject`
   - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
5. Push and create a pull request

## Architecture

### Two-Phase Startup

1. **Authentication Phase** - Validates LinkedIn browser profile exists
2. **Server Runtime Phase** - Creates FastMCP server and registers tools

### Key Components

- **Browser Manager** (`drivers/browser.py`) - Singleton browser instance shared across tools
- **Config Manager** (`config/`) - Configuration from CLI args, env vars, or defaults
- **Tool Registration** (`tools/`) - Modular tool registration pattern
- **Error Handling** (`error_handler.py`) - Maps exceptions to user-friendly responses
- **Progress Callbacks** (`callbacks.py`) - Bridges scraper progress to MCP progress reporting

### Key Dependencies

- `fastmcp` - MCP server framework
- `linkedin-scraper-patchright` - LinkedIn web scraping library
- `patchright` - Anti-detection browser automation (Playwright fork)

## Troubleshooting

### Browser Authentication Issues

If you see authentication errors:
1. Delete the profile directory: `rm -rf ~/.linkedin-mcp/profile/`
2. Re-authenticate: `uv run -m linkedin_mcp_server --get-session --no-headless`
3. Log in manually in the browser window that opens

### Rate Limiting

LinkedIn may rate-limit requests. The server includes automatic rate limit detection and will pause requests when limits are hit.

### Browser Not Found

If the browser isn't found, reinstall it:
```bash
uv run patchright install chromium
```

## Project Structure

```
linkedin-mcp-server/
├── src/linkedin_mcp_server/
│   ├── cli_main.py          # Entry point
│   ├── server.py            # FastMCP server setup
│   ├── authentication.py    # LinkedIn auth flow
│   ├── config/              # Configuration management
│   ├── drivers/             # Browser automation
│   ├── tools/               # MCP tool implementations
│   └── utils/               # Error handling, callbacks
├── tests/                   # Test suite
├── pyproject.toml           # Project configuration
└── README.md                # Project documentation
```

## Support

For issues, questions, or contributions, please open an issue in the repository.

## License

See LICENSE file for details.
