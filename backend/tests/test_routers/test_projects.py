def test_create_project(client):
    response = client.post("/api/projects/", json={
        "name": "Chicago Mfg",
        "keyword": "manufacturing",
        "location": "Chicago",
        "radius": 50.0,
    })
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["name"] == "Chicago Mfg"
    assert body["data"]["id"] is not None


def test_list_projects(client):
    client.post("/api/projects/", json={
        "name": "P1", "keyword": "k", "location": "L"
    })
    client.post("/api/projects/", json={
        "name": "P2", "keyword": "k", "location": "L"
    })
    response = client.get("/api/projects/")
    body = response.json()
    assert body["success"] is True
    assert len(body["data"]) == 2


def test_get_project(client):
    create_resp = client.post("/api/projects/", json={
        "name": "Test", "keyword": "k", "location": "L"
    })
    pid = create_resp.json()["data"]["id"]

    response = client.get(f"/api/projects/{pid}")
    body = response.json()
    assert body["success"] is True
    assert body["data"]["name"] == "Test"


def test_get_project_not_found(client):
    response = client.get("/api/projects/999")
    body = response.json()
    assert body["success"] is False
    assert "not found" in body["error"].lower()


def test_update_project(client):
    create_resp = client.post("/api/projects/", json={
        "name": "Old", "keyword": "k", "location": "L"
    })
    pid = create_resp.json()["data"]["id"]

    response = client.put(f"/api/projects/{pid}", json={"name": "New"})
    body = response.json()
    assert body["success"] is True
    assert body["data"]["name"] == "New"
    assert body["data"]["keyword"] == "k"


def test_delete_project(client):
    create_resp = client.post("/api/projects/", json={
        "name": "Del", "keyword": "k", "location": "L"
    })
    pid = create_resp.json()["data"]["id"]

    response = client.delete(f"/api/projects/{pid}")
    body = response.json()
    assert body["success"] is True

    get_resp = client.get(f"/api/projects/{pid}")
    assert get_resp.json()["success"] is False
