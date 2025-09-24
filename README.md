# Quantum Banking - Full-Stack Banking Application

A secure, production-ready banking application with quantum-inspired OTP generation, implementing a complete authentication flow with React frontend and Flask backend. Features auto-generated account numbers, real-time email OTP delivery, and a modern responsive UI.

## 🏦 Features

- **Auto-Generated Account Numbers**: System automatically creates unique 10-digit account numbers
- **Secure Authentication**: Account number + password login with bcrypt hashing (12 salt rounds)
- **Quantum-Inspired OTP**: Advanced OTP generation with cryptographic randomness and email delivery
- **Real-time Email Delivery**: Professional HTML email templates with Gmail SMTP integration
- **Smart Registration Flow**: No auto-redirect, users can save account numbers before proceeding
- **Professional UI**: Responsive design with custom CSS utilities (Tailwind-inspired)
- **Multi-Port CORS Support**: Frontend can run on ports 3000-3003
- **Production Ready**: Comprehensive error handling, rate limiting, and security measures

## 🛠️ Tech Stack

### Backend
- **Flask** (Python) with Blueprints
- **MySQL** database with connection pooling
- **bcrypt** for password hashing
- **JWT** for session management
- **SMTP** for email delivery
- **Quantum OTP Generator** (simulation)

### Frontend
- **React 18** with modern hooks and functional components
- **Custom CSS Utilities** (Tailwind-inspired) for consistent styling
- **Axios** for API communication with error handling
- **React Router DOM** for navigation and protected routes
- **Responsive Design** optimized for all device sizes
- **Real-time Form Validation** with user-friendly error messages

## 📋 Prerequisites

Before running the application, ensure you have:

- **Python 3.8+** installed
- **Node.js 16+** and npm installed
- **MySQL Server** running
- **Gmail account** with App Password enabled

## 🚀 Quick Start Guide

### 1. Clone & Setup

```bash
# Navigate to project directory
cd C:\Users\yuvanshankar\OneDrive\Desktop\LIL3

# Setup backend
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt

# Setup frontend
cd ..\frontend
npm install
```

### 2. Configure Environment Variables

Create `backend\.env` from the example:

```bash
cd backend
copy .env.example .env
```

Edit `.env` with your settings:

```env
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASS=your_mysql_password
DB_NAME=quantum_banking

# SMTP Email Configuration (Gmail)
SMTP_EMAIL=QUANTUM.BANK3@GMAIL.COM
SMTP_PASSWORD=srdl cxmf ebjf ewrq
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587

# Security
JWT_SECRET=quantum_banking_super_secret_key_2025_production_grade_security_token_hash

# Development Settings
DEBUG_OTP=true  # Set to false in production
```

### 3. Setup Gmail App Password

✅ **Already Configured**: The application is pre-configured with working Gmail SMTP settings:
- **Email**: QUANTUM.BANK3@GMAIL.COM
- **App Password**: Configured and ready to use
- **SMTP Server**: smtp.gmail.com:587

> **Note**: If you need to use a different email account, follow these steps:
1. **Enable 2FA** on your Gmail account
2. Go to [Google Account Settings](https://myaccount.google.com/)
3. Navigate to **Security** → **App passwords**
4. Generate a new App Password for "Mail"
5. Update the `.env` file with your credentials

### 4. Setup Database

```bash
# Start MySQL server (if not running)
net start MySQL80

# Connect to MySQL
mysql -u root -p

# Run the schema file
source C:/Users/yuvanshankar/OneDrive/Desktop/LIL3/backend/sql/schema.sql

# Verify setup
USE quantum_banking;
SHOW TABLES;
SELECT * FROM users;
```

**Alternative Setup Script:**
```bash
# Use the automated database setup script
cd C:\Users\yuvanshankar\OneDrive\Desktop\LIL3
.\setup_database.bat
```

### 5. Run the Application

**Start Backend** (Terminal 1):
```bash
cd backend
venv\Scripts\activate
python app.py
```

**Start Frontend** (Terminal 2):
```bash
cd frontend
npm start
```

**Access Application**:
- Frontend: http://localhost:3000 (or 3001, 3002, 3003)
- Backend API: http://localhost:5000

> **Note**: The application supports multiple frontend ports (3000-3003) due to CORS configuration. If port 3000 is occupied, React will automatically suggest an alternative port.

## 🧪 Testing the Application

### Sample Accounts
The database includes test accounts with password `password123`:

| Account Number | Email | Name | Balance |
|---|---|---|---|
| 1234567890 | john.doe@example.com | John Doe | $6,839.51 |
| 9876543210 | jane.smith@example.com | Jane Smith | $8,435.00 |
| 1111222233 | bob.johnson@example.com | Bob Johnson | $3,250.00 |

### Test Flow
1. **Register**: Create a new account (account number auto-generated)
2. **Save Account Number**: System displays your unique 10-digit account number
3. **Login**: Enter account number and password
4. **OTP**: Check your email for the 6-digit quantum-inspired code
5. **Dashboard**: View account information, balance, and transaction history

### New Registration Flow
- **Auto-Generated Account Numbers**: No need to choose account numbers
- **Smart UI**: Registration success page displays account number prominently
- **User Control**: Manual "Continue to Login" button (no auto-redirect)
- **Account Number Saving**: Users can copy/save their account number before proceeding

### API Testing with cURL

```bash
# Register new user (account number auto-generated)
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Test User\",\"email\":\"test@example.com\",\"password\":\"password123\"}"

# Login (request OTP)
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"account_number\":\"1234567890\",\"password\":\"password123\"}"

# Verify OTP (replace with actual OTP from email)
curl -X POST http://localhost:5000/api/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d "{\"account_number\":\"1234567890\",\"otp\":\"123456\"}"

# Access user dashboard (replace TOKEN with actual JWT)
curl -X GET http://localhost:5000/api/dashboard/user \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Get transaction history (replace TOKEN with actual JWT)
curl -X GET http://localhost:5000/api/dashboard/transactions \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🔐 Security Features

### Authentication & Authorization
- **bcrypt password hashing** (salt rounds: 12)
- **JWT tokens** with 24-hour expiry
- **Rate limiting** for OTP requests (max 3 per hour)
- **Input validation** on all endpoints

### OTP Security
- **Quantum-inspired generation** with cryptographic randomness
- **2-minute expiry** for all OTPs
- **One-time use** enforcement
- **Email delivery** with professional templates

### Database Security
- **Parameterized queries** prevent SQL injection
- **Foreign key constraints** ensure data integrity
- **Indexes** for optimal performance
- **Connection pooling** for scalability

## 🎨 Frontend Features

### User Experience
- **Responsive design** works on all devices
- **Real-time validation** with error messages
- **Loading states** and progress indicators
- **Professional animations** and transitions

### Components
- **Login**: Account number + password authentication
- **Register**: Account creation with password strength indicator
- **OTP Verify**: 6-digit code input with timer and resend
- **Dashboard**: Account overview, transactions, and quick actions
- **NavBar**: User information and logout functionality

## 📁 Project Structure

```
LIL3/
├── backend/
│   ├── app.py              # Flask application entry point
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example       # Environment variables template
│   ├── routes/
│   │   ├── auth.py        # Authentication endpoints
│   │   └── dashboard.py   # Protected dashboard endpoints
│   ├── utils/
│   │   ├── db.py          # Database connection and queries
│   │   ├── security.py    # Password hashing and JWT
│   │   ├── mailer.py      # Email sending functionality
│   │   └── quantum_otp.py # Quantum-inspired OTP generator
│   └── sql/
│       └── schema.sql     # Database schema and sample data
├── frontend/
│   ├── package.json       # Node.js dependencies
│   ├── tailwind.config.js # Tailwind CSS configuration
│   ├── src/
│   │   ├── App.jsx        # Main application component
│   │   ├── api.js         # API client and utilities
│   │   ├── index.css      # Global styles with custom utilities
│   │   └── components/
│   │       ├── Login.jsx      # Login form component
│   │       ├── Register.jsx   # Registration form with auto-generated accounts
│   │       ├── OtpVerify.jsx  # OTP verification with timer
│   │       ├── Dashboard.jsx  # User dashboard with transactions
│   │       └── NavBar.jsx     # Navigation component
│   └── public/
│       └── index.html     # HTML template
└── README.md              # This file
```

## 🔬 Quantum OTP Generator

The application includes a **quantum-inspired OTP generator** that simulates quantum randomness:

### Current Implementation (Simulation)
- **Photon polarization simulation** using cryptographic methods
- **Quantum state representation** with deterministic randomness
- **HMAC-based extraction** for uniform distribution
- **Clearly marked as MOCK** for development

### Future Integration
The system is designed for easy integration with real quantum hardware:

```python
# Example integration with IBM Quantum
from qiskit import QuantumCircuit, transpile
from qiskit.providers.ibmq import IBMQ

def real_quantum_otp(user_id):
    # Connect to quantum hardware
    provider = IBMQ.get_provider()
    backend = provider.get_backend('ibmq_qasm_simulator')
    
    # Create quantum circuit for randomness
    qc = QuantumCircuit(6, 6)
    for i in range(6):
        qc.h(i)  # Hadamard gate for superposition
        qc.measure(i, i)
    
    # Execute and extract random bits
    job = backend.run(qc, shots=1)
    result = job.result()
    # Process quantum measurements into OTP
```

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Check MySQL is running
net start mysql

# Verify credentials in .env file
# Test connection manually
mysql -u root -p -h localhost
```

**Email Not Sending**
```bash
# Verify Gmail App Password is correct
# Check SMTP credentials in .env
# Ensure 2FA is enabled on Gmail account
```

**OTP Not Received**
- Check spam/junk folder
- Verify email address is correct
- Try resending OTP (max 3 per hour)
- Check backend logs for email errors

**Frontend Build Issues**
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Debug Mode

Enable debug mode in `.env`:
```env
DEBUG_OTP=true
```

This will:
- Include OTP in API responses (for testing)
- Add detailed logging to console
- Show request/response information

## 📝 API Documentation

### Authentication Endpoints

**POST /api/auth/register**
```json
{
  "name": "John Doe",
  "account_number": "1234567890",
  "email": "john@example.com", 
  "password": "securepassword"
}
```

**POST /api/auth/login**
```json
{
  "account_number": "1234567890",
  "password": "securepassword"
}
```

**POST /api/auth/verify-otp**
```json
{
  "account_number": "1234567890",
  "otp": "123456"
}
```

### Dashboard Endpoints (Protected)

**GET /api/dashboard/me**
- Headers: `Authorization: Bearer <token>`
- Returns: User profile and account summary

**GET /api/dashboard/transactions**
- Headers: `Authorization: Bearer <token>`
- Query params: `page`, `limit`, `type`
- Returns: Paginated transaction history

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Quantum Computing Community** for inspiration
- **Flask & React Communities** for excellent documentation
- **Tailwind CSS** for beautiful styling utilities
- **Security Research** for best practices implementation

---

**© 2025 Quantum Banking. Secure • Reliable • Advanced**

For support or questions, please create an issue in the repository.
