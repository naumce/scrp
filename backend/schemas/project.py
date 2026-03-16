from typing import Optional

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    keyword: str
    location: str
    radius: float = 50.0
    max_results: int = 60
    notes: str = ""


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    keyword: Optional[str] = None
    location: Optional[str] = None
    radius: Optional[float] = None
    max_results: Optional[int] = None
    notes: Optional[str] = None
