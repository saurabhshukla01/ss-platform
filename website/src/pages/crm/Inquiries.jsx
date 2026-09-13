import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import AdminLayout from '../../components/AdminLayout'
import api from '../../api/client'

export default function Inquiries() {
  const [inquiries, setInquiries] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/inquiries/admin').then((res) => setInquiries(res.data)).finally(() => setLoading(false))
  }, [])

  return (
    <AdminLayout title="CRM — Inquiries">
      <div className="flex gap-4 mb-5 border-b border-panelline">
        <Link to="/admin/crm" className="text-sm text-muted pb-2 hover:text-ink2">Leads</Link>
        <span className="text-sm font-medium text-electric border-b-2 border-electric pb-2">Inquiries</span>
      </div>

      <div className="panel overflow-hidden">
        <table className="w-full">
          <thead>
            <tr>
              <th className="th">Name</th>
              <th className="th">Email</th>
              <th className="th">Phone</th>
              <th className="th">Budget</th>
              <th className="th">Timeline</th>
              <th className="th">Received</th>
            </tr>
          </thead>
          <tbody>
            {!loading && inquiries.length === 0 && (
              <tr><td colSpan={6} className="td text-center text-muted2 py-10">No inquiries submitted yet.</td></tr>
            )}
            {inquiries.map((i) => (
              <tr key={i.id} className="hover:bg-canvas/60">
                <td className="td">{i.full_name}</td>
                <td className="td text-muted">{i.email}</td>
                <td className="td text-muted">{i.phone || '—'}</td>
                <td className="td text-muted">{i.budget_range || '—'}</td>
                <td className="td text-muted">{i.timeline || '—'}</td>
                <td className="td text-muted">{new Date(i.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </AdminLayout>
  )
}
