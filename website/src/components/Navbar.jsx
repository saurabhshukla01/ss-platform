import { useState } from 'react'
import { Link, NavLink } from 'react-router-dom'
import { Menu, X } from 'lucide-react'

const links = [
  { to: '/', label: 'Home' },
  { to: '/about', label: 'About' },
  { to: '/services', label: 'Services' },
  { to: '/pricing', label: 'Pricing' },
  { to: '/projects', label: 'Projects' },
  { to: '/faq', label: 'FAQ' },
  { to: '/contact', label: 'Contact' },
]

export default function Navbar() {
  const [open, setOpen] = useState(false)

  return (
    <header className="sticky top-0 z-40 bg-ink/90 backdrop-blur border-b border-line">
      <nav className="container-page flex items-center justify-between h-16">
        <Link to="/" className="font-display text-lg font-semibold text-high">
          Saurabh Shukla<span className="text-electric">.</span>
        </Link>

        <div className="hidden md:flex items-center gap-8">
          {links.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              className={({ isActive }) =>
                `text-sm transition-colors ${isActive ? 'text-electric' : 'text-muted hover:text-high'}`
              }
            >
              {l.label}
            </NavLink>
          ))}
        </div>

        <div className="hidden md:block">
          <Link to="/inquiry" className="btn-primary text-sm py-2.5 px-4">Get a Quote</Link>
        </div>

        <button className="md:hidden text-high" onClick={() => setOpen(!open)} aria-label="Toggle menu">
          {open ? <X size={22} /> : <Menu size={22} />}
        </button>
      </nav>

      {open && (
        <div className="md:hidden border-t border-line bg-ink">
          <div className="container-page py-4 flex flex-col gap-4">
            {links.map((l) => (
              <NavLink
                key={l.to}
                to={l.to}
                onClick={() => setOpen(false)}
                className={({ isActive }) => `text-sm ${isActive ? 'text-electric' : 'text-muted'}`}
              >
                {l.label}
              </NavLink>
            ))}
            <Link to="/inquiry" onClick={() => setOpen(false)} className="btn-primary text-sm py-2.5 justify-center">
              Get a Quote
            </Link>
          </div>
        </div>
      )}
    </header>
  )
}
