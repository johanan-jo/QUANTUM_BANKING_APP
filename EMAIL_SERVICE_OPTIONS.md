# Email Service Options for Render Deployment

## 1. SendGrid (Recommended)
- Free tier: 100 emails/day
- Reliable delivery from cloud platforms
- Simple SMTP setup

## 2. Mailgun
- Free tier: 5,000 emails/month (first 3 months)
- Works well with Render

## 3. Postmark
- Free trial, then paid
- Excellent deliverability

## Quick Fix: Add timeout to current SMTP connection
Add timeout handling to prevent hanging connections