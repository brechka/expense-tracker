import React, { memo } from 'react';
import styles from './index.module.css';

interface InputLabelProps {
  children: React.ReactNode;
  htmlFor?: string;
}

/**
 * InputLabel component renders a styled label element.
 * Used above form inputs to describe the expected value.
 *
 * @example
 * ```tsx
 * <InputLabel htmlFor="email">Email</InputLabel>
 * ```
 */
export const InputLabel = memo(({ children, htmlFor }: InputLabelProps) => {
  return (
    <label className={styles.label} htmlFor={htmlFor}>
      {children}
    </label>
  );
});

InputLabel.displayName = 'InputLabel';
