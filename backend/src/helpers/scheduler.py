import threading
import time
from src.db.database import SessionLocal
from src.services.reset_code_service import cleanup_expired_codes
from src.services.auth_service import cleanup_expired_refresh_tokens
from src.helpers.logger import logger

CLEANUP_INTERVAL_SECONDS = 7 * 24 * 60 * 60  # once a week


def _run_cleanup() -> None:
    while True:
        time.sleep(CLEANUP_INTERVAL_SECONDS)
        try:
            db = SessionLocal()
            try:
                rc_count = cleanup_expired_codes(db)
                rt_count = cleanup_expired_refresh_tokens(db)
                logger.info(
                    "Scheduled cleanup: removed %d expired reset codes, %d expired refresh tokens",
                    rc_count, rt_count,
                )
            finally:
                db.close()
        except Exception as e:
            logger.error("Scheduled cleanup failed: %s", e)


def start_cleanup_scheduler() -> None:
    thread = threading.Thread(target=_run_cleanup, daemon=True)
    thread.start()
    logger.info("Cleanup scheduler started (interval: weekly)")
