import { useState } from 'react'
import { Sliders, Save, CheckCircle2, Building, ShieldCheck, Clock, Mail, Globe } from 'lucide-react'

export default function SystemSettings() {
  const [saveSuccess, setSaveSuccess] = useState(false)
  const [form, setForm] = useState({
    companyName: 'SupportHub Omnichannel',
    supportEmail: 'support@supporthub.com',
    timezone: 'UTC-05:00 (Eastern Time)',
    businessHours: '09:00 AM - 06:00 PM EST',
    enforce2FA: false,
    sessionTimeout: '30',
    auditLogging: true,
  })

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setForm(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleSave = (e) => {
    e.preventDefault()
    setSaveSuccess(true)
    setTimeout(() => setSaveSuccess(false), 3000)
  }

  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8 text-[#1C1B2E]">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">System Settings</h1>
          <p className="text-[#6C7089] text-sm mt-1">Configure workspace defaults, security preferences, and organizational details.</p>
        </div>
        <button
          onClick={handleSave}
          className="flex items-center gap-2 bg-[#4F46E5] hover:bg-[#4338CA] text-white px-5 py-2.5 rounded-xl font-medium text-sm transition-colors shadow-sm"
        >
          <Save size={16} /> Save Changes
        </button>
      </div>

      {saveSuccess && (
        <div className="mb-6 flex items-center gap-2 bg-emerald-50 text-emerald-700 p-4 rounded-2xl border border-emerald-200 text-sm font-semibold animate-fadeIn">
          <CheckCircle2 size={18} />
          <span>System settings saved successfully!</span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Settings Form */}
        <div className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm lg:col-span-2 space-y-6">
          <div>
            <h2 className="text-base font-bold text-[#1C1B2E] flex items-center gap-2 mb-4">
              <Building size={18} className="text-indigo-600" /> Platform & Organization
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Company / Workspace Name</label>
                <input
                  type="text"
                  name="companyName"
                  value={form.companyName}
                  onChange={handleChange}
                  className="w-full px-3.5 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Support Email Address</label>
                <input
                  type="email"
                  name="supportEmail"
                  value={form.supportEmail}
                  onChange={handleChange}
                  className="w-full px-3.5 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">System Timezone</label>
                <select
                  name="timezone"
                  value={form.timezone}
                  onChange={handleChange}
                  className="w-full px-3.5 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                >
                  <option value="UTC-05:00 (Eastern Time)">UTC-05:00 (Eastern Time)</option>
                  <option value="UTC+00:00 (London, GMT)">UTC+00:00 (London, GMT)</option>
                  <option value="UTC+05:30 (India Standard Time)">UTC+05:30 (India Standard Time)</option>
                  <option value="UTC-08:00 (Pacific Time)">UTC-08:00 (Pacific Time)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Operating Hours</label>
                <input
                  type="text"
                  name="businessHours"
                  value={form.businessHours}
                  onChange={handleChange}
                  className="w-full px-3.5 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                />
              </div>
            </div>
          </div>

          <hr className="border-[#E5E7F3]" />

          {/* Security & Authentication */}
          <div>
            <h2 className="text-base font-bold text-[#1C1B2E] flex items-center gap-2 mb-4">
              <ShieldCheck size={18} className="text-indigo-600" /> Security & Access
            </h2>

            <div className="space-y-4">
              <div className="flex items-center justify-between py-2 border-b border-[#F3F4F6]">
                <div>
                  <div className="font-bold text-sm text-[#1C1B2E]">Enforce Two-Factor Authentication (2FA)</div>
                  <div className="text-xs text-[#9598B0] mt-0.5">Require all agents and managers to use TOTP / 2FA logins</div>
                </div>
                <button
                  type="button"
                  onClick={() => setForm(p => ({ ...p, enforce2FA: !p.enforce2FA }))}
                  className={`w-12 h-6 flex items-center rounded-full p-1 transition-colors ${
                    form.enforce2FA ? 'bg-indigo-600' : 'bg-gray-300'
                  }`}
                >
                  <div
                    className={`bg-white w-4 h-4 rounded-full shadow-md transform transition-transform ${
                      form.enforce2FA ? 'translate-x-6' : 'translate-x-0'
                    }`}
                  />
                </button>
              </div>

              <div className="flex items-center justify-between py-2 border-b border-[#F3F4F6]">
                <div>
                  <div className="font-bold text-sm text-[#1C1B2E]">Audit Logging</div>
                  <div className="text-xs text-[#9598B0] mt-0.5">Log administrative changes, ticket updates, and login attempts</div>
                </div>
                <button
                  type="button"
                  onClick={() => setForm(p => ({ ...p, auditLogging: !p.auditLogging }))}
                  className={`w-12 h-6 flex items-center rounded-full p-1 transition-colors ${
                    form.auditLogging ? 'bg-indigo-600' : 'bg-gray-300'
                  }`}
                >
                  <div
                    className={`bg-white w-4 h-4 rounded-full shadow-md transform transition-transform ${
                      form.auditLogging ? 'translate-x-6' : 'translate-x-0'
                    }`}
                  />
                </button>
              </div>

              <div className="pt-2">
                <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Session Inactivity Timeout</label>
                <select
                  name="sessionTimeout"
                  value={form.sessionTimeout}
                  onChange={handleChange}
                  className="w-full max-w-xs px-3.5 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                >
                  <option value="15">15 Minutes</option>
                  <option value="30">30 Minutes</option>
                  <option value="60">1 Hour</option>
                  <option value="480">8 Hours</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* System Overview Sidecard */}
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm space-y-4">
            <h2 className="text-base font-bold text-[#1C1B2E]">System Status</h2>
            <div className="space-y-3 text-xs">
              <div className="flex justify-between py-2 border-b border-[#F3F4F6]">
                <span className="text-[#6C7089] font-medium">Backend Environment</span>
                <span className="font-bold text-emerald-600">Healthy (v1.0.0)</span>
              </div>
              <div className="flex justify-between py-2 border-b border-[#F3F4F6]">
                <span className="text-[#6C7089] font-medium">Database Connection</span>
                <span className="font-bold text-emerald-600">PostgreSQL (Connected)</span>
              </div>
              <div className="flex justify-between py-2 border-b border-[#F3F4F6]">
                <span className="text-[#6C7089] font-medium">AI Engine Model</span>
                <span className="font-bold text-indigo-600">OpenAI / Custom RAG</span>
              </div>
              <div className="flex justify-between py-2">
                <span className="text-[#6C7089] font-medium">WebSocket Server</span>
                <span className="font-bold text-emerald-600">Active</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
