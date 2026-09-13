export const categories = [
  { name: 'Digital Products', slug: 'digital-products', desc: 'Website Development, E-Commerce, Admin Panel, REST API' },
  { name: 'Applications', slug: 'applications', desc: 'Mobile Application, Custom Software, CRM, HRMS, ERP' },
  { name: 'Infrastructure', slug: 'infrastructure', desc: 'Hosting, Deployment, SSL, DNS, Cloud, Maintenance' },
  { name: 'Business Solutions', slug: 'business-solutions', desc: 'Automation, Integration, Reporting, Custom Platforms' },
]

export const services = [
  { id: 1, slug: 'website-development', name: 'Website Development', category: 'Digital Products', short_description: 'Fast, responsive websites built on React and FastAPI, managed entirely from your Admin Panel.', starting_price: 15000, is_custom_quote_only: false },
  { id: 2, slug: 'e-commerce', name: 'E-Commerce', category: 'Digital Products', short_description: 'Full storefronts with catalogue, checkout and order management built in.', starting_price: 35000, is_custom_quote_only: false },
  { id: 3, slug: 'admin-panel', name: 'Admin Panel', category: 'Digital Products', short_description: 'A secure command center to manage services, content, leads and payments.', starting_price: 20000, is_custom_quote_only: false },
  { id: 4, slug: 'rest-api', name: 'REST API', category: 'Digital Products', short_description: 'FastAPI backends with JWT auth, documented endpoints and MySQL storage.', starting_price: 18000, is_custom_quote_only: false },
  { id: 5, slug: 'mobile-application', name: 'Mobile Application', category: 'Applications', short_description: 'Customer and business apps that connect to the same API as your website.', starting_price: null, is_custom_quote_only: true },
  { id: 6, slug: 'crm', name: 'CRM', category: 'Applications', short_description: 'Track inquiries, leads and customers through a defined sales pipeline.', starting_price: 25000, is_custom_quote_only: false },
  { id: 7, slug: 'hosting-deployment', name: 'Hosting & Deployment', category: 'Infrastructure', short_description: 'VPS or cloud hosting with SSL, DNS and Nginx configured and maintained.', starting_price: 5000, is_custom_quote_only: false },
  { id: 8, slug: 'automation-integration', name: 'Automation & Integration', category: 'Business Solutions', short_description: 'Connect your tools and automate repetitive business workflows.', starting_price: null, is_custom_quote_only: true },
]

export const plans = [
  { name: 'Starter', price: 15000, interval: 'one-time', features: ['5 pages', 'Responsive UI', 'Contact form', 'Basic SEO', 'Deployment'] },
  { name: 'Business', price: 30000, interval: 'one-time', features: ['10 pages', 'Admin panel', 'Database', 'Dynamic content', 'API integration'], featured: true },
  { name: 'Professional', price: 50000, interval: 'one-time', features: ['Custom application', 'API', 'Payment integration', 'Advanced admin', 'Deployment'] },
  { name: 'Enterprise', price: null, interval: 'custom', features: ['Architecture & integrations', 'Mobile app', 'Automation', 'Dedicated support'] },
]

export const projects = [
  { title: 'SS Collections — Catalogue Platform', summary: 'A dynamic product catalogue with an admin-managed pricing engine.', stack: 'React, FastAPI, MySQL', status: 'live' },
  { title: 'Client CRM Rollout', summary: 'Lead pipeline and follow-up tracking replacing spreadsheet workflows.', stack: 'React, FastAPI, JWT', status: 'completed' },
  { title: 'Hosting & Maintenance Program', summary: 'Managed hosting, SSL renewal and uptime monitoring for six client sites.', stack: 'Nginx, Linux, Cloudflare', status: 'live' },
]

export const testimonials = [
  { name: 'Retail client', company: 'SS Collections Group', quote: 'The admin panel means we update prices and offers ourselves — no waiting on a developer.' },
  { name: 'Service business owner', company: 'Local business', quote: 'Inquiries now land directly in a pipeline instead of getting lost in email.' },
]

export const faqs = [
  { q: 'How is pricing determined?', a: 'Standard packages have transparent starting prices. Complex or custom projects receive a formal quote after a short requirements call.' },
  { q: 'Do you offer ongoing maintenance?', a: 'Yes — hosting, SSL renewal, backups and content updates are available as monthly or yearly plans.' },
  { q: 'What technologies do you use?', a: 'React on the frontend, FastAPI and MySQL on the backend, deployed on Linux/cloud infrastructure with HTTPS.' },
  { q: 'How long does a typical project take?', a: 'A Starter site typically takes 2–3 weeks; Business and Professional builds run 4–8 weeks depending on scope.' },
]
