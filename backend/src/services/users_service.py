from sqlalchemy.orm import Session
from src.db.users_repository import insert_user, select_user_by_email, select_user_by_id, update_user_password
from src.helpers.security import hash_password, verify_password
from src.models.user_models import User


def create_user(db: Session, email: str, name: str, password: str) -> User:
    hashed = hash_password(password)
    return insert_user(db, email, name, hashed)


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = select_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def get_user_by_email(db: Session, email: str) -> User | None:
    return select_user_by_email(db, email)


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return select_user_by_id(db, user_id)


def change_password(db: Session, user_id: int, new_password: str) -> bool:
    hashed = hash_password(new_password)
    return update_user_password(db, user_id, hashed)
