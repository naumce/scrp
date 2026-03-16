import re
from typing import List

# Match various phone formats:
# +1 (312) 555-0100, +1-312-555-0100, (312) 555-0100, 312.555.0100, etc.
PHONE_REGEX = re.compile(
    r"""
    (?:
        \+?\d{1,3}[\s.\-]?       # optional country code
    )?
    \(?\d{2,4}\)?                 # area code (with optional parens)
    [\s.\-]?
    \d{3,4}                       # first part
    [\s.\-]?
    \d{3,4}                       # second part
    """,
    re.VERBOSE,
)

TEL_REGEX = re.compile(
    r'tel:([+\d\s.\-()]+)',
)

# Minimum digits to be a valid phone number
MIN_DIGITS = 7
MAX_DIGITS = 15


def _normalize(phone: str) -> str:
    return re.sub(r"[^\d+]", "", phone)


def _is_valid_phone(phone: str) -> bool:
    digits = re.sub(r"\D", "", phone)
    return MIN_DIGITS <= len(digits) <= MAX_DIGITS


def extract_phones(html: str) -> List[str]:
    """Extract unique phone numbers from HTML content."""
    found: set = set()

    for match in TEL_REGEX.finditer(html):
        raw = match.group(1).strip()
        if _is_valid_phone(raw):
            found.add(_normalize(raw))

    for match in PHONE_REGEX.finditer(html):
        raw = match.group(0).strip()
        if _is_valid_phone(raw):
            found.add(_normalize(raw))

    return sorted(found)
