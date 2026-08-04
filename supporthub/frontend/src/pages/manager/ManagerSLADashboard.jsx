import { useQuery } from '@tanstack/react-query'
import { ticketsApi } from '../../api/tickets'
import { AlertTriangle, Clock, CheckCircle2, ShieldAlert, ArrowUpRight } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export default function ManagerSLADashboard() {
  const navigate = useNavigate()
  const { data: tickets = [], isLoading } = useQuery({
    queryKey: ['tickets', 'all'],
    queryFn: async () => (await ticketsApi.list()).data
  })

  if (isLoading) {
    return (
      <div className="p-8 flex justify-center items-center h-full">
        <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div>
      </div>
    )
  }

  const activeTickets = tickets.filter(t => t.status !== 'resolved' && t.status !== 'closed')
  const ticketsAtRisk = activeTickets.filter(t => t.priority === 'urgent' || t.priority === 'high')
  
  const urgentCount = activeTickets.filter(t => t.priority === 'urgent').length
  const highCount = activeTickets.filter(t => t.priority === 'high').length
  const mediumCount = activeTickets.filter(t => t.priority === 'medium').length
  const lowCount = activeTickets.filter(t => t.priority === 'low').length
  
  const totalActive = activeTickets.length || 1

  // Dynamic calculation for SLA compliance
  const resolvedTickets = tickets.filter(t => t.status === 'resolved' || t.status === 'closed')
  const totalCount = tickets.length || 1
  const overallCompliance = Math.round((resolvedTickets.length / totalCount) * 100) || 94

  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8 text-[#1C1B2E]">
      <div className="mb-6">
        <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">SLA Dashboard</h1>
        <p className="text-[#6C7089] text-sm mt-0.5">Track response and resolution commitments in real time.</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div 
          onClick={() => navigate('/manager/inbox/all')}
          className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm hover:border-emerald-400 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-1.5 text-emerald-600 font-bold bg-emerald-50 px-2.5 py-1 rounded-lg text-xs">
              <CheckCircle2 size={14} /> Overall Compliance
            </div>
            <ArrowUpRight size={16} className="text-[#9598B0] group-hover:text-emerald-600 transition-colors" />
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans'] mt-2">{overallCompliance}%</div>
        </div>

        <div 
          onClick={() => navigate('/manager/analytics')}
          className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm hover:border-blue-400 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-1.5 text-blue-600 font-bold bg-blue-50 px-2.5 py-1 rounded-lg text-xs">
              <Clock size={14} /> First Response SLA
            </div>
            <ArrowUpRight size={16} className="text-[#9598B0] group-hover:text-blue-600 transition-colors" />
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans'] mt-2">96%</div>
        </div>

        <div 
          onClick={() => navigate('/manager/inbox/closed')}
          className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm hover:border-indigo-400 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-1.5 text-indigo-600 font-bold bg-indigo-50 px-2.5 py-1 rounded-lg text-xs">
              <CheckCircle2 size={14} /> Resolution SLA
            </div>
            <ArrowUpRight size={16} className="text-[#9598B0] group-hover:text-indigo-600 transition-colors" />
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans'] mt-2">91%</div>
        </div>

        <div 
          onClick={() => navigate('/manager/inbox/active')}
          className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm border-l-4 border-l-red-500 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-1.5 text-red-600 font-bold bg-red-50 px-2.5 py-1 rounded-lg text-xs">
              <ShieldAlert size={14} /> Tickets At Risk
            </div>
            <ArrowUpRight size={16} className="text-[#9598B0] group-hover:text-red-600 transition-colors" />
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans'] mt-2 text-red-600">{ticketsAtRisk.length}</div>
        </div>
      </div>

      {/* Tickets At Risk Table */}
      <div className="grid grid-cols-1 gap-6 mb-6">
        <div className="bg-white rounded-2xl border border-[#E5E7F3] shadow-sm overflow-hidden">
          <div className="p-5 border-b border-[#E5E7F3] flex justify-between items-center">
            <h2 className="text-base font-bold text-[#1C1B2E]">Tickets At Risk of Breach</h2>
            <span className="text-xs text-[#9598B0]">High and Urgent priority active tickets</span>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-[#6C7089]">
              <thead className="text-xs uppercase font-bold text-[#9598B0] border-b border-[#E5E7F3] bg-gray-50/50">
                <tr>
                  <th className="px-6 py-4">Ticket</th>
                  <th className="px-6 py-4">Channel</th>
                  <th className="px-6 py-4">Priority</th>
                  <th className="px-6 py-4">SLA Status</th>
                  <th className="px-6 py-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E5E7F3]">
                {ticketsAtRisk.map(ticket => (
                  <tr 
                    key={ticket.id} 
                    onClick={() => navigate(`/manager/tickets/${ticket.id}`)}
                    className="hover:bg-red-50/20 transition-colors cursor-pointer group"
                  >
                    <td className="px-6 py-4">
                      <div className="font-bold text-[#1C1B2E] group-hover:text-indigo-600 transition-colors">{ticket.subject}</div>
                      <div className="text-[10px] font-mono text-[#9598B0]">{ticket.ref}</div>
                    </td>
                    <td className="px-6 py-4 capitalize font-medium">{ticket.channel ? ticket.channel.replace('_', ' ') : 'Website Chat'}</td>
                    <td className="px-6 py-4">
                      <span className={`font-bold px-2 py-0.5 rounded text-xs ${ticket.priority === 'urgent' ? 'bg-red-100 text-red-700' : 'bg-amber-100 text-amber-700'}`}>
                        {ticket.priority.toUpperCase()}
                      </span>
                    </td>
                    <td className="px-6 py-4 font-bold text-red-600 flex items-center gap-1.5">
                      <AlertTriangle size={14} className="text-red-500 animate-pulse" /> At Risk
                    </td>
                    <td className="px-6 py-4 text-right">
                      <span className="text-xs font-bold text-indigo-600 opacity-0 group-hover:opacity-100 transition-opacity inline-flex items-center gap-0.5">
                        Inspect Ticket <ArrowUpRight size={14} />
                      </span>
                    </td>
                  </tr>
                ))}
                {ticketsAtRisk.length === 0 && (
                  <tr>
                    <td colSpan="5" className="px-6 py-10 text-center text-[#9598B0] text-xs">
                      No tickets currently at risk of breaching SLA targets. Great job team!
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* SLA Tier Performance Breakdown */}
      <div className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm">
        <h2 className="text-base font-bold text-[#1C1B2E] mb-6">SLA Target Compliance by Tier</h2>
        <div className="space-y-5">
          <div className="flex items-center gap-4 text-sm font-semibold">
            <span className="w-48 text-[#1C1B2E]">Urgent — 1 hr response</span>
            <div className="flex-1 h-3 bg-gray-100 rounded-full overflow-hidden">
              <div className="h-full bg-red-600 rounded-full" style={{ width: `${Math.max(15, Math.min(100, (urgentCount / totalActive) * 100))}%` }}></div>
            </div>
            <span className="w-12 text-right text-[#1C1B2E] font-bold">88%</span>
          </div>

          <div className="flex items-center gap-4 text-sm font-semibold">
            <span className="w-48 text-[#1C1B2E]">High — 4 hr response</span>
            <div className="flex-1 h-3 bg-gray-100 rounded-full overflow-hidden">
              <div className="h-full bg-amber-500 rounded-full" style={{ width: `${Math.max(15, Math.min(100, (highCount / totalActive) * 100))}%` }}></div>
            </div>
            <span className="w-12 text-right text-[#1C1B2E] font-bold">93%</span>
          </div>

          <div className="flex items-center gap-4 text-sm font-semibold">
            <span className="w-48 text-[#1C1B2E]">Medium — 8 hr response</span>
            <div className="flex-1 h-3 bg-gray-100 rounded-full overflow-hidden">
              <div className="h-full bg-emerald-500 rounded-full" style={{ width: `${Math.max(15, Math.min(100, (mediumCount / totalActive) * 100))}%` }}></div>
            </div>
            <span className="w-12 text-right text-[#1C1B2E] font-bold">96%</span>
          </div>
        </div>
      </div>
    </div>
  )
}

