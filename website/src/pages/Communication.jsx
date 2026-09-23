import { useEffect, useState } from 'react'
import AdminLayout from '../components/AdminLayout'
import api from '../api/client'

export default function Communication() {
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/communication/logs').then((res) => setLogs(res.data)).finally(() => setLoading(false))
  }, [])

  return (
    <AdminLayout title="Communication">
      <p className="text-sm text-muted mb-4">
        Every outbound and inbound touch with a lead or customer, across channels. New entries are
        created from a lead's detail page or logged automatically when the backend sends email/WhatsApp.
      </p>
      <div className="panel overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr>
              <th className="th">Channel</th>
              <th className="th">Direction</th>
              <th className="th">Subject</th>
              <th className="th">Status</th>
              <th className="th">Date</th>
            </tr>
          </thead>
          <tbody>
            {!loading && logs.length === 0 && (
              <tr><td colSpan={5} className="td text-center text-muted2 py-10">No communication logged yet.</td></tr>
            )}
            {logs.map((l) => (
              <tr key={l.id} className="hover:bg-canvas/60">
                <td className="td capitalize">{l.channel}</td>
                <td className="td text-muted capitalize">{l.direction}</td>
                <td className="td text-muted">{l.subject || '—'}</td>
                <td className="td text-muted">{l.status || '—'}</td>
                <td className="td text-muted">{new Date(l.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </AdminLayout>
  )
}
