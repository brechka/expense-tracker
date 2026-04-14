import type { Category } from '@/types';

export type Expense = {
    id: number;
    name: string;
    amount: number;
    currency: string;
    category: string;
    date: string | null;
    display_order?: number | null;
};

export type CreateExpensePayload = {
    name: string;
    amount: number;
    currency: string;
    category: string;
    date: string | null;
};

export const categoryOptions: Category[] = [
    'mobile',
    'credit',
    'other_payment',
    'hobby',
    'subscription',
    'transport',
    'restaurant',
    'utility',
    'shopping',
    'debt',
];

export const currencyOptions = ['USD', 'EUR', 'PLN'] as const;

export function formatDate(date: string | null): string {
    if (!date) return '-';
    const d = new Date(date);
    if (Number.isNaN(d.getTime())) return '-';
    return d.toLocaleDateString(undefined, { day: '2-digit', month: 'short', year: 'numeric' });
}

export function formatCategory(category: string): string {
    if (!category) return category;
    return category
        .split('_')
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ');
}

export function getCurrencySymbol(currency: string): string {
    switch (currency) {
        case 'USD': return '$';
        case 'EUR': return '€';
        case 'PLN': return 'zł';
        default: return currency;
    }
}

export function formatAmount(amount: number, currency: string): string {
    const formattedAmount = Number.isFinite(amount) ? amount.toLocaleString() : String(amount);
    return `-${getCurrencySymbol(currency)}${formattedAmount}`;
}

export function getTodayDateString(): string {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

export function formatDateForInput(date: string | null): string {
    if (!date) return getTodayDateString();
    const d = new Date(date);
    if (Number.isNaN(d.getTime())) return getTodayDateString();
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}
