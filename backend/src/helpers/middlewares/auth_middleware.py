from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.helpers.security import decode_token, TokenError
from src.helpers.logger import logger


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        protected_prefixes=("/api/expenses", "/api/users", "/api/invoices"),
        exclude_prefixes=("/api/auth", "/api/ping", "/docs", "/openapi.json", "/redoc"),
    ):
        super().__init__(app)
        self.protected_prefixes = tuple(protected_prefixes)
        self.exclude_prefixes = tuple(exclude_prefixes)

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.method.upper() == "OPTIONS":
            return await call_next(request)

        path = request.url.path
        method = request.method

        if any(path.startswith(p) for p in self.exclude_prefixes) or not any(
            path.startswith(p) for p in self.protected_prefixes
        ):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning(
                "Unauthorized: missing or malformed Authorization header | %s %s | client=%s",
                method, path, request.client.host if request.client else "unknown",
            )
            return JSONResponse(status_code=401, content={"detail": "Not authenticated"})

        token = auth_header.split(" ", 1)[1].strip()
        user_id, error = decode_token(token)

        if error == TokenError.EXPIRED:
            logger.warning(
                "Unauthorized: expired token | %s %s | client=%s",
                method, path, request.client.host if request.client else "unknown",
            )
            return JSONResponse(status_code=401, content={"detail": "Token has expired"})

        if error == TokenError.INVALID or user_id is None:
            logger.warning(
                "Unauthorized: invalid token | %s %s | client=%s",
                method, path, request.client.host if request.client else "unknown",
            )
            return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})

        request.state.user_id = user_id
        return await call_next(request)
