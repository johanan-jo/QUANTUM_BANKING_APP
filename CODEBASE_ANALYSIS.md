# Codebase & Architecture Analysis: Quantum Banking Application

**Generated Date**: October 2026  
**Repository**: `QUANTUM_BANKING_APP` (`LIL3`)  
**Technology Stack**: Flask (Python 3.13/3.8+), React 18, PostgreSQL (Supabase), SendGrid / Gmail SMTP, Vercel & Render  

---

## 1. Executive Summary

**Quantum Banking** is a full-stack financial technology demonstration and prototype banking web application. It integrates a simulated **quantum-inspired One-Time Password (OTP)** mechanism, standard **Bcrypt password hashing**, **JWT session authentication**, and **real-time email dispatch** via SendGrid/SMTP.

The repository is structured as a dual-tier monolith comprising a Flask REST API backend (`/backend`) and a Create-React-App frontend (`/frontend`), alongside extensive ethical hacking, automated security testing, and deployment orchestration files.

---

## 2. Architecture & System Flow

```
[ Client Browser ]
        │  ▲
        │  │ (HTTPS / REST API)
        ▼  │
┌────────────────────────┐
│  React 18 Frontend     │ (Vercel)
│  - App.jsx             │
│  - Axios Client        │
│  - CSS Theme Engine    │
└──────────┬─────────────┘
           │
           ▼
┌────────────────────────┐
│   Flask REST API       │ (Render / Local Port 5000)
│  - /api/auth/*         │
│  - /api/dashboard/*    │
└────┬───────────────┬───┘
     │               │
     ▼               ▼
┌──────────────┐  ┌────────────────────────────────┐
│  PostgreSQL  │  │  Quantum OTP Engine & Mailer   │
│  (Supabase)  │  │  - QuantumOTPGenerator (Sim)   │
│  - users     │  │  - SendGrid API / Gmail SMTP   │
│  - otps      │  └────────────────────────────────┘
└──────────────┘
```

### Key Workflow
1. **User Registration**: Client submits name, email, and password. The backend auto-generates a unique 10-digit account number, hashes the password using bcrypt, stores the user in PostgreSQL, and dispatches a welcome email.
2. **Authentication Step 1 (Login)**: Client provides account number and password. Server validates credentials against the database. If valid, the Quantum OTP Engine generates a 6-digit OTP code, saves it to the database with a 5-minute expiry, and sends the code to the user's email asynchronously via a background worker thread.
3. **Authentication Step 2 (OTP Verification)**: Client submits the 6-digit OTP. The server validates the OTP against active unexpired tokens, marks the token as used, and returns an encrypted JWT signed with `HS256` (24-hour expiration).
4. **Authorized Session (Dashboard)**: The client includes `Authorization: Bearer <JWT>` on subsequent requests to fetch account details, transaction history, and balance.

---

## 3. Directory & File Inventory

### 3.1 Root Directory Analysis

| File / Directory | Size / State | Purpose & Role |
| :--- | :--- | :--- |
| `backend/` | Directory | Complete Flask REST API backend and database modules. |
| `frontend/` | Directory | Complete React 18 single-page application. |
| `penetration_test_report.json` | 948 bytes | JSON report from previous automated security audits; records 2 medium rate-limiting findings. |
| `professional_pentest.py` | ~12 KB | Comprehensive ethical hacking suite covering SQLi, auth bypass, OTP timing, and recon. |
| `security_assessment.py` | ~10 KB | Secondary security audit script testing JWT vulnerabilities, XSS, headers, and CORS. |
| `otp_attack_simulation.py` | ~8 KB | Simulation tool for OTP timing attacks and brute-force vulnerability checks. |
| `test_sql_injection.py` | ~5 KB | Automated SQL injection test harness against auth endpoints. |
| `sql_injection_examples.py` | ~3.5 KB | Educational code sample comparing vulnerable string formatting vs secure parameterized queries. |
| `Procfile` | 89 bytes | Heroku/Render process configuration: runs `gunicorn` inside `backend/`. |
| `render.yaml` | 647 bytes | Render blueprint configuring the web service, build steps, and environment variables. |
| `vercel.json` | 382 bytes | Vercel deployment spec for building React and routing rewrites to `/index.html`. |
| `app.py`, `application.py`, `main.py`, `server.py`, `wsgi.py` | **0 bytes (Empty)** | Placeholder root entry points often expected by standard PaaS buildpacks; actual application entry point is `backend/app.py`. |
| `requirements.txt` | 154 bytes | Root-level Python dependencies (mirrors backend requirements). |
| `setup.bat`, `setup.sh`, `setup_database.bat` | Script files | Automation scripts for environment bootstrapping, venv creation, and DB setup. |

### 3.2 Backend Structure (`/backend`)

| Path | Purpose |
| :--- | :--- |
| `app.py` | Flask application factory (`create_app`), CORS middleware, blueprint registration, and health endpoints (`/`, `/api/health`). |
| `routes/auth.py` | Authentication controller: handles `/register`, `/login`, and `/verify-otp`. |
| `routes/dashboard.py` | Dashboard controller: handles `/me`, `/transfer`, `/deposit`, `/withdraw` (protected via `@token_required`). |
| `utils/db.py` | PostgreSQL database connection pool (`psycopg2.pool.SimpleConnectionPool`), transactional helpers, and parameterized SQL queries. |
| `utils/security.py` | Cryptographic utilities: `hash_password`, `verify_password`, `generate_jwt_token`, `decode_jwt_token`, `@token_required` decorator, and input validators. |
| `utils/quantum_otp.py` | Simulation engine for quantum OTP generation using simulated photon polarizations (horizontal, diagonal, circular, mixed) combined with HMAC-SHA256. |
| `utils/mailer.py` | Multi-provider email dispatch engine: primary delivery via SendGrid REST API, fallback to Gmail SMTP SSL/TLS with HTML templating. |
| `sql/postgres_schema.sql` | Supabase/PostgreSQL DDL: table schemas for `users` and `otps` with indexing. |
| `sql/schema.sql` | Legacy MySQL/SQLite schema definitions. |
| `.env.example` | Template for environment variables (`DATABASE_URL`, `JWT_SECRET`, `SENDGRID_API_KEY`, `SMTP_*`). |

### 3.3 Frontend Structure (`/frontend`)

| Path | Purpose |
| :--- | :--- |
| `src/App.jsx` | Primary React application controller; manages view transitions (`login`, `register`, `otp`, `dashboard`) and auth state. |
| `src/api.js` | Centralized Axios HTTP client, API base URL configuration, request/response interceptors, and JWT local storage helpers. |
| `src/config.js` | Environment configuration detecting `process.env.REACT_APP_API_URL` or defaulting to `http://localhost:5000/api`. |
| `src/index.css` & `src/legendary.css` | Styling layers providing banking glassmorphism, responsive grids, and animations without relying on runtime Tailwind post-processing. |
| `src/components/` | UI component library with standard and "Legendary" visual themes: `Login.jsx`, `Register.jsx`, `OtpVerify.jsx`, `Dashboard.jsx`, etc. |

---

## 4. Deep-Dive Security & Vulnerability Audit

### 4.1 SQL Injection Protection: **PASS**
* **Findings**: In `backend/utils/db.py`, queries are executed using `cursor.execute(query, params)` with tuple parameterization (`%s`).
* **Verification**: Running `test_sql_injection.py` confirms that payloads such as `admin' --`, `' OR '1'='1`, and `'; DROP TABLE users; --` are handled as literal string inputs and do not disrupt the SQL parser.

### 4.2 Rate Limiting & Brute-Force Protection: **PARTIAL / MEDIUM RISK**
* **Identified in `penetration_test_report.json`**:
  1. *Issue 1*: "Multiple OTP attempts allowed without blocking"
  2. *Issue 2*: "Allowed 50 rapid requests without blocking"
* **Code State**:
  * In `backend/routes/auth.py`, `count_recent_otps(user['id'], hours=1)` limits OTP generation requests to 3 per hour.
  * **Vulnerability**: In `verify-otp`, there is **no attempt counter or temporary lockout** on repeated failed OTP verification attempts. An attacker could theoretically brute-force the 6-digit OTP within its 5-minute validity window.
  * **Vulnerability**: There is no IP-based global rate limiting middleware (e.g., `Flask-Limiter`) applied to `/api/auth/login` or `/api/auth/register`.

### 4.3 Sensitive Configuration & Debug Leaks: **LOW / MEDIUM RISK**
* **Debug OTP Mode**: Lines 157–159 in `backend/routes/auth.py` reveal the OTP directly in the API response if `DEBUG_OTP=true`:
  ```python
  if os.getenv('DEBUG_OTP', 'false').lower() == 'true':
      response_data['debug_otp'] = otp_code
  ```
  While intentional for development, this presents a critical authentication bypass if mistakenly enabled in staging or production.
* **CORS Wildcard Configuration**: `app.py` specifies `resources={r"/api/*": {"origins": "*"}}` with `supports_credentials=True`. Modern browsers restrict credentialed requests with wildcard origins.

### 4.4 Password & Token Cryptography: **PASS**
* Password hashing uses industry-standard `bcrypt.hashpw` with per-hash random salt generation.
* JWT generation uses `HS256` with expiration validation (`jwt.ExpiredSignatureError`).

---

## 5. Technical Debt & Code Cleanup Opportunities

1. **Empty Root Python Files**: `app.py`, `application.py`, `main.py`, `server.py`, and `wsgi.py` in the project root are 0 bytes. If a PaaS default detector picks one of these empty root files instead of following `Procfile` / `render.yaml`, the build or startup will crash.
2. **Redundant Frontend Components**: Inside `frontend/src/components/`, there are multiple variants of the same screens (`Login.jsx`, `LoginClean.jsx`, `LoginLegendary.jsx`, `RegisterClean.jsx`, etc.). Only one variant is actively imported into `App.jsx`. The unused legacy variants should be archived or removed.
3. **Mock Data in Protected Endpoints**: In `backend/routes/dashboard.py`, account balances and transaction histories are procedurally generated using Python's `random.seed(user['id'])` rather than queried from real database tables (`accounts`, `transactions`).
4. **Quantum OTP Nature**: As documented in `backend/utils/quantum_otp.py`, the module is an algorithmic simulation utilizing pseudo-random bit entropy, suitable for demonstration purposes.

---

## 6. Actionable Recommendations

| Priority | Category | Action Item |
| :--- | :--- | :--- |
| **High** | Security | Implement `Flask-Limiter` on `/api/auth/login` and `/api/auth/verify-otp` (e.g., max 5 failed attempts per 10 minutes). |
| **High** | Security | Add failed OTP counter in the `otps` table to invalidate an OTP token after 3 incorrect verification attempts. |
| **Medium** | Security | Restrict CORS origin in `backend/app.py` from `*` to the actual production frontend domain (e.g., Vercel URL). |
| **Medium** | Cleanup | Populate or remove the 0-byte root entry point files (`app.py`, `wsgi.py`) by redirecting them to `backend.app:create_app()`. |
| **Low** | Architecture | Implement actual `transactions` and `accounts` database tables to replace mock random data in `dashboard.py`. |

---

## 7. Summary Table of Key Existing Documentation

| Document | Purpose |
| :--- | :--- |
| [`README.md`](file:///c:/Users/johan/Downloads/LIL3/LIL3/README.md) | High-level project overview, quickstart instructions, and stack summary. |
| [`DEPLOYMENT_GUIDE.md`](file:///c:/Users/johan/Downloads/LIL3/LIL3/DEPLOYMENT_GUIDE.md) | Step-by-step production setup across Vercel, Render, and Supabase. |
| [`EMAIL_SETUP_GUIDE.md`](file:///c:/Users/johan/Downloads/LIL3/LIL3/EMAIL_SETUP_GUIDE.md) | Comprehensive configuration guide for SendGrid API and Gmail SMTP app passwords. |
| [`ENVIRONMENT_VARIABLES.md`](file:///c:/Users/johan/Downloads/LIL3/LIL3/ENVIRONMENT_VARIABLES.md) | Exhaustive environment variable reference for both backend and frontend. |
| [`MIGRATION_SUMMARY.md`](file:///c:/Users/johan/Downloads/LIL3/LIL3/MIGRATION_SUMMARY.md) | Technical notes on the migration from SQLite to PostgreSQL. |
| [`PROJECT_STATUS.md`](file:///c:/Users/johan/Downloads/LIL3/LIL3/PROJECT_STATUS.md) | Development log detailing CSS and React build resolution. |
