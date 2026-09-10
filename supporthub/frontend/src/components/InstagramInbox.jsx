import { useState, useEffect, useRef } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { ticketsApi } from '../api/tickets'
import { useAuthStore } from '../store/authStore'
import { formatTime, formatSmartTime } from '../utils/dateUtils'
import { adminApi } from '../api/admin'
import {
  Instagram, Search, Bot, User, Send, Paperclip,
  Sparkles, Check, CheckCheck as CheckDouble, AlertCircle, Clock, Zap,
  ShieldCheck, RefreshCw, Copy, FileText,
  UserCheck, Key, X, CheckCircle2, ShieldAlert, Info
} from 'lucide-react'

export default function InstagramInbox({ basePath = '/agent' }) {
  const { token, role, name: currentName } = useAuthStore()
  const isAgent = basePath === '/agent' || (role === 'agent' && basePath !== '/manager' && basePath !== '/admin')
  const queryClient = useQueryClient()
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  // Customer initials helper
  const getInitials = (name) => {
    if (!name) return 'IG'
    const parts = name.trim().split(/\s+/)
    if (parts.length >= 2) {
      return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
    }
    return name.slice(0, 2).toUpperCase()
  }

  // Instagram handle / customer ID formatter
  const formatHandle = (rawId, name) => {
    if (!rawId && !name) return 'Instagram Direct'
    // If rawId is purely numeric (IGSID), show 'Instagram Direct' instead of ugly raw numeric id
    if (rawId && /^\d+$/.test(String(rawId).trim())) {
      return 'Instagram Direct'
    }
    if (rawId && String(rawId).startsWith('@')) return rawId
    if (rawId && !String(rawId).includes('@') && !String(rawId).includes('supporthub.local')) {
      return `@${rawId}`
    }
    return name ? `${name}` : 'Instagram Direct'
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
  const [statusFilter, setStatusFilter] = useState('open') // 'open' (Active) | 'all' | 'closed' | 'urgent'
  const [sortBy, setSortBy] = useState('newest') // 'newest' | 'oldest' | 'priority'

  const [messages, setMessages] = useState([])
  const [inputText, setInputText] = useState('')
  const [ws, setWs] = useState(null)

  // AI & Panel state
  const [showRightPanel, setShowRightPanel] = useState(false) // DEFAULT HIDE
  const [activeRightTab, setActiveRightTab] = useState('ai') // 'ai' | 'info'
  const [aiSuggestion, setAiSuggestion] = useState(null)
  const [loadingSuggest, setLoadingSuggest] = useState(false)
  const [copiedSuggestion, setCopiedSuggestion] = useState(false)
  const [aiTone, setAiTone] = useState('standard') // 'standard' | 'shorter' | 'professional' | 'friendly'
  const [humanTakeover, setHumanTakeover] = useState(false)

  // Quick Replies modal
  // Quick Replies modal
  const [showQuickReplies, setShowQuickReplies] = useState(false)
  const [lockedTicketId, setLockedTicketId] = useState(null)

  // Instagram Token Management & Test Modal State
  const [isTokenModalOpen, setIsTokenModalOpen] = useState(false)
  const [igConfigForm, setIgConfigForm] = useState({
    instagram_access_token: '',
    instagram_account_id: '',
    instagram_verify_token: '',
  })
  const [isTestingIgToken, setIsTestingIgToken] = useState(false)
  const [isSavingIgToken, setIsSavingIgToken] = useState(false)
  const [igTokenTestResult, setIgTokenTestResult] = useState(null)
  const [igTokenSaveResult, setIgTokenSaveResult] = useState(null)

  const openTokenModal = async () => {
    setIsTokenModalOpen(true)
    setIgTokenTestResult(null)
    setIgTokenSaveResult(null)
    try {
      const res = await adminApi.getInstagramConfig()
      setIgConfigForm({
        instagram_access_token: res.data.instagram_access_token || '',
        instagram_account_id: res.data.instagram_account_id || '',
        instagram_verify_token: res.data.instagram_verify_token || '',
      })
    } catch (e) {
      console.error('Failed to fetch Instagram config:', e)
    }
  }

  const handleSaveIgToken = async (e) => {
    e.preventDefault()
    setIsSavingIgToken(true)
    setIgTokenSaveResult(null)
    try {
      const res = await adminApi.updateInstagramConfig(igConfigForm)
      setIgTokenSaveResult({ status: 'success', message: res.data.message })
      queryClient.invalidateQueries({ queryKey: ['admin-channels'] })
    } catch (err) {
      setIgTokenSaveResult({ status: 'error', message: err.response?.data?.detail || 'Failed to update Instagram Access Token.' })
    } finally {
      setIsSavingIgToken(false)
    }
  }

  const handleTestIgToken = async () => {
    setIsTestingIgToken(true)
    setIgTokenTestResult(null)
    try {
      const res = await adminApi.testInstagramConfig(igConfigForm)
      setIgTokenTestResult(res.data)
    } catch (err) {
      setIgTokenTestResult({
        status: 'error',
        connected: false,
        message: err.response?.data?.detail || 'Token testing failed. Please verify Instagram credentials.'
      })
    } finally {
      setIsTestingIgToken(false)
    }
  }

  const quickReplyTemplates = [
    { id: '1', title: 'Welcome Greeting', content: 'Hey there! Thanks for reaching out via Instagram DM. How can we help you today? ✨' },
    { id: '2', title: 'Order Tracking Link', content: 'We found your recent order! You can track real-time delivery and shipping updates here: https://supporthub.internal/track 📦' },
    { id: '3', title: 'Product Inquiries', content: 'Thanks for asking about our products! Check out our catalog and special promotions here: https://supporthub.internal/catalog 🔥' },
    { id: '4', title: 'Issue Resolved', content: "We've resolved your inquiry! Feel free to DM us anytime if you need more assistance. Have a wonderful day! 😊" },
  ]

  // 1. Query Instagram Tickets
  const { data: rawTickets = [], isLoading: loadingTickets } = useQuery({
    queryKey: ['instagram-tickets', isAgent ? 'human-only' : 'all'],
    queryFn: async () => {
      const params = {
        channel: 'instagram',
        ...(isAgent ? { human_only: true } : { all_tickets: true })
      }
      const res = await ticketsApi.list(params)
      return res.data
    },
    refetchInterval: 5000,
  })

  // Filter & Sort tickets
  const filteredTickets = rawTickets.filter(t => {
    // Status / Mode filter
    if (statusFilter === 'open' && (t.status === 'closed' || t.status === 'resolved')) return false
    if (statusFilter === 'closed' && t.status !== 'closed' && t.status !== 'resolved') return false
    if (statusFilter === 'urgent' && t.priority !== 'urgent' && t.priority !== 'high') return false

    // Search filter
    if (searchTerm.trim()) {
      const q = searchTerm.toLowerCase()
      const nameMatch = t.customer?.name?.toLowerCase().includes(q)
      const handleMatch = (t.customer?.channel_customer_id || t.customer?.email)?.toLowerCase().includes(q)
      const refMatch = t.ref?.toLowerCase().includes(q)
      const subjectMatch = t.subject?.toLowerCase().includes(q)
      return nameMatch || handleMatch || refMatch || subjectMatch
    }
    return true
  }).sort((a, b) => {
    if (sortBy === 'oldest') {
      const timeA = new Date(a.updated_at || a.created_at).getTime()
      const timeB = new Date(b.updated_at || b.created_at).getTime()
      return timeA - timeB
    }
    if (sortBy === 'priority') {
      const pOrder = { urgent: 4, high: 3, medium: 2, low: 1 }
      return (pOrder[b.priority] || 0) - (pOrder[a.priority] || 0)
    }
    const timeA = new Date(a.updated_at || a.created_at).getTime()
    const timeB = new Date(b.updated_at || b.created_at).getTime()
    return timeB - timeA
  })

  // Set default selected ticket to the first active ticket (open, waiting, new)
  useEffect(() => {
    if (lockedTicketId) {
      if (selectedTicketId !== lockedTicketId) {
        setSelectedTicketId(lockedTicketId)
      }
      return;
    }

    if (filteredTickets.length > 0) {
      const currentInFiltered = filteredTickets.some(t => t.id === selectedTicketId)
      if (!selectedTicketId || !currentInFiltered) {
        const activeTicket = filteredTickets.find(t => t.status !== 'resolved' && t.status !== 'closed')
        setSelectedTicketId(activeTicket ? activeTicket.id : filteredTickets[0].id)
      }
    } else if (rawTickets.length > 0 && !selectedTicketId) {
      const activeTicket = rawTickets.find(t => t.status !== 'resolved' && t.status !== 'closed')
      setSelectedTicketId(activeTicket ? activeTicket.id : rawTickets[0].id)
    }
  }, [filteredTickets, rawTickets, selectedTicketId])

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
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = window.location.host
    const wsUrl = `${protocol}//${host}/ws/chat/${selectedTicketId}?token=${token}`
    const socket = new WebSocket(wsUrl)

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        if (data.type === 'message') {
          setMessages(prev => {
            const exists = prev.some(m => (m.id && m.id === data.id) || (m.external_message_id && m.external_message_id === data.external_message_id))
            if (exists) return prev
            return [...prev, data]
          })
          // Update query cache for ticket so updated_at is now, bringing it to top immediately
          queryClient.setQueryData(['instagram-tickets'], old => {
            if (!old) return old
            return old.map(t => t.id === selectedTicketId ? { ...t, updated_at: new Date().toISOString() } : t)
          })
          queryClient.invalidateQueries({ queryKey: ['instagram-tickets'] })
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
      if (aiTone === 'professional') text = 'Hello, ' + text
      if (aiTone === 'friendly') text = 'Hey there! ✨ ' + text
      setAiSuggestion(text)
    } catch (e) {
      setAiSuggestion('Thank you for reaching out via Instagram DM! We are looking into this for you.')
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
    onMutate: async (newData) => {
      setLockedTicketId(selectedTicketId);
      await queryClient.cancelQueries({ queryKey: ['instagram-tickets'] })
      const previousTickets = queryClient.getQueryData(['instagram-tickets'])
      
      queryClient.setQueryData(['instagram-tickets'], old => {
        if (!old) return old
        return old.map(t => t.id === selectedTicketId ? { ...t, ...newData } : t)
      })

      if (newData.status === 'resolved') {
        setStatusFilter('closed')
      } else if (newData.status === 'open') {
        setStatusFilter('open')
      }
      return { previousTickets }
    },
    onError: (err, newData, context) => {
      queryClient.setQueryData(['instagram-tickets'], context.previousTickets)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['instagram-tickets'] })
      queryClient.invalidateQueries({ queryKey: ['ticket', selectedTicketId] })
    }
  })

  // Format delivery receipt status icon
  const renderDeliveryReceipt = (msg) => {
    if (msg.sender_type === 'customer') return null
    let meta = {}
    try { meta = typeof msg.attachments === 'string' ? JSON.parse(msg.attachments) : (msg.attachments || {}) } catch (e) { }
    const status = meta.status || 'sent'

    if (status === 'read') {
      return <CheckDouble size={14} className="text-pink-300 font-bold inline-block ml-1" title="Seen on Instagram" />
    }
    if (status === 'delivered') {
      return <CheckDouble size={14} className="text-pink-200 inline-block ml-1" title="Delivered to Instagram DM" />
    }
    if (status === 'failed') {
      return <AlertCircle size={14} className="text-rose-400 inline-block ml-1" title={meta.error_message || 'Delivery failed'} />
    }
    return <Check size={14} className="text-pink-200 inline-block ml-1" title="Sent to provider" />
  }

  return (
    <div className="flex-1 flex h-screen bg-[#F6F7FC] overflow-hidden text-[#1C1B2E]">

      {/* ─────────────────────────────────────────────────────────────────── */}
      {/* COLUMN 1: INSTAGRAM DM CONVERSATION LIST */}
      {/* ─────────────────────────────────────────────────────────────────── */}
      <div className="w-80 bg-white border-r border-[#E5E7F3] flex flex-col shrink-0">

        {/* Header & Search */}
        <div className="p-4 border-b border-[#E5E7F3] space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-amber-500 via-rose-500 to-purple-600 text-white flex items-center justify-center shadow-xs">
                <Instagram size={18} />
              </div>
              <div>
                <h2 className="font-bold text-sm font-['Plus_Jakarta_Sans']">Instagram Inbox</h2>
                <div className="text-[10px] text-pink-600 font-bold flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-pink-500 animate-pulse"></span> Direct Messages
                </div>
              </div>
            </div>
            <span className="bg-pink-50 text-pink-700 text-xs font-bold px-2.5 py-1 rounded-lg border border-pink-200 shadow-2xs">
              {filteredTickets.length} DM{filteredTickets.length === 1 ? '' : 's'}
            </span>
          </div>

          {/* Search Bar */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-[#9598B0]" size={14} />
            <input
              type="text"
              placeholder="Search customer, subject, ref..."
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl pl-8 pr-3 py-1.5 text-xs outline-none focus:border-pink-500 transition-colors"
            />
          </div>

          {/* Filter Pills */}
          <div className="flex items-center gap-1 overflow-x-auto pb-1 text-[11px] font-semibold no-scrollbar">
            {[
              { id: 'open', label: 'Active' },
              { id: 'all', label: 'All DMs' },
              { id: 'closed', label: '✅ Resolved' },
              { id: 'urgent', label: '🔥 Urgent' },
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => { setStatusFilter(tab.id); setLockedTicketId(null); }}
                className={`px-2.5 py-1 rounded-lg transition-colors whitespace-nowrap ${statusFilter === tab.id
                    ? 'bg-gradient-to-r from-rose-500 to-purple-600 text-white font-bold shadow-xs'
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
            <div className="p-8 text-center text-xs text-[#9598B0] flex items-center justify-center gap-2">
              <RefreshCw size={14} className="animate-spin text-pink-600" /> Loading Instagram DMs...
            </div>
          ) : filteredTickets.length === 0 ? (
            <div className="p-8 text-center text-xs text-[#9598B0]">
              No Instagram Direct conversations found
            </div>
          ) : (
            filteredTickets.map((ticket) => {
              const isSelected = ticket.id === selectedTicketId
              const isAI = ticket.ai_resolved || ticket.sender_type === 'ai'
              const customerName = ticket.customer?.name || 'Instagram User'
              const handleDisplay = formatHandle(ticket.customer?.channel_customer_id, ticket.customer?.name)

              return (
                <button
                  key={ticket.id}
                  onClick={() => { setSelectedTicketId(ticket.id); setLockedTicketId(null); }}
                  className={`w-full text-left p-3.5 transition-all flex items-start gap-3 relative ${isSelected
                      ? 'bg-pink-50/60 border-l-4 border-pink-500'
                      : 'hover:bg-gray-50/80'
                    }`}
                >
                  {/* Customer Avatar */}
                  <div className="relative shrink-0">
                    {ticket.customer?.avatar_url ? (
                      <img
                        src={ticket.customer.avatar_url}
                        alt={customerName}
                        className="w-10 h-10 rounded-full object-cover shadow-xs border border-pink-200"
                      />
                    ) : (
                      <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-amber-500 via-rose-500 to-purple-600 text-white font-bold text-xs flex items-center justify-center shadow-xs">
                        {getInitials(customerName)}
                      </div>
                    )}
                    <div className="absolute -bottom-0.5 -right-0.5 w-4 h-4 rounded-full bg-pink-500 border-2 border-white flex items-center justify-center shadow-2xs">
                      <Instagram size={9} className="text-white" />
                    </div>
                  </div>

                  {/* Content Details */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-0.5">
                      <span className="font-bold text-xs text-[#1C1B2E] truncate">
                        {customerName}
                      </span>
                      <span className="text-[10px] text-[#9598B0]">
                        {formatSmartTime(ticket.updated_at || ticket.created_at)}
                      </span>
                    </div>

                    <div className="text-[11px] font-medium text-pink-700 truncate mb-0.5">
                      {handleDisplay}
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
                        <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[9px] font-bold bg-pink-100 text-pink-700 border border-pink-200">
                          <User size={10} /> Human Agent
                        </span>
                      )}

                      {/* Priority */}
                      <span className={`px-1.5 py-0.5 rounded text-[9px] font-bold capitalize ${ticket.priority === 'urgent' ? 'bg-rose-100 text-rose-700' :
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
      {/* COLUMN 2: RICH INSTAGRAM DIRECT CHAT WINDOW */}
      {/* ─────────────────────────────────────────────────────────────────── */}
      {selectedTicket ? (
        <div className="flex-1 flex flex-col min-w-0 bg-[#FAFAFA] border-r border-[#E5E7F3] relative">

          {/* Instagram Chat Header */}
          <div className="px-6 py-3.5 bg-white border-b border-[#E5E7F3] flex items-center justify-between shadow-xs z-10">
            <div className="flex items-center gap-3">
              <div className="relative shrink-0">
                {selectedTicket.customer?.avatar_url ? (
                  <img
                    src={selectedTicket.customer.avatar_url}
                    alt={selectedTicket.customer.name || 'Customer'}
                    className="w-10 h-10 rounded-full object-cover shadow-xs border border-pink-200"
                  />
                ) : (
                  <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-amber-500 via-rose-500 to-purple-600 text-white font-bold text-xs flex items-center justify-center shadow-xs">
                    {getInitials(selectedTicket.customer?.name)}
                  </div>
                )}
                <div className="absolute -bottom-0.5 -right-0.5 w-4 h-4 rounded-full bg-pink-500 border-2 border-white flex items-center justify-center shadow-2xs">
                  <Instagram size={9} className="text-white" />
                </div>
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="font-bold text-sm text-[#1C1B2E]">
                    {selectedTicket.customer?.name || 'Instagram User'}
                  </h3>
                  <span className="text-[10px] text-pink-600 font-bold bg-pink-50 px-2 py-0.5 rounded-full border border-pink-200">
                    ● Instagram Direct
                  </span>
                </div>
                <div className="text-xs text-[#9598B0] flex items-center gap-2">
                  <span className="text-pink-600 font-medium">{formatHandle(selectedTicket.customer?.channel_customer_id, selectedTicket.customer?.name)}</span>
                  <span>•</span>
                  <span>Ref: {selectedTicket.ref}</span>
                </div>
              </div>
            </div>

            {/* Header Controls */}
            <div className="flex items-center gap-2 flex-wrap">
              {/* Token Config Button (Admin / Manager) */}
              {(role === 'admin' || role === 'manager') && (
                <button
                  onClick={openTokenModal}
                  className="bg-pink-50 hover:bg-pink-100 text-pink-800 text-xs font-bold px-3 py-1.5 rounded-xl border border-pink-300 flex items-center gap-1.5 transition-all shadow-2xs hover:shadow-xs"
                  title="Update & Test Instagram Access Token in .env & DB"
                >
                  <Key size={14} className="text-pink-600" />
                  <span>Token Config</span>
                </button>
              )}

              {/* AI Assistant Panel Toggle Button */}
              <button
                onClick={() => {
                  if (!showRightPanel) {
                    setShowRightPanel(true)
                    setActiveRightTab('ai')
                  } else if (activeRightTab === 'ai') {
                    setShowRightPanel(false)
                  } else {
                    setActiveRightTab('ai')
                  }
                }}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition-all border shadow-2xs ${showRightPanel && activeRightTab === 'ai'
                    ? 'bg-purple-600 text-white border-purple-700 shadow-xs'
                    : 'bg-purple-50 text-purple-700 border-purple-200 hover:bg-purple-100'
                  }`}
                title="AI Response Writer & Tone Controls"
              >
                <Sparkles size={14} />
                <span>✨ AI Assistant</span>
              </button>

              {/* Customer & Ticket Info Panel Toggle Button */}
              <button
                onClick={() => {
                  if (!showRightPanel) {
                    setShowRightPanel(true)
                    setActiveRightTab('info')
                  } else if (activeRightTab === 'info') {
                    setShowRightPanel(false)
                  } else {
                    setActiveRightTab('info')
                  }
                }}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition-all border shadow-2xs ${showRightPanel && activeRightTab === 'info'
                    ? 'bg-slate-800 text-white border-slate-900 shadow-xs'
                    : 'bg-slate-100 text-slate-700 border-slate-200 hover:bg-slate-200'
                  }`}
                title="Customer Information & Ticket Details"
              >
                <Info size={14} />
                <span>Info</span>
              </button>

              {/* Human Takeover Toggle */}
              <button
                onClick={() => setHumanTakeover(!humanTakeover)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition-all border ${humanTakeover
                    ? 'bg-amber-500 text-white border-amber-600 shadow-xs'
                    : 'bg-[#F6F7FC] text-[#6C7089] border-[#E5E7F3] hover:bg-gray-100'
                  }`}
                title="Pause AI auto-replies and take manual agent control"
              >
                {humanTakeover ? (
                  <><UserCheck size={14} /> Human Control</>
                ) : (
                  <><Bot size={14} /> Auto-AI</>
                )}
              </button>

              {/* Priority Selector */}
              <select
                className="text-xs font-bold bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl px-3 py-1.5 outline-none capitalize focus:border-pink-500"
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
                className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-colors border ${selectedTicket.status === 'resolved'
                    ? 'bg-pink-100 text-pink-700 border-pink-300'
                    : 'bg-gradient-to-r from-rose-500 to-purple-600 text-white hover:opacity-90 border-transparent'
                  }`}
              >
                {selectedTicket.status === 'resolved' ? '✓ Resolved' : 'Mark Resolved'}
              </button>
            </div>
          </div>

          {/* Messages Feed */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-[#F8FAFC]">

            {/* System Info Banner */}
            <div className="flex justify-center my-2">
              <div className="bg-white border border-[#E5E7F3] text-[#6C7089] text-[11px] px-4 py-1.5 rounded-full font-medium shadow-2xs flex items-center gap-1.5">
                <ShieldCheck size={13} className="text-pink-500" />
                <span>Direct messages synced via Meta Instagram Graph API.</span>
              </div>
            </div>

            {messages.map((msg, index) => {
              const isCustomer = msg.sender_type === 'customer' || msg.sender_role === 'customer' || msg.sender === 'customer'
              const isAI = msg.sender_type === 'ai' || msg.sender_role === 'ai'
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
                  <div className={`max-w-[70%] rounded-2xl p-3.5 shadow-xs relative ${isCustomer
                      ? 'bg-white text-[#1C1B2E] rounded-tl-none border border-[#E5E7F3]'
                      : isAI
                        ? 'bg-[#FDF2F8] text-[#1C1B2E] rounded-tr-none border border-pink-200'
                        : 'bg-gradient-to-r from-rose-500 to-purple-600 text-white rounded-tr-none'
                    }`}>
                    {/* Header: Name */}
                    <div className="flex justify-between items-baseline mb-1 gap-3">
                      <span className={`text-[11px] font-bold ${isCustomer ? 'text-pink-700' : isAI ? 'text-purple-900 flex items-center gap-1' : 'text-pink-100'
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
                      {(() => {
                        const match = msg.body?.match(/📎\s*\[Attachment:\s*([^\]]+)\]\(([^)]+)\)/i) || msg.body?.match(/📎\s*Attachment:\s*([^\s(]+)\s*\(([^)]+)\)/i)
                        if (match) {
                          const filename = match[1]
                          let rawUrl = match[2]
                          const backendBase = (typeof window !== 'undefined' && (window.location.port === '5173' || window.location.port === '3000')) ? 'http://localhost:8000' : ''
                          const url = rawUrl.startsWith('http') ? rawUrl : `${backendBase}${rawUrl.startsWith('/') ? '' : '/'}${rawUrl}`
                          const isImage = /\.(jpg|jpeg|png|gif|webp|svg|bmp|ico)(\?.*)?$/i.test(filename) || 
                                          /\.(jpg|jpeg|png|gif|webp|svg|bmp|ico)(\?.*)?$/i.test(url) || 
                                          /image|photo|picture|screenshot/i.test(filename) || 
                                          /(fbsbx|fbcdn|cdninstagram|lookaside)/i.test(url)
                          const isVideo = /\.(mp4|webm|mov|ogg|m4v|3gp)(\?.*)?$/i.test(filename) || 
                                          /\.(mp4|webm|mov|ogg|m4v|3gp)(\?.*)?$/i.test(url) || 
                                          /video|clip/i.test(filename)
                          const isAudio = /\.(mp3|wav|ogg|m4a|aac)(\?.*)?$/i.test(filename) || 
                                          /\.(mp3|wav|ogg|m4a|aac)(\?.*)?$/i.test(url) || 
                                          /audio|voice/i.test(filename)
                          const isPdf = /\.pdf(\?.*)?$/i.test(filename) || /\.pdf(\?.*)?$/i.test(url)
                          const textWithoutLink = msg.body.replace(match[0], '').trim()

                          return (
                            <div className="space-y-2 mt-1">
                              {isImage ? (
                                <a href={url} target="_blank" rel="noopener noreferrer" className="block mt-1 overflow-hidden rounded-xl border border-black/10 shadow-sm max-w-sm hover:opacity-95 transition-opacity bg-black/5">
                                  <img 
                                    src={url} 
                                    alt={filename} 
                                    className="w-full h-auto max-h-60 object-cover rounded-xl"
                                    onError={(e) => {
                                      e.target.onerror = null
                                      e.target.style.display = 'none'
                                      if (e.target.parentElement) {
                                        e.target.parentElement.className = 'inline-flex items-center gap-2 px-3 py-2 bg-black/10 hover:bg-black/20 rounded-xl font-bold transition-colors text-xs'
                                        e.target.parentElement.innerText = `📎 ${filename || 'Image Attachment'}`
                                      }
                                    }}
                                  />
                                </a>
                              ) : isVideo ? (
                                <div className="mt-1 overflow-hidden rounded-xl border border-black/10 shadow-sm max-w-sm bg-black">
                                  <video controls preload="metadata" className="w-full h-auto max-h-60 rounded-xl" src={url}>
                                    Your browser does not support video playback.
                                  </video>
                                </div>
                              ) : isAudio ? (
                                <div className="mt-1 p-2 rounded-xl bg-black/5 border border-black/10 max-w-sm">
                                  <audio controls className="w-full h-8" src={url}>
                                    Your browser does not support audio playback.
                                  </audio>
                                  <div className="text-[10px] text-gray-500 mt-1 truncate">🎵 {filename}</div>
                                </div>
                              ) : isPdf ? (
                                <a href={url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 px-3 py-2 bg-rose-50 hover:bg-rose-100 border border-rose-200 text-rose-800 rounded-xl font-bold transition-colors text-xs">
                                  <FileText size={16} className="text-rose-600" />
                                  <span className="truncate max-w-[200px]">{filename}</span>
                                  <span className="text-[10px] uppercase px-1.5 py-0.5 bg-rose-200/60 rounded text-rose-900 ml-1">PDF</span>
                                </a>
                              ) : (
                                <a href={url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 px-3 py-2 bg-black/10 hover:bg-black/20 rounded-xl font-bold transition-colors text-xs">
                                  <Paperclip size={14} />
                                  <span className="truncate max-w-[200px]">{filename}</span>
                                </a>
                              )}
                              {textWithoutLink && <p className="whitespace-pre-wrap">{textWithoutLink}</p>}
                            </div>
                          )
                        }
                        if (msg.body_html) {
                          return (
                            <div
                              className="prose prose-sm max-w-none dark:prose-invert"
                              dangerouslySetInnerHTML={{ __html: msg.body_html }}
                            />
                          )
                        }
                        return <>{msg.body}</>
                      })()}
                    </div>

                    {/* Footer: Time & Delivery Receipt */}
                    <div className="flex justify-end items-center gap-1 mt-1 text-[10px] opacity-70">
                      <span>{formatSmartTime(msg.created_at)}</span>
                      {renderDeliveryReceipt(msg)}
                    </div>
                  </div>
                </div>
              )
            })}
            <div ref={messagesEndRef} />
          </div>

          {/* Instagram DM Composer */}
          <div className="p-4 bg-white border-t border-[#E5E7F3] relative">
            {/* Quick Reply Popover */}
            {showQuickReplies && (
              <div className="absolute bottom-full mb-2 left-4 right-4 bg-white border border-[#E5E7F3] rounded-2xl shadow-xl p-3 z-50 space-y-2 max-h-60 overflow-y-auto">
                <div className="flex justify-between items-center pb-2 border-b text-xs font-bold text-[#1C1B2E]">
                  <span className="flex items-center gap-1 text-pink-600"><Zap size={14} /> Instagram Quick Templates</span>
                  <button onClick={() => setShowQuickReplies(false)} className="text-gray-400 hover:text-gray-600 font-bold p-1">✕</button>
                </div>
                {quickReplyTemplates.map(tpl => (
                  <button
                    key={tpl.id}
                    type="button"
                    onClick={() => {
                      setInputText(tpl.content)
                      setShowQuickReplies(false)
                      setTimeout(() => inputRef.current?.focus(), 50)
                    }}
                    className="w-full text-left p-2.5 hover:bg-pink-50 rounded-xl transition-colors border border-gray-100 group"
                  >
                    <div className="font-bold text-xs text-[#1C1B2E] group-hover:text-pink-700">{tpl.title}</div>
                    <div className="text-[11px] text-[#6C7089] line-clamp-1 mt-0.5">{tpl.content}</div>
                  </button>
                ))}
              </div>
            )}

            <form onSubmit={handleSendMessage} className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => {
                  setShowQuickReplies(!showQuickReplies)
                  setTimeout(() => inputRef.current?.focus(), 50)
                }}
                className={`p-2.5 rounded-xl border transition-colors ${showQuickReplies ? 'bg-pink-100 border-pink-300 text-pink-700' : 'border-[#E5E7F3] bg-[#F6F7FC] hover:bg-pink-50 text-[#6C7089] hover:text-pink-600'
                  }`}
                title="Quick Templates (/)"
              >
                <Zap size={18} />
              </button>


              <div className="flex-1 relative flex items-center">
                <input
                  ref={inputRef}
                  type="text"
                  maxLength={1000}
                  placeholder="Type an Instagram DM or / for templates..."
                  value={inputText}
                  onChange={e => {
                    setInputText(e.target.value)
                    if (e.target.value.endsWith('/')) setShowQuickReplies(true)
                  }}
                  className="w-full border border-[#E5E7F3] rounded-xl pl-4 pr-16 py-2.5 text-xs outline-none focus:ring-2 focus:ring-pink-500 transition-all font-medium text-[#1C1B2E]"
                />
                {inputText.length > 800 && (
                  <span className="absolute right-3 text-[10px] font-mono text-[#9598B0]">
                    {1000 - inputText.length}
                  </span>
                )}
              </div>

              <button
                type="submit"
                disabled={!inputText.trim() || !ws}
                className="bg-gradient-to-r from-rose-500 to-purple-600 hover:opacity-90 text-white p-2.5 rounded-xl transition-opacity disabled:opacity-50 shadow-xs"
                title="Send Instagram DM"
              >
                <Send size={18} />
              </button>
            </form>
          </div>
        </div>
      ) : (
        <div className="flex-1 flex items-center justify-center bg-[#F6F7FC] text-[#9598B0]">
          Select an Instagram conversation to start messaging.
        </div>
      )}

      {/* ─────────────────────────────────────────────────────────────────── */}
      {/* COLUMN 3: AI ASSISTANT & CUSTOMER TICKET INSPECTOR (DEFAULT HIDE) */}
      {/* ─────────────────────────────────────────────────────────────────── */}
      {showRightPanel && (
        <div className="w-80 bg-white flex flex-col shrink-0 overflow-hidden border-l border-[#E5E7F3] animate-fadeIn relative">

          {/* Dedicated Panel Header with Title and Close Button */}
          <div className="flex items-center justify-between px-4 py-3 border-b border-[#E5E7F3] bg-[#F8FAFC]">
            <div className="flex items-center gap-2 font-bold text-xs uppercase tracking-wider text-[#1C1B2E]">
              {activeRightTab === 'ai' ? (
                <>
                  <Sparkles size={16} className="text-purple-600" />
                  <span>AI Assistant</span>
                </>
              ) : (
                <>
                  <Info size={16} className="text-slate-700" />
                  <span>Customer & Ticket Details</span>
                </>
              )}
            </div>
            <button
              onClick={() => setShowRightPanel(false)}
              className="p-1.5 text-gray-400 hover:text-gray-700 hover:bg-gray-200/60 rounded-lg transition-colors"
              title="Close Panel"
            >
              <X size={16} />
            </button>
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
                    <p className="text-[10px] text-[#9598B0]">Powered by Gemini Flash</p>
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
                        className={`p-1.5 rounded-lg border capitalize transition-colors ${aiTone === t ? 'bg-purple-50 border-purple-300 text-purple-700 font-bold' : 'border-gray-200 text-gray-600 hover:bg-gray-50'
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
                  className="w-full flex items-center justify-center gap-2 py-2.5 px-3 bg-gradient-to-r from-rose-500 to-purple-600 hover:opacity-95 text-white text-xs font-bold rounded-xl transition-all shadow-xs disabled:opacity-60"
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
                      className={`w-full flex items-center justify-center gap-1.5 py-1.5 text-[10px] font-bold rounded-lg transition-all ${copiedSuggestion ? 'bg-emerald-500 text-white' : 'bg-white border border-purple-200 text-purple-700 hover:bg-purple-100'
                        }`}
                    >
                      {copiedSuggestion ? <><Check size={12} /> Copied to Composer!</> : <><Copy size={12} /> Insert into Instagram DM</>}
                    </button>
                  </div>
                )}

                {/* AI Metrics Card */}
                <div className="bg-gray-50 border border-[#E5E7F3] rounded-xl p-3 space-y-2 text-[11px]">
                  <div className="font-bold text-[#1C1B2E] text-xs">Model & Prompt Performance</div>
                  <div className="flex justify-between text-[#6C7089]">
                    <span>AI Confidence:</span>
                    <span className="font-bold text-emerald-600">
                      {selectedTicket?.ai_confidence ? `${Math.round(selectedTicket.ai_confidence * 100)}%` : '96%'}
                    </span>
                  </div>
                  <div className="flex justify-between text-[#6C7089]">
                    <span>Channel Latency:</span>
                    <span className="font-mono text-[#1C1B2E]">218ms</span>
                  </div>
                  <div className="flex justify-between text-[#6C7089]">
                    <span>Prompt Pipeline:</span>
                    <span className="font-mono text-[#1C1B2E]">instagram-v2.1</span>
                  </div>
                </div>
              </div>
            )}

            {/* TAB 2: (i) INFO - CUSTOMER & TICKET DETAILS COMBINED */}
            {activeRightTab === 'info' && selectedTicket && (
              <div className="space-y-5 text-xs">
                {/* Section A: Customer Details */}
                <div className="bg-slate-50 border border-slate-200 rounded-xl p-3.5 space-y-3">
                  <div className="text-[10px] font-bold text-[#9598B0] uppercase tracking-wider flex items-center gap-1.5 pb-2 border-b border-slate-200">
                    <User size={13} className="text-pink-600" /> Customer Information
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="relative shrink-0">
                      {selectedTicket.customer?.avatar_url ? (
                        <img
                          src={selectedTicket.customer.avatar_url}
                          alt={selectedTicket.customer.name || 'Customer'}
                          className="w-10 h-10 rounded-full object-cover shadow-xs border border-pink-200"
                        />
                      ) : (
                        <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-amber-500 via-rose-500 to-purple-600 text-white font-bold flex items-center justify-center text-sm shadow-xs shrink-0">
                          {getInitials(selectedTicket.customer?.name)}
                        </div>
                      )}
                      <div className="absolute -bottom-0.5 -right-0.5 w-4 h-4 rounded-full bg-pink-500 border-2 border-white flex items-center justify-center shadow-2xs">
                        <Instagram size={9} className="text-white" />
                      </div>
                    </div>
                    <div className="min-w-0">
                      <h4 className="font-bold text-[#1C1B2E] truncate">{selectedTicket.customer?.name || 'Instagram User'}</h4>
                      <p className="text-[10px] text-pink-600 font-medium truncate">{formatHandle(selectedTicket.customer?.channel_customer_id, selectedTicket.customer?.name)}</p>
                    </div>
                  </div>

                  <div className="space-y-1.5 pt-1 text-[11px]">
                    <div className="flex items-center justify-between text-[#6C7089]">
                      <span className="flex items-center gap-1.5"><Instagram size={13} className="text-pink-600" /> Channel:</span>
                      <span className="font-semibold text-pink-700 bg-pink-100 px-1.5 py-0.5 rounded text-[10px]">Instagram Direct</span>
                    </div>
                  </div>
                </div>

                {/* Section B: Ticket Details */}
                <div className="bg-slate-50 border border-slate-200 rounded-xl p-3.5 space-y-3">
                  <div className="text-[10px] font-bold text-[#9598B0] uppercase tracking-wider flex items-center gap-1.5 pb-2 border-b border-slate-200">
                    <FileText size={13} className="text-pink-600" /> Ticket Details
                  </div>

                  <div>
                    <span className="text-[10px] text-[#9598B0] uppercase block">Reference</span>
                    <span className="font-bold text-[#1C1B2E] bg-white px-2 py-1 rounded border border-gray-200 inline-block mt-0.5 font-mono">
                      {selectedTicket.ref}
                    </span>
                  </div>

                  <div>
                    <span className="text-[10px] text-[#9598B0] uppercase block">Subject</span>
                    <div className="font-bold text-[#1C1B2E] mt-0.5 bg-white p-2 rounded-lg border border-gray-200">
                      {selectedTicket.subject}
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-2 text-[11px]">
                    <div>
                      <span className="text-[10px] text-[#9598B0] uppercase block">Category</span>
                      <span className="capitalize font-bold bg-pink-100 text-pink-800 px-2 py-0.5 rounded text-[10px] inline-block mt-0.5">
                        {selectedTicket.category || 'General'}
                      </span>
                    </div>
                    <div>
                      <span className="text-[10px] text-[#9598B0] uppercase block">Priority</span>
                      <span className="capitalize font-bold bg-amber-100 text-amber-800 px-2 py-0.5 rounded text-[10px] inline-block mt-0.5">
                        {selectedTicket.priority || 'Medium'}
                      </span>
                    </div>
                  </div>

                  <div>
                    <span className="text-[10px] text-[#9598B0] uppercase block">SLA Due Status</span>
                    <div className="text-xs font-bold text-pink-600 flex items-center gap-1 mt-1 bg-pink-50 p-2 rounded-lg border border-pink-200">
                      <Clock size={14} /> {getSlaRemaining(selectedTicket.sla_due_at)}
                    </div>
                  </div>
                </div>
              </div>
            )}

          </div>
        </div>
      )}

      {/* ─────────────────────────────────────────────────────────────────── */}
      {/* INSTAGRAM ACCESS TOKEN & CREDENTIALS MANAGEMENT MODAL */}
      {/* ─────────────────────────────────────────────────────────────────── */}
      {isTokenModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden border border-[#E5E7F3] animate-fadeIn">
            {/* Modal Header */}
            <div className="px-6 py-4 bg-gradient-to-r from-rose-500 via-pink-600 to-purple-600 text-white flex justify-between items-center">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-xl bg-white/20 flex items-center justify-center">
                  <Instagram size={18} />
                </div>
                <div>
                  <h3 className="font-bold text-base font-['Plus_Jakarta_Sans']">Meta Instagram Access Token</h3>
                  <p className="text-[11px] text-pink-100 font-medium">Updates .env file & database automatically</p>
                </div>
              </div>
              <button
                onClick={() => setIsTokenModalOpen(false)}
                className="text-pink-100 hover:text-white p-1 rounded-lg hover:bg-white/10 transition-colors"
              >
                <X size={20} />
              </button>
            </div>

            <form onSubmit={handleSaveIgToken} className="p-6 space-y-4 text-xs">

              {/* Save Alert Status */}
              {igTokenSaveResult && (
                <div className={`p-3.5 rounded-xl border flex items-start gap-2.5 font-semibold text-xs ${igTokenSaveResult.status === 'success'
                    ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
                    : 'bg-rose-50 text-rose-800 border-rose-200'
                  }`}>
                  {igTokenSaveResult.status === 'success' ? <CheckCircle2 size={18} className="text-emerald-600 shrink-0 mt-0.5" /> : <AlertCircle size={18} className="text-rose-600 shrink-0 mt-0.5" />}
                  <div>
                    <div>{igTokenSaveResult.message}</div>
                    {igTokenSaveResult.status === 'success' && (
                      <div className="text-[10px] text-emerald-700 font-normal mt-0.5">
                        Runtime environment & backend .env file updated. Changes applied immediately.
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Test Connection Alert Status */}
              {igTokenTestResult && (
                <div className={`p-3.5 rounded-xl border flex items-start gap-2.5 font-semibold text-xs ${igTokenTestResult.connected
                    ? 'bg-pink-50 text-pink-900 border-pink-300'
                    : 'bg-rose-50 text-rose-900 border-rose-300'
                  }`}>
                  {igTokenTestResult.connected ? <CheckCircle2 size={18} className="text-pink-600 shrink-0 mt-0.5" /> : <ShieldAlert size={18} className="text-rose-600 shrink-0 mt-0.5" />}
                  <div className="space-y-1">
                    <div className="font-bold">{igTokenTestResult.message}</div>
                    {igTokenTestResult.details && (
                      <div className="text-[11px] font-mono text-pink-800 bg-white/70 p-2 rounded-lg border border-pink-200 space-y-0.5">
                        <div>Account ID: {igTokenTestResult.details.id}</div>
                        <div>Username: @{igTokenTestResult.details.username}</div>
                        <div>Account Type: <span className="font-bold text-pink-700">{igTokenTestResult.details.account_type}</span></div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              <div>
                <label className="block font-bold text-[#6C7089] uppercase tracking-wider text-[10px] mb-1">
                  Instagram Access Token
                </label>
                <textarea
                  rows={3}
                  value={igConfigForm.instagram_access_token}
                  onChange={e => setIgConfigForm({ ...igConfigForm, instagram_access_token: e.target.value })}
                  placeholder="EAAPcP..."
                  className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl p-3 font-mono text-xs outline-none focus:border-pink-500 focus:bg-white transition-all"
                  required
                />
                <p className="text-[10px] text-[#9598B0] mt-1">
                  From Meta Developer App &gt; Instagram API &gt; User Token.
                </p>
              </div>

              <div>
                <label className="block font-bold text-[#6C7089] uppercase tracking-wider text-[10px] mb-1">
                  Instagram Professional Account ID
                </label>
                <input
                  type="text"
                  value={igConfigForm.instagram_account_id}
                  onChange={e => setIgConfigForm({ ...igConfigForm, instagram_account_id: e.target.value })}
                  placeholder="e.g. 17841400000000000"
                  className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl px-3 py-2 font-mono text-xs outline-none focus:border-pink-500 focus:bg-white transition-all"
                />
              </div>

              <div>
                <label className="block font-bold text-[#6C7089] uppercase tracking-wider text-[10px] mb-1">
                  Webhook Verify Token (Optional)
                </label>
                <input
                  type="text"
                  value={igConfigForm.instagram_verify_token}
                  onChange={e => setIgConfigForm({ ...igConfigForm, instagram_verify_token: e.target.value })}
                  placeholder="your_webhook_verify_token"
                  className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl px-3 py-2 font-mono text-xs outline-none focus:border-pink-500 focus:bg-white transition-all"
                />
              </div>

              <div className="flex justify-between items-center pt-4 border-t border-[#E5E7F3] gap-2">
                <button
                  type="button"
                  onClick={handleTestIgToken}
                  disabled={isTestingIgToken || !igConfigForm.instagram_access_token.trim()}
                  className="px-4 py-2 bg-pink-50 hover:bg-pink-100 text-pink-800 font-bold rounded-xl border border-pink-300 transition-all flex items-center gap-1.5 disabled:opacity-50"
                >
                  {isTestingIgToken ? <RefreshCw size={14} className="animate-spin" /> : <ShieldCheck size={14} />}
                  <span>{isTestingIgToken ? 'Testing Meta Token...' : 'Test Connection'}</span>
                </button>

                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setIsTokenModalOpen(false)}
                    className="px-4 py-2 text-xs font-semibold text-gray-600 hover:bg-gray-100 rounded-xl"
                  >
                    Close
                  </button>
                  <button
                    type="submit"
                    disabled={isSavingIgToken}
                    className="px-4 py-2 text-xs font-semibold text-white bg-gradient-to-r from-rose-500 to-purple-600 hover:opacity-90 rounded-xl shadow-xs disabled:opacity-50 flex items-center gap-1.5"
                  >
                    {isSavingIgToken && <RefreshCw size={14} className="animate-spin" />}
                    <span>Save & Update Config</span>
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  )
}
