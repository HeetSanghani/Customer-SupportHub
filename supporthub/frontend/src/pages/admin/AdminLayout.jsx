import { Routes, Route, Navigate, Link } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'
import { useQuery } from '@tanstack/react-query'
import { authApi } from '../../api/auth'
import { Users, Shield, LogOut, Inbox, LayoutDashboard } from 'lucide-react'
import UnifiedInbox from '../../components/UnifiedInbox'
import TicketDetail from '../../components/TicketDetail'
import AdminOverview from './AdminOverview'

// ─── Users View ──────────────────────────────────────────────────────────────
function UserDirectory() {
  const { data: users, isLoading } = useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const res = await authApi.listUsers()
      return res.data
    }
  })

  return (
    <div className="flex-1 p-8 overflow-auto">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-2xl font-bold text-[#1C1B2E] mb-1" style={{ fontFamily: 'Plus Jakarta Sans, sans-serif' }}>User Directory</h1>
          <p className="text-sm text-[#6C7089]">Manage roles, permissions, and accounts across the platform.</p>
        </div>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-10"><div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div></div>
      ) : (
        <div className="bg-white rounded-xl border border-[#E5E7F3] overflow-hidden shadow-sm">
          <table className="w-full text-left text-sm text-[#6C7089]">
            <thead className="bg-[#F9FAFB] border-b border-[#E5E7F3] text-xs uppercase font-bold text-[#9598B0]">
              <tr>
                <th className="px-6 py-4">Name & Email</th>
                <th className="px-6 py-4">Role</th>
                <th className="px-6 py-4">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E5E7F3]">
              {users?.map(user => (
                <tr key={user.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center font-bold">
                        {user.name.charAt(0)}
                      </div>
                      <div>
                        <div className="font-bold text-[#1C1B2E]">{user.name}</div>
                        <div className="text-xs text-[#9598B0]">{user.email}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`px-2.5 py-1 rounded-md text-xs font-bold uppercase ${
                      user.role === 'admin' ? 'bg-purple-100 text-purple-700' :
                      user.role === 'manager' ? 'bg-blue-100 text-blue-700' :
                      user.role === 'agent' ? 'bg-green-100 text-green-700' :
                      'bg-gray-100 text-gray-700'
                    }`}>
                      {user.role}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className={`w-2 h-2 rounded-full ${user.status === 'active' ? 'bg-green-500' : 'bg-red-500'}`}></div>
                      <span className="capitalize font-medium">{user.status}</span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

// ─── Layout ──────────────────────────────────────────────────────────────────
import { useLocation } from 'react-router-dom'

export default function AdminLayout() {
  const { role, logout, name } = useAuthStore()
  const location = useLocation()
  
  if (role !== 'admin') return <Navigate to="/" replace />
  
  return (
    <div className="flex h-screen bg-[#F6F7FC] overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 bg-[#111827] flex flex-col text-white">
        <div className="p-6 flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg flex items-center justify-center text-white font-bold text-xs" style={{ background: 'linear-gradient(135deg,#6366F1 0%,#A855F7 100%)' }}>S</div>
          <div className="font-bold tracking-tight" style={{ fontFamily: 'Plus Jakarta Sans, sans-serif' }}>Admin Console</div>
        </div>
        
        <nav className="flex-1 px-4 space-y-2 mt-4">
          <Link to="/admin" className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-semibold transition-colors ${location.pathname === '/admin' ? 'bg-white/10 text-white' : 'text-[#9598B0] hover:bg-white/5'}`}>
            <LayoutDashboard size={18} /> Overview
          </Link>
          <Link to="/admin/directory" className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-semibold transition-colors ${location.pathname.startsWith('/admin/directory') ? 'bg-white/10 text-white' : 'text-[#9598B0] hover:bg-white/5'}`}>
            <Users size={18} /> Directory
          </Link>
          <Link to="/admin/inbox" className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-semibold transition-colors ${location.pathname.startsWith('/admin/inbox') || location.pathname.startsWith('/admin/tickets') ? 'bg-white/10 text-white' : 'text-[#9598B0] hover:bg-white/5'}`}>
            <Inbox size={18} /> Global Inbox
          </Link>
          <div className="flex items-center gap-3 px-3 py-2.5 text-[#9598B0] opacity-50 cursor-not-allowed rounded-lg text-sm font-semibold">
            <Shield size={18} /> Security (Soon)
          </div>
        </nav>
        
        <div className="p-4 border-t border-white/10">
          <div className="flex items-center justify-between">
            <div className="text-sm font-semibold truncate">{name}</div>
            <button onClick={logout} className="text-[#9598B0] hover:text-white p-1.5 rounded-md hover:bg-white/10 transition-colors" title="Log out">
              <LogOut size={16} />
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col min-w-0">
        <Routes>
          <Route path="/" element={<AdminOverview />} />
          <Route path="/directory" element={<UserDirectory />} />
          <Route path="/inbox" element={<UnifiedInbox filter="all" basePath="/admin" />} />
          <Route path="/tickets/:id" element={<TicketDetail basePath="/admin" />} />
          <Route path="*" element={<Navigate to="/admin" replace />} />
        </Routes>
      </main>
    </div>
  )
}
