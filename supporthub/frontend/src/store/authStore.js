import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useAuthStore = create(
  persist(
    (set) => ({
      token: null,
      userId: null,
      role: null,
      name: null,
      isAuthenticated: false,

      login: (token, userId, role, name) =>
        set({ token, userId, role, name, isAuthenticated: true }),

      setRole: (role) => set({ role }),

      logout: () =>
        set({ token: null, userId: null, role: null, name: null, isAuthenticated: false }),
    }),
    { name: 'supporthub-auth' }
  )
)
