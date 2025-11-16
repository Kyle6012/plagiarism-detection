import React, { useState } from 'react';

const LoginPage: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setError(null);
        try {
            const response = await fetch('/api/v1/auth/jwt/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    username: email,
                    password: password,
                }),
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.detail || 'Login failed');
            }

            const data = await response.json();
            localStorage.setItem('token', data.access_token);
            // Redirect to dashboard or home page
            window.location.href = '/dashboard';
        } catch (error: any) {
            setError(error.message);
        }
    };

    return (
        <div className="max-w-md mx-auto mt-16 p-8 bg-dark-blue rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold text-center mb-8">Login</h2>
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
                        autoComplete="current-password"
                        required
                        className="mt-1 block w-full px-3 py-2 bg-light-blue border border-gray-600 rounded-md text-sm shadow-sm placeholder-gray-500 focus:outline-none focus:border-brand-purple focus:ring-1 focus:ring-brand-purple"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>

                <div>
                    <button
                        type="submit"
                        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-gradient-to-r from-brand-purple to-brand-pink hover:from-brand-pink hover:to-brand-purple focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-purple"
                    >
                        Sign in
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

export default LoginPage;
