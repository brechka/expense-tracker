from src.db.users_repository import insert_user, select_user_by_email, select_user_by_id, update_user_password


def test_insert_user(db_session):
    user = insert_user(db_session, "a@b.com", "Alice", "hashed123")
    assert user.id is not None
    assert user.email == "a@b.com"
    assert user.name == "Alice"


def test_select_user_by_email_found(db_session):
    insert_user(db_session, "a@b.com", "Alice", "hashed123")
    user = select_user_by_email(db_session, "a@b.com")
    assert user is not None
    assert user.email == "a@b.com"


def test_select_user_by_email_not_found(db_session):
    assert select_user_by_email(db_session, "missing@b.com") is None


def test_select_user_by_id_found(db_session):
    created = insert_user(db_session, "a@b.com", "Alice", "hashed123")
    user = select_user_by_id(db_session, created.id)
    assert user is not None
    assert user.id == created.id


def test_select_user_by_id_not_found(db_session):
    assert select_user_by_id(db_session, 9999) is None


def test_update_user_password(db_session):
    user = insert_user(db_session, "a@b.com", "Alice", "old_hash")
    assert update_user_password(db_session, user.id, "new_hash")
    db_session.refresh(user)
    assert user.hashed_password == "new_hash"


def test_update_user_password_not_found(db_session):
    assert not update_user_password(db_session, 9999, "new_hash")
