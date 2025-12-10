import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

print(f"Testing SMTP with: {SMTP_EMAIL}")
print(f"Password length: {len(SMTP_PASSWORD)} chars")
print(f"Password: {SMTP_PASSWORD[:4]}...{SMTP_PASSWORD[-4:]}")

msg = EmailMessage()
msg["Subject"] = "SMTP Test - Quantum Banking"
msg["From"] = SMTP_EMAIL
msg["To"] = "quantumbankapp@gmail.com"  # Test sending to self
msg.set_content("This is an SMTP test from your Quantum Banking app!")

try:
    print("🔗 Connecting to SMTP server...")
    s = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20)
    s.ehlo()
    print("🔐 Starting TLS...")
    s.starttls()
    print(f"🔑 Logging in as {SMTP_EMAIL}...")
    s.login(SMTP_EMAIL, SMTP_PASSWORD)
    print("📧 Sending test email...")
    s.send_message(msg)
    s.quit()
    print("✅ SMTP test email sent successfully!")
except Exception as e:
    print(f"❌ SMTP test failed: {e}")