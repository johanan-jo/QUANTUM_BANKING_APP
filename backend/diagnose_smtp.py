"""
SMTP Diagnostic Script - Troubleshoot Gmail Authentication Issues
"""
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("🔍 Gmail SMTP Diagnostic Tool")
print("=" * 60)

# Get credentials
email = os.getenv('SMTP_EMAIL')
password = os.getenv('SMTP_PASSWORD')
host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
port = int(os.getenv('SMTP_PORT', 587))

print(f"\n📧 Configuration:")
print(f"   Email: {email}")
print(f"   Password Length: {len(password) if password else 0} characters")
print(f"   Password (masked): {'*' * (len(password) - 4) + password[-4:] if password and len(password) > 4 else '****'}")
print(f"   Host: {host}")
print(f"   Port: {port}")

# Check for common issues
print("\n🔍 Checking for common issues:")

issues = []

if not email or '@' not in email:
    issues.append("❌ Invalid email format")
else:
    print(f"   ✅ Email format looks valid")

if not password:
    issues.append("❌ Password is empty")
elif len(password) != 16:
    issues.append(f"⚠️  App password length is {len(password)} (expected 16 characters)")
    print(f"   ⚠️  App password should be exactly 16 characters (yours: {len(password)})")
else:
    print(f"   ✅ Password length is correct (16 characters)")

if ' ' in password:
    issues.append("❌ Password contains spaces (remove all spaces)")
    print(f"   ❌ Password contains spaces - remove them!")
else:
    print(f"   ✅ Password has no spaces")

if email and email.upper() != email and email.lower() != email:
    print(f"   ⚠️  Email has mixed case - try lowercase: {email.lower()}")

# Test SMTP connection
print("\n🔌 Testing SMTP Connection...")
print(f"   Connecting to {host}:{port}...")

try:
    # Test connection
    server = smtplib.SMTP(host, port, timeout=10)
    print(f"   ✅ Connected to {host}:{port}")
    
    # Test STARTTLS
    print(f"   🔐 Starting TLS encryption...")
    server.starttls()
    print(f"   ✅ TLS encryption started")
    
    # Test authentication
    print(f"   🔑 Testing authentication...")
    server.login(email, password)
    print(f"   ✅ Authentication SUCCESS!")
    
    server.quit()
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED - Your SMTP configuration is working!")
    print("=" * 60)
    
except smtplib.SMTPAuthenticationError as e:
    print(f"   ❌ Authentication FAILED: {e}")
    print("\n" + "=" * 60)
    print("❌ AUTHENTICATION ERROR")
    print("=" * 60)
    print("\n🔧 Troubleshooting Steps:")
    print("\n1. Verify 2-Factor Authentication (2FA) is enabled:")
    print("   • Go to: https://myaccount.google.com/security")
    print("   • Enable 2-Step Verification if not already enabled")
    
    print("\n2. Generate a NEW App Password:")
    print("   • Go to: https://myaccount.google.com/apppasswords")
    print("   • Select 'Mail' and your device")
    print("   • Copy the 16-character password (no spaces)")
    print("   • Update .env file with: SMTP_PASSWORD=<16-char-password>")
    
    print("\n3. Check if 'Less secure app access' is needed:")
    print("   • Some accounts need this enabled")
    print("   • Go to: https://myaccount.google.com/lesssecureapps")
    
    print("\n4. Verify the email account:")
    print(f"   • Current email: {email}")
    print("   • Make sure this is the correct Gmail account")
    print("   • Try using lowercase: " + (email.lower() if email else ""))
    
except Exception as e:
    print(f"   ❌ Connection FAILED: {e}")
    print("\n" + "=" * 60)
    print("❌ CONNECTION ERROR")
    print("=" * 60)
    print(f"\nError Details: {type(e).__name__}: {e}")

if issues:
    print("\n⚠️  Issues Found:")
    for issue in issues:
        print(f"   {issue}")

print("\n" + "=" * 60)
print("📚 Helpful Links:")
print("   • Gmail App Passwords: https://myaccount.google.com/apppasswords")
print("   • 2FA Setup: https://myaccount.google.com/security")
print("   • Account Security: https://myaccount.google.com/security")
print("=" * 60)
