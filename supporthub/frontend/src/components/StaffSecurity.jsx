import { useState } from 'react'
import { authApi } from '../api/auth'
import { KeyRound, Eye, EyeOff, CheckCircle2, AlertCircle, Smartphone, Laptop, Lock } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function StaffSecurity({ basePath }) {
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  const [showCurrentPassword, setShowCurrentPassword] = useState(false)
  const [showNewPassword, setShowNewPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)

  const [twoFactorEnabled, setTwoFactorEnabled] = useState(false)
  const [statusMessage, setStatusMessage] = useState(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const getPasswordStrength = (pwd) => {
    if (!pwd) return { score: 0, label: '', color: 'bg-gray-200', text: 'text-gray-500' }
    let score = 0
    if (pwd.length >= 8) score += 1
    if (/[A-Z]/.test(pwd)) score += 1
    if (/[0-9]/.test(pwd)) score += 1
    if (/[^A-Za-z0-9]/.test(pwd)) score += 1
    if (score <= 1) return { score: 25, label: 'Weak', color: 'bg-rose-500', text: 'text-rose-600' }
    if (score <= 3) return { score: 65, label: 'Medium', color: 'bg-amber-500', text: 'text-amber-600' }
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
      await authApi.changePassword({ current_password: currentPassword, new_password: newPassword })
      setStatusMessage({ type: 'success', text: 'Password changed successfully!' })
      setCurrentPassword('')
      setNewPassword('')
      setConfirmPassword('')
    } catch (err) {
      const msg = err.response?.data?.detail || 'Failed to update password. Please try again.'
      setStatusMessage({ type: 'error', text: msg })
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8 text-[#1C1B2E]">
      <div className="max-w-3xl mx-auto space-y-6">

        {/* Header */}
        <div>
          <Link
            to={`${basePath}/profile`}
            className="inline-flex items-center gap-1.5 text-xs font-bold text-indigo-600 hover:text-indigo-700 mb-3 transition-colors"
          >
            ← Back to Profile
          </Link>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">Account Security &amp; Credentials</h1>
            <span className="text-xs font-bold bg-emerald-50 text-emerald-700 px-2.5 py-0.5 rounded-full border border-emerald-200">
              Protected
            </span>
          </div>
          <p className="text-[#6C7089] text-sm mt-0.5">Manage your password and account security settings.</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left: Change Password Form */}
          <div className="lg:col-span-2 bg-white rounded-2xl border border-[#E5E7F3] shadow-sm p-6 space-y-5">
            <div className="flex items-center gap-3 border-b border-[#E5E7F3] pb-4">
              <div className="p-2.5 bg-indigo-50 text-indigo-600 rounded-xl border border-indigo-100">
                <KeyRound size={20} />
              </div>
              <div>
                <h2 className="text-base font-bold text-[#1C1B2E]">Change Password</h2>
                <p className="text-xs text-[#6C7089]">Update your account password regularly for optimal security.</p>
              </div>
            </div>

            {statusMessage && (
              <div className={`flex items-center gap-2 text-xs font-bold px-4 py-3 rounded-xl border ${
                statusMessage.type === 'success'
                  ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                  : 'bg-rose-50 text-rose-700 border-rose-200'
              }`}>
                {statusMessage.type === 'success' ? <CheckCircle2 size={15} /> : <AlertCircle size={15} />}
                <span>{statusMessage.text}</span>
              </div>
            )}

            <form onSubmit={handlePasswordSubmit} className="space-y-4">
              {/* Current Password */}
              <div>
                <label className="block text-xs font-bold text-[#1C1B2E] mb-1.5">Current Password</label>
                <div className="relative">
                  <input
                    type={showCurrentPassword ? 'text' : 'password'}
                    value={currentPassword}
                    onChange={e => setCurrentPassword(e.target.value)}
                    placeholder="••••••••••••"
                    className="w-full px-4 py-3 bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500 font-mono pr-12 transition-colors"
                  />
                  <button
                    type="button"
                    onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 p-1"
                  >
                    {showCurrentPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>
              </div>

              {/* New Password */}
              <div>
                <label className="block text-xs font-bold text-[#1C1B2E] mb-1.5">New Password</label>
                <div className="relative">
                  <input
                    type={showNewPassword ? 'text' : 'password'}
                    value={newPassword}
                    onChange={e => setNewPassword(e.target.value)}
                    placeholder="••••••••••••"
                    className="w-full px-4 py-3 bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500 font-mono pr-12 transition-colors"
                  />
                  <button
                    type="button"
                    onClick={() => setShowNewPassword(!showNewPassword)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 p-1"
                  >
                    {showNewPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>
                {newPassword && (
                  <div className="mt-2 space-y-1">
                    <div className="flex justify-between text-[11px] font-bold">
                      <span className="text-[#9598B0]">Password Strength</span>
                      <span className={strength.text}>{strength.label}</span>
                    </div>
                    <div className="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
                      <div className={`h-full transition-all duration-300 ${strength.color}`} style={{ width: `${strength.score}%` }}></div>
                    </div>
                  </div>
                )}
              </div>

              {/* Confirm Password */}
              <div>
                <label className="block text-xs font-bold text-[#1C1B2E] mb-1.5">Confirm New Password</label>
                <div className="relative">
                  <input
                    type={showConfirmPassword ? 'text' : 'password'}
                    value={confirmPassword}
                    onChange={e => setConfirmPassword(e.target.value)}
                    placeholder="••••••••••••"
                    className="w-full px-4 py-3 bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500 font-mono pr-12 transition-colors"
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 p-1"
                  >
                    {showConfirmPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>
                {confirmPassword && newPassword && (
                  <p className={`text-[11px] font-bold mt-1 ${newPassword === confirmPassword ? 'text-emerald-600' : 'text-rose-600'}`}>
                    {newPassword === confirmPassword ? '✓ Passwords match' : '✗ Passwords do not match'}
                  </p>
                )}
              </div>

              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-extrabold shadow-sm transition-all disabled:opacity-50 mt-2"
              >
                {isSubmitting ? 'Updating Password...' : 'Save Password Changes'}
              </button>
            </form>
          </div>

          {/* Right: Security Info */}
          <div className="space-y-4">
            {/* 2FA Card */}
            <div className="bg-white rounded-2xl border border-[#E5E7F3] shadow-sm p-5 space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <div className="p-2 bg-emerald-50 text-emerald-600 rounded-xl">
                    <Smartphone size={18} />
                  </div>
                  <div>
                    <h3 className="font-bold text-sm text-[#1C1B2E]">Two-Factor Auth</h3>
                    <p className="text-[11px] text-[#6C7089]">SMS or Authenticator Code</p>
                  </div>
                </div>
                <button
                  onClick={() => setTwoFactorEnabled(!twoFactorEnabled)}
                  className={`w-11 h-6 rounded-full transition-colors relative p-0.5 ${twoFactorEnabled ? 'bg-indigo-600' : 'bg-gray-200'}`}
                >
                  <div className={`w-5 h-5 bg-white rounded-full shadow transition-transform ${twoFactorEnabled ? 'translate-x-5' : 'translate-x-0'}`}></div>
                </button>
              </div>
              <p className="text-xs text-[#6C7089] leading-relaxed">
                Add an extra layer of protection to your account by requiring a verification code upon login.
              </p>
            </div>

            {/* Active Session */}
            <div className="bg-white rounded-2xl border border-[#E5E7F3] shadow-sm p-5 space-y-3">
              <h3 className="font-bold text-sm text-[#1C1B2E] flex items-center gap-2">
                <Laptop size={16} className="text-indigo-600" /> Active Session
              </h3>
              <div className="p-3 bg-[#F6F7FC] rounded-xl border border-[#E5E7F3] text-xs space-y-1">
                <div className="font-bold text-[#1C1B2E] flex items-center justify-between">
                  <span>Linux Chrome Browser</span>
                  <span className="text-[10px] font-extrabold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">Current</span>
                </div>
                <div className="text-[11px] text-[#6C7089]">IP: 127.0.0.1 (Local Session)</div>
              </div>
            </div>

            {/* Password Tips */}
            <div className="bg-indigo-50 rounded-2xl border border-indigo-100 p-4">
              <h4 className="text-xs font-bold text-indigo-800 mb-2 flex items-center gap-1.5">
                <Lock size={12} /> Password Tips
              </h4>
              <ul className="text-[11px] text-indigo-700 space-y-1">
                <li>• Use at least 8 characters</li>
                <li>• Mix uppercase &amp; lowercase letters</li>
                <li>• Include numbers and symbols</li>
                <li>• Avoid using personal information</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
