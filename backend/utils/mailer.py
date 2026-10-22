"""
Email Dispatcher Module for Quantum Banking Application

Dispatches transactional emails (OTP codes and welcome notifications) using
the official Google Gmail API with OAuth 2.0 refresh-token authentication.

Replaces deprecated/expired SendGrid integration while preserving the existing
function signatures, HTML styling, and error handling contracts.
"""

import os
import logging
from typing import Optional, Dict, Any, Tuple
from utils.gmail_service import (
    send_email_via_gmail,
    GmailServiceError,
    _mask_email
)

logger = logging.getLogger("quantum_banking.mailer")


def send_otp_email(to_email: str, otp: str) -> bool:
    """
    Send a Quantum-Inspired OTP email via Gmail API OAuth 2.0.

    Args:
        to_email: Recipient email address
        otp: 6-digit OTP code

    Returns:
        bool: True if dispatched successfully, False if sending failed.
    """
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
      <p style="color: #d63384; font-weight: bold;">This OTP will expire in 5 minutes</p>
    </div>
    <p style="color: #666; text-align: center; font-size: 14px;">If you didn't request this OTP, please ignore this email and ensure your account is secure.</p>
  </div>
  <div style="background: #343a40; padding: 15px; text-align: center;">
    <p style="color: #adb5bd; margin: 0; font-size: 12px;">© 2026 Quantum Banking. Secure • Reliable • Advanced</p>
  </div>
</body>
</html>
"""

    text_content = f"""Quantum Banking - Login OTP

Your one-time password for secure login: {otp}

This OTP will expire in 5 minutes.

If you didn't request this OTP, please ignore this email and ensure your account is secure.
"""

    try:
        # Note: We do NOT log the actual OTP value for security
        logger.info("Attempting OTP dispatch to %s via Gmail API", _mask_email(to_email))
        send_email_via_gmail(
            to_email=to_email,
            subject=subject,
            html_body=html_content,
            plain_body=text_content
        )
        logger.info("OTP successfully sent to %s", _mask_email(to_email))
        return True
    except GmailServiceError as gse:
        logger.error("Gmail API delivery failed for %s: %s", _mask_email(to_email), str(gse))
        return False
    except Exception as e:
        logger.error("Unexpected error delivering OTP to %s: %s", _mask_email(to_email), str(e))
        return False


def send_welcome_email(to_email: str, name: str, account_number: str) -> bool:
    """
    Send a welcome onboarding email to newly registered users via Gmail API.

    Args:
        to_email: Recipient email address
        name: Full name of the user
        account_number: Auto-generated 10-digit account number

    Returns:
        bool: True if dispatched successfully, False if sending failed.
    """
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
    <p style="color: #666;">You can now log in to your account using your account number and password. For security, you will receive a quantum-inspired OTP via email during each login.</p>
  </div>
  <div style="background: #343a40; padding: 15px; text-align: center;">
    <p style="color: #adb5bd; margin: 0; font-size: 12px;">© 2026 Quantum Banking. Secure • Reliable • Advanced</p>
  </div>
</body>
</html>
"""

    text_content = f"""Welcome to Quantum Banking, {name}!

Congratulations! Your Quantum Banking account has been successfully created.

Account Details:
- Account Number: {account_number}
- Email: {to_email}

You can now log in using your account number and password. For security, you will receive a quantum-inspired OTP via email during each login.
"""

    try:
        logger.info("Attempting welcome email dispatch to %s via Gmail API", _mask_email(to_email))
        send_email_via_gmail(
            to_email=to_email,
            subject=subject,
            html_body=html_content,
            plain_body=text_content
        )
        logger.info("Welcome email successfully sent to %s", _mask_email(to_email))
        return True
    except GmailServiceError as gse:
        logger.error("Gmail API delivery failed for welcome email to %s: %s", _mask_email(to_email), str(gse))
        return False
    except Exception as e:
        logger.error("Unexpected error delivering welcome email to %s: %s", _mask_email(to_email), str(e))
        return False


def send_email_via_sendgrid(*args, **kwargs):
    """
    Deprecated: Provided for backward compatibility.
    Redirects to Gmail API delivery.
    """
    to_email = kwargs.get("to_email") or (args[0] if len(args) > 0 else "")
    subject = kwargs.get("subject") or (args[1] if len(args) > 1 else "")
    html_body = kwargs.get("html_body") or (args[2] if len(args) > 2 else "")
    plain_body = kwargs.get("plain_body") or (args[3] if len(args) > 3 else None)
    from_email = kwargs.get("from_email") or (args[4] if len(args) > 4 else None)

    res = send_email_via_gmail(
        to_email=to_email,
        subject=subject,
        html_body=html_body,
        plain_body=plain_body,
        from_email=from_email
    )
    return 200, res, {}
