import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Eye, EyeOff } from 'lucide-react'
import { useAuthStore } from '../store/authStore'
import { authApi } from '../api/auth'

export default function RegisterPage() {
  const [form, setForm] = useState({ email: '', name: '', password: '' })
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
      await authApi.register(form)
      navigate('/login')
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed.')
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
          <div className="font-bold text-base text-[#1C1B2E]" style={{ fontFamily: 'Plus Jakarta Sans, sans-serif' }}>SupportHub</div>
        </div>
        <h1 className="text-xl font-bold text-[#1C1B2E] mb-1" style={{ fontFamily: 'Plus Jakarta Sans, sans-serif' }}>Create account</h1>
        <p className="text-sm text-[#6C7089] mb-6">Get started as a customer</p>

        {error && <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3 mb-4">{error}</div>}

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          {['name', 'email', 'password'].map(field => (
            <div key={field}>
              <label className="text-xs font-bold text-[#6C7089] uppercase tracking-wide block mb-1">{field}</label>
              {field === 'password' ? (
                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={form[field]}
                    onChange={e => setForm(f => ({ ...f, [field]: e.target.value }))}
                    required
                    className="w-full border border-[#E5E7F3] rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 pr-10"
                  />
                  <button
                    type="button"
                    className="absolute inset-y-0 right-0 pr-3 flex items-center text-[#9598B0] hover:text-[#6C7089]"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                  </button>
                </div>
              ) : (
                <input
                  type={field === 'email' ? 'email' : 'text'}
                  value={form[field]}
                  onChange={e => setForm(f => ({ ...f, [field]: e.target.value }))}
                  required
                  className="w-full border border-[#E5E7F3] rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              )}
            </div>
          ))}
          <button type="submit" disabled={loading}
            className="w-full py-2.5 rounded-lg font-bold text-sm text-white transition-opacity disabled:opacity-60"
            style={{ background: 'linear-gradient(135deg,#6366F1 0%,#A855F7 100%)' }}>
            {loading ? 'Creating…' : 'Create account'}
          </button>
        </form>
        <p className="text-center text-sm text-[#9598B0] mt-6">
          Already have an account? <Link to="/login" className="text-indigo-600 font-semibold hover:underline">Sign in</Link>
        </p>
      </div>
    </div>
  )
}
