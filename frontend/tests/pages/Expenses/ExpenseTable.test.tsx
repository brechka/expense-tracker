import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ExpenseTable } from '@/pages/Expenses/ExpenseTable';
import type { Expense } from '@/pages/Expenses/constants';

vi.mock('@/components', () => ({
  Icon: ({ icon }: { icon: string }) => <span data-testid={`icon-${icon}`} />,
}));

const expense: Expense = {
  id: 1,
  name: 'Netflix',
  amount: 15.99,
  currency: 'USD',
  category: 'subscription',
  date: '2024-06-01T00:00:00Z',
};

const noop = vi.fn();
const dragNoop = vi.fn() as unknown as (e: React.DragEvent, id: number) => void;

function renderTable(expenses: Expense[] = [expense], menuOpenId: number | null = null) {
  return render(
    <ExpenseTable
      expenses={expenses}
      menuOpenId={menuOpenId}
      draggedExpenseId={null}
      dragOverExpenseId={null}
      onToggleMenu={noop}
      onEdit={noop}
      onDelete={noop}
      onDragStart={dragNoop}
      onDragOver={dragNoop}
      onDragLeave={noop}
      onDrop={dragNoop}
      onDragEnd={noop}
    />,
  );
}

describe('ExpenseTable', () => {
  beforeEach(() => vi.clearAllMocks());

  it('renders table headers', () => {
    renderTable();
    expect(screen.getByText('Name')).toBeInTheDocument();
    expect(screen.getByText('Category')).toBeInTheDocument();
    expect(screen.getByText('Date')).toBeInTheDocument();
    expect(screen.getByText('Total')).toBeInTheDocument();
  });

  it('renders expense row', () => {
    renderTable();
    expect(screen.getByText('Netflix')).toBeInTheDocument();
    expect(screen.getByText('Subscription')).toBeInTheDocument();
    expect(screen.getByText(/-\$15.99/)).toBeInTheDocument();
  });

  it('renders category icon', () => {
    renderTable();
    expect(screen.getByTestId('icon-subscription')).toBeInTheDocument();
  });

  it('shows menu dropdown when menuOpenId matches', () => {
    renderTable([expense], 1);
    expect(screen.getByText('Edit')).toBeInTheDocument();
    expect(screen.getByText('Delete')).toBeInTheDocument();
  });

  it('does not show menu dropdown when menuOpenId is null', () => {
    renderTable([expense], null);
    expect(screen.queryByText('Edit')).not.toBeInTheDocument();
  });

  it('calls onToggleMenu when ⋯ button clicked', async () => {
    const user = userEvent.setup();
    renderTable();
    await user.click(screen.getByLabelText('More options'));
    expect(noop).toHaveBeenCalledWith(1);
  });

  it('calls onEdit when Edit clicked', async () => {
    const user = userEvent.setup();
    renderTable([expense], 1);
    await user.click(screen.getByText('Edit'));
    expect(noop).toHaveBeenCalledWith(expense);
  });

  it('calls onDelete when Delete clicked', async () => {
    const user = userEvent.setup();
    renderTable([expense], 1);
    await user.click(screen.getByText('Delete'));
    expect(noop).toHaveBeenCalledWith(1);
  });
});
