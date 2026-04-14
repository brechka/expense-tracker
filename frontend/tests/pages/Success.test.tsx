import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Success from '@/pages/Success';

describe('Success', () => {
  it('renders success message', () => {
    render(
      <MemoryRouter>
        <Success />
      </MemoryRouter>,
    );
    expect(screen.getByText(/change password successfully/i)).toBeInTheDocument();
  });

  it('renders OK button', () => {
    render(
      <MemoryRouter>
        <Success />
      </MemoryRouter>,
    );
    expect(screen.getByRole('button', { name: /ok/i })).toBeInTheDocument();
  });

  it('renders password changed illustration', () => {
    render(
      <MemoryRouter>
        <Success />
      </MemoryRouter>,
    );
    expect(screen.getByAltText(/password changed/i)).toBeInTheDocument();
  });
});
