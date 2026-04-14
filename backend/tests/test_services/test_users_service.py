from src.services.users_service import create_user, authenticate_user, get_user_by_email, get_user_by_id, change_password


def test_create_user(db_session):
    user = create_user(db_session, "a@b.com", "Alice", "password123")
    assert user.id is not None
    assert user.email == "a@b.com"
    assert user.hashed_password != "password123"


def test_authenticate_user_success(db_session):
    create_user(db_session, "a@b.com", "Alice", "password123")
    user = authenticate_user(db_session, "a@b.com", "password123")
    assert user is not None
    assert user.email == "a@b.com"


def test_authenticate_user_wrong_password(db_session):
    create_user(db_session, "a@b.com", "Alice", "password123")
    assert authenticate_user(db_session, "a@b.com", "wrong") is None


def test_authenticate_user_no_user(db_session):
    assert authenticate_user(db_session, "missing@b.com", "password123") is None


def test_get_user_by_email(db_session):
    create_user(db_session, "a@b.com", "Alice", "password123")
    assert get_user_by_email(db_session, "a@b.com") is not None
    assert get_user_by_email(db_session, "missing@b.com") is None


def test_get_user_by_id(db_session):
    user = create_user(db_session, "a@b.com", "Alice", "password123")
    assert get_user_by_id(db_session, user.id) is not None
    assert get_user_by_id(db_session, 9999) is None


def test_change_password(db_session):
    user = create_user(db_session, "a@b.com", "Alice", "password123")
    assert change_password(db_session, user.id, "newpass456")
    assert authenticate_user(db_session, "a@b.com", "newpass456") is not None
    assert authenticate_user(db_session, "a@b.com", "password123") is None


def test_change_password_not_found(db_session):
    assert not change_password(db_session, 9999, "newpass456")
