import React, { useState, useCallback } from 'react';
import { Link } from 'react-router-dom';

const UploadForm: React.FC = () => {
    const [files, setFiles] = useState<File[]>([]);
    const [batchId, setBatchId] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [isUploading, setIsUploading] = useState(false);
    const [dragIsOver, setDragIsOver] = useState(false);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setFiles(Array.from(e.target.files));
        }
    };

    const onDrop = useCallback((event: React.DragEvent<HTMLDivElement>) => {
        event.preventDefault();
        setDragIsOver(false);
        if (event.dataTransfer.files) {
            setFiles(Array.from(event.dataTransfer.files));
        }
    }, []);

    const onDragOver = useCallback((event: React.DragEvent<HTMLDivElement>) => {
        event.preventDefault();
        setDragIsOver(true);
    }, []);

    const onDragLeave = useCallback((event: React.DragEvent<HTMLDivElement>) => {
        event.preventDefault();
        setDragIsOver(false);
    }, []);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (files.length === 0) return;

        setIsUploading(true);
        setError(null);
        setBatchId(null);

        const formData = new FormData();
        files.forEach(file => {
            formData.append('files', file);
        });

        try {
            const token = localStorage.getItem('token');
            const response = await fetch('/api/v1/documents/upload', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
                body: formData,
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.detail || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            setBatchId(data.data.batch_id);
            setFiles([]);
        } catch (e: any) {
            setError(e.message);
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div>
            <h2 className="text-3xl font-bold text-color-text-primary mb-8">Upload Documents</h2>
            <div className="p-8 bg-color-surface rounded-lg shadow-lg">
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label htmlFor="file-upload" className="block text-sm font-medium text-color-text-secondary">
                            Select files to upload
                        </label>
                        <div
                            onDrop={onDrop}
                            onDragOver={onDragOver}
                            onDragLeave={onDragLeave}
                            className={`mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-dashed rounded-md ${dragIsOver ? 'border-color-primary' : 'border-color-border'}`}
                        >
                            <div className="space-y-1 text-center">
                                 {/* Icon can be added here */}
                                <div className="flex text-sm text-color-text-secondary">
                                    <label htmlFor="file-upload" className="relative cursor-pointer bg-color-surface rounded-md font-medium text-color-primary hover:text-color-primary-hover focus-within:outline-none">
                                        <span>Upload files</span>
                                        <input id="file-upload" name="file-upload" type="file" multiple className="sr-only" onChange={handleFileChange} />
                                    </label>
                                    <p className="pl-1">or drag and drop</p>
                                </div>
                                <p className="text-xs text-color-text-secondary">
                                    DOCX, PDF, TXT, etc.
                                </p>
                            </div>
                        </div>
                    </div>

                    {files.length > 0 && (
                        <div>
                            <h3 className="text-sm font-medium text-color-text-secondary">Selected files:</h3>
                            <ul className="mt-2 border border-color-border rounded-md divide-y divide-color-border">
                                {files.map((file, index) => (
                                    <li key={index} className="px-3 py-2 text-sm text-color-text-primary">{file.name}</li>
                                ))}
                            </ul>
                        </div>
                    )}

                    <div>
                        <button
                            type="submit"
                            disabled={files.length === 0 || isUploading}
                            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-color-primary hover:bg-color-primary-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-color-primary disabled:opacity-50"
                        >
                            {isUploading ? 'Uploading...' : 'Upload'}
                        </button>
                    </div>
                </form>
                {batchId && (
                    <div className="mt-4 p-4 bg-green-900 bg-opacity-50 rounded-lg text-center">
                        <p className="text-sm font-medium text-green-400">Upload successful!</p>
                        <p className="text-sm text-color-text-secondary mt-1">Batch ID: {batchId}</p>
                        <Link to={`/results/${batchId}`} className="mt-2 inline-block text-sm font-medium text-color-primary hover:underline">
                            View results
                        </Link>
                    </div>
                )}
                {error && (
                    <div className="mt-4 p-4 bg-red-900 bg-opacity-50 rounded-lg">
                        <p className="text-sm font-medium text-red-400">{error}</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default UploadForm;
