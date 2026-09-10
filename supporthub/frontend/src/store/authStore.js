import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { queryClient } from '../api/queryClient'

export const useAuthStore = create(
  persist(
    (set) => ({
      token: null,
      refreshToken: null,
      userId: null,
      id: null,
      role: null,
      name: null,
      isAuthenticated: false,

      login: (token, userId, role, name, refreshToken = null) => {
        try {
          queryClient.clear()
        } catch (e) {
          console.error('Failed to clear query cache on login:', e)
        }
        set({ token, refreshToken, userId, id: userId, role, name, isAuthenticated: true })
      },

      setToken: (token, refreshToken = null) =>
        set((state) => ({
          token,
          refreshToken: refreshToken || state.refreshToken,
        })),

      setRole: (role) => set({ role }),
      updateUser: (name) => set({ name }),

      logout: () => {
        try {
          queryClient.clear()
        } catch (e) {
          console.error('Failed to clear query cache on logout:', e)
        }
        set({ token: null, refreshToken: null, userId: null, role: null, name: null, isAuthenticated: false })
      },
    }),
    { name: 'supporthub-auth' }
  )
)
