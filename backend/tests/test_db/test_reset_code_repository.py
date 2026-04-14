from datetime import datetime, timedelta, timezone
from src.db.reset_code_repository import (
    insert_reset_code, select_reset_code, mark_code_used,
    delete_user_reset_codes, delete_reset_code, delete_expired_codes,
)
from src.db.users_repository import insert_user


def _make_user(db):
    return insert_user(db, "a@b.com", "Alice", "hashed")


def test_insert_and_select(db_session):
    user = _make_user(db_session)
    exp = datetime.now(timezone.utc) + timedelta(minutes=10)
    insert_reset_code(db_session, "123456", user.id, exp)
    assert select_reset_code(db_session, "123456") is not None


def test_select_expired(db_session):
    user = _make_user(db_session)
    exp = datetime.now(timezone.utc) - timedelta(seconds=1)
    insert_reset_code(db_session, "old123", user.id, exp)
    assert select_reset_code(db_session, "old123") is None


def test_select_used(db_session):
    user = _make_user(db_session)
    exp = datetime.now(timezone.utc) + timedelta(minutes=10)
    rc = insert_reset_code(db_session, "used12", user.id, exp)
    mark_code_used(db_session, rc)
    assert select_reset_code(db_session, "used12") is None


def test_select_not_found(db_session):
    assert select_reset_code(db_session, "nonexistent") is None


def test_delete_user_reset_codes(db_session):
    user = _make_user(db_session)
    exp = datetime.now(timezone.utc) + timedelta(minutes=10)
    insert_reset_code(db_session, "c1", user.id, exp)
    insert_reset_code(db_session, "c2", user.id, exp)
    assert delete_user_reset_codes(db_session, user.id) == 2


def test_delete_reset_code(db_session):
    user = _make_user(db_session)
    exp = datetime.now(timezone.utc) + timedelta(minutes=10)
    rc = insert_reset_code(db_session, "del123", user.id, exp)
    delete_reset_code(db_session, rc.id)
    assert select_reset_code(db_session, "del123") is None


def test_delete_expired_codes(db_session):
    user = _make_user(db_session)
    old = datetime.now(timezone.utc) - timedelta(days=1)
    future = datetime.now(timezone.utc) + timedelta(minutes=10)
    insert_reset_code(db_session, "old", user.id, old)
    insert_reset_code(db_session, "fresh", user.id, future)
    assert delete_expired_codes(db_session) == 1
    assert select_reset_code(db_session, "fresh") is not None
