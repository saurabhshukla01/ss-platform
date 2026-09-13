# SS Platform

A single system with two parts that work together:

- **`backend/`** — FastAPI + MySQL REST API (auth, services, CRM,
  website content, theme/branding settings, analytics)
- **`website/`** — React + Vite app serving both the **public
  website** and the **Admin Panel** that manages it

## Quick start

Set up the backend first, then the website — each has its own
step-by-step README:

1. **[backend/README.md](backend/README.md)** — install, configure
   `.env`, create the MySQL database, run migrations, seed data, start
   the API.
2. **[website/README.md](website/README.md)** — install, configure
   `.env`, start the dev server.

Once both are running:

| | URL |
|---|---|
| Public website | http://localhost:5173 |
| Admin Panel | http://localhost:5173/admin |
| API docs (Swagger) | http://127.0.0.1:8000/docs |

Default admin login (seeded by the backend — change after first login):

```
Email:    admin@ssplatform.com
Password: ChangeMe123!
```

## How it fits together

The website's public pages (Home, Services, Pricing, Projects, About,
etc.) fetch their content from the API — services, projects, team,
testimonials, announcements, and the site's theme colors are all
editable from the Admin Panel under **Website** and reflect on the
public site on the next page load. If the API is unreachable, the
public pages fall back to built-in placeholder content so the site
never looks broken.
