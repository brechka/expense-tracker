import secrets
from datetime import datetime, timedelta, timezone
from enum import Enum

import jwt
from passlib.context import CryptContext

from src.config import SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

_TOKEN_ISSUER = "expense-tracker"


def _jti() -> str:
    return secrets.token_hex(16)


class TokenError(Enum):
    EXPIRED = "expired"
    INVALID = "invalid"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
        {"sub": str(user_id), "exp": expire, "iat": now, "iss": _TOKEN_ISSUER, "jti": _jti()},
        SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


def create_refresh_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return jwt.encode(
        {"sub": str(user_id), "exp": expire, "iat": now, "iss": _TOKEN_ISSUER, "type": "refresh", "jti": _jti()},
        SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


def decode_token(token: str) -> tuple[int | None, TokenError | None]:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            issuer=_TOKEN_ISSUER,
            options={"require": ["exp", "iat", "iss", "sub"]},
        )
        if payload.get("type") == "refresh":
            return None, TokenError.INVALID
        return int(payload["sub"]), None
    except jwt.ExpiredSignatureError:
        return None, TokenError.EXPIRED
    except (jwt.InvalidTokenError, KeyError, ValueError):
        return None, TokenError.INVALID


def decode_refresh_token(token: str) -> tuple[int | None, TokenError | None]:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            issuer=_TOKEN_ISSUER,
            options={"require": ["exp", "iat", "iss", "sub"]},
        )
        if payload.get("type") != "refresh":
            return None, TokenError.INVALID
        return int(payload["sub"]), None
    except jwt.ExpiredSignatureError:
        return None, TokenError.EXPIRED
    except (jwt.InvalidTokenError, KeyError, ValueError):
        return None, TokenError.INVALID
