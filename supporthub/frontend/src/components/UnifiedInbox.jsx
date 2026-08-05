import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { ticketsApi } from '../api/tickets'
import { 
  CheckCircle, Search, Filter, Bell, Mail, MessageSquare, 
  Smartphone, Instagram, Facebook, AlertCircle, Bot
} from 'lucide-react'

export default function UnifiedInbox({ filter, basePath }) {
  const navigate = useNavigate()
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedChannel, setSelectedChannel] = useState('all')

  const { data: rawTickets = [], isLoading } = useQuery({
    queryKey: ['tickets', basePath, filter],
    queryFn: async () => {
      const params = (filter !== 'all' && filter !== 'active' && filter !== 'closed' && filter !== 'resolved') ? { status: filter } : {}
      const res = await ticketsApi.list(params)
      return res.data
    },
  })

  // Apply active status filter & channel filter & search term
  const tickets = rawTickets.filter(t => {
    // Status filter
    if (filter === 'active' && (t.status === 'resolved' || t.status === 'closed')) return false
    if ((filter === 'closed' || filter === 'resolved') && (t.status !== 'resolved' && t.status !== 'closed')) return false
    
    // Channel filter
    if (selectedChannel !== 'all' && t.channel !== selectedChannel) return false

    // Search term
    if (searchTerm.trim()) {
      const q = searchTerm.toLowerCase()
      const subjectMatch = t.subject?.toLowerCase().includes(q)
      const refMatch = t.ref?.toLowerCase().includes(q)
      const categoryMatch = t.category?.toLowerCase().includes(q)
      return subjectMatch || refMatch || categoryMatch
    }

    return true
  })

  const channels = [
    { id: 'all', label: 'All Channels' },
    { id: 'email', label: 'Email', icon: Mail },
    { id: 'website_chat', label: 'Website Chat', icon: MessageSquare },
    { id: 'whatsapp', label: 'WhatsApp', icon: Smartphone },
    { id: 'instagram', label: 'Instagram', icon: Instagram },
    { id: 'facebook', label: 'Facebook', icon: Facebook },
  ]

  const getChannelBadge = (channel) => {
    switch (channel) {
      case 'email':
        return <span className="flex items-center gap-1.5 text-xs text-[#6C7089]"><Mail size={14} className="text-indigo-500" /> Email</span>
      case 'website_chat':
        return <span className="flex items-center gap-1.5 text-xs text-[#6C7089]"><MessageSquare size={14} className="text-blue-500" /> Website Chat</span>
      case 'whatsapp':
        return <span className="flex items-center gap-1.5 text-xs text-[#6C7089]"><Smartphone size={14} className="text-emerald-500" /> WhatsApp</span>
      case 'instagram':
        return <span className="flex items-center gap-1.5 text-xs text-[#6C7089]"><Instagram size={14} className="text-purple-500" /> Instagram</span>
      case 'facebook':
        return <span className="flex items-center gap-1.5 text-xs text-[#6C7089]"><Facebook size={14} className="text-blue-600" /> Facebook</span>
      default:
        return <span className="flex items-center gap-1.5 text-xs text-[#6C7089]"><MessageSquare size={14} /> {channel}</span>
    }
  }

  const getStatusBadge = (status) => {
    switch (status) {
      case 'resolved':
      case 'closed':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-50 text-emerald-600 border border-emerald-200">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> Resolved
          </span>
        )
      case 'open':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-blue-50 text-blue-600 border border-blue-200">
            <span className="w-1.5 h-1.5 rounded-full bg-blue-500"></span> Open
          </span>
        )
      case 'new':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-sky-50 text-sky-600 border border-sky-200">
            <span className="w-1.5 h-1.5 rounded-full bg-sky-500"></span> New
          </span>
        )
      case 'waiting':
      case 'pending':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-amber-50 text-amber-600 border border-amber-200">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-500"></span> Waiting
          </span>
        )
      case 'escalated':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-rose-50 text-rose-600 border border-rose-200">
            <span className="w-1.5 h-1.5 rounded-full bg-rose-500"></span> Escalated
          </span>
        )
      default:
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-gray-100 text-gray-600 border border-gray-200">
            {status}
          </span>
        )
    }
  }

  const getPriorityStyle = (priority) => {
    switch (priority) {
      case 'urgent': return 'text-rose-600 font-bold'
      case 'high': return 'text-amber-600 font-bold'
      case 'medium': return 'text-amber-700 font-semibold'
      default: return 'text-gray-600 font-medium'
    }
  }

  const getAgentBadge = (ticket) => {
    if (ticket.ai_resolved || ticket.sender_type === 'ai') {
      return (
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 rounded-full bg-purple-600 text-white flex items-center justify-center text-[10px]">
            <Bot size={12} />
          </div>
          <span className="text-xs font-semibold text-[#1C1B2E]">AI Assistant</span>
        </div>
      )
    }
    if (!ticket.agent_id) {
      return <span className="text-xs text-[#9598B0] font-medium">Unassigned</span>
    }
    return (
      <div className="flex items-center gap-2">
        <div className="w-6 h-6 rounded-full bg-indigo-600 text-white font-bold text-[10px] flex items-center justify-center">
          EW
        </div>
        <span className="text-xs font-semibold text-[#1C1B2E]">Emma Wilson</span>
      </div>
    )
  }

  const getSlaBadge = (ticket) => {
    if (ticket.status === 'resolved' || ticket.status === 'closed') {
      return <span className="text-xs text-[#6C7089]">Closed on time</span>
    }
    if (ticket.priority === 'urgent' || ticket.status === 'escalated') {
      return <span className="text-xs text-rose-600 font-bold">Overdue by 38m</span>
    }
    if (ticket.status === 'waiting') {
      return <span className="text-xs text-amber-600 font-semibold">1h 05m left</span>
    }
    return <span className="text-xs text-emerald-600 font-semibold">2h 45m left</span>
  }

  const pageTitle = filter === 'active' ? 'Active Tickets' : (filter === 'closed' || filter === 'resolved') ? 'Closed Tickets' : filter === 'waiting' ? 'Snoozed Tickets' : filter === 'escalated' ? 'Escalated Tickets' : 'All Tickets'

  return (
    <div className="flex-1 flex flex-col h-screen bg-[#F6F7FC] overflow-hidden text-[#1C1B2E]">
      {/* Top Header Bar */}
      <div className="h-16 bg-white border-b border-[#E5E7F3] px-8 flex items-center justify-between shrink-0">
        <h1 className="text-xl font-bold font-['Plus_Jakarta_Sans']">{pageTitle}</h1>
        <div className="flex items-center gap-4">
          <div className="relative w-80">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-[#9598B0]" size={16} />
            <input
              type="text"
              placeholder="Search tickets, customers, articles..."
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl pl-9 pr-4 py-2 text-xs outline-none focus:border-indigo-500 transition-colors"
            />
          </div>
          <div className="relative cursor-pointer p-2 rounded-xl hover:bg-gray-100 transition-colors text-[#6C7089]">
            <Bell size={18} />
            <span className="absolute top-1 right-1 w-4 h-4 bg-rose-500 text-white font-bold text-[9px] rounded-full flex items-center justify-center">4</span>
          </div>
          <div className="w-8 h-8 rounded-full bg-indigo-600 text-white font-bold text-xs flex items-center justify-center">
            EW
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 overflow-y-auto p-8 space-y-6">
        <div>
          <h2 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">{pageTitle}</h2>
          <p className="text-[#6C7089] text-xs mt-0.5">All customer conversations, across every channel, in one place.</p>
        </div>

        {/* Filter Pills Bar */}
        <div className="flex items-center justify-between flex-wrap gap-3">
          <div className="flex items-center gap-2 overflow-x-auto pb-1">
            {channels.map(ch => {
              const Icon = ch.icon
              const isSelected = selectedChannel === ch.id
              return (
                <button
                  key={ch.id}
                  onClick={() => setSelectedChannel(ch.id)}
                  className={`flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold transition-all whitespace-nowrap ${
                    isSelected
                      ? 'bg-[#6366F1] text-white shadow-sm'
                      : 'bg-white text-[#6C7089] hover:bg-gray-50 border border-[#E5E7F3]'
                  }`}
                >
                  {Icon && <Icon size={14} />}
                  {ch.label}
                </button>
              )
            })}
          </div>

          <button className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold bg-white text-[#6C7089] border border-[#E5E7F3] hover:bg-gray-50 transition-colors">
            <Filter size={14} /> Filter
          </button>
        </div>

        {/* Data Table */}
        <div className="bg-white rounded-2xl border border-[#E5E7F3] shadow-sm overflow-hidden">
          {isLoading ? (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div>
            </div>
          ) : tickets.length === 0 ? (
            <div className="text-center py-20 text-[#6C7089]">
              <CheckCircle size={48} className="mx-auto mb-4 text-[#E5E7F3]" />
              <p className="font-bold text-base text-[#1C1B2E]">No messages found</p>
              <p className="text-xs text-[#9598B0] mt-1">There are no tickets matching your current search and channel filter.</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr className="border-b border-[#E5E7F3] bg-[#F9FAFB] text-[10px] uppercase font-bold text-[#9598B0] tracking-wider">
                    <th className="py-3.5 px-6">Ticket</th>
                    <th className="py-3.5 px-6">Subject</th>
                    <th className="py-3.5 px-6">Channel</th>
                    <th className="py-3.5 px-6">Status</th>
                    <th className="py-3.5 px-6">Priority</th>
                    <th className="py-3.5 px-6">Agent</th>
                    <th className="py-3.5 px-6">SLA</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#E5E7F3]">
                  {tickets.map(ticket => (
                    <tr
                      key={ticket.id}
                      onClick={() => navigate(`${basePath}/tickets/${ticket.id}`)}
                      className="hover:bg-indigo-50/40 transition-colors cursor-pointer"
                    >
                      <td className="py-4 px-6 font-mono text-[#9598B0] font-medium whitespace-nowrap">
                        {ticket.ref}
                      </td>
                      <td className="py-4 px-6 max-w-xs">
                        <div className="font-bold text-[#1C1B2E] text-xs line-clamp-1">{ticket.subject}</div>
                        <div className="text-[11px] text-[#9598B0] mt-0.5 capitalize">
                          {ticket.customer?.name || 'Sarah Johnson'} · {ticket.category || 'General'}
                        </div>
                      </td>
                      <td className="py-4 px-6 whitespace-nowrap">
                        {getChannelBadge(ticket.channel)}
                      </td>
                      <td className="py-4 px-6 whitespace-nowrap">
                        {getStatusBadge(ticket.status)}
                      </td>
                      <td className={`py-4 px-6 whitespace-nowrap capitalize ${getPriorityStyle(ticket.priority)}`}>
                        {ticket.priority || 'medium'}
                      </td>
                      <td className="py-4 px-6 whitespace-nowrap">
                        {getAgentBadge(ticket)}
                      </td>
                      <td className="py-4 px-6 whitespace-nowrap">
                        {getSlaBadge(ticket)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
