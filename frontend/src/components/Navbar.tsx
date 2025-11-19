import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const Navbar = () => {
  const { isAuthenticated, logout } = useAuth();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    window.location.href = '/';
  };

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="bg-color-surface border-b border-color-border sticky top-0 z-50 backdrop-blur-sm bg-opacity-95">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link
            to="/"
            className="flex items-center space-x-2 text-xl font-bold text-color-primary hover:text-color-primary-light transition-colors"
          >
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span>PlagDetect</span>
          </Link>

          <div className="flex items-center space-x-1">
            {isAuthenticated ? (
              <>
                <Link
                  to="/dashboard"
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    isActive('/dashboard')
                      ? 'bg-color-primary text-white'
                      : 'text-color-text-secondary hover:text-color-text-primary hover:bg-color-surface-hover'
                  }`}
                >
                  Dashboard
                </Link>
                <Link
                  to="/upload"
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    isActive('/upload')
                      ? 'bg-color-primary text-white'
                      : 'text-color-text-secondary hover:text-color-text-primary hover:bg-color-surface-hover'
                  }`}
                >
                  Upload
                </Link>
                <button
                  onClick={handleLogout}
                  className="ml-2 px-4 py-2 rounded-lg font-medium text-color-text-secondary hover:text-color-error hover:bg-color-surface-hover transition-all"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="px-4 py-2 rounded-lg font-medium text-color-text-secondary hover:text-color-text-primary hover:bg-color-surface-hover transition-all"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="ml-2 px-4 py-2 rounded-lg font-medium bg-color-primary text-white hover:bg-color-primary-hover transition-all"
                >
                  Get Started
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
