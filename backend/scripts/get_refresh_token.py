#!/usr/bin/env python3
"""
Gmail API OAuth 2.0 Refresh Token Generator for Quantum Banking

This script runs locally to perform the one-time interactive OAuth consent flow
and obtain a refresh token for the authorized sender account.

How to use:
1. Place your downloaded `client_secret.json` from Google Cloud Console in this directory,
   OR supply GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET as environment variables / CLI inputs.
2. Run: python get_refresh_token.py
3. Complete the Google account authentication in your browser.
4. Copy the output REFRESH_TOKEN to your `.env` and Render dashboard.
"""

import os
import sys
import json

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def main():
    print("=" * 60)
    print("🔑 Quantum Banking - Gmail OAuth 2.0 Refresh Token Helper")
    print("=" * 60)

    client_id = None
    client_secret = None

    # Option A: Look for client_secret.json in current directory or backend/
    json_candidates = [
        "client_secret.json",
        os.path.join(os.path.dirname(__file__), "client_secret.json"),
        os.path.join(os.path.dirname(__file__), "..", "client_secret.json"),
    ]

    found_json = None
    for path in json_candidates:
        if os.path.exists(path):
            found_json = path
            break

    if found_json:
        print(f"📄 Found OAuth client file: {found_json}")
        try:
            with open(found_json, "r") as f:
                data = json.load(f)
                info = data.get("installed") or data.get("web") or {}
                client_id = info.get("client_id")
                client_secret = info.get("client_secret")
        except Exception as e:
            print(f"⚠️ Could not parse {found_json}: {e}")

    # Option B: Look in environment variables
    if not client_id or not client_secret:
        client_id = os.getenv("GMAIL_CLIENT_ID")
        client_secret = os.getenv("GMAIL_CLIENT_SECRET")

    # Option C: Interactive prompt
    if not client_id or not client_secret:
        print("\nCould not find client_secret.json or environment variables.")
        print("Please enter your OAuth 2.0 Client credentials from Google Cloud Console:")
        client_id = input("Client ID: ").strip()
        client_secret = input("Client Secret: ").strip()

    if not client_id or not client_secret:
        print("❌ Error: Both Client ID and Client Secret are required to proceed.")
        sys.exit(1)

    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost", "urn:ietf:wg:oauth:2.0:oob"]
        }
    }

    try:
        print("\n🌐 Launching local authentication server for Google consent...")
        flow = InstalledAppFlow.from_client_config(client_config, scopes=SCOPES)
        # prompt='consent' and access_type='offline' ensures a refresh_token is always returned
        creds = flow.run_local_server(port=0, prompt="consent", access_type="offline")

        if not creds.refresh_token:
            print("⚠️ Warning: Google did not return a refresh token.")
            print("Ensure access_type='offline' and prompt='consent' were set, or revoke previous app access in Google Account permissions.")
        else:
            print("\n" + "=" * 60)
            print("✅ SUCCESS! Copy these into your .env and Render Environment Variables:")
            print("=" * 60)
            print(f"GMAIL_CLIENT_ID={client_id}")
            print(f"GMAIL_CLIENT_SECRET={client_secret}")
            print(f"GMAIL_REFRESH_TOKEN={creds.refresh_token}")
            print("=" * 60)
            print("Keep your Client Secret and Refresh Token strictly confidential!")

    except Exception as e:
        print(f"\n❌ OAuth flow failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
