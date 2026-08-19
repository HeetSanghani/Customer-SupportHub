import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useAuthStore = create(
  persist(
    (set) => ({
      token: null,
      refreshToken: null,
      userId: null,
      role: null,
      name: null,
      isAuthenticated: false,

      login: (token, userId, role, name, refreshToken = null) =>
        set({ token, refreshToken, userId, role, name, isAuthenticated: true }),

      setToken: (token, refreshToken = null) =>
        set((state) => ({
          token,
          refreshToken: refreshToken || state.refreshToken,
        })),

      setRole: (role) => set({ role }),
      updateUser: (name) => set({ name }),

      logout: () =>
        set({ token: null, refreshToken: null, userId: null, role: null, name: null, isAuthenticated: false }),
    }),
    { name: 'supporthub-auth' }
  )
)
