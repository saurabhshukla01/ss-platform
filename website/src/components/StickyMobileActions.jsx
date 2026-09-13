import { Link } from 'react-router-dom'
import { Phone, MessageCircle, FileText } from 'lucide-react'
import { trackEvent } from '../api/analytics'

export default function StickyMobileActions() {
  return (
    <div className="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-surface border-t border-line grid grid-cols-3">
      <a
        href="https://wa.me/910000000000"
        onClick={() => trackEvent('whatsapp_click')}
        className="flex flex-col items-center justify-center gap-1 py-3 text-xs text-muted hover:text-cyan"
      >
        <MessageCircle size={18} />
        WhatsApp
      </a>
      <a
        href="tel:+910000000000"
        onClick={() => trackEvent('call_click')}
        className="flex flex-col items-center justify-center gap-1 py-3 text-xs text-muted hover:text-cyan border-x border-line"
      >
        <Phone size={18} />
        Call
      </a>
      <Link
        to="/inquiry"
        onClick={() => trackEvent('quote_click')}
        className="flex flex-col items-center justify-center gap-1 py-3 text-xs text-electric"
      >
        <FileText size={18} />
        Get Quote
      </Link>
    </div>
  )
}
