import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import AdminLayout from '../../components/AdminLayout'
import StatusBadge from '../../components/StatusBadge'
import api from '../../api/client'

const STATUSES = ['ALL', 'NEW', 'CONTACTED', 'QUALIFIED', 'PROPOSAL_SENT', 'NEGOTIATION', 'CONVERTED', 'CLOSED']

export default function Leads() {
  const [leads, setLeads] = useState([])
  const [filter, setFilter] = useState('ALL')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    const params = filter !== 'ALL' ? { status_filter: filter } : {}
    api.get('/crm/leads', { params }).then((res) => setLeads(res.data)).finally(() => setLoading(false))
  }, [filter])

  return (
    <AdminLayout title="CRM — Leads">
      <div className="flex gap-4 mb-5 border-b border-panelline">
        <span className="text-sm font-medium text-electric border-b-2 border-electric pb-2">Leads</span>
        <Link to="/admin/crm/inquiries" className="text-sm text-muted pb-2 hover:text-ink2">Inquiries</Link>
      </div>

      <div className="flex flex-wrap gap-2 mb-4">
        {STATUSES.map((s) => (
          <button
            key={s}
            onClick={() => setFilter(s)}
            className={`text-xs px-3 py-1.5 rounded border ${filter === s ? 'border-electric text-electric bg-electric/5' : 'border-panelline text-muted'
              }`}
          >
            {s === 'ALL' ? 'All' : s.replace('_', ' ')}
          </button>
        ))}
      </div>

      <div className="panel overflow-hidden">
        <table className="w-full">
          <thead>
            <tr>
              <th className="th">ID</th>
              <th className="th">Source</th>
              <th className="th">Status</th>
              <th className="th">Est. value</th>
              <th className="th">Created</th>
              <th className="th"></th>
            </tr>
          </thead>
          <tbody>
            {!loading && leads.length === 0 && (
              <tr><td colSpan={6} className="td text-center text-muted2 py-10">No leads match this filter.</td></tr>
            )}
            {leads.map((l) => (
              <tr key={l.id} className="hover:bg-canvas/60">
                <td className="td">#{l.id}</td>
                <td className="td text-muted">{l.source || '—'}</td>
                <td className="td"><StatusBadge status={l.status} /></td>
                <td className="td">{l.estimated_value ? `₹${Number(l.estimated_value).toLocaleString('en-IN')}` : '—'}</td>
                <td className="td text-muted">{new Date(l.created_at).toLocaleDateString()}</td>
                <td className="td text-right">
                  <Link to={`/admin/crm/leads/${l.id}`} className="btn-ghost">Open</Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </AdminLayout>
  )
}