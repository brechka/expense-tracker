import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { Button, Input } from '../components';
import { AuthLayout } from '../layouts';

interface VerificationFormData {
  code: string;
}

const schema = yup.object({
  code: yup
    .string()
    .required('Reset code is required')
    .min(6, 'Reset code must be at least 6 characters')
    .max(8, 'Reset code must be at most 8 characters'),
});

const VerificationCode: React.FC = () => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const location = useLocation();
  const navigate = useNavigate();

  const state = (location.state || {}) as { email?: string };
  const email = state.email;

  const { control, handleSubmit, formState: { errors } } = useForm<VerificationFormData>({
    resolver: yupResolver(schema),
    mode: 'onSubmit',
  });

  const onSubmit = async (data: VerificationFormData) => {
    setSubmitError(null);
    setIsSubmitting(true);
    try {
      navigate('/restore-password', { state: { email, reset_code: data.code } });
    } catch (e) {
      setSubmitError(e instanceof Error ? e.message : 'Failed to continue.');
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
        <p style={{ color: '#718096', fontSize: '0.95rem', margin: 0 }}>Type a code</p>
      </div>

      <div style={{ textAlign: 'center', color: '#718096', margin: '0 0 1rem 0' }}>
        <p>We have sent you a code to verify your email<br />
          <span style={{ color: '#667eea', fontWeight: 600 }}>{email || 'your email'}</span>
        </p>
        <p style={{ fontSize: '0.9rem' }}>This code expires in 10 minutes</p>
      </div>

      {submitError && (
        <div style={{ padding: '12px', backgroundColor: '#fee2e2', color: '#991b1b', borderRadius: '8px', marginBottom: '1rem', fontSize: '0.9rem', textAlign: 'center' }}>
          {submitError}
        </div>
      )}

      {!email && (
        <div style={{ marginBottom: '1rem', textAlign: 'center', fontSize: '0.9rem', color: '#718096' }}>
          Please go back and submit your email first.{' '}
          <Link to="/forgot-password" style={{ color: '#667eea', textDecoration: 'none', fontWeight: 600 }}>Back</Link>
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', marginBottom: '1.25rem' }}>
        <Controller
          name="code"
          control={control}
          render={({ field }) => (
            <Input
              placeholder="Reset code"
              value={field.value}
              onChange={field.onChange}
              onBlur={field.onBlur}
              disabled={isSubmitting || !email}
              error={!!errors.code}
              helperText={errors.code?.message}
            />
          )}
        />
        <Button type="submit" disabled={isSubmitting || !email}>
          {isSubmitting ? 'Checking...' : 'Continue'}
        </Button>
      </form>

      <div style={{ textAlign: 'center', color: '#718096', fontSize: '0.9rem' }}>
        Change your email?{' '}
        <Link to="/forgot-password" style={{ color: '#667eea', textDecoration: 'none', fontWeight: 600 }}>Change</Link>
      </div>
    </AuthLayout>
  );
};

export default VerificationCode;
