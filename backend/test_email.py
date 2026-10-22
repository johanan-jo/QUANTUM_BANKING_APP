"""
Test email configuration and Gmail API OAuth 2.0 delivery
"""
import os
import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure backend directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv

load_dotenv()

def mask_secret(val: str, show_chars: int = 4) -> str:
    if not val:
        return "Not set"
    if len(val) <= show_chars:
        return "*" * len(val)
    return val[:show_chars] + "*" * (len(val) - show_chars)

print("🔍 Quantum Banking - Email Configuration Check (Gmail API OAuth 2.0):")
print("=" * 60)
client_id = os.getenv("GMAIL_CLIENT_ID") or os.getenv("GOOGLE_CLIENT_ID")
client_secret = os.getenv("GMAIL_CLIENT_SECRET") or os.getenv("GOOGLE_CLIENT_SECRET")
refresh_token = os.getenv("GMAIL_REFRESH_TOKEN") or os.getenv("GOOGLE_REFRESH_TOKEN")
sender_email = os.getenv("GMAIL_SENDER_EMAIL") or os.getenv("FROM_EMAIL") or os.getenv("SMTP_EMAIL")

print(f"GMAIL_CLIENT_ID:      {mask_secret(client_id, 8)}")
print(f"GMAIL_CLIENT_SECRET:  {mask_secret(client_secret, 4)}")
print(f"GMAIL_REFRESH_TOKEN:  {mask_secret(refresh_token, 6)}")
print(f"GMAIL_SENDER_EMAIL:   {sender_email or 'Not set'}")
print("=" * 60)

if not client_id or not client_secret or not refresh_token:
    print("⚠️ Missing OAuth 2.0 credentials in environment.")
    print("Run `python scripts/get_refresh_token.py` to generate tokens.")
    print("Then populate GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, and GMAIL_REFRESH_TOKEN.")
    sys.exit(0)

# Optional test email sending
user_choice = input("\nDo you want to test email sending? (y/n): ").strip().lower()
if user_choice == "y":
    test_email = input("Enter recipient test email address: ").strip()
    if not test_email:
        print("❌ No recipient address entered. Aborting test.")
        sys.exit(1)
        
    try:
        from utils.mailer import send_otp_email
        print(f"\n📧 Sending test OTP to {test_email}...")
        
        # Test with a dummy OTP
        success = send_otp_email(test_email, "987654")
        if success:
            print("✅ Email sent successfully via Gmail API!")
        else:
            print("❌ Failed to send email. Check error logs and OAuth token validity.")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
else:
    print("\nEmail test skipped.")
