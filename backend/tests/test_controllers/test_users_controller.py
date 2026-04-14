def test_get_me(auth_client, test_user):
    resp = auth_client.get("/api/users/me")
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == test_user.email
    assert data["name"] == test_user.name
    assert "hashed_password" not in data


def test_get_me_unauthenticated(client):
    resp = client.get("/api/users/me")
    assert resp.status_code == 401


def test_get_me_invalid_token(client):
    client.headers["Authorization"] = "Bearer invalid_token"
    resp = client.get("/api/users/me")
    assert resp.status_code == 401
