import { useState } from 'react'
import { Routes, Route, Navigate, Link, useNavigate, useLocation } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { ticketsApi } from '../../api/tickets'
import { useAuthStore } from '../../store/authStore'
import { MessageSquare, LogOut, User, Star } from 'lucide-react'

import CustomerLiveChat from './CustomerLiveChat'
import CustomerProfile from './CustomerProfile'
import CustomerReviews from './CustomerReviews'

// ─── Layout ──────────────────────────────────────────────────────────────────
export default function CustomerLayout() {
  const { role, logout, name } = useAuthStore()
  const location = useLocation()

  // Active tickets for notification badge calculation
  const { data: tickets = [] } = useQuery({
    queryKey: ['tickets', 'customer'],
    queryFn: async () => {
      const res = await ticketsApi.list()
      return res.data
    },
    refetchInterval: 10000,
  })

  const activeCount = tickets.filter(t => t.status !== 'resolved' && t.status !== 'closed').length
  
  if (role !== 'customer') return <Navigate to="/" replace />
  
  return (
    <div className="flex h-screen bg-[#F6F7FC] overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-[#E5E7F3] flex flex-col z-20">
        <div className="p-6 flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg flex items-center justify-center text-white font-bold text-xs" style={{ background: 'linear-gradient(135deg,#6366F1 0%,#A855F7 100%)' }}>S</div>
          <div>
            <div className="font-bold text-[#1C1B2E] tracking-tight leading-none" style={{ fontFamily: 'Plus Jakarta Sans, sans-serif' }}>SupportHub</div>
            <div className="text-[9px] text-[#9598B0] uppercase tracking-widest mt-1">AI Omnichannel Platform</div>
          </div>
        </div>
        
        <div className="px-4 py-3">
           <div className="text-[10px] font-bold text-[#9598B0] uppercase tracking-wider mb-2 px-3">Support</div>
           <nav className="space-y-1">
             <Link to="/customer" className={`flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-semibold transition-colors ${location.pathname === '/customer' || location.pathname.startsWith('/customer/chat') ? 'bg-indigo-50 text-indigo-700' : 'text-[#6C7089] hover:bg-gray-50'}`}>
               <div className="flex items-center gap-3">
                 <MessageSquare size={18} /> Live Chat
               </div>
               {activeCount > 0 && (
                 <span className="bg-[#6366F1] text-white text-[10px] font-bold px-2 py-0.5 rounded-full">
                   {activeCount}
                 </span>
               )}
             </Link>
             <Link to="/customer/reviews" className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-semibold transition-colors ${location.pathname === '/customer/reviews' ? 'bg-indigo-50 text-indigo-700' : 'text-[#6C7089] hover:bg-gray-50'}`}>
               <Star size={18} /> My Reviews
             </Link>
             <Link to="/customer/profile" className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-semibold transition-colors ${location.pathname === '/customer/profile' ? 'bg-indigo-50 text-indigo-700' : 'text-[#6C7089] hover:bg-gray-50'}`}>
               <User size={18} /> Customer Profile
             </Link>
           </nav>
        </div>
        
        <div className="mt-auto p-4 border-t border-[#E5E7F3]">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold text-xs">
                {name ? name.split(' ').map(n => n[0]).join('').substring(0,2).toUpperCase() : 'CU'}
              </div>
              <div>
                <div className="text-sm font-bold text-[#1C1B2E] truncate max-w-[120px] leading-tight">{name}</div>
                <div className="text-[10px] text-[#9598B0] capitalize">Customer</div>
              </div>
            </div>
            <button onClick={logout} className="text-[#9598B0] hover:text-red-500 p-1.5 rounded-md hover:bg-red-50 transition-colors" title="Log out">
              <LogOut size={16} />
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col min-w-0">
        <Routes>
          <Route path="/" element={<CustomerLiveChat />} />
          <Route path="/chat/:id" element={<CustomerLiveChat />} />
          <Route path="/reviews" element={<CustomerReviews />} />
          <Route path="/profile" element={<CustomerProfile />} />
          <Route path="*" element={<Navigate to="/customer" replace />} />
        </Routes>
      </main>
    </div>
  )
}
