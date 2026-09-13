import { useEffect, useState } from 'react'
import api from '../api/client'

const FIELDS = [
  { name: 'site_name', label: 'Site name', type: 'text' },
  { name: 'tagline', label: 'Tagline', type: 'text' },
  { name: 'primary_color', label: 'Primary color (buttons, links)', type: 'color' },
  { name: 'primary_dark_color', label: 'Primary hover color', type: 'color' },
  { name: 'accent_color', label: 'Accent color (highlights)', type: 'color' },
]

/**
 * Lets an admin edit the site-wide branding (name, tagline, colors) that
 * powers the public website's theme. Reads/writes GET & PUT /settings/theme.
 * The public site picks up saved changes on next load via ThemeProvider.
 */
export default function BrandingPanel() {
  const [form, setForm] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    api.get('/settings/theme')
      .then((res) => setForm(res.data))
      .catch(() => setError('Could not load theme settings.'))
      .finally(() => setLoading(false))
  }, [])

  function handleChange(e) {
    const { name, value } = e.target
    setForm({ ...form, [name]: value })
    setMessage('')
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setSaving(true)
    setError('')
    setMessage('')
    try {
      const res = await api.put('/settings/theme', form)
      setForm(res.data)
      setMessage('Saved — changes appear on the public site on next page load.')
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not save theme settings.')
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <p className="text-muted2 text-sm py-6">Loading theme settings…</p>
  if (!form) return <p className="text-red-600 text-sm py-6">{error || 'Could not load theme settings.'}</p>

  return (
    <form onSubmit={handleSubmit} className="panel p-5 max-w-xl space-y-4">
      <div>
        <h3 className="text-sm font-medium text-ink2">Default site branding</h3>
        <p className="text-xs text-muted2 mt-1">
          Controls the colors and name used across the public website (buttons, links,
          highlights) and the browser tab title.
        </p>
      </div>

      {FIELDS.map((fld) => (
        <div key={fld.name} className="flex items-center gap-3">
          <label className="label w-56 shrink-0">{fld.label}</label>
          {fld.type === 'color' ? (
            <div className="flex items-center gap-2">
              <input
                type="color"
                name={fld.name}
                value={form[fld.name] || '#000000'}
                onChange={handleChange}
                className="h-9 w-14 rounded border border-line cursor-pointer bg-transparent"
              />
              <span className="text-xs text-muted2 font-mono">{form[fld.name]}</span>
            </div>
          ) : (
            <input
              type="text"
              name={fld.name}
              className="input"
              value={form[fld.name] || ''}
              onChange={handleChange}
            />
          )}
        </div>
      ))}

      {error && <p className="text-xs text-red-600">{error}</p>}
      {message && <p className="text-xs text-green-600">{message}</p>}

      <div className="flex gap-2 pt-2">
        <button type="submit" disabled={saving} className="btn-primary">
          {saving ? 'Saving…' : 'Save branding'}
        </button>
      </div>
    </form>
  )
}
