import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from db.models import Business
from services.enrichment_service import (
    EnrichmentJobStatus,
    get_job_status,
    _enrich_single,
    start_enrichment,
    _jobs,
)
from services.scraper_service import ScrapeResult


def _make_business(id=1, website="https://test.com", **kw):
    return Business(
        id=id,
        project_id=1,
        name=f"Biz{id}",
        website=website,
        **kw,
    )


def _make_scrape_result(**overrides):
    defaults = dict(
        status="success",
        emails=["info@test.com"],
        phones=["+15551234"],
        social_links=["https://linkedin.com/company/test"],
        contact_page="https://test.com/contact",
        error_message="",
    )
    defaults.update(overrides)
    return ScrapeResult(**defaults)


# --- get_job_status ---


def test_get_job_status_no_job():
    status = get_job_status(9999)
    assert status.project_id == 9999
    assert status.total == 0
    assert status.running is False


def test_get_job_status_existing():
    _jobs[777] = EnrichmentJobStatus(project_id=777, total=5, running=True)
    try:
        status = get_job_status(777)
        assert status.total == 5
        assert status.running is True
    finally:
        _jobs.pop(777, None)


# --- _enrich_single ---


@pytest.mark.asyncio
async def test_enrich_single_success():
    biz = _make_business()
    client = AsyncMock()
    sem = asyncio.Semaphore(5)
    job = EnrichmentJobStatus(project_id=1, total=1, running=True)

    result = _make_scrape_result()
    with patch(
        "services.enrichment_service.scrape_business",
        new_callable=AsyncMock,
        return_value=result,
    ):
        data = await _enrich_single(biz, client, sem, job)

    assert data["status"] == "success"
    assert data["business_id"] == 1
    assert json.loads(data["emails_json"]) == ["info@test.com"]
    assert job.completed == 1
    assert job.in_progress == 0


@pytest.mark.asyncio
async def test_enrich_single_failed_scrape():
    biz = _make_business()
    client = AsyncMock()
    sem = asyncio.Semaphore(5)
    job = EnrichmentJobStatus(project_id=1, total=1, running=True)

    result = _make_scrape_result(status="failed", error_message="timeout")
    with patch(
        "services.enrichment_service.scrape_business",
        new_callable=AsyncMock,
        return_value=result,
    ):
        data = await _enrich_single(biz, client, sem, job)

    assert data["status"] == "failed"
    assert job.failed == 1
    assert job.in_progress == 0


@pytest.mark.asyncio
async def test_enrich_single_exception():
    biz = _make_business()
    client = AsyncMock()
    sem = asyncio.Semaphore(5)
    job = EnrichmentJobStatus(project_id=1, total=1, running=True)

    with patch(
        "services.enrichment_service.scrape_business",
        new_callable=AsyncMock,
        side_effect=RuntimeError("connection failed"),
    ):
        data = await _enrich_single(biz, client, sem, job)

    assert data["status"] == "failed"
    assert "connection failed" in data["error_message"]
    assert job.failed == 1
    assert job.in_progress == 0


# --- start_enrichment ---


@pytest.mark.asyncio
async def test_start_enrichment_success():
    biz1 = _make_business(id=1)
    biz2 = _make_business(id=2, website="https://other.com")

    result = _make_scrape_result()

    with patch(
        "services.enrichment_service.scrape_business",
        new_callable=AsyncMock,
        return_value=result,
    ), patch(
        "services.enrichment_service.get_engine",
    ) as mock_engine, patch(
        "services.enrichment_service.Session",
    ) as MockSession:
        mock_session = MagicMock()
        MockSession.return_value.__enter__ = MagicMock(return_value=mock_session)
        MockSession.return_value.__exit__ = MagicMock(return_value=False)

        # Mock the repo methods
        mock_repo_instance = MagicMock()
        mock_repo_instance.find_by_business.return_value = None

        with patch(
            "services.enrichment_service.EnrichmentRepository",
            return_value=mock_repo_instance,
        ):
            job = await start_enrichment(1, [biz1, biz2])

    assert job.running is False
    assert job.total == 2
    assert job.completed == 2
    assert job.failed == 0
    assert mock_repo_instance.create.call_count == 2


@pytest.mark.asyncio
async def test_start_enrichment_no_website():
    biz_no_site = _make_business(id=1, website="")

    with patch(
        "services.enrichment_service.get_engine",
    ), patch(
        "services.enrichment_service.Session",
    ) as MockSession:
        mock_session = MagicMock()
        MockSession.return_value.__enter__ = MagicMock(return_value=mock_session)
        MockSession.return_value.__exit__ = MagicMock(return_value=False)

        mock_repo_instance = MagicMock()
        mock_repo_instance.find_by_business.return_value = None

        with patch(
            "services.enrichment_service.EnrichmentRepository",
            return_value=mock_repo_instance,
        ):
            job = await start_enrichment(1, [biz_no_site])

    assert job.failed == 1
    assert job.completed == 0
    # Should create a "No website URL" entry
    mock_repo_instance.create.assert_called_once()
    call_data = mock_repo_instance.create.call_args[0][0]
    assert call_data["status"] == "failed"
    assert "No website" in call_data["error_message"]


@pytest.mark.asyncio
async def test_start_enrichment_updates_existing():
    biz = _make_business(id=1)
    result = _make_scrape_result()

    existing_enrichment = MagicMock()
    existing_enrichment.id = 99

    with patch(
        "services.enrichment_service.scrape_business",
        new_callable=AsyncMock,
        return_value=result,
    ), patch(
        "services.enrichment_service.get_engine",
    ), patch(
        "services.enrichment_service.Session",
    ) as MockSession:
        mock_session = MagicMock()
        MockSession.return_value.__enter__ = MagicMock(return_value=mock_session)
        MockSession.return_value.__exit__ = MagicMock(return_value=False)

        mock_repo_instance = MagicMock()
        mock_repo_instance.find_by_business.return_value = existing_enrichment

        with patch(
            "services.enrichment_service.EnrichmentRepository",
            return_value=mock_repo_instance,
        ):
            job = await start_enrichment(1, [biz])

    assert job.completed == 1
    mock_repo_instance.update.assert_called_once()
    mock_repo_instance.create.assert_not_called()
