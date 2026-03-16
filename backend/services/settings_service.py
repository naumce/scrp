"""Read user-configured settings from the database.

Falls back to hardcoded defaults if not set.
"""
from sqlmodel import Session, select

from db.database import get_engine
from db.models import Setting

DEFAULTS = {
    "default_radius": "50",
    "default_max_results": "60",
    "scrape_timeout": "10",
    "scrape_concurrency": "5",
}


def get_all_settings() -> dict:
    """Read all settings from DB, merged with defaults."""
    engine = get_engine()
    with Session(engine) as session:
        rows = session.exec(select(Setting)).all()
    result = dict(DEFAULTS)
    for row in rows:
        result[row.key] = row.value
    return result


def get_setting(key: str) -> str:
    """Read a single setting value."""
    return get_all_settings().get(key, DEFAULTS.get(key, ""))


def get_scrape_timeout() -> int:
    return int(get_setting("scrape_timeout"))


def get_scrape_concurrency() -> int:
    return int(get_setting("scrape_concurrency"))
