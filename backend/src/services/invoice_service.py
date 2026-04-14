import io
import json
import base64
import os
from datetime import datetime

from fastapi import HTTPException, UploadFile
from PIL import Image

from src.helpers.logger import logger
from src.models.invoice_models import (
    InvoiceAnalysisResponse,
    MAX_FILE_SIZE,
    ALLOWED_CONTENT_TYPES,
    ALLOWED_EXTENSIONS,
)


def validate_file_format(file: UploadFile) -> None:
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file format. Only JPG files are allowed.")
    if not file.filename or not any(file.filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(status_code=400, detail="Invalid file extension. Only .jpg or .jpeg files are allowed.")


async def read_and_validate_size(file: UploadFile) -> bytes:
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size of 5 MB. Received: {len(contents) / 1024 / 1024:.2f} MB",
        )
    return contents


def parse_invoice_image(image_bytes: bytes) -> InvoiceAnalysisResponse:
    try:
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode != "RGB":
            image = image.convert("RGB")
        buf = io.BytesIO()
        image.save(buf, format="JPEG")
        image_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    except Exception as exc:
        logger.error("Failed to process image: %s", exc)
        raise HTTPException(status_code=422, detail="Invalid image file. Please ensure the file is a valid JPG image.")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not set — returning placeholder invoice data")
        return InvoiceAnalysisResponse(
            name="Invoice", amount=0.0, currency=None, date=datetime.now().strftime("%Y-%m-%d"),
        )

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                'Extract invoice data from this image and return ONLY a valid JSON object with these exact fields:\n'
                                '{"name": "company or merchant name", "amount": 0.00, "currency": "USD" or "EUR" or null, "date": "YYYY-MM-DD"}\n'
                                'If you cannot find a value, use null for optional fields or a reasonable default.'
                            ),
                        },
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
                    ],
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
        )
        parsed = json.loads(response.choices[0].message.content)
        logger.info("OpenAI extracted: %s", parsed)
    except Exception as exc:
        logger.error("OpenAI API call failed: %s", exc)
        raise HTTPException(status_code=422, detail="Failed to analyze invoice image. Please try again.")

    if not parsed.get("name"):
        parsed["name"] = "Invoice"
    if parsed.get("amount") is None:
        raise HTTPException(status_code=422, detail="Could not extract amount from invoice.")
    if not parsed.get("date"):
        parsed["date"] = datetime.now().strftime("%Y-%m-%d")
    if parsed.get("currency") not in (None, "USD", "EUR"):
        parsed["currency"] = None

    return InvoiceAnalysisResponse(**parsed)
