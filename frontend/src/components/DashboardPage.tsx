import React, { useState, useEffect } from 'react';

interface DashboardMetrics {
    num_batches: number;
    num_documents: number;
}

const DashboardPage: React.FC = () => {
    const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchMetrics = async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch('/api/v1/users/me/dashboard', {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                setMetrics(data.data);
            } catch (e: any) {
                setError(e.message);
            }
        };

        fetchMetrics();
    }, []);

    return (
        <div className="max-w-4xl mx-auto mt-16 p-8 bg-dark-blue rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold text-center mb-8">My Dashboard</h2>
            {error && (
                <div className="p-4 bg-light-blue rounded-lg">
                    <p className="text-sm font-medium text-red-400">Error: {error}</p>
                </div>
            )}
            {metrics && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div className="p-8 bg-light-blue rounded-lg">
                        <h3 className="text-lg font-medium text-white">Batches Uploaded</h3>
                        <p className="mt-2 text-3xl font-bold text-brand-purple">{metrics.num_batches}</p>
                    </div>
                    <div className="p-8 bg-light-blue rounded-lg">
                        <h3 className="text-lg font-medium text-white">Documents Processed</h3>
                        <p className="mt-2 text-3xl font-bold text-brand-pink">{metrics.num_documents}</p>
                    </div>
                </div>
            )}
        </div>
    );
};

export default DashboardPage;
