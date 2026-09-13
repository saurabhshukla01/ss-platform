# Saurabh Shukla Technology Platform — Public Website

React + Vite + React Router + Axios + Tailwind CSS + Lucide Icons,
implementing the 8–10 page public website from the Business Growth
Blueprint (sections 3–5, 7, 10, 14, 17).

## Pages implemented

| Route | Purpose |
|---|---|
| `/` | Home — hero with live system-flow panel, services, why-us, projects, testimonials, FAQ preview, CTA |
| `/about` | Saurabh profile, CTO positioning, working approach, expertise |
| `/services` | Dynamic service catalogue with category filter (from API, falls back to placeholder data) |
| `/services/:slug` | Service detail — features, packages, technologies, FAQ, inquiry CTA |
| `/pricing` | Package cards, monthly/yearly toggle, coupon field |
| `/checkout` | Customer details → order summary → gateway → result (UI flow; gateway wiring is a backend task) |
| `/projects` | Live/completed project portfolio |
| `/contact` | Contact form (posts to `/inquiries`), email/phone/WhatsApp |
| `/inquiry` | Detailed "Get Quote" form — service, budget, timeline, message (posts to `/inquiries`) |
| `/faq` | FAQ + Privacy Policy + Terms & Conditions + tracking notice (anchors: `#privacy`, `#terms`) |

Sticky mobile action bar (WhatsApp / Call / Get Quote) and an animated
announcement bar appear site-wide, matching section 4.

## Backend integration

The site talks to the FastAPI backend built earlier:
- `GET /services`, `GET /services/{slug}` — service catalogue and detail
- `POST /inquiries` — Contact and Get Quote form submissions
- `POST /analytics/session`, `/page-view`, `/event` — first-party visitor
  tracking, fired automatically on every route change and on key actions
  (quote clicks, WhatsApp/call clicks, service views, pricing views, form
  submits) via `src/api/analytics.js`

If the API is unreachable, pages fall back to realistic placeholder
content (`src/data/placeholder.js`) so the site still renders fully —
useful for design review before the backend is deployed.

## Setup

```bash
cd frontend
npm install

cp .env.example .env
# set VITE_API_BASE_URL to your backend URL (defaults to http://localhost:8000/api/v1)

npm run dev       # http://localhost:5173
npm run build      # production build to dist/
```

## Design system

- **Color**: dark ink base (`#0A0E14`) with a single controlled electric-blue
  accent (`#3B82F6`) and cyan (`#22D3EE`) reserved for live-status and
  highlight moments; a light paper section (`#F4F6F9`) breaks up the page
  for the "why choose us" block.
- **Type**: Space Grotesk for headings, IBM Plex Sans for body text.
- **Components**: hairline-bordered, sharp-cornered cards (not soft-shadow
  rounded cards) — see `tailwind.config.js` tokens and `src/index.css`
  for the shared `.card-dark`, `.btn-primary` etc. utility classes.

## Not yet built
Admin Panel UI, real payment gateway integration (Checkout page models
the flow but needs Razorpay SDK wiring), blog pages, SEO sitemap
generation. The backend already has the tables/endpoints these will
sit on top of.
