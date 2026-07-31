import { useQuery } from '@tanstack/react-query'
import { ticketsApi } from '../../api/tickets'
import { authApi } from '../../api/auth'
import { Users, Link as LinkIcon, BookOpen, Bot, CheckCircle2, AlertTriangle, Mail, MessageSquare, Phone, Instagram, Facebook } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export default function AdminOverview() {
  const navigate = useNavigate()

  const { data: tickets = [], isLoading: isLoadingTickets } = useQuery({
    queryKey: ['tickets', 'all'],
    queryFn: async () => {
      const res = await ticketsApi.list()
      return res.data
    }
  })

  const { data: users = [], isLoading: isLoadingUsers } = useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const res = await authApi.listUsers()
      return res.data
    }
  })

  if (isLoadingTickets || isLoadingUsers) {
    return <div className="flex justify-center items-center h-full"><div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div></div>
  }

  const totalUsers = users.length
  
  // Fake KB count for now
  const kbArticles = 48
  
  const totalTickets = tickets.length
  const aiResolved = tickets.filter(t => t.ai_resolved).length
  const aiResolutionRate = totalTickets > 0 ? Math.round((aiResolved / totalTickets) * 100) : 0
  
  const recentUsers = users.slice(0, 5)

  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8 text-[#1C1B2E]">
      <div className="mb-6">
        <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">Admin Overview</h1>
        <p className="text-[#6C7089] text-sm">System health, users and integrations at a glance.</p>
      </div>

      {/* Top Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div onClick={() => navigate('/admin')} className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm cursor-pointer hover:border-indigo-300 hover:shadow-md transition-all">
          <div className="flex justify-between items-start mb-2">
            <div className="w-8 h-8 bg-indigo-50 rounded-lg flex items-center justify-center text-indigo-500">
              <Users size={16} />
            </div>
            <span className="text-xs font-bold text-emerald-600 bg-emerald-50 px-2 py-1 rounded-md">+2</span>
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{totalUsers}</div>
          <div className="text-sm text-[#6C7089] font-medium mt-1">Total Users</div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm">
          <div className="flex justify-between items-start mb-2">
            <div className="w-8 h-8 bg-blue-50 rounded-lg flex items-center justify-center text-blue-500">
              <LinkIcon size={16} />
            </div>
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">4 / 5</div>
          <div className="text-sm text-[#6C7089] font-medium mt-1">Connected Channels</div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm">
          <div className="flex justify-between items-start mb-2">
            <div className="w-8 h-8 bg-purple-50 rounded-lg flex items-center justify-center text-purple-500">
              <BookOpen size={16} />
            </div>
            <span className="text-xs font-bold text-emerald-600 bg-emerald-50 px-2 py-1 rounded-md">+3</span>
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{kbArticles}</div>
          <div className="text-sm text-[#6C7089] font-medium mt-1">KB Articles</div>
        </div>

        <div onClick={() => navigate('/admin/inbox')} className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm cursor-pointer hover:border-emerald-300 hover:shadow-md transition-all">
          <div className="flex justify-between items-start mb-2">
            <div className="w-8 h-8 bg-emerald-50 rounded-lg flex items-center justify-center text-emerald-500">
              <Bot size={16} />
            </div>
            <span className="text-xs font-bold text-emerald-600 bg-emerald-50 px-2 py-1 rounded-md">+6%</span>
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{aiResolutionRate}%</div>
          <div className="text-sm text-[#6C7089] font-medium mt-1">AI Auto-Resolution</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Users */}
        <div className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm lg:col-span-2">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-sm font-bold">Recent Users</h2>
            <button onClick={() => navigate('/admin')} className="text-xs font-semibold text-[#6C7089] hover:text-[#1C1B2E]">Manage &gt;</button>
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
                      <div className="font-bold text-[#1C1B2E]">{user.name}</div>
                      <div className="text-xs text-[#9598B0]">{user.email}</div>
                    </td>
                    <td className="py-3 capitalize">{user.role.replace('_', ' ')}</td>
                    <td className="py-3">
                      <span className="text-emerald-600 font-semibold text-xs">Active</span>
                    </td>
                    <td className="py-3 text-xs">Just now</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Channel Status */}
        <div className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm">
          <h2 className="text-sm font-bold mb-6">Channel Status</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Mail size={16} className="text-blue-500" />
                <div>
                  <div className="text-sm font-semibold">Email</div>
                  <div className="text-xs text-[#9598B0]">support@brand.com</div>
                </div>
              </div>
              <span className="text-xs font-bold text-emerald-600 bg-emerald-50 px-2 py-1 rounded-md">Connected</span>
            </div>
            
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <MessageSquare size={16} className="text-indigo-500" />
                <div>
                  <div className="text-sm font-semibold">Website Chat</div>
                  <div className="text-xs text-[#9598B0]">brand.com widget</div>
                </div>
              </div>
              <span className="text-xs font-bold text-emerald-600 bg-emerald-50 px-2 py-1 rounded-md">Connected</span>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Phone size={16} className="text-green-500" />
                <div>
                  <div className="text-sm font-semibold">WhatsApp</div>
                  <div className="text-xs text-[#9598B0]">+1 415 555 0100</div>
                </div>
              </div>
              <span className="text-xs font-bold text-emerald-600 bg-emerald-50 px-2 py-1 rounded-md">Connected</span>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Instagram size={16} className="text-pink-500" />
                <div>
                  <div className="text-sm font-semibold">Instagram</div>
                  <div className="text-xs text-[#9598B0]">@brand.official</div>
                </div>
              </div>
              <span className="text-xs font-bold text-emerald-600 bg-emerald-50 px-2 py-1 rounded-md">Connected</span>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Facebook size={16} className="text-blue-600" />
                <div>
                  <div className="text-sm font-semibold">Facebook</div>
                  <div className="text-xs text-[#9598B0]">/brand.page</div>
                </div>
              </div>
              <span className="text-xs font-bold text-orange-600 bg-orange-50 px-2 py-1 rounded-md">Needs attention</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
