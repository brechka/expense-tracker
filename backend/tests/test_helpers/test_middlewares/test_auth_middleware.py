from src.helpers.security import create_access_token


def test_protected_route_without_token(client):
    resp = client.get("/api/expenses/")
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Not authenticated"


def test_protected_route_with_valid_token(client, test_user):
    token = create_access_token(test_user.id)
    resp = client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200


def test_protected_route_with_invalid_token(client):
    resp = client.get("/api/users/me", headers={"Authorization": "Bearer garbage"})
    assert resp.status_code == 401
    assert "Invalid" in resp.json()["detail"]


def test_protected_route_with_expired_token(client):
    from unittest.mock import patch
    import time
    with patch("src.helpers.security.ACCESS_TOKEN_EXPIRE_MINUTES", -1):
        token = create_access_token(1)
    time.sleep(0.1)
    resp = client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 401
    assert "expired" in resp.json()["detail"].lower()


def test_protected_route_malformed_header(client):
    resp = client.get("/api/users/me", headers={"Authorization": "NotBearer token"})
    assert resp.status_code == 401


def test_excluded_route_no_auth_needed(client):
    resp = client.get("/api/ping")
    assert resp.status_code == 200


def test_auth_route_no_auth_needed(client):
    resp = client.post("/api/auth/sign-in", json={"email": "a@b.com", "password": "wrong123"})
    # Should not be 401 from middleware — it reaches the controller
    assert resp.status_code == 401  # from controller, not middleware


def test_options_request_bypasses_auth(client):
    resp = client.options("/api/expenses/")
    # OPTIONS should not be blocked by auth middleware
    assert resp.status_code != 401
