"""Test SendGrid email sending locally.

Run: python test_sendgrid.py

Requires env vars: SENDGRID_API_KEY, FROM_EMAIL
"""
import os
from dotenv import load_dotenv

load_dotenv()

from utils.mailer import send_email_via_sendgrid

TO_EMAIL = os.getenv("SMTP_EMAIL", "quantumbankapp@gmail.com")
SUBJECT = "SendGrid Test - Quantum Banking"
HTML = """
<html>
<body style="font-family: Arial, sans-serif;">
  <h2>SendGrid Test Email</h2>
  <p>This is a test email sent via SendGrid API from Quantum Banking app.</p>
  <p style="color: #667eea;"><strong>If you received this, SendGrid is working!</strong></p>
</body>
</html>
"""
TEXT = "SendGrid Test Email\n\nThis is a test email sent via SendGrid API from Quantum Banking app.\n\nIf you received this, SendGrid is working!"

try:
    status, body, headers = send_email_via_sendgrid(TO_EMAIL, SUBJECT, HTML, TEXT)
    print(f"✓ Email sent successfully!")
    print(f"Status: {status}")
    print(f"Response: {body}")
except Exception as e:
    print(f"✗ Failed to send email: {e}")
