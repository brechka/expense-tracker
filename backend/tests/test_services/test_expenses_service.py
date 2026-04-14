import pytest
from src.services.expenses_service import (
    create_expense,
    list_expenses,
    get_expense,
    list_expenses_filtered,
    update_expense,
    delete_expense,
)
from src.models.user_models import User
from src.helpers.security import hash_password

USER_ID = None


@pytest.fixture(autouse=True)
def create_test_user(db_session):
    global USER_ID
    user = User(email="svc@test.com", name="Svc User", hashed_password=hash_password("password123"))
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    USER_ID = user.id


def test_create_expense_service(db_session):
    expense = create_expense(db_session, "Groceries", 50.0, "USD", "Food", "2024-02-01", USER_ID)
    assert expense.id is not None
    assert expense.name == "Groceries"
    assert expense.amount == 50.0
    assert expense.currency == "USD"
    assert expense.category == "Food"
    assert expense.date == "2024-02-01"


def test_list_expenses_service_empty(db_session):
    result = list_expenses(db_session, USER_ID)
    assert result == []


def test_list_expenses_service(db_session):
    create_expense(db_session, "A", 1.0, "USD", "Food", "2024-01-01", USER_ID)
    create_expense(db_session, "B", 2.0, "USD", "Food", "2024-02-01", USER_ID)
    result = list_expenses(db_session, USER_ID)
    assert len(result) == 2


def test_list_expenses_service_ordered_by_display_order(db_session):
    create_expense(db_session, "Old", 1.0, "USD", "Food", "2024-01-01", USER_ID)
    create_expense(db_session, "New", 2.0, "USD", "Food", "2024-06-01", USER_ID)
    result = list_expenses(db_session, USER_ID)
    # Sorted by display_order ascending — newest inserted comes first
    assert result[0].name == "New"
    assert result[1].name == "Old"


def test_get_expense_service_found(db_session):
    created = create_expense(db_session, "Gym", 30.0, "EUR", "Health", "2024-04-01", USER_ID)
    found = get_expense(db_session, created.id, USER_ID)
    assert found is not None
    assert found.name == "Gym"
    assert found.id == created.id


def test_get_expense_service_not_found(db_session):
    result = get_expense(db_session, 9999, USER_ID)
    assert result is None


def test_list_expenses_filtered_service_from_date(db_session):
    create_expense(db_session, "A", 1.0, "USD", "Food", "2024-01-01", USER_ID)
    create_expense(db_session, "B", 2.0, "USD", "Food", "2024-06-01", USER_ID)
    expenses, total = list_expenses_filtered(db_session, USER_ID, from_date="2024-03-01")
    assert len(expenses) == 1
    assert total == 1
    assert expenses[0].name == "B"


def test_list_expenses_filtered_service_to_date(db_session):
    create_expense(db_session, "A", 1.0, "USD", "Food", "2024-01-01", USER_ID)
    create_expense(db_session, "B", 2.0, "USD", "Food", "2024-06-01", USER_ID)
    expenses, total = list_expenses_filtered(db_session, USER_ID, to_date="2024-03-01")
    assert len(expenses) == 1
    assert total == 1
    assert expenses[0].name == "A"


def test_list_expenses_filtered_service_pagination(db_session):
    for i in range(5):
        create_expense(db_session, f"E{i}", 1.0, "USD", "Food", f"2024-01-{10+i:02d}", USER_ID)
    expenses, total = list_expenses_filtered(db_session, USER_ID, limit=2, offset=0)
    assert len(expenses) == 2
    assert total == 5


def test_update_expense_service(db_session):
    created = create_expense(db_session, "Gym", 30.0, "EUR", "Health", "2024-04-01", USER_ID)
    updated = update_expense(db_session, created.id, USER_ID, {"name": "Yoga"})
    assert updated is not None
    assert updated.name == "Yoga"
    assert updated.amount == 30.0


def test_update_expense_service_multiple_fields(db_session):
    created = create_expense(db_session, "Gym", 30.0, "EUR", "Health", "2024-04-01", USER_ID)
    updated = update_expense(db_session, created.id, USER_ID, {"name": "Yoga", "amount": 15.0, "currency": "USD"})
    assert updated.name == "Yoga"
    assert updated.amount == 15.0
    assert updated.currency == "USD"
    assert updated.category == "Health"


def test_update_expense_service_not_found(db_session):
    result = update_expense(db_session, 9999, USER_ID, {"name": "X"})
    assert result is None


def test_delete_expense_service(db_session):
    created = create_expense(db_session, "Gym", 30.0, "EUR", "Health", "2024-04-01", USER_ID)
    assert delete_expense(db_session, created.id, USER_ID) is True
    assert get_expense(db_session, created.id, USER_ID) is None


def test_delete_expense_service_not_found(db_session):
    assert delete_expense(db_session, 9999, USER_ID) is False


def test_delete_then_list(db_session):
    e1 = create_expense(db_session, "A", 1.0, "USD", "Food", "2024-01-01", USER_ID)
    create_expense(db_session, "B", 2.0, "USD", "Food", "2024-02-01", USER_ID)
    delete_expense(db_session, e1.id, USER_ID)
    result = list_expenses(db_session, USER_ID)
    assert len(result) == 1
    assert result[0].name == "B"


def test_reorder_expenses_service(db_session):
    from src.services.expenses_service import reorder_expenses
    e1 = create_expense(db_session, "A", 1.0, "USD", "Food", "2024-01-01", USER_ID)
    e2 = create_expense(db_session, "B", 2.0, "USD", "Food", "2024-02-01", USER_ID)
    updated = reorder_expenses(db_session, USER_ID, [e2.id, e1.id])
    assert updated == 2
    result = list_expenses(db_session, USER_ID)
    assert result[0].name == "B"
    assert result[1].name == "A"
