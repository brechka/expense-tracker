from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from src.db.refresh_token_repository import (
    insert_refresh_token,
    select_refresh_token,
    delete_refresh_token,
    delete_all_user_refresh_tokens,
    delete_expired_refresh_tokens,
)
from src.helpers.security import create_access_token, create_refresh_token
from src.config import REFRESH_TOKEN_EXPIRE_DAYS


def issue_tokens(db: Session, user_id: int) -> tuple[str, str]:
    access = create_access_token(user_id)
    refresh = create_refresh_token(user_id)
    expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    insert_refresh_token(db, refresh, user_id, expires_at)
    return access, refresh


def rotate_refresh(db: Session, old_token: str) -> tuple[str, str] | None:
    stored = select_refresh_token(db, old_token)
    if not stored:
        return None
    user_id = stored.user_id
    delete_refresh_token(db, old_token)
    return issue_tokens(db, user_id)


def revoke_refresh(db: Session, token: str) -> bool:
    return delete_refresh_token(db, token)


def revoke_all_user_tokens(db: Session, user_id: int) -> int:
    return delete_all_user_refresh_tokens(db, user_id)


def cleanup_expired_refresh_tokens(db: Session) -> int:
    return delete_expired_refresh_tokens(db)
