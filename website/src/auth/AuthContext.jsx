import {
  createContext,
  useContext,
  useEffect,
  useState,
} from 'react'

import api from '../api/client'


const AuthContext =
  createContext(null)


export function AuthProvider({
  children,
}) {

  const [admin, setAdmin] =
    useState(null)

  const [loading, setLoading] =
    useState(true)


  // =======================================================
  // LOAD CURRENT ADMIN
  // =======================================================

  async function loadAdmin() {

    const token =
      localStorage.getItem(
        'access_token'
      )

    if (!token) {
      setAdmin(null)
      setLoading(false)
      return
    }

    try {

      const response =
        await api.get('/auth/me')

      setAdmin(
        response.data
      )

      localStorage.setItem(
        'admin',
        JSON.stringify(
          response.data
        )
      )

    } catch (error) {

      console.error(
        'Failed to load admin:',
        error
      )

      localStorage.removeItem(
        'access_token'
      )

      localStorage.removeItem(
        'admin'
      )

      setAdmin(null)

    } finally {

      setLoading(false)

    }
  }


  // =======================================================
  // INITIAL AUTH CHECK
  // =======================================================

  useEffect(() => {
    loadAdmin()
  }, [])


  // =======================================================
  // LOGIN
  // =======================================================

  async function login(
    email,
    password
  ) {

    if (!email || !password) {
      throw new Error(
        'Email and password are required.'
      )
    }


    // =====================================================
    // FASTAPI OAUTH2 LOGIN
    // =====================================================
    //
    // OAuth2PasswordRequestForm expects:
    //
    // username=<email>
    // password=<password>
    //
    // Content-Type:
    // application/x-www-form-urlencoded
    //
    // =====================================================

    const formData =
      new URLSearchParams()

    formData.append(
      'username',
      email.trim()
    )

    formData.append(
      'password',
      password
    )


    const response =
      await api.post(
        '/auth/login',
        formData,
        {
          headers: {
            'Content-Type':
              'application/x-www-form-urlencoded',
          },
        }
      )


    // =====================================================
    // GET ACCESS TOKEN
    // =====================================================

    const accessToken =
      response.data.access_token


    if (!accessToken) {
      throw new Error(
        'Authentication token was not returned.'
      )
    }


    // =====================================================
    // SAVE ACCESS TOKEN
    // =====================================================

    localStorage.setItem(
      'access_token',
      accessToken
    )


    // =====================================================
    // LOAD LOGGED-IN ADMIN
    // =====================================================

    try {

      const meResponse =
        await api.get(
          '/auth/me'
        )

      const adminData =
        meResponse.data


      // Save admin in React state
      setAdmin(
        adminData
      )


      // Save admin in localStorage
      localStorage.setItem(
        'admin',
        JSON.stringify(
          adminData
        )
      )


      return adminData

    } catch (error) {

      console.error(
        'Failed to load logged-in admin:',
        error
      )


      // ===================================================
      // TOKEN INVALID
      // ===================================================

      localStorage.removeItem(
        'access_token'
      )

      localStorage.removeItem(
        'admin'
      )

      setAdmin(null)

      throw error
    }
  }


  // =======================================================
  // LOGOUT
  // =======================================================

  function logout() {

    localStorage.removeItem(
      'access_token'
    )

    localStorage.removeItem(
      'admin'
    )

    setAdmin(null)
  }


  // =======================================================
  // PROVIDER VALUE
  // =======================================================

  const value = {
    admin,
    loading,
    login,
    logout,
    isAuthenticated: !!admin,
  }


  // =======================================================
  // AUTH CONTEXT PROVIDER
  // =======================================================

  return (
    <AuthContext.Provider
      value={value}
    >
      {children}
    </AuthContext.Provider>
  )
}


// =========================================================
// USE AUTH HOOK
// =========================================================

export function useAuth() {

  const context =
    useContext(
      AuthContext
    )


  if (!context) {
    throw new Error(
      'useAuth must be used inside AuthProvider'
    )
  }


  return context
}
