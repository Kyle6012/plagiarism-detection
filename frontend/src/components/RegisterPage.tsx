import React, { useState } from 'react';

const RegisterPage: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setError(null);

        if (password !== confirmPassword) {
            setError("Passwords do not match");
            return;
        }

        try {
            const response = await fetch('/api/v1/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email,
                    password,
                }),
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.detail || 'Registration failed');
            }

            // Redirect to login page
            window.location.href = '/login';
        } catch (error: any) {
            setError(error.message);
        }
    };

    return (
        <div className="max-w-md mx-auto mt-16 p-8 bg-dark-blue rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold text-center mb-8">Create an Account</h2>
            <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                    <label htmlFor="email" className="block text-sm font-medium text-gray-300">
                        Email
                    </label>
                    <input
                        id="email"
                        name="email"
                        type="email"
                        autoComplete="email"
                        required
                        className="mt-1 block w-full px-3 py-2 bg-light-blue border border-gray-600 rounded-md text-sm shadow-sm placeholder-gray-500 focus:outline-none focus:border-brand-purple focus:ring-1 focus:ring-brand-purple"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>

                <div>
                    <label htmlFor="password" className="block text-sm font-medium text-gray-300">
                        Password
                    </label>
                    <input
                        id="password"
                        name="password"
                        type="password"
                        autoComplete="new-password"
                        required
                        className="mt-1 block w-full px-3 py-2 bg-light-blue border border-gray-600 rounded-md text-sm shadow-sm placeholder-gray-500 focus:outline-none focus:border-brand-purple focus:ring-1 focus:ring-brand-purple"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>

                <div>
                    <label htmlFor="confirm-password" className="block text-sm font-medium text-gray-300">
                        Confirm Password
                    </label>
                    <input
                        id="confirm-password"
                        name="confirm-password"
                        type="password"
                        autoComplete="new-password"
                        required
                        className="mt-1 block w-full px-3 py-2 bg-light-blue border border-gray-600 rounded-md text-sm shadow-sm placeholder-gray-500 focus:outline-none focus:border-brand-purple focus:ring-1 focus:ring-brand-purple"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                    />
                </div>

                <div>
                    <button
                        type="submit"
                        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-gradient-to-r from-brand-purple to-brand-pink hover:from-brand-pink hover:to-brand-purple focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-purple"
                    >
                        Register
                    </button>
                </div>
            </form>
            {error && (
                <div className="mt-4 p-4 bg-light-blue rounded-lg">
                    <p className="text-sm font-medium text-red-400">{error}</p>
                </div>
            )}
        </div>
    );
};

export default RegisterPage;
