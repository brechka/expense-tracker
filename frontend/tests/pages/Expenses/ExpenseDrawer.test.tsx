import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ExpenseDrawer } from '@/pages/Expenses/ExpenseDrawer';

vi.mock('@/components', () => ({
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
}));

const noop = vi.fn();

function renderDrawer(overrides = {}) {
  const defaults = {
    editingExpenseId: null,
    createName: '',
    setCreateName: noop,
    createAmount: '',
    setCreateAmount: noop,
    createCurrency: 'USD' as const,
    setCreateCurrency: noop,
    createCategory: 'hobby' as const,
    setCreateCategory: noop,
    createDate: '2024-06-01',
    setCreateDate: noop,
    creating: false,
    createError: null,
    onSubmit: noop,
    onClose: noop,
    onUploadInvoice: noop,
  };
  return render(<ExpenseDrawer {...defaults} {...overrides} />);
}

describe('ExpenseDrawer', () => {
  beforeEach(() => vi.clearAllMocks());

  it('renders "Create expense" title when not editing', () => {
    renderDrawer();
    expect(screen.getByText('Create expense')).toBeInTheDocument();
  });

  it('renders "Edit expense" title when editing', () => {
    renderDrawer({ editingExpenseId: 5 });
    expect(screen.getByText('Edit expense')).toBeInTheDocument();
  });

  it('renders Upload Invoice button', () => {
    renderDrawer();
    expect(screen.getByText('Upload Invoice')).toBeInTheDocument();
  });

  it('calls onUploadInvoice when Upload Invoice clicked', () => {
    const onUploadInvoice = vi.fn();
    renderDrawer({ onUploadInvoice });
    screen.getByText('Upload Invoice').click();
    expect(onUploadInvoice).toHaveBeenCalledTimes(1);
  });

  it('renders form fields', () => {
    renderDrawer();
    expect(screen.getByText('Name')).toBeInTheDocument();
    expect(screen.getByText('Payment amount')).toBeInTheDocument();
    expect(screen.getByText('Select category')).toBeInTheDocument();
    expect(screen.getByText('Select date')).toBeInTheDocument();
  });

  it('shows error banner when createError is set', () => {
    renderDrawer({ createError: 'Name is required' });
    expect(screen.getByText('Name is required')).toBeInTheDocument();
  });

  it('shows "Create" button text when not editing', () => {
    renderDrawer();
    expect(screen.getByText('Create')).toBeInTheDocument();
  });

  it('shows "Update" button text when editing', () => {
    renderDrawer({ editingExpenseId: 1 });
    expect(screen.getByText('Update')).toBeInTheDocument();
  });

  it('shows "Creating…" when creating', () => {
    renderDrawer({ creating: true });
    expect(screen.getByText('Creating…')).toBeInTheDocument();
  });

  it('shows "Updating…" when updating', () => {
    renderDrawer({ creating: true, editingExpenseId: 1 });
    expect(screen.getByText('Updating…')).toBeInTheDocument();
  });

  it('calls onClose when close button clicked', () => {
    const onClose = vi.fn();
    renderDrawer({ onClose });
    screen.getByLabelText('Close').click();
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it('renders category buttons for all categories', () => {
    renderDrawer();
    expect(screen.getByLabelText('Category mobile')).toBeInTheDocument();
    expect(screen.getByLabelText('Category subscription')).toBeInTheDocument();
    expect(screen.getByLabelText('Category debt')).toBeInTheDocument();
  });

  it('renders currency select with options', () => {
    renderDrawer();
    const select = screen.getByLabelText('Currency');
    expect(select).toBeInTheDocument();
    expect(screen.getByText('USD')).toBeInTheDocument();
    expect(screen.getByText('EUR')).toBeInTheDocument();
    expect(screen.getByText('PLN')).toBeInTheDocument();
  });
});
