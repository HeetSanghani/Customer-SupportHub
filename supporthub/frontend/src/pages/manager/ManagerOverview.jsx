import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { ticketsApi } from '../../api/tickets'
import { authApi } from '../../api/auth'
import { CheckCircle2, Ticket as TicketIcon, Clock, Bot, AlertTriangle, Star, MessageSquare, X, ChevronRight, Filter } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { formatDateTime } from '../../utils/dateUtils'

export default function ManagerOverview() {
  const navigate = useNavigate()
  const [showReviewsModal, setShowReviewsModal] = useState(false)
  const [selectedStarFilter, setSelectedStarFilter] = useState('all')

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

  const { data: csatReviews = [], isLoading: isLoadingCsat } = useQuery({
    queryKey: ['csat', 'all'],
    queryFn: async () => {
      try {
        const res = await ticketsApi.getAllCsat()
        return res.data
      } catch (err) {
        console.error('Failed to load CSAT reviews', err)
        return []
      }
    }
  })

  if (isLoadingTickets || isLoadingUsers || isLoadingCsat) {
    return (
      <div className="flex justify-center items-center h-full">
        <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div>
      </div>
    )
  }

  const agents = users.filter(u => u.role === 'agent')

  const totalTickets = tickets.length
  const closedTickets = tickets.filter(t => t.status === 'resolved' || t.status === 'closed').length
  const closedPercentage = totalTickets > 0 ? Math.round((closedTickets / totalTickets) * 100) : 0

  const aiResolved = tickets.filter(t => t.ai_resolved).length
  const aiResolutionRate = totalTickets > 0 ? Math.round((aiResolved / totalTickets) * 100) : 0
  
  const slaCompliance = totalTickets > 0 ? Math.round((closedTickets / totalTickets) * 100) : 100
  const recentActivity = tickets.slice(0, 4)

  // 1. Purely Dynamic Channels Breakdown from actual DB tickets
  const channelCounts = {
    email: tickets.filter(t => t.channel === 'email').length,
    chat: tickets.filter(t => t.channel === 'website_chat' || t.channel === 'chat').length,
    whatsapp: tickets.filter(t => t.channel === 'whatsapp').length,
    instagram: tickets.filter(t => t.channel === 'instagram').length,
    facebook: tickets.filter(t => t.channel === 'facebook').length,
  }

  const channelDisplayData = [
    { id: 'email', label: 'Email', count: channelCounts.email, color: '#6366F1' },
    { id: 'website_chat', label: 'Website Chat', count: channelCounts.chat, color: '#3B82F6' },
    { id: 'whatsapp', label: 'WhatsApp', count: channelCounts.whatsapp, color: '#10B981' },
    { id: 'instagram', label: 'Instagram', count: channelCounts.instagram, color: '#8B5CF6' },
    { id: 'facebook', label: 'Facebook', count: channelCounts.facebook, color: '#2563EB' },
  ]
  const maxChannel = Math.max(...channelDisplayData.map(c => c.count), 1)

  // 2. Purely Dynamic CSAT Analytics from actual DB reviews
  const totalCsatCount = csatReviews.length
  const avgCsatRating = totalCsatCount > 0
    ? (csatReviews.reduce((sum, r) => sum + (r.rating || 0), 0) / totalCsatCount).toFixed(1)
    : '0.0'

  const count5Star = csatReviews.filter(r => r.rating === 5).length
  const count4Star = csatReviews.filter(r => r.rating === 4).length
  const count3Star = csatReviews.filter(r => r.rating === 3).length
  const countLowStar = csatReviews.filter(r => r.rating <= 2).length

  const excellentPct = totalCsatCount > 0 ? Math.round((count5Star / totalCsatCount) * 100) : 0
  const goodPct = totalCsatCount > 0 ? Math.round((count4Star / totalCsatCount) * 100) : 0
  const fairPct = totalCsatCount > 0 ? Math.round((count3Star / totalCsatCount) * 100) : 0
  const poorPct = totalCsatCount > 0 ? Math.round((countLowStar / totalCsatCount) * 100) : 0

  const filteredReviews = csatReviews.filter(r => {
    if (selectedStarFilter === '5') return r.rating === 5
    if (selectedStarFilter === '4') return r.rating === 4
    if (selectedStarFilter === '3_lower') return r.rating <= 3
    return true
  })

  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8 text-[#1C1B2E]">
      <div className="mb-6">
        <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">Support Overview</h1>
        <p className="text-[#6C7089] text-sm">Today's snapshot across all channels, agents, and customer reviews.</p>
      </div>

      {/* Top Stats Cards with updated redirection */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        {/* Total Tickets -> All Tickets */}
        <div
          onClick={() => navigate('/manager/inbox/all')}
          className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm cursor-pointer hover:border-indigo-400 hover:shadow-md transition-all group"
        >
          <div className="flex justify-between items-start mb-2">
            <div className="w-9 h-9 bg-indigo-50 rounded-xl flex items-center justify-center text-indigo-600 group-hover:bg-indigo-600 group-hover:text-white transition-colors">
              <TicketIcon size={18} />
            </div>
            <span className="text-xs font-bold text-indigo-600 bg-indigo-50 px-2.5 py-1 rounded-full">Live</span>
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{totalTickets.toLocaleString()}</div>
          <div className="flex items-center justify-between text-sm text-[#6C7089] font-medium mt-1">
            <span>Total Tickets</span>
            <span className="text-xs text-indigo-600 font-semibold group-hover:underline flex items-center gap-0.5">View All &rarr;</span>
          </div>
        </div>

        {/* Open vs Closed -> Closed Tickets */}
        <div
          onClick={() => navigate('/manager/inbox/closed')}
          className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm cursor-pointer hover:border-emerald-400 hover:shadow-md transition-all group"
        >
          <div className="flex justify-between items-start mb-2">
            <div className="w-9 h-9 bg-emerald-50 rounded-xl flex items-center justify-center text-emerald-600 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
              <CheckCircle2 size={18} />
            </div>
            <span className="text-xs font-bold text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-full">{closedTickets} Closed</span>
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{closedPercentage}% closed</div>
          <div className="flex items-center justify-between text-sm text-[#6C7089] font-medium mt-1">
            <span>Open vs Closed</span>
            <span className="text-xs text-emerald-600 font-semibold group-hover:underline flex items-center gap-0.5">View Closed &rarr;</span>
          </div>
        </div>

        {/* SLA Compliance -> Active Tickets */}
        <div
          onClick={() => navigate('/manager/inbox/active')}
          className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm cursor-pointer hover:border-orange-400 hover:shadow-md transition-all group"
        >
          <div className="flex justify-between items-start mb-2">
            <div className="w-9 h-9 bg-orange-50 rounded-xl flex items-center justify-center text-orange-600 group-hover:bg-orange-600 group-hover:text-white transition-colors">
              <Clock size={18} />
            </div>
            <span className="text-xs font-bold text-orange-600 bg-orange-50 px-2.5 py-1 rounded-full">SLA Target</span>
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{slaCompliance}%</div>
          <div className="flex items-center justify-between text-sm text-[#6C7089] font-medium mt-1">
            <span>SLA Compliance</span>
            <span className="text-xs text-orange-600 font-semibold group-hover:underline flex items-center gap-0.5">View Active &rarr;</span>
          </div>
        </div>

        {/* AI Resolution Rate -> All Tickets */}
        <div
          onClick={() => navigate('/manager/inbox/all')}
          className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm cursor-pointer hover:border-purple-400 hover:shadow-md transition-all group"
        >
          <div className="flex justify-between items-start mb-2">
            <div className="w-9 h-9 bg-purple-50 rounded-xl flex items-center justify-center text-purple-600 group-hover:bg-purple-600 group-hover:text-white transition-colors">
              <Bot size={18} />
            </div>
            <span className="text-xs font-bold text-purple-600 bg-purple-50 px-2.5 py-1 rounded-full">{aiResolved} AI Resolved</span>
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{aiResolutionRate}%</div>
          <div className="flex items-center justify-between text-sm text-[#6C7089] font-medium mt-1">
            <span>AI Resolution Rate</span>
            <span className="text-xs text-purple-600 font-semibold group-hover:underline flex items-center gap-0.5">Details &rarr;</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        {/* Dynamic Tickets by Channel */}
        <div className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm lg:col-span-2 flex flex-col justify-between">
          <div className="flex justify-between items-center mb-6">
            <div>
              <h2 className="text-base font-bold text-[#1C1B2E]">Tickets by Channel (All time)</h2>
              <p className="text-xs text-[#9598B0]">Live volume distribution across support touchpoints</p>
            </div>
            <button
              onClick={() => navigate('/manager/inbox/all')}
              className="text-xs font-bold text-indigo-600 hover:bg-indigo-50 px-3 py-1.5 rounded-lg transition-colors flex items-center gap-1"
            >
              Open Team Inbox &rarr;
            </button>
          </div>

          <div className="flex items-end gap-3 h-52 pt-4 px-2">
            {channelDisplayData.map((ch) => {
              const heightPct = maxChannel > 0 && ch.count > 0 ? Math.max((ch.count / maxChannel) * 100, 8) : 4
              return (
                <div
                  key={ch.id}
                  onClick={() => navigate('/manager/inbox/all')}
                  className="flex-1 flex flex-col items-center gap-2 group cursor-pointer h-full justify-end"
                >
                  <div className="w-full bg-slate-100 rounded-t-lg flex-1 flex items-end p-1 relative overflow-hidden group-hover:bg-slate-200 transition-colors">
                    <div
                      className="w-full rounded-t-md transition-all duration-500 relative flex items-center justify-center"
                      style={{
                        height: `${heightPct}%`,
                        backgroundColor: ch.color,
                      }}
                    >
                      {ch.count > 0 && (
                        <span className="text-[10px] font-bold text-white opacity-0 group-hover:opacity-100 transition-opacity">
                          {ch.count}
                        </span>
                      )}
                    </div>

                    <div className="absolute -top-9 left-1/2 -translate-x-1/2 bg-slate-900 text-white text-[11px] font-semibold px-2.5 py-1 rounded-md opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10 shadow-lg pointer-events-none">
                      {ch.label}: <span className="font-bold text-emerald-400">{ch.count} Tickets</span>
                    </div>
                  </div>
                  <div className="text-xs text-[#6C7089] font-bold text-center leading-tight group-hover:text-indigo-600 transition-colors">
                    {ch.label} ({ch.count})
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        {/* Dynamic Customer Satisfaction */}
        <div className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm flex flex-col justify-between">
          <div className="flex justify-between items-center mb-2">
            <h2 className="text-base font-bold text-[#1C1B2E]">Customer Satisfaction</h2>
            <span className="text-xs font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">Live CSAT</span>
          </div>

          <div className="flex flex-col items-center justify-center my-4">
            <div className="text-5xl font-black text-[#1C1B2E] tracking-tight">{avgCsatRating}</div>
            <div className="flex text-yellow-400 gap-1 my-2 text-xl">
              <Star fill={parseFloat(avgCsatRating) >= 1 ? "currentColor" : "none"} size={20} />
              <Star fill={parseFloat(avgCsatRating) >= 2 ? "currentColor" : "none"} size={20} />
              <Star fill={parseFloat(avgCsatRating) >= 3 ? "currentColor" : "none"} size={20} />
              <Star fill={parseFloat(avgCsatRating) >= 4 ? "currentColor" : "none"} size={20} />
              <Star fill={parseFloat(avgCsatRating) >= 4.5 ? "currentColor" : "none"} size={20} />
            </div>
            <div className="text-xs text-[#9598B0] font-medium">
              Based on <span className="font-bold text-slate-800">{totalCsatCount} verified customer reviews</span>
            </div>
          </div>

          <div className="space-y-2.5 mb-4">
            <div className="flex items-center gap-3 text-xs font-semibold">
              <span className="w-16 text-[#6C7089]">Excellent</span>
              <div className="flex-1 h-2.5 bg-gray-100 rounded-full overflow-hidden">
                <div className="h-full bg-emerald-500 rounded-full transition-all duration-500" style={{ width: `${excellentPct}%` }}></div>
              </div>
              <span className="w-9 text-right text-[#1C1B2E] font-bold">{excellentPct}%</span>
            </div>
            <div className="flex items-center gap-3 text-xs font-semibold">
              <span className="w-16 text-[#6C7089]">Good</span>
              <div className="flex-1 h-2.5 bg-gray-100 rounded-full overflow-hidden">
                <div className="h-full bg-indigo-500 rounded-full transition-all duration-500" style={{ width: `${goodPct}%` }}></div>
              </div>
              <span className="w-9 text-right text-[#1C1B2E] font-bold">{goodPct}%</span>
            </div>
            <div className="flex items-center gap-3 text-xs font-semibold">
              <span className="w-16 text-[#6C7089]">Fair</span>
              <div className="flex-1 h-2.5 bg-gray-100 rounded-full overflow-hidden">
                <div className="h-full bg-amber-400 rounded-full transition-all duration-500" style={{ width: `${fairPct}%` }}></div>
              </div>
              <span className="w-9 text-right text-[#1C1B2E] font-bold">{fairPct}%</span>
            </div>
            <div className="flex items-center gap-3 text-xs font-semibold">
              <span className="w-16 text-[#6C7089]">Poor</span>
              <div className="flex-1 h-2.5 bg-gray-100 rounded-full overflow-hidden">
                <div className="h-full bg-red-500 rounded-full transition-all duration-500" style={{ width: `${poorPct}%` }}></div>
              </div>
              <span className="w-9 text-right text-[#1C1B2E] font-bold">{poorPct}%</span>
            </div>
          </div>

          <button
            onClick={() => setShowReviewsModal(true)}
            className="w-full py-2.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-bold text-xs rounded-xl transition-colors flex items-center justify-center gap-2"
          >
            <MessageSquare size={15} /> View Actual Customer Reviews ({csatReviews.length})
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Agent Snapshot */}
        <div className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-base font-bold text-[#1C1B2E]">Agent Performance Snapshot</h2>
            <span className="text-xs font-bold text-[#6C7089]">{agents.length} Active Agents</span>
          </div>
          <div className="space-y-4">
            {agents.map((agent) => {
              const agentTickets = tickets.filter(t => t.agent_id === agent.id)
              const agentClosed = agentTickets.filter(t => t.status === 'resolved' || t.status === 'closed').length
              const agentTicketIds = agentTickets.map(t => t.id)
              const agentCsats = csatReviews.filter(r => agentTicketIds.includes(r.ticket_id))
              const avgCsat = agentCsats.length > 0
                ? (agentCsats.reduce((sum, r) => sum + r.rating, 0) / agentCsats.length).toFixed(1)
                : (csatReviews.length > 0 ? (csatReviews.reduce((sum, r) => sum + r.rating, 0) / csatReviews.length).toFixed(1) : '5.0')
              const agentSla = agentTickets.length > 0 ? Math.round((agentClosed / agentTickets.length) * 100) : 100

              return (
                <div key={agent.id} className="flex items-center justify-between p-3 rounded-xl hover:bg-slate-50 transition-colors">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-600 text-white flex items-center justify-center font-bold text-sm shadow-sm">
                      {agent.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()}
                    </div>
                    <div>
                      <div className="font-bold text-sm text-[#1C1B2E]">{agent.name}</div>
                      <div className="text-xs text-[#9598B0]">
                        {agentTickets.length} assigned tickets · CSAT {avgCsat} ★
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-xs font-bold text-emerald-600">{agentSla}% SLA</div>
                    <div className="text-[11px] text-[#9598B0]">{agentClosed} resolved</div>
                  </div>
                </div>
              )
            })}
            {agents.length === 0 && <div className="text-sm text-[#9598B0] text-center py-4">No active agents found</div>}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-base font-bold text-[#1C1B2E]">Recent Activity</h2>
            <button onClick={() => navigate('/manager/inbox/all')} className="text-xs font-bold text-indigo-600 hover:underline">View All</button>
          </div>
          <div className="space-y-4">
            {recentActivity.map((ticket) => (
              <div key={ticket.id} className="flex gap-3.5 p-2 rounded-xl hover:bg-slate-50 transition-colors">
                <div className="mt-0.5">
                  {ticket.ai_resolved ? (
                    <div className="w-7 h-7 bg-purple-100 rounded-lg flex items-center justify-center text-purple-600">
                      <Bot size={15} />
                    </div>
                  ) : ticket.priority === 'urgent' ? (
                    <div className="w-7 h-7 bg-red-100 rounded-lg flex items-center justify-center text-red-600">
                      <AlertTriangle size={15} />
                    </div>
                  ) : (
                    <div className="w-7 h-7 bg-emerald-100 rounded-lg flex items-center justify-center text-emerald-600">
                      <CheckCircle2 size={15} />
                    </div>
                  )}
                </div>
                <div className="flex-1">
                  <div className="text-sm font-bold text-[#1C1B2E]">
                    {ticket.ai_resolved ? `AI resolved ticket ${ticket.ref} automatically` :
                     ticket.priority === 'urgent' ? `High priority ticket ${ticket.ref} escalated` :
                     `New ticket ${ticket.ref} created via ${ticket.channel}`}
                  </div>
                  <div className="text-xs text-[#6C7089] truncate max-w-md">{ticket.subject}</div>
                  <div className="text-[11px] text-[#9598B0] mt-1 font-medium">
                    {formatDateTime(ticket.created_at)}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Actual Customer Reviews Modal */}
      {showReviewsModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-2xl rounded-2xl shadow-2xl flex flex-col max-h-[85vh] overflow-hidden animate-in fade-in zoom-in-95 duration-200">
            {/* Modal Header */}
            <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50">
              <div>
                <h3 className="font-bold text-lg text-slate-900 flex items-center gap-2">
                  <MessageSquare className="text-indigo-600" size={20} /> Actual Customer Reviews
                </h3>
                <p className="text-xs text-slate-500">Live feedback submitted by customers after ticket resolution</p>
              </div>
              <button
                onClick={() => setShowReviewsModal(false)}
                className="w-8 h-8 rounded-full bg-slate-200 hover:bg-slate-300 flex items-center justify-center text-slate-600 transition-colors"
              >
                <X size={18} />
              </button>
            </div>

            {/* Filter Tabs */}
            <div className="px-6 py-3 border-b border-slate-100 bg-white flex items-center gap-2 overflow-x-auto">
              <span className="text-xs font-bold text-slate-400 flex items-center gap-1 mr-1">
                <Filter size={14} /> Filter:
              </span>
              <button
                onClick={() => setSelectedStarFilter('all')}
                className={`px-3 py-1 rounded-full text-xs font-bold transition-colors ${selectedStarFilter === 'all' ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}`}
              >
                All ({csatReviews.length})
              </button>
              <button
                onClick={() => setSelectedStarFilter('5')}
                className={`px-3 py-1 rounded-full text-xs font-bold transition-colors ${selectedStarFilter === '5' ? 'bg-emerald-600 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}`}
              >
                5 Stars ★ ({count5Star})
              </button>
              <button
                onClick={() => setSelectedStarFilter('4')}
                className={`px-3 py-1 rounded-full text-xs font-bold transition-colors ${selectedStarFilter === '4' ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}`}
              >
                4 Stars ★ ({count4Star})
              </button>
              <button
                onClick={() => setSelectedStarFilter('3_lower')}
                className={`px-3 py-1 rounded-full text-xs font-bold transition-colors ${selectedStarFilter === '3_lower' ? 'bg-amber-600 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}`}
              >
                3 Stars & Lower ({count3Star + countLowStar})
              </button>
            </div>

            {/* Reviews List */}
            <div className="p-6 overflow-y-auto space-y-4 flex-1">
              {filteredReviews.length === 0 ? (
                <div className="text-center py-10 text-slate-400">
                  No customer reviews matching this rating filter.
                </div>
              ) : (
                filteredReviews.map((rev) => (
                  <div key={rev.id} className="p-4 rounded-xl border border-slate-100 bg-slate-50/50 hover:bg-slate-50 transition-colors">
                    <div className="flex justify-between items-start mb-2">
                      <div className="flex items-center gap-2.5">
                        <div className="w-8 h-8 rounded-full bg-indigo-100 text-indigo-700 font-bold text-xs flex items-center justify-center">
                          {rev.customer_name?.substring(0, 2).toUpperCase() || 'CU'}
                        </div>
                        <div>
                          <div className="text-xs font-bold text-slate-900">{rev.customer_name}</div>
                          <div className="text-[11px] text-slate-500 font-mono">{rev.ticket_ref} · {rev.ticket_subject}</div>
                        </div>
                      </div>
                      <div className="flex items-center gap-1 bg-amber-50 text-amber-700 border border-amber-200 px-2 py-0.5 rounded-full text-xs font-bold">
                        <span>{rev.rating}</span>
                        <Star fill="currentColor" size={12} className="text-amber-500" />
                      </div>
                    </div>
                    {rev.comment && (
                      <p className="text-xs text-slate-700 italic bg-white p-3 rounded-lg border border-slate-100 mt-2">
                        "{rev.comment}"
                      </p>
                    )}
                    <div className="text-[10px] text-slate-400 text-right mt-2">
                      {formatDateTime(rev.created_at)}
                    </div>
                  </div>
                ))
              )}
            </div>

            {/* Modal Footer */}
            <div className="p-4 border-t border-slate-100 bg-slate-50 flex justify-end">
              <button
                onClick={() => setShowReviewsModal(false)}
                className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs rounded-xl transition-colors"
              >
                Close Reviews
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
