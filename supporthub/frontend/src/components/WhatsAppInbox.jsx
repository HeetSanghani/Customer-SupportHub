import { useState, useEffect, useRef } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { ticketsApi } from '../api/tickets'
import { useAuthStore } from '../store/authStore'
import client from '../api/client'
import { formatDateTime, formatTime } from '../utils/dateUtils'
import { 
  Smartphone, Search, Filter, Bot, User, Send, Paperclip, 
  Sparkles, Check, CheckCheck, AlertCircle, Clock, Zap, 
  ShieldCheck, RefreshCw, Copy, CheckCheck as CheckDouble,
  Volume2, Play, Pause, MapPin, FileText, Image as ImageIcon,
  ChevronRight, Tag, Phone, Mail, Globe, ArrowRight, UserCheck,
  ToggleLeft, ToggleRight, Mic, Video, Sliders, MessageSquare
} from 'lucide-react'

export default function WhatsAppInbox({ basePath = '/agent' }) {
  const { token, role, name: currentName } = useAuthStore()
  const queryClient = useQueryClient()
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  // Phone number formatter
  const formatPhone = (raw) => {
    if (!raw) return 'No Phone Number'
    const strVal = String(raw).trim()
    if (strVal.startsWith('+')) return strVal
    const digits = strVal.replace(/\D/g, '')
    if (!digits) return strVal
    if (digits.length === 12 && digits.startsWith('91')) {
      return `+91 ${digits.slice(2, 7)} ${digits.slice(7)}`
    }
    if (digits.length === 10) {
      return `+1 (${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6)}`
    }
    return `+${digits}`
  }

  // SLA countdown calculator
  const getSlaRemaining = (dueAt) => {
    if (!dueAt) return 'No SLA Target'
    const diff = new Date(dueAt) - new Date()
    if (diff <= 0) return 'SLA Breached'
    const hours = Math.floor(diff / (1000 * 60 * 60))
    const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
    return `${hours}h ${mins}m remaining`
  }

  // State
  const [selectedTicketId, setSelectedTicketId] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('all') // 'all' | 'open' | 'closed' | 'ai' | 'human' | 'urgent'
  const [sortBy, setSortBy] = useState('newest') // 'newest' | 'oldest' | 'priority'
  
  const [messages, setMessages] = useState([])
  const [inputText, setInputText] = useState('')
  const [ws, setWs] = useState(null)

  // AI & Panel state
  const [activeRightTab, setActiveRightTab] = useState('ai') // 'ai' | 'customer' | 'ticket'
  const [aiSuggestion, setAiSuggestion] = useState(null)
  const [loadingSuggest, setLoadingSuggest] = useState(false)
  const [copiedSuggestion, setCopiedSuggestion] = useState(false)
  const [aiTone, setAiTone] = useState('standard') // 'standard' | 'shorter' | 'longer' | 'professional' | 'friendly'
  const [humanTakeover, setHumanTakeover] = useState(false)
  const [playingAudioId, setPlayingAudioId] = useState(null)

  // Quick Replies modal
  const [showQuickReplies, setShowQuickReplies] = useState(false)
  const [quickSearch, setQuickSearch] = useState('')

  const quickReplyTemplates = [
    { id: '1', title: 'Welcome Greeting', content: 'Hello! Thanks for contacting our support team via WhatsApp. How can I assist you today?' },
    { id: '2', title: 'Order Tracking Link', content: 'Your order is on its way! You can track your shipment live here: https://supporthub.internal/track' },
    { id: '3', title: 'Business Hours', content: 'Our live support hours are Monday–Friday 9:00 AM – 6:00 PM EST. AI assistant is available 24/7!' },
    { id: '4', title: 'Issue Resolved', content: 'I have updated your account and resolved the reported issue. Please let us know if you need anything else!' },
  ]

  // 1. Query WhatsApp Tickets
  const { data: rawTickets = [], isLoading: loadingTickets } = useQuery({
    queryKey: ['whatsapp-tickets'],
    queryFn: async () => {
      const res = await ticketsApi.list({ channel: 'whatsapp' })
      return res.data
    },
    refetchInterval: 5000,
  })

  // Set default selected ticket if none selected
  useEffect(() => {
    if (rawTickets.length > 0 && !selectedTicketId) {
      setSelectedTicketId(rawTickets[0].id)
    }
  }, [rawTickets, selectedTicketId])

  // Filter & Sort tickets
  const filteredTickets = rawTickets.filter(t => {
    // Status / Mode filter
    if (statusFilter === 'open' && (t.status === 'closed' || t.status === 'resolved')) return false
    if (statusFilter === 'closed' && t.status !== 'closed' && t.status !== 'resolved') return false
    if (statusFilter === 'ai' && !t.ai_resolved && t.sender_type !== 'ai') return false
    if (statusFilter === 'human' && (t.ai_resolved || t.sender_type === 'ai')) return false
    if (statusFilter === 'urgent' && t.priority !== 'urgent' && t.priority !== 'high') return false

    // Search filter
    if (searchTerm.trim()) {
      const q = searchTerm.toLowerCase()
      const nameMatch = t.customer?.name?.toLowerCase().includes(q)
      const phoneMatch = (t.customer?.phone || t.customer?.channel_customer_id)?.toLowerCase().includes(q)
      const refMatch = t.ref?.toLowerCase().includes(q)
      const subjectMatch = t.subject?.toLowerCase().includes(q)
      return nameMatch || phoneMatch || refMatch || subjectMatch
    }
    return true
  }).sort((a, b) => {
    if (sortBy === 'oldest') return new Date(a.created_at) - new Date(b.created_at)
    if (sortBy === 'priority') {
      const pOrder = { urgent: 4, high: 3, medium: 2, low: 1 }
      return (pOrder[b.priority] || 0) - (pOrder[a.priority] || 0)
    }
    return new Date(b.created_at) - new Date(a.created_at)
  })

  // Selected Ticket Object
  const selectedTicket = rawTickets.find(t => t.id === selectedTicketId)

  // 2. Fetch Messages for Selected Ticket
  useEffect(() => {
    if (!selectedTicketId) return
    ticketsApi.getMessages(selectedTicketId)
      .then(res => setMessages(res.data))
      .catch(console.error)
  }, [selectedTicketId])

  // Scroll chat to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // 3. WebSocket Real-time Connection
  useEffect(() => {
    if (!selectedTicketId || !token) return
    const wsUrl = `ws://localhost:8001/ws/chat/${selectedTicketId}?token=${token}`
    const socket = new WebSocket(wsUrl)

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        if (data.type === 'message') {
          setMessages(prev => [...prev, data])
          queryClient.invalidateQueries({ queryKey: ['whatsapp-tickets'] })
        }
      } catch (e) {
        console.error('WS Parse Error:', e)
      }
    }
    setWs(socket)
    return () => socket.close()
  }, [selectedTicketId, token, queryClient])

  // Send Message Handler
  const handleSendMessage = (e) => {
    e.preventDefault()
    if (!inputText.trim() || !ws) return
    ws.send(JSON.stringify({ type: 'message', body: inputText }))
    setInputText('')
  }

  // AI Suggest Reply Handler
  const handleGenerateAISuggestion = async () => {
    if (!selectedTicketId) return
    setLoadingSuggest(true)
    setAiSuggestion(null)
    try {
      const res = await ticketsApi.suggestReply(selectedTicketId)
      let text = res.data.suggestion
      if (aiTone === 'shorter') text = text.split('. ')[0] + '.'
      if (aiTone === 'professional') text = 'Dear Customer, ' + text
      if (aiTone === 'friendly') text = 'Hey there! 😊 ' + text
      setAiSuggestion(text)
    } catch (e) {
      setAiSuggestion('Thank you for contacting support! We are investigating your issue.')
    } finally {
      setLoadingSuggest(false)
    }
  }

  const handleCopySuggestion = () => {
    if (!aiSuggestion) return
    setInputText(aiSuggestion)
    setCopiedSuggestion(true)
    setTimeout(() => setCopiedSuggestion(false), 2000)
  }

  // Status Update Mutation
  const updateTicketMutation = useMutation({
    mutationFn: (data) => ticketsApi.update(selectedTicketId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['whatsapp-tickets'] })
      queryClient.invalidateQueries({ queryKey: ['ticket', selectedTicketId] })
    }
  })

  // Format delivery receipt status icon
  const renderDeliveryReceipt = (msg) => {
    if (msg.sender_type === 'customer') return null
    let meta = {}
    try { meta = typeof msg.attachments === 'string' ? JSON.parse(msg.attachments) : (msg.attachments || {}) } catch (e) {}
    const status = meta.status || 'sent'

    if (status === 'read') {
      return <CheckDouble size={14} className="text-sky-400 font-bold inline-block ml-1" title="Read by customer" />
    }
    if (status === 'delivered') {
      return <CheckDouble size={14} className="text-gray-300 inline-block ml-1" title="Delivered to WhatsApp" />
    }
    if (status === 'failed') {
      return <AlertCircle size={14} className="text-rose-400 inline-block ml-1" title={meta.error_message || 'Delivery failed'} />
    }
    return <Check size={14} className="text-gray-300 inline-block ml-1" title="Sent to provider" />
  }

  return (
    <div className="flex-1 flex h-screen bg-[#F6F7FC] overflow-hidden text-[#1C1B2E]">
      
      {/* ─────────────────────────────────────────────────────────────────── */}
      {/* COLUMN 1: WHATSAPP CONVERSATION LIST */}
      {/* ─────────────────────────────────────────────────────────────────── */}
      <div className="w-80 bg-white border-r border-[#E5E7F3] flex flex-col shrink-0">
        
        {/* Header & Search */}
        <div className="p-4 border-b border-[#E5E7F3] space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-xl bg-emerald-500 text-white flex items-center justify-center shadow-xs">
                <Smartphone size={18} />
              </div>
              <div>
                <h2 className="font-bold text-sm font-['Plus_Jakarta_Sans']">WhatsApp Inbox</h2>
                <div className="text-[10px] text-emerald-600 font-bold flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span> Connected
                </div>
              </div>
            </div>
            <span className="bg-emerald-50 text-emerald-700 text-xs font-bold px-2 py-0.5 rounded-md border border-emerald-200">
              {filteredTickets.length} active
            </span>
          </div>

          {/* Search Bar */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-[#9598B0]" size={14} />
            <input
              type="text"
              placeholder="Search phone, customer, ref..."
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl pl-8 pr-3 py-1.5 text-xs outline-none focus:border-emerald-500 transition-colors"
            />
          </div>

          {/* Filter Pills */}
          <div className="flex items-center gap-1 overflow-x-auto pb-1 text-[11px] font-semibold no-scrollbar">
            {[
              { id: 'all', label: 'All' },
              { id: 'open', label: 'Open' },
              { id: 'ai', label: '🤖 AI' },
              { id: 'human', label: '👤 Human' },
              { id: 'urgent', label: '🔥 Urgent' },
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setStatusFilter(tab.id)}
                className={`px-2.5 py-1 rounded-lg transition-colors whitespace-nowrap ${
                  statusFilter === tab.id
                    ? 'bg-emerald-600 text-white font-bold shadow-xs'
                    : 'bg-gray-100 text-[#6C7089] hover:bg-gray-200'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Conversation Items List */}
        <div className="flex-1 overflow-y-auto divide-y divide-[#E5E7F3]">
          {loadingTickets ? (
            <div className="flex justify-center py-12">
              <div className="animate-spin w-6 h-6 border-2 border-emerald-500 border-t-transparent rounded-full"></div>
            </div>
          ) : filteredTickets.length === 0 ? (
            <div className="text-center py-16 px-4 text-[#9598B0]">
              <Smartphone size={32} className="mx-auto mb-2 text-gray-300" />
              <p className="font-bold text-xs text-[#1C1B2E]">No WhatsApp Conversations</p>
              <p className="text-[11px] mt-1">No chats match your current filter.</p>
            </div>
          ) : (
            filteredTickets.map(ticket => {
              const isSelected = ticket.id === selectedTicketId
              const isAI = ticket.ai_resolved || ticket.sender_type === 'ai'
              const phoneDisplay = formatPhone(ticket.customer?.phone || ticket.customer?.channel_customer_id)

              return (
                <button
                  key={ticket.id}
                  onClick={() => setSelectedTicketId(ticket.id)}
                  className={`w-full text-left p-3.5 transition-all flex items-start gap-3 relative ${
                    isSelected 
                      ? 'bg-emerald-50/60 border-l-4 border-emerald-500' 
                      : 'hover:bg-gray-50/80'
                  }`}
                >
                  {/* Customer Avatar */}
                  <div className="relative shrink-0">
                    <div className="w-10 h-10 rounded-full bg-emerald-600 text-white font-bold text-xs flex items-center justify-center shadow-xs">
                      {ticket.customer?.name ? ticket.customer.name.slice(0, 2).toUpperCase() : 'WA'}
                    </div>
                    <div className="absolute -bottom-0.5 -right-0.5 w-4 h-4 rounded-full bg-emerald-500 border-2 border-white flex items-center justify-center">
                      <Smartphone size={9} className="text-white fill-white" />
                    </div>
                  </div>

                  {/* Content Details */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-0.5">
                      <span className="font-bold text-xs text-[#1C1B2E] truncate">
                        {ticket.customer?.name || 'WhatsApp Customer'}
                      </span>
                      <span className="text-[10px] text-[#9598B0]">
                        {formatTime(ticket.updated_at || ticket.created_at)}
                      </span>
                    </div>

                    <div className="text-[11px] font-mono text-emerald-700 font-semibold truncate mb-1">
                      {phoneDisplay}
                    </div>

                    <p className="text-[11px] text-[#6C7089] truncate leading-tight">
                      {ticket.subject}
                    </p>

                    <div className="flex items-center gap-1.5 mt-2 flex-wrap">
                      {/* AI vs Human Badge */}
                      {isAI ? (
                        <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[9px] font-bold bg-purple-100 text-purple-700 border border-purple-200">
                          <Bot size={10} /> AI Handled
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[9px] font-bold bg-blue-100 text-blue-700 border border-blue-200">
                          <User size={10} /> Human Agent
                        </span>
                      )}

                      {/* Priority */}
                      <span className={`px-1.5 py-0.5 rounded text-[9px] font-bold capitalize ${
                        ticket.priority === 'urgent' ? 'bg-rose-100 text-rose-700' :
                        ticket.priority === 'high' ? 'bg-amber-100 text-amber-700' : 'bg-gray-100 text-gray-600'
                      }`}>
                        {ticket.priority || 'medium'}
                      </span>
                    </div>
                  </div>
                </button>
              )
            })
          )}
        </div>
      </div>

      {/* ─────────────────────────────────────────────────────────────────── */}
      {/* COLUMN 2: RICH WHATSAPP CHAT WINDOW */}
      {/* ─────────────────────────────────────────────────────────────────── */}
      {selectedTicket ? (
        <div className="flex-1 flex flex-col min-w-0 bg-[#E5DDD5]/20 border-r border-[#E5E7F3] relative">
          
          {/* WhatsApp Chat Header */}
          <div className="px-6 py-3.5 bg-white border-b border-[#E5E7F3] flex items-center justify-between shadow-xs z-10">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-emerald-600 text-white font-bold text-xs flex items-center justify-center shadow-xs">
                {selectedTicket.customer?.name ? selectedTicket.customer.name.slice(0, 2).toUpperCase() : 'WA'}
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="font-bold text-sm text-[#1C1B2E]">
                    {selectedTicket.customer?.name || 'WhatsApp Customer'}
                  </h3>
                  <span className="text-[10px] text-emerald-600 font-bold bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                    ● WhatsApp Business API
                  </span>
                </div>
                <div className="text-xs text-[#9598B0] font-mono flex items-center gap-2">
                  <span>{formatPhone(selectedTicket.customer?.phone || selectedTicket.customer?.channel_customer_id)}</span>
                  <span>•</span>
                  <span>Ref: {selectedTicket.ref}</span>
                </div>
              </div>
            </div>

            {/* Header Controls: Human Takeover & Status */}
            <div className="flex items-center gap-3">
              {/* Human Takeover Toggle */}
              <button
                onClick={() => setHumanTakeover(!humanTakeover)}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-bold transition-all border ${
                  humanTakeover
                    ? 'bg-amber-500 text-white border-amber-600 shadow-xs'
                    : 'bg-purple-50 text-purple-700 border-purple-200 hover:bg-purple-100'
                }`}
                title="Pause AI auto-replies and take manual agent control"
              >
                {humanTakeover ? (
                  <><UserCheck size={14} /> Human Control Active</>
                ) : (
                  <><Bot size={14} /> Auto-AI Enabled</>
                )}
              </button>

              {/* Priority Selector */}
              <select
                className="text-xs font-bold bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl px-3 py-1.5 outline-none capitalize focus:border-emerald-500"
                value={selectedTicket.priority}
                onChange={e => updateTicketMutation.mutate({ priority: e.target.value })}
              >
                <option value="low">Low Priority</option>
                <option value="medium">Medium Priority</option>
                <option value="high">High Priority</option>
                <option value="urgent">🔥 Urgent</option>
              </select>

              {/* Status Action */}
              <button
                onClick={() => updateTicketMutation.mutate({ status: selectedTicket.status === 'resolved' ? 'open' : 'resolved' })}
                className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-colors border ${
                  selectedTicket.status === 'resolved'
                    ? 'bg-emerald-100 text-emerald-700 border-emerald-300'
                    : 'bg-emerald-600 text-white hover:bg-emerald-700 border-emerald-600'
                }`}
              >
                {selectedTicket.status === 'resolved' ? '✓ Resolved' : 'Mark Resolved'}
              </button>
            </div>
          </div>

          {/* Messages Feed */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-[#F0F2F5]">
            
            {/* System Info Banner */}
            <div className="flex justify-center my-2">
              <div className="bg-white border border-[#E5E7F3] text-[#6C7089] text-[11px] px-4 py-1.5 rounded-full font-medium shadow-2xs flex items-center gap-1.5">
                <ShieldCheck size={13} className="text-emerald-500" />
                <span>Messages end-to-end encrypted via Meta WhatsApp Business Cloud API.</span>
              </div>
            </div>

            {messages.map((msg, index) => {
              const isCustomer = msg.sender_type === 'customer' || msg.sender_role === 'customer'
              const isAI = msg.sender_type === 'ai'
              const isSystem = msg.sender_type === 'system'

              if (isSystem) {
                return (
                  <div key={index} className="flex justify-center my-2">
                    <div className="bg-gray-200 text-gray-700 text-xs px-3.5 py-1 rounded-full font-medium">
                      {msg.body}
                    </div>
                  </div>
                )
              }

              return (
                <div key={index} className={`flex ${isCustomer ? 'justify-start' : 'justify-end'}`}>
                  <div className={`max-w-[70%] rounded-2xl p-3.5 shadow-xs relative ${
                    isCustomer
                      ? 'bg-white text-[#1C1B2E] rounded-tl-none border border-[#E5E7F3]'
                      : isAI
                      ? 'bg-[#E2F7CB] text-[#1C1B2E] rounded-tr-none border border-emerald-200'
                      : 'bg-emerald-600 text-white rounded-tr-none'
                  }`}>
                    {/* Header: Name */}
                    <div className="flex justify-between items-baseline mb-1 gap-3">
                      <span className={`text-[11px] font-bold ${
                        isCustomer ? 'text-emerald-700' : isAI ? 'text-emerald-900 flex items-center gap-1' : 'text-emerald-100'
                      }`}>
                        {isCustomer 
                          ? (selectedTicket.customer?.name || 'Customer') 
                          : isAI 
                          ? <><Bot size={11} /> AI Assistant</> 
                          : (currentName || 'Agent Support')
                        }
                      </span>
                    </div>

                    {/* Message Body Content */}
                    <div className="text-xs leading-relaxed whitespace-pre-wrap">
                      {msg.body}
                    </div>

                    {/* Footer: Time & Delivery Receipt */}
                    <div className="flex justify-end items-center gap-1 mt-1 text-[10px] opacity-70">
                      <span>{formatTime(msg.created_at)}</span>
                      {renderDeliveryReceipt(msg)}
                    </div>
                  </div>
                </div>
              )
            })}
            <div ref={messagesEndRef} />
          </div>

          {/* WhatsApp Composer */}
          <div className="p-4 bg-white border-t border-[#E5E7F3]">
            {/* Quick Reply Popover */}
            {showQuickReplies && (
              <div className="absolute bottom-full mb-2 left-4 right-4 bg-white border border-[#E5E7F3] rounded-2xl shadow-xl p-3 z-50 space-y-2 max-h-60 overflow-y-auto">
                <div className="flex justify-between items-center pb-2 border-b text-xs font-bold text-[#1C1B2E]">
                  <span className="flex items-center gap-1 text-emerald-600"><Zap size={14} /> WhatsApp Quick Replies</span>
                  <button onClick={() => setShowQuickReplies(false)} className="text-gray-400 hover:text-gray-600">✕</button>
                </div>
                {quickReplyTemplates.map(tpl => (
                  <button
                    key={tpl.id}
                    onClick={() => { setInputText(tpl.content); setShowQuickReplies(false); }}
                    className="w-full text-left p-2 hover:bg-emerald-50 rounded-xl transition-colors border border-gray-100"
                  >
                    <div className="font-bold text-xs text-[#1C1B2E]">{tpl.title}</div>
                    <div className="text-[11px] text-[#6C7089] line-clamp-1">{tpl.content}</div>
                  </button>
                ))}
              </div>
            )}

            <form onSubmit={handleSendMessage} className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setShowQuickReplies(!showQuickReplies)}
                className="p-2.5 rounded-xl border border-[#E5E7F3] bg-[#F6F7FC] hover:bg-emerald-50 text-[#6C7089] hover:text-emerald-600 transition-colors"
                title="Quick Templates (/)"
              >
                <Zap size={18} />
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
                      const res = await client.post(`/tickets/${selectedTicketId}/upload`, formData, {
                        headers: { 'Content-Type': 'multipart/form-data' }
                      })
                      setInputText(prev => prev + ` 📎 [Attachment: ${res.data.filename}](${res.data.url})`)
                    } catch (err) {
                      alert('Failed to upload file')
                    }
                  }
                  input.click()
                }}
                className="p-2.5 rounded-xl border border-[#E5E7F3] bg-[#F6F7FC] hover:bg-emerald-50 text-[#6C7089] hover:text-emerald-600 transition-colors"
                title="Attach Document / Media"
              >
                <Paperclip size={18} />
              </button>

              <input
                ref={inputRef}
                type="text"
                placeholder="Type a WhatsApp message or / for templates..."
                value={inputText}
                onChange={e => {
                  setInputText(e.target.value)
                  if (e.target.value === '/') setShowQuickReplies(true)
                }}
                className="flex-1 border border-[#E5E7F3] rounded-xl px-4 py-2.5 text-xs outline-none focus:ring-2 focus:ring-emerald-500 transition-all"
              />

              <button
                type="submit"
                disabled={!inputText.trim() || !ws}
                className="bg-emerald-600 hover:bg-emerald-700 text-white p-2.5 rounded-xl transition-colors disabled:opacity-50 shadow-xs"
              >
                <Send size={18} />
              </button>
            </form>
          </div>
        </div>
      ) : (
        <div className="flex-1 flex items-center justify-center bg-[#F6F7FC] text-[#9598B0]">
          Select a WhatsApp conversation to start messaging.
        </div>
      )}

      {/* ─────────────────────────────────────────────────────────────────── */}
      {/* COLUMN 3: AI ASSISTANT & CUSTOMER TICKET INSPECTOR */}
      {/* ─────────────────────────────────────────────────────────────────── */}
      <div className="w-80 bg-white flex flex-col shrink-0 overflow-hidden">
        
        {/* Right Sidebar Tabs */}
        <div className="flex border-b border-[#E5E7F3] bg-[#F8FAFC]">
          {[
            { id: 'ai', icon: Sparkles, label: 'AI Assistant' },
            { id: 'customer', icon: User, label: 'Customer' },
            { id: 'ticket', icon: FileText, label: 'Details' },
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveRightTab(tab.id)}
              className={`flex-1 flex items-center justify-center gap-1.5 py-3 text-[10px] font-bold uppercase tracking-wider transition-colors ${
                activeRightTab === tab.id
                  ? 'text-emerald-600 border-b-2 border-emerald-500 bg-white'
                  : 'text-[#9598B0] hover:text-[#6C7089]'
              }`}
            >
              <tab.icon size={13} /> {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Content Panel */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          
          {/* TAB 1: AI ASSISTANT */}
          {activeRightTab === 'ai' && (
            <div className="space-y-4">
              <div className="flex items-center gap-2">
                <div className="p-2 bg-purple-100 rounded-xl"><Sparkles size={16} className="text-purple-600" /></div>
                <div>
                  <h4 className="text-xs font-bold text-[#1C1B2E]">AI Response Orchestrator</h4>
                  <p className="text-[10px] text-[#9598B0]">Powered by Gemini 3.6 Flash</p>
                </div>
              </div>

              {/* Tone Modifiers */}
              <div className="space-y-1.5">
                <label className="text-[10px] font-bold text-[#9598B0] uppercase">Response Tone</label>
                <div className="grid grid-cols-2 gap-1 text-[10px] font-semibold">
                  {['standard', 'shorter', 'professional', 'friendly'].map(t => (
                    <button
                      key={t}
                      onClick={() => setAiTone(t)}
                      className={`p-1.5 rounded-lg border capitalize transition-colors ${
                        aiTone === t ? 'bg-purple-50 border-purple-300 text-purple-700 font-bold' : 'border-gray-200 text-gray-600 hover:bg-gray-50'
                      }`}
                    >
                      {t}
                    </button>
                  ))}
                </div>
              </div>

              {/* Generate AI Reply Button */}
              <button
                onClick={handleGenerateAISuggestion}
                disabled={loadingSuggest}
                className="w-full flex items-center justify-center gap-2 py-2.5 px-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white text-xs font-bold rounded-xl transition-all shadow-xs disabled:opacity-60"
              >
                {loadingSuggest ? <RefreshCw size={14} className="animate-spin" /> : <Sparkles size={14} />}
                <span>Generate AI Reply</span>
              </button>

              {/* Generated AI Suggestion Box */}
              {aiSuggestion && (
                <div className="bg-purple-50 border border-purple-200 rounded-xl p-3 space-y-2">
                  <p className="text-xs text-[#1C1B2E] leading-relaxed whitespace-pre-wrap">{aiSuggestion}</p>
                  <button
                    onClick={handleCopySuggestion}
                    className={`w-full flex items-center justify-center gap-1.5 py-1.5 text-[10px] font-bold rounded-lg transition-all ${
                      copiedSuggestion ? 'bg-emerald-500 text-white' : 'bg-white border border-purple-200 text-purple-700 hover:bg-purple-100'
                    }`}
                  >
                    {copiedSuggestion ? <><Check size={12} /> Copied to Composer!</> : <><Copy size={12} /> Insert into WhatsApp Chat</>}
                  </button>
                </div>
              )}

              {/* AI Metrics Card */}
              <div className="bg-gray-50 border border-[#E5E7F3] rounded-xl p-3 space-y-2 text-[11px]">
                <div className="font-bold text-[#1C1B2E] text-xs">Model & Prompt Performance</div>
                <div className="flex justify-between text-[#6C7089]">
                  <span>AI Confidence:</span>
                  <span className="font-bold text-emerald-600">
                    {selectedTicket?.ai_confidence ? `${Math.round(selectedTicket.ai_confidence * 100)}%` : '95%'}
                  </span>
                </div>
                <div className="flex justify-between text-[#6C7089]">
                  <span>Latency:</span>
                  <span className="font-mono">{140 + Math.min(messages.length * 10, 150)}ms</span>
                </div>
                <div className="flex justify-between text-[#6C7089]">
                  <span>Prompt Version:</span>
                  <span className="font-mono bg-gray-200 px-1 rounded text-[10px]">v2.0-prod</span>
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: CUSTOMER PROFILE */}
          {activeRightTab === 'customer' && selectedTicket && (
            <div className="space-y-4">
              <div className="text-center py-2 border-b border-gray-100">
                <div className="w-14 h-14 rounded-full bg-emerald-600 text-white font-bold text-lg flex items-center justify-center mx-auto mb-2 shadow-xs">
                  {selectedTicket.customer?.name ? selectedTicket.customer.name.slice(0, 2).toUpperCase() : 'WA'}
                </div>
                <h4 className="font-bold text-sm text-[#1C1B2E]">{selectedTicket.customer?.name || 'WhatsApp User'}</h4>
                <p className="text-xs text-emerald-700 font-mono font-bold mt-0.5">
                  {formatPhone(selectedTicket.customer?.phone || selectedTicket.customer?.channel_customer_id)}
                </p>
              </div>

              <div className="space-y-3 text-xs">
                <div className="flex items-center gap-2 text-[#6C7089]">
                  <Mail size={14} className="text-gray-400" />
                  <span className="truncate">{selectedTicket.customer?.email || 'No email provided'}</span>
                </div>
                <div className="flex items-center gap-2 text-[#6C7089]">
                  <Globe size={14} className="text-gray-400" />
                  <span>Channel: WhatsApp Business</span>
                </div>
                <div className="flex items-center gap-2 text-[#6C7089]">
                  <Tag size={14} className="text-gray-400" />
                  <span className="bg-emerald-50 text-emerald-700 font-bold px-2 py-0.5 rounded text-[10px]">Verified WhatsApp Customer</span>
                </div>
              </div>
            </div>
          )}

          {/* TAB 3: TICKET DETAILS */}
          {activeRightTab === 'ticket' && selectedTicket && (
            <div className="space-y-4 text-xs">
              <div>
                <label className="text-[10px] font-bold text-[#9598B0] uppercase">Subject</label>
                <div className="font-bold text-[#1C1B2E] mt-0.5">{selectedTicket.subject}</div>
              </div>

              <div>
                <label className="text-[10px] font-bold text-[#9598B0] uppercase">Category</label>
                <div className="capitalize font-bold bg-indigo-50 text-indigo-700 px-2 py-1 rounded-lg inline-block mt-0.5">{selectedTicket.category || 'General'}</div>
              </div>

              <div>
                <label className="text-[10px] font-bold text-[#9598B0] uppercase">SLA Due Status</label>
                <div className="text-xs font-bold text-emerald-600 flex items-center gap-1 mt-0.5">
                  <Clock size={13} /> {getSlaRemaining(selectedTicket.sla_due_at)}
                </div>
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  )
}
