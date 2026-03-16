def test_get_settings_defaults(client):
    resp = client.get("/api/settings")
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["default_radius"] == "50"
    assert body["data"]["default_max_results"] == "60"
    assert body["data"]["scrape_timeout"] == "10"
    assert body["data"]["scrape_concurrency"] == "5"


def test_update_settings(client):
    resp = client.put("/api/settings", json={
        "default_radius": "100",
        "default_max_results": "120",
    })
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["default_radius"] == "100"
    assert body["data"]["default_max_results"] == "120"
    # Unchanged values keep defaults
    assert body["data"]["scrape_timeout"] == "10"


def test_update_settings_persists(client):
    client.put("/api/settings", json={"default_radius": "75"})
    resp = client.get("/api/settings")
    body = resp.json()
    assert body["data"]["default_radius"] == "75"


def test_update_settings_ignores_unknown_keys(client):
    resp = client.put("/api/settings", json={
        "default_radius": "30",
        "unknown_key": "should_be_ignored",
    })
    body = resp.json()
    assert body["success"] is True
    assert "unknown_key" not in body["data"]


def test_update_settings_overwrites(client):
    client.put("/api/settings", json={"default_radius": "50"})
    client.put("/api/settings", json={"default_radius": "99"})
    resp = client.get("/api/settings")
    assert resp.json()["data"]["default_radius"] == "99"
