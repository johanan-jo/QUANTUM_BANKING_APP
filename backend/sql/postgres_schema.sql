-- Quantum Banking Database Schema (PostgreSQL/Supabase)
-- This file creates the complete database structure for the banking application

-- Drop tables if they exist (for clean reinstall)
DROP TABLE IF EXISTS otps CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Drop views if they exist
DROP VIEW IF EXISTS user_balance_summary;
DROP VIEW IF EXISTS recent_transactions;

-- Users table - stores user account information
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    account_number VARCHAR(10) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Create indexes for users table
CREATE INDEX idx_users_account_number ON users(account_number);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_users_active ON users(is_active);

-- OTPs table - stores one-time passwords for authentication
CREATE TABLE otps (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    otp_code VARCHAR(6) NOT NULL,
    expiry TIMESTAMP WITH TIME ZONE NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Foreign key constraint
    CONSTRAINT fk_otps_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create indexes for otps table
CREATE INDEX idx_otps_user_id ON otps(user_id);
CREATE INDEX idx_otps_otp_code ON otps(otp_code);
CREATE INDEX idx_otps_expiry ON otps(expiry);
CREATE INDEX idx_otps_used ON otps(used);
CREATE INDEX idx_otps_created_at ON otps(created_at);
CREATE INDEX idx_otps_cleanup ON otps(expiry, used);

-- Composite index for OTP verification (most important query)
CREATE INDEX idx_otps_user_otp ON otps(user_id, otp_code, used, expiry);

-- Transactions table - stores transaction history (optional for demo)
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    transaction_id VARCHAR(50) UNIQUE NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL CHECK (transaction_type IN ('credit', 'debit')),
    description VARCHAR(255) NOT NULL,
    reference_number VARCHAR(50),
    status VARCHAR(20) DEFAULT 'completed' CHECK (status IN ('pending', 'completed', 'failed', 'cancelled')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Foreign key constraint
    CONSTRAINT fk_transactions_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create indexes for transactions table
CREATE INDEX idx_transactions_user_id ON transactions(user_id);
CREATE INDEX idx_transactions_transaction_id ON transactions(transaction_id);
CREATE INDEX idx_transactions_type ON transactions(transaction_type);
CREATE INDEX idx_transactions_status ON transactions(status);
CREATE INDEX idx_transactions_created_at ON transactions(created_at);
CREATE INDEX idx_transactions_amount ON transactions(amount);

-- Composite index for user transaction history
CREATE INDEX idx_transactions_user_date ON transactions(user_id, created_at DESC);

-- Create function to update updated_at timestamp automatically
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for users table
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample user accounts
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

-- Display success message and sample data
SELECT 'Database schema created successfully!' as message;

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
SUPABASE SETUP INSTRUCTIONS:

1. Go to your Supabase project: https://app.supabase.com
2. Navigate to SQL Editor
3. Create a new query and paste this entire file
4. Click "Run" to execute the schema
5. Verify tables in Table Editor

CONNECTION STRING:
Get your connection string from: Project Settings > Database > Connection String
Format: postgresql://postgres:[YOUR-PASSWORD]@[HOST]/postgres

ENVIRONMENT VARIABLES FOR BACKEND:
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres

NOTES FOR PASSWORD GENERATION:

The sample users have password "password123" hashed with bcrypt.
To generate your own bcrypt hash, use this Python script:

```python
import bcrypt

password = "your_password_here"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print(f"Hashed password: {hashed.decode('utf-8')}")
```

SECURITY NOTES:

- All passwords are stored as bcrypt hashes
- OTPs expire after 2 minutes
- Foreign key constraints ensure data integrity
- Indexes optimize query performance
- Sample data is for testing only - remove in production
- Use service_role key for backend DB access (never expose to frontend)
- Enable Row Level Security (RLS) if needed for additional protection
*/
