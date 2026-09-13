import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer className="border-t border-line bg-surface mt-24">
      <div className="container-page py-12 grid grid-cols-2 md:grid-cols-4 gap-8">
        <div className="col-span-2 md:col-span-1">
          <p className="font-display text-lg font-semibold text-high">Saurabh Shukla<span className="text-electric">.</span></p>
          <p className="text-muted text-sm mt-2">CTO — SS Collections Group</p>
          <p className="text-muted2 text-sm mt-4">Build. Automate. Grow.</p>
        </div>

        <div>
          <p className="text-high text-sm font-medium mb-3">Explore</p>
          <ul className="space-y-2 text-sm text-muted">
            <li><Link to="/services" className="hover:text-electric">Services</Link></li>
            <li><Link to="/pricing" className="hover:text-electric">Pricing</Link></li>
            <li><Link to="/projects" className="hover:text-electric">Projects</Link></li>
            <li><Link to="/about" className="hover:text-electric">About</Link></li>
          </ul>
        </div>

        <div>
          <p className="text-high text-sm font-medium mb-3">Company</p>
          <ul className="space-y-2 text-sm text-muted">
            <li><Link to="/faq" className="hover:text-electric">FAQ</Link></li>
            <li><Link to="/faq#privacy" className="hover:text-electric">Privacy Policy</Link></li>
            <li><Link to="/faq#terms" className="hover:text-electric">Terms &amp; Conditions</Link></li>
            <li><Link to="/contact" className="hover:text-electric">Contact</Link></li>
          </ul>
        </div>

        <div>
          <p className="text-high text-sm font-medium mb-3">Start a project</p>
          <p className="text-muted text-sm mb-3">Tell us what you're building — we'll reply with next steps.</p>
          <Link to="/inquiry" className="btn-ghost text-sm">Get a free consultation</Link>
        </div>
      </div>

      <div className="border-t border-line">
        <div className="container-page py-4 text-xs text-muted2">
          © {new Date().getFullYear()} Saurabh Shukla / SS Collections Group. All rights reserved.
        </div>
      </div>
    </footer>
  )
}
