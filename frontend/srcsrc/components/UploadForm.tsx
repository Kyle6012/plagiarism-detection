import React, { useState } from 'react';

const UploadForm: React.FC = () => {
    const [files, setFiles] = useState<FileList | null>(null);
    const [batchId, setBatchId] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        console.log("Files selected:", e.target.files);
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
            const response = await fetch('/api/v1/documents/upload', {
                method: 'POST',
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
        <div>
            <form onSubmit={handleSubmit}>
                <input type="file" multiple onChange={handleFileChange} />
                <button type="submit">Upload</button>
            </form>
            {batchId && <p>Batch ID: {batchId}</p>}
            {error && <p>Error: {error}</p>}
        </div>
    );
};

export default UploadForm;
