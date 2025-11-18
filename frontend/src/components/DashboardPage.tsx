import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface DashboardMetrics {
    num_batches: number;
    num_documents: number;
}

// Mock data for the chart
const chartData = [
    { name: 'Jan', documents: 400, batches: 24 },
    { name: 'Feb', documents: 300, batches: 13 },
    { name: 'Mar', documents: 200, batches: 98 },
    { name: 'Apr', documents: 278, batches: 39 },
    { name: 'May', documents: 189, batches: 48 },
    { name: 'Jun', documents: 239, batches: 38 },
    { name: 'Jul', documents: 349, batches: 43 },
];

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

    const averageDocumentsPerBatch = metrics ? (metrics.num_documents / metrics.num_batches).toFixed(2) : 0;

    return (
        <div>
            <h2 className="text-3xl font-bold text-color-text-primary mb-8">Dashboard</h2>
            {error && (
                <div className="p-4 bg-red-900 bg-opacity-50 rounded-lg">
                    <p className="text-sm font-medium text-red-400">Error: {error}</p>
                </div>
            )}
            {metrics && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div className="p-6 bg-color-surface rounded-lg shadow-lg">
                        <h3 className="text-lg font-medium text-color-text-secondary">Batches Uploaded</h3>
                        <p className="mt-2 text-4xl font-bold text-color-primary">{metrics.num_batches}</p>
                    </div>
                    <div className="p-6 bg-color-surface rounded-lg shadow-lg">
                        <h3 className="text-lg font-medium text-color-text-secondary">Documents Processed</h3>
                        <p className="mt-2 text-4xl font-bold text-color-primary">{metrics.num_documents}</p>
                    </div>
                    <div className="p-6 bg-color-surface rounded-lg shadow-lg">
                        <h3 className="text-lg font-medium text-color-text-secondary">Avg. Documents per Batch</h3>
                        <p className="mt-2 text-4xl font-bold text-color-primary">{averageDocumentsPerBatch}</p>
                    </div>
                </div>
            )}

            <div className="mt-8">
                 <h3 className="text-2xl font-bold text-color-text-primary mb-4">Activity Overview</h3>
                <div className="p-6 bg-color-surface rounded-lg shadow-lg" style={{ width: '100%', height: 400 }}>
                    <ResponsiveContainer>
                        <BarChart
                            data={chartData}
                            margin={{
                                top: 5, right: 30, left: 20, bottom: 5,
                            }}
                        >
                            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                            <XAxis dataKey="name" stroke="#9CA3AF" />
                            <YAxis stroke="#9CA3AF" />
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: '#1F2937',
                                    border: '1px solid #374151',
                                    color: '#F9FAFB',
                                }}
                            />
                            <Legend wrapperStyle={{ color: '#F9FAFB' }} />
                            <Bar dataKey="documents" fill="#6366F1" />
                            <Bar dataKey="batches" fill="#4F46E5" />
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
};

export default DashboardPage;
