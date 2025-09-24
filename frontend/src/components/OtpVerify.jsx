import React, { useState, useEffect } from 'react';
import { authAPI, errorHandler, authUtils } from '../api';

const OtpVerify = ({ accountNumber, onVerifySuccess, onBack }) => {
  const [otp, setOtp] = useState(['', '', '', '', '', '']);
  const [loading, setLoading] = useState(false);
  const [resendLoading, setResendLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [timeLeft, setTimeLeft] = useState(120); // 2 minutes in seconds
  const [canResend, setCanResend] = useState(false);

  // Timer effect
  useEffect(() => {
    if (timeLeft > 0) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    } else {
      setCanResend(true);
    }
  }, [timeLeft]);

  // Format time display
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleOtpChange = (index, value) => {
    // Only allow digits
    if (!/^\d*$/.test(value)) return;

    const newOtp = [...otp];
    newOtp[index] = value;
    setOtp(newOtp);

    // Clear messages when user starts typing
    if (error) setError('');
    if (success) setSuccess('');

    // Auto-focus next input
    if (value && index < 5) {
      const nextInput = document.getElementById(`otp-${index + 1}`);
      if (nextInput) nextInput.focus();
    }
  };

  const handleKeyDown = (index, e) => {
    // Handle backspace to move to previous input
    if (e.key === 'Backspace' && !otp[index] && index > 0) {
      const prevInput = document.getElementById(`otp-${index - 1}`);
      if (prevInput) prevInput.focus();
    }
    
    // Handle Enter to submit
    if (e.key === 'Enter') {
      handleSubmit(e);
    }
  };

  const handlePaste = (e) => {
    e.preventDefault();
    const paste = e.clipboardData.getData('text');
    const digits = paste.match(/\d/g);
    
    if (digits && digits.length >= 6) {
      const newOtp = digits.slice(0, 6);
      setOtp(newOtp);
      
      // Focus the last input
      const lastInput = document.getElementById('otp-5');
      if (lastInput) lastInput.focus();
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const otpCode = otp.join('');
      
      if (otpCode.length !== 6) {
        throw new Error('Please enter the complete 6-digit OTP');
      }

      // Verify OTP
      const response = await authAPI.verifyOTP({
        account_number: accountNumber,
        otp: otpCode
      });

      // Store authentication data
      authUtils.setToken(response.token);
      authUtils.setUser(response.user);

      setSuccess('Login successful! Redirecting to dashboard...');
      
      // Redirect to dashboard
      setTimeout(() => {
        onVerifySuccess(response);
      }, 1500);

    } catch (err) {
      setError(errorHandler.formatError(err));
      // Clear OTP on error
      setOtp(['', '', '', '', '', '']);
      const firstInput = document.getElementById('otp-0');
      if (firstInput) firstInput.focus();
    } finally {
      setLoading(false);
    }
  };

  const handleResendOtp = async () => {
    setResendLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await authAPI.resendOTP(accountNumber);
      
      if (response.status === 'otp_sent') {
        setSuccess('New OTP sent to your email!');
        setTimeLeft(120); // Reset timer
        setCanResend(false);
        
        // Clear current OTP
        setOtp(['', '', '', '', '', '']);
        const firstInput = document.getElementById('otp-0');
        if (firstInput) firstInput.focus();
      }

    } catch (err) {
      setError(errorHandler.formatError(err));
    } finally {
      setResendLoading(false);
    }
  };

  const currentOtpValue = otp.join('');
  const isComplete = currentOtpValue.length === 6;

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-700 py-12 px-4 sm:px-6 lg:px-8">
      <div className="form-container animate-slideIn">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center">
              <span className="text-2xl">📧</span>
            </div>
          </div>
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Verify Your Identity
          </h2>
          <p className="text-gray-600">
            Enter the 6-digit code sent to your email
          </p>
          <p className="text-sm text-gray-500 mt-1">
            Account: {accountNumber}
          </p>
        </div>

        {/* Success Message */}
        {success && (
          <div className="alert alert-success mb-6 animate-fadeIn">
            <div className="flex items-center">
              <span className="text-green-500 mr-2">✅</span>
              <span>{success}</span>
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

        {/* OTP Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* OTP Input Fields */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-4 text-center">
              Enter OTP Code
            </label>
            <div className="flex justify-center space-x-3">
              {otp.map((digit, index) => (
                <input
                  key={index}
                  id={`otp-${index}`}
                  type="text"
                  maxLength="1"
                  value={digit}
                  onChange={(e) => handleOtpChange(index, e.target.value)}
                  onKeyDown={(e) => handleKeyDown(index, e)}
                  onPaste={index === 0 ? handlePaste : undefined}
                  className="w-12 h-12 text-center text-xl font-bold border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  disabled={loading || success}
                />
              ))}
            </div>
          </div>

          {/* Timer Display */}
          <div className="text-center">
            {timeLeft > 0 ? (
              <p className="text-sm text-gray-600">
                OTP expires in: <span className="font-mono font-bold text-red-600">{formatTime(timeLeft)}</span>
              </p>
            ) : (
              <p className="text-sm text-red-600 font-medium">
                OTP has expired. Please request a new one.
              </p>
            )}
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading || !isComplete || success}
            className="btn-primary w-full focus-ring disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <div className="flex items-center justify-center">
                <div className="loading-spinner mr-2"></div>
                Verifying...
              </div>
            ) : success ? (
              'Verified Successfully!'
            ) : (
              'Verify OTP'
            )}
          </button>
        </form>

        {/* Resend OTP */}
        <div className="mt-6 text-center space-y-4">
          <div>
            {canResend ? (
              <button
                type="button"
                onClick={handleResendOtp}
                disabled={resendLoading || loading || success}
                className="text-blue-600 hover:text-blue-500 text-sm font-medium disabled:opacity-50"
              >
                {resendLoading ? (
                  <span className="flex items-center justify-center">
                    <div className="loading-spinner mr-2 border-blue-600"></div>
                    Sending...
                  </span>
                ) : (
                  'Resend OTP'
                )}
              </button>
            ) : (
              <p className="text-sm text-gray-500">
                Didn't receive the code? You can resend after {formatTime(timeLeft)}
              </p>
            )}
          </div>

          {/* Back Button */}
          <button
            type="button"
            onClick={onBack}
            className="text-gray-600 hover:text-gray-500 text-sm"
            disabled={loading || success}
          >
            ← Back to Login
          </button>
        </div>

        {/* Help Section */}
        <div className="mt-8 p-4 bg-blue-50 rounded-lg border border-blue-200">
          <div className="text-center">
            <h4 className="text-sm font-medium text-blue-900 mb-2">Need Help?</h4>
            <div className="text-xs text-blue-700 space-y-1">
              <p>• Check your email inbox and spam folder</p>
              <p>• Make sure you entered the latest OTP</p>
              <p>• OTP is valid for 2 minutes only</p>
              <p>• Contact support if issues persist</p>
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

export default OtpVerify;
