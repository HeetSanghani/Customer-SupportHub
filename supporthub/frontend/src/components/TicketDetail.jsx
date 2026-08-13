import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { ticketsApi } from '../api/tickets'
import { useAuthStore } from '../store/authStore'
import { ArrowLeft, Send, Bot, Clock, Zap, X, Search, Paperclip, Sparkles, Copy, CheckCheck, FileText, Link2, RefreshCw, ChevronDown, ChevronUp, Lightbulb } from 'lucide-react'
import client from '../api/client'
import { formatDateTime, formatTime } from '../utils/dateUtils'

export default function TicketDetail({ basePath }) {
  const { id } = useParams()
  const navigate = useNavigate()
  const { token, role, name: currentName } = useAuthStore()
  const queryClient = useQueryClient()
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)
  
  const [messages, setMessages] = useState([])
  const [inputText, setInputText] = useState('')
  const [wsConnected, setWsConnected] = useState(false)
  const wsRef = useRef(null)
  const [showQuickReplies, setShowQuickReplies] = useState(false)
  const [quickSearch, setQuickSearch] = useState('')

  // Phase 6 — AI Agent Tools state
  const [aiSuggestion, setAiSuggestion] = useState(null)
  const [aiSummary, setAiSummary] = useState(null)
  const [similarTickets, setSimilarTickets] = useState([])
  const [loadingSuggest, setLoadingSuggest] = useState(false)
  const [loadingSummary, setLoadingSummary] = useState(false)
  const [loadingSimilar, setLoadingSimilar] = useState(false)
  const [copiedSuggestion, setCopiedSuggestion] = useState(false)
  const [aiPanelTab, setAiPanelTab] = useState('suggest') // 'suggest' | 'summary' | 'similar'

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

  // WebSocket Connection Lifecycle
  useEffect(() => {
    if (!token || !id) return

    let isSubscribed = true

    // Close any previous socket if id changed or existing socket is open
    if (wsRef.current) {
      if (
        wsRef.current.readyState === WebSocket.OPEN ||
        wsRef.current.readyState === WebSocket.CONNECTING
      ) {
        console.log('[WS CLIENT] Closing previous WebSocket before opening new connection | ticketId:', id)
        wsRef.current.close()
      }
      wsRef.current = null
      setWsConnected(false)
    }

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = window.location.host // works with Vite proxy and direct dev server
    const wsUrl = `${protocol}//${host}/ws/chat/${id}?token=${token}`
    
    console.log('[WS CLIENT] Connecting | ticketId:', id)
    const socket = new WebSocket(wsUrl)
    wsRef.current = socket

    socket.onopen = () => {
      if (!isSubscribed) {
        socket.close()
        return
      }
      console.log(`[WS CLIENT] OPEN\nticketId=${id}`)
      setWsConnected(true)
    }
    
    socket.onmessage = (event) => {
      if (!isSubscribed) return
      try {
        const data = JSON.parse(event.data)
        if (data.type === 'message') {
          console.log(`[WS CLIENT] MESSAGE event received\nticketId=${id}\nmessageId=${data.id}`)
          console.log('[WS CLIENT] Appending message to state:', data)
          setMessages(prev => {
            const exists = prev.some(m => (m.id && m.id === data.id) || (m.external_message_id && m.external_message_id === data.external_message_id))
            if (exists) {
              console.log('[WS CLIENT] Duplicate message ignored:', data.id || data.external_message_id)
              return prev
            }
            return [...prev, data]
          })
        } else if (data.type === 'ticket_update' || data.type === 'inbox_update') {
          console.log('[WS CLIENT] Invalidating ticket queries due to event:', data.type)
          queryClient.invalidateQueries({ queryKey: ['ticket', id] })
          queryClient.invalidateQueries({ queryKey: ['tickets'] })
        }
      } catch (err) {
        console.error('[WS CLIENT] Error parsing WebSocket message:', err)
      }
    }
    
    socket.onclose = (event) => {
      console.log('[WS CLIENT] CLOSE | code:', event.code, 'reason:', event.reason)
      if (wsRef.current === socket) {
        wsRef.current = null
        setWsConnected(false)
      }
    }

    socket.onerror = (event) => {
      console.error('[WS CLIENT] ERROR', event)
    }
    
    return () => {
      isSubscribed = false
      if (wsRef.current === socket) {
        console.log('[WS CLIENT] Cleanup closing socket for ticketId:', id)
        socket.close()
        wsRef.current = null
        setWsConnected(false)
      }
    }
  }, [id, token, queryClient])

  const sendMessage = (e) => {
    e.preventDefault()
    if (!inputText.trim()) return
    const socket = wsRef.current
    if (!socket || socket.readyState !== WebSocket.OPEN) {
      console.warn('[WS CLIENT] Cannot send message, socket is not connected')
      return
    }
    
    socket.send(JSON.stringify({ type: 'message', body: inputText }))
    setInputText('')
  }

  const updateMutation = useMutation({
    mutationFn: (data) => ticketsApi.update(id, data),
    onSuccess: (res) => {
      queryClient.setQueryData(['ticket', id], res.data)
    }
  })

  // Phase 6 handlers
  const handleSuggestReply = async () => {
    setLoadingSuggest(true)
    setAiSuggestion(null)
    try {
      const res = await ticketsApi.suggestReply(id)
      setAiSuggestion(res.data.suggestion)
    } catch (e) {
      setAiSuggestion('Unable to generate suggestion right now.')
    } finally {
      setLoadingSuggest(false)
    }
  }

  const handleSummarize = async () => {
    setLoadingSummary(true)
    setAiSummary(null)
    try {
      const res = await ticketsApi.summarize(id)
      setAiSummary(res.data.summary)
    } catch (e) {
      setAiSummary('Unable to generate summary right now.')
    } finally {
      setLoadingSummary(false)
    }
  }

  const handleSimilar = async () => {
    setLoadingSimilar(true)
    setSimilarTickets([])
    try {
      const res = await ticketsApi.getSimilar(id)
      setSimilarTickets(res.data)
    } catch (e) {
      setSimilarTickets([])
    } finally {
      setLoadingSimilar(false)
    }
  }

  const handleCopySuggestion = () => {
    if (!aiSuggestion) return
    navigator.clipboard.writeText(aiSuggestion)
    setInputText(aiSuggestion)
    setCopiedSuggestion(true)
    setTimeout(() => setCopiedSuggestion(false), 2000)
  }

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
              <p className="text-xs text-[#9598B0] flex items-center gap-2 mt-0.5">
                <span className="font-bold text-slate-800 bg-slate-100 px-1.5 py-0.5 rounded border border-slate-200 font-mono text-[11px]">ID: #{ticket.id}</span>
                <span>•</span>
                <span className="font-mono text-indigo-600 font-semibold">{ticket.ref}</span>
                <span>•</span>
                <span>{formatDateTime(ticket.created_at)}</span>
              </p>
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
                      {formatTime(msg.created_at)}
                    </span>
                  </div>
                  {(() => {
                    const match = msg.body?.match(/📎\s*\[Attachment:\s*([^\]]+)\]\(([^)]+)\)/)
                    if (match) {
                      const filename = match[1]
                      const url = match[2]
                      const isImage = /\.(jpg|jpeg|png|gif|webp|svg)/i.test(filename) || /\.(jpg|jpeg|png|gif|webp|svg)/i.test(url)
                      const textWithoutLink = msg.body.replace(match[0], '').trim()

                      return (
                        <div className="space-y-2">
                          {textWithoutLink && <p className="text-sm whitespace-pre-wrap leading-relaxed">{textWithoutLink}</p>}
                          {isImage ? (
                            <a href={url} target="_blank" rel="noopener noreferrer" className="block mt-1 overflow-hidden rounded-xl border border-white/20 shadow-sm max-w-xs hover:opacity-95 transition-opacity">
                              <img src={url} alt={filename} className="w-full h-auto max-h-48 object-cover rounded-xl" />
                            </a>
                          ) : (
                            <a href={url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 px-3 py-1.5 bg-black/10 hover:bg-black/20 rounded-xl text-xs font-bold transition-colors underline">
                              📎 {filename}
                            </a>
                          )}
                        </div>
                      )
                    }
                    if (msg.body_html) {
                      return (
                        <div
                          className="text-sm leading-relaxed prose prose-sm max-w-none dark:prose-invert"
                          dangerouslySetInnerHTML={{ __html: msg.body_html }}
                        />
                      )
                    }
                    return <p className="text-sm whitespace-pre-wrap leading-relaxed">{msg.body}</p>
                  })()}
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

              <button
                type="button"
                onClick={async () => {
                  const input = document.createElement('input')
                  input.type = 'file'
                  input.onchange = async (e) => {
                    const file = e.target.files[0]
                    if (!file) return
                    const formData = new FormData()
                    formData.append('file', file)
                    try {
                      const res = await client.post(`/tickets/${id}/upload`, formData, {
                        headers: { 'Content-Type': 'multipart/form-data' }
                      })
                      setInputText(prev => prev + ` 📎 [Attachment: ${res.data.filename}](${res.data.url})`)
                    } catch (err) {
                      console.error('File upload failed:', err?.response?.data || err.message)
                      alert(`Failed to upload file: ${err?.response?.data?.detail || err.message}`)
                    }
                  }
                  input.click()
                }}
                className="p-3 rounded-xl border bg-[#F6F7FC] hover:bg-gray-100 text-[#6C7089] border-[#E5E7F3] transition-colors"
                title="Attach file or screenshot"
              >
                <Paperclip size={18} />
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
                disabled={!inputText.trim() || !wsConnected}
                className="bg-indigo-600 hover:bg-indigo-700 text-white p-3 rounded-xl transition-colors disabled:opacity-50"
              >
                <Send size={20} />
              </button>
            </form>
          )}
        </div>
      </div>

      {/* Right Sidebar */}
      <div className="w-80 bg-white border-l border-[#E5E7F3] flex flex-col overflow-hidden">
        {/* Ticket Details */}
        <div className="p-5 border-b border-[#E5E7F3] space-y-4">
          <h3 className="font-bold text-[#1C1B2E] uppercase text-xs tracking-wider">Ticket Details</h3>

          <div>
            <div className="text-xs text-[#9598B0] mb-1">Category</div>
            <div className="capitalize text-xs bg-indigo-50 text-indigo-700 font-bold inline-block px-2.5 py-1 rounded-lg">{ticket.category}</div>
            {ticket.sentiment && (
              <span className={`ml-2 capitalize text-xs font-bold inline-block px-2.5 py-1 rounded-lg ${
                ticket.sentiment === 'frustrated' || ticket.sentiment === 'negative' ? 'bg-red-50 text-red-600'
                : ticket.sentiment === 'positive' ? 'bg-emerald-50 text-emerald-700'
                : 'bg-gray-100 text-gray-600'
              }`}>{ticket.sentiment}</span>
            )}
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
              <div className="text-xs text-[#9598B0] mb-2">Status</div>
              <div className="flex flex-wrap gap-2">
                <button onClick={() => updateMutation.mutate({ status: 'open' })} className={`px-3 py-1.5 rounded-lg text-xs font-bold border transition-colors ${ticket.status === 'open' ? 'bg-indigo-50 border-indigo-200 text-indigo-700' : 'bg-white border-[#E5E7F3] text-[#6C7089] hover:bg-gray-50'}`}>Open</button>
                <button onClick={() => updateMutation.mutate({ status: 'waiting' })} className={`flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-bold border transition-colors ${ticket.status === 'waiting' ? 'bg-orange-50 border-orange-200 text-orange-700' : 'bg-white border-[#E5E7F3] text-[#6C7089] hover:bg-gray-50'}`}><Clock size={12} /> Snooze</button>
                <button onClick={() => updateMutation.mutate({ status: 'resolved' })} className={`flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-bold border transition-colors ${ticket.status === 'resolved' ? 'bg-green-50 border-green-200 text-green-700' : 'bg-white border-[#E5E7F3] text-[#6C7089] hover:bg-gray-50'}`}>✓ Resolve</button>
              </div>
            </div>
          )}
        </div>

        {/* Phase 6 — AI Agent Panel (agents/managers only) */}
        {(role === 'agent' || role === 'manager' || role === 'admin') && (
          <div className="flex-1 flex flex-col overflow-hidden">
            {/* Tab Switcher */}
            <div className="flex border-b border-[#E5E7F3] bg-[#F8FAFC]">
              {[
                { id: 'suggest', icon: Sparkles, label: 'Reply' },
                { id: 'summary', icon: FileText, label: 'Summary' },
                { id: 'similar', icon: Link2, label: 'Similar' },
              ].map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setAiPanelTab(tab.id)}
                  className={`flex-1 flex items-center justify-center gap-1.5 py-3 text-[10px] font-bold uppercase tracking-wide transition-colors ${
                    aiPanelTab === tab.id
                      ? 'text-indigo-600 border-b-2 border-indigo-500 bg-white'
                      : 'text-[#9598B0] hover:text-[#6C7089]'
                  }`}
                >
                  <tab.icon size={13} /> {tab.label}
                </button>
              ))}
            </div>

            {/* Tab Content */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3">

              {/* ── Suggest Reply Tab ── */}
              {aiPanelTab === 'suggest' && (
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <div className="p-1.5 bg-indigo-100 rounded-lg"><Sparkles size={14} className="text-indigo-600" /></div>
                    <div>
                      <div className="text-xs font-bold text-[#1C1B2E]">AI Suggested Reply</div>
                      <div className="text-[10px] text-[#9598B0]">Drafts a reply based on the conversation</div>
                    </div>
                  </div>

                  <button
                    onClick={handleSuggestReply}
                    disabled={loadingSuggest}
                    className="w-full flex items-center justify-center gap-2 py-2.5 px-3 bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white text-xs font-bold rounded-xl transition-all shadow-sm disabled:opacity-60"
                  >
                    {loadingSuggest ? (
                      <><RefreshCw size={13} className="animate-spin" /> Generating...</>
                    ) : (
                      <><Sparkles size={13} /> Generate AI Reply</>  
                    )}
                  </button>

                  {aiSuggestion && (
                    <div className="bg-indigo-50 border border-indigo-200 rounded-xl p-3 space-y-2">
                      <p className="text-xs text-[#1C1B2E] leading-relaxed whitespace-pre-wrap">{aiSuggestion}</p>
                      <div className="flex gap-2 pt-1">
                        <button
                          onClick={handleCopySuggestion}
                          className={`flex-1 flex items-center justify-center gap-1.5 py-2 text-[10px] font-bold rounded-lg transition-all ${
                            copiedSuggestion
                              ? 'bg-emerald-500 text-white'
                              : 'bg-white border border-indigo-200 text-indigo-700 hover:bg-indigo-100'
                          }`}
                        >
                          {copiedSuggestion ? <><CheckCheck size={12} /> Copied to composer!</> : <><Copy size={12} /> Use this reply</>}
                        </button>
                      </div>
                    </div>
                  )}

                  <div className="bg-amber-50 border border-amber-100 rounded-xl p-3">
                    <div className="flex items-center gap-1.5 mb-1">
                      <Lightbulb size={12} className="text-amber-500" />
                      <span className="text-[10px] font-bold text-amber-700">Pro Tip</span>
                    </div>
                    <p className="text-[10px] text-amber-700 leading-relaxed">Click <strong>"Use this reply"</strong> to paste the AI suggestion directly into the message composer. You can edit it before sending.</p>
                  </div>
                </div>
              )}

              {/* ── Summary Tab ── */}
              {aiPanelTab === 'summary' && (
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <div className="p-1.5 bg-blue-100 rounded-lg"><FileText size={14} className="text-blue-600" /></div>
                    <div>
                      <div className="text-xs font-bold text-[#1C1B2E]">AI Ticket Summary</div>
                      <div className="text-[10px] text-[#9598B0]">Condenses the full conversation</div>
                    </div>
                  </div>

                  <button
                    onClick={handleSummarize}
                    disabled={loadingSummary}
                    className="w-full flex items-center justify-center gap-2 py-2.5 px-3 bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white text-xs font-bold rounded-xl transition-all shadow-sm disabled:opacity-60"
                  >
                    {loadingSummary ? (
                      <><RefreshCw size={13} className="animate-spin" /> Summarizing...</>
                    ) : (
                      <><FileText size={13} /> Generate Summary</>
                    )}
                  </button>

                  {aiSummary && (
                    <div className="bg-blue-50 border border-blue-200 rounded-xl p-3">
                      <p className="text-xs text-[#1C1B2E] leading-relaxed">{aiSummary}</p>
                    </div>
                  )}

                  {!aiSummary && !loadingSummary && (
                    <div className="text-center py-6 text-[#9598B0] text-[10px]">
                      <Bot size={28} className="mx-auto mb-2 opacity-30" />
                      Click the button above to generate an AI summary of this ticket.
                    </div>
                  )}
                </div>
              )}

              {/* ── Similar Tickets Tab ── */}
              {aiPanelTab === 'similar' && (
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <div className="p-1.5 bg-emerald-100 rounded-lg"><Link2 size={14} className="text-emerald-600" /></div>
                    <div>
                      <div className="text-xs font-bold text-[#1C1B2E]">Similar Past Cases</div>
                      <div className="text-[10px] text-[#9598B0]">Find resolved tickets with similar issues</div>
                    </div>
                  </div>

                  <button
                    onClick={handleSimilar}
                    disabled={loadingSimilar}
                    className="w-full flex items-center justify-center gap-2 py-2.5 px-3 bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600 text-white text-xs font-bold rounded-xl transition-all shadow-sm disabled:opacity-60"
                  >
                    {loadingSimilar ? (
                      <><RefreshCw size={13} className="animate-spin" /> Searching...</>
                    ) : (
                      <><Link2 size={13} /> Find Similar Cases</>
                    )}
                  </button>

                  {similarTickets.length > 0 && (
                    <div className="space-y-2">
                      {similarTickets.map(t => (
                        <div key={t.id} className="bg-emerald-50 border border-emerald-100 rounded-xl p-3 space-y-1.5">
                          <div className="flex items-center justify-between">
                            <span className="text-[10px] font-bold text-emerald-700 font-mono">{t.ref}</span>
                            <span className="text-[10px] bg-emerald-200 text-emerald-800 px-2 py-0.5 rounded-full font-bold">{Math.round(t.similarity * 100)}% match</span>
                          </div>
                          <p className="text-xs font-semibold text-[#1C1B2E] line-clamp-2">{t.subject}</p>
                          <div className="flex items-center gap-1.5">
                            <span className="text-[9px] bg-gray-100 text-gray-600 px-2 py-0.5 rounded-md font-semibold uppercase">{t.category}</span>
                            <span className="text-[9px] bg-green-100 text-green-700 px-2 py-0.5 rounded-md font-semibold capitalize">✓ {t.status}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {similarTickets.length === 0 && !loadingSimilar && (
                    <div className="text-center py-6 text-[#9598B0] text-[10px]">
                      <Link2 size={28} className="mx-auto mb-2 opacity-30" />
                      Click above to search for similar resolved cases that may contain useful solutions.
                    </div>
                  )}
                </div>
              )}

            </div>
          </div>
        )}
      </div>
    </div>
  )
}
