from sqlalchemy.orm import Session
from src.models.user_models import User


def insert_user(db: Session, email: str, name: str, hashed_password: str) -> User:
    user = User(email=email, name=name, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def select_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def select_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def update_user_password(db: Session, user_id: int, hashed_password: str) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    user.hashed_password = hashed_password
    db.commit()
    return True
