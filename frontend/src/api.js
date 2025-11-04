/**
 * API utilities for communicating with the backend
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

/**
 * HTTP client wrapper with error handling
 */
class APIClient {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  /**
   * Get authorization headers with JWT token
   */
  getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` })
    };
  }

  /**
   * Make HTTP request with error handling
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    
    const config = {
      headers: this.getAuthHeaders(),
      ...options
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `HTTP error! status: ${response.status}`);
      }

      return data;
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      throw error;
    }
  }

  /**
   * GET request
   */
  async get(endpoint) {
    return this.request(endpoint, { method: 'GET' });
  }

  /**
   * POST request
   */
  async post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  /**
   * PUT request
   */
  async put(endpoint, data) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  /**
   * DELETE request
   */
  async delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }
}

// Create global API client instance
const api = new APIClient();

// Authentication API calls
export const authAPI = {
  /**
   * Register new user
   */
  register: async (userData) => {
    return api.post('/auth/register', userData);
  },

  /**
   * Login user and request OTP
   */
  login: async (credentials) => {
    return api.post('/auth/login', credentials);
  },

  /**
   * Verify OTP and complete login
   */
  verifyOTP: async (otpData) => {
    return api.post('/auth/verify-otp', otpData);
  },

  /**
   * Resend OTP to user's email
   */
  resendOTP: async (accountNumber) => {
    return api.post('/auth/resend-otp', { account_number: accountNumber });
  }
};

// Dashboard API calls
export const dashboardAPI = {
  /**
   * Get user dashboard data
   */
  getUserData: async () => {
    return api.get('/dashboard/me');
  },

  /**
   * Get user transactions with pagination
   */
  getTransactions: async (page = 1, limit = 10, type = '') => {
    const params = new URLSearchParams({
      page: page.toString(),
      limit: limit.toString(),
      ...(type && { type })
    });
    return api.get(`/dashboard/transactions?${params}`);
  },

  /**
   * Get account summary
   */
  getAccountSummary: async () => {
    return api.get('/dashboard/account-summary');
  }
};

// Utility functions
export const authUtils = {
  /**
   * Store authentication token
   */
  setToken: (token) => {
    localStorage.setItem('token', token);
  },

  /**
   * Get stored authentication token
   */
  getToken: () => {
    return localStorage.getItem('token');
  },

  /**
   * Remove authentication token
   */
  removeToken: () => {
    localStorage.removeItem('token');
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated: () => {
    const token = localStorage.getItem('token');
    return !!token;
  },

  /**
   * Store user data
   */
  setUser: (userData) => {
    localStorage.setItem('user', JSON.stringify(userData));
  },

  /**
   * Get stored user data
   */
  getUser: () => {
    const userData = localStorage.getItem('user');
    return userData ? JSON.parse(userData) : null;
  },

  /**
   * Clear all authentication data
   */
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  }
};

/**
 * Error handling utilities
 */
export const errorHandler = {
  /**
   * Format error message for display
   */
  formatError: (error) => {
    if (typeof error === 'string') {
      return error;
    }
    
    if (error.message) {
      return error.message;
    }
    
    return 'An unexpected error occurred. Please try again.';
  },

  /**
   * Handle authentication errors
   */
  handleAuthError: (error) => {
    const errorMessage = errorHandler.formatError(error);
    
    // If token is invalid or expired, logout user
    if (errorMessage.includes('invalid') || errorMessage.includes('expired')) {
      authUtils.logout();
      return 'Session expired. Please login again.';
    }
    
    return errorMessage;
  }
};

export default api;
