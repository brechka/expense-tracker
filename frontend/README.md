# Expense Tracker — Frontend

React 18 + TypeScript + Vite

## Setup

Requires Node.js 18+.

```bash
npm install
npm run dev
```

Runs at http://localhost:3000. Expects the backend API at http://localhost:8000.

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start dev server |
| `npm run build` | Production build |
| `npm run test` | Run tests (44 tests) |
| `npm run test:watch` | Tests in watch mode |
| `npm run lint` | ESLint |
| `npm run stylelint` | CSS linting |
| `npm run format` | Prettier |
| `npm run storybook` | Storybook at http://localhost:6006 |

## Project Structure

```
src/
├── components/    # Reusable UI (Button, Input, Icon, DatePicker, etc.)
├── pages/         # Route pages (SignIn, SignUp, Expenses, Profile, etc.)
├── routes/        # React Router config with auth guards
├── layouts/       # Page layouts (AuthLayout)
└── utils/         # API client, Sentry, performance utils
```

## Key Libraries

- react-hook-form + yup — form handling & validation
- axios — HTTP client with automatic token refresh
- react-router-dom — routing with auth guards
- CSS Modules — scoped styling
