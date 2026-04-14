from datetime import datetime, timezone
from sqlalchemy.orm import Session
from src.models.reset_code_models import ResetCode


def insert_reset_code(db: Session, code: str, user_id: int, expires_at: datetime) -> ResetCode:
    rc = ResetCode(code=code, user_id=user_id, expires_at=expires_at)
    db.add(rc)
    db.commit()
    db.refresh(rc)
    return rc


def select_reset_code(db: Session, code: str) -> ResetCode | None:
    rc = db.query(ResetCode).filter(ResetCode.code == code).first()
    if not rc:
        return None
    if rc.used:
        return None
    expires_at = rc.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at <= datetime.now(timezone.utc):
        db.delete(rc)
        db.commit()
        return None
    return rc


def mark_code_used(db: Session, rc: ResetCode) -> None:
    rc.used = True
    db.commit()


def delete_user_reset_codes(db: Session, user_id: int) -> int:
    count = db.query(ResetCode).filter(ResetCode.user_id == user_id).delete()
    db.commit()
    return count


def delete_reset_code(db: Session, code_id: int) -> None:
    db.query(ResetCode).filter(ResetCode.id == code_id).delete()
    db.commit()


def delete_expired_codes(db: Session) -> int:
    count = db.query(ResetCode).filter(ResetCode.expires_at <= datetime.now(timezone.utc)).delete()
    db.commit()
    return count
