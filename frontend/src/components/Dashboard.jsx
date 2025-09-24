import React, { useState, useEffect } from 'react';
import { dashboardAPI, errorHandler, authUtils } from '../api';
import NavBar from './NavBar';

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [transactionsLoading, setTransactionsLoading] = useState(false);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('overview');
  const [currentPage, setCurrentPage] = useState(1);
  const [transactionType, setTransactionType] = useState('');

  const user = authUtils.getUser();

  useEffect(() => {
    loadDashboardData();
    loadTransactions();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const data = await dashboardAPI.getUserData();
      setDashboardData(data);
      setError('');
    } catch (err) {
      setError(errorHandler.handleAuthError(err));
    } finally {
      setLoading(false);
    }
  };

  const loadTransactions = async (page = 1, type = '') => {
    try {
      setTransactionsLoading(true);
      const data = await dashboardAPI.getTransactions(page, 10, type);
      setTransactions(data.transactions || []);
      setCurrentPage(page);
      setTransactionType(type);
    } catch (err) {
      console.error('Failed to load transactions:', err);
    } finally {
      setTransactionsLoading(false);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getTransactionIcon = (type) => {
    return type === 'credit' ? '📈' : '📉';
  };

  const getTransactionColor = (type) => {
    return type === 'credit' ? 'text-green-600' : 'text-red-600';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <NavBar user={user} />
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <div className="loading-spinner border-blue-600 mb-4"></div>
            <p className="text-gray-600">Loading your dashboard...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50">
        <NavBar user={user} />
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <div className="text-red-500 text-4xl mb-4">⚠️</div>
            <p className="text-red-600 font-medium">{error}</p>
            <button 
              onClick={loadDashboardData}
              className="btn-primary mt-4"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <NavBar user={user} />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome back, {dashboardData?.user?.name}! 👋
          </h1>
          <p className="text-gray-600">
            Here's what's happening with your account today.
          </p>
        </div>

        {/* Account Balance Card */}
        <div className="balance-card mb-8 animate-slideIn">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h2 className="text-lg font-medium text-white/90 mb-1">
                Account Balance
              </h2>
              <p className="text-white/70 text-sm">
                {dashboardData?.account?.account_type}
              </p>
            </div>
            <div className="text-right">
              <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
                <span className="text-xl">💰</span>
              </div>
            </div>
          </div>
          
          <div className="mb-4">
            <h3 className="text-4xl font-bold text-white mb-2">
              {formatCurrency(dashboardData?.account?.balance || 0)}
            </h3>
            <div className="flex items-center space-x-4 text-white/80 text-sm">
              <span>Account: {dashboardData?.user?.account_number}</span>
              <span>•</span>
              <span className="flex items-center">
                <span className="w-2 h-2 bg-green-400 rounded-full mr-1"></span>
                Active
              </span>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="bg-white/10 rounded-lg p-3">
              <p className="text-white/70 text-xs mb-1">This Month</p>
              <p className="text-white font-semibold">
                {formatCurrency(dashboardData?.monthly_summary?.net_change || 0)}
              </p>
            </div>
            <div className="bg-white/10 rounded-lg p-3">
              <p className="text-white/70 text-xs mb-1">Transactions</p>
              <p className="text-white font-semibold">
                {dashboardData?.monthly_summary?.transaction_count || 0}
              </p>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="mb-6">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              {[
                { id: 'overview', label: 'Overview', icon: '📊' },
                { id: 'transactions', label: 'Transactions', icon: '💳' },
                { id: 'actions', label: 'Quick Actions', icon: '⚡' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <span className="mr-2">{tab.icon}</span>
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-fadeIn">
            {/* Monthly Summary */}
            <div className="metric-card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Monthly Summary</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Total Credits</span>
                  <span className="font-semibold text-green-600">
                    {formatCurrency(dashboardData?.monthly_summary?.total_credits || 0)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Total Debits</span>
                  <span className="font-semibold text-red-600">
                    {formatCurrency(dashboardData?.monthly_summary?.total_debits || 0)}
                  </span>
                </div>
                <div className="border-t pt-2 flex justify-between">
                  <span className="text-gray-900 font-medium">Net Change</span>
                  <span className={`font-bold ${
                    (dashboardData?.monthly_summary?.net_change || 0) >= 0 
                      ? 'text-green-600' 
                      : 'text-red-600'
                  }`}>
                    {formatCurrency(dashboardData?.monthly_summary?.net_change || 0)}
                  </span>
                </div>
              </div>
            </div>

            {/* Recent Transactions Preview */}
            <div className="metric-card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
              <div className="space-y-3">
                {dashboardData?.recent_transactions?.slice(0, 3).map((transaction, index) => (
                  <div key={index} className="flex justify-between items-center">
                    <div className="flex items-center">
                      <span className="mr-2">{getTransactionIcon(transaction.type)}</span>
                      <div>
                        <p className="text-sm font-medium text-gray-900">
                          {transaction.description}
                        </p>
                        <p className="text-xs text-gray-500">
                          {formatDate(transaction.date)}
                        </p>
                      </div>
                    </div>
                    <span className={`font-semibold ${getTransactionColor(transaction.type)}`}>
                      {transaction.type === 'credit' ? '+' : '-'}
                      {formatCurrency(transaction.amount)}
                    </span>
                  </div>
                ))}
              </div>
              <button
                onClick={() => setActiveTab('transactions')}
                className="mt-4 text-blue-600 hover:text-blue-500 text-sm font-medium"
              >
                View all transactions →
              </button>
            </div>

            {/* Account Info */}
            <div className="metric-card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Account Information</h3>
              <div className="space-y-3">
                <div>
                  <p className="text-sm text-gray-600">Account Holder</p>
                  <p className="font-medium">{dashboardData?.user?.name}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Account Number</p>
                  <p className="font-medium font-mono">{dashboardData?.user?.account_number}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Email</p>
                  <p className="font-medium">{dashboardData?.user?.email}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Member Since</p>
                  <p className="font-medium">{dashboardData?.user?.member_since}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'transactions' && (
          <div className="space-y-6 animate-fadeIn">
            {/* Transaction Filters */}
            <div className="card">
              <div className="card-body">
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
                  <h3 className="text-lg font-semibold text-gray-900">Transaction History</h3>
                  <div className="flex space-x-3">
                    <select
                      value={transactionType}
                      onChange={(e) => loadTransactions(1, e.target.value)}
                      className="input-field py-2 text-sm"
                      disabled={transactionsLoading}
                    >
                      <option value="">All Transactions</option>
                      <option value="credit">Credits Only</option>
                      <option value="debit">Debits Only</option>
                    </select>
                    <button
                      onClick={() => loadTransactions(currentPage, transactionType)}
                      className="btn-secondary py-2 px-4 text-sm"
                      disabled={transactionsLoading}
                    >
                      {transactionsLoading ? 'Loading...' : 'Refresh'}
                    </button>
                  </div>
                </div>
              </div>
            </div>

            {/* Transactions List */}
            <div className="card">
              <div className="card-body p-0">
                {transactionsLoading ? (
                  <div className="flex items-center justify-center py-12">
                    <div className="loading-spinner border-blue-600 mr-3"></div>
                    <span className="text-gray-600">Loading transactions...</span>
                  </div>
                ) : transactions.length > 0 ? (
                  <div className="divide-y divide-gray-200">
                    {transactions.map((transaction, index) => (
                      <div key={index} className="transaction-item">
                        <div className="flex items-center">
                          <div className="mr-4">
                            <span className="text-2xl">{getTransactionIcon(transaction.type)}</span>
                          </div>
                          <div className="flex-1">
                            <p className="font-medium text-gray-900">
                              {transaction.description}
                            </p>
                            <div className="flex items-center space-x-2 text-sm text-gray-500">
                              <span>{formatDate(transaction.date)}</span>
                              <span>•</span>
                              <span>ID: {transaction.id}</span>
                              <span>•</span>
                              <span className="status-badge status-success">
                                {transaction.status || 'Completed'}
                              </span>
                            </div>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className={`font-bold text-lg ${getTransactionColor(transaction.type)}`}>
                            {transaction.type === 'credit' ? '+' : '-'}
                            {formatCurrency(transaction.amount)}
                          </p>
                          {transaction.reference && (
                            <p className="text-xs text-gray-500">
                              Ref: {transaction.reference}
                            </p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-12">
                    <div className="text-gray-400 text-4xl mb-4">📭</div>
                    <p className="text-gray-600">No transactions found</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'actions' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 animate-fadeIn">
            {dashboardData?.quick_actions?.map((action, index) => (
              <div key={index} className="card hover:shadow-xl transition-shadow duration-300 cursor-pointer">
                <div className="card-body text-center">
                  <div className="text-4xl mb-4">{action.icon}</div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {action.title}
                  </h3>
                  <p className="text-gray-600 text-sm mb-4">
                    {action.description}
                  </p>
                  <button className="btn-primary w-full">
                    Get Started
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
