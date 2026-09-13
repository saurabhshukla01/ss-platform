import { useEffect, useState } from 'react'
import { Plus, Pencil, Trash2, X } from 'lucide-react'
import api from '../api/client'

/**
 * Generic manager for the backend's simple_crud_router convention:
 *   GET    {base}/admin
 *   POST   {base}/admin
 *   PUT    {base}/admin/{id}
 *   DELETE {base}/admin/{id}
 *
 * fields: [{ name, label, type: 'text'|'number'|'textarea'|'checkbox', required }]
 * columns: [{ key, label, render?(row) }]
 */
export default function CrudManager({ base, fields, columns, emptyLabel = 'No items yet.' }) {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(null) // null | 'new' | item
  const [form, setForm] = useState({})
  const [error, setError] = useState('')

  function defaultForm() {
    const f = {}
    fields.forEach((fld) => { f[fld.name] = fld.type === 'checkbox' ? false : '' })
    return f
  }

  function load() {
    setLoading(true)
    api.get(`${base}/admin`).then((res) => setItems(res.data)).finally(() => setLoading(false))
  }

  useEffect(load, [base])

  function startNew() {
    setForm(defaultForm())
    setEditing('new')
    setError('')
  }

  function startEdit(item) {
    const f = {}
    fields.forEach((fld) => { f[fld.name] = item[fld.name] ?? (fld.type === 'checkbox' ? false : '') })
    setForm(f)
    setEditing(item)
    setError('')
  }

  function handleChange(e) {
    const { name, value, type, checked } = e.target
    setForm({ ...form, [name]: type === 'checkbox' ? checked : value })
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    const payload = {}
    fields.forEach((fld) => {
      let v = form[fld.name]
      if (fld.type === 'number' && v !== '') v = Number(v)
      if (fld.type === 'number' && v === '') v = null
      payload[fld.name] = v
    })
    try {
      if (editing === 'new') {
        await api.post(`${base}/admin`, payload)
      } else {
        await api.put(`${base}/admin/${editing.id}`, payload)
      }
      setEditing(null)
      load()
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not save.')
    }
  }

  async function handleDelete(item) {
    if (!window.confirm('Delete this item?')) return
    await api.delete(`${base}/admin/${item.id}`)
    load()
  }

  return (
    <div>
      <div className="flex justify-end mb-3">
        <button onClick={startNew} className="btn-primary"><Plus size={15} /> Add</button>
      </div>

      {editing && (
        <form onSubmit={handleSubmit} className="panel p-5 mb-4 space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium text-ink2">{editing === 'new' ? 'New item' : 'Edit item'}</h3>
            <button type="button" onClick={() => setEditing(null)} className="text-muted hover:text-ink2"><X size={16} /></button>
          </div>
          <div className="grid sm:grid-cols-2 gap-3">
            {fields.map((fld) => (
              <div key={fld.name} className={fld.type === 'textarea' ? 'sm:col-span-2' : ''}>
                <label className="label">{fld.label}</label>
                {fld.type === 'textarea' ? (
                  <textarea name={fld.name} rows={3} className="input" value={form[fld.name] || ''} onChange={handleChange} required={fld.required} />
                ) : fld.type === 'checkbox' ? (
                  <input type="checkbox" name={fld.name} checked={!!form[fld.name]} onChange={handleChange} className="mt-1" />
                ) : (
                  <input
                    type={fld.type || 'text'} name={fld.name} className="input"
                    value={form[fld.name] ?? ''} onChange={handleChange} required={fld.required}
                  />
                )}
              </div>
            ))}
          </div>
          {error && <p className="text-xs text-red-600">{error}</p>}
          <div className="flex gap-2">
            <button type="submit" className="btn-primary">Save</button>
            <button type="button" onClick={() => setEditing(null)} className="btn-secondary">Cancel</button>
          </div>
        </form>
      )}

      <div className="panel overflow-hidden">
        <table className="w-full">
          <thead>
            <tr>
              {columns.map((c) => <th key={c.key} className="th">{c.label}</th>)}
              <th className="th"></th>
            </tr>
          </thead>
          <tbody>
            {!loading && items.length === 0 && (
              <tr><td colSpan={columns.length + 1} className="td text-center text-muted2 py-10">{emptyLabel}</td></tr>
            )}
            {items.map((item) => (
              <tr key={item.id} className="hover:bg-canvas/60">
                {columns.map((c) => (
                  <td key={c.key} className="td">{c.render ? c.render(item) : String(item[c.key] ?? '—')}</td>
                ))}
                <td className="td text-right whitespace-nowrap">
                  <button onClick={() => startEdit(item)} className="btn-ghost mr-3"><Pencil size={13} /></button>
                  <button onClick={() => handleDelete(item)} className="text-red-600 hover:text-red-700 text-sm inline-flex items-center gap-1">
                    <Trash2 size={13} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
