import time
from collections import defaultdict, deque
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from src.helpers.logger import logger


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiter using sliding-window with deque for O(1) cleanup."""

    def __init__(
        self,
        app,
        rate_limit_prefixes: tuple[str, ...] = ("/api/auth/sign-in", "/api/auth/sign-up", "/api/auth/forgot-password", "/api/auth/restore-password"),
        max_requests: int = 10,
        window_seconds: int = 60,
        max_keys: int = 10000,
    ):
        super().__init__(app)
        self.rate_limit_prefixes = rate_limit_prefixes
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.max_keys = max_keys
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    def _clean(self, key: str, now: float) -> None:
        cutoff = now - self.window_seconds
        dq = self._hits[key]
        while dq and dq[0] <= cutoff:
            dq.popleft()

    def _evict_stale_keys(self, now: float) -> None:
        if len(self._hits) <= self.max_keys:
            return
        cutoff = now - self.window_seconds
        stale = [k for k, dq in self._hits.items() if not dq or dq[-1] <= cutoff]
        for k in stale:
            del self._hits[k]

    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path
        if not any(path.startswith(p) for p in self.rate_limit_prefixes):
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        key = f"{client_ip}:{path}"
        now = time.time()

        self._clean(key, now)
        self._evict_stale_keys(now)

        if len(self._hits[key]) >= self.max_requests:
            logger.warning("Rate limit exceeded: %s %s from %s", request.method, path, client_ip)
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Please try again later."},
                headers={"Retry-After": str(self.window_seconds)},
            )

        self._hits[key].append(now)
        return await call_next(request)

    def reset(self) -> None:
        self._hits.clear()
