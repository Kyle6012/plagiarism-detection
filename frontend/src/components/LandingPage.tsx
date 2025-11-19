import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const LandingPage: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen">
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-96 h-96 bg-color-primary opacity-10 rounded-full blur-3xl"></div>
        <div className="absolute top-1/2 -left-40 w-96 h-96 bg-color-accent opacity-10 rounded-full blur-3xl"></div>
      </div>

      <section className="container mx-auto px-4 py-20">
        <div className="text-center max-w-4xl mx-auto">
          <div className="inline-block mb-4 px-4 py-2 bg-color-primary bg-opacity-10 border border-color-primary border-opacity-30 rounded-full text-color-primary text-sm font-semibold">
            Advanced AI-Powered Detection
          </div>
          <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
            Uncover the Truth in <span className="text-color-primary">Your Text</span>
          </h1>
          <p className="text-xl text-color-text-secondary mb-10 leading-relaxed max-w-2xl mx-auto">
            The most advanced plagiarism and AI-generated content detection system.
            Protect academic integrity and ensure originality with cutting-edge technology.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            {isAuthenticated ? (
              <Link
                to="/dashboard"
                className="btn-primary inline-flex items-center"
              >
                Go to Dashboard
                <svg className="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </Link>
            ) : (
              <>
                <Link
                  to="/register"
                  className="btn-primary inline-flex items-center"
                >
                  Get Started Free
                  <svg className="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </Link>
                <Link
                  to="/login"
                  className="btn-secondary inline-flex items-center"
                >
                  Sign In
                </Link>
              </>
            )}
          </div>
        </div>
      </section>

      <section className="container mx-auto px-4 py-20">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="card text-center group">
            <div className="w-16 h-16 mx-auto mb-4 bg-color-primary bg-opacity-10 rounded-2xl flex items-center justify-center group-hover:bg-opacity-20 transition-all">
              <svg className="w-8 h-8 text-color-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold mb-3 text-color-text-primary">Plagiarism Detection</h3>
            <p className="text-color-text-secondary leading-relaxed">
              Compare documents against millions of sources to identify potential plagiarism with high accuracy.
            </p>
          </div>

          <div className="card text-center group">
            <div className="w-16 h-16 mx-auto mb-4 bg-color-accent bg-opacity-10 rounded-2xl flex items-center justify-center group-hover:bg-opacity-20 transition-all">
              <svg className="w-8 h-8 text-color-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold mb-3 text-color-text-primary">AI Content Detection</h3>
            <p className="text-color-text-secondary leading-relaxed">
              Identify AI-generated text using advanced machine learning models and behavioral analysis.
            </p>
          </div>

          <div className="card text-center group">
            <div className="w-16 h-16 mx-auto mb-4 bg-color-success bg-opacity-10 rounded-2xl flex items-center justify-center group-hover:bg-opacity-20 transition-all">
              <svg className="w-8 h-8 text-color-success" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold mb-3 text-color-text-primary">Fast & Accurate</h3>
            <p className="text-color-text-secondary leading-relaxed">
              Get results in seconds with industry-leading accuracy and comprehensive reporting.
            </p>
          </div>
        </div>
      </section>

      <section className="container mx-auto px-4 py-20">
        <div className="card max-w-3xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4 text-color-text-primary">How It Works</h2>
          <p className="text-color-text-secondary mb-8 text-lg">
            Our three-step process makes detection simple and efficient
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12">
            <div className="relative">
              <div className="w-12 h-12 mx-auto mb-4 bg-color-primary text-white rounded-full flex items-center justify-center font-bold text-xl">
                1
              </div>
              <h4 className="font-bold mb-2 text-color-text-primary">Upload</h4>
              <p className="text-sm text-color-text-secondary">Upload your documents in various formats</p>
            </div>
            <div className="relative">
              <div className="w-12 h-12 mx-auto mb-4 bg-color-primary text-white rounded-full flex items-center justify-center font-bold text-xl">
                2
              </div>
              <h4 className="font-bold mb-2 text-color-text-primary">Analyze</h4>
              <p className="text-sm text-color-text-secondary">AI processes and compares content</p>
            </div>
            <div className="relative">
              <div className="w-12 h-12 mx-auto mb-4 bg-color-primary text-white rounded-full flex items-center justify-center font-bold text-xl">
                3
              </div>
              <h4 className="font-bold mb-2 text-color-text-primary">Review</h4>
              <p className="text-sm text-color-text-secondary">Get detailed results and reports</p>
            </div>
          </div>
        </div>
      </section>

      <section className="container mx-auto px-4 py-20">
        <div className="card bg-gradient-to-r from-color-primary to-color-accent p-12 text-center">
          <h2 className="text-3xl font-bold mb-4 text-white">Ready to Get Started?</h2>
          <p className="text-white text-opacity-90 mb-8 text-lg max-w-2xl mx-auto">
            Join thousands of educators and institutions protecting academic integrity
          </p>
          {isAuthenticated ? (
            <Link
              to="/upload"
              className="inline-flex items-center px-8 py-3 bg-white text-color-primary font-bold rounded-lg hover:bg-opacity-90 transition-all"
            >
              Upload Documents
              <svg className="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </Link>
          ) : (
            <Link
              to="/register"
              className="inline-flex items-center px-8 py-3 bg-white text-color-primary font-bold rounded-lg hover:bg-opacity-90 transition-all"
            >
              Sign Up Now
              <svg className="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </Link>
          )}
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
