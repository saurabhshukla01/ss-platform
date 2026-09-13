import { Link } from 'react-router-dom'
import { ArrowUpRight } from 'lucide-react'
import { trackEvent } from '../api/analytics'

export default function ServiceCard({ service }) {
  const priceLabel = service.is_custom_quote_only
    ? 'Custom quote'
    : service.starting_price
    ? `From ₹${Number(service.starting_price).toLocaleString('en-IN')}`
    : 'Contact for pricing'

  return (
    <Link
      to={`/services/${service.slug}`}
      onClick={() => trackEvent('service_view', undefined, { service_slug: service.slug })}
      className="group card-dark hover:border-electric transition-colors flex flex-col justify-between min-h-[190px]"
    >
      <div>
        <p className="text-xs text-muted2 mb-2">{service.category}</p>
        <h3 className="text-lg font-medium text-high group-hover:text-electric transition-colors">
          {service.name}
        </h3>
        <p className="text-sm text-muted mt-2 leading-relaxed">{service.short_description}</p>
      </div>
      <div className="flex items-center justify-between mt-6 pt-4 border-t border-line">
        <span className="text-sm text-cyan">{priceLabel}</span>
        <ArrowUpRight size={16} className="text-muted2 group-hover:text-electric transition-colors" />
      </div>
    </Link>
  )
}
