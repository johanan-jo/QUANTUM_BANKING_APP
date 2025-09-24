@echo off
setlocal EnableDelayedExpansion

:: Quantum Banking - Windows Setup Script
:: This script helps set up and run the complete banking application on Windows

title Quantum Banking - Setup Script

:: Colors (Windows doesn't support colors directly, but we'll use echo for formatting)
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "PURPLE=[95m"
set "CYAN=[96m"
set "WHITE=[97m"
set "NC=[0m"

:: Function to print headers
:print_header
echo.
echo ================================================================
echo   %~1
echo ================================================================
echo.
goto :eof

:: Function to print steps
:print_step
echo [STEP] %~1
goto :eof

:: Function to print success
:print_success
echo [SUCCESS] %~1
goto :eof

:: Function to print warnings
:print_warning
echo [WARNING] %~1
goto :eof

:: Function to print errors
:print_error
echo [ERROR] %~1
goto :eof

:: Function to check if command exists
:command_exists
where %1 >nul 2>nul
goto :eof

:: Main script starts here
call :print_header "QUANTUM BANKING - AUTOMATED SETUP"

:: Check prerequisites
call :print_header "CHECKING PREREQUISITES"

call :print_step "Checking Python installation..."
call :command_exists python
if %errorlevel% equ 0 (
    for /f "tokens=2" %%v in ('python --version 2^>^&1') do set python_version=%%v
    call :print_success "Python found: !python_version!"
) else (
    call :print_error "Python not found. Please install Python 3.8 or higher."
    pause
    exit /b 1
)

call :print_step "Checking Node.js installation..."
call :command_exists node
if %errorlevel% equ 0 (
    for /f "tokens=1" %%v in ('node --version 2^>^&1') do set node_version=%%v
    call :print_success "Node.js found: !node_version!"
) else (
    call :print_error "Node.js not found. Please install Node.js 16 or higher."
    pause
    exit /b 1
)

call :print_step "Checking MySQL installation..."
call :command_exists mysql
if %errorlevel% equ 0 (
    call :print_success "MySQL found"
) else (
    call :print_warning "MySQL not found. Please install MySQL Server."
)

:: Show menu
echo.
echo Choose setup option:
echo 1. Full setup (recommended for first time)
echo 2. Setup backend only
echo 3. Setup frontend only
echo 4. Start servers (skip setup)
echo 5. Run tests only
echo 6. Exit
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto full_setup
if "%choice%"=="2" goto setup_backend
if "%choice%"=="3" goto setup_frontend
if "%choice%"=="4" goto start_servers
if "%choice%"=="5" goto run_tests
if "%choice%"=="6" goto exit_script

call :print_error "Invalid choice. Please run the script again."
pause
exit /b 1

:full_setup
call :setup_backend
call :setup_frontend
call :setup_database
call :start_servers
goto show_final_instructions

:setup_backend
call :print_header "SETTING UP BACKEND"

cd backend

call :print_step "Creating Python virtual environment..."
python -m venv venv
call :print_success "Virtual environment created"

call :print_step "Activating virtual environment..."
call venv\Scripts\activate
call :print_success "Virtual environment activated"

call :print_step "Installing Python dependencies..."
pip install -r requirements.txt
call :print_success "Python dependencies installed"

call :print_step "Checking environment configuration..."
if not exist .env (
    call :print_warning ".env file not found. Creating from template..."
    copy .env.example .env
    call :print_warning "Please edit .env file with your configuration:"
    call :print_warning "  - Database credentials"
    call :print_warning "  - Gmail SMTP settings"
    call :print_warning "  - JWT secret key"
) else (
    call :print_success ".env file found"
)

cd ..
goto :eof

:setup_frontend
call :print_header "SETTING UP FRONTEND"

cd frontend

call :print_step "Installing Node.js dependencies..."
npm install
call :print_success "Node.js dependencies installed"

cd ..
goto :eof

:setup_database
call :print_header "SETTING UP DATABASE"

call :print_step "Database setup instructions..."
call :print_warning "Please run the following commands manually:"
echo 1. Start MySQL server
echo 2. Connect to MySQL: mysql -u root -p
echo 3. Run schema file: source %cd%\backend\sql\schema.sql
echo 4. Verify setup: USE quantum_banking; SHOW TABLES;
echo.
pause

goto :eof

:start_servers
call :print_header "STARTING SERVERS"

:: Start backend in a new window
call :print_step "Starting backend server..."
start "Quantum Banking Backend" cmd /k "cd backend && venv\Scripts\activate && python app.py"
call :print_success "Backend started in new window"

:: Wait a moment
timeout /t 3 /nobreak >nul

:: Start frontend in a new window
call :print_step "Starting frontend server..."
start "Quantum Banking Frontend" cmd /k "cd frontend && npm start"
call :print_success "Frontend started in new window"

goto :eof

:run_tests
call :print_header "RUNNING API TESTS"

cd backend
call venv\Scripts\activate
call :print_step "Running API test suite..."
python test_api.py
cd ..
pause
goto :eof

:show_final_instructions
call :print_header "QUANTUM BANKING IS READY!"

echo Application URLs:
echo   Frontend: http://localhost:3000
echo   Backend API: http://localhost:5000
echo   API Health: http://localhost:5000/api/health
echo.

echo Test Accounts (password: password123):
echo   Account: 1234567890, Email: john.doe@example.com
echo   Account: 9876543210, Email: jane.smith@example.com
echo.

echo Next Steps:
echo   1. Open http://localhost:3000 in your browser
echo   2. Try logging in with a test account
echo   3. Check your email for OTP verification
echo   4. Explore the dashboard features
echo.

echo To stop the servers:
echo   Close the backend and frontend windows that opened
echo.

call :print_warning "Don't forget to configure your .env file with real SMTP settings!"
echo.

echo Press any key to exit this setup script...
pause >nul
goto :eof

:exit_script
call :print_success "Goodbye!"
exit /b 0

:eof
