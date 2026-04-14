import io
import pytest
from unittest.mock import MagicMock, AsyncMock
from fastapi import HTTPException
from PIL import Image

from src.services.invoice_service import validate_file_format, read_and_validate_size, parse_invoice_image


def _make_jpeg(width=10, height=10) -> bytes:
    img = Image.new("RGB", (width, height), color="red")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def _mock_upload(filename="invoice.jpg", content_type="image/jpeg"):
    f = MagicMock()
    f.filename = filename
    f.content_type = content_type
    return f


def test_validate_file_format_valid():
    validate_file_format(_mock_upload("test.jpg", "image/jpeg"))
    validate_file_format(_mock_upload("test.jpeg", "image/jpeg"))


def test_validate_file_format_invalid_content_type():
    with pytest.raises(HTTPException) as exc:
        validate_file_format(_mock_upload("test.jpg", "image/png"))
    assert exc.value.status_code == 400


def test_validate_file_format_invalid_extension():
    with pytest.raises(HTTPException) as exc:
        validate_file_format(_mock_upload("test.gif", "image/jpeg"))
    assert exc.value.status_code == 400


def test_validate_file_format_no_filename():
    f = _mock_upload()
    f.filename = None
    with pytest.raises(HTTPException):
        validate_file_format(f)


@pytest.mark.asyncio
async def test_read_and_validate_size_ok():
    f = MagicMock()
    f.read = AsyncMock(return_value=b"x" * 100)
    result = await read_and_validate_size(f)
    assert len(result) == 100


@pytest.mark.asyncio
async def test_read_and_validate_size_too_large():
    f = MagicMock()
    f.read = AsyncMock(return_value=b"x" * (5 * 1024 * 1024 + 1))
    with pytest.raises(HTTPException) as exc:
        await read_and_validate_size(f)
    assert exc.value.status_code == 400


def test_parse_invoice_image_no_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    jpg = _make_jpeg()
    result = parse_invoice_image(jpg)
    assert result.name == "Invoice"
    assert result.amount == 0.0
    assert result.date


def test_parse_invoice_image_invalid_bytes():
    with pytest.raises(HTTPException) as exc:
        parse_invoice_image(b"not-a-real-image")
    assert exc.value.status_code == 422
