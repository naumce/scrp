import re
from typing import List
from urllib.parse import urlparse

SOCIAL_DOMAINS = {
    "facebook.com": "facebook",
    "fb.com": "facebook",
    "twitter.com": "twitter",
    "x.com": "twitter",
    "linkedin.com": "linkedin",
    "instagram.com": "instagram",
    "youtube.com": "youtube",
    "tiktok.com": "tiktok",
}

SOCIAL_URL_REGEX = re.compile(
    r'https?://(?:www\.)?(?:'
    + "|".join(re.escape(d) for d in SOCIAL_DOMAINS)
    + r')[^\s"\'<>]*',
)


def _normalize_url(url: str) -> str:
    url = url.rstrip("/").rstrip(")")
    # Remove tracking params
    if "?" in url:
        url = url.split("?")[0]
    return url


def _is_profile_url(url: str) -> bool:
    """Filter out generic social pages (login, share, etc.)."""
    parsed = urlparse(url)
    path = parsed.path.lower().strip("/")

    skip_paths = {"share", "sharer", "intent", "login", "signup", "help", "about"}
    if path in skip_paths:
        return False

    # Must have a meaningful path (profile/company page)
    return len(path) > 0


def extract_social_links(html: str) -> List[str]:
    """Extract unique social media profile URLs from HTML content."""
    found: set = set()

    for match in SOCIAL_URL_REGEX.finditer(html):
        url = _normalize_url(match.group(0))
        if _is_profile_url(url):
            found.add(url)

    return sorted(found)
