import React, { useState } from 'react';
import { authAPI, errorHandler } from '../api';

const Login = ({ onLoginSuccess, onSwitchToRegister }) => {
  const [formData, setFormData] = useState({
    account_number: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    // Clear error when user starts typing
    if (error) setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Validate input
      if (!formData.account_number || !formData.password) {
        throw new Error('Please fill in all fields');
      }

      if (formData.account_number.length !== 10 || !formData.account_number.match(/^\d+$/)) {
        throw new Error('Account number must be exactly 10 digits');
      }

      // Send login request
      const response = await authAPI.login({
        account_number: formData.account_number,
        password: formData.password
      });

      // Handle successful login request
      if (response.status === 'otp_sent') {
        onLoginSuccess(formData.account_number, response);
      }

    } catch (err) {
      setError(errorHandler.formatError(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-700 py-12 px-4 sm:px-6 lg:px-8">
      <div className="form-container animate-slideIn">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center">
              <span className="text-2xl">🏦</span>
            </div>
          </div>
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome Back
          </h2>
          <p className="text-gray-600">
            Sign in to your Quantum Banking account
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="alert alert-error mb-6 animate-fadeIn">
            <div className="flex items-center">
              <span className="text-red-500 mr-2">⚠️</span>
              <span>{error}</span>
            </div>
          </div>
        )}

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="account_number" className="block text-sm font-medium text-gray-700 mb-2">
              Account Number
            </label>
            <input
              id="account_number"
              name="account_number"
              type="text"
              placeholder="Enter your 10-digit account number"
              value={formData.account_number}
              onChange={handleChange}
              className="input-field focus-ring"
              maxLength="10"
              disabled={loading}
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              placeholder="Enter your password"
              value={formData.password}
              onChange={handleChange}
              className="input-field focus-ring"
              disabled={loading}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-primary w-full focus-ring disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <div className="flex items-center justify-center">
                <div className="loading-spinner mr-2"></div>
                Signing In...
              </div>
            ) : (
              'Sign In'
            )}
          </button>
        </form>

        {/* Additional Options */}
        <div className="mt-8 space-y-4">
          <div className="text-center">
            <button
              type="button"
              className="text-blue-600 hover:text-blue-500 text-sm font-medium"
              disabled={loading}
            >
              Forgot your password?
            </button>
          </div>

          <div className="border-t border-gray-200 pt-6">
            <div className="text-center">
              <p className="text-sm text-gray-600 mb-3">
                Don't have an account?
              </p>
              <button
                type="button"
                onClick={onSwitchToRegister}
                className="btn-secondary w-full focus-ring"
                disabled={loading}
              >
                Create New Account
              </button>
            </div>
          </div>
        </div>

        {/* Security Notice */}
        <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
          <div className="flex items-start">
            <span className="text-blue-500 mr-2 mt-0.5">🔒</span>
            <div className="text-sm text-blue-700">
              <p className="font-medium mb-1">Secure Login Process</p>
              <p>After entering your credentials, we'll send a one-time password (OTP) to your registered email for enhanced security.</p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 text-center">
          <p className="text-xs text-gray-500">
            © 2025 Quantum Banking. Secure • Reliable • Advanced
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
