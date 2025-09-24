# Gmail SMTP Setup Guide

## Option 1: Use Gmail SMTP (Recommended)

### Step 1: Enable 2-Factor Authentication
1. Go to your Google Account settings
2. Security → 2-Step Verification
3. Turn on 2-Step Verification

### Step 2: Generate App Password
1. Go to Google Account → Security
2. Under "2-Step Verification" → App passwords
3. Select "Mail" and generate password
4. Copy the 16-character password

### Step 3: Update .env file
```env
SMTP_EMAIL=your_gmail@gmail.com
SMTP_PASSWORD=your_16_character_app_password
```

## Option 2: Use Outlook/Hotmail
```env
SMTP_EMAIL=your_email@outlook.com
SMTP_PASSWORD=your_password
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
```

## Option 3: For Testing (Use Temporary Email)
You can use services like:
- Mailtrap.io (for development)
- Ethereal Email (for testing)

## Current Configuration Needed:
- Replace `test@example.com` with your real email
- Replace `test_password` with your app password
- The system will automatically use Gmail SMTP settings

## Test Command:
After configuration, you can test email with:
```bash
python -c "from utils.mailer import send_otp_email; send_otp_email('test@recipient.com', '123456')"
```
