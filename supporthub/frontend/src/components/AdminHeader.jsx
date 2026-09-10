import { useState, useRef, useEffect } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import {
  Smartphone, Instagram, Facebook, Mail, LogOut,
  ChevronDown, Shield, User, Lock
} from 'lucide-react'

export default function AdminHeader() {
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
    : 'AU'

  const getPageTitle = () => {
    const path = location.pathname
    if (path === '/admin') return 'Admin Overview'
    if (path === '/admin/users' || path === '/admin/directory') return 'User Management'
    if (path === '/admin/channels') return 'Channel Integrations'
    if (path === '/admin/help-center') return 'Help Center Management'
    if (path === '/admin/ai-settings') return 'AI Settings'
    if (path === '/admin/roles') return 'Roles & Permissions'
    if (path === '/admin/settings') return 'System Settings'
    if (path.startsWith('/admin/inbox/active')) return 'Active Tickets'
    if (path.startsWith('/admin/inbox/closed')) return 'Closed Tickets'
    if (path.startsWith('/admin/inbox')) return 'Global Inbox'
    if (path.startsWith('/admin/profile')) return 'My Profile'
    if (path.startsWith('/admin/security')) return 'Account Security & Credentials'
    if (path.startsWith('/admin/whatsapp')) return 'WhatsApp Inbox'
    if (path.startsWith('/admin/instagram')) return 'Instagram Direct Inbox'
    if (path.startsWith('/admin/email')) return 'Email Inbox'
    if (path.startsWith('/admin/facebook')) return 'Facebook Inbox'
    if (path.startsWith('/admin/tickets')) return 'Ticket Detail'
    return 'Admin Workspace'
  }

  const getPageSubtitle = () => {
    const path = location.pathname
    if (path === '/admin') return 'System health, users and integrations at a glance'
    if (path === '/admin/users' || path === '/admin/directory') return 'Manage customers, agents, managers & administrators'
    if (path === '/admin/channels') return 'Connect and manage WhatsApp, Instagram, Facebook & Email'
    if (path === '/admin/help-center') return 'Manage customer-facing knowledge base articles & FAQs'
    if (path === '/admin/ai-settings') return 'Configure autonomous AI resolution, confidence and behavior'
    if (path === '/admin/roles') return 'Define role permissions and access privileges across staff'
    if (path === '/admin/settings') return 'Platform configurations, branding, and system preferences'
    if (path.startsWith('/admin/inbox/active')) return 'All ongoing conversations requiring attention'
    if (path.startsWith('/admin/inbox/closed')) return 'Historical and completed support tickets'
    if (path.startsWith('/admin/inbox')) return 'All customer conversations across every channel'
    if (path.startsWith('/admin/profile')) return 'Manage your personal profile and account credentials'
    if (path.startsWith('/admin/security')) return 'Update password and authentication credentials'
    if (path.startsWith('/admin/whatsapp')) return 'Direct WhatsApp customer conversations'
    if (path.startsWith('/admin/instagram')) return 'Direct Instagram messaging conversations'
    if (path.startsWith('/admin/email')) return 'Direct Email ticket communications'
    if (path.startsWith('/admin/facebook')) return 'Direct Facebook Messenger communications'
    if (path.startsWith('/admin/tickets')) return 'View and manage customer ticket details'
    return 'SupportHub Administration Platform'
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

      {/* RIGHT: Admin Profile Dropdown */}
      <div className="flex items-center gap-3">
        <div className="relative" ref={dropdownRef}>
          <button
            onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            className={`flex items-center gap-2.5 p-1.5 sm:px-3 sm:py-1.5 rounded-xl border transition-all ${
              isDropdownOpen
                ? 'border-indigo-400 bg-indigo-50/60 shadow-sm ring-2 ring-indigo-500/10'
                : 'border-[#E5E7F3] hover:border-indigo-300 hover:bg-gray-50'
            }`}
            aria-label="Admin Menu"
          >
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-500 text-white flex items-center justify-center font-extrabold text-xs shadow-xs">
              {userInitials}
            </div>
            <div className="hidden sm:block text-left">
              <div className="text-xs font-bold text-[#1C1B2E] truncate max-w-[120px] leading-tight">
                {name || 'Admin User'}
              </div>
              <div className="text-[10px] text-indigo-600 font-bold leading-none mt-0.5 flex items-center gap-1">
                <span>● Admin</span>
              </div>
            </div>
            <ChevronDown size={14} className={`text-[#6C7089] transition-transform duration-200 ${isDropdownOpen ? 'rotate-180' : ''}`} />
          </button>

          {isDropdownOpen && (
            <div className="absolute right-0 mt-2 w-72 bg-white rounded-2xl shadow-xl border border-[#E5E7F3] py-2 z-50">
              {/* Profile Info */}
              <div className="px-4 py-3 border-b border-gray-100 bg-gray-50/60 rounded-t-2xl">
                <div className="flex items-center justify-between mb-1">
                  <div className="text-xs font-extrabold text-[#1C1B2E] truncate">{name || 'Admin User'}</div>
                  <span className="text-[9px] font-extrabold bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full uppercase border border-indigo-200">
                    ADMIN
                  </span>
                </div>
                <div className="text-[11px] text-[#6C7089] truncate">{email || 'admin@supporthub.com'}</div>
              </div>

              {/* Profile & Security Links */}
              <div className="py-1 space-y-0.5">
                <Link
                  to="/admin/profile"
                  onClick={() => setIsDropdownOpen(false)}
                  className={`flex items-center gap-3 px-4 py-2.5 text-xs font-semibold transition-colors rounded-lg mx-1 ${location.pathname === '/admin/profile' ? 'bg-indigo-50 text-indigo-600 font-bold' : 'text-[#1C1B2E] hover:bg-gray-50'}`}
                >
                  <User size={15} className="text-indigo-600" />
                  <span>My Profile</span>
                </Link>
                <Link
                  to="/admin/security"
                  onClick={() => setIsDropdownOpen(false)}
                  className={`flex items-center gap-3 px-4 py-2.5 text-xs font-semibold transition-colors rounded-lg mx-1 ${location.pathname === '/admin/security' ? 'bg-indigo-50 text-indigo-600 font-bold' : 'text-[#1C1B2E] hover:bg-gray-50'}`}
                >
                  <Lock size={15} className="text-indigo-600" />
                  <span>Account Security &amp; Credentials</span>
                </Link>
              </div>

              {/* Direct Channels */}
              <div className="border-t border-gray-100 pt-2.5 pb-1 px-4 mt-1">
                <div className="text-[10px] font-extrabold text-[#9598B0] uppercase tracking-wider mb-2">
                  Direct Channels
                </div>
                <div className="grid grid-cols-2 gap-1.5">
                  <Link
                    to="/admin/whatsapp"
                    onClick={() => setIsDropdownOpen(false)}
                    className={`flex items-center gap-2 p-2 rounded-xl text-[11px] font-bold border transition-colors ${
                      location.pathname === '/admin/whatsapp'
                        ? 'bg-emerald-600 text-white border-emerald-600'
                        : 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border-emerald-200/60'
                    }`}
                  >
                    <Smartphone size={14} className={location.pathname === '/admin/whatsapp' ? 'text-white' : 'text-emerald-600'} />
                    <span>WhatsApp</span>
                  </Link>

                  <Link
                    to="/admin/instagram"
                    onClick={() => setIsDropdownOpen(false)}
                    className={`flex items-center gap-2 p-2 rounded-xl text-[11px] font-bold border transition-colors ${
                      location.pathname === '/admin/instagram'
                        ? 'bg-rose-600 text-white border-rose-600'
                        : 'bg-rose-50 text-rose-700 hover:bg-rose-100 border-rose-200/60'
                    }`}
                  >
                    <Instagram size={14} className={location.pathname === '/admin/instagram' ? 'text-white' : 'text-rose-600'} />
                    <span>Instagram</span>
                  </Link>

                  <Link
                    to="/admin/email"
                    onClick={() => setIsDropdownOpen(false)}
                    className={`flex items-center gap-2 p-2 rounded-xl text-[11px] font-bold border transition-colors ${
                      location.pathname === '/admin/email'
                        ? 'bg-indigo-600 text-white border-indigo-600'
                        : 'bg-indigo-50 text-indigo-700 hover:bg-indigo-100 border-indigo-200/60'
                    }`}
                  >
                    <Mail size={14} className={location.pathname === '/admin/email' ? 'text-white' : 'text-indigo-600'} />
                    <span>Email</span>
                  </Link>

                  <Link
                    to="/admin/facebook"
                    onClick={() => setIsDropdownOpen(false)}
                    className={`flex items-center gap-2 p-2 rounded-xl text-[11px] font-bold border transition-colors ${
                      location.pathname === '/admin/facebook'
                        ? 'bg-blue-600 text-white border-blue-600'
                        : 'bg-blue-50 text-blue-700 hover:bg-blue-100 border-blue-200/60'
                    }`}
                  >
                    <Facebook size={14} className={location.pathname === '/admin/facebook' ? 'text-white' : 'text-blue-600'} />
                    <span>Facebook</span>
                  </Link>
                </div>
              </div>

              {/* Sign Out */}
              <div className="border-t border-gray-100 mt-2 pt-1 px-1">
                <button
                  onClick={handleLogout}
                  className="w-full flex items-center gap-2.5 px-3 py-2 text-xs font-bold text-rose-600 hover:bg-rose-50 rounded-xl transition-colors"
                >
                  <LogOut size={14} />
                  <span>Sign Out</span>
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}
