# Deployment Guide - Quantum Banking App

Complete guide to deploy your Quantum Banking application using free services:
- **Frontend**: Vercel (free tier)
- **Backend**: Railway or Render (free tier)
- **Database**: Supabase (free tier)

---

## 📋 Prerequisites

1. GitHub account (for connecting repositories)
2. Accounts on:
   - [Supabase](https://supabase.com) - Database
   - [Railway](https://railway.app) OR [Render](https://render.com) - Backend
   - [Vercel](https://vercel.com) - Frontend
3. Gmail account with App Password for SMTP

---

## 🗄️ Step 1: Setup Supabase Database

### 1.1 Create Supabase Project
1. Go to https://app.supabase.com
2. Click "New Project"
3. Choose organization and fill in:
   - Project name: `quantum-banking`
   - Database password: (save this securely)
   - Region: Choose closest to you
4. Wait for project to be created (~2 minutes)

### 1.2 Run Database Schema
1. In your Supabase project, go to **SQL Editor**
2. Click "New Query"
3. Copy the entire contents of `backend/sql/postgres_schema.sql`
4. Paste into the SQL editor
5. Click "Run" to execute
6. Verify tables created: Go to **Table Editor** and see `users`, `otps`, `transactions`

### 1.3 Get Connection String
1. Go to **Project Settings** > **Database**
2. Scroll to **Connection String** section
3. Select **URI** tab
4. Copy the connection string (format: `postgresql://postgres:[YOUR-PASSWORD]@...`)
5. Replace `[YOUR-PASSWORD]` with your actual database password
6. Save this - you'll need it for backend deployment

**Example:**
```
postgresql://postgres:your_actual_password@db.abcdefghijklmnop.supabase.co:5432/postgres
```

---

## 🚀 Step 2: Deploy Backend (Choose ONE option)

### Option A: Railway (Recommended - Easiest)

#### 2.1 Setup Railway Project
1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `QUANTUM_BANKING_APP` repository
6. Railway will auto-detect and deploy

#### 2.2 Configure Environment Variables
1. In Railway dashboard, click on your service
2. Go to **Variables** tab
3. Add these variables:

```bash
DATABASE_URL=postgresql://postgres:your_password@db.xxxxx.supabase.co:5432/postgres
JWT_SECRET=generate-random-64-char-string
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
DEBUG_OTP=false
FLASK_ENV=production
```

**Generate JWT_SECRET:**
```powershell
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

#### 2.3 Get Backend URL
1. Railway will auto-deploy after you save variables
2. Click on your service > **Settings** > **Networking**
3. Click "Generate Domain"
4. Copy the URL (e.g., `https://your-app.up.railway.app`)
5. Save this for frontend configuration

---

### Option B: Render

#### 2.1 Setup Render Service
1. Go to https://render.com
2. Sign in with GitHub
3. Click "New +" > "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: `quantum-banking-backend`
   - **Root Directory**: Leave blank (or use `/backend` if needed)
   - **Environment**: Python 3
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Plan**: Free

#### 2.2 Add Environment Variables
In Render dashboard, go to **Environment** tab and add:

```bash
DATABASE_URL=postgresql://postgres:your_password@db.xxxxx.supabase.co:5432/postgres
JWT_SECRET=generate-random-64-char-string
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
DEBUG_OTP=false
FLASK_ENV=production
```

#### 2.3 Deploy
1. Click "Create Web Service"
2. Wait for deployment (~5 minutes)
3. Copy your service URL (e.g., `https://quantum-banking-backend.onrender.com`)

---

## 🌐 Step 3: Deploy Frontend (Vercel)

### 3.1 Setup Vercel Project
1. Go to https://vercel.com
2. Sign in with GitHub
3. Click "Add New..." > "Project"
4. Import your `QUANTUM_BANKING_APP` repository
5. Configure:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

### 3.2 Add Environment Variable
Before deploying, add this environment variable:

1. Click **Environment Variables**
2. Add:
   - **Key**: `REACT_APP_API_URL`
   - **Value**: `https://your-backend-url.railway.app/api` (or your Render URL + `/api`)
   - **Environments**: Production, Preview, Development (check all)

**Important**: Make sure to include `/api` at the end of your backend URL!

**Example:**
```
REACT_APP_API_URL=https://quantum-banking-backend.up.railway.app/api
```

### 3.3 Deploy
1. Click "Deploy"
2. Wait for build (~2-3 minutes)
3. Your app will be live at: `https://your-app.vercel.app`

---

## 🔒 Step 4: Configure Gmail App Password (SMTP)

### 4.1 Enable 2-Factor Authentication
1. Go to https://myaccount.google.com
2. Navigate to **Security**
3. Enable **2-Step Verification** if not already enabled

### 4.2 Generate App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select app: **Mail**
3. Select device: **Other** (custom name) - enter "Quantum Banking"
4. Click **Generate**
5. Copy the 16-character password (format: `xxxx xxxx xxxx xxxx`)
6. Use this as `SMTP_PASSWORD` in your backend environment variables

### 4.3 Update Backend Environment
- In Railway or Render, update the `SMTP_PASSWORD` variable with your app password
- Redeploy if necessary

---

## ✅ Step 5: CORS Configuration (Already Done! ✨)

### 5.1 CORS Pre-configured
Good news! The backend CORS is already configured with wildcard patterns to support any deployment:

```python
CORS(app, origins=[
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'https://*.vercel.app',    # All Vercel deployments ✅
    'https://*.railway.app',   # All Railway deployments ✅
    'https://*.onrender.com'   # All Render deployments ✅
])
```

**What this means:**
- ✅ Your Vercel frontend will work immediately with Railway/Render backend
- ✅ Preview deployments on Vercel work automatically
- ✅ No need to update CORS after each deployment
- ✅ Works for team members' deployments too

**Optional:** If you want to restrict to specific domains only:
1. Edit `backend/app.py`
2. Replace wildcards with your exact URLs
3. Example: `'https://quantum-banking.vercel.app'`
4. Commit and push - backend will auto-redeploy

---

## 🧪 Step 6: Test Your Deployment

### 6.1 Test Backend Health
Open in browser:
```
https://your-backend-url.railway.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "services": {
    "database": "connected",
    "email": "configured",
    "quantum_otp": "active"
  }
}
```

### 6.2 Test Frontend
1. Visit your Vercel URL: `https://your-app.vercel.app`
2. Try registering a new account
3. Check your email for OTP
4. Login and verify dashboard loads

### 6.3 Sample Test Account
Use these credentials to test (from sample data):
- **Account Number**: `1234567890`
- **Password**: `password123`

---

## 🚨 Troubleshooting

### Backend Issues

**Error: "Database connection failed"**
- Verify `DATABASE_URL` is correct in environment variables
- Check Supabase project is active (not paused)
- Ensure password doesn't contain special characters that need URL encoding

**Error: "SMTP authentication failed"**
- Verify Gmail App Password is correct
- Ensure 2FA is enabled on Gmail account
- Check `SMTP_EMAIL` and `SMTP_PASSWORD` are set correctly

**Error: "Module not found"**
- Check `requirements.txt` is in `backend/` folder
- Verify build command includes: `cd backend && pip install -r requirements.txt`

### Frontend Issues

**Error: "Network Error" or "Failed to fetch"**
- Check `REACT_APP_API_URL` is set correctly in Vercel
- Ensure backend URL includes `/api` at the end
- Verify backend is deployed and healthy
- Check browser console for CORS errors

**CORS Error**
- Add your Vercel domain to CORS origins in `backend/app.py`
- Redeploy backend after changes

**OTP not received**
- Check spam/junk folder
- Verify SMTP credentials are correct
- Check backend logs for email errors

---

## 📊 Monitoring & Logs

### Railway Logs
1. Go to Railway dashboard
2. Click on your service
3. View **Deployments** tab for logs

### Render Logs
1. Go to Render dashboard
2. Click on your service
3. View **Logs** tab

### Vercel Logs
1. Go to Vercel dashboard
2. Click on your project
3. View **Deployments** > Select deployment > **Function Logs**

---

## 🔄 Making Updates

### Update Backend
1. Make code changes locally
2. Commit and push to GitHub
3. Railway/Render auto-deploys (wait ~2-3 minutes)

### Update Frontend
1. Make code changes locally
2. Commit and push to GitHub
3. Vercel auto-deploys (wait ~2-3 minutes)

### Update Environment Variables
- Railway: Dashboard > Variables > Add/Edit
- Render: Dashboard > Environment > Add/Edit
- Vercel: Dashboard > Settings > Environment Variables

Changes to environment variables require redeployment.

---

## 💰 Cost Breakdown (All FREE!)

| Service | Free Tier Limits |
|---------|------------------|
| **Supabase** | 500 MB database, 2 GB bandwidth/month |
| **Railway** | 500 hours/month, $5 credit |
| **Render** | 750 hours/month |
| **Vercel** | 100 GB bandwidth/month, unlimited deployments |

**Total Monthly Cost: $0** 🎉

---

## 🔐 Security Checklist

- [ ] Set strong `JWT_SECRET` (min 64 characters)
- [ ] Set `DEBUG_OTP=false` in production
- [ ] Use Gmail App Password (not account password)
- [ ] Never commit `.env` file to GitHub
- [ ] Keep Supabase password secure
- [ ] Enable Supabase Row Level Security (RLS) if needed
- [ ] Regularly update dependencies
- [ ] Monitor error logs for suspicious activity

---

## 📚 Useful Commands

### Local Development

**Backend:**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

**Frontend:**
```powershell
cd frontend
npm install
npm start
```

### Generate Secure Secrets
```powershell
# JWT Secret
python -c "import secrets; print(secrets.token_urlsafe(64))"

# Bcrypt Password Hash
python -c "import bcrypt; pw='password123'; print(bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode())"
```

---

## 🆘 Need Help?

1. Check logs in Railway/Render/Vercel dashboards
2. Verify all environment variables are set correctly
3. Test backend health endpoint directly
4. Check browser console for frontend errors
5. Review this guide step by step

---

**🎉 Congratulations! Your Quantum Banking app is now live!**

Frontend: `https://your-app.vercel.app`  
Backend: `https://your-backend.railway.app`  
Database: Supabase PostgreSQL
