import {
  createContext,
  useContext,
  useEffect,
  useState,
} from 'react'

import api, {
  getToken,
  setToken,
} from '../api/client'

/*
|--------------------------------------------------------------------------
| Auth Context
|--------------------------------------------------------------------------
*/

const AuthContext = createContext(null)

/*
|--------------------------------------------------------------------------
| Development Static Login
|--------------------------------------------------------------------------
|
| IMPORTANT:
| VITE_* variables are visible in the browser.
| Use this ONLY for local development.
|
*/

const STATIC_ADMIN_ENABLED =
  import.meta.env.VITE_ENABLE_STATIC_ADMIN === 'true'

const STATIC_ADMIN_EMAIL =
  import.meta.env.VITE_STATIC_ADMIN_EMAIL || ''

const STATIC_ADMIN_PASSWORD =
  import.meta.env.VITE_STATIC_ADMIN_PASSWORD || ''

/*
|--------------------------------------------------------------------------
| Auth Provider
|--------------------------------------------------------------------------
*/

export function AuthProvider({ children }) {
  const [admin, setAdmin] = useState(null)
  const [loading, setLoading] = useState(true)

  /*
  |--------------------------------------------------------------------------
  | Initial Authentication Check
  |--------------------------------------------------------------------------
  */

  useEffect(() => {
    checkAuthentication()
  }, [])

  async function checkAuthentication() {
    try {
      /*
      |--------------------------------------------------------------------------
      | 1. Check JWT
      |--------------------------------------------------------------------------
      */

      const token = getToken()

      if (token) {
        try {
          const response = await api.get('/auth/me')

          setAdmin(response.data)

          return
        } catch (error) {
          console.warn(
            'Existing JWT is invalid:',
            error?.response?.data || error.message,
          )

          setToken(null)
        }
      }

      /*
      |--------------------------------------------------------------------------
      | 2. Check Static Development Login
      |--------------------------------------------------------------------------
      */

      if (STATIC_ADMIN_ENABLED) {
        const storedAdmin =
          localStorage.getItem('static_admin')

        if (storedAdmin) {
          try {
            const parsedAdmin = JSON.parse(
              storedAdmin,
            )

            setAdmin(parsedAdmin)

            return
          } catch (error) {
            console.warn(
              'Invalid static admin session.',
            )

            localStorage.removeItem(
              'static_admin',
            )
          }
        }
      }

      /*
      |--------------------------------------------------------------------------
      | No Authentication
      |--------------------------------------------------------------------------
      */

      setAdmin(null)
    } finally {
      setLoading(false)
    }
  }

  /*
  |--------------------------------------------------------------------------
  | Login
  |--------------------------------------------------------------------------
  */

  async function login(email, password) {
    const cleanEmail = email.trim()

    /*
    |--------------------------------------------------------------------------
    | First Try FastAPI Authentication
    |--------------------------------------------------------------------------
    */

    try {
      const body = new URLSearchParams()

      body.append('username', cleanEmail)
      body.append('password', password)

      const response = await api.post(
        '/auth/login',
        body,
        {
          headers: {
            'Content-Type':
              'application/x-www-form-urlencoded',
          },
        },
      )

      const token =
        response.data?.access_token

      if (!token) {
        throw new Error(
          'FastAPI login succeeded but access_token was not returned.',
        )
      }

      /*
      |--------------------------------------------------------------------------
      | Save JWT
      |--------------------------------------------------------------------------
      */

      setToken(token)

      /*
      |--------------------------------------------------------------------------
      | Remove Static Session
      |--------------------------------------------------------------------------
      */

      localStorage.removeItem(
        'static_admin',
      )

      /*
      |--------------------------------------------------------------------------
      | Get Current Admin
      |--------------------------------------------------------------------------
      */

      const meResponse =
        await api.get('/auth/me')

      setAdmin(meResponse.data)

      return meResponse.data
    } catch (apiError) {
      console.warn(
        'FastAPI login failed:',
        apiError?.response?.data ||
          apiError.message,
      )

      /*
      |--------------------------------------------------------------------------
      | Development Static Login Fallback
      |--------------------------------------------------------------------------
      */

      if (
        STATIC_ADMIN_ENABLED &&
        cleanEmail === STATIC_ADMIN_EMAIL &&
        password === STATIC_ADMIN_PASSWORD
      ) {
        const staticAdmin = {
          id: 'static-admin',
          name: 'SS Platform Admin',
          email: STATIC_ADMIN_EMAIL,
          username: 'admin',
          is_admin: true,
          role: 'super_admin',
          auth_type: 'static',
        }

        /*
        |--------------------------------------------------------------------------
        | Static Session
        |--------------------------------------------------------------------------
        */

        setToken(null)

        localStorage.setItem(
          'static_admin',
          JSON.stringify(staticAdmin),
        )

        setAdmin(staticAdmin)

        return staticAdmin
      }

      /*
      |--------------------------------------------------------------------------
      | No Authentication
      |--------------------------------------------------------------------------
      */

      throw apiError
    }
  }

  /*
  |--------------------------------------------------------------------------
  | Logout
  |--------------------------------------------------------------------------
  */

  function logout() {
    setToken(null)

    localStorage.removeItem(
      'static_admin',
    )

    setAdmin(null)

    window.location.href = '/login'
  }

  /*
  |--------------------------------------------------------------------------
  | Refresh Authentication
  |--------------------------------------------------------------------------
  */

  async function refreshAuth() {
    setLoading(true)

    try {
      await checkAuthentication()
    } finally {
      setLoading(false)
    }
  }

  /*
  |--------------------------------------------------------------------------
  | Context Value
  |--------------------------------------------------------------------------
  */

  const value = {
    admin,
    loading,

    login,
    logout,

    refreshAuth,

    isAuthenticated: Boolean(admin),

    staticLoginEnabled:
      STATIC_ADMIN_ENABLED,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

/*
|--------------------------------------------------------------------------
| useAuth Hook
|--------------------------------------------------------------------------
*/

export function useAuth() {
  const context =
    useContext(AuthContext)

  if (!context) {
    throw new Error(
      'useAuth() must be used inside <AuthProvider>.',
    )
  }

  return context
}
