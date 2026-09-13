# Saurabh Shukla Technology Platform — Backend Foundation

FastAPI + MySQL backend implementing the core data model and REST API
from the Business Growth Blueprint document (sections 6, 8, 9, 11, 13, 15).

## Stack
- Python 3.13+, FastAPI, Pydantic v2, SQLAlchemy 2 (typed models), Alembic
- MySQL (PyMySQL driver)
- JWT auth (python-jose) + bcrypt password hashing (passlib)

## What's implemented in this foundation

**Database (MySQL, section 11)** — full SQLAlchemy model set for all
domains in the spec: Identity, Services, CRM, Commerce, Subscriptions,
Credits, Analytics, Content, Brand, Operations (`app/models/`).

**REST API (section 13)** — working endpoints:
- `POST /api/v1/auth/login`, `GET /api/v1/auth/me` — Admin JWT auth
- `GET /api/v1/services`, `GET /api/v1/services/{slug}` — public catalogue
- `POST/PUT/DELETE /api/v1/services/admin/*` — admin CRUD (permission-gated)
- `POST /api/v1/inquiries` — public "Get Quote"/Contact form → auto-creates a `NEW` lead
- `GET /api/v1/inquiries/admin`, `GET /api/v1/inquiries/admin/{id}` — admin view
- `GET/PATCH /api/v1/crm/leads/*` — lead pipeline (status transitions, notes, follow-ups)
- `POST /api/v1/analytics/session|page-view|event` — first-party visitor tracking (section 9)
- `GET /api/v1/analytics/admin/summary` — visitor/session/event KPIs (section 18)

**Security (section 15)** — JWT auth, role/permission-based authorization
(`require_permission(...)` dependency), bcrypt hashing, CORS config,
no sensitive payment data stored (only gateway references — see
`payment_transactions` model comment), audit log table ready for use.

**Not yet built** (next phases): payment gateway integration (Razorpay),
subscription billing/renewal jobs, admin panel UI, public website,
content/SEO admin endpoints, email/WhatsApp sending, file uploads.
The database tables for all of these already exist so the next phase
is wiring routers + business logic on top of them.

## Setup

```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edit .env: set DB_USER, DB_PASSWORD, DB_NAME, SECRET_KEY

# Create the MySQL database first:
#   CREATE DATABASE ss_platform_db CHARACTER SET utf8mb4;

# Generate and apply the first migration (creates all tables)
alembic revision --autogenerate -m "initial schema"
alembic upgrade head

# Seed baseline roles/permissions/super-admin + sample categories
python -m app.seed

# Run the API
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs
Health check: http://localhost:8000/health

Default seeded login (change immediately):
`admin@ssplatform.com` / `ChangeMe123!`

## Project layout

```
app/
  core/        config, database session, JWT/password security, auth deps
  models/      SQLAlchemy models, one file per domain (matches spec section 11)
  schemas/     Pydantic request/response schemas
  routers/     API endpoints, grouped by module
  seed.py      baseline data for local/dev bring-up
  main.py      FastAPI app + CORS + router registration
alembic/       migration environment (autogenerates from app/models)
```

## Design notes
- Every domain table from the spec's section 11 has a corresponding
  model, even where no API endpoint exists yet (e.g. `blogs`,
  `subscription_plans`) — this lets Alembic generate the complete
  schema now, with routers added incrementally without further
  migrations for new features that reuse these tables.
- `LeadStatus` enum matches the exact pipeline in section 8:
  `NEW → CONTACTED → QUALIFIED → PROPOSAL_SENT → NEGOTIATION → CONVERTED/CLOSED`.
- Analytics tracking uses a first-party `visitor_uuid`/`session_uuid`
  generated client-side (no third-party cookies), matching section 9.
- Payment models intentionally store only gateway references
  (`gateway_order_id`, `gateway_payment_id`) — never card/bank details,
  per section 7 and 15.
