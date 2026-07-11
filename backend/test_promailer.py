1import os
from utils.mailer import send_email_via_promailer

# Load env from .env if needed
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

TO = os.getenv("TEST_TO") or os.getenv("SMTP_EMAIL")
SUBJECT = "Promailer Test - Quantum Banking"
FROM = os.getenv("FROM_EMAIL")

html = "<p>This is a test email sent via Promailer API.</p>"
text = "This is a test email sent via Promailer API."

try:
    resp = send_email_via_promailer(TO, SUBJECT, html, plain_body=text)
    print("Sent, status:", resp.status_code)
    print(resp.text)
except Exception as e:
    print("Failed to send via Promailer:", e)
