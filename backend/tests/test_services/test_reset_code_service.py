from src.services.reset_code_service import (
    generate_code, create_reset_code, validate_reset_code,
    consume_reset_code, cleanup_expired_codes, generate_reset_link,
)
from src.db.users_repository import insert_user
from src.db.reset_code_repository import insert_reset_code
from datetime import datetime, timedelta, timezone


def _make_user(db):
    return insert_user(db, "rc@test.com", "RC User", "hashed")


def test_generate_code_length():
    code = generate_code()
    assert len(code) == 6
    assert code.isdigit()


def test_generate_code_unique():
    codes = {generate_code() for _ in range(50)}
    assert len(codes) > 1


def test_create_reset_code(db_session):
    user = _make_user(db_session)
    code = create_reset_code(db_session, user.id)
    assert len(code) == 6
    assert code.isdigit()


def test_create_reset_code_deletes_old(db_session):
    user = _make_user(db_session)
    code1 = create_reset_code(db_session, user.id)
    code2 = create_reset_code(db_session, user.id)
    assert code1 != code2
    assert validate_reset_code(db_session, code1) is None
    assert validate_reset_code(db_session, code2) is not None


def test_validate_reset_code_valid(db_session):
    user = _make_user(db_session)
    code = create_reset_code(db_session, user.id)
    rc = validate_reset_code(db_session, code)
    assert rc is not None
    assert rc.user_id == user.id


def test_validate_reset_code_invalid(db_session):
    assert validate_reset_code(db_session, "000000") is None


def test_consume_reset_code(db_session):
    user = _make_user(db_session)
    code = create_reset_code(db_session, user.id)
    rc = validate_reset_code(db_session, code)
    consume_reset_code(db_session, rc)
    assert validate_reset_code(db_session, code) is None


def test_cleanup_expired_codes(db_session):
    user = _make_user(db_session)
    old = datetime.now(timezone.utc) - timedelta(days=1)
    insert_reset_code(db_session, "old123", user.id, old)
    count = cleanup_expired_codes(db_session)
    assert count >= 1


def test_generate_reset_link():
    link = generate_reset_link("123456")
    assert "123456" in link
    assert "/auth/restore-password" in link
