import {
  Navigate,
  Route,
  Routes,
} from 'react-router-dom'

import ProtectedRoute from './components/ProtectedRoute'

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
          PUBLIC ROUTES
          ===================================================== */}

      <Route
        path="/login"
        element={<Login />}
      />

      {/* =====================================================
          PROTECTED ADMIN ROUTES
          ===================================================== */}

      <Route
        element={<ProtectedRoute />}
      >
        {/* Dashboard */}

        <Route
          path="/admin"
          element={<Dashboard />}
        />

        {/* Root */}

        <Route
          path="/"
          element={
            <Navigate
              to="/admin"
              replace
            />
          }
        />

        {/* Analytics */}

        <Route
          path="/analytics"
          element={
            <AnalyticsPage />
          }
        />

        {/* =================================================
            CRM
            ================================================= */}

        <Route
          path="/crm"
          element={<Leads />}
        />

        <Route
          path="/crm/inquiries"
          element={
            <Inquiries />
          }
        />

        <Route
          path="/crm/leads/:id"
          element={
            <LeadDetail />
          }
        />

        {/* =================================================
            SERVICES
            ================================================= */}

        <Route
          path="/services"
          element={
            <ServicesList />
          }
        />

        <Route
          path="/services/new"
          element={
            <ServiceForm />
          }
        />

        <Route
          path="/services/:id/edit"
          element={
            <ServiceForm />
          }
        />

        {/* =================================================
            SUBSCRIPTIONS
            ================================================= */}

        <Route
          path="/subscriptions"
          element={
            <Subscriptions />
          }
        />

        {/* =================================================
            PAYMENTS
            ================================================= */}

        <Route
          path="/payments"
          element={
            <Payments />
          }
        />

        {/* =================================================
            WEBSITE
            ================================================= */}

        <Route
          path="/website"
          element={
            <Website />
          }
        />

        {/* =================================================
            CONTENT
            ================================================= */}

        <Route
          path="/content"
          element={
            <Content />
          }
        />

        {/* =================================================
            SEO
            ================================================= */}

        <Route
          path="/seo"
          element={<SEO />}
        />

        {/* =================================================
            COMMUNICATION
            ================================================= */}

        <Route
          path="/communication"
          element={
            <Communication />
          }
        />

        {/* =================================================
            SETTINGS
            ================================================= */}

        <Route
          path="/settings"
          element={
            <Settings />
          }
        />

        {/* =================================================
            AUDIT LOGS
            ================================================= */}

        <Route
          path="/audit-logs"
          element={
            <AuditLogs />
          }
        />
      </Route>

      {/* =====================================================
          UNKNOWN ROUTES
          ===================================================== */}

      <Route
        path="*"
        element={
          <Navigate
            to="/admin"
            replace
          />
        }
      />
    </Routes>
  )
}
