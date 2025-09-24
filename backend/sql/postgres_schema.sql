-- PostgreSQL Schema for Quantum Banking
-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    account_number VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    balance DECIMAL(12, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create transactions table
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(20) NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    description TEXT,
    balance_after DECIMAL(12, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_users_account_number ON users(account_number);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_transactions_user_id ON transactions(user_id);
CREATE INDEX idx_transactions_created_at ON transactions(created_at);

-- Insert sample data
INSERT INTO users (account_number, name, email, password_hash, balance) VALUES
('1234567890', 'John Doe', 'john.doe@example.com', '$2b$12$example_hash_here_1234567890123456', 6839.51),
('9876543210', 'Jane Smith', 'jane.smith@example.com', '$2b$12$example_hash_here_1234567890123456', 8435.00),
('1111222233', 'Bob Johnson', 'bob.johnson@example.com', '$2b$12$example_hash_here_1234567890123456', 3250.00);

-- Insert sample transactions
INSERT INTO transactions (user_id, type, amount, description, balance_after) VALUES
(1, 'credit', 5000.00, 'Initial deposit', 5000.00),
(1, 'credit', 1839.51, 'Salary payment', 6839.51),
(2, 'credit', 8435.00, 'Business transfer', 8435.00),
(3, 'credit', 3250.00, 'Initial balance', 3250.00);