from unittest.mock import patch, AsyncMock

from services.overpass_service import BusinessResult


MOCK_RESULTS = [
    BusinessResult(
        osm_id="node/123",
        name="ACME Corp",
        address="100 Main St, Chicago",
        phone="+1-555-0100",
        website="https://acme.com",
        category="Factory",
        lat=41.88,
        lon=-87.63,
    ),
    BusinessResult(
        osm_id="node/456",
        name="Bob's Shop",
        address="200 Oak Ave",
        phone="",
        website="",
        category="Shop",
        lat=41.87,
        lon=-87.64,
    ),
]


def test_search_places_success(client):
    pid_resp = client.post("/api/projects/", json={
        "name": "Test", "keyword": "manufacturing", "location": "Chicago"
    })
    pid = pid_resp.json()["data"]["id"]

    with patch(
        "routers.search.search_businesses",
        new_callable=AsyncMock,
        return_value=MOCK_RESULTS,
    ):
        response = client.post("/api/search/places", json={
            "project_id": pid,
            "keyword": "manufacturing",
            "location": "Chicago",
            "radius": 50.0,
            "max_results": 60,
        })

    body = response.json()
    assert body["success"] is True
    assert len(body["data"]) == 2
    assert body["data"][0]["name"] == "ACME Corp"
    assert body["data"][0]["project_id"] == pid
    assert body["data"][1]["name"] == "Bob's Shop"


def test_search_places_geocode_error(client):
    pid_resp = client.post("/api/projects/", json={
        "name": "Test", "keyword": "k", "location": "L"
    })
    pid = pid_resp.json()["data"]["id"]

    with patch(
        "routers.search.search_businesses",
        new_callable=AsyncMock,
        side_effect=ValueError("Could not geocode location: BadPlace"),
    ):
        response = client.post("/api/search/places", json={
            "project_id": pid,
            "keyword": "test",
            "location": "BadPlace",
        })

    body = response.json()
    assert body["success"] is False
    assert "geocode" in body["error"].lower()


def test_search_places_stores_businesses(client):
    pid_resp = client.post("/api/projects/", json={
        "name": "Test", "keyword": "k", "location": "L"
    })
    pid = pid_resp.json()["data"]["id"]

    with patch(
        "routers.search.search_businesses",
        new_callable=AsyncMock,
        return_value=MOCK_RESULTS,
    ):
        client.post("/api/search/places", json={
            "project_id": pid,
            "keyword": "k",
            "location": "L",
        })

    # Verify businesses are persisted
    response = client.get(f"/api/businesses/?project_id={pid}")
    body = response.json()
    assert body["success"] is True
    assert len(body["data"]) == 2
