import asyncio
import json
import logging
from dataclasses import dataclass, field
from typing import Dict, List

import httpx
from sqlmodel import Session

from db.database import get_engine
from db.models import Business, EnrichmentResult
from repositories.enrichment_repo import EnrichmentRepository
from services.scraper_service import scrape_business
from services.settings_service import get_scrape_concurrency, get_scrape_timeout

logger = logging.getLogger(__name__)


@dataclass
class EnrichmentJobStatus:
    project_id: int
    total: int = 0
    completed: int = 0
    failed: int = 0
    in_progress: int = 0
    running: bool = False


# In-memory job tracking
_jobs: Dict[int, EnrichmentJobStatus] = {}


def get_job_status(project_id: int) -> EnrichmentJobStatus:
    return _jobs.get(
        project_id,
        EnrichmentJobStatus(project_id=project_id),
    )


async def _enrich_single(
    business: Business,
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
    job: EnrichmentJobStatus,
) -> dict:
    """Enrich a single business, controlled by semaphore."""
    async with semaphore:
        job.in_progress += 1
        try:
            result = await scrape_business(business.website, client)
            job.in_progress -= 1

            if result.status == "success":
                job.completed += 1
            else:
                job.failed += 1

            return {
                "business_id": business.id,
                "emails_json": json.dumps(result.emails),
                "phones_json": json.dumps(result.phones),
                "social_links_json": json.dumps(result.social_links),
                "contact_page": result.contact_page,
                "status": result.status,
                "error_message": result.error_message,
            }
        except Exception as e:
            job.in_progress -= 1
            job.failed += 1
            logger.error("Enrichment failed for business %d: %s", business.id, e)
            return {
                "business_id": business.id,
                "status": "failed",
                "error_message": str(e),
            }


async def start_enrichment(
    project_id: int,
    businesses: List[Business],
) -> EnrichmentJobStatus:
    """Start enrichment for a list of businesses."""
    job = EnrichmentJobStatus(
        project_id=project_id,
        total=len(businesses),
        running=True,
    )
    _jobs[project_id] = job

    concurrency = get_scrape_concurrency()
    timeout = get_scrape_timeout()
    semaphore = asyncio.Semaphore(concurrency)

    async with httpx.AsyncClient(timeout=timeout) as client:
        tasks = [
            _enrich_single(biz, client, semaphore, job)
            for biz in businesses
            if biz.website
        ]

        # Mark businesses without websites as failed immediately
        no_website_count = len(businesses) - len(tasks)
        job.failed += no_website_count

        results = await asyncio.gather(*tasks)

    # Save results to database
    engine = get_engine()
    with Session(engine) as session:
        repo = EnrichmentRepository(session)
        for result_data in results:
            # Check if enrichment already exists for this business
            existing = repo.find_by_business(result_data["business_id"])
            if existing:
                repo.update(existing.id, result_data)
            else:
                repo.create(result_data)

        # Also create failed entries for businesses without websites
        for biz in businesses:
            if not biz.website:
                existing = repo.find_by_business(biz.id)
                if not existing:
                    repo.create({
                        "business_id": biz.id,
                        "status": "failed",
                        "error_message": "No website URL",
                    })

    job.running = False
    return job
