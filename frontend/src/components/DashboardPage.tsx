import React from 'react';

const DashboardPage: React.FC = () => {
    // Mock data for now
    const submissions = [
        { id: 1, filename: 'document1.txt', status: 'Processed', similarity: '15%' },
        { id: 2, filename: 'document2.docx', status: 'Processing', similarity: 'N/A' },
        { id: 3, filename: 'document3.pdf', status: 'Processed', similarity: '85%' },
    ];

    return (
        <div className="max-w-4xl mx-auto mt-16 p-8 bg-dark-blue rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold text-center mb-8">My Dashboard</h2>
            <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-600">
                    <thead className="bg-light-blue">
                        <tr>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                                Filename
                            </th>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                                Status
                            </th>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                                Similarity
                            </th>
                        </tr>
                    </thead>
                    <tbody className="bg-dark-blue divide-y divide-gray-600">
                        {submissions.map((submission) => (
                            <tr key={submission.id}>
                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-white">
                                    {submission.filename}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                                    {submission.status}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                                    {submission.similarity}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default DashboardPage;
