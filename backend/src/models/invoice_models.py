from typing import Literal
from pydantic import BaseModel

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_CONTENT_TYPES = ["image/jpeg", "image/jpg"]
ALLOWED_EXTENSIONS = [".jpg", ".jpeg"]


class InvoiceAnalysisResponse(BaseModel):
    name: str
    amount: float
    currency: Literal["USD", "EUR"] | None = None
    date: str
