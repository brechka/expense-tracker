import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components';
import { AuthLayout } from '../layouts';

const Success: React.FC = () => {
  const navigate = useNavigate();

  return (
    <AuthLayout>
      <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '1.5rem' }}>
          <img
            src="/password_changed.svg"
            alt="Password changed successfully"
            style={{ width: '100%', maxWidth: '240px', height: 'auto' }}
          />
        </div>
        <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: '#2d3748', margin: '0 0 1rem 0' }}>
          Change password successfully!
        </h1>
        <p style={{ color: '#718096', lineHeight: 1.5, margin: '0 0 1.5rem 0' }}>
          You have successfully changed password.
          Please use the new password when logging in.
        </p>
      </div>

      <Button onClick={() => navigate('/sign-in')}>OK</Button>
    </AuthLayout>
  );
};

export default Success;
