from sqlalchemy import inspect
from src.db.database import Base, engine


def test_create_all_creates_expenses_table():
    Base.metadata.drop_all(bind=engine)
    import src.models.expense_models  # noqa: F401
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    assert "expenses" in inspector.get_table_names()
