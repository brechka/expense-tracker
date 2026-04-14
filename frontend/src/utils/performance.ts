/**
 * Performance monitor for tracking component render metrics.
 * Available in browser console via window.__performanceMonitor
 *
 * Usage:
 *   window.__performanceMonitor.logReport()
 *   window.__performanceMonitor.getMetrics('Expenses')
 *   window.__performanceMonitor.reset()
 */

interface RenderMetric {
  count: number;
  totalMs: number;
  lastMs: number;
}

const metrics = new Map<string, RenderMetric>();

export function trackRender(componentName: string, durationMs: number): void {
  const existing = metrics.get(componentName) || { count: 0, totalMs: 0, lastMs: 0 };
  existing.count += 1;
  existing.totalMs += durationMs;
  existing.lastMs = durationMs;
  metrics.set(componentName, existing);
}

export function getMetrics(componentName: string): RenderMetric | undefined {
  return metrics.get(componentName);
}

export function logReport(): void {
  console.table(
    Array.from(metrics.entries()).map(([name, m]) => ({
      Component: name,
      Renders: m.count,
      'Total (ms)': m.totalMs.toFixed(2),
      'Avg (ms)': (m.totalMs / m.count).toFixed(2),
      'Last (ms)': m.lastMs.toFixed(2),
    }))
  );
}

export function reset(): void {
  metrics.clear();
}

if (typeof window !== 'undefined') {
  (window as unknown as Record<string, unknown>).__performanceMonitor = { trackRender, getMetrics, logReport, reset };
}
