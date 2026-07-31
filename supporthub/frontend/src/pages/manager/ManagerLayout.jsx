import { useState } from 'react'
import { Routes, Route, Navigate, Link, useLocation } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'
import { LogOut, LayoutDashboard, Settings, BookOpen, Inbox, Clock, CheckCircle, ChevronDown } from 'lucide-react'
import KnowledgeBase from './KnowledgeBase'
import ManagerOverview from './ManagerOverview'
import UnifiedInbox from '../../components/UnifiedInbox'
import TicketDetail from '../../components/TicketDetail'

export default function ManagerLayout() {
  const { role, logout, name } = useAuthStore()
  const location = useLocation()
  const [inboxExpanded, setInboxExpanded] = useState(false)
  
  if (role !== 'manager' && role !== 'admin') return <Navigate to="/" replace />
  
  const isInboxActive = location.pathname.startsWith('/manager/inbox') || location.pathname.startsWith('/manager/tickets')

  return (
    <div className="flex h-screen bg-[#F6F7FC] overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 bg-slate-900 flex flex-col text-white z-20">
        <div className="p-6 flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg flex items-center justify-center text-white font-bold text-xs" style={{ background: 'linear-gradient(135deg,#6366F1 0%,#A855F7 100%)' }}>S</div>
          <div className="font-bold tracking-tight" style={{ fontFamily: 'Plus Jakarta Sans, sans-serif' }}>Manager Dashboard</div>
        </div>
        
        <nav className="flex-1 px-4 space-y-2 mt-4 overflow-y-auto">
          <Link to="/manager" className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-semibold transition-colors ${location.pathname === '/manager' ? 'bg-white/10 text-white' : 'text-[#9598B0] hover:bg-white/5'}`}>
            <LayoutDashboard size={18} /> Overview
          </Link>

          {/* Team Inbox Accordion */}
          <div>
            <button
              onClick={() => setInboxExpanded(!inboxExpanded)}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-semibold transition-colors ${isInboxActive ? 'bg-white/10 text-white' : 'text-[#9598B0] hover:bg-white/5'}`}
            >
              <div className="flex items-center gap-3">
                <Inbox size={18} /> Team Inbox
              </div>
              <ChevronDown size={16} className={`transition-transform duration-200 ${inboxExpanded ? 'rotate-180' : ''}`} />
            </button>

            {inboxExpanded && (
              <div className="pl-6 pr-1 py-1.5 space-y-1">
                <Link
                  to="/manager/inbox/active"
                  className={`flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-semibold transition-colors ${location.pathname === '/manager/inbox/active' ? 'bg-indigo-600 text-white shadow-sm' : 'text-[#9598B0] hover:bg-white/5 hover:text-white'}`}
                >
                  <Clock size={14} /> Active Tickets
                </Link>

                <Link
                  to="/manager/inbox/closed"
                  className={`flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-semibold transition-colors ${location.pathname === '/manager/inbox/closed' ? 'bg-indigo-600 text-white shadow-sm' : 'text-[#9598B0] hover:bg-white/5 hover:text-white'}`}
                >
                  <CheckCircle size={14} /> Closed Tickets
                </Link>

                <Link
                  to="/manager/inbox/all"
                  className={`flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-semibold transition-colors ${location.pathname === '/manager/inbox/all' || location.pathname === '/manager/inbox' ? 'bg-indigo-600 text-white shadow-sm' : 'text-[#9598B0] hover:bg-white/5 hover:text-white'}`}
                >
                  <Inbox size={14} /> All Tickets
                </Link>
              </div>
            )}
          </div>

          <Link to="/manager/knowledge" className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-semibold transition-colors ${location.pathname.startsWith('/manager/knowledge') ? 'bg-white/10 text-white' : 'text-[#9598B0] hover:bg-white/5'}`}>
            <BookOpen size={18} /> Knowledge Base
          </Link>
          <div className="flex items-center gap-3 px-3 py-2.5 text-[#9598B0] opacity-50 cursor-not-allowed rounded-lg text-sm font-semibold">
            <Settings size={18} /> Queue Setup (Soon)
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
          <Route path="/" element={<ManagerOverview />} />
          <Route path="/inbox" element={<UnifiedInbox filter="all" basePath="/manager" />} />
          <Route path="/inbox/all" element={<UnifiedInbox filter="all" basePath="/manager" />} />
          <Route path="/inbox/active" element={<UnifiedInbox filter="active" basePath="/manager" />} />
          <Route path="/inbox/closed" element={<UnifiedInbox filter="closed" basePath="/manager" />} />
          <Route path="/tickets/:id" element={<TicketDetail basePath="/manager" />} />
          <Route path="/knowledge/*" element={<KnowledgeBase />} />
          <Route path="*" element={<Navigate to="/manager" replace />} />
        </Routes>
      </main>
    </div>
  )
}
