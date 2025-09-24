#!/bin/bash

# Quantum Banking - Project Setup Script
# This script helps set up and run the complete banking application

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    color=$1
    message=$2
    echo -e "${color}${message}${NC}"
}

print_header() {
    echo
    print_color $PURPLE "================================================================"
    print_color $PURPLE "  $1"
    print_color $PURPLE "================================================================"
    echo
}

print_step() {
    print_color $CYAN "🔵 $1"
}

print_success() {
    print_color $GREEN "✅ $1"
}

print_warning() {
    print_color $YELLOW "⚠️  $1"
}

print_error() {
    print_color $RED "❌ $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python installation
check_python() {
    print_step "Checking Python installation..."
    
    if command_exists python3; then
        python_version=$(python3 --version 2>&1 | cut -d" " -f2)
        print_success "Python found: $python_version"
        return 0
    elif command_exists python; then
        python_version=$(python --version 2>&1 | cut -d" " -f2)
        if [[ $python_version == 3.* ]]; then
            print_success "Python found: $python_version"
            return 0
        else
            print_error "Python 3.8+ required, found: $python_version"
            return 1
        fi
    else
        print_error "Python not found. Please install Python 3.8 or higher."
        return 1
    fi
}

# Function to check Node.js installation
check_nodejs() {
    print_step "Checking Node.js installation..."
    
    if command_exists node; then
        node_version=$(node --version)
        print_success "Node.js found: $node_version"
        return 0
    else
        print_error "Node.js not found. Please install Node.js 16 or higher."
        return 1
    fi
}

# Function to check MySQL installation
check_mysql() {
    print_step "Checking MySQL installation..."
    
    if command_exists mysql; then
        mysql_version=$(mysql --version)
        print_success "MySQL found: $mysql_version"
        return 0
    else
        print_warning "MySQL not found. Please install MySQL Server."
        return 1
    fi
}

# Function to setup backend
setup_backend() {
    print_header "SETTING UP BACKEND"
    
    cd backend
    
    print_step "Creating Python virtual environment..."
    if command_exists python3; then
        python3 -m venv venv
    else
        python -m venv venv
    fi
    print_success "Virtual environment created"
    
    print_step "Activating virtual environment..."
    source venv/bin/activate  # For Unix/Linux/macOS
    # On Windows, use: venv\Scripts\activate
    print_success "Virtual environment activated"
    
    print_step "Installing Python dependencies..."
    pip install -r requirements.txt
    print_success "Python dependencies installed"
    
    print_step "Checking environment configuration..."
    if [ ! -f .env ]; then
        print_warning ".env file not found. Creating from template..."
        cp .env.example .env
        print_warning "Please edit .env file with your configuration:"
        print_warning "  - Database credentials"
        print_warning "  - Gmail SMTP settings"
        print_warning "  - JWT secret key"
    else
        print_success ".env file found"
    fi
    
    cd ..
}

# Function to setup frontend
setup_frontend() {
    print_header "SETTING UP FRONTEND"
    
    cd frontend
    
    print_step "Installing Node.js dependencies..."
    npm install
    print_success "Node.js dependencies installed"
    
    print_step "Building Tailwind CSS..."
    npx tailwindcss build -i src/index.css -o src/output.css
    print_success "Tailwind CSS built"
    
    cd ..
}

# Function to setup database
setup_database() {
    print_header "SETTING UP DATABASE"
    
    print_step "Checking MySQL connection..."
    if ! command_exists mysql; then
        print_error "MySQL not found. Please install MySQL Server first."
        return 1
    fi
    
    print_warning "Please run the following commands manually:"
    print_color $WHITE "1. Start MySQL server"
    print_color $WHITE "2. Connect to MySQL: mysql -u root -p"
    print_color $WHITE "3. Run schema file: source $(pwd)/backend/sql/schema.sql"
    print_color $WHITE "4. Verify setup: USE quantum_banking; SHOW TABLES;"
    
    echo
    read -p "Press Enter after completing database setup..."
}

# Function to start backend
start_backend() {
    print_header "STARTING BACKEND SERVER"
    
    cd backend
    
    print_step "Activating virtual environment..."
    source venv/bin/activate
    
    print_step "Starting Flask server..."
    print_color $GREEN "Backend will run at: http://localhost:5000"
    python app.py &
    BACKEND_PID=$!
    
    cd ..
    
    # Wait a moment for server to start
    sleep 3
    
    # Check if backend is running
    if curl -s http://localhost:5000/ > /dev/null; then
        print_success "Backend server started successfully!"
    else
        print_error "Backend server failed to start"
        return 1
    fi
}

# Function to start frontend
start_frontend() {
    print_header "STARTING FRONTEND SERVER"
    
    cd frontend
    
    print_step "Starting React development server..."
    print_color $GREEN "Frontend will run at: http://localhost:3000"
    npm start &
    FRONTEND_PID=$!
    
    cd ..
    
    print_success "Frontend server started successfully!"
}

# Function to run tests
run_tests() {
    print_header "RUNNING API TESTS"
    
    cd backend
    source venv/bin/activate
    
    print_step "Running API test suite..."
    python test_api.py
    
    cd ..
}

# Function to display final instructions
show_final_instructions() {
    print_header "🎉 QUANTUM BANKING IS READY!"
    
    print_color $WHITE "Application URLs:"
    print_color $CYAN "  Frontend: http://localhost:3000"
    print_color $CYAN "  Backend API: http://localhost:5000"
    print_color $CYAN "  API Health: http://localhost:5000/api/health"
    
    echo
    print_color $WHITE "Test Accounts (password: password123):"
    print_color $YELLOW "  Account: 1234567890, Email: john.doe@example.com"
    print_color $YELLOW "  Account: 9876543210, Email: jane.smith@example.com"
    
    echo
    print_color $WHITE "Next Steps:"
    print_color $GREEN "  1. Open http://localhost:3000 in your browser"
    print_color $GREEN "  2. Try logging in with a test account"
    print_color $GREEN "  3. Check your email for OTP verification"
    print_color $GREEN "  4. Explore the dashboard features"
    
    echo
    print_color $WHITE "To stop the servers:"
    print_color $RED "  Press Ctrl+C in this terminal"
    
    echo
    print_warning "Don't forget to configure your .env file with real SMTP settings!"
}

# Function to cleanup on exit
cleanup() {
    print_header "SHUTTING DOWN SERVERS"
    
    if [ ! -z "$BACKEND_PID" ]; then
        print_step "Stopping backend server..."
        kill $BACKEND_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        print_step "Stopping frontend server..."
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    print_success "Servers stopped. Goodbye!"
}

# Trap exit signals to cleanup
trap cleanup EXIT INT TERM

# Main function
main() {
    print_header "🏦 QUANTUM BANKING - AUTOMATED SETUP"
    
    # Check prerequisites
    print_header "CHECKING PREREQUISITES"
    
    check_python || exit 1
    check_nodejs || exit 1
    check_mysql || print_warning "MySQL check failed - you'll need to set it up manually"
    
    # Show menu
    echo
    print_color $WHITE "Choose setup option:"
    print_color $CYAN "1. Full setup (recommended for first time)"
    print_color $CYAN "2. Setup backend only"
    print_color $CYAN "3. Setup frontend only" 
    print_color $CYAN "4. Start servers (skip setup)"
    print_color $CYAN "5. Run tests only"
    print_color $CYAN "6. Exit"
    
    echo
    read -p "Enter your choice (1-6): " choice
    
    case $choice in
        1)
            setup_backend
            setup_frontend
            setup_database
            start_backend
            start_frontend
            show_final_instructions
            
            # Keep script running
            print_color $YELLOW "Press Ctrl+C to stop the servers..."
            wait
            ;;
        2)
            setup_backend
            print_success "Backend setup complete!"
            ;;
        3)
            setup_frontend
            print_success "Frontend setup complete!"
            ;;
        4)
            start_backend
            start_frontend
            show_final_instructions
            
            # Keep script running
            print_color $YELLOW "Press Ctrl+C to stop the servers..."
            wait
            ;;
        5)
            run_tests
            ;;
        6)
            print_success "Goodbye!"
            exit 0
            ;;
        *)
            print_error "Invalid choice. Please run the script again."
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
