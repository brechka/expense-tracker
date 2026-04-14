from fastapi import APIRouter, File, UploadFile

from src.models.invoice_models import InvoiceAnalysisResponse
from src.services.invoice_service import validate_file_format, read_and_validate_size, parse_invoice_image

router = APIRouter(prefix="/api/invoices", tags=["invoices"])


@router.post("/analyze", response_model=InvoiceAnalysisResponse)
async def analyze_invoice(file: UploadFile = File(...)):
    """
    Analyze a JPG invoice image (up to 5 MB) and extract expense data.
    The file is processed in memory and never saved to disk.
    """
    validate_file_format(file)
    contents = await read_and_validate_size(file)
    return parse_invoice_image(contents)
