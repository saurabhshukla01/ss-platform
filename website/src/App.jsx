import {
  Route,
  Routes,
} from 'react-router-dom'

import ProtectedRoute from './components/ProtectedRoute'

import Home from './pages/Home'
import About from './pages/About'
import Services from './pages/Services'
import ServiceDetail from './pages/ServiceDetail'
import PricingPublic from './pages/Pricing'
import ProjectsPublic from './pages/Projects'
import FAQLegal from './pages/FAQLegal'
import Contact from './pages/Contact'
import InquiryPublic from './pages/Inquiry'
import CheckoutPublic from './pages/Checkout'
import NotFound from './pages/NotFound'

import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import AnalyticsPage from './pages/AnalyticsPage'

import Leads from './pages/crm/Leads'
import Inquiries from './pages/crm/Inquiries'
import LeadDetail from './pages/crm/LeadDetail'

import ServicesList from './pages/services/ServicesList'
import ServiceForm from './pages/services/ServiceForm'

import Subscriptions from './pages/Subscriptions'
import Payments from './pages/Payments'
import Website from './pages/Website'
import Content from './pages/Content'
import SEO from './pages/SEO'
import Communication from './pages/Communication'
import Settings from './pages/Settings'
import AuditLogs from './pages/AuditLogs'

export default function App() {
  return (
    <Routes>
      {/* =====================================================
          PUBLIC WEBSITE — the customer-facing site, managed
          from the Admin Panel (Website / Content / Settings).
          ===================================================== */}

      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/services" element={<Services />} />
      <Route path="/services/:slug" element={<ServiceDetail />} />
      <Route path="/pricing" element={<PricingPublic />} />
      <Route path="/projects" element={<ProjectsPublic />} />
      <Route path="/faq" element={<FAQLegal />} />
      <Route path="/contact" element={<Contact />} />
      <Route path="/inquiry" element={<InquiryPublic />} />
      <Route path="/checkout" element={<CheckoutPublic />} />

      {/* =====================================================
          ADMIN LOGIN
          ===================================================== */}

      <Route
        path="/login"
        element={<Login />}
      />

      {/* =====================================================
          PROTECTED ADMIN ROUTES — all live under /admin so they
          never collide with the public site's paths above.
          ===================================================== */}

      <Route
        element={<ProtectedRoute />}
      >
        {/* Dashboard */}

        <Route
          path="/admin"
          element={<Dashboard />}
        />

        {/* Analytics */}

        <Route
          path="/admin/analytics"
          element={
            <AnalyticsPage />
          }
        />

        {/* =================================================
            CRM
            ================================================= */}

        <Route
          path="/admin/crm"
          element={<Leads />}
        />

        <Route
          path="/admin/crm/inquiries"
          element={
            <Inquiries />
          }
        />

        <Route
          path="/admin/crm/leads/:id"
          element={
            <LeadDetail />
          }
        />

        {/* =================================================
            SERVICES
            ================================================= */}

        <Route
          path="/admin/services"
          element={
            <ServicesList />
          }
        />

        <Route
          path="/admin/services/new"
          element={
            <ServiceForm />
          }
        />

        <Route
          path="/admin/services/:id/edit"
          element={
            <ServiceForm />
          }
        />

        {/* =================================================
            SUBSCRIPTIONS
            ================================================= */}

        <Route
          path="/admin/subscriptions"
          element={
            <Subscriptions />
          }
        />

        {/* =================================================
            PAYMENTS
            ================================================= */}

        <Route
          path="/admin/payments"
          element={
            <Payments />
          }
        />

        {/* =================================================
            WEBSITE
            ================================================= */}

        <Route
          path="/admin/website"
          element={
            <Website />
          }
        />

        {/* =================================================
            CONTENT
            ================================================= */}

        <Route
          path="/admin/content"
          element={
            <Content />
          }
        />

        {/* =================================================
            SEO
            ================================================= */}

        <Route
          path="/admin/seo"
          element={<SEO />}
        />

        {/* =================================================
            COMMUNICATION
            ================================================= */}

        <Route
          path="/admin/communication"
          element={
            <Communication />
          }
        />

        {/* =================================================
            SETTINGS
            ================================================= */}

        <Route
          path="/admin/settings"
          element={
            <Settings />
          }
        />

        {/* =================================================
            AUDIT LOGS
            ================================================= */}

        <Route
          path="/admin/audit-logs"
          element={
            <AuditLogs />
          }
        />
      </Route>

      {/* =====================================================
          UNKNOWN ROUTES — public 404 (keeps site nav/footer)
          ===================================================== */}

      <Route
        path="*"
        element={<NotFound />}
      />
    </Routes>
  )
}
