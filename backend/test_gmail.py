#!/usr/bin/env python3
"""
Automated & Manual Diagnostic Tool for Gmail API OAuth 2.0 Integration

Usage:
    # 1. Run configuration diagnostics:
    python test_gmail.py

    # 2. Run dry-run / mock message compilation:
    python test_gmail.py --dry-run

    # 3. Send an actual test email:
    python test_gmail.py --send recipient@example.com
"""

import os
import sys
import argparse

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

from utils.gmail_service import (
    GmailService,
    GmailServiceError,
    _mask_email
)
from utils.mailer import send_otp_email, send_welcome_email

def run_diagnostics():
    print("=" * 65)
    print("🔬 Quantum Banking - Gmail API Diagnostic Report")
    print("=" * 65)

    client_id = os.getenv("GMAIL_CLIENT_ID") or os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GMAIL_CLIENT_SECRET") or os.getenv("GOOGLE_CLIENT_SECRET")
    refresh_token = os.getenv("GMAIL_REFRESH_TOKEN") or os.getenv("GOOGLE_REFRESH_TOKEN")
    sender_email = (
        os.getenv("GMAIL_SENDER_EMAIL")
        or os.getenv("FROM_EMAIL")
        or os.getenv("SMTP_EMAIL")
    )

    all_present = True
    print("\n1. Environment Variables Check:")
    for var_name, val in [
        ("GMAIL_CLIENT_ID", client_id),
        ("GMAIL_CLIENT_SECRET", client_secret),
        ("GMAIL_REFRESH_TOKEN", refresh_token),
        ("GMAIL_SENDER_EMAIL", sender_email),
    ]:
        if not val:
            print(f"   ❌ {var_name:<20}: MISSING")
            all_present = False
        else:
            if "SECRET" in var_name or "TOKEN" in var_name:
                preview = val[:4] + "*" * 12
            elif "ID" in var_name:
                preview = val[:8] + "..." + val[-10:] if len(val) > 18 else "Set"
            else:
                preview = val
            print(f"   ✅ {var_name:<20}: Configured ({preview})")

    if not all_present:
        print("\n⚠️ Status: Environment variables are incomplete.")
        print("   Follow the instructions in GMAIL_API_SETUP.md to set up credentials.")
        return False

    print("\n2. Testing OAuth Token Refresh & Credentials Validation...")
    service = GmailService()
    try:
        creds = service.get_credentials()
        print(f"   ✅ OAuth credentials refreshed and valid! (Expiry: {creds.expiry})")
    except GmailServiceError as gse:
        print(f"   ❌ Token refresh failed: {gse}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

    print("\n3. Testing Gmail API Service Resource Initialization...")
    try:
        gmail_res = service.get_service()
        profile = gmail_res.users().getProfile(userId="me").execute()
        gmail_address = profile.get("emailAddress", "Unknown")
        print(f"   ✅ Gmail API connected successfully! Authorized mailbox: {gmail_address}")
    except Exception as e:
        print(f"   ❌ Gmail API profile lookup failed: {e}")
        return False

    print("\n🎉 Diagnostics complete: All Gmail API components operational!")
    return True


def run_dry_run():
    print("Testing MIME message creation and encoding (no network calls)...")
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import base64

    message = MIMEMultipart("alternative")
    message["to"] = "user@example.com"
    message["from"] = "bank@example.com"
    message["subject"] = "Test Subject"
    message.attach(MIMEText("Plain text body", "plain", "utf-8"))
    message.attach(MIMEText("<h1>HTML body</h1>", "html", "utf-8"))
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    assert len(raw) > 0
    print("✅ MIME message generation and Base64 urlsafe encoding verified.")


def main():
    parser = argparse.ArgumentParser(description="Gmail API test harness")
    parser.add_argument("--dry-run", action="store_true", help="Perform dry-run without sending emails")
    parser.add_argument("--send", type=str, help="Recipient email address to send a test OTP email")
    args = parser.parse_args()

    if args.dry_run:
        run_dry_run()
        return

    if args.send:
        recipient = args.send.strip()
        print(f"🚀 Dispatching test OTP to {recipient}...")
        success = send_otp_email(recipient, "741852")
        if success:
            print("✅ Test OTP email sent successfully via Gmail API!")
        else:
            print("❌ Failed to send test OTP email. See logs for details.")
        return

    run_diagnostics()


if __name__ == "__main__":
    main()
