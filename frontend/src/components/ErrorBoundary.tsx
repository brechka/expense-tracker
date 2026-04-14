import { Component } from 'react';
import type { ErrorInfo, ReactNode } from 'react';
import { Sentry } from '../utils/sentry';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    Sentry.captureException(error, { extra: { componentStack: errorInfo.componentStack } });
  }

  render(): ReactNode {
    if (this.state.hasError) {
      if (this.props.fallback) return this.props.fallback;
      return (
        <div style={{ padding: 40, textAlign: 'center', fontFamily: 'system-ui, sans-serif' }}>
          <h1 style={{ color: '#991b1b', fontSize: '1.5rem' }}>Something went wrong</h1>
          <p style={{ color: '#6b7280' }}>{this.state.error?.message || 'An unexpected error occurred.'}</p>
          <button
            type="button"
            onClick={() => { this.setState({ hasError: false, error: null }); window.location.href = '/'; }}
            style={{ marginTop: 16, padding: '10px 24px', background: '#4338ca', color: 'white', border: 'none', borderRadius: 8, cursor: 'pointer', fontSize: 16 }}
          >
            Go Home
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
