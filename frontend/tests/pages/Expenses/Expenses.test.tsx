import { render, screen, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import Expenses from '@/pages/Expenses/Expenses';

const mockGet = vi.fn();
const mockPost = vi.fn();
const mockPatch = vi.fn();
const mockDelete = vi.fn();

vi.mock('@/utils/api', () => ({
  apiClient: {
    get: (...args: unknown[]) => mockGet(...args),
    post: (...args: unknown[]) => mockPost(...args),
    patch: (...args: unknown[]) => mockPatch(...args),
    delete: (...args: unknown[]) => mockDelete(...args),
  },
  logout: vi.fn().mockResolvedValue(undefined),
}));

vi.mock('@/components', () => ({
  Loader: () => <div data-testid="loader">Loading...</div>,
  Logo: () => <div data-testid="logo">Logo</div>,
  Button: ({ children, ...props }: React.PropsWithChildren<React.ButtonHTMLAttributes<HTMLButtonElement>>) => (
    <button {...props}>{children}</button>
  ),
  Input: ({ value, onChange, placeholder, type }: { value: string; onChange: (v: string) => void; placeholder?: string; type?: string }) => (
    <input value={value} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} type={type} />
  ),
  InputLabel: ({ children }: React.PropsWithChildren) => <label>{children}</label>,
  DatePicker: ({ value, onChange }: { value: string; onChange: (v: string) => void }) => (
    <input type="date" value={value} onChange={(e) => onChange(e.target.value)} data-testid="date-picker" />
  ),
  Icon: ({ icon }: { icon: string }) => <span data-testid={`icon-${icon}`} />,
  UploadInvoiceModal: ({ isOpen }: { isOpen: boolean }) =>
    isOpen ? <div data-testid="upload-modal">Upload Modal</div> : null,
}));

const expenses = [
  { id: 1, name: 'Netflix', amount: 15.99, currency: 'USD', category: 'subscription', date: '2024-06-01T00:00:00Z' },
  { id: 2, name: 'Uber', amount: 25, currency: 'EUR', category: 'transport', date: '2024-07-10T00:00:00Z' },
];

function renderPage() {
  return render(
    <MemoryRouter>
      <Expenses />
    </MemoryRouter>,
  );
}

describe('Expenses page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockGet.mockResolvedValue({ data: { data: expenses } });
  });

  it('shows loader while fetching', () => {
    mockGet.mockReturnValue(new Promise(() => {})); // never resolves
    renderPage();
    expect(screen.getByTestId('loader')).toBeInTheDocument();
  });

  it('renders expenses after loading', async () => {
    renderPage();
    await waitFor(() => {
      expect(screen.getAllByText('Netflix').length).toBeGreaterThan(0);
    });
    expect(screen.getAllByText('Uber').length).toBeGreaterThan(0);
  });

  it('shows error on fetch failure', async () => {
    mockGet.mockRejectedValue(new Error('Network error'));
    renderPage();
    await waitFor(() => {
      expect(screen.getByText('Network error')).toBeInTheDocument();
    });
  });

  it('shows empty state when no expenses', async () => {
    mockGet.mockResolvedValue({ data: { data: [] } });
    renderPage();
    await waitFor(() => {
      expect(screen.getByText(/list of transactions are empty/i)).toBeInTheDocument();
    });
  });

  it('renders header with Profile link and Log out button', async () => {
    renderPage();
    await waitFor(() => expect(screen.getAllByText('Netflix').length).toBeGreaterThan(0));
    expect(screen.getByText('Profile')).toBeInTheDocument();
    expect(screen.getByText('Log out')).toBeInTheDocument();
  });

  it('opens drawer when FAB clicked', async () => {
    const user = userEvent.setup();
    renderPage();
    await waitFor(() => expect(screen.getAllByText('Netflix').length).toBeGreaterThan(0));
    await user.click(screen.getByLabelText('Add transaction'));
    expect(screen.getByText('Create expense')).toBeInTheDocument();
  });

  it('closes drawer when close button clicked', async () => {
    renderPage();
    await waitFor(() => expect(screen.getAllByText('Netflix').length).toBeGreaterThan(0));
    await act(async () => {
      screen.getByLabelText('Add transaction').click();
    });
    expect(screen.getByText('Create expense')).toBeInTheDocument();
    await act(async () => {
      screen.getByLabelText('Close').click();
    });
    expect(screen.queryByText('Create expense')).not.toBeInTheDocument();
  });
});
