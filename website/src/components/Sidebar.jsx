import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard, BarChart3, Users, Boxes, Repeat, CreditCard,
  Globe, FileText, Search, MessageSquare, Settings, ClipboardList,
} from 'lucide-react'

const nav = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard, end: true },
  { to: '/analytics', label: 'Analytics', icon: BarChart3 },
  { to: '/crm', label: 'CRM', icon: Users },
  { to: '/services', label: 'Services', icon: Boxes },
  { to: '/subscriptions', label: 'Subscriptions', icon: Repeat },
  { to: '/payments', label: 'Payments', icon: CreditCard },
  { to: '/website', label: 'Website', icon: Globe },
  { to: '/content', label: 'Content', icon: FileText },
  { to: '/seo', label: 'SEO', icon: Search },
  { to: '/communication', label: 'Communication', icon: MessageSquare },
  { to: '/settings', label: 'Settings', icon: Settings },
  { to: '/audit-logs', label: 'Audit Logs', icon: ClipboardList },
]

export default function Sidebar() {
  return (
    <aside className="w-60 shrink-0 bg-ink min-h-screen flex flex-col fixed inset-y-0 left-0">
      <div className="h-16 flex items-center px-6 border-b border-line">
        <span className="font-display text-white font-semibold">
          SS Platform<span className="text-electric">.</span>
        </span>
      </div>
      <nav className="flex-1 py-4 px-3 space-y-1 overflow-y-auto">
        {nav.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded text-sm transition-colors ${
                isActive ? 'bg-electric/15 text-electric' : 'text-white/60 hover:text-white hover:bg-white/5'
              }`
            }
          >
            <Icon size={17} />
            {label}
          </NavLink>
        ))}
      </nav>
      <div className="p-4 border-t border-line text-xs text-white/40">
        Business Command Center
      </div>
    </aside>
  )
}
