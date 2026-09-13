import axios from 'axios'

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  'http://127.0.0.1:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,

  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },

  timeout: 15000,
})


// =========================================================
// REQUEST INTERCEPTOR
// =========================================================

api.interceptors.request.use(
  (config) => {
    const token =
      localStorage.getItem('access_token')

    if (token) {
      config.headers.Authorization =
        `Bearer ${token}`
    }

    return config
  },

  (error) => {
    return Promise.reject(error)
  }
)


// =========================================================
// RESPONSE INTERCEPTOR
// =========================================================

api.interceptors.response.use(
  (response) => {
    return response
  },

  (error) => {
    if (
      error.response?.status === 401
    ) {
      const requestUrl =
        error.config?.url || ''

      // Don't immediately clear token when
      // the login request itself returns 401.
      if (
        !requestUrl.includes('/auth/login')
      ) {
        localStorage.removeItem(
          'access_token'
        )

        localStorage.removeItem(
          'admin'
        )
      }
    }

    return Promise.reject(error)
  }
)


export default api