import { useState, useCallback } from 'react';
import { apiClient } from '@/utils/api';
import type { Category } from '@/types';
import type { Expense, CreateExpensePayload } from './constants';
import { currencyOptions, getTodayDateString, formatDateForInput } from './constants';

export function useExpenseForm(
    setExpenses: React.Dispatch<React.SetStateAction<Expense[]>>,
) {
    const [drawerOpen, setDrawerOpen] = useState(false);
    const [editingExpenseId, setEditingExpenseId] = useState<number | null>(null);
    const [createName, setCreateName] = useState('');
    const [createAmount, setCreateAmount] = useState('');
    const [createCurrency, setCreateCurrency] = useState<(typeof currencyOptions)[number]>('USD');
    const [createCategory, setCreateCategory] = useState<Category>('hobby');
    const [createDate, setCreateDate] = useState(getTodayDateString());
    const [creating, setCreating] = useState(false);
    const [createError, setCreateError] = useState<string | null>(null);

    const resetCreateForm = useCallback(() => {
        setCreateName('');
        setCreateAmount('');
        setCreateCurrency('USD');
        setCreateCategory('hobby');
        setCreateDate(getTodayDateString());
        setCreateError(null);
        setEditingExpenseId(null);
    }, []);

    const handleDrawerOpen = useCallback(() => {
        resetCreateForm();
        setDrawerOpen(true);
    }, [resetCreateForm]);

    const handleDrawerClose = useCallback(() => {
        setDrawerOpen(false);
        resetCreateForm();
    }, [resetCreateForm]);

    const handleEditExpense = useCallback((expense: Expense) => {
        setCreateName(expense.name);
        setCreateAmount(String(expense.amount));
        setCreateCurrency(expense.currency as (typeof currencyOptions)[number]);
        setCreateCategory(expense.category as Category);
        setCreateDate(formatDateForInput(expense.date));
        setEditingExpenseId(expense.id);
        setDrawerOpen(true);
    }, []);

    const handleInvoiceUploadSuccess = useCallback((data: { name: string; amount: number; currency?: string; date: string }) => {
        resetCreateForm();
        setCreateName(data.name);
        setCreateAmount(String(data.amount));
        if (data.currency && currencyOptions.includes(data.currency as (typeof currencyOptions)[number])) {
            setCreateCurrency(data.currency as (typeof currencyOptions)[number]);
        }
        setCreateDate(data.date);
        setCreateError(null);
        setDrawerOpen(true);
    }, [resetCreateForm]);

    const handleCreateExpense = useCallback(async (e: React.FormEvent) => {
        e.preventDefault();
        setCreateError(null);

        const trimmedName = createName.trim();
        const amountNum = Number(createAmount);

        if (!trimmedName) return setCreateError('Name is required');
        if (!Number.isFinite(amountNum) || amountNum <= 0) return setCreateError('Amount must be greater than 0');
        if (!createCurrency) return setCreateError('Currency is required');
        if (!createCategory) return setCreateError('Category is required');

        const payload: CreateExpensePayload = {
            name: trimmedName,
            amount: amountNum,
            currency: createCurrency,
            category: createCategory,
            date: createDate ? new Date(createDate).toISOString() : null,
        };

        try {
            setCreating(true);
            if (editingExpenseId) {
                const res = await apiClient.patch(`/api/expenses/${editingExpenseId}`, payload);
                setExpenses((prev) => prev.map((exp) => (exp.id === editingExpenseId ? (res.data as Expense) : exp)));
            } else {
                const res = await apiClient.post('/api/expenses', payload);
                setExpenses((prev) => [res.data as Expense, ...prev]);
            }
            resetCreateForm();
            if (!window.matchMedia('(min-width: 1100px)').matches) setDrawerOpen(false);
        } catch (err) {
            setCreateError(err instanceof Error ? err.message : editingExpenseId ? 'Failed to update expense' : 'Failed to create expense');
        } finally {
            setCreating(false);
        }
    }, [createName, createAmount, createCurrency, createCategory, createDate, editingExpenseId, resetCreateForm, setExpenses]);

    return {
        drawerOpen,
        editingExpenseId,
        createName,
        setCreateName,
        createAmount,
        setCreateAmount,
        createCurrency,
        setCreateCurrency,
        createCategory,
        setCreateCategory,
        createDate,
        setCreateDate,
        creating,
        createError,
        handleDrawerOpen,
        handleDrawerClose,
        handleEditExpense,
        handleInvoiceUploadSuccess,
        handleCreateExpense,
    };
}
