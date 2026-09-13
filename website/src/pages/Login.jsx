import { useEffect, useState } from 'react'

import {
  useLocation,
  useNavigate,
} from 'react-router-dom'

import { useAuth } from '../auth/AuthContext'


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


  // =======================================================
  // ALREADY LOGGED IN
  // =======================================================

  useEffect(() => {

    if (
      !authLoading &&
      admin
    ) {

      navigate(
        '/admin',
        {
          replace: true,
        }
      )

    }

  }, [
    admin,
    authLoading,
    navigate,
  ])


  // =======================================================
  // LOGIN
  // =======================================================

  async function handleSubmit(
    event
  ) {

    event.preventDefault()

    setError('')
    setLoading(true)


    try {

      await login(
        email,
        password
      )


      const destination =
        location.state?.from?.pathname ||
        '/admin'


      navigate(
        destination,
        {
          replace: true,
        }
      )


    } catch (err) {

      console.error(
        'Login failed:',
        err
      )


      const status =
        err?.response?.status

      const detail =
        err?.response?.data?.detail


      if (
        status === 401
      ) {

        setError(
          'Incorrect email or password.'
        )

      } else if (
        status === 403
      ) {

        setError(
          typeof detail === 'string'
            ? detail
            : 'Your account is disabled.'
        )

      } else if (
        status === 422
      ) {

        setError(
          'Please enter a valid email and password.'
        )

      } else if (
        typeof detail === 'string'
      ) {

        setError(
          detail
        )

      } else {

        setError(
          'Unable to connect to the server. Please try again.'
        )

      }

    } finally {

      setLoading(false)

    }
  }


  // =======================================================
  // UI
  // =======================================================

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

        {/* BRAND */}

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


        {/* LOGIN CARD */}

        <form
          onSubmit={
            handleSubmit
          }

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
              margin:
                '0 0 8px',

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
            Sign in with your admin
            email and password.
          </p>


          {/* EMAIL */}

          <div
            style={{
              marginBottom: '18px',
            }}
          >

            <label
              htmlFor="email"
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
              id="email"

              type="email"

              required

              autoComplete="email"

              value={email}

              onChange={(event) =>
                setEmail(
                  event.target.value
                )
              }

              placeholder="admin@example.com"

              disabled={loading}

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


          {/* PASSWORD */}

          <div
            style={{
              marginBottom: '18px',
            }}
          >

            <label
              htmlFor="password"
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
              id="password"

              type="password"

              required

              autoComplete="current-password"

              value={password}

              onChange={(event) =>
                setPassword(
                  event.target.value
                )
              }

              placeholder="Enter your password"

              disabled={loading}

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


          {/* ERROR */}

          {error && (

            <div
              role="alert"

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


          {/* BUTTON */}

          <button
            type="submit"

            disabled={
              loading ||
              !email ||
              !password
            }

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

              cursor:
                loading
                  ? 'not-allowed'
                  : 'pointer',

              opacity:
                loading
                  ? 0.65
                  : 1,
            }}
          >

            {loading
              ? 'Signing in...'
              : 'Sign in'}

          </button>

        </form>


        {/* FOOTER */}

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