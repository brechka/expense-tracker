from src.db.database import engine, Base
import src.models.expense_models  # noqa: F401 - register models
import src.models.user_models  # noqa: F401 - register models
import src.models.refresh_token_models  # noqa: F401 - register models
import src.models.reset_code_models  # noqa: F401 - register models

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables created.")
