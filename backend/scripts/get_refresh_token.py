#!/usr/bin/env python3
import json
from google_auth_oauthlib.flow import InstalledAppFlow

# Scope limited to sending emails
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def main():
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json",
        scopes=SCOPES
    )
    creds = flow.run_local_server(port=0)  # opens browser for consent
    print("=== COPY THESE (keep them secret) ===")
    print("REFRESH_TOKEN:", creds.refresh_token)
    # client_id and client_secret are in client_secret.json, but print if you want:
    try:
        with open("client_secret.json", "r") as f:
            client_info = json.load(f)
            client_id = client_info.get("installed", {}).get("client_id")
            client_secret = client_info.get("installed", {}).get("client_secret")
            if client_id:
                print("CLIENT_ID:", client_id)
            if client_secret:
                print("CLIENT_SECRET:", client_secret)
    except Exception:
        pass
    print("=== END ===")

if __name__ == "__main__":
    main()
