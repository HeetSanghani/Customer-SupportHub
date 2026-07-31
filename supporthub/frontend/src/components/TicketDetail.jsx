import { useState, useEffect, useRef } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { ticketsApi } from '../api/tickets'
import { useAuthStore } from '../store/authStore'
import { Send, ArrowLeft, Clock, CheckCircle, Zap, Search, X } from 'lucide-react'

export default function TicketDetail({ basePath }) {
  const { id } = useParams()
  const navigate = useNavigate()
  const { token, role, name: currentName } = useAuthStore()
  const queryClient = useQueryClient()
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)
  
  const [messages, setMessages] = useState([])
  const [inputText, setInputText] = useState('')
  const [ws, setWs] = useState(null)
  const [showQuickReplies, setShowQuickReplies] = useState(false)
  const [quickSearch, setQuickSearch] = useState('')

  const quickReplyTemplates = [
    {
      id: '1',
      title: 'Refund Processed',
      category: 'Billing',
      content: 'Your refund has been processed and should appear in 5-7 business days.'
    },
    {
      id: '2',
      title: 'Order Shipped',
      category: 'Orders',
      content: 'Great news — your order has shipped! Tracking details are on their way to your inbox.'
    },
    {
      id: '3',
      title: 'Password Reset Sent',
      category: 'Account',
      content: "I've sent a password reset link to your registered email, valid for 30 minutes."
    },
    {
      id: '4',
      title: 'Escalation Notice',
      category: 'General',
      content: "I'm looping in a specialist who can dig deeper into this for you — you'll hear back within 2 hours."
    },
    {
      id: '5',
      title: 'CSAT Follow-up',
      category: 'General',
      content: "Glad we could help! We'd love your feedback — a quick survey link is on its way."
    },
    {
      id: '6',
      title: 'Shipping Delay Apology',
      category: 'Shipping',
      content: 'Apologies for the delay — your courier is reporting a short hold, updated ETA is within 48 hours.'
    }
  ]

  const filteredQuickReplies = quickReplyTemplates.filter(r => 
    r.title.toLowerCase().includes(quickSearch.toLowerCase()) ||
    r.category.toLowerCase().includes(quickSearch.toLowerCase()) ||
    r.content.toLowerCase().includes(quickSearch.toLowerCase())
  )

  const { data: ticket, isLoading } = useQuery({
    queryKey: ['ticket', id],
    queryFn: async () => {
      const res = await ticketsApi.get(id)
      return res.data
    },
  })

  // Fetch initial messages
  useEffect(() => {
    ticketsApi.getMessages(id).then(res => setMessages(res.data)).catch(console.error)
  }, [id])

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // WebSocket Connection
  useEffect(() => {
    if (!token) return

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    // Assume backend is on the Vite proxy host (which doesn't proxy WS well if not configured)
    // Actually Vite proxies WS if configured, but let's connect directly to backend for safety.
    // Wait, let's use the standard WS proxy or direct backend URL.
    // We'll connect directly to 8001 to avoid Vite proxy issues for websockets in dev.
    const wsUrl = `ws://localhost:8001/ws/chat/${id}?token=${token}`
    
    const socket = new WebSocket(wsUrl)
    
    socket.onopen = () => console.log('WS Connected to room:', id)
    
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'message') {
        setMessages(prev => [...prev, data])
      }
    }
    
    socket.onclose = () => console.log('WS Disconnected')
    setWs(socket)
    
    return () => socket.close()
  }, [id, token])

  const sendMessage = (e) => {
    e.preventDefault()
    if (!inputText.trim() || !ws) return
    
    ws.send(JSON.stringify({ type: 'message', body: inputText }))
    setInputText('')
  }

  const updateMutation = useMutation({
    mutationFn: (data) => ticketsApi.update(id, data),
    onSuccess: (res) => {
      queryClient.setQueryData(['ticket', id], res.data)
    }
  })

  if (isLoading) return <div className="flex justify-center py-20"><div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div></div>
  if (!ticket) return <div className="p-8">Ticket not found</div>

  return (
    <div className="flex-1 flex h-full bg-white overflow-hidden">
      {/* Left Chat Area */}
      <div className="flex-1 flex flex-col min-w-0 border-r border-[#E5E7F3]">
        {/* Header */}
        <div className="px-6 py-4 border-b border-[#E5E7F3] flex items-center justify-between bg-white shadow-sm z-10">
          <div className="flex items-center gap-4">
            <button onClick={() => navigate(basePath)} className="text-[#9598B0] hover:text-[#1C1B2E] transition-colors p-1 -ml-1">
              <ArrowLeft size={20} />
            </button>
            <div>
              <div className="flex items-center gap-3 mb-1">
                <h1 className="text-lg font-bold text-[#1C1B2E] truncate max-w-md">{ticket.subject}</h1>
                <span className="px-2 py-0.5 border border-[#E5E7F3] rounded-md text-xs font-bold uppercase text-[#6C7089]">{ticket.status}</span>
              </div>
              <p className="text-xs text-[#9598B0] font-mono">{ticket.ref} • {new Date(ticket.created_at).toLocaleString()}</p>
            </div>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 bg-[#F6F7FC] space-y-6">
          {messages.map((msg, i) => {
            const isCustomer = msg.sender_type === 'customer' || msg.sender_role === 'customer'
            const isSystem = msg.sender_type === 'system'
            const isAI = msg.sender_type === 'ai'
            
            if (isSystem) {
              return (
                <div key={i} className="flex justify-center my-2">
                  <div className="bg-[#E5E7F3] text-[#6C7089] text-xs px-3.5 py-1.5 rounded-full font-medium shadow-xs">
                    {msg.body}
                  </div>
                </div>
              )
            }

            return (
              <div key={i} className={`flex ${isCustomer ? 'justify-start' : 'justify-end'}`}>
                <div className={`max-w-[75%] rounded-2xl p-4 ${
                  isCustomer
                    ? 'bg-white text-[#1C1B2E] rounded-bl-none shadow-sm border border-[#E5E7F3]' 
                    : isAI 
                    ? 'bg-[#F5F3FF] text-[#4C1D95] rounded-br-none shadow-sm border border-[#DDD6FE]' 
                    : 'bg-[#6366F1] text-white rounded-br-none shadow-md'
                }`}>
                  <div className="flex justify-between items-baseline mb-1 gap-4">
                    <span className="text-xs font-bold opacity-85 flex items-center gap-1">
                      {isCustomer ? (msg.sender_name || 'Customer User') : isAI ? '✨ AI Agent' : (msg.sender_name || 'Agent User')}
                    </span>
                    <span className="text-[10px] opacity-70">
                      {new Date(msg.created_at || Date.now()).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                  <p className="text-sm whitespace-pre-wrap leading-relaxed">{msg.body}</p>
                </div>
              </div>
            )
          })}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="relative p-4 bg-white border-t border-[#E5E7F3]">
          {/* Quick Reply Popover Menu */}
          {showQuickReplies && (
            <div className="absolute bottom-full mb-3 left-4 right-4 bg-white border border-[#E5E7F3] rounded-2xl shadow-2xl p-4 z-50 space-y-3 max-h-72 flex flex-col">
              <div className="flex items-center justify-between pb-2 border-b border-[#E5E7F3]">
                <div className="flex items-center gap-2 font-bold text-xs text-[#1C1B2E]">
                  <Zap size={14} className="text-amber-500 fill-amber-500" />
                  <span>Insert Quick Reply</span>
                </div>
                <button
                  type="button"
                  onClick={() => setShowQuickReplies(false)}
                  className="text-[#9598B0] hover:text-[#1C1B2E] p-1 rounded-lg hover:bg-gray-100"
                >
                  <X size={16} />
                </button>
              </div>

              <div className="relative">
                <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#9598B0]" />
                <input
                  type="text"
                  placeholder="Search templates or categories..."
                  value={quickSearch}
                  onChange={e => setQuickSearch(e.target.value)}
                  className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl pl-8 pr-3 py-1.5 text-xs outline-none focus:border-indigo-500"
                />
              </div>

              <div className="flex-1 overflow-y-auto space-y-2 pr-1">
                {filteredQuickReplies.map(tpl => (
                  <button
                    key={tpl.id}
                    type="button"
                    onClick={() => {
                      setInputText(tpl.content)
                      setShowQuickReplies(false)
                      setQuickSearch('')
                      inputRef.current?.focus()
                    }}
                    className="w-full p-2.5 rounded-xl border border-[#E5E7F3] hover:border-indigo-300 hover:bg-indigo-50/30 text-left transition-all space-y-1 group"
                  >
                    <div className="flex justify-between items-center text-xs">
                      <span className="font-bold text-[#1C1B2E] group-hover:text-indigo-600">{tpl.title}</span>
                      <span className="text-[10px] font-semibold px-2 py-0.5 rounded-md bg-gray-100 text-[#6C7089]">
                        {tpl.category}
                      </span>
                    </div>
                    <p className="text-[11px] text-[#6C7089] line-clamp-1 italic">
                      "{tpl.content}"
                    </p>
                  </button>
                ))}

                {filteredQuickReplies.length === 0 && (
                  <div className="text-center py-6 text-xs text-[#9598B0]">
                    No quick replies match "{quickSearch}"
                  </div>
                )}
              </div>
            </div>
          )}

          {ticket.status === 'closed' || ticket.status === 'resolved' ? (
            <div className="text-center p-4 text-[#9598B0] bg-gray-50 rounded-xl border border-[#E5E7F3] font-medium text-xs flex items-center justify-center gap-2">
              <span className="w-2 h-2 rounded-full bg-gray-400"></span>
              This ticket is <span className="font-bold capitalize">{ticket.status}</span>. Messaging and Quick Replies are only available for active tickets.
            </div>
          ) : (
            <form onSubmit={sendMessage} className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setShowQuickReplies(!showQuickReplies)}
                className={`p-3 rounded-xl border transition-colors flex items-center gap-1.5 text-xs font-semibold ${
                  showQuickReplies 
                    ? 'bg-amber-500 text-white border-amber-500 shadow-sm' 
                    : 'bg-[#F6F7FC] hover:bg-gray-100 text-[#6C7089] border-[#E5E7F3]'
                }`}
                title="Insert Quick Reply (or type /)"
              >
                <Zap size={18} className={showQuickReplies ? 'fill-white' : 'text-amber-500 fill-amber-500'} />
              </button>

              <input 
                ref={inputRef}
                type="text" 
                placeholder="Type your message or / for quick replies..." 
                className="flex-1 border border-[#E5E7F3] rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
                value={inputText}
                onChange={e => {
                  const val = e.target.value
                  setInputText(val)
                  if (val === '/') {
                    setShowQuickReplies(true)
                  }
                }}
              />

              <button 
                type="submit" 
                disabled={!inputText.trim() || !ws}
                className="bg-indigo-600 hover:bg-indigo-700 text-white p-3 rounded-xl transition-colors disabled:opacity-50"
              >
                <Send size={20} />
              </button>
            </form>
          )}
        </div>
      </div>

      {/* Right Sidebar (Details/Actions) */}
      <div className="w-80 bg-white p-6 border-l border-[#E5E7F3] overflow-y-auto">
        <h3 className="font-bold text-[#1C1B2E] mb-6 uppercase text-xs tracking-wider">Ticket Details</h3>
        
        <div className="space-y-6">
          <div>
            <div className="text-xs text-[#9598B0] mb-1">Customer</div>
            <div className="font-semibold text-[#1C1B2E]">{role === 'customer' ? currentName : ticket.customer_id}</div>
          </div>
          
          <div>
            <div className="text-xs text-[#9598B0] mb-1">Category</div>
            <div className="capitalize text-sm bg-gray-100 inline-block px-2 py-1 rounded font-medium">{ticket.category}</div>
          </div>

          <div>
            <div className="text-xs text-[#9598B0] mb-1">Priority</div>
            {role === 'customer' ? (
               <div className="capitalize text-sm font-bold">{ticket.priority}</div>
            ) : (
              <select 
                className="w-full text-sm border border-[#E5E7F3] rounded-lg p-2 outline-none focus:border-indigo-500 capitalize font-bold"
                value={ticket.priority}
                onChange={e => updateMutation.mutate({ priority: e.target.value })}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            )}
          </div>

          {(role === 'agent' || role === 'admin') && (
            <div>
              <div className="text-xs text-[#9598B0] mb-1">Status</div>
              <div className="flex flex-wrap gap-2">
                <button 
                  onClick={() => updateMutation.mutate({ status: 'open' })}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold border transition-colors ${ticket.status === 'open' ? 'bg-indigo-50 border-indigo-200 text-indigo-700' : 'bg-white border-[#E5E7F3] text-[#6C7089] hover:bg-gray-50'}`}
                >
                  Open
                </button>
                <button 
                  onClick={() => updateMutation.mutate({ status: 'waiting' })}
                  className={`flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-bold border transition-colors ${ticket.status === 'waiting' ? 'bg-orange-50 border-orange-200 text-orange-700' : 'bg-white border-[#E5E7F3] text-[#6C7089] hover:bg-gray-50'}`}
                >
                  <Clock size={14} /> Snooze
                </button>
                <button 
                  onClick={() => updateMutation.mutate({ status: 'resolved' })}
                  className={`flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-bold border transition-colors ${ticket.status === 'resolved' ? 'bg-green-50 border-green-200 text-green-700' : 'bg-white border-[#E5E7F3] text-[#6C7089] hover:bg-gray-50'}`}
                >
                  <CheckCircle size={14} /> Resolve
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
