# 🚀 Quick Deploy Guide - TL;DR

## 3-Step Deployment (15 minutes total)

### Step 1: Database (Supabase) - 5 min
1. Go to https://supabase.com → New Project
2. SQL Editor → Paste `backend/sql/postgres_schema.sql` → Run
3. Settings → Database → Copy connection string → Save it

### Step 2: Backend (Railway) - 5 min
1. Go to https://railway.app → Deploy from GitHub
2. Add environment variables:
   ```
   DATABASE_URL=your-supabase-connection-string
   JWT_SECRET=run: python -c "import secrets; print(secrets.token_urlsafe(64))"
   SMTP_EMAIL=your-email@gmail.com
   SMTP_PASSWORD=your-gmail-app-password
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   DEBUG_OTP=false
   ```
3. Generate Domain → Copy backend URL

### Step 3: Frontend (Vercel) - 5 min
1. Go to https://vercel.com → Import GitHub repo
2. Root Directory: `frontend`
3. Add environment variable:
   ```
   REACT_APP_API_URL=https://your-backend.railway.app/api
   ```
4. Deploy → Done!

---

## Free Tier Limits
- ✅ Supabase: 500 MB database
- ✅ Railway: 500 hours/month ($5 credit)
- ✅ Vercel: Unlimited deployments
- **Cost: $0/month**

---

## Test Your Deployment
1. Visit frontend URL
2. Register new account
3. Check email for OTP
4. Login and view dashboard

Sample account (from seed data):
- Account: `1234567890`
- Password: `password123`

---

## Troubleshooting

**Backend won't start?**
- Check all env vars are set in Railway
- View logs in Railway dashboard

**OTP not received?**
- Use Gmail App Password (not account password)
- Check spam folder
- Verify SMTP_EMAIL and SMTP_PASSWORD

**Frontend can't connect?**
- Check REACT_APP_API_URL includes `/api`
- Add Vercel domain to CORS in `backend/app.py`
- Redeploy backend

**CORS error?**
Edit `backend/app.py`, add your Vercel URL to CORS:
```python
CORS(app, origins=[
    'https://your-app.vercel.app',
    'https://*.vercel.app'
])
```

---

## Files You Changed
- ✅ `backend/utils/db.py` - PostgreSQL connection
- ✅ `backend/requirements.txt` - psycopg2-binary
- ✅ `backend/sql/postgres_schema.sql` - Postgres schema
- ✅ `backend/.env.example` - Updated env template
- ✅ `backend/app.py` - DATABASE_URL support
- ✅ `Procfile` - Railway/Render config
- ✅ `railway.toml` - Railway config
- ✅ `render.yaml` - Render config
- ✅ `vercel.json` - Vercel frontend config

---

## Important URLs
- Supabase: https://app.supabase.com
- Railway: https://railway.app
- Render: https://render.com (alternative to Railway)
- Vercel: https://vercel.com

Full guide: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
