import React from 'react';
import { Icon } from '@/components';
import type { Category } from '@/types';
import type { Expense } from './constants';
import { categoryOptions, formatCategory, formatDate, formatAmount } from './constants';
import styles from './Expenses.module.css';

type Props = {
    expenses: Expense[];
    draggedExpenseId: number | null;
    dragOverExpenseId: number | null;
    onDragStart: (e: React.DragEvent, id: number) => void;
    onDragOver: (e: React.DragEvent, id: number) => void;
    onDragLeave: () => void;
    onDrop: (e: React.DragEvent, id: number) => void;
    onDragEnd: () => void;
};

export const ExpenseMobileList: React.FC<Props> = ({
    expenses, draggedExpenseId, dragOverExpenseId,
    onDragStart, onDragOver, onDragLeave, onDrop, onDragEnd,
}) => (
    <div className={styles.mobileCardList}>
        {expenses.map((expense) => {
            const iconCandidate = expense.category as Category;
            const canRenderIcon = categoryOptions.includes(iconCandidate);
            const isDragging = draggedExpenseId === expense.id;
            const isDragOver = dragOverExpenseId === expense.id;
            return (
                <div
                    className={`${styles.expenseCard} ${isDragging ? styles.dragging : ''} ${isDragOver ? styles.dragOver : ''}`}
                    key={expense.id}
                    draggable
                    onDragStart={(e) => onDragStart(e, expense.id)}
                    onDragOver={(e) => onDragOver(e, expense.id)}
                    onDragLeave={onDragLeave}
                    onDrop={(e) => onDrop(e, expense.id)}
                    onDragEnd={onDragEnd}
                >
                    <div className={styles.cardLeft}>
                        <span className={styles.cardIcon} aria-hidden="true">
                            {canRenderIcon ? <Icon icon={iconCandidate} size={24} color="white" /> : null}
                        </span>
                        <div className={styles.cardInfo}>
                            <div className={styles.cardName}>{expense.name}</div>
                            <div className={styles.cardCategory}>{formatCategory(expense.category)}</div>
                        </div>
                    </div>
                    <div className={styles.cardRight}>
                        <div className={styles.cardAmount}>
                            {formatAmount(expense.amount, expense.currency)}
                        </div>
                        <div className={styles.cardDate}>{formatDate(expense.date)}</div>
                    </div>
                </div>
            );
        })}
    </div>
);
