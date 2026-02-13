# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- CHANGELOG.md following Keep a Changelog v1.1.0 format with version history
- HANDOFF.md for session handoff tracking and context preservation between sessions
- Session management section in CLAUDE.md with instructions to update documentation
- QUICK_START.md - Beginner-friendly one-page guide for getting started
- `.mcp.json` - MCP server configuration for Claude Code CLI integration
- `test_linkedin_search.py` - Standalone test script for manual LinkedIn search testing
- `.DS_Store` added to `.gitignore` for macOS compatibility

### Changed
- CLAUDE.md converted from symlink to regular file with enhanced documentation structure
- Development workflow now requires updating HANDOFF.md and CHANGELOG.md at end of each session

### Removed
- AGENTS.md (was symlink target, content now in CLAUDE.md)

## [3.0.3] - 2026-02-13

### Added
- Cookie bridge for cross-platform Docker portability

## [3.0.2] - 2026-02-13

### Changed
- **BREAKING**: Switched to `linkedin-scraper-patchright` from PyPI (#148)
- Dependency now available through official PyPI package instead of git repository

## [3.0.1] - 2026-02-13

### Fixed
- Person scraper bug fix (#145)
- Improved profile scraping reliability

## [3.0.0] - 2026-02-13

### Changed
- **BREAKING**: Switched from Playwright to Patchright with persistent browser context (#143)
- Browser profiles now stored at `~/.linkedin-mcp/profile/` instead of session files
- Old `session.json` files and `LINKEDIN_COOKIE` environment variables no longer supported
- Users must run `--get-session` again to create new browser profile

### Removed
- Support for `session.json` authentication files
- Support for `LINKEDIN_COOKIE` environment variable

## [2.3.7] - 2026-02-12

### Fixed
- Docker: Install git for git-based dependency resolution (#140)

## [2.3.6] - 2026-02-12

### Fixed
- Use linkedin_scraper fork with rate limit fix (#139)

## [2.3.5] - 2026-02-01

### Fixed
- Add `linkedin-scraper-mcp` CLI alias for cleaner uvx usage

## [2.3.4] - 2026-02-01

### Fixed
- Regenerate uv.lock for new package name

## [2.3.3] - 2026-02-01

### Added
- Automated PyPI publishing with Trusted Publishing (#133)
- CI workflow improvements for release automation

### Changed
- Reduce Renovate PR noise with aggressive grouping

## [2.3.2] - 2026-01-27

### Fixed
- Docker: Remove non-existent /opt/python from chmod (#127)

## [2.3.1] - 2026-01-27

### Fixed
- Update linkedin-scraper to 3.1.1 to fix --get-session hang (#125)

## [2.3.0] - 2026-01-27

### Added
- Initial MCP server implementation
- Profile scraping (`get_person_profile`)
- Company scraping (`get_company_profile`)
- Company posts (`get_company_posts`)
- Job search (`search_jobs`)
- Job details (`get_job_details`)
- Session management (`close_session`)

## [2.0.0] - 2026-01-XX

### Added
- Major version release with stable API

[Unreleased]: https://github.com/stickerdaniel/linkedin-mcp-server/compare/v3.0.3...HEAD
[3.0.3]: https://github.com/stickerdaniel/linkedin-mcp-server/compare/v3.0.2...v3.0.3
[3.0.2]: https://github.com/stickerdaniel/linkedin-mcp-server/compare/v3.0.1...v3.0.2
[3.0.1]: https://github.com/stickerdaniel/linkedin-mcp-server/compare/v3.0.0...v3.0.1
[3.0.0]: https://github.com/stickerdaniel/linkedin-mcp-server/compare/v2.3.7...v3.0.0
[2.3.7]: https://github.com/stickerdaniel/linkedin-mcp-server/compare/v2.3.6...v2.3.7
[2.3.6]: https://github.com/stickerdaniel/linkedin-mcp-server/compare/v2.3.5...v2.3.6
[2.3.5]: https://github.com/stickerdaniel/linkedin-mcp-server/compare/v2.3.4...v2.3.5
[2.3.4]: https://github.com/stickerdaniel/linkedin-mcp-server/compare/v2.3.3...v2.3.4
[2.3.3]: https://github.com/stickerdaniel/linkedin-mcp-server/compare/v2.3.2...v2.3.3
[2.3.2]: https://github.com/stickerdaniel/linkedin-mcp-server/compare/v2.3.1...v2.3.2
[2.3.1]: https://github.com/stickerdaniel/linkedin-mcp-server/compare/v2.3.0...v2.3.1
[2.3.0]: https://github.com/stickerdaniel/linkedin-mcp-server/compare/v2.0.0...v2.3.0
[2.0.0]: https://github.com/stickerdaniel/linkedin-mcp-server/releases/tag/v2.0.0
