import { useQuery } from '@tanstack/react-query'
import { ticketsApi } from '../../api/tickets'
import client from '../../api/client'
import { ArrowUpRight, Star, Download, Users, ShieldCheck, CheckCircle2 } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export default function ManagerAgentPerformance() {
  const navigate = useNavigate()

  const { data: tickets = [], isLoading: loadingTickets } = useQuery({
    queryKey: ['tickets', 'all'],
    queryFn: async () => (await ticketsApi.list({ all_tickets: true, limit: 200 })).data
  })

  const { data: csatReviews = [] } = useQuery({
    queryKey: ['csat', 'all'],
    queryFn: async () => (await ticketsApi.getAllCsat()).data
  })

  const { data: users = [], isLoading: loadingUsers } = useQuery({
    queryKey: ['users', 'all'],
    queryFn: async () => (await client.get('/auth/users')).data
  })

  if (loadingTickets || loadingUsers) {
    return (
      <div className="p-8 flex justify-center items-center h-full">
        <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div>
      </div>
    )
  }

  // Only show real company agents — filter out placeholder/seed accounts
  const allAgents = users.filter(u => u.role === 'agent')
  const agents = allAgents.filter(a => a.email?.endsWith('@supporthub.com'))
  const hiddenCount = allAgents.length - agents.length

  // Human-intervention ticket pool (same logic as backend human_only filter)
  const humanTickets = tickets.filter(t =>
    t.status === 'escalated' ||
    t.agent_id != null ||
    t.priority === 'urgent' ||
    (t.category || '').toLowerCase().includes('escalat')
  )

  const agentStats = agents.map(agent => {
    // Prefer tickets directly assigned; fall back to human-intervention queue
    const directTickets = tickets.filter(t => t.agent_id === agent.id)
    const visibleTickets = (agents.length === 1)
      ? tickets.filter(t => t.agent_id === agent.id || humanTickets.some(ht => ht.id === t.id))
      : (directTickets.length > 0 ? directTickets : humanTickets)
    const isDirectQueue = directTickets.length > 0

    const active = visibleTickets.filter(t => t.status !== 'resolved' && t.status !== 'closed').length
    const resolved = visibleTickets.filter(t => t.status === 'resolved' || t.status === 'closed').length
    const slaCompliance = visibleTickets.length > 0 ? Math.round((resolved / visibleTickets.length) * 100) : 100

    const ticketIds = visibleTickets.map(t => t.id)
    const agentCsats = csatReviews.filter(r => ticketIds.includes(r.ticket_id))
    const csat = agentCsats.length > 0
      ? (agentCsats.reduce((acc, c) => acc + c.rating, 0) / agentCsats.length).toFixed(1)
      : csatReviews.length > 0
        ? (csatReviews.reduce((acc, c) => acc + c.rating, 0) / csatReviews.length).toFixed(1)
        : '—'

    return {
      ...agent,
      active,
      resolved,
      total: visibleTickets.length,
      slaCompliance,
      csat,
      isDirectQueue,
    }
  })

  const handleExportCSV = () => {
    if (!agentStats.length) return
    const headers = ['Agent Name', 'Email', 'Queue Size', 'Active Tickets', 'Resolved Tickets', 'SLA Compliance (%)', 'CSAT Score']
    const rows = agentStats.map(s => [
      `"${s.name}"`,
      `"${s.email}"`,
      s.total,
      s.active,
      s.resolved,
      `"${s.slaCompliance}%"`,
      s.csat
    ])
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n')
    const encodedUri = encodeURI(csvContent)
    const link = document.createElement('a')
    link.setAttribute('href', encodedUri)
    link.setAttribute('download', 'agent_performance_report.csv')
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8 text-[#1C1B2E]">
      {/* Header */}
      <div className="mb-6 flex justify-between items-start">
        <div>
          <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">Agent Performance</h1>
          <p className="text-[#6C7089] text-sm mt-0.5">
            Track and evaluate support team volume, resolution speed, and CSAT scores.
          </p>
        </div>
        <button
          onClick={handleExportCSV}
          className="flex items-center gap-2 px-4 py-2 bg-[#6366F1] hover:bg-[#4F46E5] text-white text-xs font-bold rounded-xl transition-all shadow-sm"
        >
          <Download size={14} /> Export Performance CSV
        </button>
      </div>

      {/* Empty state */}
      {agents.length === 0 && (
        <div className="bg-white rounded-2xl border border-[#E5E7F3] shadow-sm p-16 flex flex-col items-center justify-center text-center">
          <div className="w-16 h-16 bg-indigo-50 rounded-2xl flex items-center justify-center mb-4">
            <Users size={28} className="text-indigo-400" />
          </div>
          <p className="text-lg font-bold text-[#1C1B2E]">No active agents found</p>
          <p className="text-sm text-[#9598B0] mt-2 max-w-sm">
            Invite agents with a <code className="bg-slate-100 px-1 py-0.5 rounded text-xs">@supporthub.com</code> email to see their performance data here.
          </p>
        </div>
      )}

      {agents.length > 0 && (
        <>
          {/* Summary Table */}
          <div className="bg-white rounded-2xl border border-[#E5E7F3] shadow-sm overflow-hidden mb-6">
            <div className="p-5 border-b border-[#E5E7F3] flex justify-between items-center">
              <div>
                <h2 className="text-base font-bold text-[#1C1B2E]">Support Team Overview</h2>
                <p className="text-xs text-[#9598B0] mt-0.5">{agents.length} active agent{agents.length !== 1 ? 's' : ''}</p>
              </div>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm text-[#6C7089]">
                <thead className="text-xs uppercase font-bold text-[#9598B0] border-b border-[#E5E7F3] bg-gray-50/50">
                  <tr>
                    <th className="px-6 py-4">Agent Name</th>
                    <th className="px-6 py-4">Queue Size</th>
                    <th className="px-6 py-4">Active</th>
                    <th className="px-6 py-4">Resolved</th>
                    <th className="px-6 py-4">SLA Compliance</th>
                    <th className="px-6 py-4">Avg CSAT</th>
                    <th className="px-6 py-4 text-right">View Workload</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#E5E7F3]">
                  {agentStats.map(stat => (
                    <tr
                      key={stat.id}
                      onClick={() => navigate(`/manager/inbox/all?human_only=true`)}
                      className="hover:bg-indigo-50/30 transition-colors cursor-pointer group"
                    >
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-600 text-white font-bold text-xs flex items-center justify-center uppercase shadow-sm shrink-0">
                            {stat.name.split(' ').map(n => n[0]).join('').substring(0, 2)}
                          </div>
                          <div>
                            <div className="font-bold text-[#1C1B2E] group-hover:text-indigo-600 transition-colors">{stat.name}</div>
                            <div className="text-[10px] text-[#9598B0] font-mono">{stat.email}</div>
                            {!stat.isDirectQueue && (
                              <div className="text-[10px] text-indigo-400 font-semibold">👤 Human-intervention queue</div>
                            )}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 font-bold text-indigo-600">{stat.total}</td>
                      <td className="px-6 py-4 font-bold text-[#1C1B2E]">{stat.active}</td>
                      <td className="px-6 py-4 font-bold text-emerald-600">{stat.resolved}</td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <div className="w-24 h-2 bg-gray-100 rounded-full overflow-hidden">
                            <div
                              className={`h-full rounded-full ${stat.slaCompliance >= 80 ? 'bg-emerald-500' : stat.slaCompliance >= 50 ? 'bg-amber-400' : 'bg-rose-500'}`}
                              style={{ width: `${stat.slaCompliance}%` }}
                            ></div>
                          </div>
                          <span className={`font-bold text-xs ${stat.slaCompliance >= 80 ? 'text-emerald-600' : stat.slaCompliance >= 50 ? 'text-amber-600' : 'text-rose-600'}`}>
                            {stat.slaCompliance}%
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 font-bold text-amber-600">
                        <span className="flex items-center gap-1">
                          <Star size={13} className="fill-amber-500 text-amber-500" /> {stat.csat}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-right">
                        <span className="text-xs font-bold text-indigo-600 opacity-0 group-hover:opacity-100 transition-opacity inline-flex items-center gap-0.5">
                          Tickets <ArrowUpRight size={14} />
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Individual Agent Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {agentStats.map(stat => (
              <div
                key={stat.id}
                onClick={() => navigate(`/manager/inbox/all?human_only=true`)}
                className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm hover:border-indigo-400 hover:shadow-md transition-all cursor-pointer group"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-600 text-white font-bold text-xs flex items-center justify-center uppercase shadow-sm">
                      {stat.name.split(' ').map(n => n[0]).join('').substring(0, 2)}
                    </div>
                    <div>
                      <div className="font-bold text-[#1C1B2E] group-hover:text-indigo-600 transition-colors text-sm">{stat.name}</div>
                      <div className="text-[10px] text-[#9598B0]">{stat.email}</div>
                    </div>
                  </div>
                  <ArrowUpRight size={16} className="text-[#9598B0] group-hover:text-indigo-600 transition-colors" />
                </div>

                <div className="space-y-2.5 pt-3 border-t border-[#E5E7F3]">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-[#6C7089]">Queue Size:</span>
                    <span className="font-bold text-indigo-600">{stat.total}</span>
                  </div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-[#6C7089]">Active:</span>
                    <span className="font-bold text-[#1C1B2E]">{stat.active}</span>
                  </div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-[#6C7089]">Resolved:</span>
                    <span className="font-bold text-emerald-600">{stat.resolved}</span>
                  </div>
                  <div className="flex items-center gap-2 text-xs font-semibold">
                    <span className="w-12 text-[#6C7089]">SLA</span>
                    <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full ${stat.slaCompliance >= 80 ? 'bg-emerald-500' : stat.slaCompliance >= 50 ? 'bg-amber-400' : 'bg-rose-500'}`}
                        style={{ width: `${stat.slaCompliance}%` }}
                      ></div>
                    </div>
                    <span className="w-10 text-right font-bold text-[#1C1B2E]">{stat.slaCompliance}%</span>
                  </div>
                  <div className="flex items-center gap-2 text-xs font-semibold">
                    <span className="w-12 text-[#6C7089]">CSAT</span>
                    <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-amber-400 rounded-full"
                        style={{ width: `${stat.csat !== '—' ? (parseFloat(stat.csat) / 5) * 100 : 0}%` }}
                      ></div>
                    </div>
                    <span className="w-10 text-right font-bold text-amber-600">{stat.csat}</span>
                  </div>
                </div>

                {!stat.isDirectQueue && (
                  <div className="mt-3 pt-2 border-t border-[#E5E7F3] text-[10px] text-indigo-400 font-semibold">
                    👤 Showing human-intervention queue
                  </div>
                )}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
