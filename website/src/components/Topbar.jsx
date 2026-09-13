import { LogOut, Bell } from 'lucide-react'
import { useAuth } from '../auth/AuthContext'

export default function Topbar({ title }) {
  const { admin, logout } = useAuth()

  return (
    <header className="h-16 bg-panel border-b border-panelline flex items-center justify-between px-6 sticky top-0 z-10">
      <h1 className="text-lg font-semibold text-ink2">{title}</h1>
      <div className="flex items-center gap-5">
        <button className="text-muted hover:text-ink2" aria-label="Notifications">
          <Bell size={18} />
        </button>
        <div className="flex items-center gap-3">
          <div className="text-right hidden sm:block">
            <p className="text-sm font-medium text-ink2 leading-tight">{admin?.full_name}</p>
            <p className="text-xs text-muted leading-tight">{admin?.role_name || 'Admin'}</p>
          </div>
          <div className="w-8 h-8 rounded-full bg-electric/15 text-electric flex items-center justify-center text-sm font-medium">
            {admin?.full_name?.[0] || 'A'}
          </div>
          <button onClick={logout} className="text-muted hover:text-ink2" aria-label="Log out">
            <LogOut size={18} />
          </button>
        </div>
      </div>
    </header>
  )
}
