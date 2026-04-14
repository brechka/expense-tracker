# Expense Tracker

Full-stack expense tracking application with React frontend and Python/FastAPI backend.

## Technology Stack

### Frontend — React
- React 18, TypeScript, Vite, React Router, react-hook-form, yup, axios
- CSS Modules, Storybook, vitest + Testing Library

### Backend — FastAPI
- Python 3.12, FastAPI, SQLAlchemy, Alembic, PyJWT, bcrypt, Pillow
- PostgreSQL (production) / SQLite (development)

### DevOps
- Docker, Docker Compose, Traefik (TLS), GitHub Actions CI/CD

## Quick Start

### Local Development

#### Backend

```bash
cd backend
pip install -r requirements.txt
python -m alembic upgrade head
python dev.py
```

Backend runs at http://localhost:8000 — API docs at http://localhost:8000/docs

#### Frontend

Requires Node.js 18+.

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:3000

### Docker Compose (alternative)

Requires [Docker](https://docs.docker.com/get-docker/) installed.

```bash
cp .env_template .env
# Edit .env — set SECRET_KEY, POSTGRES_PASSWORD, etc.
docker compose watch
```

Available services:

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| MailCatcher | http://localhost:1080 |

### Run Tests

```bash
# Backend (268 tests, 92% coverage)
cd backend
python -m pytest tests/ --cov=src --cov-fail-under=70 -q

# Frontend (44 tests)
cd frontend
npm run test
```

## Project Structure

```
exps-tracker/
├── backend/
│   ├── src/
│   │   ├── controllers/     # REST API endpoints
│   │   ├── services/        # Business logic
│   │   ├── db/              # Repositories & database config
│   │   ├── models/          # SQLAlchemy & Pydantic models
│   │   └── helpers/         # Middleware, utilities, logging
│   ├── tests/               # 268 tests, 92% coverage
│   ├── alembic/             # Database migrations
│   └── scripts/             # Dev/CI helper scripts
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Route pages
│   │   ├── routes/          # React Router config
│   │   ├── layouts/         # Page layouts
│   │   └── utils/           # API client, helpers
│   ├── tests/               # 44 tests (vitest + Testing Library)
│   └── .storybook/          # Storybook config
├── .github/workflows/       # CI/CD pipelines
└── docker-compose.yaml      # Docker Compose setup
```

## Architecture

The backend follows a layered architecture: Controllers → Services → Repositories → Database. Middleware handles auth (JWT), rate limiting, security headers, and request logging.

The frontend uses a component-based architecture with React Router for navigation, axios for API calls with automatic token refresh, and in-memory JWT storage (no localStorage).

Auth flow: email/password → JWT access token (30 min) + httpOnly refresh cookie (7 days). Tokens are rotated on refresh and revoked on logout.

## API Endpoints

### Authentication Endpoints
| Method | Path | Description | Auth | Request Body |
|--------|------|-------------|------|-------------|
| POST | `/api/auth/sign-up` | Register new user | No | `{email, name, password}` |
| POST | `/api/auth/sign-in` | Login user | No | `{email, password}` |
| POST | `/api/auth/token` | Refresh access token | Cookie | None |
| POST | `/api/auth/forgot-password` | Send reset code | No | `{email}` |
| POST | `/api/auth/restore-password` | Reset password | No | `{reset_code, new_password}` |
| GET | `/api/auth/logout` | Logout current device | Cookie | None |
| GET | `/api/auth/logoutAll` | Logout all devices | Cookie | None |

### User Management
| Method | Path | Description | Auth | Request Body |
|--------|------|-------------|------|-------------|
| GET | `/api/users/me` | Get current user profile | Bearer | None |

### Expense Management
| Method | Path | Description | Auth | Request Body |
|--------|------|-------------|------|-------------|
| GET | `/api/expenses` | List expenses (filtered, paginated) | Bearer | Query params |
| POST | `/api/expenses` | Create expense | Bearer | `{name, amount, currency, category, date}` |
| GET | `/api/expenses/{id}` | Get expense by ID | Bearer | None |
| PATCH | `/api/expenses/{id}` | Update expense | Bearer | `{name?, amount?, currency?, category?, date?}` |
| DELETE | `/api/expenses/{id}` | Delete expense | Bearer | None |
| PATCH | `/api/expenses/reorder` | Reorder expenses | Bearer | `{expense_ids: []}` |

### Invoice Processing
| Method | Path | Description | Auth | Request Body |
|--------|------|-------------|------|-------------|
| POST | `/api/invoices/analyze` | Analyze invoice image (OCR) | Bearer | `multipart/form-data` |

### System Endpoints
| Method | Path | Description | Auth | Response |
|--------|------|-------------|------|----------|
| GET | `/api/ping` | Health check | No | `{"message": "pong"}` |
| GET | `/docs` | API documentation (Swagger UI) | No | HTML |
| GET | `/` | Redirect to API docs | No | Redirect |

## Environment Variables

See [.env_template](.env_template) for all available variables. Key settings:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | JWT signing key | `changethis` |
| `POSTGRES_PASSWORD` | Database password | `changethis` |
| `ENVIRONMENT` | `local` / `staging` / `production` | `local` |
| `FRONTEND_HOST` | Frontend URL for email links | `http://localhost:3000` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |
| `SMTP_HOST` | Mail server | — |
| `SENTRY_DSN` | Sentry error tracking | — |
| `OPENAI_API_KEY` | Invoice OCR (optional) | — |

## Docker Compose

### Development
```bash
docker compose watch
```

### Production
```bash
docker compose -f docker-compose.yaml -f docker-compose.traefik.yml up -d
```

## Pre-commit & Code Linting

```bash
# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```
