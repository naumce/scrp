import re
from typing import List
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

# Keywords that suggest a contact/about page
CONTACT_KEYWORDS = re.compile(
    r"\b(contact|about|team|company|impressum|kontakt|reach\s*us)\b",
    re.IGNORECASE,
)

CONTACT_HREF_PATTERNS = re.compile(
    r"/(contact|about|team|company|impressum|kontakt|reach-us|about-us|contact-us)",
    re.IGNORECASE,
)


def find_contact_pages(html: str, base_url: str, max_pages: int = 3) -> List[str]:
    """Find contact/about page URLs from the homepage HTML."""
    soup = BeautifulSoup(html, "lxml")
    found: set = set()
    base_domain = urlparse(base_url).netloc

    for link in soup.find_all("a", href=True):
        href = link["href"]
        text = link.get_text(strip=True).lower()

        # Check link text for contact keywords
        text_match = bool(CONTACT_KEYWORDS.search(text))
        # Check href path for contact patterns
        href_match = bool(CONTACT_HREF_PATTERNS.search(href))

        if text_match or href_match:
            full_url = urljoin(base_url, href)
            parsed = urlparse(full_url)

            # Only follow links on the same domain
            if parsed.netloc == base_domain and parsed.scheme in ("http", "https"):
                found.add(full_url.split("#")[0].split("?")[0])

        if len(found) >= max_pages:
            break

    return sorted(found)
