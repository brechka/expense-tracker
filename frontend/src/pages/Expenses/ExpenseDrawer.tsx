import React from 'react';
import { Button, DatePicker, Icon, Input, InputLabel } from '@/components';
import type { Category } from '@/types';
import { categoryOptions, currencyOptions } from './constants';
import styles from './Expenses.module.css';

type Props = {
    editingExpenseId: number | null;
    createName: string;
    setCreateName: (v: string) => void;
    createAmount: string;
    setCreateAmount: (v: string) => void;
    createCurrency: (typeof currencyOptions)[number];
    setCreateCurrency: (v: (typeof currencyOptions)[number]) => void;
    createCategory: Category;
    setCreateCategory: (v: Category) => void;
    createDate: string;
    setCreateDate: (v: string) => void;
    creating: boolean;
    createError: string | null;
    onSubmit: (e: React.FormEvent) => void;
    onClose: () => void;
    onUploadInvoice: () => void;
};

export const ExpenseDrawer: React.FC<Props> = ({
    editingExpenseId, createName, setCreateName, createAmount, setCreateAmount,
    createCurrency, setCreateCurrency, createCategory, setCreateCategory,
    createDate, setCreateDate, creating, createError,
    onSubmit, onClose, onUploadInvoice,
}) => (
    <aside className={styles.drawer} aria-label={editingExpenseId ? 'Edit expense drawer' : 'Create expense drawer'}>
        <div className={styles.drawerHeader}>
            <div className={styles.drawerTitle}>{editingExpenseId ? 'Edit expense' : 'Create expense'}</div>
            <button type="button" className={styles.uploadInvoiceButton} onClick={onUploadInvoice}>
                Upload Invoice
            </button>
        </div>
        <form className={styles.drawerForm} onSubmit={onSubmit}>
            {createError && <div className={styles.errorBanner}>{createError}</div>}

            <div className={styles.field}>
                <InputLabel>Name</InputLabel>
                <Input placeholder="Text input" value={createName} onChange={setCreateName} />
            </div>

            <div className={styles.field}>
                <InputLabel>Payment amount</InputLabel>
                <div className={styles.amountRow}>
                    <Input placeholder="0" type="number" value={createAmount} onChange={setCreateAmount} />
                    <select
                        className={styles.select}
                        value={createCurrency}
                        onChange={(e) => setCreateCurrency(e.target.value as (typeof currencyOptions)[number])}
                        aria-label="Currency"
                    >
                        {currencyOptions.map((c) => (
                            <option key={c} value={c}>{c}</option>
                        ))}
                    </select>
                </div>
            </div>

            <div className={styles.field}>
                <InputLabel>Select category</InputLabel>
                <div className={styles.categoryGrid}>
                    {categoryOptions.map((cat) => {
                        const selected = createCategory === cat;
                        return (
                            <button
                                key={cat}
                                type="button"
                                className={`${styles.categoryBtn} ${selected ? styles.categoryBtnSelected : ''}`}
                                onClick={() => setCreateCategory(cat)}
                                aria-label={`Category ${cat}`}
                                title={cat}
                            >
                                <Icon icon={cat} size={20} color="grey" />
                            </button>
                        );
                    })}
                </div>
            </div>

            <div className={styles.field}>
                <InputLabel>Select date</InputLabel>
                <DatePicker value={createDate} onChange={setCreateDate} />
            </div>

            <div className={styles.drawerFooter}>
                <button type="button" className={styles.closeFab} onClick={onClose} aria-label="Close" title="Close">
                    ×
                </button>
                <Button type="submit" disabled={creating}>
                    {creating ? (editingExpenseId ? 'Updating…' : 'Creating…') : (editingExpenseId ? 'Update' : 'Create')}
                </Button>
            </div>
        </form>
    </aside>
);
