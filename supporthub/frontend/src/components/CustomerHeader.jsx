import { useState, useRef, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import { Sparkles, HelpCircle, User, ShoppingBag, Truck, RotateCcw, Lock, Star, Phone, Instagram, Mail, LogOut, ChevronDown, BookOpen } from 'lucide-react'

export default function CustomerHeader({
  onOpenWhatsApp,
  onOpenInstagram,
  onOpenEmail
}) {
  const { name, email, logout } = useAuthStore()
  const navigate = useNavigate()

  const [isHelpOpen, setIsHelpOpen] = useState(false)
  const [isAccountOpen, setIsAccountOpen] = useState(false)

  const helpRef = useRef(null)
  const accountRef = useRef(null)

  // Close dropdowns when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (helpRef.current && !helpRef.current.contains(event.target)) {
        setIsHelpOpen(false)
      }
      if (accountRef.current && !accountRef.current.contains(event.target)) {
        setIsAccountOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleLogout = () => {
    logout()
    navigate('/login', { replace: true })
  }

  const userInitials = name
    ? name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
    : 'CU'

  return (
    <header className="h-16 bg-white border-b border-[#E5E7F3] px-4 md:px-6 flex items-center justify-between z-30 shrink-0 select-none shadow-sm">
      {/* LEFT: Brand Logo & Status Indicator */}
      <div className="flex items-center gap-4">
        <Link to="/customer" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-xl flex items-center justify-center text-white font-extrabold text-base shadow-md shadow-indigo-200 transition-transform group-hover:scale-105"
            style={{ background: 'linear-gradient(135deg,#6366F1 0%,#A855F7 100%)' }}>
            S
          </div>
          <div>
            <div className="font-extrabold text-[#1C1B2E] tracking-tight leading-none text-lg" style={{ fontFamily: 'Plus Jakarta Sans, sans-serif' }}>
              SupportHub
            </div>
            <div className="text-[10px] text-indigo-600 font-bold uppercase tracking-wider mt-0.5 flex items-center gap-1">
              <Sparkles size={10} className="text-amber-400" /> AI Support
            </div>
          </div>
        </Link>

        {/* Live Support Indicator */}
        <div className="hidden sm:flex items-center gap-2 px-3 py-1 bg-emerald-50 text-emerald-700 rounded-full text-xs font-semibold border border-emerald-100">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <span>Support Online</span>
        </div>
      </div>

      {/* RIGHT: Clean Header Navigation (Help + Account) */}
      <div className="flex items-center gap-3">
        {/* HELP MENU DROPDOWN */}
        <div className="relative" ref={helpRef}>
          <button
            onClick={() => { setIsHelpOpen(!isHelpOpen); setIsAccountOpen(false) }}
            className={`flex items-center gap-2 px-3 py-2 rounded-xl text-sm font-semibold transition-all ${
              isHelpOpen ? 'bg-indigo-50 text-indigo-600' : 'text-[#6C7089] hover:bg-gray-100 hover:text-[#1C1B2E]'
            }`}
            aria-label="Help & FAQs menu"
          >
            <HelpCircle size={18} className="text-indigo-600" />
            <span className="hidden sm:inline">Help</span>
            <ChevronDown size={14} className={`transition-transform duration-200 ${isHelpOpen ? 'rotate-180' : ''}`} />
          </button>

          {isHelpOpen && (
            <div className="absolute right-0 mt-2 w-64 bg-white rounded-2xl shadow-xl border border-[#E5E7F3] py-2 z-50 animate-fadeIn">
              <div className="px-4 py-2 border-b border-gray-100">
                <div className="text-xs font-extrabold text-[#9598B0] uppercase tracking-wider">Help & Resources</div>
              </div>
              <div className="py-1">
                <Link
                  to="/customer/help"
                  onClick={() => setIsHelpOpen(false)}
                  className="flex items-center gap-3 px-4 py-2.5 text-xs font-bold text-[#1C1B2E] hover:bg-indigo-50 hover:text-indigo-600 transition-colors"
                >
                  <BookOpen size={16} className="text-indigo-600" />
                  <span>Help Center & FAQs</span>
                </Link>
              </div>
              <div className="border-t border-gray-100 pt-2 pb-1 px-4">
                <div className="text-[10px] font-extrabold text-[#9598B0] uppercase tracking-wider mb-1">Direct Contact</div>
                <button
                  onClick={() => { onOpenEmail(); setIsHelpOpen(false) }}
                  className="w-full flex items-center gap-2 py-1.5 text-xs text-[#6C7089] hover:text-indigo-600 text-left"
                >
                  <Mail size={14} className="text-blue-500" /> Email Support
                </button>
                <button
                  onClick={() => { onOpenWhatsApp(); setIsHelpOpen(false) }}
                  className="w-full flex items-center gap-2 py-1.5 text-xs text-[#6C7089] hover:text-emerald-600 text-left"
                >
                  <Phone size={14} className="text-emerald-500" /> WhatsApp Support
                </button>
              </div>
            </div>
          )}
        </div>

        {/* ACCOUNT MENU DROPDOWN */}
        <div className="relative" ref={accountRef}>
          <button
            onClick={() => { setIsAccountOpen(!isAccountOpen); setIsHelpOpen(false) }}
            className={`flex items-center gap-2.5 p-1.5 sm:px-3 sm:py-1.5 rounded-xl border transition-all ${
              isAccountOpen
                ? 'border-indigo-300 bg-indigo-50/50 shadow-sm'
                : 'border-[#E5E7F3] hover:border-indigo-200 hover:bg-gray-50'
            }`}
            aria-label="Account menu"
          >
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-600 to-purple-600 text-white flex items-center justify-center font-extrabold text-xs shadow-sm">
              {userInitials}
            </div>
            <div className="hidden sm:block text-left">
              <div className="text-xs font-bold text-[#1C1B2E] truncate max-w-[110px] leading-tight">{name || 'Account'}</div>
              <div className="text-[10px] text-[#9598B0] font-medium leading-none mt-0.5">Customer</div>
            </div>
            <ChevronDown size={14} className={`text-[#6C7089] transition-transform duration-200 ${isAccountOpen ? 'rotate-180' : ''}`} />
          </button>

          {isAccountOpen && (
            <div className="absolute right-0 mt-2 w-72 bg-white rounded-2xl shadow-xl border border-[#E5E7F3] py-2 z-50 animate-fadeIn">
              {/* User Header */}
              <div className="px-4 py-3 border-b border-gray-100 bg-gray-50/50 rounded-t-2xl">
                <div className="text-xs font-extrabold text-[#1C1B2E] truncate">{name}</div>
                <div className="text-[11px] text-[#9598B0] truncate">{email}</div>
              </div>

              {/* Navigation Items */}
              <div className="py-2 space-y-0.5">
                <Link
                  to="/customer/profile"
                  onClick={() => setIsAccountOpen(false)}
                  className="flex items-center gap-3 px-4 py-2 text-xs font-semibold text-[#1C1B2E] hover:bg-indigo-50 hover:text-indigo-600 transition-colors"
                >
                  <User size={16} className="text-indigo-600" /> My Profile
                </Link>
                <Link
                  to="/customer/orders"
                  onClick={() => setIsAccountOpen(false)}
                  className="flex items-center gap-3 px-4 py-2 text-xs font-semibold text-[#1C1B2E] hover:bg-indigo-50 hover:text-indigo-600 transition-colors"
                >
                  <ShoppingBag size={16} className="text-indigo-600" /> My Orders
                </Link>
                <Link
                  to="/customer/shipments"
                  onClick={() => setIsAccountOpen(false)}
                  className="flex items-center gap-3 px-4 py-2 text-xs font-semibold text-[#1C1B2E] hover:bg-indigo-50 hover:text-indigo-600 transition-colors"
                >
                  <Truck size={16} className="text-indigo-600" /> Shipments & Tracking
                </Link>
                <Link
                  to="/customer/returns"
                  onClick={() => setIsAccountOpen(false)}
                  className="flex items-center gap-3 px-4 py-2 text-xs font-semibold text-[#1C1B2E] hover:bg-indigo-50 hover:text-indigo-600 transition-colors"
                >
                  <RotateCcw size={16} className="text-indigo-600" /> Returns & Refunds
                </Link>
                <Link
                  to="/customer/settings"
                  onClick={() => setIsAccountOpen(false)}
                  className="flex items-center gap-3 px-4 py-2 text-xs font-semibold text-[#1C1B2E] hover:bg-indigo-50 hover:text-indigo-600 transition-colors"
                >
                  <Lock size={16} className="text-indigo-600" /> Security Settings
                </Link>
                <Link
                  to="/customer/reviews"
                  onClick={() => setIsAccountOpen(false)}
                  className="flex items-center gap-3 px-4 py-2 text-xs font-semibold text-[#1C1B2E] hover:bg-indigo-50 hover:text-indigo-600 transition-colors"
                >
                  <Star size={16} className="text-indigo-600" /> My Reviews
                </Link>
              </div>

              {/* Omnichannel Section */}
              <div className="border-t border-gray-100 pt-2 pb-1 px-4">
                <div className="text-[10px] font-extrabold text-[#9598B0] uppercase tracking-wider mb-1">Direct Channels</div>
                <div className="grid grid-cols-3 gap-1">
                  <button
                    onClick={() => { onOpenWhatsApp(); setIsAccountOpen(false) }}
                    className="flex flex-col items-center justify-center p-2 rounded-xl bg-emerald-50 text-emerald-700 hover:bg-emerald-100 transition-colors text-[10px] font-bold"
                  >
                    <Phone size={14} className="mb-0.5" /> WhatsApp
                  </button>
                  <button
                    onClick={() => { onOpenInstagram(); setIsAccountOpen(false) }}
                    className="flex flex-col items-center justify-center p-2 rounded-xl bg-rose-50 text-rose-700 hover:bg-rose-100 transition-colors text-[10px] font-bold"
                  >
                    <Instagram size={14} className="mb-0.5" /> Instagram
                  </button>
                  <button
                    onClick={() => { onOpenEmail(); setIsAccountOpen(false) }}
                    className="flex flex-col items-center justify-center p-2 rounded-xl bg-blue-50 text-blue-700 hover:bg-blue-100 transition-colors text-[10px] font-bold"
                  >
                    <Mail size={14} className="mb-0.5" /> Email
                  </button>
                </div>
              </div>

              {/* Sign Out Footer */}
              <div className="border-t border-gray-100 pt-2 px-2">
                <button
                  onClick={handleLogout}
                  className="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-bold text-rose-600 hover:bg-rose-50 transition-colors text-left"
                >
                  <LogOut size={16} /> Sign Out
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}
