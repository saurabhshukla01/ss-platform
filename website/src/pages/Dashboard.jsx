import { useEffect, useState } from 'react'
import { Users, Eye, TrendingUp, Boxes } from 'lucide-react'
import AdminLayout from '../components/AdminLayout'
import StatCard from '../components/StatCard'
import StatusBadge from '../components/StatusBadge'
import api from '../api/client'

export default function Dashboard() {
  const [summary, setSummary] = useState(null)
  const [leads, setLeads] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      api.get('/analytics/admin/summary').catch(() => ({ data: null })),
      api.get('/crm/leads').catch(() => ({ data: [] })),
    ]).then(([s, l]) => {
      setSummary(s.data)
      setLeads(l.data.slice(0, 6))
    }).finally(() => setLoading(false))
  }, [])

  const convertedCount = leads.filter((l) => l.status === 'CONVERTED').length
  const conversionRate = leads.length ? Math.round((convertedCount / leads.length) * 100) : 0

  return (
    <AdminLayout title="Dashboard">
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard label="Total visitors" icon={Eye} value={summary?.total_visitors ?? '—'} hint="First-party tracked" />
        <StatCard label="Total sessions" icon={Users} value={summary?.total_sessions ?? '—'} />
        <StatCard label="Leads in pipeline" icon={Boxes} value={leads.length} />
        <StatCard label="Conversion rate" icon={TrendingUp} value={`${conversionRate}%`} hint="Of recent leads" />
      </div>

      <div className="grid lg:grid-cols-3 gap-6 mt-6">
        <div className="lg:col-span-2 panel">
          <div className="px-5 py-4 border-b border-panelline flex items-center justify-between">
            <h2 className="text-sm font-medium text-ink2">Recent leads</h2>
            <a href="/crm" className="btn-ghost">View all</a>
          </div>
          <table className="w-full">
            <thead>
              <tr>
                <th className="th">Lead</th>
                <th className="th">Source</th>
                <th className="th">Status</th>
              </tr>
            </thead>
            <tbody>
              {!loading && leads.length === 0 && (
                <tr><td colSpan={3} className="td text-center text-muted2 py-8">No leads yet.</td></tr>
              )}
              {leads.map((l) => (
                <tr key={l.id}>
                  <td className="td">Lead #{l.id}</td>
                  <td className="td text-muted">{l.source || '—'}</td>
                  <td className="td"><StatusBadge status={l.status} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="panel p-5">
          <h2 className="text-sm font-medium text-ink2 mb-4">Top events</h2>
          <div className="space-y-3">
            {summary?.top_events?.length ? summary.top_events.map((e) => (
              <div key={e.event_type} className="flex items-center justify-between text-sm">
                <span className="text-muted capitalize">{e.event_type.replace(/_/g, ' ')}</span>
                <span className="text-ink2 font-medium">{e.count}</span>
              </div>
            )) : <p className="text-sm text-muted2">No events tracked yet.</p>}
          </div>

          <h2 className="text-sm font-medium text-ink2 mb-4 mt-6 pt-4 border-t border-panelline">Top sources</h2>
          <div className="space-y-3">
            {summary?.top_utm_sources?.length ? summary.top_utm_sources.map((s) => (
              <div key={s.source} className="flex items-center justify-between text-sm">
                <span className="text-muted">{s.source}</span>
                <span className="text-ink2 font-medium">{s.count}</span>
              </div>
            )) : <p className="text-sm text-muted2">No campaign traffic tracked yet.</p>}
          </div>
        </div>
      </div>
    </AdminLayout>
  )
}
