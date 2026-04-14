import pytest
from pydantic import ValidationError
from src.models.expense_models import ExpenseCreate, ExpenseUpdate, ExpenseResponse, ExpenseListResponse


class TestExpenseCreate:
    def test_valid(self):
        e = ExpenseCreate(name="Lunch", amount=10.0, currency="USD", category="Food", date="2024-01-01")
        assert e.name == "Lunch"
        assert e.amount == 10.0

    def test_strips_whitespace(self):
        e = ExpenseCreate(name="  Lunch  ", amount=5.0, currency=" USD ", category=" Food ", date=" 2024-01-01 ")
        assert e.name == "Lunch"
        assert e.currency == "USD"
        assert e.category == "Food"
        assert e.date == "2024-01-01"

    def test_empty_name_raises(self):
        with pytest.raises(ValidationError):
            ExpenseCreate(name="", amount=10.0, currency="USD", category="Food", date="2024-01-01")

    def test_empty_currency_raises(self):
        with pytest.raises(ValidationError):
            ExpenseCreate(name="Lunch", amount=10.0, currency="", category="Food", date="2024-01-01")

    def test_empty_category_raises(self):
        with pytest.raises(ValidationError):
            ExpenseCreate(name="Lunch", amount=10.0, currency="USD", category="", date="2024-01-01")

    def test_empty_date_raises(self):
        with pytest.raises(ValidationError):
            ExpenseCreate(name="Lunch", amount=10.0, currency="USD", category="Food", date="")

    def test_whitespace_only_name_raises(self):
        with pytest.raises(ValidationError):
            ExpenseCreate(name="   ", amount=10.0, currency="USD", category="Food", date="2024-01-01")

    def test_zero_amount_raises(self):
        with pytest.raises(ValidationError):
            ExpenseCreate(name="Lunch", amount=0, currency="USD", category="Food", date="2024-01-01")

    def test_negative_amount_raises(self):
        with pytest.raises(ValidationError):
            ExpenseCreate(name="Lunch", amount=-5.0, currency="USD", category="Food", date="2024-01-01")

    def test_missing_fields_raises(self):
        with pytest.raises(ValidationError):
            ExpenseCreate(name="Lunch")


class TestExpenseUpdate:
    def test_all_none_by_default(self):
        e = ExpenseUpdate()
        assert e.name is None
        assert e.amount is None
        assert e.currency is None
        assert e.category is None
        assert e.date is None

    def test_partial_fields(self):
        e = ExpenseUpdate(name="Dinner", amount=20.0)
        assert e.name == "Dinner"
        assert e.amount == 20.0
        assert e.currency is None

    def test_strips_whitespace(self):
        e = ExpenseUpdate(name="  Dinner  ", currency=" EUR ")
        assert e.name == "Dinner"
        assert e.currency == "EUR"

    def test_empty_name_raises(self):
        with pytest.raises(ValidationError):
            ExpenseUpdate(name="")

    def test_whitespace_only_name_raises(self):
        with pytest.raises(ValidationError):
            ExpenseUpdate(name="   ")

    def test_empty_currency_raises(self):
        with pytest.raises(ValidationError):
            ExpenseUpdate(currency="")

    def test_empty_category_raises(self):
        with pytest.raises(ValidationError):
            ExpenseUpdate(category="")

    def test_empty_date_raises(self):
        with pytest.raises(ValidationError):
            ExpenseUpdate(date="")

    def test_zero_amount_raises(self):
        with pytest.raises(ValidationError):
            ExpenseUpdate(amount=0)

    def test_negative_amount_raises(self):
        with pytest.raises(ValidationError):
            ExpenseUpdate(amount=-1.0)

    def test_exclude_unset(self):
        e = ExpenseUpdate(name="X")
        dumped = e.model_dump(exclude_unset=True)
        assert dumped == {"name": "X"}

    def test_exclude_unset_empty(self):
        e = ExpenseUpdate()
        dumped = e.model_dump(exclude_unset=True)
        assert dumped == {}


class TestExpenseResponse:
    def test_from_dict(self):
        r = ExpenseResponse(id=1, name="Lunch", amount=10.0, currency="USD", category="Food", date="2024-01-01")
        assert r.id == 1
        assert r.name == "Lunch"

    def test_from_attributes(self):
        class FakeORM:
            id = 1
            name = "Lunch"
            amount = 10.0
            currency = "USD"
            category = "Food"
            date = "2024-01-01"

        r = ExpenseResponse.model_validate(FakeORM())
        assert r.id == 1
        assert r.amount == 10.0

    def test_all_fields_present(self):
        r = ExpenseResponse(id=5, name="Bus", amount=2.5, currency="EUR", category="Transport", date="2024-06-01")
        assert r.id == 5
        assert r.name == "Bus"
        assert r.amount == 2.5
        assert r.currency == "EUR"
        assert r.category == "Transport"
        assert r.date == "2024-06-01"


class TestExpenseListResponse:
    def test_with_data(self):
        item = ExpenseResponse(id=1, name="A", amount=1.0, currency="USD", category="Food", date="2024-01-01")
        r = ExpenseListResponse(data=[item], total=1, limit=10, offset=0)
        assert len(r.data) == 1
        assert r.total == 1
        assert r.limit == 10
        assert r.offset == 0

    def test_empty_data(self):
        r = ExpenseListResponse(data=[], total=0)
        assert r.data == []
        assert r.total == 0
        assert r.limit is None
        assert r.offset is None

    def test_limit_offset_optional(self):
        r = ExpenseListResponse(data=[], total=0, limit=None, offset=None)
        assert r.limit is None
        assert r.offset is None
