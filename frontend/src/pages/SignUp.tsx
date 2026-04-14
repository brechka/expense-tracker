import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { Button, Input, PasswordInput } from '../components';
import { AuthLayout } from '../layouts';
import { apiClient, setAccessToken } from '../utils/api';

interface SignUpFormData {
  name: string;
  email: string;
  password: string;
}

const signUpSchema = yup.object({
  name: yup
    .string()
    .required('Name is required')
    .min(2, 'Name must be at least 2 characters')
    .max(100, 'Name must not exceed 100 characters'),
  email: yup
    .string()
    .required('Email is required')
    .email('Please enter a valid email address'),
  password: yup
    .string()
    .required('Password is required')
    .min(8, 'Password must be at least 8 characters'),
});

const SignUp: React.FC = () => {
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<SignUpFormData>({
    resolver: yupResolver(signUpSchema),
    mode: 'onSubmit',
  });

  const onSubmit = async (data: SignUpFormData) => {
    setIsSubmitting(true);
    setSubmitError(null);
    setSuccessMessage(null);

    try {
      const res = await apiClient.post<{ access_token: string }>('/api/auth/sign-up', {
        name: data.name,
        email: data.email,
        password: data.password,
      });

      setAccessToken(res.data.access_token);
      navigate('/', { replace: true });
    } catch (error) {
      setSubmitError(
        error instanceof Error
          ? error.message
          : 'Registration failed. Please try again.'
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <AuthLayout>
      <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 700, color: '#2d3748', margin: '0 0 0.5rem 0' }}>
          Welcome to us,
        </h1>
        <p style={{ color: '#718096', fontSize: '0.95rem', margin: 0 }}>
          Hello there, create new account
        </p>
      </div>

      {successMessage && (
        <div style={{
          padding: '12px', backgroundColor: '#d1fae5', color: '#065f46',
          borderRadius: '8px', marginBottom: '1rem', fontSize: '0.9rem', textAlign: 'center'
        }}>
          {successMessage}
        </div>
      )}

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
          name="name"
          control={control}
          render={({ field }) => (
            <Input
              placeholder="Name"
              value={field.value}
              onChange={field.onChange}
              onBlur={field.onBlur}
              error={!!errors.name}
              helperText={errors.name?.message}
            />
          )}
        />

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
            />
          )}
        />

        <p style={{ fontSize: '0.8rem', color: '#718096', margin: '0 0 0.5rem 0' }}>
          By creating an account you agree to our{' '}
          <span style={{ color: '#667eea', cursor: 'pointer' }}>Terms and Conditions</span>
        </p>

        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Signing Up...' : 'Sign Up'}
        </Button>
      </form>

      <div style={{ textAlign: 'center', color: '#718096', fontSize: '0.9rem' }}>
        <p>
          Already have an account?{' '}
          <Link to="/sign-in" style={{ color: '#667eea', textDecoration: 'none', fontWeight: 600 }}>
            Sign In
          </Link>
        </p>
      </div>
    </AuthLayout>
  );
};

export default SignUp;
