from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from src.controllers.expenses_controller import router as expenses_router
from src.controllers.auth_controller import router as auth_router
from src.controllers.users_controller import router as users_router
from src.controllers.invoice_controller import router as invoice_router
from src.helpers.exception import AppException
from src.helpers.middlewares.error_handler import validation_exception_handler, app_exception_handler, generic_exception_handler
from src.helpers.middlewares.auth_middleware import AuthMiddleware
from src.helpers.middlewares.rate_limiter import RateLimitMiddleware
from src.helpers.middlewares.security_headers import SecurityHeadersMiddleware
from src.helpers.middlewares.request_logger import RequestLoggingMiddleware
from src.helpers.scheduler import start_cleanup_scheduler
from src.config import CORS_ORIGINS


@asynccontextmanager
async def lifespan(application: FastAPI):
    start_cleanup_scheduler()
    yield


app = FastAPI(title="Expense Tracker API", lifespan=lifespan)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.add_middleware(SecurityHeadersMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
    expose_headers=["Content-Length"],
    max_age=600,
)

app.add_middleware(RateLimitMiddleware)
app.add_middleware(AuthMiddleware)
app.add_middleware(RequestLoggingMiddleware)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(expenses_router)
app.include_router(invoice_router)


@app.get("/", include_in_schema=False)
def root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")


@app.get("/api/ping")
def ping():
    return {"message": "pong"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Expense Tracker API",
        version="1.0.0",
        description="API documentation with JWT Bearer authentication",
        routes=app.routes,
    )
    components = openapi_schema.setdefault("components", {})
    security_schemes = components.setdefault("securitySchemes", {})
    security_schemes["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    for path, methods in openapi_schema.get("paths", {}).items():
        if path.startswith("/api/users") or path.startswith("/api/expenses") or path.startswith("/api/invoices"):
            for method_obj in methods.values():
                method_obj.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

