import { useQuery } from '@tanstack/react-query'
import { ticketsApi } from '../../api/tickets'
import { BarChart3, Clock, CheckCircle2, Smile } from 'lucide-react'

export default function ManagerAnalytics() {
  const { data: tickets = [], isLoading } = useQuery({ queryKey: ['tickets', 'all'], queryFn: async () => (await ticketsApi.list()).data })
  const { data: csatReviews = [] } = useQuery({ queryKey: ['csat', 'all'], queryFn: async () => (await ticketsApi.getAllCsat()).data })

  if (isLoading) return <div className="p-8 flex justify-center"><div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div></div>

  const totalTickets = tickets.length
  const aiResolved = tickets.filter(t => t.ai_resolved).length
  const agentResolved = tickets.filter(t => t.status === 'resolved' && !t.ai_resolved).length
  
  const avgCsat = csatReviews.length > 0 ? (csatReviews.reduce((sum, r) => sum + r.rating, 0) / csatReviews.length).toFixed(1) : '0.0'

  const categories = tickets.reduce((acc, t) => {
    acc[t.category] = (acc[t.category] || 0) + 1
    return acc
  }, {})

  const maxCategory = Math.max(...Object.values(categories), 1)

  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8 text-[#1C1B2E]">
      <div className="mb-6">
        <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">Analytics</h1>
        <p className="text-[#6C7089] text-sm mt-1">Ticket volume, resolution trends and channel performance.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm">
          <div className="flex justify-between items-start mb-2">
            <div className="w-8 h-8 bg-indigo-50 rounded-lg flex items-center justify-center text-indigo-500">
              <BarChart3 size={16} />
            </div>
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{totalTickets}</div>
          <div className="text-sm text-[#6C7089] font-medium mt-1">Total Tickets</div>
        </div>
        <div className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm">
          <div className="flex justify-between items-start mb-2">
            <div className="w-8 h-8 bg-blue-50 rounded-lg flex items-center justify-center text-blue-500">
              <Clock size={16} />
            </div>
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">11m 40s</div>
          <div className="text-sm text-[#6C7089] font-medium mt-1">Avg. First Response (Est)</div>
        </div>
        <div className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm">
          <div className="flex justify-between items-start mb-2">
            <div className="w-8 h-8 bg-emerald-50 rounded-lg flex items-center justify-center text-emerald-500">
              <CheckCircle2 size={16} />
            </div>
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">2h 15m</div>
          <div className="text-sm text-[#6C7089] font-medium mt-1">Avg. Resolution Time (Est)</div>
        </div>
        <div className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm">
          <div className="flex justify-between items-start mb-2">
            <div className="w-8 h-8 bg-purple-50 rounded-lg flex items-center justify-center text-purple-500">
              <Smile size={16} />
            </div>
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{avgCsat} <span className="text-lg text-[#9598B0]">/ 5</span></div>
          <div className="text-sm text-[#6C7089] font-medium mt-1">CSAT Score</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm">
          <h2 className="text-sm font-bold mb-6">Tickets by Category</h2>
          <div className="space-y-4">
            {Object.entries(categories).map(([cat, count]) => (
              <div key={cat} className="flex items-center gap-3 text-sm font-semibold">
                <span className="w-24 text-[#6C7089] truncate">{cat}</span>
                <div className="flex-1 h-3 bg-gray-100 rounded-full overflow-hidden">
                  <div className="h-full bg-indigo-500" style={{ width: `${(count / maxCategory) * 100}%` }}></div>
                </div>
                <span className="w-8 text-right text-[#6C7089]">{count}</span>
              </div>
            ))}
            {Object.keys(categories).length === 0 && <p className="text-sm text-[#9598B0]">No category data available.</p>}
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm flex flex-col">
          <h2 className="text-sm font-bold mb-6">AI vs Human Resolution</h2>
          <div className="flex-1 flex items-center justify-center gap-8">
            <div className="relative w-32 h-32 flex-shrink-0">
              <svg viewBox="0 0 100 100" className="w-full h-full transform -rotate-90">
                <circle cx="50" cy="50" r="40" fill="transparent" stroke="#E5E7F3" strokeWidth="12" />
                <circle cx="50" cy="50" r="40" fill="transparent" stroke="#8B5CF6" strokeWidth="12" strokeDasharray={`${totalTickets > 0 ? (aiResolved / totalTickets) * 251.2 : 0} 251.2`} />
              </svg>
            </div>
            <div className="space-y-3 flex-1">
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-sm bg-purple-500"></div>
                  <span className="font-semibold text-[#1C1B2E]">AI Resolved</span>
                </div>
                <span className="font-bold text-[#6C7089]">{totalTickets > 0 ? Math.round((aiResolved / totalTickets) * 100) : 0}%</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-sm bg-blue-500"></div>
                  <span className="font-semibold text-[#1C1B2E]">Agent Resolved</span>
                </div>
                <span className="font-bold text-[#6C7089]">{totalTickets > 0 ? Math.round((agentResolved / totalTickets) * 100) : 0}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
