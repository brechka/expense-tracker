import React, { useState } from 'react';
import { Link, useLocation, useNavigate, useSearchParams } from 'react-router-dom';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { Button, PasswordInput } from '../components';
import { AuthLayout } from '../layouts';
import { apiClient } from '../utils/api';

interface RestorePasswordFormData {
  new_password: string;
  confirm_password: string;
}

const schema = yup.object({
  new_password: yup
    .string()
    .required('Password is required')
    .min(8, 'Password must be at least 8 characters'),
  confirm_password: yup
    .string()
    .required('Please confirm your password')
    .oneOf([yup.ref('new_password')], 'Passwords do not match'),
});

const RestorePassword: React.FC = () => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const location = useLocation();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const state = (location.state || {}) as { email?: string; reset_code?: string };
  const resetCode = state.reset_code || searchParams.get('code');

  const { control, handleSubmit, formState: { errors } } = useForm<RestorePasswordFormData>({
    resolver: yupResolver(schema),
    mode: 'onSubmit',
  });

  const onSubmit = async (data: RestorePasswordFormData) => {
    setSubmitError(null);
    if (!resetCode) { setSubmitError('Reset code is missing. Please restart the password reset flow.'); return; }

    setIsSubmitting(true);
    try {
      await apiClient.post('/api/auth/restore-password', {
        reset_code: resetCode,
        new_password: data.new_password,
      });
      navigate('/success');
    } catch (e) {
      setSubmitError(e instanceof Error ? e.message : 'Failed to reset password.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <AuthLayout>
      <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 700, color: '#2d3748', margin: '0 0 0.5rem 0' }}>
          Change password
        </h1>
        <p style={{ color: '#718096', fontSize: '0.95rem', margin: 0 }}>Type your new password</p>
      </div>

      {submitError && (
        <div style={{ padding: '12px', backgroundColor: '#fee2e2', color: '#991b1b', borderRadius: '8px', marginBottom: '1rem', fontSize: '0.9rem', textAlign: 'center' }}>
          {submitError}
        </div>
      )}

      {!resetCode && (
        <div style={{ marginBottom: '1rem', textAlign: 'center', fontSize: '0.9rem', color: '#718096' }}>
          Missing reset code.{' '}
          <Link to="/forgot-password" style={{ color: '#667eea', textDecoration: 'none', fontWeight: 600 }}>Start over</Link>
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', marginBottom: '1.25rem' }}>
        <Controller
          name="new_password"
          control={control}
          render={({ field }) => (
            <PasswordInput
              placeholder="New password"
              value={field.value}
              onChange={field.onChange}
              onBlur={field.onBlur}
              disabled={isSubmitting || !resetCode}
              error={!!errors.new_password}
              helperText={errors.new_password?.message}
            />
          )}
        />
        <Controller
          name="confirm_password"
          control={control}
          render={({ field }) => (
            <PasswordInput
              placeholder="Confirm password"
              value={field.value}
              onChange={field.onChange}
              onBlur={field.onBlur}
              disabled={isSubmitting || !resetCode}
              error={!!errors.confirm_password}
              helperText={errors.confirm_password?.message}
            />
          )}
        />
        <Button type="submit" disabled={isSubmitting || !resetCode}>
          {isSubmitting ? 'Saving...' : 'Change password'}
        </Button>
      </form>
    </AuthLayout>
  );
};

export default RestorePassword;
