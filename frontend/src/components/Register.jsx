import React, { useState } from 'react';
import { authAPI, errorHandler } from '../api';

const Register = ({ onRegisterSuccess, onSwitchToLogin }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    generatedAccountNumber: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    // Clear messages when user starts typing
    if (error) setError('');
    if (success) setSuccess('');
  };

  const validateForm = () => {
    const { name, email, password, confirmPassword } = formData;

    if (!name || !email || !password || !confirmPassword) {
      throw new Error('Please fill in all fields');
    }

    if (name.length < 2) {
      throw new Error('Name must be at least 2 characters long');
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      throw new Error('Please enter a valid email address');
    }

    if (password.length < 8) {
      throw new Error('Password must be at least 8 characters long');
    }

    if (password !== confirmPassword) {
      throw new Error('Passwords do not match');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      // Validate form
      validateForm();

      // Send registration request
      const response = await authAPI.register({
        name: formData.name.trim(),
        email: formData.email.trim().toLowerCase(),
        password: formData.password
      });

      // Handle successful registration
      setSuccess(`Registration successful! Your account number is: ${response.account_number}`);
      
      // Store account number for user reference
      setFormData(prev => ({ ...prev, generatedAccountNumber: response.account_number }));

    } catch (err) {
      setError(errorHandler.formatError(err));
    } finally {
      setLoading(false);
    }
  };

  const handleContinueToLogin = () => {
    if (formData.generatedAccountNumber) {
      onRegisterSuccess(formData.generatedAccountNumber);
    } else {
      onSwitchToLogin();
    }
  };

  const getPasswordStrength = (password) => {
    if (!password) return { strength: 0, label: '', color: '' };
    
    let strength = 0;
    if (password.length >= 8) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;

    const levels = [
      { label: 'Very Weak', color: 'bg-red-500' },
      { label: 'Weak', color: 'bg-orange-500' },
      { label: 'Fair', color: 'bg-yellow-500' },
      { label: 'Good', color: 'bg-blue-500' },
      { label: 'Strong', color: 'bg-green-500' }
    ];

    return { strength, ...levels[Math.min(strength, 4)] };
  };

  const passwordStrength = getPasswordStrength(formData.password);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-700 py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-lg mx-auto bg-white rounded-xl shadow-2xl p-8 animate-slideIn">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center">
              <span className="text-2xl">🏦</span>
            </div>
          </div>
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Create Account
          </h2>
          <p className="text-gray-600">
            Join Quantum Banking today
          </p>
        </div>

        {/* Success Message */}
        {success && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-6 animate-fadeIn">
            <div className="text-center">
              <div className="flex justify-center mb-4">
                <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center">
                  <span className="text-2xl text-white">✅</span>
                </div>
              </div>
              <h3 className="text-xl font-bold text-green-800 mb-2">
                Account Created Successfully!
              </h3>
              <p className="text-green-700 mb-4">
                Welcome to Quantum Banking! Your account is ready to use.
              </p>
              
              {/* Account Number Display */}
              {formData.generatedAccountNumber && (
                <div className="bg-white border-2 border-green-300 rounded-lg p-4 mb-4">
                  <p className="text-sm font-medium text-gray-600 mb-1">Your Account Number:</p>
                  <p className="text-2xl font-bold text-gray-900 mb-2 tracking-wider">
                    {formData.generatedAccountNumber}
                  </p>
                  <p className="text-xs text-gray-500">
                    Please save this account number securely. You'll need it for login.
                  </p>
                </div>
              )}
              
              <button
                onClick={handleContinueToLogin}
                className="btn btn-primary w-full"
                type="button"
              >
                Continue to Login
              </button>
            </div>
          </div>
        )}

        {/* Error Alert */}
        {error && (
          <div className="alert alert-error mb-6 animate-fadeIn">
            <div className="flex items-center">
              <span className="text-red-500 mr-2">⚠️</span>
              <span>{error}</span>
            </div>
          </div>
        )}

        {/* Registration Form */}
        {/* Registration Form - Hide when successful */}
        {!success && (
          <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
              Full Name
            </label>
            <input
              id="name"
              name="name"
              type="text"
              placeholder="Enter your full name"
              value={formData.name}
              onChange={handleChange}
              className="input-field focus-ring"
              disabled={loading || success}
            />
          </div>

          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
              Email Address
            </label>
            <input
              id="email"
              name="email"
              type="email"
              placeholder="Enter your email address"
              value={formData.email}
              onChange={handleChange}
              className="input-field focus-ring"
              disabled={loading || success}
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
              placeholder="Create a strong password"
              value={formData.password}
              onChange={handleChange}
              className="input-field focus-ring"
              disabled={loading || success}
            />
            
            {/* Password Strength Indicator */}
            {formData.password && (
              <div className="mt-2">
                <div className="flex items-center space-x-2">
                  <div className="flex-1 bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full transition-all duration-300 ${passwordStrength.color}`}
                      style={{ width: `${(passwordStrength.strength / 5) * 100}%` }}
                    ></div>
                  </div>
                  <span className="text-xs text-gray-600">{passwordStrength.label}</span>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  Use 8+ characters with a mix of letters, numbers & symbols
                </p>
              </div>
            )}
          </div>

          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-2">
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              placeholder="Confirm your password"
              value={formData.confirmPassword}
              onChange={handleChange}
              className="input-field focus-ring"
              disabled={loading || success}
            />
            {formData.confirmPassword && formData.password !== formData.confirmPassword && (
              <p className="text-red-500 text-xs mt-1">Passwords do not match</p>
            )}
          </div>

          <button
            type="submit"
            disabled={loading || success}
            className="btn-primary w-full focus-ring disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <div className="flex items-center justify-center">
                <div className="loading-spinner mr-2"></div>
                Creating Account...
              </div>
            ) : success ? (
              'Account Created Successfully!'
            ) : (
              'Create Account'
            )}
          </button>
        </form>
        )}

        {/* Terms and Conditions */}
        <div className="mt-6 text-center">
          <p className="text-xs text-gray-500">
            By creating an account, you agree to our{' '}
            <button className="text-blue-600 hover:text-blue-500">Terms of Service</button>
            {' '}and{' '}
            <button className="text-blue-600 hover:text-blue-500">Privacy Policy</button>
          </p>
        </div>

        {/* Switch to Login */}
        {!success && (
          <div className="mt-8 border-t border-gray-200 pt-6">
            <div className="text-center">
              <p className="text-sm text-gray-600 mb-3">
                Already have an account?
              </p>
              <button
                type="button"
                onClick={onSwitchToLogin}
                className="btn-secondary w-full focus-ring"
                disabled={loading}
              >
                Sign In Instead
              </button>
            </div>
          </div>
        )}

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

export default Register;
