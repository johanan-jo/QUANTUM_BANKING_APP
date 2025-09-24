@echo off
echo ========================================
echo   Setting up Banking Database
echo ========================================
echo.

set MYSQL_PATH="C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"

echo Creating database and tables...
echo Please enter your MySQL root password when prompted.
echo.

%MYSQL_PATH% -u root -p -e "CREATE DATABASE IF NOT EXISTS quantum_banking CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to create database. Please check your MySQL root password.
    pause
    exit /b 1
)

echo Database created successfully!
echo.

echo Setting up tables and sample data...
%MYSQL_PATH% -u root -p quantum_banking < backend\sql\schema.sql

if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to create tables. Please check the schema file.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Database setup completed!
echo ========================================
echo.
echo Database: quantum_banking
echo Tables created: users, otps, transactions
echo Sample data loaded with test accounts
echo.
echo Test accounts:
echo - Email: john.doe@example.com
echo - Password: SecurePass123!
echo.
echo - Email: jane.smith@example.com  
echo - Password: MyPassword456!
echo.
pause
