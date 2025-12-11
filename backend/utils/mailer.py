"""Gmail API mailer utilities for sending OTP and welcome emails.

This module exposes:
- send_email_via_gmail_api(to_email, subject, html_body, plain_body=None)
- send_otp_email(to_email, otp)
- send_welcome_email(to_email, name, account_number)

It uses a stored OAuth2 refresh token to obtain short-lived access tokens
so the app can send via the Gmail REST API (avoids outbound SMTP blocking).
"""
import os
import base64
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


def send_email_via_gmail_api(to_email: str, subject: str, html_body: str, plain_body: str = None):
    """Send an email via Gmail API using OAuth2 refresh token.

    Required env vars:
      - GOOGLE_CLIENT_ID
      - GOOGLE_CLIENT_SECRET
      - GOOGLE_REFRESH_TOKEN
      - FROM_EMAIL

    Returns the API response on success.
    """
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    refresh_token = os.environ.get("GOOGLE_REFRESH_TOKEN")
    from_email = os.environ.get("FROM_EMAIL")

    if not (client_id and client_secret and refresh_token and from_email):
        raise RuntimeError(
            "Missing Google OAuth env vars (GOOGLE_CLIENT_ID/SECRET/REFRESH_TOKEN/FROM_EMAIL)"
        )

    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
    )
    # Exchange refresh token for an access token
    creds.refresh(Request())

    msg = EmailMessage()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    if plain_body:
        msg.set_content(plain_body)
    msg.add_alternative(html_body, subtype="html")

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    service = build("gmail", "v1", credentials=creds)
    message = {"raw": raw}
    sent = service.users().messages().send(userId="me", body=message).execute()
    return sent


def send_otp_email(to_email: str, otp: str):
    """Compose and send OTP email."""
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

    return send_email_via_gmail_api(to_email, subject, html_content, plain_body=text_content)


def send_welcome_email(to_email: str, name: str, account_number: str):
    """Compose and send welcome email."""
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

    return send_email_via_gmail_api(to_email, subject, html_content)
