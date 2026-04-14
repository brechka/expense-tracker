import React, { useCallback, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { logout } from '@/utils/api';
import { Loader, Logo, UploadInvoiceModal } from '@/components';
import { useExpenses } from './useExpenses';
import { useExpenseForm } from './useExpenseForm';
import { ExpenseTable } from './ExpenseTable';
import { ExpenseMobileList } from './ExpenseMobileList';
import { ExpenseDrawer } from './ExpenseDrawer';
import styles from './Expenses.module.css';

const Expenses: React.FC = () => {
    const navigate = useNavigate();
    const [uploadModalOpen, setUploadModalOpen] = useState(false);

    const {
        expenses, setExpenses, loading, error,
        menuOpenId, draggedExpenseId, dragOverExpenseId,
        handleToggleMenu, handleDeleteExpense,
        handleDragStart, handleDragOver, handleDragLeave, handleDrop, handleDragEnd,
    } = useExpenses();

    const form = useExpenseForm(setExpenses);

    const handleSignOut = useCallback(async () => {
        await logout();
        navigate('/sign-in');
    }, [navigate]);

    const handleEdit = useCallback((expense: typeof expenses[0]) => {
        form.handleEditExpense(expense);
        // close the action menu after opening drawer
    }, [form]);

    const handleEditFromMenu = useCallback((expense: typeof expenses[0]) => {
        handleEdit(expense);
    }, [handleEdit]);

    return (
        <div className={styles.page}>
            <header className={styles.header}>
                <div className={styles.logoWrap} aria-label="YAET">
                    <Logo />
                </div>
                <div className={styles.headerActions}>
                    <Link to="/profile" className={styles.headerTextAction}>Profile</Link>
                    <button className={styles.headerTextAction} type="button" onClick={handleSignOut}>Log out</button>
                </div>
            </header>

            <div className={styles.layout}>
                <main className={styles.content}>
                    <div className={styles.tableCard}>
                        {loading ? (
                            <div className={styles.loadingWrapper}><Loader /></div>
                        ) : error ? (
                            <div className={styles.errorWrapper}>
                                <div className={styles.errorBanner}>{error}</div>
                            </div>
                        ) : expenses.length === 0 ? (
                            <div className={styles.emptyWrap}>
                                <div className={styles.emptyTitle}>The list of transactions are empty</div>
                                <p className={styles.emptySubtitle}>
                                    start to add a new one&nbsp; by clicking add button in the left bottom corner of your screen
                                </p>
                                <img className={styles.emptyImg} src="/no_transactions.svg" alt="No transactions" />
                            </div>
                        ) : (
                            <>
                                <ExpenseTable
                                    expenses={expenses}
                                    menuOpenId={menuOpenId}
                                    draggedExpenseId={draggedExpenseId}
                                    dragOverExpenseId={dragOverExpenseId}
                                    onToggleMenu={handleToggleMenu}
                                    onEdit={handleEditFromMenu}
                                    onDelete={handleDeleteExpense}
                                    onDragStart={handleDragStart}
                                    onDragOver={handleDragOver}
                                    onDragLeave={handleDragLeave}
                                    onDrop={handleDrop}
                                    onDragEnd={handleDragEnd}
                                />
                                <ExpenseMobileList
                                    expenses={expenses}
                                    draggedExpenseId={draggedExpenseId}
                                    dragOverExpenseId={dragOverExpenseId}
                                    onDragStart={handleDragStart}
                                    onDragOver={handleDragOver}
                                    onDragLeave={handleDragLeave}
                                    onDrop={handleDrop}
                                    onDragEnd={handleDragEnd}
                                />
                            </>
                        )}
                    </div>
                </main>

                <button type="button" className={styles.fab} aria-label="Add transaction" title="Add" onClick={form.handleDrawerOpen}>
                    +
                </button>

                {form.drawerOpen && <div className={styles.backdrop} onClick={form.handleDrawerClose} />}

                {form.drawerOpen && (
                    <ExpenseDrawer
                        editingExpenseId={form.editingExpenseId}
                        createName={form.createName}
                        setCreateName={form.setCreateName}
                        createAmount={form.createAmount}
                        setCreateAmount={form.setCreateAmount}
                        createCurrency={form.createCurrency}
                        setCreateCurrency={form.setCreateCurrency}
                        createCategory={form.createCategory}
                        setCreateCategory={form.setCreateCategory}
                        createDate={form.createDate}
                        setCreateDate={form.setCreateDate}
                        creating={form.creating}
                        createError={form.createError}
                        onSubmit={form.handleCreateExpense}
                        onClose={form.handleDrawerClose}
                        onUploadInvoice={() => setUploadModalOpen(true)}
                    />
                )}

                <UploadInvoiceModal
                    isOpen={uploadModalOpen}
                    onClose={() => setUploadModalOpen(false)}
                    onUploadSuccess={form.handleInvoiceUploadSuccess}
                />
            </div>
        </div>
    );
};

export default Expenses;
