import { useEffect, useState } from 'react'
import AdminLayout from '../components/AdminLayout'
import Tabs from '../components/Tabs'
import CrudManager from '../components/CrudManager'
import api from '../api/client'

const TABS = ['Orders', 'Transactions', 'Coupons']
const ORDER_STATUSES = ['PENDING', 'PAID', 'FAILED', 'CANCELLED', 'REFUNDED']

export default function Payments() {
  const [tab, setTab] = useState('Orders')

  return (
    <AdminLayout title="Payments">
      <Tabs tabs={TABS} active={tab} onChange={setTab} />

      {tab === 'Orders' && <OrdersList />}
      {tab === 'Transactions' && <TransactionsList />}

      {tab === 'Coupons' && (
        <CrudManager
          base="/payments/coupons"
          fields={[
            { name: 'code', label: 'Coupon code', required: true },
            { name: 'description', label: 'Description' },
            { name: 'discount_type', label: 'Discount type', type: 'select', options: ['percent', 'flat'], required: true },
            { name: 'discount_value', label: 'Discount value', type: 'number', required: true },
            { name: 'max_uses', label: 'Max uses', type: 'number' },
          ]}
          columns={[
            { key: 'code', label: 'Code' },
            { key: 'discount_type', label: 'Type' },
            { key: 'discount_value', label: 'Value' },
            { key: 'is_active', label: 'Active', render: (r) => (r.is_active ? 'Yes' : 'No') },
          ]}
          emptyLabel="No coupons yet."
        />
      )}
    </AdminLayout>
  )
}

function OrdersList() {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)

  function load() {
    setLoading(true)
    api.get('/payments/orders/admin').then((res) => setOrders(res.data)).finally(() => setLoading(false))
  }
  useEffect(load, [])

  async function updateStatus(id, status) {
    await api.patch(`/payments/orders/admin/${id}/status`, { status })
    load()
  }

  return (
    <div className="panel overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr>
            <th className="th">Order #</th>
            <th className="th">Customer</th>
            <th className="th">Total</th>
            <th className="th">Status</th>
            <th className="th">Date</th>
            <th className="th">Change status</th>
          </tr>
        </thead>
        <tbody>
          {!loading && orders.length === 0 && (
            <tr><td colSpan={6} className="td text-center text-muted2 py-10">No orders yet — orders appear once checkout is wired to a payment gateway.</td></tr>
          )}
          {orders.map((o) => (
            <tr key={o.id} className="hover:bg-canvas/60">
              <td className="td">{o.order_number}</td>
              <td className="td text-muted">#{o.customer_id}</td>
              <td className="td">₹{Number(o.total_amount).toLocaleString('en-IN')}</td>
              <td className="td">{o.status}</td>
              <td className="td text-muted">{new Date(o.created_at).toLocaleDateString()}</td>
              <td className="td">
                <select value={o.status} onChange={(e) => updateStatus(o.id, e.target.value)} className="input py-1 text-xs">
                  {ORDER_STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
                </select>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function TransactionsList() {
  const [payments, setPayments] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/payments/transactions/admin').then((res) => setPayments(res.data)).finally(() => setLoading(false))
  }, [])

  return (
    <div className="panel overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr>
            <th className="th">Payment ID</th>
            <th className="th">Order</th>
            <th className="th">Gateway</th>
            <th className="th">Amount</th>
            <th className="th">Status</th>
          </tr>
        </thead>
        <tbody>
          {!loading && payments.length === 0 && (
            <tr><td colSpan={5} className="td text-center text-muted2 py-10">No payment transactions yet.</td></tr>
          )}
          {payments.map((p) => (
            <tr key={p.id} className="hover:bg-canvas/60">
              <td className="td">{p.gateway_payment_id || `#${p.id}`}</td>
              <td className="td text-muted">#{p.order_id}</td>
              <td className="td text-muted">{p.gateway}</td>
              <td className="td">{p.currency} {Number(p.amount).toLocaleString('en-IN')}</td>
              <td className="td">{p.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <p className="text-xs text-muted2 p-4 border-t border-panelline">
        Only gateway references are ever stored here — never card numbers, CVV or bank credentials.
      </p>
    </div>
  )
}
