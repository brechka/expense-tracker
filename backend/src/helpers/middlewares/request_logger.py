import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from src.helpers.logger import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs every API request with method, path, status code, and duration."""

    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "%s %s -> %d (%.1fms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response
