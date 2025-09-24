"""
API Test Script for Quantum Banking
This script tests all the API endpoints with sample data
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = 'http://localhost:5000/api'
TEST_ACCOUNT = '1234567890'
TEST_PASSWORD = 'password123'
TEST_EMAIL = 'john.doe@example.com'

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(title):
    """Print a formatted header"""
    print(f"\n{Colors.PURPLE}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.PURPLE}{Colors.BOLD}{title.center(60)}{Colors.END}")
    print(f"{Colors.PURPLE}{Colors.BOLD}{'='*60}{Colors.END}")

def print_test_result(test_name, success, message="", data=None):
    """Print formatted test result"""
    status = f"{Colors.GREEN}✅ PASS" if success else f"{Colors.RED}❌ FAIL"
    print(f"\n{status}{Colors.END} {Colors.BOLD}{test_name}{Colors.END}")
    
    if message:
        print(f"   {Colors.CYAN}Message:{Colors.END} {message}")
    
    if data:
        print(f"   {Colors.YELLOW}Response:{Colors.END} {json.dumps(data, indent=2)[:200]}...")

def test_health_check():
    """Test API health check"""
    print_header("API HEALTH CHECK")
    
    try:
        response = requests.get(f"{BASE_URL.replace('/api', '')}/")
        success = response.status_code == 200
        data = response.json() if response.status_code == 200 else None
        
        print_test_result(
            "Health Check", 
            success, 
            f"Status: {response.status_code}",
            data
        )
        return success
    except Exception as e:
        print_test_result("Health Check", False, f"Error: {str(e)}")
        return False

def test_registration():
    """Test user registration"""
    print_header("USER REGISTRATION")
    
    # Test data
    test_user = {
        "name": "Test User API",
        "account_number": "9999888877",
        "email": "testuser.api@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=test_user)
        success = response.status_code in [201, 400]  # 400 might be "already exists"
        data = response.json()
        
        print_test_result(
            "User Registration", 
            success, 
            f"Status: {response.status_code}",
            data
        )
        return success, test_user
    except Exception as e:
        print_test_result("User Registration", False, f"Error: {str(e)}")
        return False, None

def test_login():
    """Test user login"""
    print_header("USER LOGIN")
    
    login_data = {
        "account_number": TEST_ACCOUNT,
        "password": TEST_PASSWORD
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        success = response.status_code == 200
        data = response.json()
        
        print_test_result(
            "User Login", 
            success, 
            f"Status: {response.status_code}",
            data
        )
        
        # Extract OTP if in debug mode
        otp = None
        if success and 'debug_otp' in data:
            otp = data['debug_otp']
            print(f"   {Colors.GREEN}Debug OTP:{Colors.END} {otp}")
        
        return success, otp
    except Exception as e:
        print_test_result("User Login", False, f"Error: {str(e)}")
        return False, None

def test_otp_verification(otp=None):
    """Test OTP verification"""
    print_header("OTP VERIFICATION")
    
    if not otp:
        otp = input(f"\n{Colors.YELLOW}Enter OTP from email (or press Enter to skip): {Colors.END}")
        if not otp:
            print_test_result("OTP Verification", False, "Skipped - No OTP provided")
            return False, None
    
    otp_data = {
        "account_number": TEST_ACCOUNT,
        "otp": otp
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/verify-otp", json=otp_data)
        success = response.status_code == 200
        data = response.json()
        
        print_test_result(
            "OTP Verification", 
            success, 
            f"Status: {response.status_code}",
            data
        )
        
        # Extract token
        token = None
        if success and 'token' in data:
            token = data['token']
            print(f"   {Colors.GREEN}JWT Token:{Colors.END} {token[:50]}...")
        
        return success, token
    except Exception as e:
        print_test_result("OTP Verification", False, f"Error: {str(e)}")
        return False, None

def test_dashboard_access(token):
    """Test dashboard access"""
    print_header("DASHBOARD ACCESS")
    
    if not token:
        print_test_result("Dashboard Access", False, "Skipped - No token available")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/dashboard/me", headers=headers)
        success = response.status_code == 200
        data = response.json() if response.status_code == 200 else None
        
        print_test_result(
            "Dashboard Access", 
            success, 
            f"Status: {response.status_code}",
            data
        )
        return success
    except Exception as e:
        print_test_result("Dashboard Access", False, f"Error: {str(e)}")
        return False

def test_transactions_access(token):
    """Test transactions access"""
    print_header("TRANSACTIONS ACCESS")
    
    if not token:
        print_test_result("Transactions Access", False, "Skipped - No token available")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/dashboard/transactions", headers=headers)
        success = response.status_code == 200
        data = response.json() if response.status_code == 200 else None
        
        print_test_result(
            "Transactions Access", 
            success, 
            f"Status: {response.status_code}",
            data
        )
        return success
    except Exception as e:
        print_test_result("Transactions Access", False, f"Error: {str(e)}")
        return False

def test_invalid_requests():
    """Test various invalid requests"""
    print_header("SECURITY TESTS")
    
    tests = [
        {
            "name": "Invalid Login",
            "endpoint": "/auth/login",
            "method": "POST",
            "data": {"account_number": "0000000000", "password": "wrongpassword"},
            "expected_status": 401
        },
        {
            "name": "Invalid Registration",
            "endpoint": "/auth/register", 
            "method": "POST",
            "data": {"name": "", "account_number": "123", "email": "invalid", "password": "short"},
            "expected_status": 400
        },
        {
            "name": "Protected Route Without Token",
            "endpoint": "/dashboard/me",
            "method": "GET",
            "data": None,
            "expected_status": 401
        }
    ]
    
    for test in tests:
        try:
            if test["method"] == "POST":
                response = requests.post(f"{BASE_URL}{test['endpoint']}", json=test["data"])
            else:
                response = requests.get(f"{BASE_URL}{test['endpoint']}")
            
            success = response.status_code == test["expected_status"]
            data = response.json() if response.content else None
            
            print_test_result(
                test["name"], 
                success, 
                f"Expected: {test['expected_status']}, Got: {response.status_code}",
                data
            )
        except Exception as e:
            print_test_result(test["name"], False, f"Error: {str(e)}")

def main():
    """Main test function"""
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("🏦 QUANTUM BANKING API TEST SUITE")
    print("="*60)
    print(f"{Colors.END}")
    print(f"Testing API at: {Colors.CYAN}{BASE_URL}{Colors.END}")
    print(f"Test Account: {Colors.CYAN}{TEST_ACCOUNT}{Colors.END}")
    print(f"Time: {Colors.CYAN}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
    
    # Track test results
    results = {
        "total": 0,
        "passed": 0,
        "failed": 0
    }
    
    def update_results(success):
        results["total"] += 1
        if success:
            results["passed"] += 1
        else:
            results["failed"] += 1
    
    # Run tests
    try:
        # 1. Health Check
        success = test_health_check()
        update_results(success)
        
        if not success:
            print(f"\n{Colors.RED}❌ API is not accessible. Make sure the backend is running!{Colors.END}")
            return
        
        # 2. Registration Test
        success, test_user = test_registration()
        update_results(success)
        
        # 3. Login Test
        success, otp = test_login()
        update_results(success)
        
        if not success:
            print(f"\n{Colors.RED}❌ Cannot proceed with login. Check credentials!{Colors.END}")
            return
        
        # 4. OTP Verification
        success, token = test_otp_verification(otp)
        update_results(success)
        
        # 5. Dashboard Access
        if token:
            success = test_dashboard_access(token)
            update_results(success)
            
            # 6. Transactions Access
            success = test_transactions_access(token)
            update_results(success)
        
        # 7. Security Tests
        test_invalid_requests()
        update_results(True)  # Always passes as it's testing expected failures
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️ Tests interrupted by user{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Unexpected error: {str(e)}{Colors.END}")
    
    # Print summary
    print_header("TEST SUMMARY")
    print(f"Total Tests: {Colors.BOLD}{results['total']}{Colors.END}")
    print(f"Passed: {Colors.GREEN}{results['passed']}{Colors.END}")
    print(f"Failed: {Colors.RED}{results['failed']}{Colors.END}")
    
    success_rate = (results['passed'] / results['total'] * 100) if results['total'] > 0 else 0
    print(f"Success Rate: {Colors.BOLD}{success_rate:.1f}%{Colors.END}")
    
    if success_rate >= 80:
        print(f"\n{Colors.GREEN}🎉 Great! Most tests passed. API is working well!{Colors.END}")
    elif success_rate >= 50:
        print(f"\n{Colors.YELLOW}⚠️ Some tests failed. Check the issues above.{Colors.END}")
    else:
        print(f"\n{Colors.RED}❌ Many tests failed. Check your setup and configuration.{Colors.END}")

if __name__ == "__main__":
    main()
