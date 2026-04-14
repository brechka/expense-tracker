import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { Button, Input, PasswordInput } from '../components';
import { AuthLayout } from '../layouts';
import { apiClient, setAccessToken } from '../utils/api';

interface SignInFormData {
  email: string;
  password: string;
}

const signInSchema = yup.object({
  email: yup
    .string()
    .required('Email is required')
    .email('Please enter a valid email address'),
  password: yup
    .string()
    .required('Password is required')
    .min(8, 'Password must be at least 8 characters'),
});

const SignIn: React.FC = () => {
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<SignInFormData>({
    resolver: yupResolver(signInSchema),
    mode: 'onSubmit',
  });

  const onSubmit = async (data: SignInFormData) => {
    setIsSubmitting(true);
    setSubmitError(null);

    try {
      const res = await apiClient.post<{ access_token: string; token_type: string }>(
        '/api/auth/sign-in',
        { email: data.email, password: data.password }
      );

      setAccessToken(res.data.access_token);
      navigate('/', { replace: true });
    } catch (error) {
      setSubmitError(
        error instanceof Error
          ? error.message
          : 'Sign in failed. Please try again.'
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <AuthLayout>
      <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 700, color: '#2d3748', margin: '0 0 0.5rem 0' }}>
          Welcome Back
        </h1>
        <p style={{ color: '#718096', fontSize: '0.95rem', margin: 0 }}>
          Hello there, sign in to continue
        </p>
      </div>

      {submitError && (
        <div style={{
          padding: '12px', backgroundColor: '#fee2e2', color: '#991b1b',
          borderRadius: '8px', marginBottom: '1rem', fontSize: '0.9rem', textAlign: 'center'
        }}>
          {submitError}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', marginBottom: '1.25rem' }}>
        <Controller
          name="email"
          control={control}
          render={({ field }) => (
            <Input
              type="email"
              placeholder="Email"
              value={field.value}
              onChange={field.onChange}
              onBlur={field.onBlur}
              error={!!errors.email}
              helperText={errors.email?.message}
              disabled={isSubmitting}
            />
          )}
        />

        <Controller
          name="password"
          control={control}
          render={({ field }) => (
            <PasswordInput
              placeholder="Password"
              value={field.value}
              onChange={field.onChange}
              onBlur={field.onBlur}
              error={!!errors.password}
              helperText={errors.password?.message}
              disabled={isSubmitting}
            />
          )}
        />

        <div style={{ textAlign: 'right', margin: '-0.5rem 0 0 0' }}>
          <Link to="/forgot-password" style={{ color: '#667eea', textDecoration: 'none', fontSize: '0.9rem' }}>
            Forgot your password?
          </Link>
        </div>

        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Signing in...' : 'Sign In'}
        </Button>
      </form>

      <div style={{ textAlign: 'center', color: '#718096', fontSize: '0.9rem' }}>
        <p>
          Don't have an account?{' '}
          <Link to="/sign-up" style={{ color: '#667eea', textDecoration: 'none', fontWeight: 600 }}>
            Sign Up
          </Link>
        </p>
      </div>
    </AuthLayout>
  );
};

export default SignIn;
