import { render, screen } from '@testing-library/react';
import { AuthLayout } from '@/layouts';

describe('AuthLayout', () => {
  it('renders children inside the content panel', () => {
    render(<AuthLayout><p>Test content</p></AuthLayout>);
    expect(screen.getByText('Test content')).toBeInTheDocument();
  });

  it('renders the desktop logo image', () => {
    render(<AuthLayout><span>child</span></AuthLayout>);
    const logo = screen.getByAltText('YAET - Yet Another Expense Tracker');
    expect(logo).toBeInTheDocument();
    expect(logo.tagName).toBe('IMG');
  });

  it('renders the login illustration', () => {
    render(<AuthLayout><span>child</span></AuthLayout>);
    expect(screen.getByAltText('Login illustration')).toBeInTheDocument();
  });
});
