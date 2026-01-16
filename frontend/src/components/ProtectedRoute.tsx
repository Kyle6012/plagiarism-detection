import { useContext } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { AuthContext } from '../contexts/AuthContext';

interface ProtectedRouteProps {
  children: JSX.Element;
  requiredRole?: 'admin' | 'moderator' | 'user';
}

const ProtectedRoute = ({ children, requiredRole = 'user' }: ProtectedRouteProps) => {
  const authContext = useContext(AuthContext);
  const location = useLocation();
  
  // Check if context exists
  if (!authContext) {
    // If context is not available, redirect to login
    return <Navigate to="/login" replace />;
  }

  const { isAuthenticated, token } = authContext;

  // Check if user is authenticated
  if (!isAuthenticated || !token) {
    // Redirect to login with return url
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // If this is an admin route, we'll check the user's role via API call
  if (requiredRole === 'admin') {
    // For now, we'll just render the component and let the backend handle authorization
    // In a real app, you might want to fetch user data first to check role
    return children;
  }

  // For other roles, just check authentication
  return children;
};

export default ProtectedRoute;