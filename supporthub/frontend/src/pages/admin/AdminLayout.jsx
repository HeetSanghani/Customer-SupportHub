import { useState } from 'react'
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
  Clock,
  CheckCircle,
  ChevronDown
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
import AdminHeader from '../../components/AdminHeader'
import StaffProfile from '../../components/StaffProfile'
import StaffSecurity from '../../components/StaffSecurity'

export default function AdminLayout() {
  const { role, isAuthenticated } = useAuthStore()
  const location = useLocation()
  const navigate = useNavigate()
  const isInboxActive = location.pathname.startsWith('/admin/inbox') || location.pathname.startsWith('/admin/tickets')
  const [inboxExpanded, setInboxExpanded] = useState(true)

  // Redirect to login if not authenticated
  if (!isAuthenticated) return <Navigate to="/login" replace />

  const navItems = [
    { label: 'Dashboard', path: '/admin', icon: LayoutDashboard, exact: true },
    { label: 'User Management', path: '/admin/users', icon: Users },
    { label: 'Channel Integrations', path: '/admin/channels', icon: Link2 },
    { label: 'Help Center Management', path: '/admin/help-center', icon: BookOpen },
    { label: 'AI Settings', path: '/admin/ai-settings', icon: Bot },
    { label: 'Roles & Permissions', path: '/admin/roles', icon: ShieldCheck },
    { label: 'System Settings', path: '/admin/settings', icon: Sliders },
  ]

  return (
    <div className="flex h-screen bg-[#F6F7FC] overflow-hidden">
      {/* Modern Dark Sidebar (matching Manager role) */}
      <aside className="w-64 bg-[#1C1B2E] flex flex-col text-white z-20 shrink-0 shadow-lg">
        {/* Header Branding */}
        <div className="p-5 flex items-center justify-between border-b border-white/10">
          <Link to="/admin" className="flex items-center gap-2.5 group">
            <div
              className="w-9 h-9 rounded-xl flex items-center justify-center text-white font-extrabold text-sm shadow-md transition-transform group-hover:scale-105"
              style={{ background: 'linear-gradient(135deg, #6366F1 0%, #A855F7 100%)' }}
            >
              S
            </div>
            <div>
              <div className="font-bold tracking-tight leading-none text-base" style={{ fontFamily: 'Plus Jakarta Sans, sans-serif' }}>
                SupportHub
              </div>
              <div className="text-[9px] text-[#9598B0] uppercase tracking-widest mt-1">Admin Dashboard</div>
            </div>
          </Link>
        </div>

        {/* Navigation Items */}
        <nav className="flex-1 px-3.5 space-y-1 mt-4 overflow-y-auto">
          <div className="text-[9px] font-extrabold text-[#9598B0] uppercase tracking-wider px-3 mb-1.5">
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
                className={`flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-bold transition-all ${
                  isActive
                    ? 'bg-[#6366F1] text-white shadow-md shadow-indigo-500/20'
                    : 'text-[#9598B0] hover:bg-white/5 hover:text-white'
                }`}
              >
                <Icon size={16} />
                <span>{item.label}</span>
              </Link>
            )
          })}

          {/* Global Inbox Accordion */}
          <div className="pt-2">
            <div className="text-[9px] font-extrabold text-[#9598B0] uppercase tracking-wider px-3 mb-1.5">
              Operations
            </div>

            <div>
              <button
                type="button"
                onClick={() => setInboxExpanded(!inboxExpanded)}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer select-none ${
                  isInboxActive
                    ? 'bg-[#6366F1] text-white shadow-md shadow-indigo-500/20'
                    : 'text-[#9598B0] hover:bg-white/5 hover:text-white'
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <Inbox size={16} />
                  <span>Global Inbox</span>
                </div>
                <ChevronDown
                  size={14}
                  className={`text-white/70 transition-transform duration-200 ${inboxExpanded ? 'rotate-180' : ''}`}
                />
              </button>

              {inboxExpanded && (
                <div className="pl-6 pr-1 py-1 space-y-0.5 mt-0.5">
                  <Link
                    to="/admin/inbox/active"
                    className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                      location.pathname === '/admin/inbox/active'
                        ? 'bg-white/10 text-white font-bold'
                        : 'text-[#9598B0] hover:bg-white/5 hover:text-white'
                    }`}
                  >
                    <Clock size={13} />
                    <span>Active Tickets</span>
                  </Link>

                  <Link
                    to="/admin/inbox/closed"
                    className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                      location.pathname === '/admin/inbox/closed'
                        ? 'bg-white/10 text-white font-bold'
                        : 'text-[#9598B0] hover:bg-white/5 hover:text-white'
                    }`}
                  >
                    <CheckCircle size={13} />
                    <span>Closed Tickets</span>
                  </Link>

                  <Link
                    to="/admin/inbox/all"
                    className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                      location.pathname === '/admin/inbox/all' || location.pathname === '/admin/inbox'
                        ? 'bg-white/10 text-white font-bold'
                        : 'text-[#9598B0] hover:bg-white/5 hover:text-white'
                    }`}
                  >
                    <Inbox size={13} />
                    <span>All Tickets</span>
                  </Link>
                </div>
              )}
            </div>
          </div>
        </nav>

        {/* Bottom spacer */}
        <div className="h-4" />
      </aside>

      {/* Main Content Area with Header */}
      <main className="flex-1 flex flex-col min-w-0 h-screen overflow-hidden">
        <AdminHeader />

        <div className="flex-1 overflow-y-auto">
          <Routes>
            <Route path="/" element={<AdminOverview />} />
            <Route path="/profile" element={<StaffProfile basePath="/admin" />} />
            <Route path="/security" element={<StaffSecurity basePath="/admin" />} />
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
            <Route path="/inbox/all" element={<UnifiedInbox filter="all" basePath="/admin" />} />
            <Route path="/inbox/live" element={<Navigate to="/admin/inbox/active" replace />} />
            <Route path="/inbox/active" element={<UnifiedInbox filter="active" basePath="/admin" />} />
            <Route path="/inbox/closed" element={<UnifiedInbox filter="closed" basePath="/admin" />} />
            <Route path="/tickets/:id" element={<TicketDetail basePath="/admin" />} />
            <Route path="*" element={<Navigate to="/admin" replace />} />
          </Routes>
        </div>
      </main>
    </div>
  )
}
