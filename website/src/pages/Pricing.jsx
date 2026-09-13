import { useState } from 'react'
import Layout from '../components/Layout'
import PricingCard from '../components/PricingCard'
import { plans } from '../data/placeholder'

export default function Pricing() {
  const [billing, setBilling] = useState('monthly')

  return (
    <Layout>
      <section className="container-page pt-16 pb-10 text-center">
        <p className="label-eyebrow mb-3 justify-center flex">Pricing</p>
        <h1 className="text-4xl md:text-5xl font-semibold text-high">
          Packages that scale with the project.
        </h1>
        <p className="text-muted mt-4 max-w-xl mx-auto">
          One-time packages for fixed-scope builds, or recurring plans for
          ongoing hosting, maintenance and support.
        </p>

        <div className="inline-flex items-center gap-1 mt-8 border border-line rounded p-1">
          {['monthly', 'yearly'].map((b) => (
            <button
              key={b}
              onClick={() => setBilling(b)}
              className={`text-sm px-4 py-2 rounded capitalize transition-colors ${
                billing === b ? 'bg-electric text-ink' : 'text-muted'
              }`}
            >
              {b}
            </button>
          ))}
        </div>
        <p className="text-xs text-muted2 mt-2">
          {billing === 'yearly' ? 'Yearly billing applies to subscription/maintenance plans.' : 'Package prices below are one-time unless noted.'}
        </p>
      </section>

      <section className="container-page pb-16">
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {plans.map((p) => <PricingCard key={p.name} plan={p} />)}
        </div>
      </section>

      <section className="container-page pb-24">
        <div className="card-dark max-w-md">
          <p className="text-high font-medium">Have a coupon?</p>
          <div className="flex gap-2 mt-3">
            <input
              type="text"
              placeholder="Enter coupon code"
              className="flex-1 bg-surface2 border border-line rounded px-3 py-2 text-sm text-high placeholder:text-muted2 focus:outline-none focus:border-electric"
            />
            <button className="btn-secondary text-sm px-4">Apply</button>
          </div>
          <p className="text-xs text-muted2 mt-2">Coupons are validated at checkout.</p>
        </div>
      </section>
    </Layout>
  )
}
