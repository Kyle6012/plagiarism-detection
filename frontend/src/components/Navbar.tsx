import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const Navbar = () => {
  const { isAuthenticated, logout } = useAuth();

  return (
    <nav className="glass" style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      zIndex: 1000,
      padding: '16px 0'
    }}>
      <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '12px', textDecoration: 'none' }}>
          <div style={{
            width: '40px',
            height: '40px',
            background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
            borderRadius: '10px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <span style={{ fontSize: '20px' }}>📄</span>
          </div>
          <span className="gradient-text" style={{ fontSize: '20px', fontWeight: 700 }}>PlagDetect</span>
        </Link>

        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          {isAuthenticated ? (
            <>
              <Link to="/dashboard" className="btn-ghost" style={{ textDecoration: 'none' }}>Dashboard</Link>
              <Link to="/upload" className="btn-ghost" style={{ textDecoration: 'none' }}>Upload</Link>
              <Link to="/ai-check" className="btn-ghost" style={{ textDecoration: 'none' }}>AI Check</Link>
              <button className="btn-ghost" onClick={() => { logout(); window.location.href = '/'; }}>Logout</button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn-ghost" style={{ textDecoration: 'none' }}>Login</Link>
              <Link to="/register" className="btn-primary" style={{ textDecoration: 'none' }}>Get Started</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
