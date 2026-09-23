import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard,
  BarChart3,
  Users,
  Boxes,
  Repeat,
  CreditCard,
  Globe,
  FileText,
  Search,
  MessageSquare,
  Settings,
  ClipboardList,
} from 'lucide-react'

const nav = [
  {
    to: '/admin',
    label: 'Dashboard',
    icon: LayoutDashboard,
    end: true,
  },
  {
    to: '/admin/analytics',
    label: 'Analytics',
    icon: BarChart3,
  },
  {
    to: '/admin/crm',
    label: 'CRM',
    icon: Users,
  },
  {
    to: '/admin/services',
    label: 'Services',
    icon: Boxes,
  },
  {
    to: '/admin/subscriptions',
    label: 'Subscriptions',
    icon: Repeat,
  },
  {
    to: '/admin/payments',
    label: 'Payments',
    icon: CreditCard,
  },
  {
    to: '/admin/website',
    label: 'Website',
    icon: Globe,
  },
  {
    to: '/admin/content',
    label: 'Content',
    icon: FileText,
  },
  {
    to: '/admin/seo',
    label: 'SEO',
    icon: Search,
  },
  {
    to: '/admin/communication',
    label: 'Communication',
    icon: MessageSquare,
  },
  {
    to: '/admin/settings',
    label: 'Settings',
    icon: Settings,
  },
  {
    to: '/admin/audit-logs',
    label: 'Audit Logs',
    icon: ClipboardList,
  },
]

export default function Sidebar() {
  return (
    <aside className="w-60 shrink-0 bg-ink min-h-screen flex flex-col fixed inset-y-0 left-0 z-40">
      {/* Logo */}
      <div className="h-16 flex items-center px-6 border-b border-line">
        <span className="font-display text-white font-semibold">
          SS Platform
          <span className="text-electric">.</span>
        </span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 py-4 px-3 space-y-1 overflow-y-auto">
        {nav.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              [
                'flex items-center gap-3',
                'px-3 py-2.5',
                'rounded',
                'text-sm',
                'transition-colors',
                'duration-150',
                isActive
                  ? 'bg-electric/15 text-electric'
                  : 'text-white/60 hover:text-white hover:bg-white/5',
              ].join(' ')
            }
          >
            <Icon size={17} />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-line text-xs text-white/40">
        Business Command Center
      </div>
    </aside>
  )
}