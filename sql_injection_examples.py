"""
SQL Injection Examples - Educational Purpose Only
This file demonstrates SQL injection vulnerabilities and their fixes
"""

# ❌ VULNERABLE CODE EXAMPLES (DON'T USE THESE!)

def vulnerable_login_example(account_number, password):
    """
    VULNERABLE: String concatenation allows SQL injection
    """
    # BAD - Vulnerable to SQL injection
    query = f"SELECT * FROM users WHERE account_number = '{account_number}' AND password = '{password}'"
    # ATTACK: account_number = "1234567890' OR '1'='1' --"
    # RESULT: Query becomes: SELECT * FROM users WHERE account_number = '1234567890' OR '1'='1' --' AND password = 'anything'
    # This bypasses authentication!
    
def vulnerable_search_example(search_term):
    """
    VULNERABLE: Direct string formatting
    """
    # BAD - Vulnerable
    query = "SELECT * FROM users WHERE name LIKE '%" + search_term + "%'"
    # ATTACK: search_term = "'; DROP TABLE users; --"
    # RESULT: Deletes the entire users table!

# 🛡️ SECURE CODE EXAMPLES (YOUR CURRENT IMPLEMENTATION)

def secure_login_example(account_number, password):
    """
    SECURE: Parameterized queries prevent injection
    """
    # GOOD - Your current implementation
    query = "SELECT * FROM users WHERE account_number = %s AND password = %s"
    return execute_query(query, (account_number, password), fetch_one=True)
    # Even if attacker sends: "1234567890' OR '1'='1' --"
    # It's treated as literal string, not SQL code

def secure_search_example(search_term):
    """
    SECURE: Parameters are escaped automatically
    """
    # GOOD - Safe approach
    query = "SELECT * FROM users WHERE name LIKE %s"
    search_pattern = f"%{search_term}%"
    return execute_query(query, (search_pattern,), fetch_all=True)

# 🔍 COMMON SQL INJECTION ATTACKS

"""
1. AUTHENTICATION BYPASS:
   Input: account_number = "admin' --"
   Malicious Query: SELECT * FROM users WHERE account_number = 'admin' --' AND password = '...'
   Result: Password check is commented out

2. UNION ATTACKS:
   Input: account_number = "1' UNION SELECT username, password FROM admin_users --"
   Result: Exposes admin credentials

3. BLIND SQL INJECTION:
   Input: account_number = "1' AND (SELECT COUNT(*) FROM users) > 10 --"
   Result: Information disclosure through response timing

4. DATABASE DESTRUCTION:
   Input: search = "'; DROP TABLE users; --"
   Result: Destroys data

5. DATA EXFILTRATION:
   Input: account_number = "1' UNION SELECT credit_card, ssn FROM sensitive_data --"
   Result: Steals sensitive information
"""

# 🛡️ DEFENSE STRATEGIES (ALREADY IMPLEMENTED IN YOUR APP)

"""
1. PARAMETERIZED QUERIES (✅ Your app uses this)
   - Use placeholders (%s) instead of string concatenation
   - Database driver handles escaping automatically

2. INPUT VALIDATION (✅ Your app has this)
   - Validate data types, lengths, and formats
   - Whitelist allowed characters

3. LEAST PRIVILEGE (✅ Recommended)
   - Database user should have minimal permissions
   - Don't use root/admin accounts for applications

4. ERROR HANDLING (✅ Your app does this)
   - Don't expose database errors to users
   - Log errors securely

5. STORED PROCEDURES (Optional enhancement)
   - Pre-compiled SQL reduces attack surface
   - Additional layer of security
"""

# 📊 TESTING FOR SQL INJECTION

def test_sql_injection_inputs():
    """
    Test cases to verify your application is secure
    Try these inputs in your login form - they should fail gracefully
    """
    malicious_inputs = [
        "admin' --",
        "' OR '1'='1",
        "'; DROP TABLE users; --",
        "1' UNION SELECT * FROM information_schema.tables --",
        "admin' AND (SELECT COUNT(*) FROM users) > 0 --",
        "' OR 1=1 #",
        "admin'; INSERT INTO users VALUES('hacker', 'password'); --"
    ]
    
    print("Test these inputs in your login form:")
    for i, input_test in enumerate(malicious_inputs, 1):
        print(f"{i}. Account Number: {input_test}")
        print("   Expected Result: Login should fail with 'Invalid credentials'")
        print()

if __name__ == "__main__":
    test_sql_injection_inputs()