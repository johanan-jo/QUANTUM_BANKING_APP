 import React, { useState, useEffect } from 'react';
import { authUtils } from './api';

// Import components
import Login from './components/Login';
import Register from './components/Register';
import OtpVerify from './components/OtpVerify';
import Dashboard from './components/Dashboard';

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
        return isAuthenticated ? <Dashboard /> : (
          <Login
            onLoginSuccess={handleLoginSuccess}
            onSwitchToRegister={() => setCurrentView('register')}
          />
        );
      
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



export default App;
