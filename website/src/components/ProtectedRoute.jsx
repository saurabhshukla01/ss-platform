import {
  Navigate,
  Outlet,
  useLocation,
} from 'react-router-dom'

import { useAuth } from '../auth/AuthContext'

export default function ProtectedRoute() {
  const {
    admin,
    loading,
  } = useAuth()

  const location =
    useLocation()

  /*
  |--------------------------------------------------------------------------
  | Authentication Loading
  |--------------------------------------------------------------------------
  */

  if (loading) {
    return (
      <div
        style={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: '#0b0f19',
          color: '#ffffff',
          fontFamily:
            'Arial, Helvetica, sans-serif',
        }}
      >
        <div
          style={{
            textAlign: 'center',
          }}
        >
          <div
            style={{
              fontSize: '32px',
              fontWeight: '700',
              marginBottom: '10px',
            }}
          >
            SS Platform
            <span
              style={{
                color: '#00e5ff',
              }}
            >
              .
            </span>
          </div>

          <div
            style={{
              color:
                'rgba(255,255,255,0.55)',
              fontSize: '14px',
            }}
          >
            Checking authentication...
          </div>
        </div>
      </div>
    )
  }

  /*
  |--------------------------------------------------------------------------
  | Not Authenticated
  |--------------------------------------------------------------------------
  */

  if (!admin) {
    return (
      <Navigate
        to="/login"
        replace
        state={{
          from: location,
        }}
      />
    )
  }

  /*
  |--------------------------------------------------------------------------
  | Authenticated
  |--------------------------------------------------------------------------
  */

  return <Outlet />
}
