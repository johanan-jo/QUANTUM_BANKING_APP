"""
Test email configuration
"""
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

print("🔍 Email Configuration Check:")
print("=" * 40)
print(f"SMTP_HOST: {os.getenv('SMTP_HOST', 'Not set')}")
print(f"SMTP_PORT: {os.getenv('SMTP_PORT', 'Not set')}")
print(f"SMTP_EMAIL: {os.getenv('SMTP_EMAIL', 'Not set')}")
print(f"SMTP_PASSWORD: {'*' * len(os.getenv('SMTP_PASSWORD', '')) if os.getenv('SMTP_PASSWORD') else 'Not set'}")
print(f"JWT_SECRET: {'*' * len(os.getenv('JWT_SECRET', '')) if os.getenv('JWT_SECRET') else 'Not set'}")
print("=" * 40)

# Test email sending
if input("\nDo you want to test email sending? (y/n): ").lower() == 'y':
    test_email = input("Enter test email address: ")
    
    try:
        from utils.mailer import send_otp_email
        print(f"\n📧 Sending test OTP to {test_email}...")
        
        if send_otp_email(test_email, "123456"):
            print("✅ Email sent successfully!")
        else:
            print("❌ Failed to send email. Check your SMTP configuration.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("\nEmail test skipped.")
    
print("\n📋 Next steps:")
print("1. Configure your Gmail/email settings in .env")
print("2. Make sure 2FA is enabled and app password is generated")
print("3. Test email sending before using the app")
