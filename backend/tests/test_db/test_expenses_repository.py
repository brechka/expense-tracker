import pytest
from src.db.expenses_repository import (
    insert_expense,
    select_all_expenses,
    select_expense_by_id,
    select_expenses_filtered,
    update_expense_by_id,
    delete_expense_by_id,
    reorder_expenses,
)
from src.models.user_models import User
from src.helpers.security import hash_password

USER_ID = None


@pytest.fixture(autouse=True)
def create_test_user(db_session):
    global USER_ID
    user = User(email="repo@test.com", name="Repo User", hashed_password=hash_password("password123"))
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    USER_ID = user.id


def test_insert_expense(db_session):
    expense = insert_expense(db_session, "Coffee", 4.5, "USD", "Drinks", "2024-01-10", USER_ID)
    assert expense.id is not None
    assert expense.name == "Coffee"
    assert expense.amount == 4.5
    assert expense.currency == "USD"
    assert expense.category == "Drinks"
    assert expense.date == "2024-01-10"


def test_insert_multiple_expenses_unique_ids(db_session):
    e1 = insert_expense(db_session, "A", 1.0, "USD", "Food", "2024-01-01", USER_ID)
    e2 = insert_expense(db_session, "B", 2.0, "USD", "Food", "2024-01-02", USER_ID)
    assert e1.id != e2.id


def test_select_all_expenses_empty(db_session):
    result = select_all_expenses(db_session, USER_ID)
    assert result == []


def test_select_all_expenses_ordered_by_display_order(db_session):
    insert_expense(db_session, "Old", 1.0, "USD", "Food", "2024-01-01", USER_ID)
    insert_expense(db_session, "New", 2.0, "USD", "Food", "2024-06-01", USER_ID)
    result = select_all_expenses(db_session, USER_ID)
    assert len(result) == 2
    # Sorted by display_order ascending — newest inserted comes first
    assert result[0].name == "New"
    assert result[1].name == "Old"
    assert result[0].display_order < result[1].display_order


def test_select_expense_by_id_found(db_session):
    created = insert_expense(db_session, "Taxi", 15.0, "EUR", "Transport", "2024-03-01", USER_ID)
    found = select_expense_by_id(db_session, created.id, USER_ID)
    assert found is not None
    assert found.id == created.id
    assert found.name == "Taxi"


def test_select_expense_by_id_not_found(db_session):
    result = select_expense_by_id(db_session, 9999, USER_ID)
    assert result is None


def test_select_expenses_filtered_no_filters(db_session):
    insert_expense(db_session, "A", 1.0, "USD", "Food", "2024-01-01", USER_ID)
    insert_expense(db_session, "B", 2.0, "USD", "Food", "2024-02-01", USER_ID)
    expenses, total = select_expenses_filtered(db_session, USER_ID)
    assert len(expenses) == 2
    assert total == 2


def test_select_expenses_filtered_pagination(db_session):
    for i in range(5):
        insert_expense(db_session, f"E{i}", 1.0, "USD", "Food", f"2024-01-{10+i:02d}", USER_ID)
    expenses, total = select_expenses_filtered(db_session, USER_ID, limit=2, offset=1)
    assert len(expenses) == 2
    assert total == 5


def test_select_expenses_filtered_limit_only(db_session):
    for i in range(5):
        insert_expense(db_session, f"E{i}", 1.0, "USD", "Food", f"2024-01-{10+i:02d}", USER_ID)
    expenses, total = select_expenses_filtered(db_session, USER_ID, limit=3)
    assert len(expenses) == 3
    assert total == 5


def test_select_expenses_filtered_offset_only(db_session):
    for i in range(5):
        insert_expense(db_session, f"E{i}", 1.0, "USD", "Food", f"2024-01-{10+i:02d}", USER_ID)
    expenses, total = select_expenses_filtered(db_session, USER_ID, offset=3)
    assert len(expenses) == 2
    assert total == 5


def test_select_expenses_filtered_from_date(db_session):
    insert_expense(db_session, "Old", 1.0, "USD", "Food", "2024-01-01", USER_ID)
    insert_expense(db_session, "New", 2.0, "USD", "Food", "2024-06-01", USER_ID)
    expenses, total = select_expenses_filtered(db_session, USER_ID, from_date="2024-03-01")
    assert len(expenses) == 1
    assert total == 1
    assert expenses[0].name == "New"


def test_select_expenses_filtered_to_date(db_session):
    insert_expense(db_session, "Old", 1.0, "USD", "Food", "2024-01-01", USER_ID)
    insert_expense(db_session, "New", 2.0, "USD", "Food", "2024-06-01", USER_ID)
    expenses, total = select_expenses_filtered(db_session, USER_ID, to_date="2024-03-01")
    assert len(expenses) == 1
    assert total == 1
    assert expenses[0].name == "Old"


def test_select_expenses_filtered_date_range(db_session):
    insert_expense(db_session, "Old", 1.0, "USD", "Food", "2024-01-01", USER_ID)
    insert_expense(db_session, "Mid", 1.0, "USD", "Food", "2024-03-15", USER_ID)
    insert_expense(db_session, "New", 1.0, "USD", "Food", "2024-06-01", USER_ID)
    expenses, total = select_expenses_filtered(db_session, USER_ID, from_date="2024-02-01", to_date="2024-05-01")
    assert len(expenses) == 1
    assert total == 1
    assert expenses[0].name == "Mid"


def test_select_expenses_filtered_no_match(db_session):
    insert_expense(db_session, "A", 1.0, "USD", "Food", "2024-01-01", USER_ID)
    expenses, total = select_expenses_filtered(db_session, USER_ID, from_date="2025-01-01")
    assert len(expenses) == 0
    assert total == 0


def test_update_expense_by_id(db_session):
    created = insert_expense(db_session, "Taxi", 15.0, "EUR", "Transport", "2024-03-01", USER_ID)
    updated = update_expense_by_id(db_session, created.id, USER_ID, {"name": "Bus", "amount": 5.0})
    assert updated is not None
    assert updated.name == "Bus"
    assert updated.amount == 5.0
    assert updated.currency == "EUR"


def test_update_expense_by_id_single_field(db_session):
    created = insert_expense(db_session, "Taxi", 15.0, "EUR", "Transport", "2024-03-01", USER_ID)
    updated = update_expense_by_id(db_session, created.id, USER_ID, {"name": "Bus"})
    assert updated.name == "Bus"
    assert updated.amount == 15.0
    assert updated.currency == "EUR"
    assert updated.category == "Transport"
    assert updated.date == "2024-03-01"


def test_update_expense_by_id_persists(db_session):
    created = insert_expense(db_session, "Taxi", 15.0, "EUR", "Transport", "2024-03-01", USER_ID)
    update_expense_by_id(db_session, created.id, USER_ID, {"name": "Bus"})
    fetched = select_expense_by_id(db_session, created.id, USER_ID)
    assert fetched.name == "Bus"


def test_update_expense_by_id_not_found(db_session):
    result = update_expense_by_id(db_session, 9999, USER_ID, {"name": "X"})
    assert result is None


def test_delete_expense_by_id(db_session):
    created = insert_expense(db_session, "Taxi", 15.0, "EUR", "Transport", "2024-03-01", USER_ID)
    assert delete_expense_by_id(db_session, created.id, USER_ID) is True
    assert select_expense_by_id(db_session, created.id, USER_ID) is None


def test_delete_expense_by_id_not_found(db_session):
    assert delete_expense_by_id(db_session, 9999, USER_ID) is False


def test_delete_expense_does_not_affect_others(db_session):
    e1 = insert_expense(db_session, "A", 1.0, "USD", "Food", "2024-01-01", USER_ID)
    e2 = insert_expense(db_session, "B", 2.0, "USD", "Food", "2024-02-01", USER_ID)
    delete_expense_by_id(db_session, e1.id, USER_ID)
    assert select_expense_by_id(db_session, e2.id, USER_ID) is not None
    all_expenses = select_all_expenses(db_session, USER_ID)
    assert len(all_expenses) == 1


def test_reorder_expenses(db_session):
    e1 = insert_expense(db_session, "A", 1.0, "USD", "Food", "2024-01-01", USER_ID)
    e2 = insert_expense(db_session, "B", 2.0, "USD", "Food", "2024-02-01", USER_ID)
    e3 = insert_expense(db_session, "C", 3.0, "USD", "Food", "2024-03-01", USER_ID)
    # Reorder: C, A, B
    updated = reorder_expenses(db_session, USER_ID, [e3.id, e1.id, e2.id])
    assert updated == 3
    result = select_all_expenses(db_session, USER_ID)
    assert [r.name for r in result] == ["C", "A", "B"]


def test_insert_expense_sets_display_order(db_session):
    e1 = insert_expense(db_session, "A", 1.0, "USD", "Food", "2024-01-01", USER_ID)
    e2 = insert_expense(db_session, "B", 2.0, "USD", "Food", "2024-02-01", USER_ID)
    assert e1.display_order is not None
    assert e2.display_order is not None
    assert e2.display_order < e1.display_order
