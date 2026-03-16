import json
import logging
from dataclasses import dataclass, field
from typing import List, Optional

import httpx

from config import settings
from extractors.email_extractor import extract_emails
from extractors.phone_extractor import extract_phones
from extractors.social_extractor import extract_social_links
from extractors.contact_page_finder import find_contact_pages

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; LocalBizScraper/0.1)",
    "Accept": "text/html,application/xhtml+xml",
}


@dataclass(frozen=True)
class ScrapeResult:
    emails: List[str] = field(default_factory=list)
    phones: List[str] = field(default_factory=list)
    social_links: List[str] = field(default_factory=list)
    contact_page: str = ""
    status: str = "success"
    error_message: str = ""


async def fetch_page(
    url: str,
    client: httpx.AsyncClient,
    timeout: int = 0,
    max_retries: int = 0,
) -> Optional[str]:
    """Fetch a page with retries. Returns HTML or None on failure."""
    if timeout <= 0:
        timeout = settings.scrape_timeout
    if max_retries <= 0:
        max_retries = settings.scrape_max_retries

    for attempt in range(max_retries + 1):
        try:
            response = await client.get(
                url,
                headers=HEADERS,
                timeout=timeout,
                follow_redirects=True,
            )
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.warning(
                "Fetch attempt %d/%d failed for %s: %s",
                attempt + 1,
                max_retries + 1,
                url,
                str(e),
            )
            if attempt == max_retries:
                return None

    return None


async def scrape_business(website: str, client: httpx.AsyncClient) -> ScrapeResult:
    """Scrape a business website for contact information."""
    if not website:
        return ScrapeResult(status="failed", error_message="No website URL")

    # Ensure URL has scheme
    url = website if website.startswith("http") else f"https://{website}"

    # Fetch homepage
    homepage_html = await fetch_page(url, client)
    if homepage_html is None:
        return ScrapeResult(status="failed", error_message="Could not fetch homepage")

    all_html = [homepage_html]
    contact_page_url = ""

    # Find and fetch contact pages
    contact_pages = find_contact_pages(homepage_html, url, max_pages=3)
    for page_url in contact_pages:
        page_html = await fetch_page(page_url, client)
        if page_html:
            all_html.append(page_html)
            if not contact_page_url:
                contact_page_url = page_url

    # Extract from all collected pages
    combined_html = "\n".join(all_html)
    emails = extract_emails(combined_html)
    phones = extract_phones(combined_html)
    social_links = extract_social_links(combined_html)

    return ScrapeResult(
        emails=emails,
        phones=phones,
        social_links=social_links,
        contact_page=contact_page_url,
        status="success",
    )
