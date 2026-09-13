const colors = {
  NEW: 'bg-status-new/10 text-status-new',
  CONTACTED: 'bg-status-contacted/10 text-status-contacted',
  QUALIFIED: 'bg-status-qualified/10 text-status-qualified',
  PROPOSAL_SENT: 'bg-status-proposal/10 text-status-proposal',
  NEGOTIATION: 'bg-status-negotiation/10 text-status-negotiation',
  CONVERTED: 'bg-status-converted/10 text-status-converted',
  CLOSED: 'bg-status-closed/10 text-status-closed',
}

const labels = {
  NEW: 'New',
  CONTACTED: 'Contacted',
  QUALIFIED: 'Qualified',
  PROPOSAL_SENT: 'Proposal sent',
  NEGOTIATION: 'Negotiation',
  CONVERTED: 'Converted',
  CLOSED: 'Closed',
}

export default function StatusBadge({ status }) {
  return (
    <span className={`badge ${colors[status] || 'bg-gray-100 text-gray-600'}`}>
      {labels[status] || status}
    </span>
  )
}
