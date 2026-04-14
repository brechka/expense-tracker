import {
  formatDate,
  formatCategory,
  getCurrencySymbol,
  formatAmount,
  getTodayDateString,
  formatDateForInput,
  categoryOptions,
  currencyOptions,
} from '@/pages/Expenses/constants';

describe('constants', () => {
  it('categoryOptions has 10 entries', () => {
    expect(categoryOptions).toHaveLength(10);
  });

  it('currencyOptions has USD, EUR, PLN', () => {
    expect([...currencyOptions]).toEqual(['USD', 'EUR', 'PLN']);
  });
});

describe('formatDate', () => {
  it('returns "-" for null', () => {
    expect(formatDate(null)).toBe('-');
  });

  it('returns "-" for invalid date', () => {
    expect(formatDate('not-a-date')).toBe('-');
  });

  it('formats a valid ISO date', () => {
    const result = formatDate('2024-03-15T00:00:00.000Z');
    expect(result).toBeTruthy();
    expect(result).not.toBe('-');
  });
});

describe('formatCategory', () => {
  it('returns empty string for empty input', () => {
    expect(formatCategory('')).toBe('');
  });

  it('capitalises single word', () => {
    expect(formatCategory('hobby')).toBe('Hobby');
  });

  it('capitalises and joins underscored words', () => {
    expect(formatCategory('other_payment')).toBe('Other Payment');
  });
});

describe('getCurrencySymbol', () => {
  it('returns $ for USD', () => {
    expect(getCurrencySymbol('USD')).toBe('$');
  });

  it('returns € for EUR', () => {
    expect(getCurrencySymbol('EUR')).toBe('€');
  });

  it('returns zł for PLN', () => {
    expect(getCurrencySymbol('PLN')).toBe('zł');
  });

  it('returns raw code for unknown currency', () => {
    expect(getCurrencySymbol('GBP')).toBe('GBP');
  });
});

describe('formatAmount', () => {
  it('formats USD amount', () => {
    expect(formatAmount(100, 'USD')).toBe('-$100');
  });

  it('formats EUR amount', () => {
    expect(formatAmount(50, 'EUR')).toBe('-€50');
  });

  it('handles non-finite amount', () => {
    expect(formatAmount(NaN, 'USD')).toBe('-$NaN');
  });
});

describe('getTodayDateString', () => {
  it('returns YYYY-MM-DD format', () => {
    expect(getTodayDateString()).toMatch(/^\d{4}-\d{2}-\d{2}$/);
  });
});

describe('formatDateForInput', () => {
  it('returns today for null', () => {
    expect(formatDateForInput(null)).toBe(getTodayDateString());
  });

  it('returns today for invalid date', () => {
    expect(formatDateForInput('invalid')).toBe(getTodayDateString());
  });

  it('formats valid ISO date to YYYY-MM-DD', () => {
    expect(formatDateForInput('2024-06-01T12:00:00Z')).toBe('2024-06-01');
  });
});
