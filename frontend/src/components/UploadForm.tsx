import { useState } from 'react';
import { Link } from 'react-router-dom';

const UploadForm = () => {
    const [files, setFiles] = useState<File[]>([]);
    const [batchId, setBatchId] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [isUploading, setIsUploading] = useState(false);
    const [analysisType, setAnalysisType] = useState('plagiarism');

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) setFiles(Array.from(e.target.files));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (files.length === 0) return;

        setIsUploading(true);
        setError(null);
        setBatchId(null);

        const formData = new FormData();
        files.forEach(file => formData.append('files', file));

        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`/api/v1/documents/upload?analysis_type=${analysisType}`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` },
                body: formData,
            });

            if (!response.ok) throw new Error('Upload failed');

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
        <div style={{ padding: '40px 0', maxWidth: '800px', margin: '0 auto' }}>
            <div style={{ marginBottom: '40px' }}>
                <h1 style={{ fontSize: '36px', fontWeight: 700, marginBottom: '8px' }}>Upload Documents</h1>
                <p style={{ color: 'var(--text-secondary)' }}>Upload files, folders, or archives for analysis</p>
            </div>

            <div className="glass" style={{ padding: '32px' }}>
                <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                    {/* Analysis Type */}
                    <div>
                        <label style={{ display: 'block', marginBottom: '12px', fontSize: '14px', fontWeight: 500 }}>Analysis Type</label>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px' }}>
                            {['plagiarism', 'ai', 'both'].map(type => (
                                <label key={type} style={{ cursor: 'pointer' }}>
                                    <input
                                        type="radio"
                                        name="analysisType"
                                        value={type}
                                        checked={analysisType === type}
                                        onChange={(e) => setAnalysisType(e.target.value)}
                                        style={{ display: 'none' }}
                                    />
                                    <div className="card" style={{
                                        textAlign: 'center',
                                        padding: '16px',
                                        border: analysisType === type ? '1px solid var(--primary)' : '1px solid var(--glass-border)',
                                        background: analysisType === type ? 'rgba(99, 102, 241, 0.1)' : 'var(--glass)'
                                    }}>
                                        <span style={{ textTransform: 'capitalize', fontSize: '14px', fontWeight: 500 }}>{type}</span>
                                    </div>
                                </label>
                            ))}
                        </div>
                    </div>

                    {/* Upload Area */}
                    <div>
                        <label style={{ display: 'block', marginBottom: '12px', fontSize: '14px', fontWeight: 500 }}>Files</label>
                        <label style={{
                            display: 'block',
                            padding: '48px',
                            border: '2px dashed var(--glass-border)',
                            borderRadius: '12px',
                            textAlign: 'center',
                            cursor: 'pointer',
                            transition: 'all 0.3s'
                        }}>
                            <div style={{ fontSize: '48px', marginBottom: '16px' }}>📤</div>
                            <p style={{ color: 'var(--text-secondary)', marginBottom: '8px' }}>
                                <span style={{ color: 'var(--primary)' }}>Click to upload</span> or drag and drop
                            </p>
                            <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>PDF, DOCX, TXT, ZIP, TAR</p>
                            <input
                                type="file"
                                multiple
                                onChange={handleFileChange}
                                style={{ display: 'none' }}
                            />
                        </label>
                    </div>

                    {/* File List */}
                    {files.length > 0 && (
                        <div>
                            <p style={{ fontSize: '14px', marginBottom: '12px', color: 'var(--text-secondary)' }}>Selected: {files.length} files</p>
                            <div style={{ maxHeight: '150px', overflowY: 'auto' }}>
                                {files.map((file, i) => (
                                    <div key={i} style={{ padding: '8px 12px', background: 'rgba(255, 255, 255, 0.03)', borderRadius: '6px', fontSize: '13px', marginBottom: '6px' }}>
                                        {file.name} <span style={{ color: 'var(--text-muted)' }}>({(file.size / 1024).toFixed(1)} KB)</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    <button type="submit" className="btn-primary" disabled={files.length === 0 || isUploading} style={{ width: '100%', justifyContent: 'center' }}>
                        {isUploading ? 'Uploading...' : 'Upload & Analyze'}
                    </button>
                </form>

                {batchId && (
                    <div style={{ marginTop: '24px', padding: '16px', background: 'rgba(34, 197, 94, 0.1)', border: '1px solid rgba(34, 197, 94, 0.3)', borderRadius: '12px' }}>
                        <p style={{ fontSize: '14px', marginBottom: '8px', color: '#22c55e' }}>✓ Upload successful!</p>
                        <Link to={`/results/${batchId}`} style={{ color: 'var(--primary)', fontSize: '14px' }}>View results →</Link>
                    </div>
                )}

                {error && (
                    <div style={{ marginTop: '24px', padding: '16px', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '12px', color: '#ef4444', fontSize: '14px' }}>
                        {error}
                    </div>
                )}
            </div>
        </div>
    );
};

export default UploadForm;
