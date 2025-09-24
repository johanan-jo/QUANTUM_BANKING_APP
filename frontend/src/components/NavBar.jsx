import React from 'react';
import { authUtils } from '../api';

const NavBar = ({ user }) => {
  const handleLogout = () => {
    if (window.confirm('Are you sure you want to logout?')) {
      authUtils.logout();
    }
  };

  return (
    <nav className="navbar">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and Brand */}
          <div className="flex items-center">
            <div className="flex-shrink-0 flex items-center">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center mr-3">
                <span className="text-white font-bold">🏦</span>
              </div>
              <div>
                <h1 className="text-xl font-bold gradient-text">Quantum Banking</h1>
                <p className="text-xs text-gray-500">Advanced Digital Banking</p>
              </div>
            </div>
          </div>

          {/* User Info and Actions */}
          <div className="flex items-center space-x-4">
            {/* User Welcome */}
            <div className="hidden md:block text-right">
              <p className="text-sm font-medium text-gray-900">
                Welcome back, {user?.name || 'User'}
              </p>
              <p className="text-xs text-gray-500">
                Account: {user?.account_number}
              </p>
            </div>

            {/* User Avatar */}
            <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold">
              {user?.name ? user.name.charAt(0).toUpperCase() : 'U'}
            </div>

            {/* Dropdown Menu */}
            <div className="relative">
              <button
                onClick={handleLogout}
                className="btn-danger focus-ring"
                title="Logout"
              >
                <span className="hidden sm:inline">Logout</span>
                <span className="sm:hidden">🚪</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile User Info */}
      <div className="md:hidden bg-gray-50 border-t border-gray-200 px-4 py-3">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-gray-900">
              {user?.name || 'User'}
            </p>
            <p className="text-xs text-gray-500">
              Account: {user?.account_number}
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-green-500 text-xs">●</span>
            <span className="text-xs text-gray-500">Online</span>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default NavBar;
