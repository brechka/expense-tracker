import { render, screen } from '@testing-library/react';
import { ExpenseMobileList } from '@/pages/Expenses/ExpenseMobileList';
import type { Expense } from '@/pages/Expenses/constants';

vi.mock('@/components', () => ({
  Icon: ({ icon }: { icon: string }) => <span data-testid={`icon-${icon}`} />,
}));

const expense: Expense = {
  id: 1,
  name: 'Uber',
  amount: 25,
  currency: 'EUR',
  category: 'transport',
  date: '2024-07-10T00:00:00Z',
};

const noop = vi.fn();
const dragNoop = vi.fn() as unknown as (e: React.DragEvent, id: number) => void;

describe('ExpenseMobileList', () => {
  it('renders expense card with name and category', () => {
    render(
      <ExpenseMobileList
        expenses={[expense]}
        draggedExpenseId={null}
        dragOverExpenseId={null}
        onDragStart={dragNoop}
        onDragOver={dragNoop}
        onDragLeave={noop}
        onDrop={dragNoop}
        onDragEnd={noop}
      />,
    );
    expect(screen.getByText('Uber')).toBeInTheDocument();
    expect(screen.getByText('Transport')).toBeInTheDocument();
    expect(screen.getByText(/-€25/)).toBeInTheDocument();
  });

  it('renders category icon', () => {
    render(
      <ExpenseMobileList
        expenses={[expense]}
        draggedExpenseId={null}
        dragOverExpenseId={null}
        onDragStart={dragNoop}
        onDragOver={dragNoop}
        onDragLeave={noop}
        onDrop={dragNoop}
        onDragEnd={noop}
      />,
    );
    expect(screen.getByTestId('icon-transport')).toBeInTheDocument();
  });

  it('renders empty when no expenses', () => {
    const { container } = render(
      <ExpenseMobileList
        expenses={[]}
        draggedExpenseId={null}
        dragOverExpenseId={null}
        onDragStart={dragNoop}
        onDragOver={dragNoop}
        onDragLeave={noop}
        onDrop={dragNoop}
        onDragEnd={noop}
      />,
    );
    expect(container.querySelectorAll('[draggable]')).toHaveLength(0);
  });
});
