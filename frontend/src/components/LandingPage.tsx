import React from 'react';
import { Link } from 'react-router-dom';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const data = [
  { name: 'Jan', Plagiarized: 20, "AI-Generated": 30 },
  { name: 'Feb', Plagiarized: 30, "AI-Generated": 40 },
  { name: 'Mar', Plagiarized: 40, "AI-Generated": 50 },
  { name: 'Apr', Plagiarized: 50, "AI-Generated": 60 },
  { name: 'May', Plagiarized: 60, "AI-Generated": 70 },
];

const LandingPage: React.FC = () => {
  return (
    <div className="text-white">
      <div className="text-center py-16">
        <h1 className="text-5xl font-bold mb-4">Uncover the Truth in Your Text</h1>
        <p className="text-xl text-gray-400 mb-8">
          The most advanced plagiarism and AI-generated content detector.
        </p>
        <div className="space-x-4">
          <Link to="/login" className="bg-gradient-to-r from-brand-purple to-brand-pink hover:from-brand-pink hover:to-brand-purple text-white font-bold py-3 px-6 rounded-lg">
            Get Started
          </Link>
          <Link to="/register" className="bg-dark-blue text-white font-bold py-3 px-6 rounded-lg">
            Learn More
          </Link>
        </div>
      </div>
      <div className="max-w-4xl mx-auto p-8 bg-dark-blue rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold text-center mb-8">Plagiarism and AI Content Detection Trends</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            <XAxis dataKey="name" stroke="#8884d8" />
            <YAxis />
            <Tooltip wrapperClassName="bg-dark-gray text-white" />
            <Legend />
            <Bar dataKey="Plagiarized" fill="#8884d8" />
            <Bar dataKey="AI-Generated" fill="#82ca9d" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default LandingPage;
