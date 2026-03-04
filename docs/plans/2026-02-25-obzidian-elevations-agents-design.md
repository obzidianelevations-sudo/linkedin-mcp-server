# Obzidian Elevations — Claude Code Agents Design

**Date:** 2026-02-25
**Status:** Implemented

## Overview

Two Claude Code subagents created for **Obzidian Elevations**, a procurement agency networking with high-net-worth professionals in the Aspire Tour and 10X Growth Conference space.

## Agents

### 1. `aspire-outreach`
**File:** `.claude/agents/aspire-outreach.md`
**Purpose:** Daily prospecting agent — finds 5 new contacts per run who publicly associate with Aspire Tour or 10X Growth Conference, researches their business, and drafts a two-message outreach sequence.

**Workflow:**
1. Searches Instagram, LinkedIn (via MCP tools), and web for keyword-matched profiles
2. Visits each profile to extract business details
3. Drafts Message 1 (conference hook + favorite speaker question)
4. Drafts Message 2 (business transition — "I'd love to learn more...")
5. Appends all 5 contacts to `~/Desktop/Obzidian Elevations/outreach-log.md`

**Tools used:** WebSearch, WebFetch, LinkedIn MCP tools, Write, Read

### 2. `instagram-strategist`
**File:** `.claude/agents/instagram-strategist.md`
**Purpose:** Full Instagram marketing expert for Obzidian Elevations. Handles caption writing, DM scripts, content strategy, hashtag research, and competitor analysis.

**Capabilities:**
- Caption writing (Feed, Reel, Story, Carousel)
- DM outreach scripts personalized by contact context
- Content strategy and posting calendar
- Hashtag research (WebSearch-backed, refreshed regularly)
- Competitor and trend analysis

**Brand voice:** Confident, polished, relationship-first. Speaks to high-achievers attending Aspire Tour / 10X Growth Conference. Never salesy.

**Output location:** `~/Desktop/Obzidian Elevations/instagram-content/`

## How to Use

**Daily outreach run:**
> "Run today's outreach" or "Find 5 new Aspire Tour contacts"

**Instagram content:**
> "Write a caption for [post idea]" or "Build next week's content plan" or "Write a DM script for someone who attended Aspire Tour"

## Design Decisions

- **Two separate agents over one combined** — outreach prospecting and content strategy are distinct workflows requiring different mindsets and tool sets
- **Project-level agents** (`.claude/agents/`) — both agents use the LinkedIn MCP tools registered in this project
- **Log-based deduplication** — the outreach agent checks `outreach-log.md` before finalizing contacts to avoid repeating the same person across daily runs
- **Desktop output** — all saved files go to `~/Desktop/Obzidian Elevations/` matching user's preference for desktop-organized work
