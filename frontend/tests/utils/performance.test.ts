import { trackRender, getMetrics, logReport, reset } from '@/utils/performance';

describe('Performance monitor', () => {
  afterEach(() => {
    reset();
  });

  it('tracks render metrics', () => {
    trackRender('TestComponent', 5.0);
    const m = getMetrics('TestComponent');
    expect(m).toBeDefined();
    expect(m!.count).toBe(1);
    expect(m!.totalMs).toBe(5.0);
    expect(m!.lastMs).toBe(5.0);
  });

  it('accumulates multiple renders', () => {
    trackRender('TestComponent', 5.0);
    trackRender('TestComponent', 10.0);
    const m = getMetrics('TestComponent');
    expect(m!.count).toBe(2);
    expect(m!.totalMs).toBe(15.0);
    expect(m!.lastMs).toBe(10.0);
  });

  it('returns undefined for unknown component', () => {
    expect(getMetrics('Unknown')).toBeUndefined();
  });

  it('reset clears all metrics', () => {
    trackRender('A', 1);
    trackRender('B', 2);
    reset();
    expect(getMetrics('A')).toBeUndefined();
    expect(getMetrics('B')).toBeUndefined();
  });

  it('logReport does not throw', () => {
    trackRender('A', 1);
    expect(() => logReport()).not.toThrow();
  });
});
