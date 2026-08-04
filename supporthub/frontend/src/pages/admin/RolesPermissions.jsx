import { useState } from 'react'
import { Shield, Check, Lock, Info, Save, CheckCircle2 } from 'lucide-react'

const INITIAL_ROLES = [
  {
    id: 'admin',
    name: 'Admin',
    description: 'Full access to all system features, settings, user management, and security configurations.',
    color: 'bg-purple-100 text-purple-700',
    permissions: {
      tickets_read: true,
      tickets_write: true,
      users_manage: true,
      channels_manage: true,
      kb_manage: true,
      ai_settings: true,
      system_config: true,
    }
  },
  {
    id: 'manager',
    name: 'Support Manager',
    description: 'Access to analytics, team reports, SLA monitoring, agent workloads, and ticket assignment.',
    color: 'bg-blue-100 text-blue-700',
    permissions: {
      tickets_read: true,
      tickets_write: true,
      users_manage: true,
      channels_manage: false,
      kb_manage: true,
      ai_settings: false,
      system_config: false,
    }
  },
  {
    id: 'agent',
    name: 'Support Agent',
    description: 'Access to assigned tickets, global inbox, direct chat replies, quick reply macros, and status toggle.',
    color: 'bg-indigo-100 text-indigo-700',
    permissions: {
      tickets_read: true,
      tickets_write: true,
      users_manage: false,
      channels_manage: false,
      kb_manage: false,
      ai_settings: false,
      system_config: false,
    }
  },
  {
    id: 'customer',
    name: 'Customer',
    description: 'Access to customer portal to submit tickets, view order status, and search Help Center articles.',
    color: 'bg-gray-100 text-gray-700',
    permissions: {
      tickets_read: false,
      tickets_write: false,
      users_manage: false,
      channels_manage: false,
      kb_manage: false,
      ai_settings: false,
      system_config: false,
    }
  }
]

const PERMISSION_LABELS = [
  { key: 'tickets_read', label: 'View All Tickets' },
  { key: 'tickets_write', label: 'Reply & Resolve Tickets' },
  { key: 'users_manage', label: 'Invite & Edit Users' },
  { key: 'channels_manage', label: 'Manage Channel Integrations' },
  { key: 'kb_manage', label: 'Manage Knowledge Base' },
  { key: 'ai_settings', label: 'Configure AI Assistant' },
  { key: 'system_config', label: 'Modify System Settings' },
]

export default function RolesPermissions() {
  const [roles, setRoles] = useState(INITIAL_ROLES)
  const [savedSuccess, setSavedSuccess] = useState(false)

  const togglePermission = (roleId, permKey) => {
    if (roleId === 'admin' && permKey === 'system_config') return // Keep admin locked to full
    setRoles(prev => prev.map(role => {
      if (role.id === roleId) {
        return {
          ...role,
          permissions: {
            ...role.permissions,
            [permKey]: !role.permissions[permKey]
          }
        }
      }
      return role
    }))
  }

  const handleSave = () => {
    setSavedSuccess(true)
    setTimeout(() => setSavedSuccess(false), 3000)
  }

  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8 text-[#1C1B2E]">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">Roles & Permissions</h1>
          <p className="text-[#6C7089] text-sm mt-1">Configure security levels and feature access across system roles.</p>
        </div>
        <button
          onClick={handleSave}
          className="flex items-center gap-2 bg-[#4F46E5] hover:bg-[#4338CA] text-white px-5 py-2.5 rounded-xl font-medium text-sm transition-colors shadow-sm"
        >
          <Save size={16} /> Save Permissions
        </button>
      </div>

      {savedSuccess && (
        <div className="mb-6 flex items-center gap-2 bg-emerald-50 text-emerald-700 p-4 rounded-2xl border border-emerald-200 text-sm font-semibold animate-fadeIn">
          <CheckCircle2 size={18} />
          <span>Role permissions updated successfully!</span>
        </div>
      )}

      {/* Role Cards Summary */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {roles.map(role => (
          <div key={role.id} className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className={`px-2.5 py-1 rounded-md text-xs font-bold ${role.color}`}>
                  {role.name}
                </span>
                <Shield size={16} className="text-[#9598B0]" />
              </div>
              <p className="text-xs text-[#6C7089] leading-relaxed">{role.description}</p>
            </div>
            <div className="mt-4 pt-3 border-t border-[#F3F4F6] text-xs font-bold text-indigo-600">
              {Object.values(role.permissions).filter(Boolean).length} / {PERMISSION_LABELS.length} Permissions Active
            </div>
          </div>
        ))}
      </div>

      {/* Permissions Matrix Table */}
      <div className="bg-white rounded-2xl border border-[#E5E7F3] shadow-sm overflow-hidden">
        <div className="px-6 py-4 border-b border-[#E5E7F3] bg-[#F9FAFB] flex items-center justify-between">
          <h2 className="font-bold text-sm text-[#1C1B2E]">Permission Matrix</h2>
          <div className="flex items-center gap-2 text-xs text-[#9598B0]">
            <Info size={14} /> Toggle checkboxes to grant or restrict access per role
          </div>
        </div>

        <table className="w-full text-left text-sm text-[#6C7089]">
          <thead className="border-b border-[#E5E7F3] text-xs uppercase font-bold text-[#9598B0]">
            <tr>
              <th className="px-6 py-4">Capability / Access</th>
              {roles.map(r => (
                <th key={r.id} className="px-6 py-4 text-center">{r.name}</th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-[#E5E7F3]">
            {PERMISSION_LABELS.map(perm => (
              <tr key={perm.key} className="hover:bg-gray-50/80 transition-colors">
                <td className="px-6 py-4 font-semibold text-[#1C1B2E]">
                  {perm.label}
                </td>
                {roles.map(role => {
                  const isChecked = role.permissions[perm.key]
                  return (
                    <td key={role.id} className="px-6 py-4 text-center">
                      <button
                        type="button"
                        onClick={() => togglePermission(role.id, perm.key)}
                        className={`w-6 h-6 rounded-md inline-flex items-center justify-center transition-all border ${
                          isChecked
                            ? 'bg-indigo-600 border-indigo-600 text-white'
                            : 'bg-gray-50 border-gray-300 text-transparent hover:border-gray-400'
                        }`}
                      >
                        <Check size={14} strokeWidth={3} />
                      </button>
                    </td>
                  )
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
