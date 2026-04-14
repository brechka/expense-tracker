import pytest
from pydantic import ValidationError
from src.models.reset_code_models import (
    ForgotPasswordRequest, RestorePasswordRequest,
    ForgotPasswordResponse, RestorePasswordResponse,
)


class TestForgotPasswordRequest:
    def test_valid(self):
        r = ForgotPasswordRequest(email="a@b.com")
        assert r.email == "a@b.com"

    def test_invalid_email(self):
        with pytest.raises(ValidationError):
            ForgotPasswordRequest(email="bad")


class TestRestorePasswordRequest:
    def test_valid(self):
        r = RestorePasswordRequest(reset_code="123456", new_password="newpass12")
        assert r.reset_code == "123456"

    def test_empty_code_raises(self):
        with pytest.raises(ValidationError):
            RestorePasswordRequest(reset_code="", new_password="newpass12")

    def test_whitespace_code_raises(self):
        with pytest.raises(ValidationError):
            RestorePasswordRequest(reset_code="   ", new_password="newpass12")

    def test_short_password_raises(self):
        with pytest.raises(ValidationError):
            RestorePasswordRequest(reset_code="123456", new_password="short")

    def test_strips_code(self):
        r = RestorePasswordRequest(reset_code="  123456  ", new_password="newpass12")
        assert r.reset_code == "123456"


class TestResponses:
    def test_forgot_password_response(self):
        r = ForgotPasswordResponse(message="sent")
        assert r.message == "sent"

    def test_restore_password_response(self):
        r = RestorePasswordResponse(message="done")
        assert r.message == "done"
