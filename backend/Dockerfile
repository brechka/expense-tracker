# ---------- build stage ----------
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- runtime stage ----------
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Non-root user for security
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copy application code
COPY scripts/ ./scripts/
COPY alembic.ini .
COPY alembic/ ./alembic/
COPY src/ ./src/

# Make app dir writable for SQLite in dev mode
RUN chown -R appuser:appgroup /app

# Environment defaults (overridden at runtime via docker-compose or -e flags)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    ENV=production \
    PORT=8000 \
    HOST=0.0.0.0

EXPOSE 8000

# Switch to non-root user
USER appuser

# Production server with multiple workers
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
