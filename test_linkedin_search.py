#!/usr/bin/env python3
"""Quick test script to search LinkedIn directly."""
import asyncio
from linkedin_scraper import JobSearchScraper
from linkedin_mcp_server.drivers.browser import get_or_create_browser


async def search_jobs(keywords: str, location: str = "", limit: int = 10):
    """Search for jobs on LinkedIn."""
    print(f"🔍 Searching for: '{keywords}' in '{location or 'Any location'}'...")

    browser = await get_or_create_browser()
    scraper = JobSearchScraper(browser.page)

    job_urls = await scraper.search(
        keywords=keywords,
        location=location,
        limit=limit
    )

    print(f"\n✅ Found {len(job_urls)} jobs:\n")
    for i, url in enumerate(job_urls, 1):
        print(f"{i}. {url}")

    return job_urls


async def get_profile(username: str):
    """Get a LinkedIn profile."""
    from linkedin_scraper import PersonScraper

    print(f"🔍 Fetching profile for: {username}...")

    browser = await get_or_create_browser()
    scraper = PersonScraper(browser.page)

    linkedin_url = f"https://www.linkedin.com/in/{username}/"
    person = await scraper.scrape(linkedin_url)

    print(f"\n✅ Profile found:")
    print(f"Name: {person.name}")
    print(f"Location: {person.location}")
    print(f"About: {person.about[:200]}..." if person.about else "")

    return person.to_dict()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  Search jobs: python test_linkedin_search.py jobs 'Python Developer' 'San Francisco'")
        print("  Get profile: python test_linkedin_search.py profile williamhgates")
        sys.exit(1)

    command = sys.argv[1]

    if command == "jobs":
        keywords = sys.argv[2] if len(sys.argv) > 2 else "Python"
        location = sys.argv[3] if len(sys.argv) > 3 else ""
        asyncio.run(search_jobs(keywords, location))
    elif command == "profile":
        username = sys.argv[2] if len(sys.argv) > 2 else "williamhgates"
        asyncio.run(get_profile(username))
    else:
        print(f"Unknown command: {command}")
        print("Use 'jobs' or 'profile'")
