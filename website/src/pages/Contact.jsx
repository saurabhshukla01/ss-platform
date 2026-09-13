import { useState } from 'react'
import Layout from '../components/Layout'
import { Mail, Phone, MessageCircle } from 'lucide-react'
import api from '../api/client'
import { trackEvent } from '../api/analytics'

export default function Contact() {
  const [form, setForm] = useState({ full_name: '', email: '', phone: '', message: '' })
  const [state, setState] = useState('idle') // idle | sending | sent | error

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setState('sending')
    try {
      await api.post('/inquiries', { ...form, preferred_contact_method: 'email', source: 'contact_page' })
      trackEvent('form_submit', '/contact')
      setState('sent')
    } catch {
      setState('error')
    }
  }

  return (
    <Layout>
      <section className="container-page pt-16 pb-24 grid md:grid-cols-2 gap-12">
        <div>
          <p className="label-eyebrow mb-3">Contact</p>
          <h1 className="text-4xl font-semibold text-high">Let's talk about your project.</h1>
          <p className="text-muted mt-4 leading-relaxed max-w-sm">
            Reach out directly, or use the form — every message is logged and
            followed up within 24 hours.
          </p>

          <div className="mt-10 space-y-4">
            <ContactLine icon={<Mail size={18} />} label="hello@ssplatform.com" href="mailto:hello@ssplatform.com" />
            <ContactLine icon={<Phone size={18} />} label="+91 00000 00000" href="tel:+910000000000" />
            <ContactLine icon={<MessageCircle size={18} />} label="Chat on WhatsApp" href="https://wa.me/910000000000" />
          </div>
        </div>

        <div className="card-dark">
          {state === 'sent' ? (
            <div className="py-8 text-center">
              <p className="text-high font-medium">Message sent.</p>
              <p className="text-muted text-sm mt-2">We'll get back to you within 24 hours.</p>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <Field label="Full name" name="full_name" value={form.full_name} onChange={handleChange} required />
              <Field label="Email" name="email" type="email" value={form.email} onChange={handleChange} required />
              <Field label="Phone" name="phone" value={form.phone} onChange={handleChange} />
              <label className="block">
                <span className="text-sm text-muted">Message</span>
                <textarea
                  name="message"
                  rows={4}
                  value={form.message}
                  onChange={handleChange}
                  required
                  className="mt-1 w-full bg-surface2 border border-line rounded px-3 py-2.5 text-sm text-high focus:outline-none focus:border-electric"
                />
              </label>
              <button type="submit" disabled={state === 'sending'} className="btn-primary w-full">
                {state === 'sending' ? 'Sending…' : 'Send message'}
              </button>
              {state === 'error' && (
                <p className="text-xs text-red-400">Something went wrong — please try again or email us directly.</p>
              )}
            </form>
          )}
        </div>
      </section>
    </Layout>
  )
}

function ContactLine({ icon, label, href }) {
  return (
    <a href={href} className="flex items-center gap-3 text-muted hover:text-electric transition-colors">
      <span className="text-electric">{icon}</span>
      {label}
    </a>
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
