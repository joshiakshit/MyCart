def test_search_returns_structure(client):
    response = client.get("/api/v1/search", params={"q": "milk"})
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "milk"
    assert "results" in data
    assert "platform_status" in data
