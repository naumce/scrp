from typing import List, Literal, Optional

from pydantic import BaseModel


class ExportRequest(BaseModel):
    project_id: int
    format: Literal["csv", "excel"]
    business_ids: Optional[List[int]] = None
