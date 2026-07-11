Promailer setup & usage for this project

Overview
- Purpose: send transactional OTP and welcome emails from Render using Promailer HTTP API (outbound HTTPS allowed).
- Required environment variables (set in Render service / locally):
  - PROMAILER_API_URL — full send endpoint (e.g. https://api.promailer.example/v1/send)
  - PROMAILER_API_KEY — secret API key (Bearer)
  - FROM_EMAIL — verified sender address (e.g. "Quantum Bank <no-reply@yourdomain.com>")

Quick steps to create an API key in Promailer
1. Sign up or log in to Promailer dashboard.
2. Verify your sender identity:
   - Add and verify the sending email or domain (follow Promailer instructions to validate via email or DNS).
3. Create an API key:
   - In the dashboard look for "API Keys" or "Integrations" → "Create API key".
   - Give it a descriptive name (e.g. "quantum-bank-render") and copy the key somewhere secure.
4. Obtain the send endpoint URL:
   - Many providers expose a single send endpoint (e.g. `https://api.promailer.example/v1/send`). Use the exact URL Promailer gives you.

Example cURL (Linux/macOS)

curl -X POST "<PROMAILER_API_URL>" \
  -H "Authorization: Bearer <PROMAILER_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "Quantum Bank <no-reply@yourdomain.com>",
    "to": "recipient@example.com",
    "subject": "Test email from Quantum Bank",
    "html": "<p>Hello — this is a test from Promailer.</p>",
    "text": "Hello — this is a test from Promailer."
  }'

PowerShell example (recommended for local testing on Windows / Render CLI)

$headers = @{ Authorization = "Bearer $env:PROMAILER_API_KEY"; 'Content-Type' = 'application/json' }
$body = @{ from = $env:FROM_EMAIL; to = 'recipient@example.com'; subject = 'Promailer test'; html = '<p>Test</p>'; text = 'Test' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri $env:PROMAILER_API_URL -Headers $headers -Body $body

Notes about request shape
- The JSON keys used above (`from`, `to`, `subject`, `html`, `text`) are common; confirm exact field names in the Promailer docs and adapt accordingly. If Promailer expects a different shape (e.g., `personalizations`, `content`, etc.), map `from/to/subject/html/text` into that shape.

Testing locally with this repo
- The repository includes a quick test script: `backend/test_promailer.py` which uses the same env vars.
- Run locally (PowerShell):

cd backend; python test_promailer.py

Setting Render environment variables
1. Go to your Render service dashboard for the backend.
2. Under "Environment" or "Environment Variables", add:
   - `PROMAILER_API_URL` = <the full send endpoint>
   - `PROMAILER_API_KEY` = <the API key you created>
   - `FROM_EMAIL` = "Quantum Bank <no-reply@yourdomain.com>"
3. Save and trigger a deploy (either via pushing a new commit or using the Render "Manual Deploy" button).

Verifying in production
- After deploy, trigger a login or welcome flow to send an OTP/welcome email.
- Check Render logs for mailer responses (request status and body). If you want more detailed logging, enable or add lightweight logging around the mailer call to print Promailer responses.
- Confirm delivery in the recipient inbox (and spam folder if missing).

Troubleshooting
- 401/403: check API key and that the key is active and not restricted.
- 4xx: inspect response body for validation errors (missing/invalid `from` or `to`, unverified sender).
- 5xx or timeouts: retry logic may help; log response and contact Promailer support.

Security
- Store `PROMAILER_API_KEY` only in Render secrets (do not commit to repo).
- Rotate API keys if you suspect exposure.

Next steps (optional)
- Add a small logging change in `backend/utils/mailer.py` to log Promailer status codes and response bodies for easier debugging in production.
- Add retries with exponential backoff for transient errors.
- If you want, I can implement the logging change and a retry wrapper — tell me to proceed.
