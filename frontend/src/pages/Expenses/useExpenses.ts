import { useEffect, useState, useCallback } from 'react';
import { apiClient } from '@/utils/api';
import type { Expense } from './constants';

export function useExpenses() {
    const [expenses, setExpenses] = useState<Expense[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [menuOpenId, setMenuOpenId] = useState<number | null>(null);
    const [draggedExpenseId, setDraggedExpenseId] = useState<number | null>(null);
    const [dragOverExpenseId, setDragOverExpenseId] = useState<number | null>(null);

    useEffect(() => {
        let mounted = true;
        (async () => {
            try {
                setLoading(true);
                setError(null);
                const res = await apiClient.get('/api/expenses');
                if (!mounted) return;
                setExpenses(res.data.data ?? res.data);
            } catch (e) {
                if (!mounted) return;
                setError(e instanceof Error ? e.message : 'Failed to load expenses');
            } finally {
                if (!mounted) return;
                setLoading(false);
            }
        })();
        return () => { mounted = false; };
    }, []);

    useEffect(() => {
        if (menuOpenId === null) return;
        const handleClickOutside = (event: MouseEvent) => {
            const target = event.target as HTMLElement;
            if (!target.closest('[data-action-menu]')) {
                setMenuOpenId(null);
            }
        };
        document.addEventListener('click', handleClickOutside);
        return () => document.removeEventListener('click', handleClickOutside);
    }, [menuOpenId]);

    const handleToggleMenu = useCallback((expenseId: number) => {
        setMenuOpenId((prev) => prev === expenseId ? null : expenseId);
    }, []);

    const handleDeleteExpense = useCallback(async (id: number) => {
        if (!confirm('Are you sure you want to delete this expense?')) return;
        try {
            await apiClient.delete(`/api/expenses/${id}`);
            setExpenses((prev) => prev.filter((exp) => exp.id !== id));
            setMenuOpenId(null);
        } catch (err) {
            alert(err instanceof Error ? err.message : 'Failed to delete expense');
        }
    }, []);

    const handleDragStart = useCallback((e: React.DragEvent, expenseId: number) => {
        setDraggedExpenseId(expenseId);
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/html', '');
    }, []);

    const handleDragOver = useCallback((e: React.DragEvent, expenseId: number) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        if (draggedExpenseId !== expenseId) {
            setDragOverExpenseId(expenseId);
        }
    }, [draggedExpenseId]);

    const handleDragLeave = useCallback(() => {
        setDragOverExpenseId(null);
    }, []);

    const handleDrop = useCallback(async (e: React.DragEvent, targetExpenseId: number) => {
        e.preventDefault();
        setDragOverExpenseId(null);

        if (!draggedExpenseId || draggedExpenseId === targetExpenseId) {
            setDraggedExpenseId(null);
            return;
        }

        const draggedIndex = expenses.findIndex((exp) => exp.id === draggedExpenseId);
        const targetIndex = expenses.findIndex((exp) => exp.id === targetExpenseId);

        if (draggedIndex === -1 || targetIndex === -1) {
            setDraggedExpenseId(null);
            return;
        }

        const newExpenses = [...expenses];
        const [draggedExpense] = newExpenses.splice(draggedIndex, 1);
        newExpenses.splice(targetIndex, 0, draggedExpense);

        setExpenses(newExpenses);
        setDraggedExpenseId(null);

        try {
            const expenseIds = newExpenses.map((exp) => exp.id);
            await apiClient.patch('/api/expenses/reorder', { expense_ids: expenseIds });
        } catch (err) {
            setExpenses(expenses);
            alert(err instanceof Error ? err.message : 'Failed to reorder expenses');
        }
    }, [draggedExpenseId, expenses]);

    const handleDragEnd = useCallback(() => {
        setDraggedExpenseId(null);
        setDragOverExpenseId(null);
    }, []);

    return {
        expenses,
        setExpenses,
        loading,
        error,
        menuOpenId,
        setMenuOpenId,
        draggedExpenseId,
        dragOverExpenseId,
        handleToggleMenu,
        handleDeleteExpense,
        handleDragStart,
        handleDragOver,
        handleDragLeave,
        handleDrop,
        handleDragEnd,
    };
}
