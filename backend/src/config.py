import os
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")
ENV = os.getenv("ENV", "development")
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
LOG_FILE = os.getenv("LOG_FILE", "app.log")

# Database — use DATABASE_URL directly, or build from Postgres env vars
_pg_server = os.getenv("POSTGRES_SERVER")
if os.getenv("DATABASE_URL"):
    DATABASE_URL = os.getenv("DATABASE_URL")
elif _pg_server:
    _pg_user = os.getenv("POSTGRES_USER", "postgres")
    _pg_pass = os.getenv("POSTGRES_PASSWORD", "")
    _pg_port = os.getenv("POSTGRES_PORT", "5432")
    _pg_db = os.getenv("POSTGRES_DB", "app")
    DATABASE_URL = f"postgresql+psycopg2://{_pg_user}:{_pg_pass}@{_pg_server}:{_pg_port}/{_pg_db}"
else:
    DATABASE_URL = "sqlite:///expenses.db"

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
if SECRET_KEY == "dev-secret-key-change-in-production" and ENVIRONMENT != "local":
    raise ValueError(
        'SECRET_KEY is set to the default value. '
        'For security, please change it for non-local deployments.'
    )

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

SMTP_SERVER = os.getenv("SMTP_SERVER", os.getenv("SMTP_HOST", "localhost"))
SMTP_PORT = int(os.getenv("SMTP_PORT", "1025"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_SENDER_NAME = os.getenv("SMTP_SENDER_NAME", "Expense Tracker")

FRONTEND_URL = os.getenv("FRONTEND_URL", os.getenv("FRONTEND_HOST", "http://localhost:3000"))

SENTRY_DSN = os.getenv("SENTRY_DSN", "")
