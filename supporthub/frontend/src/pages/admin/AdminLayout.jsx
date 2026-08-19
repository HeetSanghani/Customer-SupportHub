import { Routes, Route, Navigate, Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'
import {
  LayoutDashboard,
  Users,
  Link2,
  BookOpen,
  Bot,
  ShieldCheck,
  Sliders,
  Inbox,
  LogOut
} from 'lucide-react'

import UnifiedInbox from '../../components/UnifiedInbox'
import WhatsAppInbox from '../../components/WhatsAppInbox'
import EmailInbox from '../../components/EmailInbox'
import InstagramInbox from '../../components/InstagramInbox'
import FacebookInbox from '../../components/FacebookInbox'
import TicketDetail from '../../components/TicketDetail'
import AdminOverview from './AdminOverview'
import UserManagement from './UserManagement'
import ChannelIntegrations from './ChannelIntegrations'
import HelpCenterMgmt from './HelpCenterMgmt'
import AISettings from './AISettings'
import RolesPermissions from './RolesPermissions'
import SystemSettings from './SystemSettings'
import { Smartphone, Mail, Instagram, Facebook } from 'lucide-react'

export default function AdminLayout() {
  const { role, logout, name, setRole, isAuthenticated } = useAuthStore()
  const location = useLocation()
  const navigate = useNavigate()

  // Redirect to login if not authenticated
  if (!isAuthenticated) return <Navigate to="/login" replace />

  const handleLogout = () => {
    logout()
    navigate('/login', { replace: true })
  }

  const handleRoleChange = (newRole) => {
    setRole(newRole)
    if (newRole === 'manager') navigate('/manager')
    else if (newRole === 'agent') navigate('/agent')
    else if (newRole === 'customer') navigate('/customer')
    else navigate('/admin')
  }

  const navItems = [
    { label: 'Dashboard', path: '/admin', icon: LayoutDashboard, exact: true },
    { label: 'WhatsApp Inbox', path: '/admin/whatsapp', icon: Smartphone },
    { label: 'Instagram Inbox', path: '/admin/instagram', icon: Instagram },
    { label: 'Facebook Inbox', path: '/admin/facebook', icon: Facebook },
    { label: 'Email Inbox', path: '/admin/email', icon: Mail },
    { label: 'User Management', path: '/admin/users', icon: Users },
    { label: 'Channel Integrations', path: '/admin/channels', icon: Link2 },
    { label: 'Help Center Mgmt', path: '/admin/help-center', icon: BookOpen },
    { label: 'AI Settings', path: '/admin/ai-settings', icon: Bot },
    { label: 'Roles & Permissions', path: '/admin/roles', icon: ShieldCheck },
    { label: 'System Settings', path: '/admin/settings', icon: Sliders },
    { label: 'Global Inbox', path: '/admin/inbox', icon: Inbox },
  ]

  return (
    <div className="flex h-screen bg-[#F6F7FC] overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 bg-white flex flex-col text-[#1C1B2E] border-r border-[#E5E7F3] z-20">
        {/* Header Branding */}
        <div className="p-6 flex items-center gap-3 border-b border-[#F3F4F6]">
          <div
            className="w-8 h-8 rounded-xl flex items-center justify-center text-white font-bold text-sm shadow-md"
            style={{ background: 'linear-gradient(135deg, #6366F1 0%, #A855F7 100%)' }}
          >
            S
          </div>
          <div>
            <div className="font-bold text-sm leading-tight font-['Plus_Jakarta_Sans']">SupportHub</div>
            <div className="text-[11px] text-[#9598B0] font-medium">AI Omnichannel Platform</div>
          </div>
        </div>

        {/* Viewing As Dropdown */}
        <div className="p-4 border-b border-[#F3F4F6]">
          <div className="bg-[#F6F7FC] p-2.5 rounded-xl border border-[#E5E7F3]">
            <div className="text-[10px] font-bold text-[#9598B0] uppercase tracking-wider mb-1">
              Demo — Viewing As
            </div>
            <select
              value={role || 'admin'}
              onChange={(e) => handleRoleChange(e.target.value)}
              className="w-full bg-white border border-[#E5E7F3] rounded-lg px-2.5 py-1 text-xs font-bold text-[#1C1B2E] focus:outline-none focus:border-indigo-500 cursor-pointer"
            >
              <option value="admin">Admin</option>
              <option value="manager">Manager</option>
              <option value="agent">Agent</option>
              <option value="customer">Customer</option>
            </select>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="flex-1 px-4 space-y-1.5 mt-4 overflow-y-auto">
          <div className="px-3 pb-2 text-[10px] font-bold text-[#9598B0] uppercase tracking-wider">
            Administration
          </div>
          {navItems.map((item) => {
            const isActive = item.exact
              ? location.pathname === item.path
              : location.pathname.startsWith(item.path)
            const Icon = item.icon

            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold transition-all ${
                  isActive
                    ? 'bg-[#EEF2FF] text-[#4F46E5]'
                    : 'text-[#6C7089] hover:bg-gray-50 hover:text-[#1C1B2E]'
                }`}
              >
                <Icon size={18} className={isActive ? 'text-[#4F46E5]' : 'text-[#9598B0]'} />
                <span>{item.label}</span>
              </Link>
            )
          })}
        </nav>

        {/* Bottom User Info & Logout */}
        <div className="p-4 border-t border-[#F3F4F6] bg-white">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5 min-w-0">
              <div className="w-8 h-8 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold text-xs shadow-sm">
                {name ? name.charAt(0).toUpperCase() : 'A'}
              </div>
              <div className="min-w-0">
                <div className="text-xs font-bold text-[#1C1B2E] truncate">{name || 'Admin User'}</div>
                <div className="text-[10px] text-[#9598B0] font-medium capitalize">{role || 'admin'}</div>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="text-[#9598B0] hover:text-red-600 p-1.5 rounded-lg hover:bg-red-50 transition-colors"
              title="Log out"
            >
              <LogOut size={16} />
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <Routes>
          <Route path="/" element={<AdminOverview />} />
          <Route path="/whatsapp" element={<WhatsAppInbox basePath="/admin" />} />
          <Route path="/instagram" element={<InstagramInbox basePath="/admin" />} />
          <Route path="/facebook" element={<FacebookInbox basePath="/admin" />} />
          <Route path="/email" element={<EmailInbox basePath="/admin" />} />
          <Route path="/users" element={<UserManagement />} />
          <Route path="/directory" element={<UserManagement />} />
          <Route path="/channels" element={<ChannelIntegrations />} />
          <Route path="/help-center" element={<HelpCenterMgmt />} />
          <Route path="/ai-settings" element={<AISettings />} />
          <Route path="/roles" element={<RolesPermissions />} />
          <Route path="/settings" element={<SystemSettings />} />
          <Route path="/inbox" element={<UnifiedInbox filter="all" basePath="/admin" />} />
          <Route path="/tickets/:id" element={<TicketDetail basePath="/admin" />} />
          <Route path="*" element={<Navigate to="/admin" replace />} />
        </Routes>
      </main>
    </div>
  )
}
