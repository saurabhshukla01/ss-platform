import Layout from '../components/Layout'
import { faqs } from '../data/placeholder'

export default function FAQLegal() {
  return (
    <Layout>
      <section className="container-page pt-16 pb-16">
        <p className="label-eyebrow mb-3">FAQ &amp; Legal</p>
        <h1 className="text-4xl font-semibold text-high">Questions, policies and terms.</h1>

        <div className="mt-10 divide-y divide-line border-t border-b border-line max-w-2xl">
          {faqs.map((f) => (
            <details key={f.q} className="py-4">
              <summary className="cursor-pointer text-high font-medium">{f.q}</summary>
              <p className="text-muted text-sm mt-2 leading-relaxed">{f.a}</p>
            </details>
          ))}
        </div>
      </section>

      <section id="privacy" className="container-page py-16 border-t border-line max-w-2xl">
        <h2 className="text-2xl font-semibold text-high">Privacy Policy</h2>
        <p className="text-muted text-sm mt-4 leading-relaxed">
          We collect the information you submit through inquiry and contact forms
          (name, email, phone, project details) to respond to your request and
          manage it in our CRM. We also collect first-party visitor analytics —
          session identifiers, pages viewed, device type and referral source — to
          understand which services and marketing sources perform best. We do not
          collect unnecessary sensitive data, and analytics identifiers are not
          tied to real-world identity unless you submit a form. Payment is handled
          by a licensed gateway; we never store card numbers, CVV or bank
          credentials on this platform.
        </p>
      </section>

      <section id="terms" className="container-page py-16 border-t border-line max-w-2xl">
        <h2 className="text-2xl font-semibold text-high">Terms &amp; Conditions</h2>
        <p className="text-muted text-sm mt-4 leading-relaxed">
          Package prices shown are starting prices and may vary based on final
          scope, confirmed after a requirements discussion. Custom-quote services
          are priced individually. Recurring plans (hosting, maintenance) renew
          automatically unless cancelled before the renewal date. We do not
          guarantee a specific search engine ranking position for any project.
        </p>
      </section>

      <section className="container-page py-16 border-t border-line max-w-2xl">
        <h2 className="text-2xl font-semibold text-high">Cookie &amp; Tracking Notice</h2>
        <p className="text-muted text-sm mt-4 leading-relaxed">
          This site uses first-party, cookie-less visitor and session identifiers
          stored in your browser's local storage to measure traffic sources and
          which pages and services get the most interest. This data is used only
          for our own analytics and is never sold to third parties.
        </p>
      </section>
    </Layout>
  )
}
