import Sidebar from './Sidebar'
import Topbar from './Topbar'

export default function AdminLayout({ title, children }) {
  return (
    <div className="min-h-screen bg-canvas overflow-x-hidden">
      <Sidebar />
      <div className="ml-60">
        <Topbar title={title} />
        <main className="p-6">{children}</main>
      </div>
    </div>
  )
}
