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
            <div>
                <h2 className="text-3xl font-bold text-text-primary mb-8">Results for Batch {batchId}</h2>
                <p className="text-text-secondary">Loading...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div>
                <h2 className="text-3xl font-bold text-text-primary mb-8">Error</h2>
                <div className="p-4 bg-red-900 bg-opacity-50 rounded-lg">
                    <p className="text-sm font-medium text-red-400">{error}</p>
                </div>
            </div>
        );
    }

    return (
        <div>
            <h2 className="text-3xl font-bold text-color-text-primary mb-8">Results for Batch {batchId}</h2>
            {results.length === 0 ? (
                <p className="text-color-text-secondary">No results found for this batch.</p>
            ) : (
                <div className="space-y-4">
                    {results.map((result, index) => (
                        <div key={index} className="p-6 bg-color-surface rounded-lg shadow-lg">
                            <h3 className="text-xl font-bold text-color-primary">{result.document_name}</h3>
                            <p className="text-color-text-secondary">Similarity: {(result.similarity * 100).toFixed(2)}%</p>
                            <p className="text-color-text-secondary mt-2">
                                Compared to: {result.similar_document_name}
                            </p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default ResultsPage;
