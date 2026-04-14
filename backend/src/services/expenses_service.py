from sqlalchemy.orm import Session
from src.db.expenses_repository import (
    insert_expense, select_all_expenses, select_expense_by_id,
    select_expenses_filtered, update_expense_by_id, delete_expense_by_id,
    reorder_expenses as repo_reorder,
)
from src.models.expense_models import Expense


def create_expense(db: Session, name: str, amount: float, currency: str, category: str, date: str, user_id: int) -> Expense:
    return insert_expense(db, name, amount, currency, category, date, user_id)


def list_expenses(db: Session, user_id: int) -> list[Expense]:
    return select_all_expenses(db, user_id)


def get_expense(db: Session, expense_id: int, user_id: int) -> Expense | None:
    return select_expense_by_id(db, expense_id, user_id)


def list_expenses_filtered(
    db: Session,
    user_id: int,
    limit: int | None = None,
    offset: int | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
) -> tuple[list[Expense], int]:
    return select_expenses_filtered(db, user_id, limit, offset, from_date, to_date)


def update_expense(db: Session, expense_id: int, user_id: int, updates: dict) -> Expense | None:
    return update_expense_by_id(db, expense_id, user_id, updates)


def delete_expense(db: Session, expense_id: int, user_id: int) -> bool:
    return delete_expense_by_id(db, expense_id, user_id)


def reorder_expenses(db: Session, user_id: int, expense_ids: list[int]) -> int:
    return repo_reorder(db, user_id, expense_ids)
