import { initSentry } from '@/utils/sentry';

describe('Sentry', () => {
  it('initSentry does not throw when no DSN', () => {
    expect(() => initSentry()).not.toThrow();
  });
});
