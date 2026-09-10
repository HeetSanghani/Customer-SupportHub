import { useState } from 'react'
import { Routes, Route, Navigate, Link, useLocation } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'
import {
  LayoutDashboard, BarChart3, Users, ShieldAlert, FileText,
  GitBranch, BookOpen, Inbox, Clock, CheckCircle
} from 'lucide-react'

import KnowledgeBase from './KnowledgeBase'
import ManagerOverview from './ManagerOverview'
import UnifiedInbox from '../../components/UnifiedInbox'
import WhatsAppInbox from '../../components/WhatsAppInbox'
import EmailInbox from '../../components/EmailInbox'
import InstagramInbox from '../../components/InstagramInbox'
import FacebookInbox from '../../components/FacebookInbox'
import TicketDetail from '../../components/TicketDetail'
import ManagerAnalytics from './ManagerAnalytics'
import ManagerAgentPerformance from './ManagerAgentPerformance'
import ManagerSLADashboard from './ManagerSLADashboard'
import ManagerTicketReports from './ManagerTicketReports'
import ManagerWorkflowAutomation from './ManagerWorkflowAutomation'
import ManagerHeader from '../../components/ManagerHeader'
import StaffProfile from '../../components/StaffProfile'
import StaffSecurity from '../../components/StaffSecurity'

export default function ManagerLayout() {
  const { role, isAuthenticated } = useAuthStore()
  const location = useLocation()
  const [inboxExpanded] = useState(true)

  if (!isAuthenticated || (role !== 'manager' && role !== 'admin')) {
    return <Navigate to="/login" replace />
  }

  const isInboxActive = location.pathname.startsWith('/manager/inbox') || location.pathname.startsWith('/manager/tickets')

  const navLink = (to, icon, label, exact = false) => {
    const Icon = icon
    const isActive = exact ? location.pathname === to : location.pathname.startsWith(to)
    return (
      <Link
        to={to}
        className={`flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-bold transition-all ${
          isActive
            ? 'bg-[#6366F1] text-white shadow-md shadow-indigo-500/20'
            : 'text-[#9598B0] hover:bg-white/5 hover:text-white'
        }`}
      >
        <Icon size={16} />
        {label}
      </Link>
    )
  }

  return (
    <div className="flex h-screen bg-[#F6F7FC] overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 bg-[#1C1B2E] flex flex-col text-white z-20 shrink-0 shadow-lg">

        {/* Brand */}
        <div className="p-5 flex items-center justify-between border-b border-white/10">
          <Link to="/manager" className="flex items-center gap-2.5 group">
            <div
              className="w-9 h-9 rounded-xl flex items-center justify-center text-white font-extrabold text-sm shadow-md transition-transform group-hover:scale-105"
              style={{ background: 'linear-gradient(135deg,#6366F1 0%,#A855F7 100%)' }}
            >
              S
            </div>
            <div>
              <div className="font-bold tracking-tight leading-none text-base" style={{ fontFamily: 'Plus Jakarta Sans, sans-serif' }}>
                SupportHub
              </div>
              <div className="text-[9px] text-[#9598B0] uppercase tracking-widest mt-1">Manager Dashboard</div>
            </div>
          </Link>
        </div>

        {/* Nav */}
        <nav className="flex-1 px-3.5 space-y-1 mt-4 overflow-y-auto">

          {/* Overview */}
          <div className="text-[9px] font-extrabold text-[#9598B0] uppercase tracking-wider px-3 mb-1.5">
            Workspace
          </div>

          {navLink('/manager', LayoutDashboard, 'Overview', true)}

          {/* Insights */}
          <div className="text-[9px] font-extrabold text-[#9598B0] uppercase tracking-wider px-3 pt-3 mb-1.5">
            Insights
          </div>

          {navLink('/manager/analytics', BarChart3, 'Analytics')}
          {navLink('/manager/agent-performance', Users, 'Agent Performance')}
          {navLink('/manager/sla-dashboard', ShieldAlert, 'SLA Dashboard')}
          {navLink('/manager/reports', FileText, 'Ticket Reports')}
          {navLink('/manager/workflow', GitBranch, 'Workflow Automation Engine')}

          {/* Team Inbox Accordion */}
          <div className="text-[9px] font-extrabold text-[#9598B0] uppercase tracking-wider px-3 pt-3 mb-1.5">
            Operations
          </div>

          <div>
            <div className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-bold ${
              isInboxActive ? 'bg-[#6366F1] text-white shadow-md shadow-indigo-500/20' : 'text-[#9598B0]'
            }`}>
              <div className="flex items-center gap-2.5">
                <Inbox size={16} /> Team Inbox
              </div>
            </div>

            {inboxExpanded && (
              <div className="pl-6 pr-1 py-1 space-y-0.5 mt-0.5">
                <Link
                  to="/manager/inbox/active"
                  className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                    location.pathname === '/manager/inbox/active'
                      ? 'bg-white/10 text-white'
                      : 'text-[#9598B0] hover:bg-white/5 hover:text-white'
                  }`}
                >
                  <Clock size={13} /> Active Tickets
                </Link>
                <Link
                  to="/manager/inbox/closed"
                  className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                    location.pathname === '/manager/inbox/closed'
                      ? 'bg-white/10 text-white'
                      : 'text-[#9598B0] hover:bg-white/5 hover:text-white'
                  }`}
                >
                  <CheckCircle size={13} /> Closed Tickets
                </Link>
                <Link
                  to="/manager/inbox/all"
                  className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                    location.pathname === '/manager/inbox/all' || location.pathname === '/manager/inbox'
                      ? 'bg-white/10 text-white'
                      : 'text-[#9598B0] hover:bg-white/5 hover:text-white'
                  }`}
                >
                  <Inbox size={13} /> All Tickets
                </Link>
              </div>
            )}
          </div>

          {navLink('/manager/knowledge', BookOpen, 'Knowledge Base')}
        </nav>

        {/* Bottom spacer */}
        <div className="h-4" />
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 h-screen overflow-hidden">
        <ManagerHeader />

        <div className="flex-1 overflow-y-auto">
          <Routes>
            <Route path="/" element={<ManagerOverview />} />
            <Route path="/profile" element={<StaffProfile basePath="/manager" />} />
            <Route path="/security" element={<StaffSecurity basePath="/manager" />} />
            <Route path="/whatsapp" element={<WhatsAppInbox basePath="/manager" />} />
            <Route path="/instagram" element={<InstagramInbox basePath="/manager" />} />
            <Route path="/facebook" element={<FacebookInbox basePath="/manager" />} />
            <Route path="/email" element={<EmailInbox basePath="/manager" />} />
            <Route path="/inbox" element={<UnifiedInbox filter="all" basePath="/manager" />} />
            <Route path="/inbox/all" element={<UnifiedInbox filter="all" basePath="/manager" />} />
            <Route path="/inbox/live" element={<Navigate to="/manager/inbox/active" replace />} />
            <Route path="/inbox/active" element={<UnifiedInbox filter="active" basePath="/manager" />} />
            <Route path="/inbox/closed" element={<UnifiedInbox filter="closed" basePath="/manager" />} />
            <Route path="/tickets/:id" element={<TicketDetail basePath="/manager" />} />
            <Route path="/analytics" element={<ManagerAnalytics />} />
            <Route path="/agent-performance" element={<ManagerAgentPerformance />} />
            <Route path="/sla-dashboard" element={<ManagerSLADashboard />} />
            <Route path="/reports" element={<ManagerTicketReports />} />
            <Route path="/workflow" element={<ManagerWorkflowAutomation />} />
            <Route path="/knowledge/*" element={<KnowledgeBase />} />
            <Route path="*" element={<Navigate to="/manager" replace />} />
          </Routes>
        </div>
      </main>
    </div>
  )
}
