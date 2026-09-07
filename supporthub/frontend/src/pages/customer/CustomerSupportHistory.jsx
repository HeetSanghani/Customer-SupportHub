import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { ticketsApi } from '../../api/tickets'
import { MessageSquare, ArrowLeft, Send, CheckCircle2, Clock, Sparkles } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function CustomerSupportHistory() {
  const [selectedTicketId, setSelectedTicketId] = useState(null)
  const [replyText, setReplyText] = useState('')

  const { data: tickets = [], isLoading: loadingTickets, refetch: refetchTickets } = useQuery({
    queryKey: ['tickets', 'customer'],
    queryFn: async () => {
      const res = await ticketsApi.list()
      return res.data
    },
  })

  const { data: messages = [], refetch: refetchMessages } = useQuery({
    queryKey: ['ticket-messages', selectedTicketId],
    queryFn: async () => {
      if (!selectedTicketId) return []
      const res = await ticketsApi.getMessages(selectedTicketId)
      return res.data
    },
    enabled: !!selectedTicketId,
  })

  const handleSendMessage = async (e) => {
    e.preventDefault()
    if (!replyText.trim() || !selectedTicketId) return
    try {
      await ticketsApi.addMessage(selectedTicketId, { body: replyText })
      setReplyText('')
      refetchMessages()
    } catch (err) {
      console.error(err)
    }
  }

  const selectedTicket = tickets.find(t => t.id === selectedTicketId)

  return (
    <div className="flex-1 overflow-y-auto bg-[#F8FAFC] p-4 md:p-8 space-y-6">
      <div>
        <Link to="/customer" className="inline-flex items-center gap-1.5 text-xs font-extrabold text-indigo-600 hover:text-indigo-700 mb-2 transition-colors">
          <ArrowLeft size={14} /> Back to AI Chat
        </Link>
        <h1 className="text-2xl font-black text-[#0F172A] tracking-tight">Support Ticket History</h1>
        <p className="text-xs md:text-sm text-[#64748B]">Review your past inquiries, AI automated replies, and active conversation threads.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Ticket List (1 col) */}
        <div className="bg-white border border-[#E2E8F0] rounded-3xl p-6 shadow-2xs space-y-4">
          <h2 className="text-lg font-bold text-[#0F172A]">Your Tickets ({tickets.length})</h2>
          {loadingTickets ? (
            <div className="text-center py-8 text-[#94A3B8] text-sm">Loading tickets...</div>
          ) : tickets.length === 0 ? (
            <div className="text-center py-8 text-[#94A3B8] text-sm font-semibold">No support tickets found.</div>
          ) : (
            <div className="space-y-2.5">
              {tickets.map(t => (
                <div
                  key={t.id}
                  onClick={() => setSelectedTicketId(t.id)}
                  className={`p-4 rounded-2xl border transition-colors cursor-pointer ${
                    selectedTicketId === t.id
                      ? 'border-indigo-600 bg-indigo-50/60 ring-1 ring-indigo-200'
                      : 'border-[#E2E8F0] hover:border-indigo-200 bg-[#F8FAFC]'
                  }`}
                >
                  <div className="flex items-center justify-between text-xs mb-1">
                    <span className="font-bold text-indigo-600 font-mono">{t.ref}</span>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      t.status === 'resolved' || t.status === 'closed'
                        ? 'bg-emerald-100 text-emerald-800'
                        : 'bg-indigo-100 text-indigo-800'
                    }`}>
                      {t.status}
                    </span>
                  </div>
                  <div className="text-sm font-bold text-[#0F172A] truncate">{t.subject}</div>
                  <div className="text-xs text-[#64748B] mt-1 capitalize">Channel: {t.channel} • Category: {t.category}</div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Selected Ticket Thread (2 cols) */}
        <div className="lg:col-span-2 bg-white border border-[#E2E8F0] rounded-3xl p-6 shadow-2xs flex flex-col min-h-[500px]">
          {!selectedTicketId ? (
            <div className="flex-1 flex flex-col items-center justify-center text-[#94A3B8] text-center p-8">
              <MessageSquare size={48} className="text-indigo-200 mb-3" />
              <div className="font-bold text-[#0F172A]">No Ticket Selected</div>
              <p className="text-sm text-[#64748B] mt-1 max-w-sm">Select a support ticket from the list on the left to view the full message thread.</p>
            </div>
          ) : (
            <>
              {/* Header */}
              <div className="border-b border-[#E2E8F0] pb-4 mb-4 flex items-center justify-between">
                <div>
                  <div className="text-xs text-[#64748B]">Ref: <span className="font-bold text-indigo-600 font-mono">{selectedTicket?.ref}</span></div>
                  <h3 className="text-lg font-bold text-[#0F172A]">{selectedTicket?.subject}</h3>
                </div>
                <div className="flex items-center gap-2">
                  <Link to={`/customer/chat/${selectedTicketId}`}
                    className="px-3.5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-extrabold transition-colors flex items-center gap-1.5 shadow-xs">
                    <Sparkles size={14} className="text-amber-300" /> Open in Live AI Chat
                  </Link>
                </div>
              </div>

              {/* Messages Thread */}
              <div className="flex-1 overflow-y-auto space-y-3.5 mb-4 pr-2">
                {messages.length === 0 ? (
                  <div className="text-center text-xs text-[#94A3B8] py-6">No messages in thread.</div>
                ) : (
                  messages.map(m => (
                    <div
                      key={m.id}
                      className={`flex flex-col max-w-[80%] p-3.5 rounded-2xl ${
                        m.sender_type === 'customer'
                          ? 'ml-auto bg-indigo-600 text-white rounded-br-none'
                          : 'mr-auto bg-[#F8FAFC] text-[#0F172A] border border-[#E2E8F0] rounded-bl-none'
                      }`}
                    >
                      <div className="text-[10px] font-bold opacity-70 mb-1 flex items-center justify-between gap-4">
                        <span>{m.sender_name || (m.sender_type === 'ai' ? 'SupportHub AI' : 'Agent')}</span>
                        <span>{new Date(m.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                      </div>
                      <div className="text-sm whitespace-pre-wrap">{m.body}</div>
                    </div>
                  ))
                )}
              </div>

              {/* Reply Input */}
              <form onSubmit={handleSendMessage} className="flex gap-2 pt-3 border-t border-[#E2E8F0]">
                <input
                  type="text"
                  placeholder="Type a reply to support..."
                  value={replyText}
                  onChange={e => setReplyText(e.target.value)}
                  className="flex-1 px-4 py-2.5 rounded-xl border border-[#E2E8F0] text-sm focus:outline-none focus:border-indigo-600"
                />
                <button
                  type="submit"
                  className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-extrabold transition-colors flex items-center gap-1.5 shadow-xs"
                >
                  <Send size={14} /> Send
                </button>
              </form>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
