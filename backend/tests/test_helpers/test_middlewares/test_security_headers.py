def test_security_headers_present(client):
    resp = client.get("/api/ping")
    assert resp.headers["X-Content-Type-Options"] == "nosniff"
    assert resp.headers["X-Frame-Options"] == "DENY"
    assert resp.headers["X-XSS-Protection"] == "1; mode=block"
    assert "max-age" in resp.headers["Strict-Transport-Security"]
    assert resp.headers["Content-Security-Policy"] == "default-src 'self'"
    assert resp.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    assert resp.headers["Cache-Control"] == "no-store"


def test_security_headers_on_error_response(client):
    resp = client.get("/api/nonexistent")
    assert resp.headers["X-Content-Type-Options"] == "nosniff"
    assert resp.headers["X-Frame-Options"] == "DENY"
