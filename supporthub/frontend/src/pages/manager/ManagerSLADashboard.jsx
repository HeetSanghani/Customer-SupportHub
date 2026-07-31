import { useQuery } from '@tanstack/react-query'
import { ticketsApi } from '../../api/tickets'
import { AlertTriangle, Clock, CheckCircle2, ShieldAlert } from 'lucide-react'

export default function ManagerSLADashboard() {
  const { data: tickets = [], isLoading } = useQuery({ queryKey: ['tickets', 'all'], queryFn: async () => (await ticketsApi.list()).data })

  if (isLoading) return <div className="p-8 flex justify-center"><div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div></div>

  const activeTickets = tickets.filter(t => t.status !== 'resolved' && t.status !== 'closed')
  const ticketsAtRisk = activeTickets.filter(t => t.priority === 'urgent' || t.priority === 'high')
  
  const urgentCount = activeTickets.filter(t => t.priority === 'urgent').length
  const highCount = activeTickets.filter(t => t.priority === 'high').length
  const mediumCount = activeTickets.filter(t => t.priority === 'medium').length
  
  const totalActive = activeTickets.length || 1

  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8 text-[#1C1B2E]">
      <div className="mb-6">
        <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">SLA Dashboard</h1>
        <p className="text-[#6C7089] text-sm mt-1">Track response and resolution commitments in real time.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm">
          <div className="flex items-center gap-2 mb-2 text-emerald-600 font-bold bg-emerald-50 w-fit px-2 py-1 rounded-lg text-xs">
            <CheckCircle2 size={14} /> Overall Compliance
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans'] mt-2">94%</div>
        </div>
        <div className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm">
          <div className="flex items-center gap-2 mb-2 text-blue-600 font-bold bg-blue-50 w-fit px-2 py-1 rounded-lg text-xs">
            <Clock size={14} /> First Response SLA
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans'] mt-2">96%</div>
        </div>
        <div className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm">
          <div className="flex items-center gap-2 mb-2 text-indigo-600 font-bold bg-indigo-50 w-fit px-2 py-1 rounded-lg text-xs">
            <CheckCircle2 size={14} /> Resolution SLA
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans'] mt-2">91%</div>
        </div>
        <div className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm border-l-4 border-l-red-500">
          <div className="flex items-center gap-2 mb-2 text-red-600 font-bold bg-red-50 w-fit px-2 py-1 rounded-lg text-xs">
            <ShieldAlert size={14} /> Tickets At Risk
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans'] mt-2 text-red-600">{ticketsAtRisk.length}</div>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 mb-6">
        <div className="bg-white rounded-2xl border border-[#E5E7F3] shadow-sm overflow-hidden">
          <div className="p-5 border-b border-[#E5E7F3]">
            <h2 className="text-sm font-bold">Tickets At Risk of Breach</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-[#6C7089]">
              <thead className="text-xs uppercase font-bold text-[#9598B0] border-b border-[#E5E7F3] bg-gray-50/50">
                <tr>
                  <th className="px-6 py-4">Ticket</th>
                  <th className="px-6 py-4">Channel</th>
                  <th className="px-6 py-4">Priority</th>
                  <th className="px-6 py-4">SLA Time</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E5E7F3]">
                {ticketsAtRisk.map(ticket => (
                  <tr key={ticket.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div className="font-bold text-[#1C1B2E]">{ticket.subject}</div>
                      <div className="text-[10px] text-[#9598B0]">{ticket.ref}</div>
                    </td>
                    <td className="px-6 py-4 capitalize">{ticket.channel.replace('_', ' ')}</td>
                    <td className="px-6 py-4">
                      <span className={`font-semibold ${ticket.priority === 'urgent' ? 'text-red-600' : 'text-orange-600'}`}>
                        {ticket.priority.toUpperCase()}
                      </span>
                    </td>
                    <td className="px-6 py-4 font-bold text-red-600">At Risk</td>
                  </tr>
                ))}
                {ticketsAtRisk.length === 0 && <tr><td colSpan="4" className="px-6 py-8 text-center">No tickets at risk. Great job!</td></tr>}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm">
        <h2 className="text-sm font-bold mb-6">SLA by Priority Tier</h2>
        <div className="space-y-5">
          <div className="flex items-center gap-4 text-sm font-semibold">
            <span className="w-40 text-[#1C1B2E]">Urgent — 1 hr response</span>
            <div className="flex-1 h-3 bg-gray-100 rounded-full overflow-hidden">
              <div className="h-full bg-red-600" style={{ width: `${Math.max(10, (urgentCount/totalActive)*100)}%` }}></div>
            </div>
            <span className="w-10 text-right text-[#1C1B2E]">88%</span>
          </div>
          <div className="flex items-center gap-4 text-sm font-semibold">
            <span className="w-40 text-[#1C1B2E]">High — 4 hr response</span>
            <div className="flex-1 h-3 bg-gray-100 rounded-full overflow-hidden">
              <div className="h-full bg-orange-500" style={{ width: `${Math.max(10, (highCount/totalActive)*100)}%` }}></div>
            </div>
            <span className="w-10 text-right text-[#1C1B2E]">93%</span>
          </div>
          <div className="flex items-center gap-4 text-sm font-semibold">
            <span className="w-40 text-[#1C1B2E]">Medium — 8 hr response</span>
            <div className="flex-1 h-3 bg-gray-100 rounded-full overflow-hidden">
              <div className="h-full bg-emerald-500" style={{ width: `${Math.max(10, (mediumCount/totalActive)*100)}%` }}></div>
            </div>
            <span className="w-10 text-right text-[#1C1B2E]">96%</span>
          </div>
        </div>
      </div>
    </div>
  )
}
