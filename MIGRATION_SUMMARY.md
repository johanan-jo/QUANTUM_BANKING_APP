# Migration Summary: MySQL → PostgreSQL/Supabase

## ✅ Completed Changes

### Database Migration
- **FROM**: MySQL (PyMySQL)
- **TO**: PostgreSQL (Supabase + psycopg2-binary)

### Files Modified

#### 1. `backend/utils/db.py`
- Replaced `pymysql` with `psycopg2`
- Added connection pooling with `SimpleConnectionPool`
- Support for `DATABASE_URL` environment variable (Supabase standard)
- Updated `count_recent_otps()` query: `DATE_SUB(NOW(), INTERVAL %s HOUR)` → `NOW() - INTERVAL '%s hours'`
- Using `RealDictCursor` for dict-based row results

#### 2. `backend/requirements.txt`
- **Removed**: `PyMySQL==1.1.0`
- **Added**: `psycopg2-binary==2.9.9`
- **Added**: `gunicorn==21.2.0` (for production deployment)

#### 3. `backend/sql/postgres_schema.sql` (NEW FILE)
- Converted MySQL DDL to PostgreSQL DDL
- Changed `AUTO_INCREMENT` → `SERIAL`
- Changed `TIMESTAMP` → `TIMESTAMP WITH TIME ZONE`
- Changed `ENUM` → `VARCHAR` with `CHECK` constraints
- Added `CREATE TRIGGER` for automatic `updated_at` timestamps
- Maintained all indexes and foreign keys
- Sample data included for testing

#### 4. `backend/app.py`
- Updated `validate_environment()` to support both `DATABASE_URL` and individual DB params
- Better error messages for missing configuration

#### 5. `backend/.env.example`
- Updated with Supabase connection string format
- Added PostgreSQL-specific environment variables
- Clear instructions for each variable

### Deployment Configuration

#### 6. `Procfile` (CREATED)
- Configured for Railway/Render deployment
- Uses gunicorn with optimized worker/thread settings

#### 7. `railway.toml` (CREATED)
- Railway-specific deployment configuration
- Build and start commands for Python backend

#### 8. `render.yaml` (CREATED)
- Render-specific deployment configuration
- Auto-configured environment variables
- Health check endpoint defined

#### 9. `vercel.json` (CREATED)
- Vercel deployment configuration for React frontend
- Proper routing and build settings
- Environment variable placeholders

#### 10. `backend/Dockerfile` (CREATED)
- Production-ready Docker image
- Includes psycopg2 system dependencies
- Security best practices (non-root user)
- Gunicorn as WSGI server

#### 11. `backend/.dockerignore` (CREATED)
- Optimized Docker build context
- Excludes unnecessary files for smaller images

### Documentation

#### 12. `DEPLOYMENT_GUIDE.md` (UPDATED)
- Complete step-by-step deployment guide
- Instructions for Supabase, Railway/Render, and Vercel
- Troubleshooting section
- Cost breakdown (all FREE services)
- Security checklist

#### 13. `README.md` (UPDATED)
- Updated tech stack section (PostgreSQL/Supabase)
- Updated prerequisites
- Added deployment section
- Updated database setup instructions

---

## 🚀 Deployment Stack (ALL FREE)

| Component | Service | Free Tier |
|-----------|---------|-----------|
| Frontend | Vercel | 100 GB bandwidth/month |
| Backend | Railway OR Render | 500-750 hours/month |
| Database | Supabase | 500 MB database, 2 GB bandwidth |
| Email | Gmail SMTP | Free (with App Password) |

**Total Monthly Cost: $0**

---

## 🔄 Key SQL Changes

### MySQL → PostgreSQL Syntax

| Feature | MySQL | PostgreSQL |
|---------|-------|------------|
| Auto-increment | `INT AUTO_INCREMENT` | `SERIAL` |
| Timestamp | `TIMESTAMP DEFAULT CURRENT_TIMESTAMP` | `TIMESTAMP WITH TIME ZONE DEFAULT NOW()` |
| Date math | `DATE_SUB(NOW(), INTERVAL 1 HOUR)` | `NOW() - INTERVAL '1 hour'` |
| Enum | `ENUM('credit', 'debit')` | `VARCHAR(20) CHECK (type IN ('credit', 'debit'))` |
| Update trigger | `ON UPDATE CURRENT_TIMESTAMP` | Custom trigger function |

---

## 📝 Environment Variables Required

### Production (Railway/Render)
```bash
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres
JWT_SECRET=your-64-char-random-secret
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
DEBUG_OTP=false
FLASK_ENV=production
```

### Frontend (Vercel)
```bash
REACT_APP_API_URL=https://your-backend.railway.app/api
```

---

## ✅ Testing Checklist

- [ ] Backend starts without errors
- [ ] Database connection successful
- [ ] Health endpoint returns 200: `/api/health`
- [ ] User registration works
- [ ] OTP email delivery works
- [ ] OTP verification works
- [ ] JWT token generation works
- [ ] Dashboard loads with user data
- [ ] Frontend connects to backend API
- [ ] CORS configured correctly

---

## 🔐 Security Notes

1. **DATABASE_URL** contains password - never commit to Git
2. **DEBUG_OTP** must be `false` in production (prevents OTP leakage)
3. Use **Gmail App Password**, not account password
4. Generate strong **JWT_SECRET**: `python -c "import secrets; print(secrets.token_urlsafe(64))"`
5. Enable **Row Level Security** in Supabase for additional protection
6. Keep dependencies updated: `pip list --outdated`

---

## 🎯 Next Steps

1. **Setup Supabase**: Create project, run `postgres_schema.sql`
2. **Deploy Backend**: Choose Railway or Render, add env vars
3. **Deploy Frontend**: Connect GitHub to Vercel, add `REACT_APP_API_URL`
4. **Configure CORS**: Add Vercel domain to `backend/app.py`
5. **Test**: Register new account, verify OTP email works
6. **Monitor**: Check logs in Railway/Render/Vercel dashboards

---

## 📚 Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Render Documentation](https://render.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)

---

## 🆘 Troubleshooting

**Import Error: "psycopg2 could not be resolved"**
- Install locally: `pip install psycopg2-binary`
- Or deploy - Railway/Render will install from requirements.txt

**Database Connection Error**
- Verify `DATABASE_URL` format is correct
- Check Supabase project is active (not paused after 7 days inactivity on free tier)
- Test connection: `psql DATABASE_URL`

**OTP Not Sending**
- Check Gmail App Password is correct
- Verify SMTP env vars are set
- Check backend logs for detailed error

**CORS Error**
- Add your Vercel domain to CORS origins in `backend/app.py`
- Include both production and preview domains: `https://*.vercel.app`

---

**Migration Complete! 🎉**

Your app is now ready to deploy on:
- ✅ Vercel (Frontend)
- ✅ Railway or Render (Backend)
- ✅ Supabase (Database)

See **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** for detailed deployment instructions.
