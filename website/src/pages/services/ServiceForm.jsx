import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import AdminLayout from '../../components/AdminLayout'
import api from '../../api/client'

const emptyForm = {
  category_id: 1, name: '', slug: '', short_description: '', long_description: '',
  starting_price: '', is_custom_quote_only: false, meta_title: '', meta_description: '',
}

export default function ServiceForm() {
  const { id } = useParams()
  const isEdit = Boolean(id)
  const navigate = useNavigate()
  const [form, setForm] = useState(emptyForm)
  const [categories, setCategories] = useState([])
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    api.get('/categories/admin').then((res) => setCategories(res.data)).catch(() => {
      api.get('/categories').then((res) => setCategories(res.data)).catch(() => {})
    })
  }, [])

  useEffect(() => {
    if (!isEdit) return
    api.get('/services').then((res) => {
      const existing = res.data.find((s) => String(s.id) === id)
      if (existing) {
        setForm({
          category_id: existing.category?.id || 1,
          name: existing.name,
          slug: existing.slug,
          short_description: existing.short_description || '',
          long_description: '',
          starting_price: existing.starting_price || '',
          is_custom_quote_only: existing.is_custom_quote_only,
          meta_title: '', meta_description: '',
        })
      }
    })
  }, [id])

  function handleChange(e) {
    const { name, value, type, checked } = e.target
    setForm({ ...form, [name]: type === 'checkbox' ? checked : value })
  }

  function autoSlug(name) {
    return name.toLowerCase().trim().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '')
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setSaving(true)
    setError('')
    try {
      const payload = {
        ...form,
        category_id: Number(form.category_id),
        starting_price: form.starting_price ? Number(form.starting_price) : null,
      }
      if (isEdit) {
        delete payload.slug
        await api.put(`/services/admin/${id}`, payload)
      } else {
        await api.post('/services/admin', payload)
      }
      navigate('/services')
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not save service.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <AdminLayout title={isEdit ? 'Edit service' : 'New service'}>
      <form onSubmit={handleSubmit} className="panel p-6 max-w-2xl space-y-4">
        <div className="grid sm:grid-cols-2 gap-4">
          <div>
            <label className="label">Name</label>
            <input
              name="name" required className="input" value={form.name}
              onChange={(e) => {
                handleChange(e)
                if (!isEdit) setForm((f) => ({ ...f, name: e.target.value, slug: autoSlug(e.target.value) }))
              }}
            />
          </div>
          <div>
            <label className="label">Slug</label>
            <input name="slug" required disabled={isEdit} className="input disabled:opacity-60" value={form.slug} onChange={handleChange} />
          </div>
        </div>

        <div>
          <label className="label">Category</label>
          <select name="category_id" className="input" value={form.category_id} onChange={handleChange}>
            {categories.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
        </div>

        <div>
          <label className="label">Short description</label>
          <input name="short_description" className="input" value={form.short_description} onChange={handleChange} />
        </div>

        <div>
          <label className="label">Long description</label>
          <textarea name="long_description" rows={4} className="input" value={form.long_description} onChange={handleChange} />
        </div>

        <div className="grid sm:grid-cols-2 gap-4 items-end">
          <div>
            <label className="label">Starting price (₹)</label>
            <input
              type="number" name="starting_price" className="input disabled:opacity-50"
              value={form.starting_price} onChange={handleChange} disabled={form.is_custom_quote_only}
            />
          </div>
          <label className="flex items-center gap-2 text-sm text-muted pb-2.5">
            <input type="checkbox" name="is_custom_quote_only" checked={form.is_custom_quote_only} onChange={handleChange} />
            Custom quote only
          </label>
        </div>

        <div className="grid sm:grid-cols-2 gap-4">
          <div>
            <label className="label">Meta title (SEO)</label>
            <input name="meta_title" className="input" value={form.meta_title} onChange={handleChange} />
          </div>
          <div>
            <label className="label">Meta description (SEO)</label>
            <input name="meta_description" className="input" value={form.meta_description} onChange={handleChange} />
          </div>
        </div>

        {error && <p className="text-xs text-red-600">{error}</p>}

        <div className="flex gap-3 pt-2">
          <button type="submit" disabled={saving} className="btn-primary">
            {saving ? 'Saving…' : isEdit ? 'Save changes' : 'Create service'}
          </button>
          <button type="button" onClick={() => navigate('/services')} className="btn-secondary">Cancel</button>
        </div>
      </form>
    </AdminLayout>
  )
}
