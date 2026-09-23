import { useEffect, useState } from 'react'
import AdminLayout from '../components/AdminLayout'
import Tabs from '../components/Tabs'
import CrudManager from '../components/CrudManager'
import api from '../api/client'

const TABS = ['Plans', 'Active Subscriptions']
const STATUSES = ['ACTIVE', 'PAST_DUE', 'CANCELLED', 'EXPIRED']

export default function Subscriptions() {
  const [tab, setTab] = useState('Plans')

  return (
    <AdminLayout title="Subscriptions">
      <Tabs tabs={TABS} active={tab} onChange={setTab} />

      {tab === 'Plans' && (
        <CrudManager
          base="/subscriptions/plans"
          fields={[
            { name: 'name', label: 'Plan name', required: true },
            { name: 'price', label: 'Price (₹)', type: 'number', required: true },
            { name: 'billing_interval', label: 'Billing interval', type: 'select', options: ['MONTHLY', 'YEARLY'], required: true },
            { name: 'features', label: 'Features (free text / JSON)', type: 'textarea' },
          ]}
          columns={[
            { key: 'name', label: 'Plan' },
            { key: 'price', label: 'Price', render: (r) => `₹${Number(r.price).toLocaleString('en-IN')}` },
            { key: 'billing_interval', label: 'Billing' },
          ]}
          emptyLabel="No subscription plans yet — add one to show it on the Pricing page."
        />
      )}

      {tab === 'Active Subscriptions' && <SubscriptionsList />}
    </AdminLayout>
  )
}

function SubscriptionsList() {
  const [subs, setSubs] = useState([])
  const [loading, setLoading] = useState(true)

  function load() {
    setLoading(true)
    api.get('/subscriptions/admin').then((res) => setSubs(res.data)).finally(() => setLoading(false))
  }
  useEffect(load, [])

  async function updateStatus(id, status) {
    await api.patch(`/subscriptions/admin/${id}/status`, { status })
    load()
  }

  return (
    <div className="panel overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr>
            <th className="th">ID</th>
            <th className="th">Customer</th>
            <th className="th">Plan</th>
            <th className="th">Status</th>
            <th className="th">Next renewal</th>
            <th className="th">Change status</th>
          </tr>
        </thead>
        <tbody>
          {!loading && subs.length === 0 && (
            <tr><td colSpan={6} className="td text-center text-muted2 py-10">No subscriptions yet.</td></tr>
          )}
          {subs.map((s) => (
            <tr key={s.id} className="hover:bg-canvas/60">
              <td className="td">#{s.id}</td>
              <td className="td text-muted">#{s.customer_id}</td>
              <td className="td text-muted">#{s.plan_id}</td>
              <td className="td">{s.status}</td>
              <td className="td text-muted">{s.next_renewal_date ? new Date(s.next_renewal_date).toLocaleDateString() : '—'}</td>
              <td className="td">
                <select
                  value={s.status}
                  onChange={(e) => updateStatus(s.id, e.target.value)}
                  className="input py-1 text-xs"
                >
                  {STATUSES.map((st) => <option key={st} value={st}>{st}</option>)}
                </select>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
