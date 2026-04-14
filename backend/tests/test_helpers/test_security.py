import time
from unittest.mock import patch
from src.helpers.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token, TokenError,
)


def test_hash_and_verify():
    hashed = hash_password("secret123")
    assert hashed != "secret123"
    assert verify_password("secret123", hashed)
    assert not verify_password("wrong", hashed)


def test_create_access_token_and_decode():
    token = create_access_token(42)
    user_id, error = decode_token(token)
    assert user_id == 42
    assert error is None


def test_create_refresh_token_and_decode():
    token = create_refresh_token(42)
    user_id, error = decode_token(token)
    assert user_id is None
    assert error == TokenError.INVALID


def test_decode_invalid_token():
    user_id, error = decode_token("garbage.token.here")
    assert user_id is None
    assert error == TokenError.INVALID


def test_decode_expired_token():
    with patch("src.helpers.security.ACCESS_TOKEN_EXPIRE_MINUTES", -1):
        token = create_access_token(42)
    time.sleep(0.1)
    user_id, error = decode_token(token)
    assert user_id is None
    assert error == TokenError.EXPIRED
