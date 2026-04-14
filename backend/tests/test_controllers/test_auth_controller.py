from unittest.mock import patch, AsyncMock


def test_sign_up(client):
    resp = client.post("/api/auth/sign-up", json={"email": "new@test.com", "name": "New", "password": "password123"})
    assert resp.status_code == 201
    assert "access_token" in resp.json()
    assert "refresh_token" in resp.cookies


def test_sign_up_duplicate(client):
    client.post("/api/auth/sign-up", json={"email": "dup@test.com", "name": "A", "password": "password123"})
    resp = client.post("/api/auth/sign-up", json={"email": "dup@test.com", "name": "B", "password": "password123"})
    assert resp.status_code == 400


def test_sign_up_short_password(client):
    resp = client.post("/api/auth/sign-up", json={"email": "x@test.com", "name": "X", "password": "short"})
    assert resp.status_code == 422


def test_sign_up_empty_name(client):
    resp = client.post("/api/auth/sign-up", json={"email": "x@test.com", "name": "  ", "password": "password123"})
    assert resp.status_code == 422


def test_sign_in(client):
    client.post("/api/auth/sign-up", json={"email": "u@test.com", "name": "U", "password": "password123"})
    resp = client.post("/api/auth/sign-in", json={"email": "u@test.com", "password": "password123"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_sign_in_wrong_password(client):
    client.post("/api/auth/sign-up", json={"email": "u@test.com", "name": "U", "password": "password123"})
    resp = client.post("/api/auth/sign-in", json={"email": "u@test.com", "password": "wrong"})
    assert resp.status_code == 401


def test_sign_in_no_user(client):
    resp = client.post("/api/auth/sign-in", json={"email": "nobody@test.com", "password": "password123"})
    assert resp.status_code == 401


def test_token_refresh(client):
    client.post("/api/auth/sign-up", json={"email": "r@test.com", "name": "R", "password": "password123"})
    resp = client.post("/api/auth/token")
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_token_refresh_no_cookie(client):
    resp = client.post("/api/auth/token")
    assert resp.status_code == 401


def test_logout(client):
    client.post("/api/auth/sign-up", json={"email": "lo@test.com", "name": "L", "password": "password123"})
    resp = client.get("/api/auth/logout")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Logged out"


def test_logout_all(client):
    client.post("/api/auth/sign-up", json={"email": "la@test.com", "name": "L", "password": "password123"})
    resp = client.get("/api/auth/logoutAll")
    assert resp.status_code == 200
    assert "Logged out from all devices" in resp.json()["message"]


def test_logout_all_no_cookie(client):
    resp = client.get("/api/auth/logoutAll")
    assert resp.status_code == 200


@patch("src.helpers.middlewares.rate_limiter.RateLimitMiddleware.dispatch", side_effect=lambda self, req, call_next: call_next(req))
@patch("src.controllers.auth_controller.email_service.send_password_reset_email", new_callable=AsyncMock, return_value=True)
def test_forgot_password(mock_email, _mock_rl, client):
    client.post("/api/auth/sign-up", json={"email": "fp@test.com", "name": "FP", "password": "password123"})
    resp = client.post("/api/auth/forgot-password", json={"email": "fp@test.com"})
    assert resp.status_code == 200
    mock_email.assert_called_once()


def test_forgot_password_unknown_email(client):
    resp = client.post("/api/auth/forgot-password", json={"email": "unknown@test.com"})
    assert resp.status_code == 200


@patch("src.helpers.middlewares.rate_limiter.RateLimitMiddleware.dispatch", side_effect=lambda self, req, call_next: call_next(req))
@patch("src.controllers.auth_controller.email_service.send_password_reset_email", new_callable=AsyncMock, return_value=True)
def test_restore_password(mock_email, _mock_rl, client):
    client.post("/api/auth/sign-up", json={"email": "rp@test.com", "name": "RP", "password": "password123"})
    client.post("/api/auth/forgot-password", json={"email": "rp@test.com"})
    code = mock_email.call_args.kwargs["reset_code"]
    resp = client.post("/api/auth/restore-password", json={"reset_code": code, "new_password": "newpass456"})
    assert resp.status_code == 200
    login = client.post("/api/auth/sign-in", json={"email": "rp@test.com", "password": "newpass456"})
    assert login.status_code == 200


def test_restore_password_invalid_code(client):
    resp = client.post("/api/auth/restore-password", json={"reset_code": "000000", "new_password": "newpass456"})
    assert resp.status_code == 400
