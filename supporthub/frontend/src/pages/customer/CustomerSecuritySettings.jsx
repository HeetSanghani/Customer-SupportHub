import { useState } from 'react'
import { authApi } from '../../api/auth'
import { KeyRound, ShieldCheck, CheckCircle2, AlertCircle, ArrowLeft } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function CustomerSecuritySettings() {
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [statusMsg, setStatusMsg] = useState({ type: '', text: '' })
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setStatusMsg({ type: '', text: '' })

    if (!currentPassword || !newPassword || !confirmPassword) {
      setStatusMsg({ type: 'error', text: 'Please complete all password fields.' })
      return
    }

    if (newPassword !== confirmPassword) {
      setStatusMsg({ type: 'error', text: 'New password and confirmation do not match.' })
      return
    }

    if (newPassword.length < 8) {
      setStatusMsg({ type: 'error', text: 'New password must be at least 8 characters long.' })
      return
    }

    setLoading(true)
    try {
      await authApi.changePassword({
        current_password: currentPassword,
        new_password: newPassword,
        confirm_password: confirmPassword,
      })
      setStatusMsg({ type: 'success', text: 'Password updated successfully! Next login will require your new password.' })
      setCurrentPassword('')
      setNewPassword('')
      setConfirmPassword('')
    } catch (err) {
      const detail = err.response?.data?.detail || 'Failed to update password. Please check your current password.'
      setStatusMsg({ type: 'error', text: detail })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex-1 overflow-y-auto bg-[#F6F7FC] p-8 space-y-8 max-w-4xl">
      <div>
        <div className="flex items-center gap-2 text-xs text-[#6C7089] mb-1">
          <Link to="/customer" className="hover:text-indigo-600 flex items-center gap-1"><ArrowLeft size={12}/> Dashboard</Link> / Security Settings
        </div>
        <h1 className="text-2xl font-bold text-[#1C1B2E]">Account Security & Password</h1>
        <p className="text-sm text-[#6C7089]">Update your authentication credentials and manage security preferences.</p>
      </div>

      <div className="bg-white border border-[#E5E7F3] rounded-2xl p-8 shadow-sm space-y-6">
        <div className="flex items-center gap-3 border-b border-[#F0F1F7] pb-4">
          <div className="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold">
            <KeyRound size={20} />
          </div>
          <div>
            <h2 className="text-lg font-bold text-[#1C1B2E]">Change Password</h2>
            <p className="text-xs text-[#6C7089]">Enforce strong password requirements for account protection.</p>
          </div>
        </div>

        {statusMsg.text && (
          <div className={`p-4 rounded-xl text-sm font-semibold flex items-center gap-3 ${
            statusMsg.type === 'success' ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' : 'bg-rose-50 text-rose-800 border border-rose-200'
          }`}>
            {statusMsg.type === 'success' ? <CheckCircle2 size={18} className="text-emerald-500"/> : <AlertCircle size={18} className="text-rose-500"/>}
            {statusMsg.text}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5 max-w-md">
          <div>
            <label className="block text-xs font-bold text-[#1C1B2E] mb-1.5">Current Password</label>
            <input
              type="password"
              value={currentPassword}
              onChange={e => setCurrentPassword(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl border border-[#E5E7F3] text-sm focus:outline-none focus:border-indigo-600"
              placeholder="Enter current password"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-[#1C1B2E] mb-1.5">New Password</label>
            <input
              type="password"
              value={newPassword}
              onChange={e => setNewPassword(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl border border-[#E5E7F3] text-sm focus:outline-none focus:border-indigo-600"
              placeholder="At least 8 characters"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-[#1C1B2E] mb-1.5">Confirm New Password</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={e => setConfirmPassword(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl border border-[#E5E7F3] text-sm focus:outline-none focus:border-indigo-600"
              placeholder="Re-enter new password"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-sm font-semibold transition-colors shadow-sm disabled:opacity-50"
          >
            {loading ? 'Updating Password...' : 'Update Password'}
          </button>
        </form>
      </div>
    </div>
  )
}
