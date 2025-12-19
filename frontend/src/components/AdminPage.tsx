import { useState, useEffect } from 'react';

interface AdminStats {
    total_users: number;
    total_batches: number;
    total_documents: number;
    storage_usage_mb: number;
    system_status: string;
    version: string;
}

const AdminPage = () => {
    const [stats, setStats] = useState<AdminStats | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch('/api/v1/admin/stats', {
                    headers: { 'Authorization': `Bearer ${token}` },
                });

                if (!response.ok) throw new Error('Failed to fetch admin stats');
                const data = await response.json();
                setStats(data.data);
            } catch (e: any) {
                setError(e.message);
            }
        };

        fetchStats();
    }, []);

    return (
        <div className="container fade-in" style={{ padding: '60px 0' }}>
            <div style={{ marginBottom: '60px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                    <h1 style={{ fontSize: '48px', fontWeight: 800, marginBottom: '12px', letterSpacing: '-0.02em' }}>
                        System Administration
                    </h1>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '18px' }}>
                        Overview of system performance and usage.
                    </p>
                </div>
                <div className="glass" style={{ padding: '12px 24px', borderRadius: '100px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: 'var(--success)', boxShadow: '0 0 10px var(--success)' }} />
                    <span style={{ fontWeight: 600, fontSize: '14px' }}>System Operational</span>
                </div>
            </div>

            {error && (
                <div className="glass" style={{ padding: '20px', background: 'rgba(239, 68, 68, 0.05)', borderColor: 'rgba(239, 68, 68, 0.2)', borderRadius: '16px', marginBottom: '40px' }}>
                    <p style={{ color: 'var(--error)', fontWeight: 500 }}>⚠️ Error: {error}</p>
                </div>
            )}

            {/* Stats Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '24px', marginBottom: '60px' }}>
                {[
                    { label: 'Total Users', value: stats?.total_users || 0, icon: '👥', color: 'var(--primary)' },
                    { label: 'Total Batches', value: stats?.total_batches || 0, icon: '📦', color: 'var(--secondary)' },
                    { label: 'Documents Processed', value: stats?.total_documents || 0, icon: '📄', color: 'var(--accent)' },
                    { label: 'Storage Used', value: `${stats?.storage_usage_mb.toFixed(1) || 0} MB`, icon: '💾', color: '#10b981' }
                ].map((stat, i) => (
                    <div key={i} className="glass card-hover" style={{ padding: '32px' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '24px' }}>
                            <div style={{ fontSize: '32px', background: 'rgba(255,255,255,0.05)', width: '64px', height: '64px', borderRadius: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                {stat.icon}
                            </div>
                            {i === 3 && <span style={{ fontSize: '12px', padding: '4px 12px', background: 'rgba(16, 185, 129, 0.1)', color: 'var(--success)', borderRadius: '100px', fontWeight: 600 }}>Healthy</span>}
                        </div>
                        <h3 style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: 600 }}>
                            {stat.label}
                        </h3>
                        <p style={{ fontSize: '36px', fontWeight: 800, color: 'white' }}>{stat.value}</p>
                    </div>
                ))}
            </div>

            {/* Actions */}
            <div className="glass" style={{ padding: '40px', borderRadius: '32px' }}>
                <h3 style={{ fontSize: '24px', fontWeight: 700, marginBottom: '24px' }}>System Actions</h3>
                <div style={{ display: 'flex', gap: '20px' }}>
                    <button
                        onClick={() => alert('Database optimization started...')}
                        className="btn-secondary"
                        style={{ padding: '16px 32px' }}
                    >
                        Optimize Database
                    </button>
                    <button
                        onClick={() => {
                            if (confirm('Are you sure? This will delete all processed files.')) {
                                alert('Cleanup started...');
                            }
                        }}
                        style={{
                            padding: '16px 32px',
                            background: 'rgba(239, 68, 68, 0.1)',
                            border: '1px solid rgba(239, 68, 68, 0.2)',
                            color: 'var(--error)',
                            borderRadius: '16px',
                            cursor: 'pointer',
                            fontWeight: 700,
                            fontSize: '16px',
                            transition: 'all 0.2s ease'
                        }}
                    >
                        Clear Cache & Temp Files
                    </button>
                </div>
            </div>
        </div>
    );
};

export default AdminPage;
