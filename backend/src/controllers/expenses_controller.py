from fastapi import APIRouter, HTTPException, Depends, Query, Request
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.helpers.logger import logger
from src.models.expense_models import ExpenseCreate, ExpenseResponse, ExpenseListResponse, ExpenseUpdate, ReorderRequest
from src.services.expenses_service import create_expense, list_expenses_filtered, get_expense, update_expense, delete_expense, reorder_expenses

router = APIRouter(prefix="/api/expenses", tags=["expenses"])


def _get_user_id(request: Request) -> int:
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user_id


@router.post("/", response_model=ExpenseResponse, status_code=201)
def add_expense(request: Request, expense: ExpenseCreate, db: Session = Depends(get_db)):
    user_id = _get_user_id(request)
    result = create_expense(db, expense.name, expense.amount, expense.currency, expense.category, expense.date, user_id)
    logger.info("Expense created: id=%s name=%s amount=%s", result.id, result.name, result.amount)
    return result


@router.get("/", response_model=ExpenseListResponse)
def get_expenses(
    request: Request,
    limit: int | None = Query(None, ge=1),
    offset: int | None = Query(None, ge=0),
    fromDate: str | None = Query(None),
    toDate: str | None = Query(None),
    db: Session = Depends(get_db),
):
    user_id = _get_user_id(request)
    expenses, total = list_expenses_filtered(db, user_id, limit, offset, fromDate, toDate)
    return ExpenseListResponse(data=expenses, total=total, limit=limit, offset=offset)


@router.patch("/reorder", response_model=dict)
def reorder(request: Request, body: ReorderRequest, db: Session = Depends(get_db)):
    user_id = _get_user_id(request)
    if not body.expense_ids:
        raise HTTPException(status_code=400, detail="expense_ids must not be empty")
    updated = reorder_expenses(db, user_id, body.expense_ids)
    logger.info("Expenses reordered for user %s: %d updated", user_id, updated)
    return {"updated": updated}


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense_by_id(request: Request, expense_id: int, db: Session = Depends(get_db)):
    user_id = _get_user_id(request)
    expense = get_expense(db, expense_id, user_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.patch("/{expense_id}", response_model=ExpenseResponse)
def patch_expense(request: Request, expense_id: int, updates: ExpenseUpdate, db: Session = Depends(get_db)):
    user_id = _get_user_id(request)
    update_data = updates.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    expense = update_expense(db, expense_id, user_id, update_data)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    logger.info("Expense updated: id=%s fields=%s", expense_id, list(update_data.keys()))
    return expense


@router.delete("/{expense_id}", status_code=204)
def remove_expense(request: Request, expense_id: int, db: Session = Depends(get_db)):
    user_id = _get_user_id(request)
    if not delete_expense(db, expense_id, user_id):
        raise HTTPException(status_code=404, detail="Expense not found")
    logger.info("Expense deleted: id=%s", expense_id)
