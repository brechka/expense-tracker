import pytest
from pydantic import ValidationError
from src.models.user_models import UserCreate, UserLogin, UserResponse, TokenResponse, MessageResponse


class TestUserCreate:
    def test_valid(self):
        u = UserCreate(email="a@b.com", name="Alice", password="password123")
        assert u.email == "a@b.com"
        assert u.name == "Alice"

    def test_strips_name(self):
        u = UserCreate(email="a@b.com", name="  Alice  ", password="password123")
        assert u.name == "Alice"

    def test_empty_name_raises(self):
        with pytest.raises(ValidationError):
            UserCreate(email="a@b.com", name="", password="password123")

    def test_whitespace_name_raises(self):
        with pytest.raises(ValidationError):
            UserCreate(email="a@b.com", name="   ", password="password123")

    def test_short_password_raises(self):
        with pytest.raises(ValidationError):
            UserCreate(email="a@b.com", name="Alice", password="short")

    def test_invalid_email_raises(self):
        with pytest.raises(ValidationError):
            UserCreate(email="not-an-email", name="Alice", password="password123")


class TestUserLogin:
    def test_valid(self):
        u = UserLogin(email="a@b.com", password="password123")
        assert u.email == "a@b.com"

    def test_invalid_email_raises(self):
        with pytest.raises(ValidationError):
            UserLogin(email="bad", password="password123")


class TestUserResponse:
    def test_from_dict(self):
        r = UserResponse(id=1, email="a@b.com", name="Alice")
        assert r.id == 1

    def test_from_attributes(self):
        class FakeORM:
            id = 1
            email = "a@b.com"
            name = "Alice"
        r = UserResponse.model_validate(FakeORM())
        assert r.email == "a@b.com"


class TestTokenResponse:
    def test_defaults(self):
        t = TokenResponse(access_token="abc")
        assert t.token_type == "bearer"


class TestMessageResponse:
    def test_message(self):
        m = MessageResponse(message="ok")
        assert m.message == "ok"
