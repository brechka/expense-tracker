import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button, Input } from '../components';
import { AuthLayout } from '../layouts';
import { apiClient } from '../utils/api';

const ForgotPassword: React.FC = () => {
  const [email, setEmail] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleSendCode = async () => {
    setSubmitError(null);
    if (!email.trim()) { setSubmitError('Please enter your email.'); return; }

    setIsSubmitting(true);
    try {
      await apiClient.post('/api/auth/forgot-password', { email });
      navigate('/verification-code', { state: { email } });
    } catch (e) {
      setSubmitError(e instanceof Error ? e.message : 'Failed to send reset code.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <AuthLayout>
      <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 700, color: '#2d3748', margin: '0 0 0.5rem 0' }}>
          Forgot password
        </h1>
        <p style={{ color: '#718096', fontSize: '0.95rem', margin: 0 }}>
          We will text you a code to verify it is you
        </p>
      </div>

      {submitError && (
        <div style={{ padding: '12px', backgroundColor: '#fee2e2', color: '#991b1b', borderRadius: '8px', marginBottom: '1rem', fontSize: '0.9rem', textAlign: 'center' }}>
          {submitError}
        </div>
      )}

      <form onSubmit={(e) => { e.preventDefault(); handleSendCode(); }} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', marginBottom: '1.25rem' }}>
        <Input type="email" placeholder="Email" onChange={setEmail} disabled={isSubmitting} />
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Sending...' : 'Send'}
        </Button>
      </form>

      <div style={{ textAlign: 'center', color: '#718096', fontSize: '0.9rem' }}>
        <Link to="/sign-in" style={{ color: '#667eea', textDecoration: 'none', fontWeight: 600 }}>← Back to Sign In</Link>
      </div>
    </AuthLayout>
  );
};

export default ForgotPassword;
