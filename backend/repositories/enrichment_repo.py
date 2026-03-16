from typing import Optional

from sqlmodel import Session, select

from db.models import EnrichmentResult
from repositories.base import Repository


class EnrichmentRepository(Repository[EnrichmentResult]):
    def __init__(self, session: Session):
        super().__init__(EnrichmentResult, session)

    def find_by_business(self, business_id: int) -> Optional[EnrichmentResult]:
        statement = select(EnrichmentResult).where(
            EnrichmentResult.business_id == business_id
        )
        return self._session.exec(statement).first()

    def find_by_businesses(
        self, business_ids: list[int]
    ) -> list[EnrichmentResult]:
        statement = select(EnrichmentResult).where(
            EnrichmentResult.business_id.in_(business_ids)  # type: ignore
        )
        return list(self._session.exec(statement).all())
