import io
from PIL import Image


def _make_jpeg(width=10, height=10) -> bytes:
    img = Image.new("RGB", (width, height), color="red")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def test_analyze_rejects_non_jpg(auth_client):
    resp = auth_client.post(
        "/api/invoices/analyze",
        files={"file": ("invoice.png", b"fakepng", "image/png")},
    )
    assert resp.status_code == 400
    assert "JPG" in resp.json()["detail"]


def test_analyze_rejects_wrong_extension(auth_client):
    resp = auth_client.post(
        "/api/invoices/analyze",
        files={"file": ("invoice.gif", b"fakegif", "image/jpeg")},
    )
    assert resp.status_code == 400
    assert "extension" in resp.json()["detail"]


def test_analyze_rejects_oversized(auth_client):
    big = b"\x00" * (5 * 1024 * 1024 + 1)
    resp = auth_client.post(
        "/api/invoices/analyze",
        files={"file": ("big.jpg", big, "image/jpeg")},
    )
    assert resp.status_code == 400
    assert "5 MB" in resp.json()["detail"]


def test_analyze_rejects_invalid_image(auth_client):
    resp = auth_client.post(
        "/api/invoices/analyze",
        files={"file": ("bad.jpg", b"not-a-real-jpeg", "image/jpeg")},
    )
    assert resp.status_code == 422
    assert "Invalid image" in resp.json()["detail"]


def test_analyze_valid_jpg_no_api_key(auth_client, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    jpg = _make_jpeg()
    resp = auth_client.post(
        "/api/invoices/analyze",
        files={"file": ("invoice.jpg", jpg, "image/jpeg")},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "name" in data
    assert "amount" in data
    assert "date" in data


def test_analyze_returns_correct_schema(auth_client, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    jpg = _make_jpeg()
    resp = auth_client.post(
        "/api/invoices/analyze",
        files={"file": ("receipt.jpeg", jpg, "image/jpeg")},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data["name"], str)
    assert isinstance(data["amount"], (int, float))
    assert isinstance(data["date"], str)
    assert data.get("currency") in (None, "USD", "EUR")


def test_analyze_unauthenticated(client):
    jpg = _make_jpeg()
    resp = client.post(
        "/api/invoices/analyze",
        files={"file": ("invoice.jpg", jpg, "image/jpeg")},
    )
    assert resp.status_code == 401
