"""
SQL Injection Security Test Script
Test your banking application's protection against SQL injection attacks
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:5000/api"

def test_sql_injection_attacks():
    """
    Test various SQL injection attacks against the banking app
    All these should fail gracefully without causing security issues
    """
    
    print("🔍 Testing SQL Injection Protection")
    print("=" * 50)
    
    # Test cases - these should all be blocked
    test_cases = [
        {
            "name": "Authentication Bypass",
            "account_number": "admin' --",
            "password": "anything",
            "description": "Attempts to bypass password check"
        },
        {
            "name": "OR-based Attack", 
            "account_number": "' OR '1'='1",
            "password": "password",
            "description": "Tries to make condition always true"
        },
        {
            "name": "UNION Attack",
            "account_number": "1' UNION SELECT * FROM users --",
            "password": "test",
            "description": "Attempts to access other table data"
        },
        {
            "name": "Comment Injection",
            "account_number": "1234567890'; --",
            "password": "ignored",
            "description": "Uses comments to bypass validation"
        },
        {
            "name": "Destructive Attack",
            "account_number": "'; DROP TABLE users; --",
            "password": "test", 
            "description": "Attempts to delete database tables"
        },
        {
            "name": "Stacked Queries",
            "account_number": "1'; INSERT INTO users VALUES('hacker', 'pwd'); --",
            "password": "test",
            "description": "Tries to execute multiple SQL statements"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test['name']}")
        print(f"   Description: {test['description']}")
        print(f"   Input: {test['account_number']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/auth/login",
                headers={"Content-Type": "application/json"},
                json={
                    "account_number": test['account_number'],
                    "password": test['password']
                },
                timeout=5
            )
            
            if response.status_code == 400 or response.status_code == 401:
                print(f"   ✅ SECURE: Attack blocked (Status: {response.status_code})")
                try:
                    error_msg = response.json().get('error', 'Unknown error')
                    print(f"   Response: {error_msg}")
                except:
                    print(f"   Response: Error parsing JSON")
            elif response.status_code == 200:
                print(f"   ⚠️  CONCERN: Login succeeded - check if this is expected")
                print(f"   Response: {response.json()}")
            else:
                print(f"   ℹ️  Server Error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Network Error: {e}")
    
    print("\n" + "=" * 50)
    print("🔍 Test Complete!")
    print("\nExpected Results:")
    print("✅ All attacks should be blocked with 400/401 status codes")
    print("✅ No sensitive information should be exposed")
    print("✅ Database should remain intact")

def test_registration_injection():
    """Test SQL injection in registration endpoint"""
    
    print("\n🔍 Testing Registration SQL Injection Protection")
    print("=" * 50)
    
    malicious_registrations = [
        {
            "name": "'; DROP TABLE users; --",
            "email": "test@example.com", 
            "password": "password123"
        },
        {
            "name": "Normal User",
            "email": "'; UPDATE users SET password='hacked' WHERE 1=1; --@example.com",
            "password": "password123"
        }
    ]
    
    for i, data in enumerate(malicious_registrations, 1):
        print(f"\n{i}. Testing registration with malicious input")
        print(f"   Name: {data['name']}")
        print(f"   Email: {data['email']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/auth/register",
                headers={"Content-Type": "application/json"},
                json=data,
                timeout=5
            )
            
            if response.status_code == 400:
                print(f"   ✅ SECURE: Registration blocked")
            elif response.status_code == 201:
                print(f"   ⚠️ REGISTERED: Check if input was properly sanitized")
                result = response.json()
                print(f"   Account Number: {result.get('account_number', 'N/A')}")
            else:
                print(f"   Status: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Network Error: {e}")

if __name__ == "__main__":
    print("🛡️ SQL Injection Security Testing Tool")
    print("Testing your Quantum Banking Application\n")
    
    # Test login injection
    test_sql_injection_attacks()
    
    # Test registration injection  
    test_registration_injection()
    
    print("\n🔐 Security Recommendations:")
    print("1. ✅ Continue using parameterized queries")
    print("2. ✅ Keep input validation strict") 
    print("3. ✅ Never expose database errors to users")
    print("4. ✅ Use least privilege database accounts")
    print("5. ✅ Log all failed authentication attempts")
    print("6. ✅ Consider adding rate limiting for failed attempts")