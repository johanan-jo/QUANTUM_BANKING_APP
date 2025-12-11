# SendGrid Setup for Email Delivery

## Step 1: Create SendGrid Account
1. Go to https://sendgrid.com/
2. Sign up for free account (100 emails/day free)
3. Verify your email address

## Step 2: Create API Key
1. Login to SendGrid dashboard
2. Go to Settings → API Keys
3. Click "Create API Key"
4. Choose "Restricted Access"
5. Give it a name like "Quantum Banking App"
6. Enable permissions for "Mail Send"
7. Click "Create & View"
8. **COPY THE API KEY** (you won't see it again!)

## Step 3: Update Environment Variables

### Local (.env file):
```
SMTP_EMAIL=quantumbankapp@gmail.com
SMTP_PASSWORD=your_sendgrid_api_key_here
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
```

### Render Dashboard:
- Go to your service → Environment
- Update:
  - `SMTP_PASSWORD` = `your_sendgrid_api_key_here`
  - `SMTP_HOST` = `smtp.sendgrid.net`
- Save Changes

## Step 4: Verify Sender Email (Important!)
1. In SendGrid → Settings → Sender Authentication
2. Click "Verify a Single Sender"
3. Add `quantumbankapp@gmail.com` as verified sender
4. Check your Gmail for verification email
5. Click verification link

## Why SendGrid Works:
- Designed for applications
- Render allows SendGrid SMTP connections
- Better deliverability than Gmail SMTP
- Free tier sufficient for testing

## Test Command:
```bash
curl -i --request POST \
--url https://api.sendgrid.com/v3/mail/send \
--header 'Authorization: Bearer your_sendgrid_api_key_here' \
--header 'Content-Type: application/json' \
--data '{"personalizations": [{"to": [{"email": "test@example.com"}]}],"from": {"email": "quantumbankapp@gmail.com"},"subject": "Test","content": [{"type": "text/plain", "value": "Hello, World!"}]}'
```