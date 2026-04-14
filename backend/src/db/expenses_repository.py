from sqlalchemy import func
from sqlalchemy.orm import Session
from src.models.expense_models import Expense
from src.helpers.logger import logger


def _next_order(db: Session, user_id: int) -> int:
    min_order = db.query(func.min(Expense.display_order)).filter(Expense.user_id == user_id).scalar()
    return (min_order or 0) - 1


def insert_expense(db: Session, name: str, amount: float, currency: str, category: str, date: str, user_id: int) -> Expense:
    order = _next_order(db, user_id)
    expense = Expense(name=name, amount=amount, currency=currency, category=category, date=date, user_id=user_id, display_order=order)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    logger.debug("DB insert expense id=%s user=%s", expense.id, user_id)
    return expense


def select_all_expenses(db: Session, user_id: int) -> list[Expense]:
    result = (
        db.query(Expense)
        .filter(Expense.user_id == user_id)
        .order_by(Expense.display_order.asc().nullslast(), Expense.date.desc())
        .all()
    )
    logger.debug("DB select all expenses user=%s count=%d", user_id, len(result))
    return result


def select_expenses_filtered(
    db: Session,
    user_id: int,
    limit: int | None = None,
    offset: int | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
) -> tuple[list[Expense], int]:
    base = db.query(Expense).filter(Expense.user_id == user_id)
    if from_date:
        base = base.filter(Expense.date >= from_date)
    if to_date:
        base = base.filter(Expense.date <= to_date)

    # Single pass: get total from subquery
    total = base.count()

    query = base.order_by(Expense.display_order.asc().nullslast(), Expense.date.desc())
    if offset is not None:
        query = query.offset(offset)
    if limit is not None:
        query = query.limit(limit)
    result = query.all()
    logger.debug("DB select filtered expenses user=%s total=%d returned=%d", user_id, total, len(result))
    return result, total


def select_expense_by_id(db: Session, expense_id: int, user_id: int) -> Expense | None:
    result = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == user_id).first()
    logger.debug("DB select expense id=%s user=%s found=%s", expense_id, user_id, result is not None)
    return result


def update_expense_by_id(db: Session, expense_id: int, user_id: int, updates: dict) -> Expense | None:
    expense = select_expense_by_id(db, expense_id, user_id)
    if not expense:
        return None
    for key, value in updates.items():
        setattr(expense, key, value)
    db.commit()
    db.refresh(expense)
    logger.debug("DB update expense id=%s fields=%s", expense_id, list(updates.keys()))
    return expense


def delete_expense_by_id(db: Session, expense_id: int, user_id: int) -> bool:
    expense = select_expense_by_id(db, expense_id, user_id)
    if not expense:
        return False
    db.delete(expense)
    db.commit()
    logger.debug("DB delete expense id=%s user=%s", expense_id, user_id)
    return True


def reorder_expenses(db: Session, user_id: int, expense_ids: list[int]) -> int:
    """Batch reorder using individual updates within a single transaction."""
    if not expense_ids:
        return 0
    updated = 0
    for position, eid in enumerate(expense_ids):
        rows = (
            db.query(Expense)
            .filter(Expense.id == eid, Expense.user_id == user_id)
            .update({Expense.display_order: position}, synchronize_session="fetch")
        )
        updated += rows
    db.commit()
    logger.debug("DB reorder expenses user=%s updated=%d", user_id, updated)
    return updated
