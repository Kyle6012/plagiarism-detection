import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

interface Metrics {
    num_batches: number;
    num_documents: number;
}

const DashboardPage = () => {
    const [metrics, setMetrics] = useState<Metrics | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchMetrics = async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch('/api/v1/users/me/dashboard', {
                    headers: { 'Authorization': `Bearer ${token}` },
                });

                if (!response.ok) throw new Error('Failed to fetch');
                const data = await response.json();
                setMetrics(data.data);
            } catch (e: any) {
                setError(e.message);
            }
        };

        fetchMetrics();
    }, []);

    const avg = metrics ? (metrics.num_documents / metrics.num_batches || 0).toFixed(1) : 0;

    return (
        <div style={{ padding: '40px 0' }}>
            <div style={{ marginBottom: '40px' }}>
                <h1 style={{ fontSize: '36px', fontWeight: 700, marginBottom: '8px' }}>Dashboard</h1>
                <p style={{ color: 'var(--text-secondary)' }}>Track your analysis activity</p>
            </div>

            {error && (
                <div style={{ padding: '16px', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '12px', marginBottom: '32px' }}>
                    <p style={{ color: '#ef4444' }}>Error: {error}</p>
                </div>
            )}

            {metrics && (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '24px', marginBottom: '48px' }}>
                    <div className="card">
                        <div style={{ fontSize: '32px', marginBottom: '12px' }}>📦</div>
                        <h3 style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '8px' }}>Total Batches</h3>
                        <p style={{ fontSize: '32px', fontWeight: 700 }}>{metrics.num_batches}</p>
                    </div>

                    <div className="card">
                        <div style={{ fontSize: '32px', marginBottom: '12px' }}>📄</div>
                        <h3 style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '8px' }}>Documents Analyzed</h3>
                        <p style={{ fontSize: '32px', fontWeight: 700 }}>{metrics.num_documents}</p>
                    </div>

                    <div className="card">
                        <div style={{ fontSize: '32px', marginBottom: '12px' }}>📊</div>
                        <h3 style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '8px' }}>Avg. per Batch</h3>
                        <p style={{ fontSize: '32px', fontWeight: 700 }}>{avg}</p>
                    </div>
                </div>
            )}

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>
                <Link to="/upload" className="card" style={{ textDecoration: 'none', color: 'inherit' }}>
                    <div style={{ fontSize: '32px', marginBottom: '12px' }}>📤</div>
                    <h3 style={{ fontSize: '18px', fontWeight: 600, marginBottom: '8px' }}>Upload Documents</h3>
                    <p style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>Check for plagiarism & AI content</p>
                </Link>

                <Link to="/ai-check" className="card" style={{ textDecoration: 'none', color: 'inherit' }}>
                    <div style={{ fontSize: '32px', marginBottom: '12px' }}>🤖</div>
                    <h3 style={{ fontSize: '18px', fontWeight: 600, marginBottom: '8px' }}>AI Detection</h3>
                    <p style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>Analyze text for AI authorship</p>
                </Link>
            </div>
        </div>
    );
};

export default DashboardPage;
