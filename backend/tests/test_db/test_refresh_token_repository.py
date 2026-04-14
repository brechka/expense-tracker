from datetime import datetime, timedelta, timezone
from src.db.refresh_token_repository import (
    insert_refresh_token, select_refresh_token, delete_refresh_token,
    delete_all_user_refresh_tokens, delete_expired_refresh_tokens,
)
from src.db.users_repository import insert_user


def _make_user(db):
    return insert_user(db, "a@b.com", "Alice", "hashed")


def test_insert_and_select(db_session):
    user = _make_user(db_session)
    exp = datetime.now(timezone.utc) + timedelta(days=7)
    insert_refresh_token(db_session, "tok1", user.id, exp)
    assert select_refresh_token(db_session, "tok1") is not None


def test_select_expired(db_session):
    user = _make_user(db_session)
    exp = datetime.now(timezone.utc) - timedelta(seconds=1)
    insert_refresh_token(db_session, "tok_old", user.id, exp)
    assert select_refresh_token(db_session, "tok_old") is None


def test_select_not_found(db_session):
    assert select_refresh_token(db_session, "nonexistent") is None


def test_delete_refresh_token(db_session):
    user = _make_user(db_session)
    exp = datetime.now(timezone.utc) + timedelta(days=7)
    insert_refresh_token(db_session, "tok1", user.id, exp)
    assert delete_refresh_token(db_session, "tok1")
    assert select_refresh_token(db_session, "tok1") is None


def test_delete_refresh_token_not_found(db_session):
    assert not delete_refresh_token(db_session, "nonexistent")


def test_delete_all_user_tokens(db_session):
    user = _make_user(db_session)
    exp = datetime.now(timezone.utc) + timedelta(days=7)
    insert_refresh_token(db_session, "t1", user.id, exp)
    insert_refresh_token(db_session, "t2", user.id, exp)
    assert delete_all_user_refresh_tokens(db_session, user.id) == 2


def test_delete_expired_refresh_tokens(db_session):
    user = _make_user(db_session)
    old = datetime.now(timezone.utc) - timedelta(days=1)
    future = datetime.now(timezone.utc) + timedelta(days=7)
    insert_refresh_token(db_session, "old", user.id, old)
    insert_refresh_token(db_session, "fresh", user.id, future)
    assert delete_expired_refresh_tokens(db_session) == 1
    assert select_refresh_token(db_session, "fresh") is not None
