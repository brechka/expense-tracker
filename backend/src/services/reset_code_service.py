import secrets
import string
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from src.db.reset_code_repository import (
    insert_reset_code,
    select_reset_code,
    mark_code_used,
    delete_user_reset_codes,
    delete_reset_code,
    delete_expired_codes,
)
from src.models.reset_code_models import ResetCode
from src.helpers.logger import logger
from src.config import FRONTEND_URL

RESET_CODE_LENGTH = 6
RESET_CODE_EXPIRE_MINUTES = 10


def generate_code() -> str:
    return "".join(secrets.choice(string.digits) for _ in range(RESET_CODE_LENGTH))


def create_reset_code(db: Session, user_id: int) -> str:
    delete_user_reset_codes(db, user_id)
    code = generate_code()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=RESET_CODE_EXPIRE_MINUTES)
    insert_reset_code(db, code, user_id, expires_at)
    logger.info("Reset code created for user %s", user_id)
    return code


def validate_reset_code(db: Session, code: str) -> ResetCode | None:
    return select_reset_code(db, code)


def consume_reset_code(db: Session, rc: ResetCode) -> None:
    delete_reset_code(db, rc.id)
    logger.info("Reset code consumed and removed for user %s", rc.user_id)


def cleanup_expired_codes(db: Session) -> int:
    count = delete_expired_codes(db)
    if count:
        logger.info("Cleaned up %d expired reset codes", count)
    return count


def generate_reset_link(code: str) -> str:
    return f"{FRONTEND_URL}/auth/restore-password?code={code}"
