from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session

from db.database import get_session
from repositories.business_repo import BusinessRepository
from repositories.enrichment_repo import EnrichmentRepository
from schemas.base import ok, err

router = APIRouter(prefix="/api/businesses", tags=["businesses"])

_NOT_FOUND = "Business not found"


def _repo(session: Session = Depends(get_session)) -> BusinessRepository:
    return BusinessRepository(session)


class BulkDeleteRequest(BaseModel):
    ids: List[int]


class UpdateNotesRequest(BaseModel):
    notes: str


@router.get("/")
def list_businesses(
    project_id: int,
    repo: BusinessRepository = Depends(_repo),
):
    businesses = repo.find_by_project(project_id)
    return ok([b.model_dump() for b in businesses])


@router.get("/stats")
def project_stats(
    project_id: int,
    session: Session = Depends(get_session),
):
    biz_repo = BusinessRepository(session)
    stats = biz_repo.get_project_stats(project_id)

    # Add enrichment stats
    enrich_repo = EnrichmentRepository(session)
    businesses = biz_repo.find_by_project(project_id)
    biz_ids = [b.id for b in businesses]
    if biz_ids:
        enrichments = enrich_repo.find_by_businesses(biz_ids)
        stats["enriched"] = sum(1 for e in enrichments if e.status == "success")
        stats["with_emails"] = sum(
            1 for e in enrichments if e.status == "success" and e.emails
        )
    else:
        stats["enriched"] = 0
        stats["with_emails"] = 0

    return ok(stats)


@router.get("/{business_id}")
def get_business(
    business_id: int,
    repo: BusinessRepository = Depends(_repo),
):
    business = repo.find_by_id(business_id)
    if business is None:
        return err(_NOT_FOUND)
    return ok(business.model_dump())


@router.patch("/{business_id}/favorite")
def toggle_favorite(
    business_id: int,
    repo: BusinessRepository = Depends(_repo),
):
    business = repo.toggle_favorite(business_id)
    if business is None:
        return err(_NOT_FOUND)
    return ok(business.model_dump())


@router.patch("/{business_id}/notes")
def update_notes(
    business_id: int,
    data: UpdateNotesRequest,
    repo: BusinessRepository = Depends(_repo),
):
    business = repo.update_notes(business_id, data.notes)
    if business is None:
        return err(_NOT_FOUND)
    return ok(business.model_dump())


@router.delete("/{business_id}")
def delete_business(
    business_id: int,
    repo: BusinessRepository = Depends(_repo),
):
    deleted = repo.delete(business_id)
    if not deleted:
        return err(_NOT_FOUND)
    return ok({"deleted": True})


@router.post("/bulk-delete")
def bulk_delete(
    data: BulkDeleteRequest,
    repo: BusinessRepository = Depends(_repo),
):
    count = repo.delete_many(data.ids)
    return ok({"deleted": count})
