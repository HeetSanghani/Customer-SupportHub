import axios from 'axios'
import { useAuthStore } from '../store/authStore'

let rawApiUrl = (import.meta.env.VITE_API_URL || '').trim()
if (rawApiUrl && !rawApiUrl.includes('.')) {
  rawApiUrl = `${rawApiUrl}.onrender.com`
}
const normalizedApiUrl = rawApiUrl
  ? (rawApiUrl.startsWith('http') ? rawApiUrl : `https://${rawApiUrl}`).replace(/\/+$/, '')
  : ''
const API_BASE = normalizedApiUrl ? `${normalizedApiUrl}/api/v1` : '/api/v1'

const client = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
})


// Attach JWT Bearer token to every request
client.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

// 401 -> silent refresh or redirect to login
client.interceptors.response.use(
  (res) => res,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry && !originalRequest.url?.includes('/auth/login') && !originalRequest.url?.includes('/auth/refresh')) {
      const { refreshToken, setToken, logout } = useAuthStore.getState()

      if (!refreshToken) {
        logout()
        if (window.location.pathname !== '/login') {
          window.location.href = '/login'
        }
        return Promise.reject(error)
      }

      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`
            return client(originalRequest)
          })
          .catch((err) => Promise.reject(err))
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        const response = await axios.post(`${API_BASE}/auth/refresh`, { refresh_token: refreshToken })
        const { access_token, refresh_token: newRefreshToken } = response.data

        setToken(access_token, newRefreshToken)
        originalRequest.headers.Authorization = `Bearer ${access_token}`
        processQueue(null, access_token)
        return client(originalRequest)
      } catch (refreshErr) {
        processQueue(refreshErr, null)
        logout()
        if (window.location.pathname !== '/login') {
          window.location.href = '/login'
        }
        return Promise.reject(refreshErr)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)

export default client
