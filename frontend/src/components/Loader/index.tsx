import { memo } from 'react';
import styles from './index.module.css';

/**
 * Loader component displays a spinning indicator.
 * Used to indicate loading state across the application.
 *
 * @example
 * ```tsx
 * <Loader />
 * ```
 */
export const Loader = memo(() => {
  return <div className={styles.spinner}></div>;
});

Loader.displayName = 'Loader';
