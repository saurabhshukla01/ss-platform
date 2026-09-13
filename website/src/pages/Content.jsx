import { useEffect, useState } from 'react'
import AdminLayout from '../components/AdminLayout'
import Tabs from '../components/Tabs'
import CrudManager from '../components/CrudManager'
import api from '../api/client'
import { Plus, Pencil, Trash2, X } from 'lucide-react'

const TABS = ['Blog Posts', 'Categories', 'FAQ']

export default function Content() {
  const [tab, setTab] = useState('Blog Posts')

  return (
    <AdminLayout title="Content">
      <Tabs tabs={TABS} active={tab} onChange={setTab} />
      {tab === 'Blog Posts' && <BlogManager />}
      {tab === 'Categories' && (
        <CrudManager
          base="/content/blog-categories"
          fields={[
            { name: 'name', label: 'Name', required: true },
            { name: 'slug', label: 'Slug', required: true },
          ]}
          columns={[{ key: 'name', label: 'Name' }, { key: 'slug', label: 'Slug' }]}
          emptyLabel="No blog categories yet."
        />
      )}
      {tab === 'FAQ' && (
        <CrudManager
          base="/content/faqs"
          fields={[
            { name: 'question', label: 'Question', required: true },
            { name: 'answer', label: 'Answer', type: 'textarea', required: true },
            { name: 'display_order', label: 'Display order', type: 'number' },
            { name: 'is_active', label: 'Active', type: 'checkbox' },
          ]}
          columns={[
            { key: 'question', label: 'Question' },
            { key: 'is_active', label: 'Active', render: (r) => (r.is_active ? 'Yes' : 'No') },
          ]}
          emptyLabel="No FAQ entries yet."
        />
      )}
    </AdminLayout>
  )
}

// Blogs use a dedicated manager because publishing sets published_at server-side
// and the slug is immutable after creation (matches /content/blogs/admin/* routes).
function BlogManager() {
  const [blogs, setBlogs] = useState([])
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState({})
  const [error, setError] = useState('')

  function load() {
    setLoading(true)
    api.get('/content/blogs/admin/all').then((res) => setBlogs(res.data)).finally(() => setLoading(false))
  }
  useEffect(load, [])

  function autoSlug(title) {
    return title.toLowerCase().trim().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '')
  }

  function startNew() {
    setForm({ title: '', slug: '', excerpt: '', content: '', is_published: false })
    setEditing('new')
    setError('')
  }

  function startEdit(blog) {
    setForm({ title: blog.title, slug: blog.slug, excerpt: blog.excerpt || '', content: '', is_published: blog.is_published })
    setEditing(blog)
    setError('')
  }

  function handleChange(e) {
    const { name, value, type, checked } = e.target
    setForm((f) => ({ ...f, [name]: type === 'checkbox' ? checked : value, ...(name === 'title' && editing === 'new' ? { slug: autoSlug(value) } : {}) }))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    try {
      if (editing === 'new') {
        await api.post('/content/blogs/admin', form)
      } else {
        const { slug, ...rest } = form
        await api.put(`/content/blogs/admin/${editing.id}`, rest)
      }
      setEditing(null)
      load()
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not save post.')
    }
  }

  async function handleDelete(blog) {
    if (!window.confirm('Delete this post?')) return
    await api.delete(`/content/blogs/admin/${blog.id}`)
    load()
  }

  return (
    <div>
      <div className="flex justify-end mb-3">
        <button onClick={startNew} className="btn-primary"><Plus size={15} /> New post</button>
      </div>

      {editing && (
        <form onSubmit={handleSubmit} className="panel p-5 mb-4 space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium text-ink2">{editing === 'new' ? 'New post' : 'Edit post'}</h3>
            <button type="button" onClick={() => setEditing(null)} className="text-muted hover:text-ink2"><X size={16} /></button>
          </div>
          <div className="grid sm:grid-cols-2 gap-3">
            <div>
              <label className="label">Title</label>
              <input name="title" className="input" value={form.title} onChange={handleChange} required />
            </div>
            <div>
              <label className="label">Slug</label>
              <input name="slug" className="input disabled:opacity-60" disabled={editing !== 'new'} value={form.slug} onChange={handleChange} required />
            </div>
          </div>
          <div>
            <label className="label">Excerpt</label>
            <input name="excerpt" className="input" value={form.excerpt} onChange={handleChange} />
          </div>
          <div>
            <label className="label">Content</label>
            <textarea name="content" rows={6} className="input" value={form.content} onChange={handleChange} />
          </div>
          <label className="flex items-center gap-2 text-sm text-muted">
            <input type="checkbox" name="is_published" checked={form.is_published} onChange={handleChange} />
            Published
          </label>
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
            <tr><th className="th">Title</th><th className="th">Published</th><th className="th"></th></tr>
          </thead>
          <tbody>
            {!loading && blogs.length === 0 && (
              <tr><td colSpan={3} className="td text-center text-muted2 py-10">No blog posts yet.</td></tr>
            )}
            {blogs.map((b) => (
              <tr key={b.id} className="hover:bg-canvas/60">
                <td className="td">{b.title}</td>
                <td className="td">{b.is_published ? 'Yes' : 'Draft'}</td>
                <td className="td text-right whitespace-nowrap">
                  <button onClick={() => startEdit(b)} className="btn-ghost mr-3"><Pencil size={13} /></button>
                  <button onClick={() => handleDelete(b)} className="text-red-600 hover:text-red-700 text-sm inline-flex items-center gap-1"><Trash2 size={13} /></button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
