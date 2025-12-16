"""SendGrid mailer wrapper.

This module sends transactional emails via SendGrid API.

Environment variables required:
- SENDGRID_API_KEY: SendGrid API key
- FROM_EMAIL: sender email address (must be verified in SendGrid)

Local test script `backend/test_sendgrid.py` can be used to validate.
"""
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from typing import Optional

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")


class SendGridError(Exception):
    pass


def send_email_via_sendgrid(to_email: str, subject: str, html_body: str, plain_body: Optional[str] = None, from_email: Optional[str] = None):
    """Send an email using SendGrid API.

    Returns status code and response body on success; raises SendGridError on failure.
    """
    api_key = SENDGRID_API_KEY or os.getenv("SENDGRID_API_KEY")
    sender = from_email or FROM_EMAIL or os.getenv("FROM_EMAIL")

    if not api_key:
        raise SendGridError("SendGrid configuration missing: SENDGRID_API_KEY must be set")
    if not sender:
        raise SendGridError("FROM_EMAIL must be set in environment variables")

    try:
        message = Mail(
            from_email=sender,
            to_emails=to_email,
            subject=subject,
            html_content=html_body,
            plain_text_content=plain_body or ""
        )
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        return response.status_code, response.body, response.headers
    except Exception as e:
        raise SendGridError(f"SendGrid API error: {e}")


def send_otp_email(to_email: str, otp: str):
    subject = "Quantum Banking - Login OTP"
    html_content = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
  <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center;">
    <h1 style="color: white; margin: 0;">Quantum Banking</h1>
  </div>
  <div style="padding: 30px; background-color: #f8f9fa;">
    <h2 style="color: #333; text-align: center;">Your Login OTP</h2>
    <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin: 20px 0;">
      <p style="color: #666; margin-bottom: 15px;">Your one-time password for secure login:</p>
      <h1 style="color: #667eea; font-size: 36px; letter-spacing: 8px; margin: 20px 0; font-family: 'Courier New', monospace;">{otp}</h1>
      <p style="color: #d63384; font-weight: bold;">This OTP will expire in 2 minutes</p>
    </div>
    <p style="color: #666; text-align: center; font-size: 14px;">If you didn't request this OTP, please ignore this email and ensure your account is secure.</p>
  </div>
  <div style="background: #343a40; padding: 15px; text-align: center;">
    <p style="color: #adb5bd; margin: 0; font-size: 12px;">© 2025 Quantum Banking. Secure • Reliable • Advanced</p>
  </div>
</body>
</html>
"""

    text_content = f"""
Quantum Banking - Login OTP

Your one-time password for secure login: {otp}

This OTP will expire in 2 minutes.

If you didn't request this OTP, please ignore this email.
"""

    status, body, headers = send_email_via_sendgrid(to_email, subject, html_content, plain_body=text_content)
    return status, body


def send_welcome_email(to_email: str, name: str, account_number: str):
    subject = "Welcome to Quantum Banking!"
    html_content = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
  <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center;">
    <h1 style="color: white; margin: 0;">Quantum Banking</h1>
  </div>
  <div style="padding: 30px; background-color: #f8f9fa;">
    <h2 style="color: #333;">Welcome, {name}!</h2>
    <p style="color: #666; font-size: 16px;">Congratulations! Your Quantum Banking account has been successfully created.</p>
    <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 20px 0;">
      <h3 style="color: #667eea; margin-top: 0;">Account Details</h3>
      <p><strong>Account Number:</strong> {account_number}</p>
      <p><strong>Email:</strong> {to_email}</p>
    </div>
    <p style="color: #666;">You can now log in to your account using your account number and password. For security, you'll receive an OTP via email during each login.</p>
  </div>
  <div style="background: #343a40; padding: 15px; text-align: center;">
    <p style="color: #adb5bd; margin: 0; font-size: 12px;">© 2025 Quantum Banking. Secure • Reliable • Advanced</p>
  </div>
</body>
</html>
"""

    status, body, headers = send_email_via_sendgrid(to_email, subject, html_content)
    return status, body

