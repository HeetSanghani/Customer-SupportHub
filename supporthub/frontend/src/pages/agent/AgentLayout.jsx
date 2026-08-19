import { useState } from 'react'
import { Routes, Route, Navigate, Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'
import { useQuery } from '@tanstack/react-query'
import { ticketsApi } from '../../api/tickets'
import { Inbox, CheckCircle, Clock, LogOut, Search, Filter, LayoutDashboard, ListFilter, Zap, BookOpen, MessageSquare, Mail, Smartphone, Instagram, Facebook } from 'lucide-react'

import UnifiedInbox from '../../components/UnifiedInbox'
import WhatsAppInbox from '../../components/WhatsAppInbox'
import EmailInbox from '../../components/EmailInbox'
import InstagramInbox from '../../components/InstagramInbox'
import FacebookInbox from '../../components/FacebookInbox'
import AgentOverview from './AgentOverview'
import AgentTicketQueue from './AgentTicketQueue'
import AgentQuickReplies from './AgentQuickReplies'
import AgentHelpCenter from './AgentHelpCenter'
import TicketDetail from '../../components/TicketDetail'

export default function AgentLayout() {
  const { role, logout, name, isAuthenticated } = useAuthStore()
  const location = useLocation()
  const navigate = useNavigate()
  const [agentStatus, setAgentStatus] = useState('online') // 'online' | 'away' | 'offline'
  const [showStatusDropdown, setShowStatusDropdown] = useState(false)

  if (!isAuthenticated || (role !== 'agent' && role !== 'admin' && role !== 'manager')) {
    return <Navigate to="/login" replace />
  }

  const handleLogout = () => {
    logout()
    navigate('/login', { replace: true })
  }

  const getStatusBadge = () => {
    switch (agentStatus) {
      case 'online':
        return <span className="text-[10px] text-emerald-400 font-bold">● Online</span>
      case 'away':
        return <span className="text-[10px] text-amber-400 font-bold">● Away</span>
      case 'offline':
        return <span className="text-[10px] text-gray-400 font-bold">● Offline</span>
      default:
        return <span className="text-[10px] text-emerald-400 font-bold">● Online</span>
    }
  }

  return (
    <div className="flex h-screen bg-[#F6F7FC] overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 bg-[#1C1B2E] flex flex-col text-white z-20">
        <div className="p-6 flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg flex items-center justify-center text-white font-bold text-xs" style={{ background: 'linear-gradient(135deg,#6366F1 0%,#A855F7 100%)' }}>S</div>
          <div>
            <div className="font-bold tracking-tight leading-none" style={{ fontFamily: 'Plus Jakarta Sans, sans-serif' }}>SupportHub</div>
            <div className="text-[9px] text-[#9598B0] uppercase tracking-widest mt-1">AI Omnichannel Platform</div>
          </div>
        </div>
        
        {/* Viewing As Dropdown Badge */}
        <div className="relative px-4 py-2 mx-4 bg-white/5 rounded-xl border border-white/10 mb-2">
          <div className="text-[9px] font-bold text-[#9598B0] uppercase tracking-wider mb-1">Demo — Viewing As</div>
          <button 
            onClick={() => setShowStatusDropdown(!showStatusDropdown)}
            className="w-full text-xs font-bold text-white flex items-center justify-between hover:opacity-80 transition-opacity outline-none"
          >
            <span>Support Agent</span>
            {getStatusBadge()}
          </button>

          {/* Interactive Agent Status Dropdown */}
          {showStatusDropdown && (
            <div className="absolute left-0 right-0 top-full mt-1 bg-[#28273F] border border-white/10 rounded-xl shadow-xl z-50 p-1.5 space-y-1 text-xs">
              <button
                onClick={() => { setAgentStatus('online'); setShowStatusDropdown(false); }}
                className={`w-full flex items-center justify-between px-3 py-1.5 rounded-lg text-left font-medium transition-colors ${agentStatus === 'online' ? 'bg-indigo-600/40 text-white font-bold' : 'text-gray-300 hover:bg-white/5'}`}
              >
                <span>Online</span>
                <span className="text-[10px] text-emerald-400">● Available</span>
              </button>
              <button
                onClick={() => { setAgentStatus('away'); setShowStatusDropdown(false); }}
                className={`w-full flex items-center justify-between px-3 py-1.5 rounded-lg text-left font-medium transition-colors ${agentStatus === 'away' ? 'bg-indigo-600/40 text-white font-bold' : 'text-gray-300 hover:bg-white/5'}`}
              >
                <span>Away</span>
                <span className="text-[10px] text-amber-400">● In a meeting</span>
              </button>
              <button
                onClick={() => { setAgentStatus('offline'); setShowStatusDropdown(false); }}
                className={`w-full flex items-center justify-between px-3 py-1.5 rounded-lg text-left font-medium transition-colors ${agentStatus === 'offline' ? 'bg-indigo-600/40 text-white font-bold' : 'text-gray-300 hover:bg-white/5'}`}
              >
                <span>Offline</span>
                <span className="text-[10px] text-gray-400">● Offline</span>
              </button>
            </div>
          )}
        </div>

        <nav className="flex-1 px-4 space-y-1.5 mt-2 overflow-y-auto">
          <div className="text-[9px] font-bold text-[#9598B0] uppercase tracking-wider px-3 mb-1">Workspace</div>
          
          <Link to="/agent" className={`flex items-center justify-between px-3 py-2 rounded-lg text-xs font-semibold transition-colors ${location.pathname === '/agent' ? 'bg-[#6366F1] text-white shadow-sm' : 'text-[#9598B0] hover:bg-white/5'}`}>
            <div className="flex items-center gap-2.5"><LayoutDashboard size={16} /> Dashboard</div>
          </Link>

          <Link to="/agent/whatsapp" className={`flex items-center justify-between px-3 py-2 rounded-lg text-xs font-semibold transition-colors ${location.pathname === '/agent/whatsapp' ? 'bg-emerald-600 text-white shadow-sm' : 'text-[#9598B0] hover:bg-white/5'}`}>
            <div className="flex items-center gap-2.5"><Smartphone size={16} className="text-emerald-400" /> WhatsApp Inbox</div>
          </Link>

          <Link to="/agent/instagram" className={`flex items-center justify-between px-3 py-2 rounded-lg text-xs font-semibold transition-colors ${location.pathname === '/agent/instagram' ? 'bg-gradient-to-r from-rose-500 to-purple-600 text-white shadow-sm' : 'text-[#9598B0] hover:bg-white/5'}`}>
            <div className="flex items-center gap-2.5"><Instagram size={16} className="text-pink-400" /> Instagram Inbox</div>
          </Link>

          <Link to="/agent/facebook" className={`flex items-center justify-between px-3 py-2 rounded-lg text-xs font-semibold transition-colors ${location.pathname === '/agent/facebook' ? 'bg-[#1877F2] text-white shadow-sm' : 'text-[#9598B0] hover:bg-white/5'}`}>
            <div className="flex items-center gap-2.5"><Facebook size={16} className="text-blue-400" /> Facebook Inbox</div>
          </Link>

          <Link to="/agent/email" className={`flex items-center justify-between px-3 py-2 rounded-lg text-xs font-semibold transition-colors ${location.pathname === '/agent/email' ? 'bg-indigo-600 text-white shadow-sm' : 'text-[#9598B0] hover:bg-white/5'}`}>
            <div className="flex items-center gap-2.5"><Mail size={16} className="text-indigo-400" /> Email Inbox</div>
          </Link>
          
          <Link to="/agent/inbox" className={`flex items-center justify-between px-3 py-2 rounded-lg text-xs font-semibold transition-colors ${location.pathname === '/agent/inbox' ? 'bg-[#6366F1] text-white shadow-sm' : 'text-[#9598B0] hover:bg-white/5'}`}>
            <div className="flex items-center gap-2.5"><MessageSquare size={16} /> All Tickets</div>
          </Link>

          <Link to="/agent/queue" className={`flex items-center justify-between px-3 py-2 rounded-lg text-xs font-semibold transition-colors ${location.pathname === '/agent/queue' ? 'bg-[#6366F1] text-white shadow-sm' : 'text-[#9598B0] hover:bg-white/5'}`}>
            <div className="flex items-center gap-2.5"><ListFilter size={16} /> Ticket Queue</div>
          </Link>

          <Link to="/agent/quick-replies" className={`flex items-center justify-between px-3 py-2 rounded-lg text-xs font-semibold transition-colors ${location.pathname === '/agent/quick-replies' ? 'bg-[#6366F1] text-white shadow-sm' : 'text-[#9598B0] hover:bg-white/5'}`}>
            <div className="flex items-center gap-2.5"><Zap size={16} /> Quick Replies</div>
          </Link>

          <Link to="/agent/help-center" className={`flex items-center justify-between px-3 py-2 rounded-lg text-xs font-semibold transition-colors ${location.pathname === '/agent/help-center' ? 'bg-[#6366F1] text-white shadow-sm' : 'text-[#9598B0] hover:bg-white/5'}`}>
            <div className="flex items-center gap-2.5"><BookOpen size={16} /> Help Center</div>
          </Link>

          <div className="text-[9px] font-bold text-[#9598B0] uppercase tracking-wider px-3 pt-3 mb-1">Status Filters</div>

          <Link to="/agent/active" className={`flex items-center justify-between px-3 py-2 rounded-lg text-xs font-semibold transition-colors ${location.pathname === '/agent/active' ? 'bg-[#6366F1] text-white shadow-sm' : 'text-[#9598B0] hover:bg-white/5'}`}>
            <div className="flex items-center gap-2.5"><Clock size={16} /> Active Tickets</div>
          </Link>

          <Link to="/agent/resolved" className={`flex items-center justify-between px-3 py-2 rounded-lg text-xs font-semibold transition-colors ${location.pathname === '/agent/resolved' ? 'bg-[#6366F1] text-white shadow-sm' : 'text-[#9598B0] hover:bg-white/5'}`}>
            <div className="flex items-center gap-2.5"><CheckCircle size={16} /> Total Resolved</div>
          </Link>
        </nav>
        
        <div className="p-4 border-t border-white/10">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-7 h-7 rounded-full bg-indigo-600 text-white font-bold text-[10px] flex items-center justify-center">
                EW
              </div>
              <div>
                <div className="text-xs font-bold truncate max-w-[120px]">{name || 'Emma Wilson'}</div>
                <div className="text-[9px] text-[#9598B0]">Support Agent</div>
              </div>
            </div>
            <button onClick={handleLogout} className="text-[#9598B0] hover:text-white p-1.5 rounded-md hover:bg-white/10 transition-colors" title="Log out">
              <LogOut size={16} />
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col min-w-0">
        <Routes>
          <Route path="/" element={<AgentOverview />} />
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
      </main>
    </div>
  )
}
