import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const LandingPage = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div style={{ padding: '60px 0' }}>
      {/* Hero */}
      <div style={{ textAlign: 'center', marginBottom: '80px' }}>
        <div style={{
          display: 'inline-block',
          padding: '8px 20px',
          background: 'rgba(99, 102, 241, 0.1)',
          border: '1px solid rgba(99, 102, 241, 0.3)',
          borderRadius: '100px',
          marginBottom: '24px',
          fontSize: '14px',
          color: 'var(--primary-light)'
        }}>
          AI-Powered Detection
        </div>

        <h1 style={{ fontSize: '56px', fontWeight: 700, marginBottom: '24px', lineHeight: 1.1 }}>
          Detect Plagiarism &<br />
          <span className="gradient-text">AI-Generated Content</span>
        </h1>

        <p style={{ fontSize: '20px', color: 'var(--text-secondary)', marginBottom: '40px', maxWidth: '600px', margin: '0 auto 40px' }}>
          Advanced detection system to protect academic integrity
        </p>

        <div style={{ display: 'flex', gap: '16px', justifyContent: 'center' }}>
          {isAuthenticated ? (
            <Link to="/dashboard" className="btn-primary" style={{ textDecoration: 'none' }}>Go to Dashboard →</Link>
          ) : (
            <>
              <Link to="/register" className="btn-primary" style={{ textDecoration: 'none' }}>Get Started Free</Link>
              <Link to="/login" className="btn-ghost" style={{ textDecoration: 'none' }}>Sign In</Link>
            </>
          )}
        </div>
      </div>

      {/* Features */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px', marginBottom: '80px' }}>
        {[
          { icon: '📄', title: 'Plagiarism Detection', desc: 'Compare documents using semantic analysis' },
          { icon: '🤖', title: 'AI Detection', desc: 'Identify AI-generated text with ML models' },
          { icon: '⚡', title: 'Lightning Fast', desc: 'Get results in seconds with batch processing' }
        ].map((feature, i) => (
          <div key={i} className="card" style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '40px', marginBottom: '16px' }}>{feature.icon}</div>
            <h3 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '12px' }}>{feature.title}</h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '15px' }}>{feature.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LandingPage;
