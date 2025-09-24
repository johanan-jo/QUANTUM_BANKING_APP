-- Quantum Banking Database Schema
-- This file creates the complete database structure for the banking application

-- Create database (run this first)
CREATE DATABASE IF NOT EXISTS quantum_banking 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Use the database
USE quantum_banking;

-- Drop tables if they exist (for clean reinstall)
DROP TABLE IF EXISTS otps;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS users;

-- Users table - stores user account information
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    account_number VARCHAR(10) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Indexes for performance
    INDEX idx_account_number (account_number),
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
);

-- OTPs table - stores one-time passwords for authentication
CREATE TABLE otps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    otp_code VARCHAR(6) NOT NULL,
    expiry DATETIME NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraint
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    -- Indexes for performance
    INDEX idx_user_id (user_id),
    INDEX idx_otp_code (otp_code),
    INDEX idx_expiry (expiry),
    INDEX idx_used (used),
    INDEX idx_created_at (created_at),
    
    -- Composite index for OTP verification
    INDEX idx_user_otp (user_id, otp_code, used, expiry)
);

-- Transactions table - stores transaction history (optional for demo)
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    transaction_id VARCHAR(50) UNIQUE NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    transaction_type ENUM('credit', 'debit') NOT NULL,
    description VARCHAR(255) NOT NULL,
    reference_number VARCHAR(50),
    status ENUM('pending', 'completed', 'failed', 'cancelled') DEFAULT 'completed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraint
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    -- Indexes for performance
    INDEX idx_user_id (user_id),
    INDEX idx_transaction_id (transaction_id),
    INDEX idx_transaction_type (transaction_type),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at),
    
    -- Composite index for user transaction history
    INDEX idx_user_date (user_id, created_at DESC)
);

-- Insert sample user account
-- Password: "password123" (hashed with bcrypt)
-- Note: Use the provided Python script to generate proper bcrypt hash
INSERT INTO users (name, account_number, email, password_hash) VALUES
('John Doe', '1234567890', 'john.doe@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LwmFkdjSDkKwWAYQ6'),
('Jane Smith', '9876543210', 'jane.smith@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LwmFkdjSDkKwWAYQ6'),
('Bob Johnson', '1111222233', 'bob.johnson@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LwmFkdjSDkKwWAYQ6');

-- Insert sample transactions for demo
INSERT INTO transactions (user_id, transaction_id, amount, transaction_type, description, reference_number) VALUES
(1, 'TXN001001', 5000.00, 'credit', 'Salary Credit', 'SAL001'),
(1, 'TXN001002', 120.50, 'debit', 'ATM Withdrawal', 'ATM001'),
(1, 'TXN001003', 89.99, 'debit', 'Online Shopping', 'SHO001'),
(1, 'TXN001004', 2500.00, 'credit', 'Freelance Payment', 'FRE001'),
(1, 'TXN001005', 450.00, 'debit', 'Electricity Bill', 'BIL001'),

(2, 'TXN002001', 7500.00, 'credit', 'Salary Credit', 'SAL002'),
(2, 'TXN002002', 200.00, 'debit', 'Restaurant', 'RES001'),
(2, 'TXN002003', 65.00, 'debit', 'Fuel Payment', 'FUE001'),
(2, 'TXN002004', 1200.00, 'credit', 'Bonus Payment', 'BON001'),

(3, 'TXN003001', 4200.00, 'credit', 'Salary Credit', 'SAL003'),
(3, 'TXN003002', 150.00, 'debit', 'Mobile Recharge', 'MOB001'),
(3, 'TXN003003', 800.00, 'debit', 'Insurance Premium', 'INS001');

-- Create views for common queries
CREATE VIEW user_balance_summary AS
SELECT 
    u.id,
    u.name,
    u.account_number,
    u.email,
    COALESCE(
        (SELECT SUM(CASE WHEN t.transaction_type = 'credit' THEN t.amount ELSE -t.amount END)
         FROM transactions t WHERE t.user_id = u.id), 
        0
    ) as current_balance,
    COUNT(t.id) as total_transactions,
    u.created_at as account_created
FROM users u
LEFT JOIN transactions t ON u.id = t.user_id
GROUP BY u.id, u.name, u.account_number, u.email, u.created_at;

-- Create view for recent transactions
CREATE VIEW recent_transactions AS
SELECT 
    t.*,
    u.name as user_name,
    u.account_number
FROM transactions t
JOIN users u ON t.user_id = u.id
ORDER BY t.created_at DESC
LIMIT 50;

-- Performance optimization: Add additional indexes
CREATE INDEX idx_users_active ON users(is_active);
CREATE INDEX idx_otps_cleanup ON otps(expiry, used);
CREATE INDEX idx_transactions_amount ON transactions(amount);

-- Show table status
SELECT 
    'Database schema created successfully!' as message,
    COUNT(*) as sample_users
FROM users;

-- Display sample data
SELECT 'Sample Users:' as info;
SELECT 
    account_number,
    name,
    email,
    'password123' as sample_password,
    created_at
FROM users;

SELECT 'Sample Transactions:' as info;
SELECT 
    u.name,
    t.transaction_id,
    t.amount,
    t.transaction_type,
    t.description,
    t.created_at
FROM transactions t
JOIN users u ON t.user_id = u.id
ORDER BY t.created_at DESC;

-- Show current balances
SELECT 'Account Balances:' as info;
SELECT 
    name,
    account_number,
    current_balance,
    total_transactions
FROM user_balance_summary;

/* 
NOTES FOR PASSWORD GENERATION:

The sample users have password "password123" hashed with bcrypt.
To generate your own bcrypt hash, use this Python script:

```python
import bcrypt

password = "your_password_here"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print(f"Hashed password: {hashed.decode('utf-8')}")
```

Or use the provided create_sample_user.py script in the backend folder.

MYSQL SETUP COMMANDS:

1. Install MySQL Server
2. Start MySQL service
3. Connect to MySQL: mysql -u root -p
4. Run this schema file: source /path/to/schema.sql
5. Verify tables: SHOW TABLES; DESCRIBE users;

SECURITY NOTES:

- All passwords are stored as bcrypt hashes
- OTPs expire after 2 minutes
- Foreign key constraints ensure data integrity
- Indexes optimize query performance
- Sample data is for testing only - remove in production
*/
