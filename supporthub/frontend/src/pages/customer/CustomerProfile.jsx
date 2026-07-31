import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { ticketsApi } from '../../api/tickets'
import { useAuthStore } from '../../store/authStore'
import { User, Mail, MessageSquare, CheckCircle, Clock, Save, Shield } from 'lucide-react'

export default function CustomerProfile() {
  const { name, role } = useAuthStore()
  const [displayName, setDisplayName] = useState(name || 'Customer User')
  const [isEditing, setIsEditing] = useState(false)
  const [savedMsg, setSavedMsg] = useState(false)

  const [emailToggle, setEmailToggle] = useState(true)
  const [whatsappToggle, setWhatsappToggle] = useState(true)
  const [marketingToggle, setMarketingToggle] = useState(false)

  const { data: tickets = [] } = useQuery({
    queryKey: ['tickets', 'customer'],
    queryFn: async () => {
      const res = await ticketsApi.list()
      return res.data
    },
  })

  const totalTickets = tickets.length
  const activeTickets = tickets.filter(t => t.status !== 'resolved' && t.status !== 'closed').length
  const resolvedTickets = tickets.filter(t => t.status === 'resolved' || t.status === 'closed').length

  const handleSave = (e) => {
    e.preventDefault()
    setIsEditing(false)
    setSavedMsg(true)
    setTimeout(() => setSavedMsg(false), 3000)
  }

  const email = displayName.toLowerCase().replace(/\s+/g, '.') + '@example.com'

  return (
    <div className="flex-1 overflow-auto bg-[#F9FAFB] p-8 text-[#1C1B2E]">
      <div className="mb-6 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">Customer Profile</h1>
          <p className="text-[#6C7089] text-sm">Manage your personal information and support stats.</p>
        </div>
        {savedMsg && (
          <div className="bg-emerald-50 text-emerald-600 px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-2 border border-emerald-200">
            <CheckCircle size={14} /> Profile updated successfully!
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Left Column: Card */}
        <div className="bg-white p-8 rounded-2xl border border-[#E5E7F3] shadow-sm flex flex-col items-center text-center">
          <div className="w-24 h-24 rounded-full bg-gradient-to-tr from-[#6366F1] to-[#A855F7] text-white flex items-center justify-center text-3xl font-bold mb-4 shadow-md">
            {displayName.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()}
          </div>
          <h2 className="text-xl font-bold font-['Plus_Jakarta_Sans']">{displayName}</h2>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-indigo-50 text-indigo-600 text-xs font-bold rounded-full mt-2 mb-6">
            <Shield size={12} /> {role.toUpperCase()} ACCOUNT
          </div>

          {/* Quick Stats Grid */}
          <div className="w-full grid grid-cols-3 gap-2 border-t border-[#E5E7F3] pt-6">
            <div className="bg-gray-50 p-3 rounded-xl border border-[#E5E7F3]">
              <div className="text-lg font-bold text-[#1C1B2E]">{totalTickets}</div>
              <div className="text-[10px] text-[#9598B0] font-semibold uppercase">Total</div>
            </div>
            <div className="bg-emerald-50 p-3 rounded-xl border border-emerald-100">
              <div className="text-lg font-bold text-emerald-600">{resolvedTickets}</div>
              <div className="text-[10px] text-emerald-600 font-semibold uppercase">Solved</div>
            </div>
            <div className="bg-indigo-50 p-3 rounded-xl border border-indigo-100">
              <div className="text-lg font-bold text-indigo-600">{activeTickets}</div>
              <div className="text-[10px] text-indigo-600 font-semibold uppercase">Active</div>
            </div>
          </div>
        </div>

        {/* Right Column: Account Form & Settings */}
        <div className="md:col-span-2 space-y-6">
          <div className="bg-white p-8 rounded-2xl border border-[#E5E7F3] shadow-sm">
            <div className="flex justify-between items-center mb-6">
              <h3 className="font-bold text-sm text-[#1C1B2E]">Account Information</h3>
              <button
                onClick={() => setIsEditing(!isEditing)}
                className="text-xs font-bold text-indigo-600 hover:text-indigo-800 transition-colors"
              >
                {isEditing ? 'Cancel' : 'Edit Profile'}
              </button>
            </div>

            <form onSubmit={handleSave}>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div>
                  <label className="text-xs text-[#9598B0] mb-1 font-semibold block">Full Name</label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={displayName}
                      onChange={e => setDisplayName(e.target.value)}
                      className="w-full border border-[#E5E7F3] rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none font-bold"
                    />
                  ) : (
                    <div className="font-bold text-sm text-[#1C1B2E]">{displayName}</div>
                  )}
                </div>

                <div>
                  <label className="text-xs text-[#9598B0] mb-1 font-semibold block">Email Address</label>
                  <div className="font-bold text-sm text-[#1C1B2E] flex items-center gap-2">
                    <Mail size={14} className="text-[#9598B0]" /> {email}
                  </div>
                </div>

                <div>
                  <label className="text-xs text-[#9598B0] mb-1 font-semibold block">Support Tier</label>
                  <div className="font-bold text-sm text-[#1C1B2E] flex items-center gap-2">
                    <MessageSquare size={14} className="text-indigo-500" /> Standard AI Support
                  </div>
                </div>

                <div>
                  <label className="text-xs text-[#9598B0] mb-1 font-semibold block">Preferred Channel</label>
                  <div className="font-bold text-sm text-[#1C1B2E] flex items-center gap-2">
                    <Clock size={14} className="text-emerald-500" /> Live Web Chat
                  </div>
                </div>
              </div>

              {isEditing && (
                <div className="mb-6 flex justify-end">
                  <button
                    type="submit"
                    className="bg-[#6366F1] hover:bg-[#4F46E5] text-white px-5 py-2 rounded-xl font-bold text-sm flex items-center gap-2 transition-colors shadow-sm"
                  >
                    <Save size={16} /> Save Changes
                  </button>
                </div>
              )}
            </form>

            {/* Notification Preferences */}
            <div className="space-y-5 border-t border-[#E5E7F3] pt-6">
              <h4 className="font-bold text-xs uppercase tracking-wider text-[#9598B0]">Notification Preferences</h4>

              <div className="flex items-center justify-between">
                <div>
                  <div className="font-bold text-sm">Email Notifications</div>
                  <div className="text-xs text-[#9598B0]">Receive updates when your support tickets change status</div>
                </div>
                <div onClick={() => setEmailToggle(!emailToggle)} className={`w-10 h-6 rounded-full p-1 cursor-pointer transition-colors ${emailToggle ? 'bg-[#6366F1]' : 'bg-[#E5E7F3]'}`}>
                  <div className={`w-4 h-4 bg-white rounded-full shadow-sm transition-transform ${emailToggle ? 'translate-x-4' : ''}`}></div>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <div className="font-bold text-sm">WhatsApp Updates</div>
                  <div className="text-xs text-[#9598B0]">Receive instant notification for agent replies via WhatsApp</div>
                </div>
                <div onClick={() => setWhatsappToggle(!whatsappToggle)} className={`w-10 h-6 rounded-full p-1 cursor-pointer transition-colors ${whatsappToggle ? 'bg-[#6366F1]' : 'bg-[#E5E7F3]'}`}>
                  <div className={`w-4 h-4 bg-white rounded-full shadow-sm transition-transform ${whatsappToggle ? 'translate-x-4' : ''}`}></div>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <div className="font-bold text-sm">Product Announcements</div>
                  <div className="text-xs text-[#9598B0]">Receive tips, features, and platform updates</div>
                </div>
                <div onClick={() => setMarketingToggle(!marketingToggle)} className={`w-10 h-6 rounded-full p-1 cursor-pointer transition-colors ${marketingToggle ? 'bg-[#6366F1]' : 'bg-[#E5E7F3]'}`}>
                  <div className={`w-4 h-4 bg-white rounded-full shadow-sm transition-transform ${marketingToggle ? 'translate-x-4' : ''}`}></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}



