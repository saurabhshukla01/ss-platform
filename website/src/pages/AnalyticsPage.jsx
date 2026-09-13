import { useEffect, useState } from 'react'
import AdminLayout from '../components/AdminLayout'
import StatCard from '../components/StatCard'
import api from '../api/client'
import { Eye, Users, FileText } from 'lucide-react'

export default function AnalyticsPage() {
  const [summary, setSummary] = useState(null)

  useEffect(() => {
    api.get('/analytics/admin/summary').then((res) => setSummary(res.data)).catch(() => {})
  }, [])

  return (
    <AdminLayout title="Analytics">
      <div className="grid sm:grid-cols-3 gap-4">
        <StatCard label="Visitors" icon={Users} value={summary?.total_visitors ?? '—'} />
        <StatCard label="Sessions" icon={Eye} value={summary?.total_sessions ?? '—'} />
        <StatCard label="Page views" icon={FileText} value={summary?.total_page_views ?? '—'} />
      </div>

      <div className="grid md:grid-cols-2 gap-6 mt-6">
        <div className="panel p-5">
          <h2 className="text-sm font-medium text-ink2 mb-4">Business events</h2>
          {summary?.top_events?.length ? (
            <div className="space-y-3">
              {summary.top_events.map((e) => (
                <BarRow key={e.event_type} label={e.event_type.replace(/_/g, ' ')} value={e.count}
                  max={Math.max(...summary.top_events.map((x) => x.count))} />
              ))}
            </div>
          ) : <p className="text-sm text-muted2">No events tracked yet — events fire automatically as visitors use the website.</p>}
        </div>

        <div className="panel p-5">
          <h2 className="text-sm font-medium text-ink2 mb-4">Traffic sources (UTM)</h2>
          {summary?.top_utm_sources?.length ? (
            <div className="space-y-3">
              {summary.top_utm_sources.map((s) => (
                <BarRow key={s.source} label={s.source} value={s.count}
                  max={Math.max(...summary.top_utm_sources.map((x) => x.count))} />
              ))}
            </div>
          ) : <p className="text-sm text-muted2">No campaign (UTM) traffic recorded yet.</p>}
        </div>
      </div>
    </AdminLayout>
  )
}

function BarRow({ label, value, max }) {
  const pct = max ? Math.round((value / max) * 100) : 0
  return (
    <div>
      <div className="flex justify-between text-sm mb-1">
        <span className="text-muted capitalize">{label}</span>
        <span className="text-ink2 font-medium">{value}</span>
      </div>
      <div className="h-1.5 bg-canvas rounded overflow-hidden">
        <div className="h-full bg-electric rounded" style={{ width: `${pct}%` }} />
      </div>
    </div>
  )
}
