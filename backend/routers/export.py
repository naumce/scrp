from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlmodel import Session

from db.database import get_session
from repositories.business_repo import BusinessRepository
from repositories.enrichment_repo import EnrichmentRepository
from schemas.base import err
from schemas.export import ExportRequest
from services.export_service import export_csv, export_excel

router = APIRouter(prefix="/api/export", tags=["export"])


@router.post("")
def create_export(
    req: ExportRequest,
    session: Session = Depends(get_session),
):
    biz_repo = BusinessRepository(session)
    enrich_repo = EnrichmentRepository(session)

    businesses = biz_repo.find_by_project(req.project_id)
    if not businesses:
        return err("No businesses found for this project")

    # Filter to selected IDs if provided
    if req.business_ids:
        id_set = set(req.business_ids)
        businesses = [b for b in businesses if b.id in id_set]
        if not businesses:
            return err("No matching businesses found")

    # Build enrichment lookup
    biz_ids = [b.id for b in businesses]
    enrichments = enrich_repo.find_by_businesses(biz_ids)
    enrichment_map = {e.business_id: e for e in enrichments}

    if req.format == "csv":
        data = export_csv(businesses, enrichment_map)
        return Response(
            content=data,
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=businesses.csv"
            },
        )

    data = export_excel(businesses, enrichment_map)
    return Response(
        content=data,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=businesses.xlsx"
        },
    )
