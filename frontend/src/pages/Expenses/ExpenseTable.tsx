import React from 'react';
import { Icon } from '@/components';
import type { Category } from '@/types';
import type { Expense } from './constants';
import { categoryOptions, formatCategory, formatDate, formatAmount } from './constants';
import styles from './Expenses.module.css';

type Props = {
    expenses: Expense[];
    menuOpenId: number | null;
    draggedExpenseId: number | null;
    dragOverExpenseId: number | null;
    onToggleMenu: (id: number) => void;
    onEdit: (expense: Expense) => void;
    onDelete: (id: number) => void;
    onDragStart: (e: React.DragEvent, id: number) => void;
    onDragOver: (e: React.DragEvent, id: number) => void;
    onDragLeave: () => void;
    onDrop: (e: React.DragEvent, id: number) => void;
    onDragEnd: () => void;
};

export const ExpenseTable: React.FC<Props> = ({
    expenses, menuOpenId, draggedExpenseId, dragOverExpenseId,
    onToggleMenu, onEdit, onDelete,
    onDragStart, onDragOver, onDragLeave, onDrop, onDragEnd,
}) => (
    <table className={styles.table}>
        <thead>
            <tr>
                <th className={styles.th}>Name</th>
                <th className={styles.th}>Category</th>
                <th className={styles.th}>Date</th>
                <th className={styles.th}>Total</th>
                <th className={styles.th}></th>
            </tr>
        </thead>
        <tbody>
            {expenses.map((expense) => {
                const iconCandidate = expense.category as Category;
                const canRenderIcon = categoryOptions.includes(iconCandidate);
                const isDragging = draggedExpenseId === expense.id;
                const isDragOver = dragOverExpenseId === expense.id;
                return (
                    <tr
                        className={`${styles.row} ${isDragging ? styles.dragging : ''} ${isDragOver ? styles.dragOver : ''}`}
                        key={expense.id}
                        draggable
                        onDragStart={(e) => onDragStart(e, expense.id)}
                        onDragOver={(e) => onDragOver(e, expense.id)}
                        onDragLeave={onDragLeave}
                        onDrop={(e) => onDrop(e, expense.id)}
                        onDragEnd={onDragEnd}
                    >
                        <td className={styles.td}>
                            <div className={styles.nameCell}>
                                <span className={styles.iconBox} aria-hidden="true">
                                    {canRenderIcon ? <Icon icon={iconCandidate} size={18} color="white" /> : null}
                                </span>
                                <span className={styles.expenseName}>{expense.name}</span>
                            </div>
                        </td>
                        <td className={styles.td}>
                            <span className={styles.muted}>{formatCategory(expense.category)}</span>
                        </td>
                        <td className={styles.td}>
                            <span className={styles.muted}>{formatDate(expense.date)}</span>
                        </td>
                        <td className={styles.td}>
                            <span className={styles.totalAmount}>
                                {formatAmount(expense.amount, expense.currency)}
                            </span>
                        </td>
                        <td className={styles.td}>
                            <div className={styles.actionMenuContainer} data-action-menu>
                                <button
                                    type="button"
                                    className={styles.menuButton}
                                    onClick={() => onToggleMenu(expense.id)}
                                    aria-label="More options"
                                >
                                    ⋯
                                </button>
                                {menuOpenId === expense.id && (
                                    <div className={styles.menuDropdown}>
                                        <button type="button" className={styles.menuItem} onClick={() => onEdit(expense)}>
                                            Edit
                                        </button>
                                        <button type="button" className={styles.menuItem} onClick={() => onDelete(expense.id)}>
                                            Delete
                                        </button>
                                    </div>
                                )}
                            </div>
                        </td>
                    </tr>
                );
            })}
        </tbody>
    </table>
);
