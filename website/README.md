# SS Platform — Website (Public Site + Admin Panel)

A single React app that serves **both**:

- the **public website** (`/`, `/about`, `/services`, `/pricing`,
  `/projects`, `/contact`, `/inquiry`, `/checkout`, `/faq`) — content
  managed from the admin panel, with sensible fallback content if the
  API is unreachable
- the **Admin Panel** (everything under `/admin/*`) — dashboard, CRM,
  services, website content, branding/theme colors, settings, etc.

Built with React + Vite + React Router + Axios + Tailwind CSS + Lucide
Icons.

> The backend (FastAPI) must be running before most of this app will
> show real data. Set that up first — see `../backend/README.md`.

---

## 1. Prerequisites

| Tool | Version | Check with |
|---|---|---|
| Node.js | 18+ (20+ recommended) | `node -v` |
| npm | 9+ | `npm -v` |

---

## 2. Install dependencies

```bash
cd ss-platform-main/website
npm install
```

---

## 3. Configure environment variables

Copy the example file to `.env`:

```bash
# macOS / Linux
cp ".env example" .env

# Windows (cmd)
copy ".env example" .env
```

Open `.env` and confirm/edit:

```ini
# Must point at your running backend (see backend/README.md)
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1

# Optional local-only login fallback if the API login fails
# (leave false/blank for normal use — real login goes through the API)
VITE_ENABLE_STATIC_ADMIN=false
VITE_STATIC_ADMIN_EMAIL=
VITE_STATIC_ADMIN_PASSWORD=
```

If your backend is running on a different host/port, update
`VITE_API_BASE_URL` to match — and make sure that same origin is listed
in the backend's `CORS_ORIGINS` (see `backend/README.md` step 6).

---

## 4. Start the backend first

In a separate terminal:

```bash
cd ../backend
source venv/bin/activate
uvicorn app.main:app --reload
```

Full instructions: `backend/README.md`. Confirm it's up by visiting
http://127.0.0.1:8000/health before continuing.

---

## 5. Run the website in development mode

Back in the `website` folder:

```bash
npm run dev
```

Vite will print a local URL, normally:

```
http://localhost:5173
```

Open that in your browser.

---

## 6. What you should see

- **`http://localhost:5173/`** — the public homepage: hero, services
  pulled from the API, "why choose us", projects, testimonials, FAQ
  preview, call to action. Colors here come from the admin-managed
  theme (see step 8).
- **`http://localhost:5173/services`**, **`/pricing`**, **`/about`**,
  **`/projects`**, **`/contact`**, **`/faq`** — the rest of the public
  site.
- **`http://localhost:5173/login`** — Admin Panel login. Use the
  seeded credentials from the backend setup:
  - Email: `admin@ssplatform.com`
  - Password: `ChangeMe123!`
- After logging in you land on **`/admin`** — the Admin Panel
  dashboard, with CRM, Services, Website, Content, SEO, Communication,
  Settings and Audit Logs in the sidebar.

If a public page looks empty or shows placeholder-looking content
instead of your real data, the backend probably hasn't been seeded yet
— run `python -m app.seed` in the backend (see its README, step 8) and
refresh.

---

## 7. Try the Admin Panel → public site loop end-to-end

This confirms everything is wired correctly:

1. Log in at `/login`.
2. Go to **Website → Services** (`/admin/services`) — add or edit a
   service.
3. Open `/services` in another tab — your change appears (services are
   fetched live from the API).
4. Go to **Website → Banners / Announcements / Projects / Team /
   Testimonials** (`/admin/website`) and add an item in any tab.
5. Refresh the relevant public page (home, `/projects`, `/about`) —
   your content appears there too.

---

## 8. Manage the site's default theme (colors)

1. Log in and go to **Website → Branding** (`/admin/website`, first
   tab).
2. Change **Primary color**, **Primary hover color**, **Accent
   color**, **Site name** or **Tagline**.
3. Click **Save branding**.
4. Refresh any public page — buttons, links and highlights across the
   whole site now use your chosen colors. (Colors are applied once on
   page load via CSS variables, so a refresh is needed to see a change
   made in another tab.)

---

## 9. Build for production

```bash
npm run build
```

Output goes to `dist/`. Preview the production build locally with:

```bash
npm run preview
```

Deploy the contents of `dist/` to any static host (Nginx, Vercel,
Netlify, S3 + CloudFront, etc.), and make sure `VITE_API_BASE_URL` was
set correctly **before** running `npm run build` (Vite bakes env vars
into the build — changing `.env` afterwards requires a rebuild).

---

## Route map

| Path | Page | Notes |
|---|---|---|
| `/` | Home | public |
| `/about` | About | public, shows admin-managed team |
| `/services` | Services list | public, filterable by category |
| `/services/:slug` | Service detail | public |
| `/pricing` | Pricing | public |
| `/projects` | Projects | public |
| `/contact` | Contact form | public, posts to `/inquiries` |
| `/inquiry` | Get a quote form | public, posts to `/inquiries` |
| `/checkout` | Checkout flow (UI only) | public |
| `/faq` | FAQ / Privacy / Terms | public |
| `/login` | Admin login | — |
| `/admin` | Dashboard | protected |
| `/admin/analytics` | Analytics | protected |
| `/admin/crm`, `/admin/crm/inquiries`, `/admin/crm/leads/:id` | CRM | protected |
| `/admin/services`, `/admin/services/new`, `/admin/services/:id/edit` | Services admin | protected |
| `/admin/subscriptions` | Subscriptions | protected |
| `/admin/payments` | Payments | protected |
| `/admin/website` | Branding / Banners / Announcements / Offers / Projects / Team / Testimonials | protected |
| `/admin/content` | Content | protected |
| `/admin/seo` | SEO | protected |
| `/admin/communication` | Communication | protected |
| `/admin/settings` | Settings | protected |
| `/admin/audit-logs` | Audit logs | protected |

"protected" routes require login and redirect to `/login` otherwise.

---

## Project layout

```
src/
  api/
    client.js       axios instance, JWT attach, base URL from VITE_API_BASE_URL
    analytics.js     first-party visitor/session/event tracking helpers
  auth/
    AuthContext.jsx  login/logout/session state
  theme/
    ThemeProvider.jsx  fetches /settings/theme, applies colors as CSS variables
  components/        shared UI: Layout, Navbar, Footer, AdminLayout, CrudManager,
                      BrandingPanel, ServiceCard, StatCard, Tabs, etc.
  pages/             one file per route (public pages at top level,
                      admin pages + pages/crm/, pages/services/ subfolders)
  data/
    placeholder.js   fallback content shown if the API is unreachable
  App.jsx            all route definitions
  main.jsx           app entry point (BrowserRouter, ThemeProvider, AuthProvider)
  index.css          Tailwind entry + shared utility classes + theme CSS variables
tailwind.config.js   design tokens (colors read from CSS variables — see ThemeProvider)
vite.config.js
.env example         copy this to .env (step 3)
```

---

## Troubleshooting

**Public pages load but show placeholder/fallback content**
The backend isn't running, isn't reachable at `VITE_API_BASE_URL`, or
hasn't been seeded. Check `backend/README.md` steps 8–10.

**Network error / CORS error in the browser console**
The backend's `CORS_ORIGINS` doesn't include `http://localhost:5173`
(or wherever this app is running). Fix it in the backend's `.env` and
restart `uvicorn`.

**Login fails with a network error, not "invalid credentials"**
The backend isn't running, or `VITE_API_BASE_URL` in `.env` is wrong.

**Changes to `.env` don't seem to apply**
Restart `npm run dev` after editing `.env` — Vite only reads it on
startup.

**Branding color change doesn't show up**
Reload the tab you're checking — colors are applied once when the app
loads, not live across open tabs.
