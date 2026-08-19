import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Eye, EyeOff } from 'lucide-react'
import { useAuthStore } from '../store/authStore'
import { authApi } from '../api/auth'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const login = useAuthStore((s) => s.login)
  const navigate = useNavigate()

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const { data } = await authApi.login({ email, password })
      login(data.access_token, data.user_id, data.role, data.name, data.refresh_token)
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Check your credentials.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#F6F7FC] px-4">
      <div className="w-full max-w-sm bg-white rounded-2xl shadow-lg p-8 border border-[#E5E7F3]">
        <div className="flex items-center gap-2 mb-8">
          <div className="w-9 h-9 rounded-xl flex items-center justify-center text-white font-bold text-sm"
               style={{ background: 'linear-gradient(135deg,#6366F1 0%,#A855F7 100%)' }}>S</div>
          <div>
            <div className="font-bold text-base text-[#1C1B2E]" style={{ fontFamily: 'Plus Jakarta Sans, sans-serif' }}>SupportHub</div>
            <div className="text-xs text-[#9598B0]">AI Omnichannel Platform</div>
          </div>
        </div>

        <h1 className="text-xl font-bold text-[#1C1B2E] mb-1" style={{ fontFamily: 'Plus Jakarta Sans, sans-serif' }}>
          Welcome back
        </h1>
        <p className="text-sm text-[#6C7089] mb-6">Sign in to your workspace</p>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3 mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div>
            <label className="text-xs font-bold text-[#6C7089] uppercase tracking-wide block mb-1">Email</label>
            <input
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              required
              className="w-full border border-[#E5E7F3] rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="you@company.com"
            />
          </div>
          <div>
            <label className="text-xs font-bold text-[#6C7089] uppercase tracking-wide block mb-1">Password</label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={e => setPassword(e.target.value)}
                required
                className="w-full border border-[#E5E7F3] rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 pr-10"
                placeholder="••••••••"
              />
              <button
                type="button"
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-[#9598B0] hover:text-[#6C7089]"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 rounded-lg font-bold text-sm text-white transition-opacity disabled:opacity-60"
            style={{ background: 'linear-gradient(135deg,#6366F1 0%,#A855F7 100%)' }}
          >
            {loading ? 'Signing in…' : 'Sign in'}
          </button>
        </form>

        <p className="text-center text-sm text-[#9598B0] mt-6">
          Don't have an account?{' '}
          <Link to="/register" className="text-indigo-600 font-semibold hover:underline">Register</Link>
        </p>

        {/* Quick Login for Development/Testing */}
        <div className="mt-8 pt-6 border-t border-[#E5E7F3]">
          <p className="text-xs font-bold text-[#6C7089] uppercase tracking-wide text-center mb-3">Quick Login (Dev Only)</p>
          <div className="grid grid-cols-2 gap-2">
            {[
              { role: 'Admin', email: 'admin@supporthub.com' },
              { role: 'Manager', email: 'manager@supporthub.com' },
              { role: 'Agent', email: 'agent@supporthub.com' },
              { role: 'Customer', email: 'customer@supporthub.com' }
            ].map(acc => (
              <button
                key={acc.role}
                type="button"
                onClick={() => {
                  setEmail(acc.email)
                  setPassword('Password123!')
                }}
                className="text-xs py-1.5 border border-[#E5E7F3] rounded-md text-[#1C1B2E] font-semibold hover:bg-gray-50 transition-colors"
              >
                {acc.role}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
