import React, { memo } from 'react';
import styles from './index.module.css';

interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  type?: 'button' | 'submit' | 'reset';
}

/**
 * Button component renders a styled button element.
 * Supports disabled state, click handler, and button type.
 *
 * @example
 * ```tsx
 * <Button onClick={() => console.log('clicked')}>Click me</Button>
 * <Button disabled>Disabled</Button>
 * <Button type="submit">Submit</Button>
 * ```
 */
export const Button = memo(({ children, onClick, disabled, type = 'button' }: ButtonProps) => {
  return (
    <button
      type={type}
      className={styles.button}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
});

Button.displayName = 'Button';
