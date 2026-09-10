import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { authApi } from '../../api/auth'
import { ticketsApi } from '../../api/tickets'
import { useAuthStore } from '../../store/authStore'
import { 
  User, Mail, Phone, Shield, Save, CheckCircle, Clock, 
  AlertCircle, Star, Award, Zap, Bell, CheckCircle2, ArrowLeft
} from 'lucide-react'

export default function AgentProfile() {
  const { name, role, email: storeEmail, updateUser } = useAuthStore()
  const queryClient = useQueryClient()

  const [displayName, setDisplayName] = useState(name || 'Agent User')
  const [displayEmail, setDisplayEmail] = useState(storeEmail || 'agent@supporthub.com')
  const [phone, setPhone] = useState('+1 (555) 382-9901')
  const [department, setDepartment] = useState('Customer Experience & Escalations')
  const [shiftHours, setShiftHours] = useState('09:00 AM - 05:00 PM EST')

  const [isEditing, setIsEditing] = useState(false)
  const [savedMsg, setSavedMsg] = useState(false)
  const [errorMsg, setErrorMsg] = useState('')

  // Notification Toggles
  const [emailAlerts, setEmailAlerts] = useState(true)
  const [browserNotifications, setBrowserNotifications] = useState(true)
  const [autoAssignment, setAutoAssignment] = useState(true)

  // Fetch agent user details
  const { data: userProfile } = useQuery({
    queryKey: ['auth', 'me'],
    queryFn: async () => {
      const res = await authApi.me()
      return res.data
    },
    staleTime: 1000 * 60 * 5
  })

  useEffect(() => {
    if (userProfile) {
      setDisplayName(userProfile.name || name || 'Agent User')
      setDisplayEmail(userProfile.email || storeEmail || 'agent@supporthub.com')
      if (userProfile.phone) setPhone(userProfile.phone)
    }
  }, [userProfile, name, storeEmail])

  // Fetch human tickets assigned / handled
  const { data: tickets = [] } = useQuery({
    queryKey: ['tickets', 'agent-profile-tickets'],
    queryFn: async () => {
      const res = await ticketsApi.list({ human_only: true })
      return res.data
    },
  })

  const totalAssigned = tickets.length
  const activeHumanTickets = tickets.filter(t => t.status === 'open' || t.status === 'escalated').length
  const resolvedCount = tickets.filter(t => t.status === 'resolved' || t.status === 'closed').length

  const updateProfileMutation = useMutation({
    mutationFn: (data) => authApi.updateMe(data),
    onSuccess: (res) => {
      setIsEditing(false)
      setSavedMsg(true)
      setErrorMsg('')
      updateUser(res.data.name)
      queryClient.invalidateQueries(['auth', 'me'])
      setTimeout(() => setSavedMsg(false), 3000)
    },
    onError: (err) => {
      setErrorMsg(err.response?.data?.detail || 'Failed to update agent profile.')
    }
  })

  const handleSave = (e) => {
    e.preventDefault()
    if (!displayName.trim() || !displayEmail.trim()) {
      setErrorMsg('Name and email are required.')
      return
    }
    updateProfileMutation.mutate({
      name: displayName,
      email: displayEmail,
      phone,
    })
  }

  const userInitials = displayName
    ? displayName.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
    : 'EW'

  return (
    <div className="flex-1 h-full overflow-y-auto bg-[#F8FAFC] p-4 md:p-8 text-[#0F172A]">
      {/* Header Banner */}
      <div className="mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <Link to="/agent" className="inline-flex items-center gap-1.5 text-xs font-extrabold text-indigo-600 hover:text-indigo-700 mb-2 transition-colors">
            <ArrowLeft size={14} /> Back to Agent Dashboard
          </Link>
          <h1 className="text-2xl font-black text-[#0F172A] tracking-tight">Agent Profile & Performance</h1>
          <p className="text-xs md:text-sm text-[#64748B]">Manage your support credentials, shift availability, and review performance metrics.</p>
        </div>
        {savedMsg && (
          <div className="bg-emerald-50 text-emerald-700 px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-2 border border-emerald-200 shadow-2xs">
            <CheckCircle2 size={16} /> Profile changes saved!
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Left Column: Agent Badge & Metrics Card */}
        <div className="space-y-6">
          <div className="bg-white p-6 md:p-8 rounded-3xl border border-[#E2E8F0] shadow-2xs flex flex-col items-center text-center relative overflow-hidden">
            <div className="absolute top-0 left-0 right-0 h-2 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500"></div>

            <div className="w-24 h-24 rounded-2xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-500 text-white flex items-center justify-center text-3xl font-extrabold mb-4 shadow-md mt-2">
              {userInitials}
            </div>
            
            <h2 className="text-xl font-black text-[#0F172A]">{displayName}</h2>
            <div className="text-xs text-[#64748B] font-semibold mt-0.5">{department}</div>

            <div className="flex flex-wrap items-center justify-center gap-2 mt-3 mb-6">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-indigo-50 text-indigo-700 text-xs font-bold rounded-full border border-indigo-100">
                <Shield size={12} /> {role ? role.toUpperCase() : 'AGENT'} ROLE
              </span>
              <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-emerald-50 text-emerald-700 text-xs font-bold rounded-full border border-emerald-200">
                <CheckCircle size={12} /> Active Duty
              </span>
            </div>

            {/* CSAT Performance */}
            <div className="w-full bg-gradient-to-r from-amber-50 to-orange-50 p-4 rounded-2xl border border-amber-200 mb-4">
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-extrabold text-amber-900 uppercase tracking-wider flex items-center gap-1">
                  <Star size={14} className="text-amber-500 fill-amber-400" /> CSAT Rating
                </span>
                <span className="text-lg font-black text-amber-700">5.0 / 5.0</span>
              </div>
              <div className="text-[11px] text-amber-800 text-left font-medium">100% positive customer feedback on human interventions.</div>
            </div>

            {/* Quick Performance Grid */}
            <div className="w-full grid grid-cols-3 gap-2 border-t border-[#E2E8F0] pt-6">
              <div className="bg-[#F8FAFC] p-3 rounded-2xl border border-[#E2E8F0]">
                <div className="text-lg font-black text-[#0F172A]">{totalAssigned}</div>
                <div className="text-[10px] text-[#94A3B8] font-semibold uppercase">Assigned</div>
              </div>
              <div className="bg-indigo-50 p-3 rounded-2xl border border-indigo-100">
                <div className="text-lg font-black text-indigo-600">{activeHumanTickets}</div>
                <div className="text-[10px] text-indigo-600 font-semibold uppercase">Active</div>
              </div>
              <div className="bg-emerald-50 p-3 rounded-2xl border border-emerald-100">
                <div className="text-lg font-black text-emerald-600">{resolvedCount}</div>
                <div className="text-[10px] text-emerald-600 font-semibold uppercase">Solved</div>
              </div>
            </div>
          </div>

          {/* Achievement Badge Card */}
          <div className="bg-white p-6 rounded-3xl border border-[#E2E8F0] shadow-2xs">
            <h3 className="text-xs font-extrabold text-[#94A3B8] uppercase tracking-wider mb-4 flex items-center gap-2">
              <Award size={16} className="text-indigo-600" /> Agent Recognition
            </h3>
            <div className="space-y-3">
              <div className="flex items-center gap-3 p-3 bg-indigo-50/50 rounded-2xl border border-indigo-100">
                <div className="p-2 bg-indigo-600 text-white rounded-xl">
                  <Zap size={18} />
                </div>
                <div>
                  <div className="text-xs font-bold text-[#0F172A]">Top Escalation Resolver</div>
                  <div className="text-[10px] text-[#64748B]">Fast average response time under 3 mins</div>
                </div>
              </div>

              <div className="flex items-center gap-3 p-3 bg-emerald-50/50 rounded-2xl border border-emerald-100">
                <div className="p-2 bg-emerald-600 text-white rounded-xl">
                  <Star size={18} />
                </div>
                <div>
                  <div className="text-xs font-bold text-[#0F172A]">5-Star Customer Champion</div>
                  <div className="text-[10px] text-[#64748B]">Maintained perfect satisfaction rating</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Information & Settings Form */}
        <div className="md:col-span-2 space-y-6">
          <div className="bg-white p-6 md:p-8 rounded-3xl border border-[#E2E8F0] shadow-2xs">
            <div className="flex justify-between items-center mb-6">
              <h3 className="font-bold text-sm text-[#0F172A]">Agent Details & Workstation Info</h3>
              {!isEditing && (
                <button
                  type="button"
                  onClick={() => setIsEditing(true)}
                  className="text-xs font-extrabold text-indigo-600 hover:text-indigo-800 transition-colors"
                >
                  Edit Profile
                </button>
              )}
            </div>

            <form onSubmit={handleSave}>
              {errorMsg && (
                <div className="mb-4 bg-rose-50 text-rose-700 px-4 py-3 rounded-xl text-xs font-bold flex items-center gap-2 border border-rose-200">
                  <AlertCircle size={14} /> {errorMsg}
                </div>
              )}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div>
                  <label className="text-xs text-[#94A3B8] mb-1 font-semibold block">Full Name</label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={displayName}
                      onChange={e => setDisplayName(e.target.value)}
                      className="w-full border border-[#E2E8F0] rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none font-bold"
                    />
                  ) : (
                    <div className="font-bold text-sm text-[#0F172A]">{displayName}</div>
                  )}
                </div>

                <div>
                  <label className="text-xs text-[#94A3B8] mb-1 font-semibold block">Agent Email</label>
                  {isEditing ? (
                    <input
                      type="email"
                      value={displayEmail}
                      onChange={e => setDisplayEmail(e.target.value)}
                      className="w-full border border-[#E2E8F0] rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none font-bold"
                    />
                  ) : (
                    <div className="font-bold text-sm text-[#0F172A] flex items-center gap-2">
                      <Mail size={14} className="text-[#94A3B8]" /> {displayEmail}
                    </div>
                  )}
                </div>

                <div>
                  <label className="text-xs text-[#94A3B8] mb-1 font-semibold block">Direct Phone</label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={phone}
                      onChange={e => setPhone(e.target.value)}
                      className="w-full border border-[#E2E8F0] rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none font-bold"
                    />
                  ) : (
                    <div className="font-bold text-sm text-[#0F172A] flex items-center gap-2">
                      <Phone size={14} className="text-[#94A3B8]" /> {phone}
                    </div>
                  )}
                </div>

                <div>
                  <label className="text-xs text-[#94A3B8] mb-1 font-semibold block">Department</label>
                  <div className="font-bold text-sm text-[#0F172A]">{department}</div>
                </div>

                <div>
                  <label className="text-xs text-[#94A3B8] mb-1 font-semibold block">Assigned Shift</label>
                  <div className="font-bold text-sm text-[#0F172A] flex items-center gap-1.5">
                    <Clock size={14} className="text-indigo-600" /> {shiftHours}
                  </div>
                </div>

                <div>
                  <label className="text-xs text-[#94A3B8] mb-1 font-semibold block">Assigned Role</label>
                  <div className="font-bold text-sm text-indigo-700 uppercase flex items-center gap-1.5">
                    <Shield size={14} className="text-indigo-600" /> {role || 'Agent'}
                  </div>
                </div>
              </div>

              {isEditing && (
                <div className="mb-6 flex justify-end gap-3">
                  <button
                    type="button"
                    onClick={() => {
                      setIsEditing(false)
                      setDisplayName(userProfile?.name || name || 'Agent User')
                      setDisplayEmail(userProfile?.email || storeEmail || 'agent@supporthub.com')
                      setErrorMsg('')
                    }}
                    className="px-5 py-2 rounded-xl font-bold text-sm text-gray-600 hover:bg-gray-100 transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={updateProfileMutation.isPending}
                    className="bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2 rounded-xl font-bold text-sm flex items-center gap-2 transition-colors shadow-sm disabled:opacity-50"
                  >
                    <Save size={16} /> {updateProfileMutation.isPending ? 'Saving...' : 'Save Changes'}
                  </button>
                </div>
              )}
            </form>

            {/* Agent Workflow Preferences */}
            <div className="space-y-5 border-t border-[#E2E8F0] pt-6">
              <h4 className="font-bold text-xs uppercase tracking-wider text-[#94A3B8] flex items-center gap-2">
                <Bell size={14} className="text-indigo-600" /> Workflow & Escalation Preferences
              </h4>

              <div className="flex items-center justify-between">
                <div>
                  <div className="font-bold text-sm text-[#0F172A]">Real-time Escalation Sound & Browser Alerts</div>
                  <div className="text-xs text-[#64748B]">Play sound when a customer requests a human agent</div>
                </div>
                <div onClick={() => setBrowserNotifications(!browserNotifications)} className={`w-10 h-6 rounded-full p-1 cursor-pointer transition-colors ${browserNotifications ? 'bg-indigo-600' : 'bg-[#E2E8F0]'}`}>
                  <div className={`w-4 h-4 bg-white rounded-full shadow-sm transition-transform ${browserNotifications ? 'translate-x-4' : ''}`}></div>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <div className="font-bold text-sm text-[#0F172A]">Email Alerts for High Priority Escalations</div>
                  <div className="text-xs text-[#64748B]">Receive email digest for urgent tickets assigned to your queue</div>
                </div>
                <div onClick={() => setEmailAlerts(!emailAlerts)} className={`w-10 h-6 rounded-full p-1 cursor-pointer transition-colors ${emailAlerts ? 'bg-indigo-600' : 'bg-[#E2E8F0]'}`}>
                  <div className={`w-4 h-4 bg-white rounded-full shadow-sm transition-transform ${emailAlerts ? 'translate-x-4' : ''}`}></div>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <div className="font-bold text-sm text-[#0F172A]">Automatic Ticket Routing</div>
                  <div className="text-xs text-[#64748B]">Allow system to automatically route incoming human requests to your active queue</div>
                </div>
                <div onClick={() => setAutoAssignment(!autoAssignment)} className={`w-10 h-6 rounded-full p-1 cursor-pointer transition-colors ${autoAssignment ? 'bg-indigo-600' : 'bg-[#E2E8F0]'}`}>
                  <div className={`w-4 h-4 bg-white rounded-full shadow-sm transition-transform ${autoAssignment ? 'translate-x-4' : ''}`}></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
