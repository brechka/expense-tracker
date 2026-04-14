from datetime import datetime, timezone
from sqlalchemy.orm import Session
from src.models.refresh_token_models import RefreshToken


def insert_refresh_token(db: Session, token: str, user_id: int, expires_at: datetime) -> RefreshToken:
    rt = RefreshToken(token=token, user_id=user_id, expires_at=expires_at)
    db.add(rt)
    db.commit()
    db.refresh(rt)
    return rt


def select_refresh_token(db: Session, token: str) -> RefreshToken | None:
    return db.query(RefreshToken).filter(
        RefreshToken.token == token,
        RefreshToken.expires_at > datetime.now(timezone.utc),
    ).first()


def delete_refresh_token(db: Session, token: str) -> bool:
    rt = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if not rt:
        return False
    db.delete(rt)
    db.commit()
    return True


def delete_all_user_refresh_tokens(db: Session, user_id: int) -> int:
    count = db.query(RefreshToken).filter(RefreshToken.user_id == user_id).delete()
    db.commit()
    return count


def delete_expired_refresh_tokens(db: Session) -> int:
    count = db.query(RefreshToken).filter(RefreshToken.expires_at <= datetime.now(timezone.utc)).delete()
    db.commit()
    return count
