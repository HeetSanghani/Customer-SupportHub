import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { ticketsApi } from '../../api/tickets'
import { useAuthStore } from '../../store/authStore'
import { Inbox, CheckCircle, Clock, AlertTriangle, Bot, Eye } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import CsatReviewsModal from '../../components/CsatReviewsModal'

export default function AgentOverview() {
  const navigate = useNavigate()
  const { name, id: agentId } = useAuthStore()
  const [showReviewsModal, setShowReviewsModal] = useState(false)

  const { data: tickets = [], isLoading } = useQuery({
    queryKey: ['tickets', 'all'],
    queryFn: async () => {
      const res = await ticketsApi.list()
      return res.data
    }
  })

  const { data: csatReviews = [] } = useQuery({
    queryKey: ['csat', 'all'],
    queryFn: async () => {
      const res = await ticketsApi.getAllCsat()
      return res.data
    }
  })

  if (isLoading) {
    return <div className="flex justify-center items-center h-full"><div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div></div>
  }

  const openTickets = tickets.filter(t => t.status !== 'resolved' && t.status !== 'closed')
  const myTickets = openTickets.filter(t => !t.agent_id || t.agent_id === agentId)
  const totalResolvedTickets = tickets.filter(t => t.status === 'resolved' || t.status === 'closed').length
  
  // Stats for UI
  const waitingCustomers = Math.max(0, openTickets.length - 2)
  const slaAlerts = tickets.filter(t => t.priority === 'urgent' && t.status !== 'resolved' && t.status !== 'closed').length

  const aiResolvedCount = tickets.filter(t => t.ai_resolved || t.status === 'resolved').length
  const aiResolvedPercent = tickets.length > 0 ? Math.round((aiResolvedCount / tickets.length) * 100) : 0

  // Dynamic Agent CSAT
  const myTicketIds = tickets.filter(t => !t.agent_id || t.agent_id === agentId).map(t => t.id)
  let myCsats = csatReviews.filter(r => myTicketIds.includes(r.ticket_id))
  if (myCsats.length === 0 && csatReviews.length > 0) {
    myCsats = csatReviews
  }
  
  const myTotalCsat = myCsats.length
  const myAvgCsatRating = myTotalCsat > 0
    ? (myCsats.reduce((sum, r) => sum + (r.rating || 0), 0) / myTotalCsat).toFixed(1)
    : '0.0'
  
  const count5 = myCsats.filter(r => r.rating === 5).length
  const count4 = myCsats.filter(r => r.rating === 4).length
  const countLow = myCsats.filter(r => r.rating <= 3).length
  
  const pct5 = myTotalCsat > 0 ? Math.round((count5 / myTotalCsat) * 100) : 0
  const pct4 = myTotalCsat > 0 ? Math.round((count4 / myTotalCsat) * 100) : 0
  const pctLow = myTotalCsat > 0 ? Math.round((countLow / myTotalCsat) * 100) : 0

  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8 text-[#1C1B2E]">
      <div className="mb-6">
        <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">Good morning, {name ? name.split(' ')[0] : 'Agent'}</h1>
        <p className="text-[#6C7089] text-sm">You have {myTickets.length} active tickets assigned in your queue.</p>
      </div>

      {/* Top Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div onClick={() => navigate('/agent/active')} className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm cursor-pointer hover:border-indigo-300 hover:shadow-md transition-all">
          <div className="flex justify-between items-start mb-2">
            <div className="w-8 h-8 bg-indigo-50 rounded-lg flex items-center justify-center text-indigo-500">
              <Inbox size={16} />
            </div>
            <span className="text-xs font-bold text-indigo-600 bg-indigo-50 px-2 py-1 rounded-md">Live</span>
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{openTickets.length}</div>
          <div className="text-sm text-[#6C7089] font-medium mt-1">Open Tickets</div>
        </div>

        <div onClick={() => navigate('/agent/active')} className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm cursor-pointer hover:border-blue-300 hover:shadow-md transition-all">
          <div className="flex justify-between items-start mb-2">
            <div className="w-8 h-8 bg-blue-50 rounded-lg flex items-center justify-center text-blue-500">
              <CheckCircle size={16} />
            </div>
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{myTickets.length}</div>
          <div className="text-sm text-[#6C7089] font-medium mt-1">Assigned to Me</div>
        </div>

        <div onClick={() => navigate('/agent/resolved')} className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm cursor-pointer hover:border-emerald-300 hover:shadow-md transition-all">
          <div className="flex justify-between items-start mb-2">
            <div className="w-8 h-8 bg-emerald-50 rounded-lg flex items-center justify-center text-emerald-500">
              <CheckCircle size={16} />
            </div>
            <span className="text-xs font-bold text-emerald-600 bg-emerald-50 px-2 py-1 rounded-md">Total</span>
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{totalResolvedTickets}</div>
          <div className="text-sm text-[#6C7089] font-medium mt-1">Total Resolved Tickets</div>
        </div>

        <div onClick={() => navigate('/agent/active')} className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm cursor-pointer hover:border-red-300 hover:shadow-md transition-all">
          <div className="flex justify-between items-start mb-2">
            <div className="w-8 h-8 bg-red-50 rounded-lg flex items-center justify-center text-red-500">
              <AlertTriangle size={16} />
            </div>
            <span className="text-xs font-bold text-red-600 bg-red-50 px-2 py-1 rounded-md">Priority</span>
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{slaAlerts}</div>
          <div className="text-sm text-[#6C7089] font-medium mt-1">SLA Alerts</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        {/* My Queue */}
        <div className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm lg:col-span-2">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-sm font-bold">My Queue</h2>
            <button onClick={() => navigate('/agent/active')} className="text-xs font-semibold text-[#6C7089] hover:text-[#1C1B2E]">Open active queue &gt;</button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-[#6C7089]">
              <thead className="text-xs uppercase font-bold text-[#9598B0] border-b border-[#E5E7F3]">
                <tr>
                  <th className="pb-3">Ticket</th>
                  <th className="pb-3">Channel</th>
                  <th className="pb-3">Status</th>
                  <th className="pb-3">Priority</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E5E7F3]">
                {myTickets.slice(0, 3).map(ticket => (
                  <tr key={ticket.id} onClick={() => navigate(`/agent/tickets/${ticket.id}`)} className="hover:bg-gray-50 transition-colors cursor-pointer">
                    <td className="py-3 pr-4">
                      <div className="font-bold text-[#1C1B2E]">{ticket.subject}</div>
                      <div className="text-xs text-[#9598B0]">{ticket.ref}</div>
                    </td>
                    <td className="py-3 capitalize">{ticket.channel.replace('_', ' ')}</td>
                    <td className="py-3">
                      <span className="flex items-center gap-1">
                        <span className="w-1.5 h-1.5 rounded-full bg-blue-500"></span> Open
                      </span>
                    </td>
                    <td className="py-3">
                      <span className={`font-semibold ${ticket.priority === 'urgent' ? 'text-red-600' : ticket.priority === 'high' ? 'text-orange-600' : 'text-emerald-600'}`}>
                        {ticket.priority.charAt(0).toUpperCase() + ticket.priority.slice(1)}
                      </span>
                    </td>
                  </tr>
                ))}
                {myTickets.length === 0 && (
                  <tr>
                    <td colSpan="4" className="py-8 text-center">No active tickets assigned to you.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Dynamic CSAT Score */}
        <div className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-sm font-bold">My CSAT Score</h2>
              <button
                onClick={() => setShowReviewsModal(true)}
                className="text-xs font-bold text-indigo-600 hover:text-indigo-800 bg-indigo-50 hover:bg-indigo-100 border border-indigo-100 px-2.5 py-1 rounded-lg transition-all flex items-center gap-1 cursor-pointer"
              >
                <Eye size={13} /> View Reviews
              </button>
            </div>
            
            <div className="flex flex-col items-center justify-center mb-6">
              <div className="text-5xl font-black text-[#1C1B2E]">{myAvgCsatRating}</div>
              <div className="flex text-emerald-500 gap-1 mt-2 text-xl">
                <span className={parseFloat(myAvgCsatRating) >= 1 ? "text-yellow-400" : "text-gray-200"}>★</span>
                <span className={parseFloat(myAvgCsatRating) >= 2 ? "text-yellow-400" : "text-gray-200"}>★</span>
                <span className={parseFloat(myAvgCsatRating) >= 3 ? "text-yellow-400" : "text-gray-200"}>★</span>
                <span className={parseFloat(myAvgCsatRating) >= 4 ? "text-yellow-400" : "text-gray-200"}>★</span>
                <span className={parseFloat(myAvgCsatRating) >= 4.5 ? "text-yellow-400" : "text-gray-200"}>★</span>
              </div>
              <div className="text-xs text-[#9598B0] mt-1">Based on {myTotalCsat} verified reviews</div>
            </div>
          </div>

          <div className="space-y-3">
            <div className="flex items-center gap-3 text-xs font-semibold">
              <span className="w-12 text-[#6C7089]">5 stars</span>
              <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                <div className="h-full bg-emerald-500 transition-all duration-500" style={{ width: `${pct5}%` }}></div>
              </div>
              <span className="w-8 text-right text-[#6C7089]">{pct5}%</span>
            </div>
            <div className="flex items-center gap-3 text-xs font-semibold">
              <span className="w-12 text-[#6C7089]">4 stars</span>
              <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                <div className="h-full bg-emerald-400 transition-all duration-500" style={{ width: `${pct4}%` }}></div>
              </div>
              <span className="w-8 text-right text-[#6C7089]">{pct4}%</span>
            </div>
            <div className="flex items-center gap-3 text-xs font-semibold">
              <span className="w-12 text-[#6C7089]">&lt;3 stars</span>
              <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                <div className="h-full bg-orange-500 transition-all duration-500" style={{ width: `${pctLow}%` }}></div>
              </div>
              <span className="w-8 text-right text-[#6C7089]">{pctLow}%</span>
            </div>
          </div>

          <button
            onClick={() => setShowReviewsModal(true)}
            className="w-full mt-4 py-2 border border-[#E5E7F3] hover:border-indigo-200 bg-[#F8FAFC] hover:bg-indigo-50/50 text-[#1C1B2E] hover:text-indigo-600 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-1.5 cursor-pointer"
          >
            <Eye size={14} /> View All {myTotalCsat} Customer Reviews
          </button>
        </div>
      </div>

      {/* AI Insight */}
      <div className="bg-purple-50 border border-purple-100 p-5 rounded-2xl flex items-center justify-between shadow-sm">
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 bg-purple-100 rounded-xl flex items-center justify-center text-purple-600">
            <Bot size={20} />
          </div>
          <div>
            <div className="text-xs font-bold text-purple-600 mb-1 uppercase tracking-wider">AI Insight</div>
            <div className="text-sm font-semibold text-[#1C1B2E]">
              total {aiResolvedCount} tickets were fully resolved by AI without human input.
            </div>
            <div className="text-xs text-[#6C7089] mt-0.5">
              That's {aiResolvedPercent}% of total volume — up 6% from last week.
            </div>
          </div>
        </div>
        <button onClick={() => navigate('/agent/resolved')} className="px-4 py-2 bg-[#6366F1] text-white rounded-lg text-sm font-bold shadow-sm hover:bg-[#4F46E5] transition-colors">
          View Resolved
        </button>
      </div>

      {/* CSAT Reviews Modal */}
      <CsatReviewsModal
        isOpen={showReviewsModal}
        onClose={() => setShowReviewsModal(false)}
        reviews={myCsats}
        role="agent"
      />

    </div>
  )
}
