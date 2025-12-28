import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

const BatchResultsPage = () => {
    const { batchId } = useParams();
    const [results, setResults] = useState<any[]>([]);
    const [error, setError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        const fetchResults = async () => {
            setIsLoading(true);
            try {
                const token = localStorage.getItem('token');
                const response = await fetch(`/api/v1/batch/${batchId}/results`, {
                    headers: { 'Authorization': `Bearer ${token}` },
                });

                if (!response.ok) throw new Error('Failed to fetch results');
                const data = await response.json();
                setResults(data.data);
            } catch (e: any) {
                setError(e.message);
            } finally {
                setIsLoading(false);
            }
        };

        if (batchId) {
            fetchResults();
        }
    }, [batchId]);

    return (
        <div className="container" style={{ padding: '40px 0' }}>
            <h1 style={{ fontSize: '36px', fontWeight: 700, marginBottom: '24px' }}>
                Analysis Results for Batch <span className="text-gradient-primary">{batchId}</span>
            </h1>

            {isLoading && <p>Loading results...</p>}
            {error && <p style={{ color: 'var(--error)' }}>Error: {error}</p>}

            <div className="glass" style={{ padding: '32px' }}>
                {results.length > 0 ? (
                    <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'grid', gap: '16px' }}>
                        {results.map((result, index) => (
                            <li key={index} className="glass card-hover" style={{ padding: '24px', borderRadius: '16px' }}>
                                <h3 style={{ fontSize: '18px', fontWeight: 600, marginBottom: '12px' }}>
                                    {result.document_name}
                                </h3>
                                <p style={{ color: 'var(--text-secondary)' }}>
                                    Similarity: {(result.similarity * 100).toFixed(1)}% compared to {result.similar_document_name}
                                </p>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>No results found for this batch.</p>
                )}
            </div>
        </div>
    );
};

export default BatchResultsPage;
