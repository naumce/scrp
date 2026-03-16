import json
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Project(SQLModel, table=True):
    __tablename__ = "projects"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    keyword: str
    location: str
    radius: float = 50.0
    max_results: int = 60
    notes: str = ""
    created_at: datetime = Field(default_factory=_utc_now)


class Business(SQLModel, table=True):
    __tablename__ = "businesses"

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id")
    place_id: str = ""
    name: str
    address: str = ""
    phone: str = ""
    website: str = ""
    rating: Optional[float] = None
    reviews: Optional[int] = None
    category: str = ""
    lat: float = 0.0
    lon: float = 0.0
    maps_url: str = ""
    is_favorite: bool = False
    notes: str = ""
    created_at: datetime = Field(default_factory=_utc_now)


class EnrichmentResult(SQLModel, table=True):
    __tablename__ = "enrichment_results"

    id: Optional[int] = Field(default=None, primary_key=True)
    business_id: int = Field(foreign_key="businesses.id")
    emails_json: str = "[]"
    phones_json: str = "[]"
    contact_page: str = ""
    social_links_json: str = "[]"
    status: str = "pending"
    error_message: str = ""
    created_at: datetime = Field(default_factory=_utc_now)

    @property
    def emails(self) -> list[str]:
        return json.loads(self.emails_json)

    @property
    def phones(self) -> list[str]:
        return json.loads(self.phones_json)

    @property
    def social_links(self) -> list[str]:
        return json.loads(self.social_links_json)


class Setting(SQLModel, table=True):
    __tablename__ = "settings"

    key: str = Field(primary_key=True)
    value: str = ""
