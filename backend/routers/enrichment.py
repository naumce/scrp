import asyncio

from fastapi import APIRouter, Depends
from sqlmodel import Session

from db.database import get_session
from repositories.business_repo import BusinessRepository
from repositories.enrichment_repo import EnrichmentRepository
from schemas.base import ok, err
from schemas.enrichment import EnrichmentStartRequest
from services.enrichment_service import start_enrichment, get_job_status

router = APIRouter(prefix="/api/enrichment", tags=["enrichment"])


@router.post("/start")
async def start_enrichment_endpoint(
    data: EnrichmentStartRequest,
    session: Session = Depends(get_session),
):
    biz_repo = BusinessRepository(session)
    businesses = []
    for bid in data.business_ids:
        biz = biz_repo.find_by_id(bid)
        if biz:
            businesses.append(biz)

    if not businesses:
        return err("No valid businesses found")

    # Run enrichment in background
    job = get_job_status(data.project_id)
    if job.running:
        return err("Enrichment already running for this project")

    asyncio.create_task(start_enrichment(data.project_id, businesses))

    return ok({
        "project_id": data.project_id,
        "total": len(businesses),
        "message": "Enrichment started",
    })


@router.get("/status/{project_id}")
async def enrichment_status(project_id: int):
    job = get_job_status(project_id)
    return ok({
        "project_id": job.project_id,
        "total": job.total,
        "completed": job.completed,
        "failed": job.failed,
        "in_progress": job.in_progress,
        "running": job.running,
    })


@router.get("/results/{project_id}")
def enrichment_results(
    project_id: int,
    session: Session = Depends(get_session),
):
    biz_repo = BusinessRepository(session)
    businesses = biz_repo.find_by_project(project_id)
    biz_ids = [b.id for b in businesses]

    if not biz_ids:
        return ok([])

    enrich_repo = EnrichmentRepository(session)
    results = enrich_repo.find_by_businesses(biz_ids)

    return ok([
        {
            "id": r.id,
            "business_id": r.business_id,
            "emails": r.emails,
            "phones": r.phones,
            "contact_page": r.contact_page,
            "social_links": r.social_links,
            "status": r.status,
            "error_message": r.error_message,
        }
        for r in results
    ])
