import React, { useState } from 'react';

const UploadForm: React.FC = () => {
    const [files, setFiles] = useState<FileList | null>(null);
    const [batchId, setBatchId] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFiles(e.target.files);
    };

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (!files) return;

        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }

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
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            setBatchId(data.data.batch_id);
            setError(null);
        } catch (e: any) {
            console.error(e);
            setError(e.message);
        }
    };

    return (
        <div className="max-w-xl mx-auto p-8 bg-dark-blue rounded-lg shadow-lg">
            <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                    <label htmlFor="file-upload" className="block text-sm font-medium text-gray-300">
                        Select files to upload
                    </label>
                    <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-600 border-dashed rounded-md">
                        <div className="space-y-1 text-center">
                            <svg className="mx-auto h-12 w-12 text-gray-500" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
                                <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                            </svg>
                            <div className="flex text-sm text-gray-400">
                                <label htmlFor="file-upload" className="relative cursor-pointer bg-dark-blue rounded-md font-medium text-brand-purple hover:text-brand-pink focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-brand-purple">
                                    <span>Upload a file</span>
                                    <input id="file-upload" name="file-upload" type="file" multiple className="sr-only" onChange={handleFileChange} />
                                </label>
                                <p className="pl-1">or drag and drop</p>
                            </div>
                            <p className="text-xs text-gray-500">
                                DOCX, PDF, TXT up to 10MB
                            </p>
                        </div>
                    </div>
                </div>

                <div>
                    <button
                        type="submit"
                        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-gradient-to-r from-brand-purple to-brand-pink hover:from-brand-pink hover:to-brand-purple focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-purple"
                    >
                        Upload
                    </button>
                </div>
            </form>
            {batchId && (
                <div className="mt-4 p-4 bg-light-blue rounded-lg">
                    <p className="text-sm font-medium text-green-400">Upload successful!</p>
                    <p className="text-sm text-gray-300">Batch ID: {batchId}</p>
                </div>
            )}
            {error && (
                <div className="mt-4 p-4 bg-light-blue rounded-lg">
                    <p className="text-sm font-medium text-red-400">Upload failed</p>
                    <p className="text-sm text-gray-300">{error}</p>
                </div>
            )}
        </div>
    );
};

export default UploadForm;
