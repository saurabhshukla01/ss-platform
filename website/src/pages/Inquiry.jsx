import { useState } from 'react'
import Layout from '../components/Layout'
import api from '../api/client'
import { services } from '../data/placeholder'
import { trackEvent } from '../api/analytics'

const budgets = ['Under ₹20,000', '₹20,000 – ₹50,000', '₹50,000 – ₹1,00,000', 'Above ₹1,00,000', 'Not sure yet']
const timelines = ['ASAP', 'Within 1 month', '1–3 months', 'Flexible']

export default function Inquiry() {
  const [form, setForm] = useState({
    full_name: '', email: '', phone: '', service_id: '',
    budget_range: '', timeline: '', preferred_contact_method: 'email', message: '',
  })
  const [state, setState] = useState('idle')

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setState('sending')
    try {
      await api.post('/inquiries', {
        ...form,
        service_id: form.service_id ? Number(form.service_id) : null,
        source: 'inquiry_page',
      })
      trackEvent('form_submit', '/inquiry')
      setState('sent')
    } catch {
      setState('error')
    }
  }

  if (state === 'sent') {
    return (
      <Layout>
        <section className="container-page py-24 text-center max-w-md mx-auto">
          <h1 className="text-2xl font-semibold text-high">Request received.</h1>
          <p className="text-muted mt-2">
            Your inquiry has entered our pipeline — expect a reply with next steps
            within 24 hours.
          </p>
        </section>
      </Layout>
    )
  }

  return (
    <Layout>
      <section className="container-page pt-16 pb-6">
        <p className="label-eyebrow mb-3">Get a quote</p>
        <h1 className="text-4xl font-semibold text-high max-w-xl">
          Tell us about the project.
        </h1>
        <p className="text-muted mt-3 max-w-xl">
          The more detail you give, the more accurate your quote will be.
        </p>
      </section>

      <section className="container-page pb-24">
        <form onSubmit={handleSubmit} className="card-dark max-w-2xl space-y-5">
          <div className="grid sm:grid-cols-2 gap-4">
            <Field label="Full name" name="full_name" value={form.full_name} onChange={handleChange} required />
            <Field label="Email" name="email" type="email" value={form.email} onChange={handleChange} required />
            <Field label="Phone" name="phone" value={form.phone} onChange={handleChange} />
            <Select label="Preferred contact" name="preferred_contact_method" value={form.preferred_contact_method} onChange={handleChange}
              options={[['email', 'Email'], ['phone', 'Phone'], ['whatsapp', 'WhatsApp']]} />
          </div>

          <Select label="Service" name="service_id" value={form.service_id} onChange={handleChange}
            options={[['', 'Select a service'], ...services.map((s) => [s.id, s.name])]} />

          <div className="grid sm:grid-cols-2 gap-4">
            <Select label="Budget" name="budget_range" value={form.budget_range} onChange={handleChange}
              options={[['', 'Select a range'], ...budgets.map((b) => [b, b])]} />
            <Select label="Timeline" name="timeline" value={form.timeline} onChange={handleChange}
              options={[['', 'Select a timeline'], ...timelines.map((t) => [t, t])]} />
          </div>

          <label className="block">
            <span className="text-sm text-muted">Project details</span>
            <textarea
              name="message"
              rows={5}
              value={form.message}
              onChange={handleChange}
              required
              placeholder="What are you trying to build, and what problem should it solve?"
              className="mt-1 w-full bg-surface2 border border-line rounded px-3 py-2.5 text-sm text-high placeholder:text-muted2 focus:outline-none focus:border-electric"
            />
          </label>

          <button type="submit" disabled={state === 'sending'} className="btn-primary w-full sm:w-auto">
            {state === 'sending' ? 'Submitting…' : 'Submit inquiry'}
          </button>
          {state === 'error' && (
            <p className="text-xs text-red-400">Something went wrong — please try again or email us directly.</p>
          )}
        </form>
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

function Select({ label, name, value, onChange, options }) {
  return (
    <label className="block">
      <span className="text-sm text-muted">{label}</span>
      <select
        name={name}
        value={value}
        onChange={onChange}
        className="mt-1 w-full bg-surface2 border border-line rounded px-3 py-2.5 text-sm text-high focus:outline-none focus:border-electric"
      >
        {options.map(([val, text]) => <option key={val} value={val}>{text}</option>)}
      </select>
    </label>
  )
}
