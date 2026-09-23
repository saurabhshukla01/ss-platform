import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import AdminLayout from '../../components/AdminLayout'
import StatusBadge from '../../components/StatusBadge'
import api from '../../api/client'

const STATUS_FLOW = ['NEW', 'CONTACTED', 'QUALIFIED', 'PROPOSAL_SENT', 'NEGOTIATION', 'CONVERTED', 'CLOSED']

export default function LeadDetail() {
  const { id } = useParams()
  const [lead, setLead] = useState(null)
  const [note, setNote] = useState('')
  const [followupAt, setFollowupAt] = useState('')
  const [followupChannel, setFollowupChannel] = useState('call')
  const [saving, setSaving] = useState(false)

  function load() {
    api.get(`/crm/leads/${id}`).then((res) => setLead(res.data))
  }

  useEffect(load, [id])

  async function updateStatus(status) {
    setSaving(true)
    await api.patch(`/crm/leads/${id}/status`, { status })
    load()
    setSaving(false)
  }

  async function submitNote(e) {
    e.preventDefault()
    if (!note.trim()) return
    await api.post(`/crm/leads/${id}/notes`, { note })
    setNote('')
    load()
  }

  async function submitFollowup(e) {
    e.preventDefault()
    if (!followupAt) return
    await api.post(`/crm/leads/${id}/followups`, {
      scheduled_at: new Date(followupAt).toISOString(),
      channel: followupChannel,
    })
    setFollowupAt('')
    load()
  }

  if (!lead) return <AdminLayout title="Lead"><p className="text-muted text-sm">Loading…</p></AdminLayout>

  return (
    <AdminLayout title={`Lead #${lead.id}`}>
      <Link to="/admin/crm" className="btn-ghost mb-4"><ArrowLeft size={14} /> Back to leads</Link>

      <div className="grid lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="panel p-5">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-sm font-medium text-ink2">Pipeline status</h2>
              <StatusBadge status={lead.status} />
            </div>
            <div className="flex flex-wrap gap-2">
              {STATUS_FLOW.map((s) => (
                <button
                  key={s}
                  disabled={saving || s === lead.status}
                  onClick={() => updateStatus(s)}
                  className={`text-xs px-3 py-1.5 rounded border transition-colors disabled:opacity-40 ${s === lead.status ? 'border-electric text-electric' : 'border-panelline text-muted hover:border-electric'
                    }`}
                >
                  {s.replace('_', ' ')}
                </button>
              ))}
            </div>
          </div>

          <div className="panel p-5">
            <h2 className="text-sm font-medium text-ink2 mb-3">Add note</h2>
            <form onSubmit={submitNote} className="flex gap-2">
              <input
                value={note}
                onChange={(e) => setNote(e.target.value)}
                placeholder="Log a call, WhatsApp reply, or internal note…"
                className="input flex-1"
              />
              <button type="submit" className="btn-secondary">Add</button>
            </form>
          </div>

          <div className="panel p-5">
            <h2 className="text-sm font-medium text-ink2 mb-3">Schedule follow-up</h2>
            <form onSubmit={submitFollowup} className="flex flex-wrap gap-2">
              <input
                type="datetime-local"
                value={followupAt}
                onChange={(e) => setFollowupAt(e.target.value)}
                className="input flex-1 min-w-[200px]"
              />
              <select value={followupChannel} onChange={(e) => setFollowupChannel(e.target.value)} className="input w-32">
                <option value="call">Call</option>
                <option value="whatsapp">WhatsApp</option>
                <option value="email">Email</option>
              </select>
              <button type="submit" className="btn-secondary">Schedule</button>
            </form>
          </div>
        </div>

        <div className="panel p-5 h-fit">
          <h2 className="text-sm font-medium text-ink2 mb-3">Lead info</h2>
          <dl className="space-y-3 text-sm">
            <Row label="Source" value={lead.source || '—'} />
            <Row label="Estimated value" value={lead.estimated_value ? `₹${Number(lead.estimated_value).toLocaleString('en-IN')}` : '—'} />
            <Row label="Inquiry ID" value={lead.inquiry_id ? `#${lead.inquiry_id}` : '—'} />
            <Row label="Customer ID" value={lead.customer_id ? `#${lead.customer_id}` : 'Not yet linked'} />
            <Row label="Created" value={new Date(lead.created_at).toLocaleString()} />
          </dl>
        </div>
      </div>
    </AdminLayout>
  )
}

function Row({ label, value }) {
  return (
    <div className="flex justify-between border-t border-panelline pt-3 first:border-0 first:pt-0">
      <dt className="text-muted">{label}</dt>
      <dd className="text-ink2 font-medium text-right">{value}</dd>
    </div>
  )
}