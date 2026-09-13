export default function StatCard({ label, value, hint, icon: Icon }) {
  return (
    <div className="panel p-5">
      <div className="flex items-start justify-between">
        <p className="text-xs font-medium text-muted">{label}</p>
        {Icon && <Icon size={16} className="text-electric" />}
      </div>
      <p className="text-2xl font-display font-semibold text-ink2 mt-2">{value}</p>
      {hint && <p className="text-xs text-muted2 mt-1">{hint}</p>}
    </div>
  )
}
