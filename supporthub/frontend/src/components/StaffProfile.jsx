import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { authApi } from '../api/auth'
import { useAuthStore } from '../store/authStore'
import { User, Mail, Save, CheckCircle2, AlertCircle, Shield, Lock } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function StaffProfile({ basePath }) {
  const { name: storeName, email: storeEmail, role, updateUser } = useAuthStore()
  const queryClient = useQueryClient()

  const [displayName, setDisplayName] = useState(storeName || '')
  const [displayEmail, setDisplayEmail] = useState(storeEmail || '')
  const [isEditing, setIsEditing] = useState(false)
  const [savedMsg, setSavedMsg] = useState(false)
  const [errorMsg, setErrorMsg] = useState('')

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
    }
  }, [userProfile])

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
    setErrorMsg('')
    updateProfileMutation.mutate({ name: displayName.trim(), email: displayEmail.trim() })
  }

  const userInitials = displayName
    ? displayName.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
    : 'AU'

  const roleLabel = role === 'admin' ? 'Administrator' : role === 'manager' ? 'Manager' : 'Support Agent'
  const roleColor = role === 'admin' ? 'bg-indigo-100 text-indigo-700 border-indigo-200' : role === 'manager' ? 'bg-purple-100 text-purple-700 border-purple-200' : 'bg-emerald-100 text-emerald-700 border-emerald-200'

  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8 text-[#1C1B2E]">
      <div className="max-w-3xl mx-auto space-y-6">

        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">My Profile</h1>
          <p className="text-[#6C7089] text-sm mt-0.5">Manage your personal account information.</p>
        </div>

        {/* Profile Card */}
        <div className="bg-white rounded-2xl border border-[#E5E7F3] shadow-sm p-8">
          {/* Avatar + Role */}
          <div className="flex items-center gap-6 mb-8 pb-6 border-b border-[#E5E7F3]">
            <div className="w-20 h-20 rounded-2xl bg-gradient-to-tr from-indigo-500 via-purple-600 to-pink-500 text-white font-extrabold text-2xl flex items-center justify-center shadow-md shrink-0">
              {userInitials}
            </div>
            <div>
              <div className="text-xl font-bold text-[#1C1B2E]">{displayName || '—'}</div>
              <div className="text-sm text-[#6C7089] mt-0.5">{displayEmail || '—'}</div>
              <span className={`mt-2 inline-flex text-xs font-bold px-2.5 py-0.5 rounded-full border ${roleColor}`}>
                {roleLabel}
              </span>
            </div>
            {!isEditing && (
              <button
                onClick={() => setIsEditing(true)}
                className="ml-auto flex items-center gap-2 px-4 py-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-xs font-bold rounded-xl border border-indigo-200 transition-colors"
              >
                <User size={14} /> Edit Profile
              </button>
            )}
          </div>

          {/* Status messages */}
          {savedMsg && (
            <div className="mb-4 flex items-center gap-2 text-xs font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-4 py-3 rounded-xl">
              <CheckCircle2 size={15} /> Profile updated successfully!
            </div>
          )}
          {errorMsg && (
            <div className="mb-4 flex items-center gap-2 text-xs font-bold text-rose-700 bg-rose-50 border border-rose-200 px-4 py-3 rounded-xl">
              <AlertCircle size={15} /> {errorMsg}
            </div>
          )}

          {/* Edit Form or Display */}
          {isEditing ? (
            <form onSubmit={handleSave} className="space-y-5">
              <div>
                <label className="block text-xs font-bold text-[#1C1B2E] mb-1.5">Full Name</label>
                <input
                  type="text"
                  value={displayName}
                  onChange={e => setDisplayName(e.target.value)}
                  className="w-full px-4 py-3 bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500 transition-colors"
                  placeholder="Your full name"
                />
              </div>
              <div>
                <label className="block text-xs font-bold text-[#1C1B2E] mb-1.5">Email Address</label>
                <input
                  type="email"
                  value={displayEmail}
                  onChange={e => setDisplayEmail(e.target.value)}
                  className="w-full px-4 py-3 bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500 transition-colors"
                  placeholder="Your email address"
                />
              </div>
              <div className="flex gap-3 pt-2">
                <button
                  type="submit"
                  disabled={updateProfileMutation.isPending}
                  className="flex items-center gap-2 px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-xl transition-all disabled:opacity-50 shadow-sm"
                >
                  <Save size={14} />
                  {updateProfileMutation.isPending ? 'Saving...' : 'Save Changes'}
                </button>
                <button
                  type="button"
                  onClick={() => { setIsEditing(false); setErrorMsg('') }}
                  className="px-6 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 text-xs font-bold rounded-xl transition-colors"
                >
                  Cancel
                </button>
              </div>
            </form>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <div className="text-xs font-bold text-[#9598B0] uppercase tracking-wider mb-1">Full Name</div>
                <div className="text-sm font-semibold text-[#1C1B2E] flex items-center gap-2">
                  <User size={14} className="text-indigo-500" /> {displayName || '—'}
                </div>
              </div>
              <div>
                <div className="text-xs font-bold text-[#9598B0] uppercase tracking-wider mb-1">Email Address</div>
                <div className="text-sm font-semibold text-[#1C1B2E] flex items-center gap-2">
                  <Mail size={14} className="text-indigo-500" /> {displayEmail || '—'}
                </div>
              </div>
              <div>
                <div className="text-xs font-bold text-[#9598B0] uppercase tracking-wider mb-1">Role</div>
                <div className="text-sm font-semibold text-[#1C1B2E] flex items-center gap-2">
                  <Shield size={14} className="text-purple-500" /> {roleLabel}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Quick Link to Security */}
        <Link
          to={`${basePath}/security`}
          className="flex items-center justify-between bg-white rounded-2xl border border-[#E5E7F3] shadow-sm p-5 hover:border-indigo-400 hover:shadow-md transition-all group"
        >
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-indigo-50 rounded-xl flex items-center justify-center text-indigo-600 group-hover:bg-indigo-600 group-hover:text-white transition-colors">
              <Lock size={18} />
            </div>
            <div>
              <div className="text-sm font-bold text-[#1C1B2E]">Account Security &amp; Credentials</div>
              <div className="text-xs text-[#6C7089]">Change your password and manage account security</div>
            </div>
          </div>
          <span className="text-xs font-bold text-indigo-600 group-hover:underline">Manage →</span>
        </Link>
      </div>
    </div>
  )
}
