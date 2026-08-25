import { useState } from 'react'
import { Routes, Route, Navigate, Link, useNavigate, useLocation } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { ticketsApi } from '../../api/tickets'
import { useAuthStore } from '../../store/authStore'
import { MessageSquare, LogOut, User, Star, Mail, BookOpen, Phone, Instagram, ShoppingBag, LayoutDashboard, Truck, RotateCcw, Lock, History } from 'lucide-react'

import CustomerDashboard from './CustomerDashboard'
import CustomerLiveChat from './CustomerLiveChat'
import CustomerOrders from './CustomerOrders'
import CustomerShipments from './CustomerShipments'
import CustomerReturnsRefunds from './CustomerReturnsRefunds'
import CustomerSupportHistory from './CustomerSupportHistory'
import CustomerSecuritySettings from './CustomerSecuritySettings'
import CustomerProfile from './CustomerProfile'
import CustomerReviews from './CustomerReviews'
import CustomerHelpCenter from './CustomerHelpCenter'
import ContactEmailModal from '../../components/ContactEmailModal'
import ContactWhatsAppModal from '../../components/ContactWhatsAppModal'
import ContactInstagramModal from '../../components/ContactInstagramModal'

// ─── Layout ──────────────────────────────────────────────────────────────────
export default function CustomerLayout() {
  const { role, logout, name, isAuthenticated } = useAuthStore()
  const location = useLocation()
  const navigate = useNavigate()
  const [isEmailModalOpen, setIsEmailModalOpen] = useState(false)
  const [isWhatsAppModalOpen, setIsWhatsAppModalOpen] = useState(false)
  const [isInstagramModalOpen, setIsInstagramModalOpen] = useState(false)

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
  
  if (!isAuthenticated || role !== 'customer') return <Navigate to="/login" replace />

  const handleLogout = () => {
    logout()
    navigate('/login', { replace: true })
  }
  
  return (
    <div className="flex h-screen bg-[#F6F7FC] overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-[#E5E7F3] flex flex-col z-20 overflow-y-auto">
        <div className="p-6 flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg flex items-center justify-center text-white font-bold text-xs" style={{ background: 'linear-gradient(135deg,#6366F1 0%,#A855F7 100%)' }}>S</div>
          <div>
            <div className="font-bold text-[#1C1B2E] tracking-tight leading-none" style={{ fontFamily: 'Plus Jakarta Sans, sans-serif' }}>SupportHub</div>
            <div className="text-[9px] text-[#9598B0] uppercase tracking-widest mt-1">AI Omnichannel Platform</div>
          </div>
        </div>
        
        <div className="px-4 py-3">
           <div className="text-[10px] font-bold text-[#9598B0] uppercase tracking-wider mb-2 px-3">Account & Support</div>
           <nav className="space-y-1">
             <Link to="/customer/dashboard" className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-semibold transition-colors ${location.pathname === '/customer' || location.pathname === '/customer/dashboard' ? 'bg-indigo-50 text-indigo-700' : 'text-[#6C7089] hover:bg-gray-50'}`}>
               <LayoutDashboard size={18} /> Dashboard Overview
             </Link>
             <Link to="/customer/chat" className={`flex items-center justify-between px-3 py-2 rounded-lg text-sm font-semibold transition-colors ${location.pathname.startsWith('/customer/chat') ? 'bg-indigo-50 text-indigo-700' : 'text-[#6C7089] hover:bg-gray-50'}`}>
               <div className="flex items-center gap-3">
                 <MessageSquare size={18} /> Live AI Assistant
               </div>
               {activeCount > 0 && (
                 <span className="bg-[#6366F1] text-white text-[10px] font-bold px-2 py-0.5 rounded-full">
                   {activeCount}
                 </span>
               )}
             </Link>
             <Link to="/customer/orders" className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-semibold transition-colors ${location.pathname === '/customer/orders' ? 'bg-indigo-50 text-indigo-700' : 'text-[#6C7089] hover:bg-gray-50'}`}>
               <ShoppingBag size={18} /> My Orders
             </Link>
             <Link to="/customer/shipments" className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-semibold transition-colors ${location.pathname === '/customer/shipments' ? 'bg-indigo-50 text-indigo-700' : 'text-[#6C7089] hover:bg-gray-50'}`}>
               <Truck size={18} /> Shipments & Tracking
             </Link>
             <Link to="/customer/returns" className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-semibold transition-colors ${location.pathname === '/customer/returns' ? 'bg-indigo-50 text-indigo-700' : 'text-[#6C7089] hover:bg-gray-50'}`}>
               <RotateCcw size={18} /> Returns & Refunds
             </Link>
             <Link to="/customer/support" className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-semibold transition-colors ${location.pathname === '/customer/support' ? 'bg-indigo-50 text-indigo-700' : 'text-[#6C7089] hover:bg-gray-50'}`}>
               <History size={18} /> Support History
             </Link>
             <Link to="/customer/profile" className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-semibold transition-colors ${location.pathname === '/customer/profile' ? 'bg-indigo-50 text-indigo-700' : 'text-[#6C7089] hover:bg-gray-50'}`}>
               <User size={18} /> Customer Profile
             </Link>
             <Link to="/customer/settings" className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-semibold transition-colors ${location.pathname === '/customer/settings' ? 'bg-indigo-50 text-indigo-700' : 'text-[#6C7089] hover:bg-gray-50'}`}>
               <Lock size={18} /> Security Settings
             </Link>
             <Link to="/customer/help" className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-semibold transition-colors ${location.pathname === '/customer/help' ? 'bg-indigo-50 text-indigo-700' : 'text-[#6C7089] hover:bg-gray-50'}`}>
               <BookOpen size={18} /> Help Center & FAQs
             </Link>
             <Link to="/customer/reviews" className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-semibold transition-colors ${location.pathname === '/customer/reviews' ? 'bg-indigo-50 text-indigo-700' : 'text-[#6C7089] hover:bg-gray-50'}`}>
               <Star size={18} /> My Reviews
             </Link>

             <div className="pt-2 text-[10px] font-bold text-[#9598B0] uppercase tracking-wider px-3">Omnichannel Channels</div>
             <button
               onClick={() => setIsWhatsAppModalOpen(true)}
               className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-semibold text-[#6C7089] hover:bg-emerald-50 hover:text-emerald-600 transition-colors text-left"
             >
               <Phone size={16} className="text-emerald-500" /> Connect WhatsApp
             </button>
             <button
               onClick={() => setIsInstagramModalOpen(true)}
               className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-semibold text-[#6C7089] hover:bg-rose-50 hover:text-rose-600 transition-colors text-left"
             >
               <Instagram size={16} className="text-rose-500" /> Connect Instagram
             </button>
             <button
               onClick={() => setIsEmailModalOpen(true)}
               className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-semibold text-[#6C7089] hover:bg-blue-50 hover:text-blue-600 transition-colors text-left"
             >
               <Mail size={16} className="text-blue-500" /> Contact Email
             </button>
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
            <button onClick={handleLogout} className="text-[#9598B0] hover:text-red-500 p-1.5 rounded-md hover:bg-red-50 transition-colors" title="Log out">
              <LogOut size={16} />
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col min-w-0">
        <Routes>
          <Route path="/" element={<CustomerDashboard />} />
          <Route path="/dashboard" element={<CustomerDashboard />} />
          <Route path="/chat" element={<CustomerLiveChat />} />
          <Route path="/chat/:id" element={<CustomerLiveChat />} />
          <Route path="/orders" element={<CustomerOrders />} />
          <Route path="/shipments" element={<CustomerShipments />} />
          <Route path="/returns" element={<CustomerReturnsRefunds />} />
          <Route path="/support" element={<CustomerSupportHistory />} />
          <Route path="/profile" element={<CustomerProfile />} />
          <Route path="/settings" element={<CustomerSecuritySettings />} />
          <Route path="/help" element={<CustomerHelpCenter />} />
          <Route path="/reviews" element={<CustomerReviews />} />
          <Route path="*" element={<Navigate to="/customer" replace />} />
        </Routes>
      </main>

      <ContactEmailModal isOpen={isEmailModalOpen} onClose={() => setIsEmailModalOpen(false)} />
      <ContactWhatsAppModal isOpen={isWhatsAppModalOpen} onClose={() => setIsWhatsAppModalOpen(false)} />
      <ContactInstagramModal isOpen={isInstagramModalOpen} onClose={() => setIsInstagramModalOpen(false)} />
    </div>
  )
}

