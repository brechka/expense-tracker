import React from 'react';
import { Link } from 'react-router-dom';
import { AuthLayout } from '../layouts';

const NotFound: React.FC = () => {
  return (
    <AuthLayout>
      <h1>404 - Page Not Found</h1>
      <p>The page you're looking for doesn't exist.</p>
      <Link to="/">Go Home</Link>
    </AuthLayout>
  );
};

export default NotFound;
