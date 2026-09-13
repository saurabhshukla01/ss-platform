import { useState } from 'react'
import Layout from '../components/Layout'
import { ShieldCheck } from 'lucide-react'

export default function Checkout() {
  const [status, setStatus] = useState('form') // form | processing | success
  const [form, setForm] = useState({ name: '', email: '', phone: '', coupon: '' })

  const subtotal = 30000
  const discount = form.coupon.trim() ? 3000 : 0
  const total = subtotal - discount

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  function handleSubmit(e) {
    e.preventDefault()
    setStatus('processing')
    // Gateway integration (Razorpay or similar) is wired on the backend Payments module.
    // This UI models the full flow: Customer Details -> Order Summary -> Gateway -> Result.
    setTimeout(() => setStatus('success'), 1200)
  }

  if (status === 'success') {
    return (
      <Layout>
        <section className="container-page py-24 text-center max-w-md mx-auto">
          <div className="w-12 h-12 rounded-full bg-cyan/20 text-cyan flex items-center justify-center mx-auto">
            <ShieldCheck size={22} />
          </div>
          <h1 className="text-2xl font-semibold text-high mt-6">Payment received</h1>
          <p className="text-muted mt-2">
            Your order is confirmed. An invoice has been generated and our team has
            been notified to begin onboarding.
          </p>
        </section>
      </Layout>
    )
  }

  return (
    <Layout>
      <section className="container-page pt-16 pb-24 grid md:grid-cols-3 gap-10">
        <form onSubmit={handleSubmit} className="md:col-span-2 space-y-6">
          <div>
            <p className="label-eyebrow mb-2">Checkout</p>
            <h1 className="text-3xl font-semibold text-high">Customer details</h1>
          </div>

          <div className="grid sm:grid-cols-2 gap-4">
            <Field label="Full name" name="name" value={form.name} onChange={handleChange} required />
            <Field label="Email" name="email" type="email" value={form.email} onChange={handleChange} required />
            <Field label="Phone" name="phone" value={form.phone} onChange={handleChange} required />
            <Field label="Coupon code" name="coupon" value={form.coupon} onChange={handleChange} />
          </div>

          <button type="submit" disabled={status === 'processing'} className="btn-primary w-full sm:w-auto">
            {status === 'processing' ? 'Processing…' : 'Proceed to payment'}
          </button>
          <p className="text-xs text-muted2">
            You'll be redirected to a secure payment gateway. Card and bank details
            are never stored on this platform.
          </p>
        </form>

        <aside className="card-dark h-fit">
          <p className="text-high font-medium">Order summary</p>
          <div className="mt-4 space-y-2 text-sm">
            <Row label="Business plan" value={`₹${subtotal.toLocaleString('en-IN')}`} />
            {discount > 0 && <Row label="Coupon discount" value={`− ₹${discount.toLocaleString('en-IN')}`} muted />}
            <div className="border-t border-line pt-2 flex justify-between font-medium text-high">
              <span>Total</span>
              <span>₹{total.toLocaleString('en-IN')}</span>
            </div>
          </div>
        </aside>
      </section>
    </Layout>
  )
}

function Field({ label, name, type = 'text', value, onChange, required }) {
  return (
    <label className="block">
      <span className="text-sm text-muted">{label}</span>
      <input
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        required={required}
        className="mt-1 w-full bg-surface2 border border-line rounded px-3 py-2.5 text-sm text-high focus:outline-none focus:border-electric"
      />
    </label>
  )
}

function Row({ label, value, muted }) {
  return (
    <div className={`flex justify-between ${muted ? 'text-cyan' : 'text-muted'}`}>
      <span>{label}</span>
      <span>{value}</span>
    </div>
  )
}
