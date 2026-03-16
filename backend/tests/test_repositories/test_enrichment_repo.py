import json

from db.models import Project, Business
from repositories.enrichment_repo import EnrichmentRepository


def _create_business(session) -> Business:
    p = Project(name="Test", keyword="k", location="L")
    session.add(p)
    session.commit()
    session.refresh(p)
    b = Business(project_id=p.id, name="TestBiz")
    session.add(b)
    session.commit()
    session.refresh(b)
    return b


def test_create_enrichment(session):
    biz = _create_business(session)
    repo = EnrichmentRepository(session)
    result = repo.create({
        "business_id": biz.id,
        "emails_json": json.dumps(["info@test.com"]),
        "phones_json": json.dumps(["+1234567890"]),
        "status": "success",
    })
    assert result.id is not None
    assert result.emails == ["info@test.com"]
    assert result.phones == ["+1234567890"]


def test_find_by_business(session):
    biz = _create_business(session)
    repo = EnrichmentRepository(session)
    repo.create({"business_id": biz.id, "status": "success"})
    found = repo.find_by_business(biz.id)
    assert found is not None
    assert found.business_id == biz.id


def test_find_by_business_not_found(session):
    repo = EnrichmentRepository(session)
    assert repo.find_by_business(999) is None


def test_find_by_businesses(session):
    biz1 = _create_business(session)
    biz2 = _create_business(session)
    repo = EnrichmentRepository(session)
    repo.create({"business_id": biz1.id, "status": "success"})
    repo.create({"business_id": biz2.id, "status": "failed"})
    results = repo.find_by_businesses([biz1.id, biz2.id])
    assert len(results) == 2


def test_enrichment_json_properties(session):
    biz = _create_business(session)
    repo = EnrichmentRepository(session)
    result = repo.create({
        "business_id": biz.id,
        "emails_json": json.dumps(["a@b.com", "c@d.com"]),
        "social_links_json": json.dumps(["https://linkedin.com/company/x"]),
        "status": "success",
    })
    assert result.emails == ["a@b.com", "c@d.com"]
    assert result.social_links == ["https://linkedin.com/company/x"]
    assert result.phones == []
