import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { Check } from 'lucide-react'
import Layout from '../components/Layout'
import api from '../api/client'
import { services as fallbackServices, faqs } from '../data/placeholder'
import { trackEvent } from '../api/analytics'

export default function ServiceDetail() {
  const { slug } = useParams()
  const fallback = fallbackServices.find((s) => s.slug === slug)
  const [service, setService] = useState(fallback || null)
  const [notFound, setNotFound] = useState(false)

  useEffect(() => {
    trackEvent('service_view', undefined, { service_slug: slug })
    api.get(`/services/${slug}`).then((res) => setService(res.data)).catch(() => {
      if (!fallback) setNotFound(true)
    })
  }, [slug])

  if (notFound) {
    return (
      <Layout>
        <section className="container-page py-24 text-center">
          <p className="text-muted">This service isn't available.</p>
          <Link to="/services" className="btn-ghost mt-4 inline-block">Back to services</Link>
        </section>
      </Layout>
    )
  }

  if (!service) return <Layout><div className="container-page py-24 text-muted">Loading…</div></Layout>

  const priceLabel = service.is_custom_quote_only
    ? 'Custom quote'
    : service.starting_price
    ? `From ₹${Number(service.starting_price).toLocaleString('en-IN')}`
    : 'Contact for pricing'

  return (
    <Layout>
      <section className="container-page pt-16 pb-10 grid md:grid-cols-3 gap-10">
        <div className="md:col-span-2">
          <p className="label-eyebrow mb-3">{service.category?.name || service.category}</p>
          <h1 className="text-3xl md:text-4xl font-semibold text-high">{service.name}</h1>
          <p className="text-muted mt-4 leading-relaxed max-w-xl">
            {service.long_description || service.short_description}
          </p>

          {service.features?.length > 0 && (
            <div className="mt-10">
              <h2 className="text-lg font-medium text-high mb-4">What's included</h2>
              <ul className="grid sm:grid-cols-2 gap-3">
                {service.features.map((f) => (
                  <li key={f.id} className="flex items-start gap-2 text-sm text-muted">
                    <Check size={16} className="text-cyan mt-0.5 shrink-0" />
                    {f.title}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {service.technologies?.length > 0 && (
            <div className="mt-10">
              <h2 className="text-lg font-medium text-high mb-4">Technologies</h2>
              <div className="flex flex-wrap gap-2">
                {service.technologies.map((t) => (
                  <span key={t.id} className="text-sm border border-line rounded px-3 py-1.5 text-muted">{t.name}</span>
                ))}
              </div>
            </div>
          )}

          <div className="mt-10">
            <h2 className="text-lg font-medium text-high mb-4">Frequently asked</h2>
            <div className="divide-y divide-line border-t border-b border-line">
              {faqs.slice(0, 2).map((f) => (
                <details key={f.q} className="py-4">
                  <summary className="cursor-pointer text-high text-sm font-medium">{f.q}</summary>
                  <p className="text-muted text-sm mt-2 leading-relaxed">{f.a}</p>
                </details>
              ))}
            </div>
          </div>
        </div>

        <aside className="card-dark h-fit sticky top-24">
          <p className="text-xs text-muted2">Starting at</p>
          <p className="text-2xl font-display font-semibold text-high mt-1">{priceLabel}</p>

          {service.packages?.length > 0 && (
            <ul className="mt-4 space-y-2">
              {service.packages.map((p) => (
                <li key={p.id} className="flex justify-between text-sm border-t border-line pt-2">
                  <span className="text-muted">{p.name}</span>
                  <span className="text-high">{p.is_custom_quote ? 'Custom' : `₹${Number(p.price).toLocaleString('en-IN')}`}</span>
                </li>
              ))}
            </ul>
          )}

          <Link
            to="/inquiry"
            onClick={() => trackEvent('quote_click', undefined, { service_slug: service.slug })}
            className="btn-primary mt-6 w-full"
          >
            Get a quote
          </Link>
          <p className="text-xs text-muted2 mt-3 text-center">Response within 24 hours.</p>
        </aside>
      </section>
    </Layout>
  )
}
