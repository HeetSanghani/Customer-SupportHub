import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useAuthStore } from './store/authStore'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import CustomerLayout from './pages/customer/CustomerLayout'
import AgentLayout from './pages/agent/AgentLayout'
import ManagerLayout from './pages/manager/ManagerLayout'
import AdminLayout from './pages/admin/AdminLayout'
import './index.css'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      retry: 1,
    },
  },
})

function RoleRouter() {
  const { isAuthenticated, role } = useAuthStore()

  if (!isAuthenticated) return <Navigate to="/login" replace />

  if (role === 'customer') return <Navigate to="/customer" replace />
  if (role === 'agent') return <Navigate to="/agent" replace />
  if (role === 'manager') return <Navigate to="/manager" replace />
  if (role === 'admin') return <Navigate to="/admin" replace />

  return <Navigate to="/login" replace />
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<RoleRouter />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/customer/*" element={<CustomerLayout />} />
          <Route path="/agent/*" element={<AgentLayout />} />
          <Route path="/manager/*" element={<ManagerLayout />} />
          <Route path="/admin/*" element={<AdminLayout />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
