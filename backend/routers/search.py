from fastapi import APIRouter, Depends
from sqlmodel import Session

from db.database import get_session
from repositories.business_repo import BusinessRepository
from schemas.base import ok, err
from schemas.business import SearchRequest
from services.overpass_service import search_businesses

router = APIRouter(prefix="/api/search", tags=["search"])


@router.post("/places")
async def search_places(
    data: SearchRequest,
    session: Session = Depends(get_session),
):
    repo = BusinessRepository(session)

    try:
        results = await search_businesses(
            location=data.location,
            keyword=data.keyword,
            radius=data.radius,
            max_results=data.max_results,
        )
    except ValueError as e:
        return err(str(e))
    except Exception as e:
        return err(f"Search failed: {str(e)}")

    # Duplicate detection: skip businesses already in this project
    existing_place_ids = repo.get_place_ids_for_project(data.project_id)

    items = []
    skipped = 0
    for r in results:
        if r.osm_id in existing_place_ids:
            skipped += 1
            continue
        items.append({
            "project_id": data.project_id,
            "place_id": r.osm_id,
            "name": r.name,
            "address": r.address,
            "phone": r.phone,
            "website": r.website,
            "category": r.category,
            "lat": r.lat,
            "lon": r.lon,
            "maps_url": f"https://www.openstreetmap.org/{r.osm_id}",
        })

    businesses = repo.create_many(items)
    return ok(
        [b.model_dump() for b in businesses],
        meta={"skipped_duplicates": skipped},
    )
