import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Plus, Pencil } from 'lucide-react'
import AdminLayout from '../../components/AdminLayout'
import Tabs from '../../components/Tabs'
import CrudManager from '../../components/CrudManager'
import api from '../../api/client'

const TABS = ['Services', 'Categories']

export default function ServicesList() {
  const [tab, setTab] = useState('Services')
  const [services, setServices] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (tab !== 'Services') return
    setLoading(true)
    api.get('/services').then((res) => setServices(res.data)).finally(() => setLoading(false))
  }, [tab])

  return (
    <AdminLayout title="Services">
      <Tabs tabs={TABS} active={tab} onChange={setTab} />

      {tab === 'Services' && (
        <>
          <div className="flex justify-end mb-4">
            <Link to="/admin/services/new" className="btn-primary"><Plus size={16} /> New service</Link>
          </div>

          <div className="panel overflow-hidden">
            <table className="w-full">
              <thead>
                <tr>
                  <th className="th">Name</th>
                  <th className="th">Category</th>
                  <th className="th">Starting price</th>
                  <th className="th">Status</th>
                  <th className="th"></th>
                </tr>
              </thead>
              <tbody>
                {!loading && services.length === 0 && (
                  <tr><td colSpan={5} className="td text-center text-muted2 py-10">No services yet — add your first one.</td></tr>
                )}
                {services.map((s) => (
                  <tr key={s.id} className="hover:bg-canvas/60">
                    <td className="td font-medium">{s.name}</td>
                    <td className="td text-muted">{s.category?.name}</td>
                    <td className="td text-muted">
                      {s.is_custom_quote_only ? 'Custom quote' : s.starting_price ? `₹${Number(s.starting_price).toLocaleString('en-IN')}` : '—'}
                    </td>
                    <td className="td">
                      <span className="badge bg-status-converted/10 text-status-converted">Active</span>
                    </td>
                    <td className="td text-right">
                      <Link to={`/admin/services/${s.id}/edit`} className="btn-ghost"><Pencil size={13} /> Edit</Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      {tab === 'Categories' && (
        <CrudManager
          base="/categories"
          fields={[
            { name: 'name', label: 'Name', required: true },
            { name: 'slug', label: 'Slug', required: true },
            { name: 'description', label: 'Description', type: 'textarea' },
            { name: 'display_order', label: 'Display order', type: 'number' },
          ]}
          columns={[
            { key: 'name', label: 'Name' },
            { key: 'slug', label: 'Slug' },
            { key: 'is_active', label: 'Active', render: (r) => (r.is_active ? 'Yes' : 'No') },
          ]}
          emptyLabel="No categories yet."
        />
      )}
    </AdminLayout>
  )
}
