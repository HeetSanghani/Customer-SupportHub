import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { ticketsApi } from '../../api/tickets'
import { useNavigate } from 'react-router-dom'
import { MessageSquare, Mail, AlertCircle, CheckCircle, Search, Bell } from 'lucide-react'

export default function AgentTicketQueue() {
  const navigate = useNavigate()
  const [searchTerm, setSearchTerm] = useState('')

  const { data: tickets = [], isLoading } = useQuery({
    queryKey: ['tickets', 'queue'],
    queryFn: async () => {
      const res = await ticketsApi.list()
      return res.data
    }
  })

  // Filter tickets based on search
  const filtered = tickets.filter(t => 
    t.subject?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    t.ref?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  // Categorize into Kanban Columns
  const newTickets = filtered.filter(t => !t.agent_id && t.status !== 'resolved' && t.status !== 'closed' && t.status !== 'escalated')
  const openTickets = filtered.filter(t => t.status === 'open' && t.agent_id)
  const waitingTickets = filtered.filter(t => t.status === 'pending' || t.status === 'waiting')
  const escalatedTickets = filtered.filter(t => t.status === 'escalated' || t.priority === 'urgent')
  const resolvedTickets = filtered.filter(t => t.status === 'resolved' || t.status === 'closed')

  const columns = [
    { id: 'new', label: 'New', color: 'bg-blue-500', count: newTickets.length, tickets: newTickets },
    { id: 'open', label: 'Open', color: 'bg-purple-500', count: openTickets.length, tickets: openTickets },
    { id: 'waiting', label: 'Waiting', color: 'bg-amber-500', count: waitingTickets.length, tickets: waitingTickets },
    { id: 'escalated', label: 'Escalated', color: 'bg-rose-500', count: escalatedTickets.length, tickets: escalatedTickets },
    { id: 'resolved', label: 'Resolved', color: 'bg-emerald-500', count: resolvedTickets.length, tickets: resolvedTickets },
  ]

  const getPriorityBadge = (priority) => {
    switch (priority) {
      case 'urgent': return 'bg-rose-50 text-rose-600 border-rose-200'
      case 'high': return 'bg-amber-50 text-amber-600 border-amber-200'
      case 'medium': return 'bg-amber-50/60 text-amber-700 border-amber-200'
      default: return 'bg-gray-50 text-gray-600 border-gray-200'
    }
  }

  const getChannelName = (channel) => {
    if (!channel) return 'Website Chat'
    return channel.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())
  }

  return (
    <div className="flex-1 flex flex-col h-screen bg-[#F6F7FC] overflow-hidden text-[#1C1B2E]">
      {/* Top Header Bar */}
      <div className="h-16 bg-white border-b border-[#E5E7F3] px-8 flex items-center justify-between shrink-0">
        <h1 className="text-xl font-bold font-['Plus_Jakarta_Sans']">Ticket Queue</h1>
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

      {/* Main Kanban Content Area */}
      <div className="flex-1 overflow-x-auto p-8">
        <div className="mb-6">
          <h2 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">Ticket Queue</h2>
          <p className="text-[#6C7089] text-xs mt-0.5">Drag-and-drop kanban view of all tickets by status.</p>
        </div>

        {isLoading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div>
          </div>
        ) : (
          <div className="grid grid-cols-5 gap-4 min-w-[1100px] h-[calc(100vh-210px)]">
            {columns.map(col => (
              <div key={col.id} className="bg-[#F1F3F9]/70 border border-[#E5E7F3] rounded-2xl p-4 flex flex-col overflow-hidden">
                {/* Column Header */}
                <div className="flex items-center justify-between mb-4 px-1">
                  <div className="flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full ${col.color}`}></div>
                    <span className="font-bold text-sm text-[#1C1B2E]">{col.label}</span>
                  </div>
                  <span className="text-xs font-bold bg-white text-[#6C7089] px-2 py-0.5 rounded-full border border-[#E5E7F3]">
                    {col.count}
                  </span>
                </div>

                {/* Column Cards Container */}
                <div className="flex-1 overflow-y-auto space-y-3 pr-1">
                  {col.tickets.map(t => (
                    <div
                      key={t.id}
                      onClick={() => navigate(`/agent/tickets/${t.id}`)}
                      className="bg-white p-4 rounded-xl border border-[#E5E7F3] shadow-sm hover:shadow-md hover:border-indigo-300 transition-all cursor-pointer space-y-2.5"
                    >
                      <div className="flex justify-between items-center text-[11px] font-mono text-[#9598B0]">
                        <span>{t.ref} · <span className="font-sans text-[#6C7089]">{getChannelName(t.channel)}</span></span>
                      </div>

                      <h4 className="font-bold text-xs text-[#1C1B2E] line-clamp-2 leading-snug">
                        {t.subject}
                      </h4>

                      <div className="flex items-center justify-between pt-1">
                        <span className={`text-[10px] font-bold px-2 py-0.5 rounded-md border capitalize ${getPriorityBadge(t.priority)}`}>
                          {t.priority || 'medium'}
                        </span>
                        <div className="w-5 h-5 rounded-full bg-indigo-600 text-white font-bold text-[9px] flex items-center justify-center uppercase">
                          {t.agent_id ? 'EW' : 'AI'}
                        </div>
                      </div>
                    </div>
                  ))}

                  {col.tickets.length === 0 && (
                    <div className="h-32 rounded-xl border border-dashed border-[#E5E7F3] flex items-center justify-center text-[11px] text-[#9598B0]">
                      No tickets
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
