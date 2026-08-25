# 16 - Frontend Authentication Audit

## Architecture Overview
- **Framework**: React 18 + Vite
- **State Management**: Zustand with `persist` middleware (`store/authStore.js`)
- **HTTP Client**: Axios with interceptors (`api/client.js`)
- **Storage**: `localStorage` (Key: `supporthub-auth`)

## Key Frontend Auth Components

### 1. State Store (`store/authStore.js`)
```javascript
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
        set((state) => ({ token, refreshToken: refreshToken || state.refreshToken })),

      logout: () =>
        set({ token: null, refreshToken: null, userId: null, role: null, name: null, isAuthenticated: false }),
    }),
    { name: 'supporthub-auth' }
  )
)
```

### 2. Axios Request & Response Interceptors (`api/client.js`)
- **Request Interceptor**: Reads JWT `token` from `useAuthStore` and automatically injects header: `Authorization: Bearer <token>`.
- **Response Interceptor (401 Handling)**:
  - If a request returns `401 Unauthorized` and a `refreshToken` exists, pauses request queue, executes `POST /api/v1/auth/refresh`, updates tokens, and retries original request.
  - If refresh fails or no refresh token exists, executes `logout()` and redirects browser to `/login`.

### 3. Route Protection & Guest Rendering
- Protected dashboard views inspect `useAuthStore.getState().role`.
- Customer views display customer live chat widget and personal ticket list.
- Unauthenticated users entering public routes can use guest chat widget.
