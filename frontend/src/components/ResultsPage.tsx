import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

interface Result {
    document_name: string;
    similarity: number;
    similar_document_name: string;
}

const ResultsPage: React.FC = () => {
    const { batchId } = useParams<{ batchId: string }>();
    const [results, setResults] = useState<Result[]>([]);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchResults = async () => {
            if (!batchId) return;

            try {
                const token = localStorage.getItem('token');
                const response = await fetch(`/api/v1/batch/${batchId}/results`, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                });

                if (!response.ok) {
                    const data = await response.json();
                    throw new Error(data.detail || 'Failed to fetch results');
                }

                const data = await response.json();
                setResults(data.data);
            } catch (e: unknown) {
                if (e instanceof Error) {
                    setError(e.message);
                } else {
                    setError('An unexpected error occurred');
                }
            } finally {
                setLoading(false);
            }
        };

        fetchResults();
    }, [batchId]);

    if (loading) {
        return (
            <div className="fade-in" style={{ padding: '100px 0', textAlign: 'center' }}>
                <div className="spinner" style={{ width: '60px', height: '60px', border: '4px solid rgba(99, 102, 241, 0.1)', borderTopColor: 'var(--primary)', borderRadius: '50%', margin: '0 auto 24px' }} />
                <h2 style={{ fontSize: '24px', fontWeight: 700 }}>Analyzing results...</h2>
                <p style={{ color: 'var(--text-secondary)' }}>This may take a few moments.</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="fade-in" style={{ padding: '60px 0', maxWidth: '600px', margin: '0 auto' }}>
                <div className="glass" style={{ padding: '40px', textAlign: 'center', border: '1px solid rgba(239, 68, 68, 0.2)' }}>
                    <div style={{ fontSize: '48px', marginBottom: '20px' }}>⚠️</div>
                    <h2 style={{ fontSize: '24px', fontWeight: 800, marginBottom: '12px', color: 'var(--error)' }}>Analysis Failed</h2>
                    <p style={{ color: 'var(--text-secondary)', marginBottom: '32px' }}>{error}</p>
                    <button onClick={() => window.location.reload()} className="btn-primary" style={{ margin: '0 auto' }}>Try Again</button>
                </div>
            </div>
        );
    }

    return (
        <div className="fade-in" style={{ padding: '60px 0', maxWidth: '1000px', margin: '0 auto' }}>
            <div style={{ marginBottom: '60px' }}>
                <h1 className="text-gradient" style={{ fontSize: '48px', fontWeight: 800, marginBottom: '12px', letterSpacing: '-0.02em' }}>
                    Analysis Report
                </h1>
                <p style={{ color: 'var(--text-secondary)', fontSize: '18px' }}>
                    Batch ID: <span style={{ color: 'var(--primary)', fontWeight: 700, fontFamily: 'monospace' }}>{batchId}</span>
                </p>
            </div>

            {results.length === 0 ? (
                <div className="glass" style={{ padding: '80px 40px', textAlign: 'center' }}>
                    <div style={{ fontSize: '64px', marginBottom: '24px' }}>🛡️</div>
                    <h2 style={{ fontSize: '28px', fontWeight: 800, marginBottom: '16px' }}>All Clear!</h2>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '18px', maxWidth: '500px', margin: '0 auto' }}>
                        No significant similarities or AI-generated content patterns were detected in this batch.
                    </p>
                </div>
            ) : (
                <div style={{ display: 'grid', gap: '32px' }}>
                    {results.map((result, index) => (
                        <div key={index} className="glass card-hover" style={{ padding: '40px', position: 'relative', overflow: 'hidden' }}>
                            <div style={{
                                position: 'absolute',
                                top: 0,
                                left: 0,
                                width: '6px',
                                height: '100%',
                                background: `linear-gradient(to bottom, var(--primary), var(--secondary))`
                            }} />

                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '32px', gap: '24px' }}>
                                <div style={{ flex: 1 }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
                                        <span style={{ fontSize: '24px' }}>📄</span>
                                        <h3 style={{ fontSize: '22px', fontWeight: 800, color: 'white' }}>{result.document_name}</h3>
                                    </div>
                                    <p style={{ fontSize: '16px', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                                        Detected similarity with <span style={{ color: 'white', fontWeight: 600 }}>{result.similar_document_name}</span>
                                    </p>
                                </div>
                                <div style={{ textAlign: 'right', minWidth: '120px' }}>
                                    <div style={{
                                        fontSize: '36px',
                                        fontWeight: 800,
                                        lineHeight: 1,
                                        marginBottom: '8px',
                                        color: result.similarity > 0.7 ? 'var(--error)' : result.similarity > 0.3 ? 'var(--warning)' : 'var(--success)'
                                    }}>
                                        {(result.similarity * 100).toFixed(1)}%
                                    </div>
                                    <div style={{ fontSize: '12px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.1em', fontWeight: 700 }}>
                                        Match Score
                                    </div>
                                </div>
                            </div>

                            <div style={{ width: '100%', height: '12px', background: 'rgba(255,255,255,0.03)', borderRadius: '100px', overflow: 'hidden', border: '1px solid var(--glass-border)' }}>
                                <div style={{
                                    width: `${result.similarity * 100}%`,
                                    height: '100%',
                                    background: `linear-gradient(to right, var(--primary), var(--secondary))`,
                                    borderRadius: '100px',
                                    transition: 'width 1.5s cubic-bezier(0.34, 1.56, 0.64, 1)'
                                }} />
                            </div>

                            <div style={{ marginTop: '32px', display: 'flex', gap: '16px' }}>
                                <button className="btn-secondary" style={{ padding: '10px 20px', fontSize: '14px' }}>View Details</button>
                                <button className="btn-secondary" style={{ padding: '10px 20px', fontSize: '14px' }}>Download Report</button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default ResultsPage;
