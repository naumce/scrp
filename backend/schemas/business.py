from pydantic import BaseModel


class SearchRequest(BaseModel):
    project_id: int
    keyword: str
    location: str
    radius: float = 50.0
    max_results: int = 60
