def _create_project(client) -> int:
    resp = client.post("/api/projects/", json={
        "name": "Test", "keyword": "k", "location": "L"
    })
    return resp.json()["data"]["id"]


def _create_business(client, project_id: int) -> dict:
    # Insert directly via search endpoint would require mocking.
    # Instead, use the DB through the project's businesses.
    # For simplicity, we'll create via the session in conftest.
    # But since we're testing the router, let's use a helper.
    pass


def test_list_businesses_empty(client):
    pid = _create_project(client)
    response = client.get(f"/api/businesses/?project_id={pid}")
    body = response.json()
    assert body["success"] is True
    assert body["data"] == []


def test_list_businesses(client, session):
    from db.models import Business
    pid = _create_project(client)
    session.add(Business(project_id=pid, name="Biz1"))
    session.add(Business(project_id=pid, name="Biz2"))
    session.commit()

    response = client.get(f"/api/businesses/?project_id={pid}")
    body = response.json()
    assert body["success"] is True
    assert len(body["data"]) == 2


def test_get_business(client, session):
    from db.models import Business
    pid = _create_project(client)
    biz = Business(project_id=pid, name="TestBiz")
    session.add(biz)
    session.commit()
    session.refresh(biz)

    response = client.get(f"/api/businesses/{biz.id}")
    body = response.json()
    assert body["success"] is True
    assert body["data"]["name"] == "TestBiz"


def test_get_business_not_found(client):
    response = client.get("/api/businesses/999")
    body = response.json()
    assert body["success"] is False


def test_toggle_favorite(client, session):
    from db.models import Business
    pid = _create_project(client)
    biz = Business(project_id=pid, name="FavBiz")
    session.add(biz)
    session.commit()
    session.refresh(biz)

    response = client.patch(f"/api/businesses/{biz.id}/favorite")
    body = response.json()
    assert body["success"] is True
    assert body["data"]["is_favorite"] is True


def test_delete_business(client, session):
    from db.models import Business
    pid = _create_project(client)
    biz = Business(project_id=pid, name="DelBiz")
    session.add(biz)
    session.commit()
    session.refresh(biz)

    response = client.delete(f"/api/businesses/{biz.id}")
    body = response.json()
    assert body["success"] is True

    get_resp = client.get(f"/api/businesses/{biz.id}")
    assert get_resp.json()["success"] is False
