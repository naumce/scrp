from typing import List

from pydantic import BaseModel


class EnrichmentStartRequest(BaseModel):
    project_id: int
    business_ids: List[int]
