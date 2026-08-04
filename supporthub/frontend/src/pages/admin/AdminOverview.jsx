import { useQuery } from '@tanstack/react-query'
import { ticketsApi } from '../../api/tickets'
import { authApi } from '../../api/auth'
import { knowledgeApi } from '../../api/knowledge'
import { adminApi } from '../../api/admin'
import { Users, Link as LinkIcon, BookOpen, Bot, Mail, MessageSquare, Phone, Instagram, Facebook } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

const CHANNEL_ICONS = {
  email: { icon: Mail, color: 'text-blue-500' },
  website_chat: { icon: MessageSquare, color: 'text-indigo-500' },
  whatsapp: { icon: Phone, color: 'text-green-500' },
  instagram: { icon: Instagram, color: 'text-pink-500' },
  facebook: { icon: Facebook, color: 'text-blue-600' },
}

const CHANNEL_NAMES = {
  email: 'Email',
  website_chat: 'Website Chat',
  whatsapp: 'WhatsApp',
  instagram: 'Instagram',
  facebook: 'Facebook',
}

export default function AdminOverview() {
  const navigate = useNavigate()

  // Real tickets
  const { data: tickets = [], isLoading: isLoadingTickets } = useQuery({
    queryKey: ['tickets', 'all'],
    queryFn: async () => {
      const res = await ticketsApi.list()
      return res.data
    }
  })

  // Real users
  const { data: users = [], isLoading: isLoadingUsers } = useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const res = await authApi.listUsers()
      return res.data
    }
  })

  // Real KB Articles
  const { data: articles = [] } = useQuery({
    queryKey: ['kb-articles'],
    queryFn: async () => {
      const res = await knowledgeApi.list()
      return res.data
    }
  })

  // Real Channels
  const { data: channels = [] } = useQuery({
    queryKey: ['admin-channels'],
    queryFn: async () => {
      const res = await adminApi.listChannels()
      return res.data
    }
  })

  if (isLoadingTickets || isLoadingUsers) {
    return (
      <div className="flex justify-center items-center h-full">
        <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div>
      </div>
    )
  }

  const totalUsers = users.length
  const connectedChannels = channels.filter(c => c.status === 'connected').length
  const totalChannels = channels.length || 5
  const kbArticles = articles.length

  const totalTickets = tickets.length
  const aiResolved = tickets.filter(t => t.ai_resolved).length
  const aiResolutionRate = totalTickets > 0 ? Math.round((aiResolved / totalTickets) * 100) : 38

  const recentUsers = users.slice(0, 5)

  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8 text-[#1C1B2E]">
      <div className="mb-6">
        <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">Admin Overview</h1>
        <p className="text-[#6C7089] text-sm mt-1">System health, users and integrations at a glance.</p>
      </div>

      {/* Top Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div
          onClick={() => navigate('/admin/users')}
          className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm cursor-pointer hover:border-indigo-300 hover:shadow-md transition-all"
        >
          <div className="flex justify-between items-start mb-2">
            <div className="w-8 h-8 bg-indigo-50 rounded-lg flex items-center justify-center text-indigo-500">
              <Users size={16} />
            </div>
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{totalUsers}</div>
          <div className="text-sm text-[#6C7089] font-medium mt-1">Total Users</div>
        </div>

        <div
          onClick={() => navigate('/admin/channels')}
          className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm cursor-pointer hover:border-blue-300 hover:shadow-md transition-all"
        >
          <div className="flex justify-between items-start mb-2">
            <div className="w-8 h-8 bg-blue-50 rounded-lg flex items-center justify-center text-blue-500">
              <LinkIcon size={16} />
            </div>
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{connectedChannels} / {totalChannels}</div>
          <div className="text-sm text-[#6C7089] font-medium mt-1">Connected Channels</div>
        </div>

        <div
          onClick={() => navigate('/admin/help-center')}
          className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm cursor-pointer hover:border-purple-300 hover:shadow-md transition-all"
        >
          <div className="flex justify-between items-start mb-2">
            <div className="w-8 h-8 bg-purple-50 rounded-lg flex items-center justify-center text-purple-500">
              <BookOpen size={16} />
            </div>
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{kbArticles}</div>
          <div className="text-sm text-[#6C7089] font-medium mt-1">KB Articles</div>
        </div>

        <div
          onClick={() => navigate('/admin/ai-settings')}
          className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm cursor-pointer hover:border-emerald-300 hover:shadow-md transition-all"
        >
          <div className="flex justify-between items-start mb-2">
            <div className="w-8 h-8 bg-emerald-50 rounded-lg flex items-center justify-center text-emerald-500">
              <Bot size={16} />
            </div>
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{aiResolutionRate}%</div>
          <div className="text-sm text-[#6C7089] font-medium mt-1">AI Auto-Resolution</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Users */}
        <div className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm lg:col-span-2">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-sm font-bold text-[#1C1B2E]">Recent Users</h2>
            <button
              onClick={() => navigate('/admin/users')}
              className="text-xs font-semibold text-[#6C7089] hover:text-[#1C1B2E]"
            >
              Manage &gt;
            </button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-[#6C7089]">
              <thead className="text-xs uppercase font-bold text-[#9598B0] border-b border-[#E5E7F3]">
                <tr>
                  <th className="pb-3">Name</th>
                  <th className="pb-3">Role</th>
                  <th className="pb-3">Status</th>
                  <th className="pb-3">Last Active</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E5E7F3]">
                {recentUsers.map(user => (
                  <tr key={user.id} className="hover:bg-gray-50 transition-colors">
                    <td className="py-3">
                      <div className="font-bold text-[#1C1B2E]">{user.name || 'User'}</div>
                      <div className="text-xs text-[#9598B0]">{user.email || ''}</div>
                    </td>
                    <td className="py-3 capitalize text-xs font-medium">
                      {(user.role || 'agent').replace('_', ' ')}
                    </td>
                    <td className="py-3">
                      <span className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md text-xs font-semibold ${
                        user.status === 'active' ? 'bg-emerald-50 text-emerald-600' :
                        user.status === 'invited' ? 'bg-amber-50 text-amber-600' : 'bg-red-50 text-red-600'
                      }`}>
                        <span className="capitalize">{user.status || 'active'}</span>
                      </span>
                    </td>
                    <td className="py-3 text-xs text-[#9598B0]">Just now</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Channel Status */}
        <div className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-sm font-bold text-[#1C1B2E]">Channel Status</h2>
            <button
              onClick={() => navigate('/admin/channels')}
              className="text-xs font-semibold text-indigo-600 hover:underline"
            >
              Configure
            </button>
          </div>
          <div className="space-y-4">
            {channels.map(channel => {
              const type = channel?.channel_type || 'website_chat'
              const info = CHANNEL_ICONS[type] || { icon: MessageSquare, color: 'text-gray-500' }
              const IconComp = info.icon || MessageSquare
              const isConn = channel?.status === 'connected'
              const isAttn = channel?.status === 'needs_attention'

              return (
                <div key={channel.id || Math.random()} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <IconComp size={16} className={info.color} />
                    <div>
                      <div className="text-sm font-semibold">{CHANNEL_NAMES[type] || type}</div>
                      <div className="text-xs text-[#9598B0]">{channel?.display_name || ''}</div>
                    </div>
                  </div>
                  <span className={`text-xs font-bold px-2 py-1 rounded-md ${
                    isConn ? 'text-emerald-600 bg-emerald-50' :
                    isAttn ? 'text-orange-600 bg-orange-50' : 'text-gray-500 bg-gray-100'
                  }`}>
                    {isConn ? 'Connected' : isAttn ? 'Needs attention' : 'Disconnected'}
                  </span>
                </div>
              )
            })}
          </div>
        </div>
      </div>
    </div>
  )
}
