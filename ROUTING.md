# Routing Implementation

This document describes the routing implementation for the Expense Tracker application.

## Frontend Routes

### Public Routes
| Path | Page | Description |
|------|------|-------------|
| `/sign-in` | SignIn | User login with email/password |
| `/sign-up` | SignUp | User registration with name/email/password |
| `/forgot-password` | ForgotPassword | Enter email to receive reset code |
| `/verification-code` | VerificationCode | Enter the reset code from email |
| `/restore-password` | RestorePassword | Set a new password |
| `/success` | Success | Password change confirmation |

### Protected Routes (require authentication)
| Path | Page | Description |
|------|------|-------------|
| `/` | Expenses | Main page — expense table with CRUD |
| `/profile` | Profile | User profile details |

### Error Handling
| Path | Page | Description |
|------|------|-------------|
| `*` | NotFound | 404 catch-all for invalid routes |

## Route Protection

Protected routes use a `requireAuth` loader that runs before the page renders:
1. Checks if an access token exists in the closure
2. If not, attempts to refresh via `POST /api/auth/token` (httpOnly cookie)
3. If refresh succeeds → page loads normally
4. If refresh fails → redirects to `/sign-in`

## Password Recovery Flow

```
/forgot-password → /verification-code → /restore-password → /success
```

State is passed between pages via React Router's `location.state`:
- ForgotPassword → VerificationCode: `{ email }`
- VerificationCode → RestorePassword: `{ email, reset_code }`

## Backend API Endpoints

### Authentication (`/api/auth`)
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/api/auth/sign-up` | Register new user | No |
| POST | `/api/auth/sign-in` | Login, returns access token | No |
| POST | `/api/auth/token` | Refresh access token | Cookie |
| POST | `/api/auth/forgot-password` | Send reset code via email | No |
| POST | `/api/auth/restore-password` | Reset password with code | No |
| GET | `/api/auth/logout` | Logout current device | Cookie |
| GET | `/api/auth/logoutAll` | Logout all devices | Cookie |

### Users (`/api/users`)
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/api/users/me` | Get current user profile | Bearer |

### Expenses (`/api/expenses`)
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/api/expenses` | List expenses (filtered, paginated) | Bearer |
| POST | `/api/expenses` | Create expense | Bearer |
| GET | `/api/expenses/:id` | Get expense by ID | Bearer |
| PATCH | `/api/expenses/:id` | Update expense | Bearer |
| DELETE | `/api/expenses/:id` | Delete expense | Bearer |
| PATCH | `/api/expenses/reorder` | Reorder expenses (drag & drop) | Bearer |

### Invoices (`/api/invoices`)
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/api/invoices/analyze` | Analyze JPG invoice image | Bearer |

## Folder Structure

```
frontend/src/
├── pages/              # Page components
│   ├── SignIn.tsx
│   ├── SignUp.tsx
│   ├── ForgotPassword.tsx
│   ├── VerificationCode.tsx
│   ├── RestorePassword.tsx
│   ├── Success.tsx
│   ├── Expenses.tsx
│   ├── Profile/
│   ├── NotFound.tsx
│   └── index.ts        # Barrel export
├── routes/
│   ├── AppRouter.tsx    # Router config with auth guards
│   └── index.ts
├── layouts/
│   └── AuthLayout/      # Shared auth page wrapper
└── components/          # Reusable UI components

backend/src/
├── controllers/         # Route handlers
│   ├── auth_controller.py
│   ├── users_controller.py
│   ├── expenses_controller.py
│   └── invoice_controller.py
├── services/            # Business logic
├── db/                  # Repository layer
├── models/              # SQLAlchemy + Pydantic models
└── helpers/
    └── middlewares/      # Auth, rate limit, security headers, request logging
```
