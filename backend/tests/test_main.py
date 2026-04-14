def test_ping(client):
    response = client.get("/api/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}


def test_404(client):
    response = client.get("/api/nonexistent")
    assert response.status_code == 404


def test_docs_accessible(client):
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_json_accessible(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert data["info"]["title"] == "Expense Tracker API"
    assert "BearerAuth" in data["components"]["securitySchemes"]
