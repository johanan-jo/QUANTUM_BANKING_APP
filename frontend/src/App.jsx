 import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { authUtils } from './api';

// Import components
import Login from './components/Login';
import Register from './components/Register';
import OtpVerify from './components/OtpVerify';
import Dashboard from './components/Dashboard';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const isAuthenticated = authUtils.isAuthenticated();
  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

function App() {
  const [currentView, setCurrentView] = useState('login'); // 'login', 'register', 'otp', 'dashboard'
  const [accountNumber, setAccountNumber] = useState('');
  const [otpData, setOtpData] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check authentication status on app load
    const checkAuth = () => {
      const authenticated = authUtils.isAuthenticated();
      setIsAuthenticated(authenticated);
      if (authenticated) {
        setCurrentView('dashboard');
      }
    };

    checkAuth();
  }, []);

  // Handle login success (credentials verified, OTP sent)
  const handleLoginSuccess = (accNumber, response) => {
    setAccountNumber(accNumber);
    setOtpData(response);
    setCurrentView('otp');
  };

  // Handle registration success
  const handleRegisterSuccess = (accNumber) => {
    setAccountNumber(accNumber);
    setCurrentView('login');
  };

  // Handle OTP verification success
  const handleVerifySuccess = (response) => {
    setIsAuthenticated(true);
    setCurrentView('dashboard');
  };

  // Navigation handlers
  const switchToRegister = () => {
    setCurrentView('register');
    setAccountNumber('');
    setOtpData(null);
  };

  const switchToLogin = () => {
    setCurrentView('login');
    setAccountNumber('');
    setOtpData(null);
  };

  const backToLogin = () => {
    setCurrentView('login');
    setOtpData(null);
  };

  // Render current view based on state
  const renderCurrentView = () => {
    switch (currentView) {
      case 'register':
        return (
          <Register
            onRegisterSuccess={handleRegisterSuccess}
            onSwitchToLogin={switchToLogin}
          />
        );
      
      case 'otp':
        return (
          <OtpVerify
            accountNumber={accountNumber}
            onVerifySuccess={handleVerifySuccess}
            onBack={backToLogin}
          />
        );
      
      case 'dashboard':
        return isAuthenticated ? <Dashboard /> : <Navigate to="/login" replace />;
      
      default: // 'login'
        return (
          <Login
            onLoginSuccess={handleLoginSuccess}
            onSwitchToRegister={switchToRegister}
          />
        );
    }
  };

  return (
    <div className="App">
      {renderCurrentView()}
    </div>
  );
}

// Alternative Router-based App (uncomment to use React Router)
/*
function AppWithRouter() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/verify-otp" element={<OtpVerify />} />
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </div>
    </Router>
  );
}
*/

export default App;
