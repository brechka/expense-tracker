import React, { memo } from 'react';
import styles from './AuthLayout.module.css';

interface AuthLayoutProps {
  children: React.ReactNode;
}

/**
 * AuthLayout wraps authentication pages with a consistent layout:
 * - Purple gradient background
 * - Desktop: left panel with logo + illustration, right panel with form
 * - Mobile: centered white card with decorative circles
 *
 * @example
 * ```tsx
 * <AuthLayout>
 *   <h1>Sign In</h1>
 *   <form>...</form>
 * </AuthLayout>
 * ```
 */
export const AuthLayout = memo(({ children }: AuthLayoutProps) => {
  return (
    <div className={styles.container}>
      <div className={styles.desktopPanel}>
        <div className={styles.desktopLogo}>
          <img src="/logo.svg" alt="YAET - Yet Another Expense Tracker" />
        </div>
        <div className={styles.desktopIllustration}>
          <img src="/login.svg" alt="Login illustration" />
        </div>
      </div>

      <div className={styles.decorations}>
        <div className={styles.circle1} />
        <div className={styles.circle2} />
        <div className={styles.circle3} />
      </div>

      <div className={styles.contentPanel}>
        {children}
      </div>
    </div>
  );
});

AuthLayout.displayName = 'AuthLayout';
