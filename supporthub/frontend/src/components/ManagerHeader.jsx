import { useState, useRef, useEffect } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import {
  Smartphone, Instagram, Facebook, Mail, LogOut,
  ChevronDown, Shield, User, Lock
} from 'lucide-react'

export default function ManagerHeader() {
  const { name, email, logout } = useAuthStore()
  const navigate = useNavigate()
  const location = useLocation()
  const [isDropdownOpen, setIsDropdownOpen] = useState(false)
  const dropdownRef = useRef(null)

  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsDropdownOpen(false)
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
    : 'MG'

  const getPageTitle = () => {
    const path = location.pathname
    if (path === '/manager') return 'Support Overview'
    if (path === '/manager/analytics') return 'Analytics Dashboard'
    if (path === '/manager/agent-performance') return 'Agent Performance'
    if (path === '/manager/sla-dashboard') return 'SLA Dashboard'
    if (path === '/manager/reports') return 'Ticket Reports'
    if (path === '/manager/workflow') return 'Workflow Automation Engine'
    if (path.startsWith('/manager/inbox/active')) return 'Active Tickets'
    if (path.startsWith('/manager/inbox/closed')) return 'Closed Tickets'
    if (path.startsWith('/manager/inbox')) return 'All Tickets'
    if (path.startsWith('/manager/knowledge')) return 'Knowledge Base'
    if (path.startsWith('/manager/whatsapp')) return 'WhatsApp Inbox'
    if (path.startsWith('/manager/instagram')) return 'Instagram Direct Inbox'
    if (path.startsWith('/manager/email')) return 'Email Inbox'
    if (path.startsWith('/manager/tickets')) return 'Ticket Detail'
    return 'Manager Workspace'
  }

  const getPageSubtitle = () => {
    const path = location.pathname
    if (path === '/manager') return 'Live snapshot across all channels, agents & reviews'
    if (path === '/manager/analytics') return 'Trends, volume, and resolution analytics'
    if (path === '/manager/agent-performance') return 'Track team volume, resolution speed & CSAT'
    if (path === '/manager/sla-dashboard') return 'Monitor SLA compliance and breach alerts'
    if (path === '/manager/reports') return 'Filter, export and review ticket reports'
    if (path === '/manager/workflow') return 'Automate routing, tagging and escalation rules'
    if (path.startsWith('/manager/inbox')) return 'All customer conversations in one place'
    if (path.startsWith('/manager/knowledge')) return 'Manage articles and team knowledge'
    return 'Manager Control Center'
  }

  return (
    <header className="h-16 bg-white border-b border-[#E5E7F3] px-4 md:px-6 flex items-center justify-between z-30 shrink-0 shadow-xs">
      {/* LEFT: Page Title */}
      <div className="flex items-center gap-4">
        <div>
          <h1 className="font-extrabold text-sm md:text-base text-[#1C1B2E] tracking-tight leading-tight">
            {getPageTitle()}
          </h1>
          <div className="text-[10px] text-[#6C7089] font-medium flex items-center gap-1.5 mt-0.5">
            <span className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse"></span>
            <span>{getPageSubtitle()}</span>
          </div>
        </div>
      </div>

      {/* RIGHT: Manager Profile Dropdown */}
      <div className="flex items-center gap-3">
        <div className="relative" ref={dropdownRef}>
          <button
            onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            className={`flex items-center gap-2.5 p-1.5 sm:px-3 sm:py-1.5 rounded-xl border transition-all ${
              isDropdownOpen
                ? 'border-indigo-400 bg-indigo-50/60 shadow-sm ring-2 ring-indigo-500/10'
                : 'border-[#E5E7F3] hover:border-indigo-300 hover:bg-gray-50'
            }`}
            aria-label="Manager Menu"
          >
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-500 text-white flex items-center justify-center font-extrabold text-xs shadow-xs">
              {userInitials}
            </div>
            <div className="hidden sm:block text-left">
              <div className="text-xs font-bold text-[#1C1B2E] truncate max-w-[120px] leading-tight">
                {name || 'Manager'}
              </div>
              <div className="text-[10px] text-indigo-600 font-bold leading-none mt-0.5 flex items-center gap-1">
                <span>● Manager</span>
              </div>
            </div>
            <ChevronDown size={14} className={`text-[#6C7089] transition-transform duration-200 ${isDropdownOpen ? 'rotate-180' : ''}`} />
          </button>

          {isDropdownOpen && (
            <div className="absolute right-0 mt-2 w-72 bg-white rounded-2xl shadow-xl border border-[#E5E7F3] py-2 z-50">
              {/* Profile Info */}
              <div className="px-4 py-3 border-b border-gray-100 bg-gray-50/60 rounded-t-2xl">
                <div className="flex items-center justify-between mb-1">
                  <div className="text-xs font-extrabold text-[#1C1B2E] truncate">{name || 'Manager'}</div>
                  <span className="text-[9px] font-extrabold bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full uppercase border border-indigo-200">
                    MANAGER
                  </span>
                </div>
                <div className="text-[11px] text-[#6C7089] truncate">{email || 'manager@supporthub.com'}</div>
              </div>

              {/* Profile & Security Links */}
              <div className="py-1 space-y-0.5">
                <Link
                  to="/manager/profile"
                  onClick={() => setIsDropdownOpen(false)}
                  className={`flex items-center gap-3 px-4 py-2.5 text-xs font-semibold transition-colors rounded-lg mx-1 ${location.pathname === '/manager/profile' ? 'bg-indigo-50 text-indigo-600 font-bold' : 'text-[#1C1B2E] hover:bg-gray-50'}`}
                >
                  <User size={15} className="text-indigo-600" />
                  <span>My Profile</span>
                </Link>
                <Link
                  to="/manager/security"
                  onClick={() => setIsDropdownOpen(false)}
                  className={`flex items-center gap-3 px-4 py-2.5 text-xs font-semibold transition-colors rounded-lg mx-1 ${location.pathname === '/manager/security' ? 'bg-indigo-50 text-indigo-600 font-bold' : 'text-[#1C1B2E] hover:bg-gray-50'}`}
                >
                  <Lock size={15} className="text-indigo-600" />
                  <span>Account Security &amp; Password</span>
                </Link>
              </div>

              {/* Direct Channels */}
              <div className="border-t border-gray-100 pt-2.5 pb-1 px-4 mt-1">
                <div className="text-[10px] font-extrabold text-[#9598B0] uppercase tracking-wider mb-2">
                  Direct Channels
                </div>
                <div className="grid grid-cols-2 gap-1.5">
                  <Link
                    to="/manager/whatsapp"
                    onClick={() => setIsDropdownOpen(false)}
                    className={`flex items-center gap-2 p-2 rounded-xl text-[11px] font-bold border transition-colors ${
                      location.pathname === '/manager/whatsapp'
                        ? 'bg-emerald-600 text-white border-emerald-600'
                        : 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border-emerald-200/60'
                    }`}
                  >
                    <Smartphone size={14} className={location.pathname === '/manager/whatsapp' ? 'text-white' : 'text-emerald-600'} />
                    <span>WhatsApp</span>
                  </Link>

                  <Link
                    to="/manager/instagram"
                    onClick={() => setIsDropdownOpen(false)}
                    className={`flex items-center gap-2 p-2 rounded-xl text-[11px] font-bold border transition-colors ${
                      location.pathname === '/manager/instagram'
                        ? 'bg-rose-600 text-white border-rose-600'
                        : 'bg-rose-50 text-rose-700 hover:bg-rose-100 border-rose-200/60'
                    }`}
                  >
                    <Instagram size={14} className={location.pathname === '/manager/instagram' ? 'text-white' : 'text-rose-600'} />
                    <span>Instagram</span>
                  </Link>

                  <Link
                    to="/manager/email"
                    onClick={() => setIsDropdownOpen(false)}
                    className={`flex items-center gap-2 p-2 rounded-xl text-[11px] font-bold border transition-colors ${
                      location.pathname === '/manager/email'
                        ? 'bg-indigo-600 text-white border-indigo-600'
                        : 'bg-indigo-50 text-indigo-700 hover:bg-indigo-100 border-indigo-200/60'
                    }`}
                  >
                    <Mail size={14} className={location.pathname === '/manager/email' ? 'text-white' : 'text-indigo-600'} />
                    <span>Email</span>
                  </Link>

                  <Link
                    to="/manager/facebook"
                    onClick={() => setIsDropdownOpen(false)}
                    className={`flex items-center gap-2 p-2 rounded-xl text-[11px] font-bold border transition-colors ${
                      location.pathname === '/manager/facebook'
                        ? 'bg-blue-600 text-white border-blue-600'
                        : 'bg-blue-50 text-blue-700 hover:bg-blue-100 border-blue-200/60'
                    }`}
                  >
                    <Facebook size={14} className={location.pathname === '/manager/facebook' ? 'text-white' : 'text-blue-600'} />
                    <span>Facebook</span>
                  </Link>
                </div>
              </div>

              {/* Sign Out */}
              <div className="border-t border-gray-100 pt-2 px-2 mt-1">
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
