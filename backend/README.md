# SS Platform — Backend (FastAPI + MySQL)

REST API powering both the **public website** and the **Admin Panel** —
services catalogue, CRM/leads, website content (banners, announcements,
projects, team, testimonials), theme/branding settings, and first-party
analytics.

---

## 1. Prerequisites

Install these before you start:

| Tool | Version | Check with |
|---|---|---|
| Python | 3.12+ | `python3 --version` |
| MySQL Server | 8.0+ (or MariaDB 10.6+) | `mysql --version` |
| pip | latest | `pip --version` |

You do **not** need Node.js for the backend — that's only for the
`website` folder (see the other README).

---

## 2. Get the code into a working folder

```bash
cd ss-platform-main/backend
```

Every command below is run from this `backend/` folder unless stated
otherwise.

---

## 3. Create and activate a virtual environment

```bash
python3 -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows (cmd)
venv\Scripts\activate.bat

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

Your terminal prompt should now show `(venv)` at the start of the line.

---

## 4. Install Python dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 5. Create the MySQL database

Open a MySQL client (`mysql -u root -p`, MySQL Workbench, phpMyAdmin,
whatever you use) and run:

```sql
CREATE DATABASE ss_platforms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

The database name `ss_platforms` must match `DB_NAME` in your `.env`
file (step 6) — change one or the other if you want a different name.

---

## 6. Configure environment variables

Copy the example file to `.env`:

```bash
# macOS / Linux
cp ".env example" .env

# Windows (cmd)
copy ".env example" .env
```

Open `.env` and fill in your real values:

```ini
APP_NAME="Saurabh Shukla Technology Platform API"
ENVIRONMENT=development
DEBUG=True
API_V1_PREFIX=/api/v1

SECRET_KEY="change-this-to-a-long-random-string"
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ALGORITHM=HS256

DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD="your_mysql_password"
DB_NAME=ss_platforms

# The frontend dev server origin(s), comma-separated
CORS_ORIGINS=http://localhost:5173
```

**Important:**
- `DB_PORT` — use `3306` for a standard local MySQL install. Only use
  `3307` (the sample default) if your MySQL is actually listening on
  that port (common with some Docker/XAMPP/Laragon setups).
- `SECRET_KEY` — must be a long random string in any real deployment.
  Generate one with: `python -c "import secrets; print(secrets.token_urlsafe(48))"`
- `CORS_ORIGINS` — must include whatever URL the website runs on, or
  the browser will block API requests. Add more than one, comma
  separated, if needed (e.g. `http://localhost:5173,https://yourdomain.com`).

---

## 7. Create the database tables (migrations)

This project uses Alembic. A migration that creates every table
already exists in `alembic/versions/`, so you normally just need to
apply it:

```bash
alembic upgrade head
```

If you ever add/change a SQLAlchemy model yourself later, generate a
new migration instead of editing the old one:

```bash
alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```

---

## 8. Seed default data

This creates the super-admin login, roles/permissions, service
categories and services, default theme colors, and sample website
content (banner, announcement, projects, team, testimonials) so the
site and admin panel aren't empty on first run.

```bash
python -m app.seed
```

This is **safe to run multiple times** — it updates existing rows
instead of duplicating them.

You'll see output ending with:

```
Super Admin Login
------------------
Email    : admin@ssplatform.com
Password : ChangeMe123!

IMPORTANT: Change the default password after first login.
```

---

## 9. Run the API server

```bash
uvicorn app.main:app --reload
```

The API is now running at:

- **API base**: http://127.0.0.1:8000/api/v1
- **Interactive docs (Swagger)**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **Health check**: http://127.0.0.1:8000/health

Keep this terminal running. Open a **new terminal** for the frontend
(see `website/README.md`).

---

## 10. Verify it works

```bash
curl http://127.0.0.1:8000/health
# {"status":"ok","environment":"development"}

curl http://127.0.0.1:8000/api/v1/services
# should return a JSON array of seeded services

curl http://127.0.0.1:8000/api/v1/settings/theme
# should return the default theme colors
```

Or just open http://127.0.0.1:8000/docs and try the endpoints from
the browser.

---

## Everyday commands (after first-time setup)

```bash
cd backend
source venv/bin/activate      # activate the venv each new terminal session
uvicorn app.main:app --reload # start the API
```

To reset/re-seed data at any time:

```bash
python -m app.seed
```

---

## API overview

| Area | Endpoints |
|---|---|
| Auth | `POST /auth/login`, `GET /auth/me` |
| Services | `GET /services`, `GET /services/{slug}`, admin CRUD under `/services/admin/*` |
| Inquiries (CRM intake) | `POST /inquiries` (public), `GET /inquiries/admin*` |
| CRM | `GET/PATCH /crm/leads/*` — lead pipeline, notes, follow-ups |
| Analytics | `POST /analytics/session\|page-view\|event`, `GET /analytics/admin/summary` |
| Website content | `GET/POST/PUT/DELETE` under `/website/banners`, `/website/announcements`, `/website/offers`, `/website/projects`, `/website/team`, `/website/testimonials` (public `GET`, everything else needs `content.manage`) |
| Theme / branding | `GET /settings/theme` (public), `PUT /settings/theme` (admin, needs `settings.manage`) |

All admin-only routes require a Bearer JWT from `/auth/login` and the
matching permission on the admin's role. The seeded `SUPER_ADMIN` role
has every permission.

---

## Project layout

```
app/
  core/        config (.env loading), DB session, JWT/password security, auth deps
  models/      SQLAlchemy models, one file per domain
  schemas/     Pydantic request/response schemas
  crud/
    generic.py   reusable CRUD router factory (list/create/update/delete)
  routers/     API endpoints, grouped by module
  seed.py      baseline + sample data for local/dev bring-up
  main.py      FastAPI app, CORS, router registration
alembic/       migration environment + versioned migrations
requirements.txt
.env example   copy this to .env (step 6)
```

---

## Troubleshooting

**`sqlalchemy.exc.OperationalError: ... Access denied` or `Unknown database`**
Your `.env` DB_* values don't match a real MySQL user/database. Re-check
step 5 and step 6.

**`Could not validate credentials` (401) when calling admin endpoints**
You're missing the `Authorization: Bearer <token>` header, or the token
expired. Log in again via `POST /auth/login`.

**CORS errors in the browser console**
Add the exact origin the website is served from to `CORS_ORIGINS` in
`.env`, then restart `uvicorn`.

**Port 8000 already in use**
Run on a different port: `uvicorn app.main:app --reload --port 8001`
(and update `VITE_API_BASE_URL` in the website's `.env` to match).

**Public site shows no services/projects/testimonials**
Run `python -m app.seed` — the site falls back to placeholder data
only if the API is unreachable or returns an empty list.


**Need to run public python server 
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

**remove reload when you run project all time
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000