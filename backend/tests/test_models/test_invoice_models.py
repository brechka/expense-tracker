import pytest
from pydantic import ValidationError
from src.models.invoice_models import InvoiceAnalysisResponse, MAX_FILE_SIZE, ALLOWED_CONTENT_TYPES, ALLOWED_EXTENSIONS


def test_valid_response():
    r = InvoiceAnalysisResponse(name="Shop", amount=10.0, date="2024-01-01")
    assert r.name == "Shop"
    assert r.currency is None


def test_valid_with_currency():
    r = InvoiceAnalysisResponse(name="Shop", amount=10.0, currency="USD", date="2024-01-01")
    assert r.currency == "USD"


def test_invalid_currency():
    with pytest.raises(ValidationError):
        InvoiceAnalysisResponse(name="Shop", amount=10.0, currency="GBP", date="2024-01-01")


def test_constants():
    assert MAX_FILE_SIZE == 5 * 1024 * 1024
    assert "image/jpeg" in ALLOWED_CONTENT_TYPES
    assert ".jpg" in ALLOWED_EXTENSIONS
