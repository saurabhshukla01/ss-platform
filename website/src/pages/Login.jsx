import { useEffect, useState } from 'react'

import {
  useLocation,
  useNavigate,
} from 'react-router-dom'

import { useAuth } from '../auth/AuthContext'

const STATIC_ADMIN_ENABLED =
  import.meta.env.VITE_ENABLE_STATIC_ADMIN ===
  'true'

const STATIC_ADMIN_EMAIL =
  import.meta.env.VITE_STATIC_ADMIN_EMAIL || ''

const STATIC_ADMIN_PASSWORD =
  import.meta.env.VITE_STATIC_ADMIN_PASSWORD || ''

export default function Login() {
  const {
    login,
    admin,
    loading: authLoading,
  } = useAuth()

  const navigate =
    useNavigate()

  const location =
    useLocation()

  const [email, setEmail] =
    useState('')

  const [password, setPassword] =
    useState('')

  const [error, setError] =
    useState('')

  const [loading, setLoading] =
    useState(false)

  /*
  |--------------------------------------------------------------------------
  | Already Logged In
  |--------------------------------------------------------------------------
  */

  useEffect(() => {
    if (!authLoading && admin) {
      navigate('/admin', {
        replace: true,
      })
    }
  }, [
    admin,
    authLoading,
    navigate,
  ])

  /*
  |--------------------------------------------------------------------------
  | Login Submit
  |--------------------------------------------------------------------------
  */

  async function handleSubmit(event) {
    event.preventDefault()

    setError('')
    setLoading(true)

    try {
      await login(
        email,
        password,
      )

      const destination =
        location.state?.from
          ?.pathname || '/admin'

      navigate(
        destination,
        {
          replace: true,
        },
      )
    } catch (err) {
      console.error(
        'Login failed:',
        err,
      )

      const detail =
        err?.response?.data
          ?.detail

      if (
        typeof detail ===
        'string'
      ) {
        setError(detail)
      } else {
        setError(
          'Incorrect email or password.',
        )
      }
    } finally {
      setLoading(false)
    }
  }

  /*
  |--------------------------------------------------------------------------
  | Development Login
  |--------------------------------------------------------------------------
  */

  function useDevelopmentLogin() {
    setEmail(
      STATIC_ADMIN_EMAIL,
    )

    setPassword(
      STATIC_ADMIN_PASSWORD,
    )

    setError('')
  }

  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background:
          'linear-gradient(135deg, #070b12 0%, #101827 50%, #070b12 100%)',
        padding: '24px',
        color: '#ffffff',
        fontFamily:
          'Inter, Arial, Helvetica, sans-serif',
      }}
    >
      <div
        style={{
          width: '100%',
          maxWidth: '440px',
        }}
      >
        {/* Brand */}

        <div
          style={{
            textAlign: 'center',
            marginBottom: '28px',
          }}
        >
          <div
            style={{
              fontSize: '32px',
              fontWeight: '800',
              letterSpacing: '-1px',
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
              marginTop: '7px',
              color:
                'rgba(255,255,255,0.5)',
              fontSize: '14px',
            }}
          >
            Technology & Business
            Administration
          </div>
        </div>

        {/* Login Card */}

        <form
          onSubmit={handleSubmit}
          style={{
            background:
              'rgba(18,24,38,0.96)',
            border:
              '1px solid rgba(255,255,255,0.08)',
            borderRadius: '16px',
            padding: '30px',
            boxShadow:
              '0 25px 70px rgba(0,0,0,0.35)',
          }}
        >
          <h1
            style={{
              margin: '0 0 8px',
              fontSize: '23px',
            }}
          >
            Administrator Login
          </h1>

          <p
            style={{
              margin:
                '0 0 25px',
              color:
                'rgba(255,255,255,0.48)',
              fontSize: '13px',
            }}
          >
            Sign in to access your
            administration panel.
          </p>

          {/* Email */}

          <div
            style={{
              marginBottom: '18px',
            }}
          >
            <label
              style={{
                display: 'block',
                marginBottom: '7px',
                color:
                  'rgba(255,255,255,0.7)',
                fontSize: '13px',
                fontWeight: '600',
              }}
            >
              Email
            </label>

            <input
              type="email"
              required
              autoComplete="email"
              value={email}
              onChange={(event) =>
                setEmail(
                  event.target.value,
                )
              }
              placeholder="admin@example.com"
              style={{
                width: '100%',
                boxSizing:
                  'border-box',
                padding:
                  '13px 14px',
                borderRadius: '9px',
                border:
                  '1px solid rgba(255,255,255,0.11)',
                background:
                  '#0a0f19',
                color: '#ffffff',
                outline: 'none',
                fontSize: '14px',
              }}
            />
          </div>

          {/* Password */}

          <div
            style={{
              marginBottom: '18px',
            }}
          >
            <label
              style={{
                display: 'block',
                marginBottom: '7px',
                color:
                  'rgba(255,255,255,0.7)',
                fontSize: '13px',
                fontWeight: '600',
              }}
            >
              Password
            </label>

            <input
              type="password"
              required
              autoComplete="current-password"
              value={password}
              onChange={(event) =>
                setPassword(
                  event.target.value,
                )
              }
              placeholder="Enter your password"
              style={{
                width: '100%',
                boxSizing:
                  'border-box',
                padding:
                  '13px 14px',
                borderRadius: '9px',
                border:
                  '1px solid rgba(255,255,255,0.11)',
                background:
                  '#0a0f19',
                color: '#ffffff',
                outline: 'none',
                fontSize: '14px',
              }}
            />
          </div>

          {/* Error */}

          {error && (
            <div
              style={{
                padding: '12px',
                marginBottom:
                  '18px',
                borderRadius: '9px',
                background:
                  'rgba(239,68,68,0.1)',
                border:
                  '1px solid rgba(239,68,68,0.28)',
                color: '#f87171',
                fontSize: '13px',
                lineHeight: '1.5',
              }}
            >
              {error}
            </div>
          )}

          {/* Submit */}

          <button
            type="submit"
            disabled={loading}
            style={{
              width: '100%',
              padding: '13px',
              border: 'none',
              borderRadius: '9px',
              background:
                'linear-gradient(135deg, #00e5ff, #00b8d4)',
              color: '#031017',
              fontWeight: '800',
              fontSize: '14px',
              cursor: loading
                ? 'not-allowed'
                : 'pointer',
              opacity: loading
                ? 0.65
                : 1,
            }}
          >
            {loading
              ? 'Signing in...'
              : 'Sign in'}
          </button>
        </form>

        {/* Development Login */}

        {STATIC_ADMIN_ENABLED && (
          <div
            style={{
              marginTop: '16px',
              padding: '18px',
              borderRadius: '12px',
              background:
                'rgba(234,179,8,0.07)',
              border:
                '1px solid rgba(234,179,8,0.25)',
            }}
          >
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent:
                  'space-between',
                marginBottom:
                  '16px',
              }}
            >
              <strong
                style={{
                  color: '#facc15',
                  fontSize: '12px',
                  letterSpacing:
                    '0.5px',
                }}
              >
                DEVELOPMENT LOGIN
              </strong>

              <span
                style={{
                  padding:
                    '4px 7px',
                  borderRadius: '5px',
                  background:
                    'rgba(250,204,21,0.1)',
                  color: '#facc15',
                  fontSize: '9px',
                  fontWeight: '700',
                }}
              >
                LOCAL ONLY
              </span>
            </div>

            {/* Static Email */}

            <div
              style={{
                marginBottom:
                  '12px',
              }}
            >
              <div
                style={{
                  color:
                    'rgba(255,255,255,0.4)',
                  fontSize: '10px',
                  marginBottom:
                    '5px',
                  textTransform:
                    'uppercase',
                }}
              >
                Email
              </div>

              <div
                style={{
                  color: '#ffffff',
                  fontFamily:
                    'monospace',
                  fontSize: '12px',
                  wordBreak:
                    'break-all',
                }}
              >
                {STATIC_ADMIN_EMAIL ||
                  'Not configured'}
              </div>
            </div>

            {/* Static Password */}

            <div
              style={{
                marginBottom:
                  '15px',
              }}
            >
              <div
                style={{
                  color:
                    'rgba(255,255,255,0.4)',
                  fontSize: '10px',
                  marginBottom:
                    '5px',
                  textTransform:
                    'uppercase',
                }}
              >
                Password
              </div>

              <div
                style={{
                  color: '#ffffff',
                  fontFamily:
                    'monospace',
                  fontSize: '12px',
                  wordBreak:
                    'break-all',
                }}
              >
                {STATIC_ADMIN_PASSWORD ||
                  'Not configured'}
              </div>
            </div>

            <button
              type="button"
              onClick={
                useDevelopmentLogin
              }
              style={{
                width: '100%',
                padding: '10px',
                borderRadius: '8px',
                border:
                  '1px solid rgba(250,204,21,0.3)',
                background:
                  'transparent',
                color: '#facc15',
                fontWeight: '700',
                cursor: 'pointer',
                fontSize: '12px',
              }}
            >
              Use Development Login
            </button>
          </div>
        )}

        {/* Footer */}

        <div
          style={{
            textAlign: 'center',
            marginTop: '20px',
            color:
              'rgba(255,255,255,0.3)',
            fontSize: '11px',
          }}
        >
          SS Platform Administration
        </div>
      </div>
    </div>
  )
}