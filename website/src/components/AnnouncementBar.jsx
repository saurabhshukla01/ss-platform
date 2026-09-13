import { X } from 'lucide-react'
import { useState } from 'react'

export default function AnnouncementBar() {
  const [open, setOpen] = useState(true)
  if (!open) return null

  return (
    <div className="bg-electric text-ink text-sm">
      <div className="container-page flex items-center justify-between py-2">
        <p className="truncate">
          New: Business plan now includes a free 30-day maintenance window — mention this on your inquiry.
        </p>
        <button
          onClick={() => setOpen(false)}
          aria-label="Dismiss announcement"
          className="shrink-0 ml-4 hover:opacity-70"
        >
          <X size={16} />
        </button>
      </div>
    </div>
  )
}
