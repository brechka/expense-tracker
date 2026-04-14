import pytest
from unittest.mock import patch, MagicMock
from src.helpers.email import EmailService


@pytest.fixture
def email_svc():
    return EmailService()


@pytest.mark.asyncio
async def test_send_email_success(email_svc):
    with patch.object(email_svc, "_send_smtp"):
        result = await email_svc.send_email("a@b.com", "Test", "<p>Hi</p>")
    assert result is True


@pytest.mark.asyncio
async def test_send_email_failure(email_svc):
    with patch.object(email_svc, "_send_smtp", side_effect=Exception("SMTP error")):
        result = await email_svc.send_email("a@b.com", "Test", "<p>Hi</p>")
    assert result is False


@pytest.mark.asyncio
async def test_send_password_reset_email(email_svc):
    with patch.object(email_svc, "_send_smtp"):
        result = await email_svc.send_password_reset_email(
            to_email="a@b.com", reset_code="123456",
            reset_link="http://localhost/reset", user_name="Alice",
        )
    assert result is True
