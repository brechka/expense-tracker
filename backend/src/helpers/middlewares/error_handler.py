from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from src.helpers.logger import logger
from src.helpers.exception import AppException


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        {"field": ".".join(str(loc) for loc in e["loc"]), "message": e["msg"]}
        for e in exc.errors()
    ]
    logger.warning("Validation error on %s %s: %s", request.method, request.url.path, errors)
    return JSONResponse(status_code=422, content={"detail": "Validation error", "errors": errors})


async def app_exception_handler(request: Request, exc: AppException):
    logger.warning("App error on %s %s: %s", request.method, request.url.path, exc.message)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


async def generic_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled error on %s %s: %s", request.method, request.url.path, str(exc), exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
