import { useEffect, useState } from 'react'
import AdminLayout from '../components/AdminLayout'
import api from '../api/client'

export default function AuditLogs() {
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(true)
  const [moduleFilter, setModuleFilter] = useState('')

  useEffect(() => {
    setLoading(true)
    const params = moduleFilter ? { module: moduleFilter } : {}
    api.get('/audit-logs', { params }).then((res) => setLogs(res.data)).finally(() => setLoading(false))
  }, [moduleFilter])

  return (
    <AdminLayout title="Audit Logs">
      <div className="mb-4">
        <input
          placeholder="Filter by module (e.g. services, leads, coupons)…"
          value={moduleFilter}
          onChange={(e) => setModuleFilter(e.target.value)}
          className="input max-w-xs"
        />
      </div>

      <div className="panel overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr>
              <th className="th">Admin</th>
              <th className="th">Action</th>
              <th className="th">Module</th>
              <th className="th">Record</th>
              <th className="th">IP</th>
              <th className="th">Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {!loading && logs.length === 0 && (
              <tr><td colSpan={6} className="td text-center text-muted2 py-10">No audit entries yet — they're written automatically on every admin create/update/delete.</td></tr>
            )}
            {logs.map((l) => (
              <tr key={l.id} className="hover:bg-canvas/60">
                <td className="td text-muted">{l.admin_id ? `#${l.admin_id}` : '—'}</td>
                <td className="td capitalize">{l.action}</td>
                <td className="td text-muted">{l.module}</td>
                <td className="td text-muted">{l.record_id || '—'}</td>
                <td className="td text-muted">{l.ip_address || '—'}</td>
                <td className="td text-muted">{new Date(l.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </AdminLayout>
  )
}
