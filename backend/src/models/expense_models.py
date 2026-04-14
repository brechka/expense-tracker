from pydantic import BaseModel, field_validator
from sqlalchemy import Integer, String, Float, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.database import Base


class Expense(Base):
    __tablename__ = "expenses"
    __table_args__ = (
        Index("ix_expenses_user_order", "user_id", "display_order"),
        Index("ix_expenses_user_date", "user_id", "date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    display_order: Mapped[int | None] = mapped_column(Integer, nullable=True)

    owner = relationship("User", back_populates="expenses")


class ExpenseCreate(BaseModel):
    name: str
    amount: float
    currency: str
    category: str
    date: str

    @field_validator("name", "currency", "category", "date")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            msg = "Field must not be empty"
            raise ValueError(msg)
        return v.strip()

    @field_validator("amount")
    @classmethod
    def positive_amount(cls, v: float) -> float:
        if v <= 0:
            msg = "Amount must be positive"
            raise ValueError(msg)
        return v


class ExpenseUpdate(BaseModel):
    name: str | None = None
    amount: float | None = None
    currency: str | None = None
    category: str | None = None
    date: str | None = None

    @field_validator("name", "currency", "category", "date")
    @classmethod
    def not_empty(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            msg = "Field must not be empty"
            raise ValueError(msg)
        return v.strip() if v is not None else v

    @field_validator("amount")
    @classmethod
    def positive_amount(cls, v: float | None) -> float | None:
        if v is not None and v <= 0:
            msg = "Amount must be positive"
            raise ValueError(msg)
        return v


class ExpenseResponse(BaseModel):
    id: int
    name: str
    amount: float
    currency: str
    category: str
    date: str
    display_order: int | None = None

    model_config = {"from_attributes": True}


class ExpenseListResponse(BaseModel):
    data: list[ExpenseResponse]
    total: int
    limit: int | None = None
    offset: int | None = None


class ReorderRequest(BaseModel):
    expense_ids: list[int]
