def test_rate_limit_allows_normal_traffic(client):
    for _ in range(5):
        resp = client.post("/api/auth/sign-in", json={"email": "a@b.com", "password": "wrong123"})
        assert resp.status_code != 429


def test_rate_limit_blocks_after_threshold(client):
    for _ in range(10):
        client.post("/api/auth/sign-in", json={"email": "a@b.com", "password": "wrong123"})
    resp = client.post("/api/auth/sign-in", json={"email": "a@b.com", "password": "wrong123"})
    assert resp.status_code == 429
    assert "Retry-After" in resp.headers


def test_rate_limit_does_not_affect_unprotected_routes(client):
    for _ in range(15):
        resp = client.get("/api/ping")
        assert resp.status_code == 200
