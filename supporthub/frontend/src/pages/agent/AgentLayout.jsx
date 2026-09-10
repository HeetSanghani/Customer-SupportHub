import { useState } from 'react'
import { Routes, Route, Navigate, Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'
import { 
  Inbox, CheckCircle, Clock, LogOut, LayoutDashboard, 
  ListFilter, Zap, BookOpen, MessageSquare, Shield, FileText
} from 'lucide-react'

import UnifiedInbox from '../../components/UnifiedInbox'
import WhatsAppInbox from '../../components/WhatsAppInbox'
import EmailInbox from '../../components/EmailInbox'
import InstagramInbox from '../../components/InstagramInbox'
import FacebookInbox from '../../components/FacebookInbox'
import AgentOverview from './AgentOverview'
import AgentTicketQueue from './AgentTicketQueue'
import AgentQuickReplies from './AgentQuickReplies'
import AgentHelpCenter from './AgentHelpCenter'
import AgentProfile from './AgentProfile'
import TicketDetail from '../../components/TicketDetail'
import AgentHeader from '../../components/AgentHeader'
import StaffProfile from '../../components/StaffProfile'
import StaffSecurity from '../../components/StaffSecurity'

export default function AgentLayout() {
  const { role, logout, name, isAuthenticated } = useAuthStore()
  const location = useLocation()
  const navigate = useNavigate()


  if (!isAuthenticated || (role !== 'agent' && role !== 'admin' && role !== 'manager')) {
    return <Navigate to="/login" replace />
  }

  const handleLogout = () => {
    logout()
    navigate('/login', { replace: true })
  }

  const userInitials = name
    ? name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
    : 'EW'

  return (
    <div className="flex h-screen bg-[#F6F7FC] overflow-hidden">
      {/* Modern Dark Sidebar */}
      <aside className="w-64 bg-[#1C1B2E] flex flex-col text-white z-20 shrink-0 shadow-lg">
        {/* Brand Logo & App Header */}
        <div className="p-5 flex items-center justify-between border-b border-white/10">
          <Link to="/agent" className="flex items-center gap-2.5 group">
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
              <div className="text-[9px] text-[#9598B0] uppercase tracking-widest mt-1">AI Omnichannel Platform</div>
            </div>
          </Link>
        </div>

        {/* Sidebar Nav Links */}
        <nav className="flex-1 px-3.5 space-y-1 mt-4 overflow-y-auto">
          {/* MAIN WORKSPACE */}
          <div className="text-[9px] font-extrabold text-[#9598B0] uppercase tracking-wider px-3 mb-1.5">
            Main Workspace
          </div>
          
          <Link 
            to="/agent" 
            className={`flex items-center justify-between px-3 py-2 rounded-xl text-xs font-bold transition-all ${
              location.pathname === '/agent' ? 'bg-[#6366F1] text-white shadow-md shadow-indigo-500/20' : 'text-[#9598B0] hover:bg-white/5 hover:text-white'
            }`}
          >
            <div className="flex items-center gap-2.5">
              <LayoutDashboard size={16} /> Dashboard
            </div>
          </Link>

          <Link 
            to="/agent/inbox" 
            className={`flex items-center justify-between px-3 py-2 rounded-xl text-xs font-bold transition-all ${
              location.pathname === '/agent/inbox' ? 'bg-[#6366F1] text-white shadow-md shadow-indigo-500/20' : 'text-[#9598B0] hover:bg-white/5 hover:text-white'
            }`}
          >
            <div className="flex items-center gap-2.5">
              <MessageSquare size={16} /> All Tickets
            </div>
          </Link>

          <Link 
            to="/agent/queue" 
            className={`flex items-center justify-between px-3 py-2 rounded-xl text-xs font-bold transition-all ${
              location.pathname === '/agent/queue' ? 'bg-[#6366F1] text-white shadow-md shadow-indigo-500/20' : 'text-[#9598B0] hover:bg-white/5 hover:text-white'
            }`}
          >
            <div className="flex items-center gap-2.5">
              <ListFilter size={16} /> Ticket Queue
            </div>
          </Link>

          {/* KNOWLEDGE & POLICIES SECTION */}
          <div className="text-[9px] font-extrabold text-[#9598B0] uppercase tracking-wider px-3 pt-3 mb-1.5">
            Knowledge & Policies
          </div>

          <Link 
            to="/agent/help-center" 
            className={`flex items-center justify-between px-3 py-2 rounded-xl text-xs font-bold transition-all ${
              location.pathname === '/agent/help-center' ? 'bg-[#6366F1] text-white shadow-md shadow-indigo-500/20' : 'text-[#9598B0] hover:bg-white/5 hover:text-white'
            }`}
          >
            <div className="flex items-center gap-2.5">
              <BookOpen size={16} /> Knowledge Base & Policies
            </div>
          </Link>

          <Link 
            to="/agent/quick-replies" 
            className={`flex items-center justify-between px-3 py-2 rounded-xl text-xs font-bold transition-all ${
              location.pathname === '/agent/quick-replies' ? 'bg-[#6366F1] text-white shadow-md shadow-indigo-500/20' : 'text-[#9598B0] hover:bg-white/5 hover:text-white'
            }`}
          >
            <div className="flex items-center gap-2.5">
              <Zap size={16} /> Quick Replies
            </div>
          </Link>

          {/* STATUS FILTERS */}
          <div className="text-[9px] font-extrabold text-[#9598B0] uppercase tracking-wider px-3 pt-3 mb-1.5">
            Status Filters
          </div>

          <Link 
            to="/agent/active" 
            className={`flex items-center justify-between px-3 py-2 rounded-xl text-xs font-bold transition-all ${
              location.pathname === '/agent/active' ? 'bg-[#6366F1] text-white shadow-md shadow-indigo-500/20' : 'text-[#9598B0] hover:bg-white/5 hover:text-white'
            }`}
          >
            <div className="flex items-center gap-2.5">
              <Clock size={16} /> Active Tickets
            </div>
          </Link>

          <Link 
            to="/agent/resolved" 
            className={`flex items-center justify-between px-3 py-2 rounded-xl text-xs font-bold transition-all ${
              location.pathname === '/agent/resolved' ? 'bg-[#6366F1] text-white shadow-md shadow-indigo-500/20' : 'text-[#9598B0] hover:bg-white/5 hover:text-white'
            }`}
          >
            <div className="flex items-center gap-2.5">
              <CheckCircle size={16} /> Total Resolved
            </div>
          </Link>
        </nav>
        
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col min-w-0 h-screen overflow-hidden">
        <AgentHeader />
        
        <div className="flex-1 overflow-y-auto">
          <Routes>
            <Route path="/" element={<AgentOverview />} />
            <Route path="/profile" element={<StaffProfile basePath="/agent" />} />
            <Route path="/security" element={<StaffSecurity basePath="/agent" />} />
            <Route path="/agent-profile" element={<AgentProfile />} />
            <Route path="/whatsapp" element={<WhatsAppInbox basePath="/agent" />} />
            <Route path="/instagram" element={<InstagramInbox basePath="/agent" />} />
            <Route path="/facebook" element={<FacebookInbox basePath="/agent" />} />
            <Route path="/email" element={<EmailInbox basePath="/agent" />} />
            <Route path="/inbox" element={<UnifiedInbox filter="all" basePath="/agent" />} />
            <Route path="/active" element={<UnifiedInbox filter="active" basePath="/agent" />} />
            <Route path="/queue" element={<AgentTicketQueue />} />
            <Route path="/quick-replies" element={<AgentQuickReplies />} />
            <Route path="/help-center" element={<AgentHelpCenter />} />
            <Route path="/resolved" element={<UnifiedInbox filter="resolved" basePath="/agent" />} />
            <Route path="/tickets/:id" element={<TicketDetail basePath="/agent" />} />
            <Route path="*" element={<Navigate to="/agent" replace />} />
          </Routes>
        </div>
      </main>
    </div>
  )
}
