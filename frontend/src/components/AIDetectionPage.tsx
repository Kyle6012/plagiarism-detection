import { useState } from 'react';

const AIDetectionPage = () => {
    const [text, setText] = useState('');
    const [result, setResult] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setError(null);
        setResult(null);

        try {
            const token = localStorage.getItem('token');
            const response = await fetch('/api/v1/ai-check', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text }),
            });

            if (!response.ok) throw new Error('Analysis failed');

            const data = await response.json();
            setResult(data.data);
        } catch (e: any) {
            setError(e.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="container" style={{ padding: '40px 0' }}>
            <div style={{ marginBottom: '40px' }}>
                <h1 className="text-gradient-primary" style={{ fontSize: '36px', fontWeight: 700, marginBottom: '8px' }}>AI Detection</h1>
                <p style={{ color: 'var(--text-secondary)' }}>Analyze text for AI-generated content</p>
            </div>

            <div className="glass" style={{ padding: '32px' }}>
                <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                    <div>
                        <label style={{ display: 'block', marginBottom: '12px', fontSize: '14px', fontWeight: 500 }}>Text to Analyze</label>
                        <textarea
                            value={text}
                            onChange={(e) => setText(e.target.value)}
                            placeholder="Paste the text you want to check for AI authorship..."
                            required
                            rows={10}
                            className="w-full bg-black/20 border border-white/10 rounded-xl p-4 text-white focus:outline-none focus:border-primary transition-colors"
                            style={{ width: '100%', background: 'rgba(0,0,0,0.2)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px', padding: '16px', color: 'white' }}
                        />
                    </div>

                    <button type="submit" className="btn-primary" disabled={!text.trim() || isLoading} style={{ width: '100%', justifyContent: 'center' }}>
                        {isLoading ? (
                            <>
                                <div className="spinner" style={{ width: '20px', height: '20px', border: '2px solid rgba(255,255,255,0.3)', borderTopColor: 'white', borderRadius: '50%' }}></div>
                                <span>Analyzing...</span>
                            </>
                        ) : 'Analyze Text'}
                    </button>
                </form>

                {result && (
                    <div className="fade-in" style={{ marginTop: '32px', padding: '24px', background: 'rgba(99, 102, 241, 0.1)', border: '1px solid rgba(99, 102, 241, 0.3)', borderRadius: '12px' }}>
                        <h3 style={{ fontSize: '18px', fontWeight: 600, marginBottom: '16px' }}>Analysis Results</h3>
                        <div style={{ display: 'grid', gap: '16px' }}>
                            <div>
                                <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '4px' }}>AI Probability</p>
                                <p className="text-gradient-primary" style={{ fontSize: '28px', fontWeight: 700 }}>
                                    {(result.score * 100).toFixed(1)}%
                                </p>
                            </div>
                            <div>
                                <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '4px' }}>Classification</p>
                                <p style={{ fontSize: '18px', fontWeight: 600 }}>{result.label || 'N/A'}</p>
                            </div>
                        </div>
                    </div>
                )}

                {error && (
                    <div className="fade-in" style={{ marginTop: '24px', padding: '16px', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '12px', color: '#ef4444', fontSize: '14px' }}>
                        {error}
                    </div>
                )}
            </div>
        </div>
    );
};

export default AIDetectionPage;
