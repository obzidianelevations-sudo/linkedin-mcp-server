# LinkedIn MCP Server: Quick Start Guide

## What is this?
A server that lets AI assistants interact with LinkedIn to fetch profiles, companies, jobs, and network data through the Model Context Protocol (MCP).

## Prerequisites
- **Python 3.12+** installed
- **[uv](https://docs.astral.sh/uv/)** package manager: `curl -LsSf https://astral.sh/uv/install.sh | sh`

---

## 🚀 Getting Started (5 minutes)

### 1. **Install Dependencies**
```bash
cd linkedin-mcp-server
uv sync
uv run patchright install chromium
```

### 2. **Authenticate with LinkedIn** (Required first time)
```bash
uv run -m linkedin_mcp_server --get-session --no-headless
```
- Browser window opens → Log into LinkedIn manually
- Session saves to `~/.linkedin-mcp/profile/`
- Your credentials stay local (never sent to the server)

### 3. **Start the Server**
```bash
uv run -m linkedin_mcp_server
```

### 4. **Connect Your AI Assistant**
Add to your MCP client config (e.g., Claude Desktop):
```json
{
  "mcpServers": {
    "linkedin": {
      "command": "uv",
      "args": ["run", "-m", "linkedin_mcp_server"],
      "cwd": "/path/to/linkedin-mcp-server"
    }
  }
}
```

---

## 📋 Best Practices

### Development Workflow
1. **Always run quality checks before committing:**
   ```bash
   uv run ruff check . --fix    # Lint & auto-fix
   uv run ruff format .         # Format code
   uv run pytest --cov          # Run tests
   ```

2. **Use conventional commits:**
   ```
   feat(tools): add job search filtering
   fix(auth): handle expired sessions
   docs: update setup instructions
   ```

3. **Install pre-commit hooks:**
   ```bash
   uv run pre-commit install
   ```

### Production Usage
- **Run in Docker** for isolation:
  ```bash
  docker run -it --rm \
    -v ~/.linkedin-mcp:/home/pwuser/.linkedin-mcp \
    stickerdaniel/linkedin-mcp-server:latest
  ```

- **Handle rate limits:** Server auto-detects LinkedIn throttling
- **Refresh auth regularly:** Re-run `--get-session` if you get auth errors

### Troubleshooting
| Issue | Solution |
|-------|----------|
| Auth errors | Delete `~/.linkedin-mcp/profile/` and re-authenticate |
| Browser not found | Run `uv run patchright install chromium` |
| Rate limited | Wait 15-30 minutes before retrying |

---

## 🛠️ Available Tools
Once connected, your AI can use tools for:
- **Profiles** - Search and retrieve LinkedIn user data
- **Companies** - Get company details and insights
- **Jobs** - Search and analyze job postings
- **Network** - Access connections and relationships

---

## 📚 Next Steps
- Read `CLAUDE.md` for architecture details
- Check `tests/` for usage examples
- Open issues on GitHub for questions
