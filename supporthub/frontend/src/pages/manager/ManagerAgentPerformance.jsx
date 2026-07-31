import { useQuery } from '@tanstack/react-query'
import { ticketsApi } from '../../api/tickets'
import client from '../../api/client'

export default function ManagerAgentPerformance() {
  const { data: tickets = [], isLoading: loadingTickets } = useQuery({ queryKey: ['tickets', 'all'], queryFn: async () => (await ticketsApi.list()).data })
  const { data: csatReviews = [] } = useQuery({ queryKey: ['csat', 'all'], queryFn: async () => (await ticketsApi.getAllCsat()).data })
  const { data: users = [], isLoading: loadingUsers } = useQuery({ queryKey: ['users', 'all'], queryFn: async () => (await client.get('/auth/users')).data })

  if (loadingTickets || loadingUsers) return <div className="p-8 flex justify-center"><div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div></div>

  const agents = users.filter(u => u.role === 'agent')

  const agentStats = agents.map(agent => {
    const agentTickets = tickets.filter(t => t.agent_id === agent.id)
    const active = agentTickets.filter(t => t.status !== 'resolved' && t.status !== 'closed').length
    const resolved = agentTickets.filter(t => t.status === 'resolved' || t.status === 'closed').length
    const slaCompliance = agentTickets.length > 0 ? Math.round((resolved / agentTickets.length) * 100) : 100 // Estimate
    
    const agentCsats = csatReviews.filter(r => agentTickets.find(t => t.id === r.ticket_id))
    const csat = agentCsats.length > 0 ? (agentCsats.reduce((acc, c) => acc + c.rating, 0) / agentCsats.length).toFixed(1) : 'N/A'

    return { ...agent, active, resolved, slaCompliance, csat, handleTime: 'N/A' }
  })

  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8 text-[#1C1B2E]">
      <div className="mb-6">
        <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">Agent Performance</h1>
        <p className="text-[#6C7089] text-sm mt-1">Compare workload, quality and speed across the team.</p>
      </div>

      <div className="bg-white rounded-2xl border border-[#E5E7F3] shadow-sm overflow-hidden mb-6">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-[#6C7089]">
            <thead className="text-xs uppercase font-bold text-[#9598B0] border-b border-[#E5E7F3] bg-gray-50/50">
              <tr>
                <th className="px-6 py-4">Agent</th>
                <th className="px-6 py-4">Active Tickets</th>
                <th className="px-6 py-4">Resolved</th>
                <th className="px-6 py-4">SLA Compliance</th>
                <th className="px-6 py-4">CSAT</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E5E7F3]">
              {agentStats.map(stat => (
                <tr key={stat.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-indigo-600 text-white font-bold text-[10px] flex items-center justify-center uppercase">
                        {stat.name.substring(0, 2)}
                      </div>
                      <div>
                        <div className="font-bold text-[#1C1B2E]">{stat.name}</div>
                        <div className="text-[10px] text-[#9598B0]">Support Agent</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 font-semibold text-[#1C1B2E]">{stat.active}</td>
                  <td className="px-6 py-4 font-semibold text-[#1C1B2E]">{stat.resolved}</td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="w-20 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                        <div className="h-full bg-emerald-500" style={{ width: `${stat.slaCompliance}%` }}></div>
                      </div>
                      <span className="font-semibold text-emerald-600">{stat.slaCompliance}%</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 font-semibold text-yellow-600">★ {stat.csat}</td>
                </tr>
              ))}
              {agentStats.length === 0 && (
                <tr><td colSpan="5" className="px-6 py-8 text-center">No agents found.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {agentStats.map(stat => (
          <div key={stat.id} className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-8 h-8 rounded-full bg-indigo-600 text-white font-bold text-[10px] flex items-center justify-center uppercase">
                {stat.name.substring(0, 2)}
              </div>
              <div className="font-bold text-[#1C1B2E]">{stat.name}</div>
            </div>
            <div className="space-y-3">
              <div className="flex items-center gap-3 text-xs font-semibold">
                <span className="w-10 text-[#6C7089]">SLA</span>
                <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div className="h-full bg-indigo-500" style={{ width: `${stat.slaCompliance}%` }}></div>
                </div>
                <span className="w-8 text-right text-[#1C1B2E]">{stat.slaCompliance}%</span>
              </div>
              <div className="flex items-center gap-3 text-xs font-semibold">
                <span className="w-10 text-[#6C7089]">CSAT</span>
                <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-500" style={{ width: `${stat.csat !== 'N/A' ? (parseFloat(stat.csat)/5)*100 : 0}%` }}></div>
                </div>
                <span className="w-8 text-right text-[#1C1B2E]">{stat.csat}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
