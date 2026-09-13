import { X } from 'lucide-react'
import { useEffect, useState } from 'react'
import api from '../api/client'

export default function AnnouncementBar() {
  const [announcement, setAnnouncement] = useState(null)
  const [dismissed, setDismissed] = useState(false)

  useEffect(() => {
    api.get('/website/announcements').then((res) => {
      if (res.data?.length) {
        setAnnouncement(res.data[0])
      }
    }).catch(() => {})
  }, [])

  if (dismissed || !announcement) return null

  return (
    <div className="bg-electric text-ink text-sm">
      <div className="container-page flex items-center justify-between py-2">
        {announcement.link_url ? (
          <a href={announcement.link_url} className="truncate hover:underline">
            {announcement.message}
          </a>
        ) : (
          <p className="truncate">{announcement.message}</p>
        )}
        <button
          onClick={() => setDismissed(true)}
          aria-label="Dismiss announcement"
          className="shrink-0 ml-4 hover:opacity-70"
        >
          <X size={16} />
        </button>
      </div>
    </div>
  )
}
