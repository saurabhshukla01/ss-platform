export default function Tabs({ tabs, active, onChange }) {
  return (
    <div className="flex flex-wrap gap-2 mb-5 border-b border-panelline">
      {tabs.map((t) => (
        <button
          key={t}
          onClick={() => onChange(t)}
          className={`text-sm pb-2 px-1 border-b-2 -mb-px transition-colors ${
            active === t ? 'border-electric text-electric font-medium' : 'border-transparent text-muted hover:text-ink2'
          }`}
        >
          {t}
        </button>
      ))}
    </div>
  )
}
