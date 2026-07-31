import { useQuery } from '@tanstack/react-query'
import { ticketsApi } from '../../api/tickets'
import { Download, FileText } from 'lucide-react'

export default function ManagerTicketReports() {
  const { data: tickets = [], isLoading } = useQuery({ queryKey: ['tickets', 'all'], queryFn: async () => (await ticketsApi.list()).data })

  if (isLoading) return <div className="p-8 flex justify-center"><div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div></div>

  const resolvedCount = tickets.filter(t => t.status === 'resolved' || t.status === 'closed').length

  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8 text-[#1C1B2E]">
      <div className="mb-6 flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">Ticket Reports</h1>
          <p className="text-[#6C7089] text-sm mt-1">Generate and export reports for stakeholders.</p>
        </div>
        <div className="flex gap-2">
          <button className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-sm font-bold transition-colors">
            <Download size={16} /> Export CSV
          </button>
          <button className="flex items-center gap-2 bg-white hover:bg-gray-50 border border-gray-200 text-[#1C1B2E] px-4 py-2 rounded-lg text-sm font-bold transition-colors">
            <FileText size={16} /> Export PDF
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm">
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{tickets.length}</div>
          <div className="text-sm text-[#6C7089] font-medium mt-1">Tickets Created</div>
        </div>
        <div className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm">
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{resolvedCount}</div>
          <div className="text-sm text-[#6C7089] font-medium mt-1">Tickets Resolved</div>
        </div>
        <div className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm">
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">2h 15m</div>
          <div className="text-sm text-[#6C7089] font-medium mt-1">Avg Resolution Time</div>
        </div>
      </div>

      <div className="bg-white rounded-2xl border border-[#E5E7F3] shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-[#6C7089]">
            <thead className="text-xs uppercase font-bold text-[#9598B0] border-b border-[#E5E7F3] bg-gray-50/50">
              <tr>
                <th className="px-6 py-4">Ticket</th>
                <th className="px-6 py-4">Category</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4">Priority</th>
                <th className="px-6 py-4">Channel</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E5E7F3]">
              {tickets.slice(0, 10).map(ticket => (
                <tr key={ticket.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <div className="font-bold text-[#1C1B2E]">{ticket.subject}</div>
                    <div className="text-[10px] text-[#9598B0]">{ticket.ref}</div>
                  </td>
                  <td className="px-6 py-4">{ticket.category}</td>
                  <td className="px-6 py-4 capitalize font-semibold">{ticket.status}</td>
                  <td className="px-6 py-4 capitalize">{ticket.priority}</td>
                  <td className="px-6 py-4 capitalize">{ticket.channel.replace('_', ' ')}</td>
                </tr>
              ))}
              {tickets.length === 0 && <tr><td colSpan="5" className="px-6 py-8 text-center">No records found.</td></tr>}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
