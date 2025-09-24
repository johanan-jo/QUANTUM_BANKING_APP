@echo off
echo ========================================
echo   Banking Application Setup Guide
echo ========================================
echo.

echo Step 1: Install MySQL Database
echo ------------------------------
echo 1. Download MySQL from: https://dev.mysql.com/downloads/mysql/
echo 2. OR use XAMPP: https://www.apachefriends.org/download.html
echo 3. Start MySQL service
echo.

echo Step 2: Create Database
echo ----------------------
echo After MySQL is installed, run these commands in MySQL:
echo.
echo mysql -u root -p
echo CREATE DATABASE quantum_banking;
echo exit
echo.
echo Then run: mysql -u root -p quantum_banking < backend\sql\schema.sql
echo.

echo Step 3: Configure Email (Optional for testing)
echo ---------------------------------------------
echo Edit backend\.env file and set:
echo - SMTP_EMAIL=your-gmail@gmail.com
echo - SMTP_PASSWORD=your-app-password
echo.
echo To get Gmail App Password:
echo 1. Enable 2-factor authentication
echo 2. Go to Google Account settings
echo 3. Generate App Password for Mail
echo.

echo Step 4: Start Application
echo ------------------------
echo 1. Backend:  cd backend && python app.py
echo 2. Frontend: cd frontend && npm start
echo 3. Visit:    http://localhost:3000
echo.

echo Test Accounts (after database setup):
echo Email: john.doe@example.com, Password: SecurePass123!
echo Email: jane.smith@example.com, Password: MyPassword456!
echo.

pause
