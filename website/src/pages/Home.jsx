import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowUpRight, Globe, Server, Database } from 'lucide-react'
import Layout from '../components/Layout'
import SectionHeading from '../components/SectionHeading'
import ServiceCard from '../components/ServiceCard'
import api from '../api/client'
import { services as fallbackServices, projects, testimonials, faqs } from '../data/placeholder'
import { trackEvent } from '../api/analytics'

export default function Home() {
  const [services, setServices] = useState(fallbackServices.slice(0, 6))
  const [homeProjects, setHomeProjects] = useState(projects)
  const [homeTestimonials, setHomeTestimonials] = useState(testimonials)

  useEffect(() => {
    api.get('/services').then((res) => {
      if (res.data?.length) {
        setServices(
          res.data.slice(0, 6).map((s) => ({ ...s, category: s.category?.name }))
        )
      }
    }).catch(() => {})

    api.get('/website/projects').then((res) => {
      if (res.data?.length) setHomeProjects(res.data.slice(0, 3))
    }).catch(() => {})

    api.get('/website/testimonials').then((res) => {
      if (res.data?.length) {
        setHomeTestimonials(
          res.data.slice(0, 2).map((t) => ({ name: t.client_name, company: t.client_company, quote: t.quote }))
        )
      }
    }).catch(() => {})
  }, [])

  return (
    <Layout>
      {/* Hero */}
      <section className="container-page pt-16 md:pt-24 pb-20 grid md:grid-cols-2 gap-12 items-center">
        <div>
          <p className="label-eyebrow mb-4">Technology &amp; Digital Solutions</p>
          <h1 className="text-4xl md:text-5xl font-semibold leading-[1.1] text-high">
            Build. Automate. Grow.
          </h1>
          <p className="mt-6 text-lg text-muted leading-relaxed max-w-md">
            A single platform for websites, applications, hosting and business
            automation — designed, built and maintained by Saurabh Shukla for
            SS Collections Group and its clients.
          </p>
          <div className="mt-8 flex flex-wrap gap-4">
            <Link
              to="/inquiry"
              onClick={() => trackEvent('quote_click', '/')}
              className="btn-primary"
            >
              Start your project
            </Link>
            <Link to="/services" className="btn-secondary">
              View services
            </Link>
          </div>
          <div className="mt-10 flex gap-8 text-sm">
            <div>
              <p className="font-display text-2xl text-high">8+</p>
              <p className="text-muted2">Services offered</p>
            </div>
            <div>
              <p className="font-display text-2xl text-high">24h</p>
              <p className="text-muted2">Typical response time</p>
            </div>
            <div>
              <p className="font-display text-2xl text-high">100%</p>
              <p className="text-muted2">Admin-managed content</p>
            </div>
          </div>
        </div>

        {/* Live system flow panel */}
        <div className="card-dark bg-surface2 font-mono text-sm">
          <div className="flex items-center gap-2 pb-4 mb-4 border-b border-line">
            <span className="pulse-dot" />
            <span className="text-muted2">platform.status — live</span>
          </div>
          <div className="space-y-4">
            <FlowRow icon={<Globe size={16} />} label="Customer Website" detail="React + Vite" />
            <FlowConnector />
            <FlowRow icon={<Server size={16} />} label="REST API" detail="FastAPI · JWT auth" />
            <FlowConnector />
            <FlowRow icon={<Database size={16} />} label="MySQL Database" detail="Leads · Orders · Analytics" />
          </div>
          <div className="mt-6 pt-4 border-t border-line text-xs text-muted2">
            Admin Panel authenticates through the same API layer as the public website.
          </div>
        </div>
      </section>

      {/* Services */}
      <section className="container-page py-20 border-t border-line">
        <div className="flex items-end justify-between flex-wrap gap-4 mb-10">
          <SectionHeading
            eyebrow="What we build"
            title="Services for every stage of growth"
            description="Standard packages with transparent starting prices, or a custom quote for complex projects."
          />
          <Link to="/services" className="btn-ghost text-sm hidden md:inline-flex items-center gap-1">
            All services <ArrowUpRight size={14} />
          </Link>
        </div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {services.map((s) => <ServiceCard key={s.slug} service={s} />)}
        </div>
      </section>

      {/* Why choose us */}
      <section className="bg-paper text-ink py-20">
        <div className="container-page">
          <SectionHeading
            light
            eyebrow="Why choose us"
            title="Engineering discipline, business focus"
            description="Every project is built to be handed over cleanly — documented, secure and manageable without a developer on standby."
          />
          <div className="grid sm:grid-cols-3 gap-6 mt-10">
            {[
              { title: 'Engineering quality', body: 'Typed models, tested endpoints and a migration history you can audit.' },
              { title: 'Transparent pricing', body: 'Starting prices shown upfront; custom quotes only where genuinely needed.' },
              { title: 'Ongoing support', body: 'Hosting, maintenance and content updates available as recurring plans.' },
            ].map((item) => (
              <div key={item.title} className="card-light">
                <h3 className="font-medium text-ink">{item.title}</h3>
                <p className="text-sm text-muted2 mt-2 leading-relaxed">{item.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Projects */}
      <section className="container-page py-20">
        <SectionHeading eyebrow="Recent work" title="Projects in production" />
        <div className="grid md:grid-cols-3 gap-5 mt-10">
          {homeProjects.map((p) => (
            <div key={p.title} className="card-dark">
              <p className="text-xs text-cyan mb-2">{p.status === 'live' ? 'Live' : 'Completed'}</p>
              <h3 className="text-high font-medium">{p.title}</h3>
              <p className="text-sm text-muted mt-2">{p.summary}</p>
              <p className="text-xs text-muted2 mt-4 pt-4 border-t border-line">{p.tech_stack || p.stack}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Testimonials */}
      <section className="container-page py-20 border-t border-line grid md:grid-cols-2 gap-6">
        {homeTestimonials.map((t) => (
          <blockquote key={t.name} className="card-dark">
            <p className="text-high leading-relaxed">&ldquo;{t.quote}&rdquo;</p>
            <footer className="mt-4 text-sm text-muted2">{t.name} — {t.company}</footer>
          </blockquote>
        ))}
      </section>

      {/* FAQ preview */}
      <section className="container-page py-20 border-t border-line">
        <SectionHeading eyebrow="Questions" title="Frequently asked" />
        <div className="mt-8 divide-y divide-line border-t border-b border-line">
          {faqs.slice(0, 3).map((f) => (
            <details key={f.q} className="group py-4">
              <summary className="cursor-pointer text-high font-medium list-none flex justify-between items-center">
                {f.q}
                <span className="text-muted2 group-open:rotate-45 transition-transform">+</span>
              </summary>
              <p className="text-muted text-sm mt-3 leading-relaxed">{f.a}</p>
            </details>
          ))}
        </div>
        <Link to="/faq" className="btn-ghost text-sm mt-6 inline-block">See all questions</Link>
      </section>

      {/* Final CTA */}
      <section className="container-page pb-24">
        <div className="card-dark bg-surface2 border-electric/40 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 py-10">
          <div>
            <h2 className="text-2xl font-semibold text-high">Ready to start your project?</h2>
            <p className="text-muted mt-2">Tell us what you need — we'll reply with a plan and starting price.</p>
          </div>
          <Link to="/inquiry" onClick={() => trackEvent('quote_click', '/')} className="btn-primary shrink-0">
            Get free consultation
          </Link>
        </div>
      </section>
    </Layout>
  )
}

function FlowRow({ icon, label, detail }) {
  return (
    <div className="flex items-center gap-3">
      <span className="text-electric">{icon}</span>
      <div>
        <p className="text-high">{label}</p>
        <p className="text-muted2 text-xs">{detail}</p>
      </div>
    </div>
  )
}

function FlowConnector() {
  return <div className="ml-2 border-l border-dashed border-line h-4" />
}
