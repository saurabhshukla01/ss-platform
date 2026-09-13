import { Link } from 'react-router-dom'
import { Check } from 'lucide-react'
import { trackEvent } from '../api/analytics'

export default function PricingCard({ plan }) {
  return (
    <div
      className={`card-dark flex flex-col ${
        plan.featured ? 'border-electric ring-1 ring-electric/40' : ''
      }`}
    >
      {plan.featured && (
        <p className="text-xs text-electric font-medium mb-3">Most chosen</p>
      )}
      <h3 className="text-xl font-medium text-high">{plan.name}</h3>
      <p className="mt-3">
        {plan.price ? (
          <>
            <span className="text-3xl font-display font-semibold text-high">₹{plan.price.toLocaleString('en-IN')}</span>
            <span className="text-muted text-sm">{plan.interval === 'one-time' ? ' one-time' : ` / ${plan.interval}`}</span>
          </>
        ) : (
          <span className="text-2xl font-display font-semibold text-high">Custom</span>
        )}
      </p>

      <ul className="mt-6 space-y-3 flex-1">
        {plan.features.map((f) => (
          <li key={f} className="flex items-start gap-2 text-sm text-muted">
            <Check size={16} className="text-cyan mt-0.5 shrink-0" />
            {f}
          </li>
        ))}
      </ul>

      <Link
        to={plan.price ? '/checkout' : '/inquiry'}
        onClick={() => trackEvent('pricing_view', undefined, { plan: plan.name })}
        className={`mt-6 text-center ${plan.featured ? 'btn-primary' : 'btn-secondary'}`}
      >
        {plan.price ? 'Choose plan' : 'Request custom quote'}
      </Link>
    </div>
  )
}
