import re
from typing import List

# Common false-positive patterns to exclude
EXCLUDE_PATTERNS = {
    "example.com",
    "example.org",
    "domain.com",
    "email.com",
    "yoursite.com",
    "yourdomain.com",
    "sentry.io",
    "wixpress.com",
}

# File extensions that aren't emails
FILE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".css", ".js"}

EMAIL_REGEX = re.compile(
    r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
)

MAILTO_REGEX = re.compile(
    r'mailto:([a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})',
)


def _is_valid_email(email: str) -> bool:
    lower = email.lower()
    domain = lower.split("@", 1)[1] if "@" in lower else ""

    if domain in EXCLUDE_PATTERNS:
        return False

    if any(lower.endswith(ext) for ext in FILE_EXTENSIONS):
        return False

    if len(email) > 254:
        return False

    return True


def extract_emails(html: str) -> List[str]:
    """Extract unique email addresses from HTML content."""
    found: set = set()

    for match in MAILTO_REGEX.finditer(html):
        email = match.group(1).strip()
        if _is_valid_email(email):
            found.add(email.lower())

    for match in EMAIL_REGEX.finditer(html):
        email = match.group(0).strip()
        if _is_valid_email(email):
            found.add(email.lower())

    return sorted(found)
