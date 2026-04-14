from src.services.auth_service import issue_tokens, rotate_refresh, revoke_refresh, revoke_all_user_tokens, cleanup_expired_refresh_tokens
from src.db.users_repository import insert_user
from src.db.refresh_token_repository import select_refresh_token, insert_refresh_token
from datetime import datetime, timedelta, timezone


def _make_user(db):
    return insert_user(db, "a@b.com", "Alice", "hashed")


def test_issue_tokens(db_session):
    user = _make_user(db_session)
    access, refresh = issue_tokens(db_session, user.id)
    assert access
    assert refresh
    assert select_refresh_token(db_session, refresh) is not None


def test_rotate_refresh(db_session):
    user = _make_user(db_session)
    _, old_refresh = issue_tokens(db_session, user.id)
    result = rotate_refresh(db_session, old_refresh)
    assert result is not None
    new_access, new_refresh = result
    assert new_access
    assert select_refresh_token(db_session, old_refresh) is None
    assert select_refresh_token(db_session, new_refresh) is not None


def test_rotate_refresh_invalid(db_session):
    assert rotate_refresh(db_session, "nonexistent") is None


def test_revoke_refresh(db_session):
    user = _make_user(db_session)
    _, refresh = issue_tokens(db_session, user.id)
    assert revoke_refresh(db_session, refresh)
    assert select_refresh_token(db_session, refresh) is None


def test_revoke_all_user_tokens(db_session):
    user = _make_user(db_session)
    issue_tokens(db_session, user.id)
    issue_tokens(db_session, user.id)
    assert revoke_all_user_tokens(db_session, user.id) == 2


def test_cleanup_expired_refresh_tokens(db_session):
    user = _make_user(db_session)
    old = datetime.now(timezone.utc) - timedelta(days=1)
    insert_refresh_token(db_session, "expired_tok", user.id, old)
    issue_tokens(db_session, user.id)
    assert cleanup_expired_refresh_tokens(db_session) == 1
