import { useState } from 'react'
import { authApi } from '../../api/auth'
import { ShieldCheck, Lock, KeyRound, Eye, EyeOff, CheckCircle2, AlertCircle, ArrowLeft, ShieldAlert, Smartphone, Laptop, Check } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function CustomerSecuritySettings() {
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  const [showCurrentPassword, setShowCurrentPassword] = useState(false)
  const [showNewPassword, setShowNewPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)

  const [twoFactorEnabled, setTwoFactorEnabled] = useState(false)
  const [statusMessage, setStatusMessage] = useState(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Password strength calculation
  const getPasswordStrength = (pwd) => {
    if (!pwd) return { score: 0, label: '', color: 'bg-gray-200' }
    let score = 0
    if (pwd.length >= 8) score += 1
    if (/[A-Z]/.test(pwd)) score += 1
    if (/[0-9]/.test(pwd)) score += 1
    if (/[^A-Za-z0-9]/.test(pwd)) score += 1

    if (score <= 1) return { score: 25, label: 'Weak', color: 'bg-rose-500', text: 'text-rose-600' }
    if (score === 2 || score === 3) return { score: 65, label: 'Medium', color: 'bg-amber-500', text: 'text-amber-600' }
    return { score: 100, label: 'Strong', color: 'bg-emerald-500', text: 'text-emerald-600' }
  }

  const strength = getPasswordStrength(newPassword)

  const handlePasswordSubmit = async (e) => {
    e.preventDefault()
    setStatusMessage(null)

    if (!currentPassword) {
      setStatusMessage({ type: 'error', text: 'Please enter your current password.' })
      return
    }
    if (newPassword.length < 6) {
      setStatusMessage({ type: 'error', text: 'New password must be at least 6 characters long.' })
      return
    }
    if (newPassword !== confirmPassword) {
      setStatusMessage({ type: 'error', text: 'New password and confirmation do not match.' })
      return
    }

    setIsSubmitting(true)
    try {
      await authApi.changePassword({
        current_password: currentPassword,
        new_password: newPassword,
      })
      setStatusMessage({ type: 'success', text: 'Your password has been changed successfully!' })
      setCurrentPassword('')
      setNewPassword('')
      setConfirmPassword('')
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Failed to update password. Please try again.'
      setStatusMessage({ type: 'error', text: msg })
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="flex-1 h-full overflow-y-auto bg-[#F8FAFC] p-4 md:p-8 text-[#0F172A] space-y-6">
      {/* Top Banner */}
      <div className="bg-white p-6 rounded-3xl border border-[#E2E8F0] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <Link to="/customer" className="inline-flex items-center gap-1.5 text-xs font-extrabold text-indigo-600 hover:text-indigo-700 mb-2 transition-colors">
            <ArrowLeft size={14} /> Back to AI Chat
          </Link>
          <h1 className="text-2xl font-black text-[#0F172A] tracking-tight flex items-center gap-2">
            Account Security & Credentials
            <span className="text-xs font-bold bg-emerald-50 text-emerald-700 px-2.5 py-0.5 rounded-full border border-emerald-200">
              Protected
            </span>
          </h1>
          <p className="text-xs md:text-sm text-[#64748B] mt-0.5">Manage your master password, 2FA authorization keys, and active device sessions.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Password Update Form */}
        <div className="lg:col-span-2 bg-white border border-[#E2E8F0] rounded-3xl p-6 md:p-8 shadow-2xs space-y-6">
          <div className="flex items-center gap-3 border-b border-[#F1F5F9] pb-4">
            <div className="p-2.5 bg-indigo-50 text-indigo-600 rounded-2xl border border-indigo-100">
              <KeyRound size={22} />
            </div>
            <div>
              <h2 className="text-lg font-black text-[#0F172A]">Change Password</h2>
              <p className="text-xs text-[#64748B]">Update your account password regularly for optimal security.</p>
            </div>
          </div>

          {statusMessage && (
            <div className={`p-4 rounded-2xl text-xs font-bold flex items-center gap-2.5 border ${
              statusMessage.type === 'success' 
                ? 'bg-emerald-50 text-emerald-800 border-emerald-200' 
                : 'bg-rose-50 text-rose-800 border-rose-200'
            }`}>
              {statusMessage.type === 'success' ? <CheckCircle2 size={16} /> : <AlertCircle size={16} />}
              <span>{statusMessage.text}</span>
            </div>
          )}

          <form onSubmit={handlePasswordSubmit} className="space-y-4">
            {/* Current Password */}
            <div>
              <label className="block text-xs font-bold text-[#0F172A] mb-1.5">Current Password</label>
              <div className="relative">
                <input
                  type={showCurrentPassword ? 'text' : 'password'}
                  value={currentPassword}
                  onChange={e => setCurrentPassword(e.target.value)}
                  placeholder="••••••••••••"
                  className="w-full px-4 py-3 bg-[#F8FAFC] border border-[#E2E8F0] rounded-2xl text-sm focus:outline-none focus:border-indigo-500 font-mono pr-12 transition-colors"
                />
                <button
                  type="button"
                  onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 p-1"
                >
                  {showCurrentPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            {/* New Password */}
            <div>
              <label className="block text-xs font-bold text-[#0F172A] mb-1.5">New Password</label>
              <div className="relative">
                <input
                  type={showNewPassword ? 'text' : 'password'}
                  value={newPassword}
                  onChange={e => setNewPassword(e.target.value)}
                  placeholder="••••••••••••"
                  className="w-full px-4 py-3 bg-[#F8FAFC] border border-[#E2E8F0] rounded-2xl text-sm focus:outline-none focus:border-indigo-500 font-mono pr-12 transition-colors"
                />
                <button
                  type="button"
                  onClick={() => setShowNewPassword(!showNewPassword)}
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 p-1"
                >
                  {showNewPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>

              {/* Password Strength Indicator */}
              {newPassword && (
                <div className="mt-2.5 space-y-1">
                  <div className="flex justify-between items-center text-[11px] font-bold">
                    <span className="text-[#64748B]">Password Strength</span>
                    <span className={strength.text}>{strength.label}</span>
                  </div>
                  <div className="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
                    <div className={`h-full transition-all duration-300 ${strength.color}`} style={{ width: `${strength.score}%` }}></div>
                  </div>
                </div>
              )}
            </div>

            {/* Confirm New Password */}
            <div>
              <label className="block text-xs font-bold text-[#0F172A] mb-1.5">Confirm New Password</label>
              <div className="relative">
                <input
                  type={showConfirmPassword ? 'text' : 'password'}
                  value={confirmPassword}
                  onChange={e => setConfirmPassword(e.target.value)}
                  placeholder="••••••••••••"
                  className="w-full px-4 py-3 bg-[#F8FAFC] border border-[#E2E8F0] rounded-2xl text-sm focus:outline-none focus:border-indigo-500 font-mono pr-12 transition-colors"
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 p-1"
                >
                  {showConfirmPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full py-3.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl text-xs font-extrabold shadow-md transition-all active:scale-[0.99] disabled:opacity-50 mt-2"
            >
              {isSubmitting ? 'Updating Password...' : 'Save Password Changes'}
            </button>
          </form>
        </div>

        {/* Right Column: Security Features & Active Devices */}
        <div className="space-y-6">
          {/* Two-Factor Authentication Card */}
          <div className="bg-white border border-[#E2E8F0] rounded-3xl p-6 shadow-2xs space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="p-2 bg-emerald-50 text-emerald-600 rounded-xl">
                  <Smartphone size={20} />
                </div>
                <div>
                  <h3 className="font-extrabold text-sm text-[#0F172A]">Two-Factor Auth</h3>
                  <p className="text-[11px] text-[#64748B]">SMS or Authenticator Code</p>
                </div>
              </div>
              <button
                onClick={() => setTwoFactorEnabled(!twoFactorEnabled)}
                className={`w-12 h-6 rounded-full transition-colors relative p-1 ${twoFactorEnabled ? 'bg-indigo-600' : 'bg-gray-200'}`}
              >
                <div className={`w-4 h-4 bg-white rounded-full transition-transform ${twoFactorEnabled ? 'translate-x-6' : 'translate-x-0'}`}></div>
              </button>
            </div>
            <p className="text-xs text-[#64748B] leading-relaxed">
              Add an extra layer of protection to your account by requiring a verification code upon login.
            </p>
          </div>

          {/* Active Device Session */}
          <div className="bg-white border border-[#E2E8F0] rounded-3xl p-6 shadow-2xs space-y-4">
            <h3 className="font-extrabold text-sm text-[#0F172A] flex items-center gap-2">
              <Laptop size={18} className="text-indigo-600" /> Active Session
            </h3>
            <div className="p-3.5 bg-[#F8FAFC] rounded-2xl border border-[#F1F5F9] text-xs space-y-1">
              <div className="font-bold text-[#0F172A] flex items-center justify-between">
                <span>Linux Chrome Browser</span>
                <span className="text-[10px] font-extrabold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">Current</span>
              </div>
              <div className="text-[11px] text-[#64748B]">IP: 127.0.0.1 (Local Session)</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
