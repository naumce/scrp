import json

from db.models import Business, EnrichmentResult


def _setup_project_with_businesses(client, session):
    resp = client.post("/api/projects/", json={
        "name": "Test", "keyword": "k", "location": "L"
    })
    pid = resp.json()["data"]["id"]

    biz1 = Business(project_id=pid, name="Biz1", website="https://biz1.com")
    biz2 = Business(project_id=pid, name="Biz2", website="https://biz2.com")
    session.add(biz1)
    session.add(biz2)
    session.commit()
    session.refresh(biz1)
    session.refresh(biz2)

    return pid, [biz1, biz2]


def test_enrichment_status_no_job(client):
    response = client.get("/api/enrichment/status/999")
    body = response.json()
    assert body["success"] is True
    assert body["data"]["total"] == 0
    assert body["data"]["running"] is False


def test_enrichment_results_empty(client):
    resp = client.post("/api/projects/", json={
        "name": "Test", "keyword": "k", "location": "L"
    })
    pid = resp.json()["data"]["id"]

    response = client.get(f"/api/enrichment/results/{pid}")
    body = response.json()
    assert body["success"] is True
    assert body["data"] == []


def test_enrichment_results_with_data(client, session):
    pid, businesses = _setup_project_with_businesses(client, session)

    # Manually insert enrichment results
    er = EnrichmentResult(
        business_id=businesses[0].id,
        emails_json=json.dumps(["info@biz1.com"]),
        phones_json=json.dumps(["+15550100"]),
        social_links_json=json.dumps(["https://linkedin.com/company/biz1"]),
        contact_page="https://biz1.com/contact",
        status="success",
    )
    session.add(er)
    session.commit()

    response = client.get(f"/api/enrichment/results/{pid}")
    body = response.json()
    assert body["success"] is True
    assert len(body["data"]) == 1
    assert body["data"][0]["emails"] == ["info@biz1.com"]
    assert body["data"][0]["status"] == "success"


def test_start_enrichment_no_businesses(client):
    resp = client.post("/api/projects/", json={
        "name": "Test", "keyword": "k", "location": "L"
    })
    pid = resp.json()["data"]["id"]

    response = client.post("/api/enrichment/start", json={
        "project_id": pid,
        "business_ids": [9999],
    })
    body = response.json()
    assert body["success"] is False
    assert "No valid" in body["error"]
