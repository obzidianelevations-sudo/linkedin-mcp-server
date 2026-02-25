"""
M&A Advisor tool — modeled on Jeff Mains' Champion Leadership philosophy.

Provides expert guidance on buying and selling businesses by combining
LinkedIn reconnaissance with structured M&A frameworks covering valuation,
due diligence, deal structuring, negotiation, and exit planning.
"""

import logging
from typing import Any, Dict

from fastmcp import Context, FastMCP
from linkedin_scraper import CompanyScraper, PersonScraper
from mcp.types import ToolAnnotations

from linkedin_mcp_server.callbacks import MCPContextProgressCallback
from linkedin_mcp_server.drivers.browser import (
    ensure_authenticated,
    get_or_create_browser,
)
from linkedin_mcp_server.error_handler import handle_tool_error

logger = logging.getLogger(__name__)

MA_ADVISOR_EXPERTISE = """
## M&A Advisory Framework (Champion Leadership / Jeff Mains Methodology)

### Operating Principles
1. Deal clarity first — understand buy-side vs sell-side, deal size, industry, and stage before advising.
2. Intel before opinion — research companies and people before forming a view.
3. Champion mindset — help people build and acquire world-class businesses with competitive moats.
4. Futureproof thinking — evaluate every deal through: competitive strategy, market expansion,
   consistent processes, employee/client retention.
5. Be direct — real answers, no endless hedging. Acknowledge risk but always provide a path forward.

### Valuation Frameworks
- SDE Multiple (SMBs): 2x–4x Seller's Discretionary Earnings
- EBITDA Multiple (mid-market): 4x–12x depending on sector and growth rate
- ARR Multiple (SaaS): 3x–10x ARR depending on growth rate, NRR, and churn
- Asset-based valuation for asset-heavy businesses
- Key value drivers: recurring revenue, customer concentration, owner dependency,
  growth trajectory, competitive moat, clean financials

### Due Diligence Checklist (Buy Side)
- Financial: 3 years P&L, balance sheets, tax returns, AR/AP aging
- Legal: entity structure, contracts, IP ownership, litigation history
- Operational: key employee agreements, customer contracts, vendor dependencies
- Technical (SaaS): codebase quality, infrastructure costs, tech debt
- Commercial: customer churn, NPS, pipeline, sales cycle length
- Owner dependency: what breaks if the founder leaves on day 1?

### Deal Red Flags
- Customer concentration >20% in a single client
- Revenue declining 2+ consecutive years
- Owner is the only salesperson and key relationship holder
- Unaudited or inconsistent financials
- Pending litigation or unresolved IP disputes
- High employee turnover in key roles

### Deal Structures
- Asset purchase vs. stock purchase (tax implications differ significantly)
- Earnouts: tie seller payout to future performance milestones
- Seller financing: seller holds a note (typically 10–30% of deal value)
- Rollover equity: seller retains minority stake post-acquisition
- LOI → Purchase Agreement → Close (typical 60–120 day process)

### Exit Planning (Sell Side)
- Start 2–3 years before target exit date
- Reduce owner dependency: document processes, build management team
- Clean up financials: separate personal from business expenses
- Build recurring revenue: buyers pay premiums for predictability
- Know your buyer universe: strategic acquirers vs. financial buyers (PE)
- Strategic acquirers pay more (synergy premium) but move slower
- PE firms pay fair market value but move fast and have capital ready

### Negotiation Principles
- Price is not the only lever — terms, structure, and timing matter as much
- First offer anchors the deal — know your number before entering the room
- Never negotiate against yourself — let the other side move first after anchoring
- Understand the other party's "why" — a seller who wants legacy preservation
  needs different deal terms than one who wants maximum cash
- Walk-away clarity: know your BATNA before every negotiation

### Engagement Workflow
1. Diagnose — clarify buy or sell side, deal size, industry, and stage
2. Research — review LinkedIn data on company and decision-maker
3. Assess — apply the relevant framework (valuation, due diligence, exit readiness)
4. Advise — give a clear, structured recommendation with reasoning
5. Next step — always close with a concrete action for the user
"""


def register_ma_advisor_tools(mcp: FastMCP) -> None:
    """
    Register the M&A advisor tool with the MCP server.

    Args:
        mcp: The MCP server instance
    """

    @mcp.tool(
        annotations=ToolAnnotations(
            title="M&A Business Advisor",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=True,
        )
    )
    async def ma_advisor(
        situation: str,
        ctx: Context,
        company_name: str = "",
        person_linkedin_username: str = "",
    ) -> Dict[str, Any]:
        """
        M&A Business Advisor: Expert guidance on buying and selling businesses.

        Modeled on Jeff Mains' Champion Leadership philosophy — direct,
        experience-backed advisory for deal sourcing, valuation, due diligence,
        negotiation, and exit planning in the SMB and SaaS space ($1M–$100M deals).

        Automatically researches named companies and people on LinkedIn before
        formulating advice, combining live intelligence with structured M&A frameworks.

        Use this tool when the user needs guidance on:
        - Evaluating a business acquisition target
        - Planning or preparing a business exit
        - Structuring a deal (earnouts, seller financing, rollover equity)
        - Conducting due diligence on a target
        - Valuing a business (SDE, EBITDA, ARR multiples)
        - Negotiation strategy for buy-side or sell-side
        - Exit readiness assessment

        Args:
            situation: Describe the deal situation or question (e.g., "I want to acquire
                       a $5M ARR SaaS company in HR tech" or "I'm planning to sell my
                       services business in 18 months — what do I need to do?")
            ctx: FastMCP context for progress reporting
            company_name: Optional LinkedIn company slug to research as part of the deal
                          (e.g., "champion-leadership-group", "hubspot")
            person_linkedin_username: Optional LinkedIn username of the owner or founder
                                      to research (e.g., "jeffkmains", "williamhgates")

        Returns:
            Dict containing:
            - situation: The user's original situation/question
            - advisory_framework: M&A expertise and frameworks to guide the response
            - company_intel: LinkedIn company data if company_name was provided
            - person_intel: LinkedIn person data if person_linkedin_username was provided
            - instructions: Guidance on how to synthesize intel into expert advice
        """
        result: Dict[str, Any] = {
            "situation": situation,
            "advisory_framework": MA_ADVISOR_EXPERTISE,
            "company_intel": None,
            "person_intel": None,
            "instructions": (
                "You are acting as a seasoned M&A advisor with the expertise and voice of "
                "Jeff Mains, founder of Champion Leadership Group. Using the advisory_framework "
                "above and any LinkedIn intel gathered below, provide a direct, structured, "
                "experience-backed response to the user's situation. Lead with your assessment, "
                "support with reasoning, and close with a concrete next step. Use clear headers."
            ),
        }

        # LinkedIn recon — company
        if company_name:
            try:
                await ensure_authenticated()
                linkedin_url = f"https://www.linkedin.com/company/{company_name}/"
                logger.info(f"M&A advisor researching company: {linkedin_url}")
                browser = await get_or_create_browser()
                scraper = CompanyScraper(
                    browser.page, callback=MCPContextProgressCallback(ctx)
                )
                company = await scraper.scrape(linkedin_url)
                result["company_intel"] = company.to_dict()
            except Exception as e:
                logger.warning(f"Could not scrape company '{company_name}': {e}")
                result["company_intel"] = {"error": f"Could not retrieve data for '{company_name}'"}

        # LinkedIn recon — person
        if person_linkedin_username:
            try:
                await ensure_authenticated()
                linkedin_url = f"https://www.linkedin.com/in/{person_linkedin_username}/"
                logger.info(f"M&A advisor researching person: {linkedin_url}")
                browser = await get_or_create_browser()
                scraper = PersonScraper(
                    browser.page, callback=MCPContextProgressCallback(ctx)
                )
                person = await scraper.scrape(linkedin_url)
                result["person_intel"] = person.to_dict()
            except Exception as e:
                logger.warning(f"Could not scrape person '{person_linkedin_username}': {e}")
                result["person_intel"] = {"error": f"Could not retrieve data for '{person_linkedin_username}'"}

        return result
