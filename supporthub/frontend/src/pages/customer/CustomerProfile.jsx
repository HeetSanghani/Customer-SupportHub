import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { ticketsApi } from '../../api/tickets'
import { authApi } from '../../api/auth'
import { useAuthStore } from '../../store/authStore'
import { User, Mail, MessageSquare, CheckCircle, Clock, Save, Shield, AlertCircle, Phone, MapPin, Tag, ArrowLeft } from 'lucide-react'

export default function CustomerProfile() {
  const { name, role, updateUser } = useAuthStore()
  const queryClient = useQueryClient()
  
  const [displayName, setDisplayName] = useState(name || 'Customer User')
  const [displayEmail, setDisplayEmail] = useState('')
  const [phone, setPhone] = useState('')
  const [address, setAddress] = useState('')
  const [city, setCity] = useState('')
  const [state, setState] = useState('')
  const [postalCode, setPostalCode] = useState('')
  const [country, setCountry] = useState('')
  
  const [isEditing, setIsEditing] = useState(false)
  const [savedMsg, setSavedMsg] = useState(false)
  const [errorMsg, setErrorMsg] = useState('')

  const [emailToggle, setEmailToggle] = useState(true)
  const [whatsappToggle, setWhatsappToggle] = useState(true)
  const [marketingToggle, setMarketingToggle] = useState(false)

  // Fetch user profile data
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
      setDisplayName(userProfile.name || '')
      setDisplayEmail(userProfile.email || '')
      setPhone(userProfile.phone || '')
      setAddress(userProfile.address || '')
      setCity(userProfile.city || '')
      setState(userProfile.state || '')
      setPostalCode(userProfile.postal_code || '')
      setCountry(userProfile.country || '')
    }
  }, [userProfile])

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
      setErrorMsg(err.response?.data?.detail || 'Failed to update profile.')
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
      address,
      city,
      state,
      postal_code: postalCode,
      country,
    })
  }

  return (
    <div className="flex-1 h-full overflow-y-auto bg-[#F8FAFC] p-4 md:p-8 text-[#0F172A]">
      <div className="mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <Link to="/customer" className="inline-flex items-center gap-1.5 text-xs font-extrabold text-indigo-600 hover:text-indigo-700 mb-2 transition-colors">
            <ArrowLeft size={14} /> Back to AI Chat
          </Link>
          <h1 className="text-2xl font-black text-[#0F172A] tracking-tight">Customer Profile</h1>
          <p className="text-xs md:text-sm text-[#64748B]">Manage your personal account details, shipping addresses, and communication preferences.</p>
        </div>
        {savedMsg && (
          <div className="bg-emerald-50 text-emerald-700 px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-2 border border-emerald-200">
            <CheckCircle size={14} /> Profile updated successfully!
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Left Column: Avatar & Summary Card */}
        <div className="bg-white p-6 md:p-8 rounded-3xl border border-[#E2E8F0] shadow-2xs flex flex-col items-center text-center">
          <div className="w-24 h-24 rounded-full bg-gradient-to-tr from-indigo-600 to-purple-600 text-white flex items-center justify-center text-3xl font-bold mb-4 shadow-md">
            {displayName ? displayName.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase() : 'CU'}
          </div>
          <h2 className="text-xl font-black text-[#0F172A]">{displayName}</h2>
          <div className="flex flex-col items-center gap-2 mt-2 mb-6">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-indigo-50 text-indigo-700 text-xs font-bold rounded-full border border-indigo-100">
              <Shield size={12} /> {role.toUpperCase()} ACCOUNT
            </span>
            {userProfile?.customer_id ? (
              <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs font-bold rounded-full">
                <Tag size={12} /> LINKED: {userProfile.customer_id}
              </span>
            ) : (
              <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-amber-50 text-amber-800 border border-amber-200 text-xs font-bold rounded-full">
                <AlertCircle size={12} /> UNLINKED ACCOUNT
              </span>
            )}
          </div>

          {/* Quick Stats Grid */}
          <div className="w-full grid grid-cols-3 gap-2 border-t border-[#E2E8F0] pt-6">
            <div className="bg-[#F8FAFC] p-3 rounded-2xl border border-[#E2E8F0]">
              <div className="text-lg font-bold text-[#0F172A]">{totalTickets}</div>
              <div className="text-[10px] text-[#94A3B8] font-semibold uppercase">Total</div>
            </div>
            <div className="bg-emerald-50 p-3 rounded-2xl border border-emerald-100">
              <div className="text-lg font-bold text-emerald-600">{resolvedTickets}</div>
              <div className="text-[10px] text-emerald-600 font-semibold uppercase">Solved</div>
            </div>
            <div className="bg-indigo-50 p-3 rounded-2xl border border-indigo-100">
              <div className="text-lg font-bold text-indigo-600">{activeTickets}</div>
              <div className="text-[10px] text-indigo-600 font-semibold uppercase">Active</div>
            </div>
          </div>
        </div>

        {/* Right Column: Account & Address Form */}
        <div className="md:col-span-2 space-y-6">
          <div className="bg-white p-6 md:p-8 rounded-3xl border border-[#E2E8F0] shadow-2xs">
            <div className="flex justify-between items-center mb-6">
              <h3 className="font-bold text-sm text-[#0F172A]">Personal Information & Address</h3>
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
                  <label className="text-xs text-[#94A3B8] mb-1 font-semibold block">Email Address</label>
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
                  <label className="text-xs text-[#94A3B8] mb-1 font-semibold block">Phone Number</label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={phone}
                      onChange={e => setPhone(e.target.value)}
                      placeholder="+1 (555) 000-0000"
                      className="w-full border border-[#E2E8F0] rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none font-bold"
                    />
                  ) : (
                    <div className="font-bold text-sm text-[#0F172A] flex items-center gap-2">
                      <Phone size={14} className="text-[#94A3B8]" /> {phone || 'Not specified'}
                    </div>
                  )}
                </div>

                <div>
                  <label className="text-xs text-[#94A3B8] mb-1 font-semibold block">Customer ID</label>
                  <div className="font-bold text-sm text-[#0F172A] flex items-center gap-2">
                    <Tag size={14} className="text-indigo-500" /> {userProfile?.customer_id || 'Unlinked'}
                  </div>
                </div>

                <div className="md:col-span-2">
                  <label className="text-xs text-[#94A3B8] mb-1 font-semibold block">Street Address</label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={address}
                      onChange={e => setAddress(e.target.value)}
                      placeholder="123 Main Street, Suite 100"
                      className="w-full border border-[#E2E8F0] rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none font-bold"
                    />
                  ) : (
                    <div className="font-bold text-sm text-[#0F172A] flex items-center gap-2">
                      <MapPin size={14} className="text-[#94A3B8]" /> {address || 'No street address provided'}
                    </div>
                  )}
                </div>

                <div>
                  <label className="text-xs text-[#94A3B8] mb-1 font-semibold block">City</label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={city}
                      onChange={e => setCity(e.target.value)}
                      placeholder="New York"
                      className="w-full border border-[#E2E8F0] rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none font-bold"
                    />
                  ) : (
                    <div className="font-bold text-sm text-[#0F172A]">{city || 'N/A'}</div>
                  )}
                </div>

                <div>
                  <label className="text-xs text-[#94A3B8] mb-1 font-semibold block">State / Province</label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={state}
                      onChange={e => setState(e.target.value)}
                      placeholder="NY"
                      className="w-full border border-[#E2E8F0] rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none font-bold"
                    />
                  ) : (
                    <div className="font-bold text-sm text-[#0F172A]">{state || 'N/A'}</div>
                  )}
                </div>

                <div>
                  <label className="text-xs text-[#94A3B8] mb-1 font-semibold block">Postal / Zip Code</label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={postalCode}
                      onChange={e => setPostalCode(e.target.value)}
                      placeholder="10001"
                      className="w-full border border-[#E2E8F0] rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none font-bold"
                    />
                  ) : (
                    <div className="font-bold text-sm text-[#0F172A]">{postalCode || 'N/A'}</div>
                  )}
                </div>

                <div>
                  <label className="text-xs text-[#94A3B8] mb-1 font-semibold block">Country</label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={country}
                      onChange={e => setCountry(e.target.value)}
                      placeholder="United States"
                      className="w-full border border-[#E2E8F0] rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none font-bold"
                    />
                  ) : (
                    <div className="font-bold text-sm text-[#0F172A]">{country || 'N/A'}</div>
                  )}
                </div>
              </div>

              {isEditing && (
                <div className="mb-6 flex justify-end gap-3">
                  <button
                    type="button"
                    onClick={() => {
                      setIsEditing(false)
                      setDisplayName(userProfile?.name || name)
                      setDisplayEmail(userProfile?.email || '')
                      setPhone(userProfile?.phone || '')
                      setAddress(userProfile?.address || '')
                      setCity(userProfile?.city || '')
                      setState(userProfile?.state || '')
                      setPostalCode(userProfile?.postal_code || '')
                      setCountry(userProfile?.country || '')
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

            {/* Notification Preferences */}
            <div className="space-y-5 border-t border-[#E2E8F0] pt-6">
              <h4 className="font-bold text-xs uppercase tracking-wider text-[#94A3B8]">Notification Preferences</h4>

              <div className="flex items-center justify-between">
                <div>
                  <div className="font-bold text-sm">Email Notifications</div>
                  <div className="text-xs text-[#94A3B8]">Receive updates when your support tickets change status</div>
                </div>
                <div onClick={() => setEmailToggle(!emailToggle)} className={`w-10 h-6 rounded-full p-1 cursor-pointer transition-colors ${emailToggle ? 'bg-indigo-600' : 'bg-[#E2E8F0]'}`}>
                  <div className={`w-4 h-4 bg-white rounded-full shadow-sm transition-transform ${emailToggle ? 'translate-x-4' : ''}`}></div>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <div className="font-bold text-sm">WhatsApp Updates</div>
                  <div className="text-xs text-[#94A3B8]">Receive instant notification for agent replies via WhatsApp</div>
                </div>
                <div onClick={() => setWhatsappToggle(!whatsappToggle)} className={`w-10 h-6 rounded-full p-1 cursor-pointer transition-colors ${whatsappToggle ? 'bg-indigo-600' : 'bg-[#E2E8F0]'}`}>
                  <div className={`w-4 h-4 bg-white rounded-full shadow-sm transition-transform ${whatsappToggle ? 'translate-x-4' : ''}`}></div>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <div className="font-bold text-sm">Product Announcements</div>
                  <div className="text-xs text-[#94A3B8]">Receive tips, features, and platform updates</div>
                </div>
                <div onClick={() => setMarketingToggle(!marketingToggle)} className={`w-10 h-6 rounded-full p-1 cursor-pointer transition-colors ${marketingToggle ? 'bg-indigo-600' : 'bg-[#E2E8F0]'}`}>
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
