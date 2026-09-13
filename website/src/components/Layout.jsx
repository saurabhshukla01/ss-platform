import { useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import Navbar from './Navbar'
import Footer from './Footer'
import AnnouncementBar from './AnnouncementBar'
import StickyMobileActions from './StickyMobileActions'
import { startSessionOnce, trackPageView } from '../api/analytics'

export default function Layout({ children }) {
  const location = useLocation()

  useEffect(() => {
    startSessionOnce()
    trackPageView(location.pathname)
    window.scrollTo(0, 0)
  }, [location.pathname])

  return (
    <div className="min-h-screen flex flex-col">
      <AnnouncementBar />
      <Navbar />
      <main className="flex-1 pb-16 md:pb-0">{children}</main>
      <Footer />
      <StickyMobileActions />
    </div>
  )
}
