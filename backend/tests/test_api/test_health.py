def test_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_platform_status(client):
    response = client.get("/api/v1/platforms/status")
    assert response.status_code == 200
    data = response.json()
    assert "blinkit" in data["platforms"]
    assert "zepto" in data["platforms"]
