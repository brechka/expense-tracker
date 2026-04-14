# Performance Optimization Guide

This document describes the performance analysis and optimizations applied to the Expense Tracker application.

## Frontend DevTools Setup

### 1. React DevTools (Primary Tool)
React DevTools browser extension provides:
- Component tree inspection
- Props and state inspection
- **Profiler for performance analysis**
- Component render tracking

**Installation:**
- [Chrome Extension](https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi)
- [Firefox Extension](https://addons.mozilla.org/en-US/firefox/addon/react-devtools/)

**Usage:**
1. Open browser DevTools (F12)
2. Navigate to "⚛️ Profiler" tab
3. Click "Record", interact with the app, click "Stop"
4. Analyze the flamegraph for components with excessive re-renders

### 2. Performance Monitor
Custom utility for tracking component render performance at runtime.

**Location:** `src/utils/performance.ts`

**Usage in Browser Console:**
```javascript
window.__performanceMonitor.logReport();    // View all metrics
window.__performanceMonitor.getMetrics('Expenses');  // Single component
window.__performanceMonitor.reset();        // Clear metrics
```

## Frontend Render Optimizations

### Component Memoization (`React.memo`)
All reusable components are wrapped with `React.memo` to prevent re-renders when props haven't changed:

| Component | Memoized | displayName |
|-----------|----------|-------------|
| Button | ✅ | ✅ |
| Input | ✅ | ✅ |
| PasswordInput | ✅ | ✅ |
| InputLabel | ✅ | ✅ |
| Logo | ✅ | ✅ |
| Loader | ✅ | ✅ |
| DatePicker | ✅ | ✅ |
| Icon | ✅ | ✅ |
| AuthLayout | ✅ | ✅ |
| UploadInvoiceModal | ✅ | ✅ |

### Callback Memoization (`useCallback`)
The Expenses page uses `useCallback` for all event handlers to maintain stable function references:
- handleSignOut, resetCreateForm, handleToggleMenu
- handleDrawerOpen, handleDrawerClose, handleEditExpense, handleDeleteExpense
- handleDragStart, handleDragOver, handleDragLeave, handleDrop, handleDragEnd
- handleInvoiceUploadSuccess, handleCreateExpense, handleBrowseClick

### Value Memoization (`useMemo`)
- **Expenses**: `rows` — memoized expense list
- **Input/PasswordInput**: `hasValue`, `className` — memoized computed values
- **Icon**: `xlinkHref`, `style` — memoized SVG references

### Pure Functions Outside Components
Utility functions moved outside components to prevent recreation on every render:
- formatDate, formatCategory, getCurrencySymbol, formatAmount, getTodayDateString
- validateFile (UploadInvoiceModal)

### Token Management
- Access token stored in closure (not localStorage/sessionStorage) — zero storage I/O
- Axios interceptors handle token attachment and auto-refresh transparently
- Refresh deduplication — concurrent 401s share a single refresh request

## Frontend Performance Benchmarks

### Before Optimization
- ❌ Components re-rendered on every parent render
- ❌ Event handlers recreated on every render (causing child re-renders)
- ❌ Expensive computations recalculated unnecessarily

### After Optimization
- ✅ Components only re-render when props/state actually change
- ✅ Event handlers have stable references (prevents child re-renders)
- ✅ Computed values cached with `useMemo`
- ✅ Performance monitor available for runtime metrics

## Backend Optimizations

### Bottlenecks Identified

| # | Area | Issue | Impact |
|---|------|-------|--------|
| 1 | Database | No connection pooling configured | New connection per request, ~5ms overhead each |
| 2 | Database | Missing composite indexes on expenses | Full table scan for filtered queries |
| 3 | Database | N+1 queries in reorder endpoint | N individual SELECT+UPDATE per expense |
| 4 | Rate limiter | O(n) list rebuild on every request | Linear scan of all timestamps |
| 5 | Middleware | No request timing visibility | Cannot identify slow endpoints |

### Solutions Implemented

#### 1. Connection Pool Tuning (`src/db/database.py`)
- pool_size=10, max_overflow=20, pool_pre_ping=True, pool_recycle=1800

#### 2. Composite Database Indexes
- `ix_expenses_user_order` on `(user_id, display_order)`
- `ix_expenses_user_date` on `(user_id, date)`

#### 3. Batch Reorder — single transaction instead of N+1 queries

#### 4. Rate Limiter — `deque` with O(1) cleanup instead of O(n) list rebuild

#### 5. Request Logging — every request logged with duration in ms

### Backend Performance Comparison

| Endpoint | Before (est.) | After (est.) | Improvement |
|----------|--------------|-------------|-------------|
| GET /api/expenses (100 rows) | ~15ms | ~8ms | ~47% faster |
| PATCH /api/expenses/reorder (20 items) | ~120ms | ~10ms | ~92% faster |
| POST /api/auth/sign-in | ~350ms | ~345ms | ~1% (bcrypt dominates) |
| GET /api/users/me | ~8ms | ~5ms | ~37% faster |

## Verification Steps

1. Install React DevTools browser extension
2. Start the dev server: `cd frontend && npm run dev`
3. Open DevTools → ⚛️ Profiler → Record → interact → Stop
4. Check flamegraph: memoized components should NOT re-render unless props change
5. Open console: `window.__performanceMonitor.logReport()` for runtime metrics
