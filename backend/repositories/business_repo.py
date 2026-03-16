from typing import List, Optional, Set

from sqlmodel import Session, select

from db.models import Business
from repositories.base import Repository


class BusinessRepository(Repository[Business]):
    def __init__(self, session: Session):
        super().__init__(Business, session)

    def find_by_project(self, project_id: int) -> list[Business]:
        statement = select(Business).where(
            Business.project_id == project_id
        )
        return list(self._session.exec(statement).all())

    def get_place_ids_for_project(self, project_id: int) -> Set[str]:
        """Get all place_ids already in a project for duplicate detection."""
        statement = select(Business.place_id).where(
            Business.project_id == project_id
        )
        return set(self._session.exec(statement).all())

    def create_many(self, items: list[dict]) -> list[Business]:
        instances = [Business(**item) for item in items]
        for inst in instances:
            self._session.add(inst)
        self._session.commit()
        for inst in instances:
            self._session.refresh(inst)
        return instances

    def delete_many(self, ids: List[int]) -> int:
        """Delete multiple businesses by ID. Returns count deleted."""
        count = 0
        for bid in ids:
            instance = self._session.get(Business, bid)
            if instance:
                self._session.delete(instance)
                count += 1
        self._session.commit()
        return count

    def toggle_favorite(self, id: int) -> Optional[Business]:
        business = self._session.get(Business, id)
        if business is None:
            return None
        business.is_favorite = not business.is_favorite
        self._session.add(business)
        self._session.commit()
        self._session.refresh(business)
        return business

    def update_notes(self, id: int, notes: str) -> Optional[Business]:
        business = self._session.get(Business, id)
        if business is None:
            return None
        business.notes = notes
        self._session.add(business)
        self._session.commit()
        self._session.refresh(business)
        return business

    def get_project_stats(self, project_id: int) -> dict:
        """Get aggregate stats for a project's businesses."""
        businesses = self.find_by_project(project_id)
        total = len(businesses)
        with_website = sum(1 for b in businesses if b.website)
        with_phone = sum(1 for b in businesses if b.phone)
        favorites = sum(1 for b in businesses if b.is_favorite)
        return {
            "total": total,
            "with_website": with_website,
            "with_phone": with_phone,
            "favorites": favorites,
        }
