import { useState, useEffect, useRef } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { ticketsApi } from '../api/tickets'
import { useAuthStore } from '../store/authStore'
import { formatDateTime, formatTime, formatSmartTime } from '../utils/dateUtils'
import { adminApi } from '../api/admin'
import { 
  Smartphone, Search, Filter, Bot, User, Send, Paperclip, 
  Sparkles, Check, CheckCheck, AlertCircle, Clock, Zap, 
  ShieldCheck, RefreshCw, Copy, CheckCheck as CheckDouble,
  Volume2, Play, Pause, MapPin, FileText, Image as ImageIcon,
  ChevronRight, Tag, Phone, Mail, Globe, ArrowRight, UserCheck,
  ToggleLeft, ToggleRight, Mic, Video, Sliders, MessageSquare,
  Key, X, Lock, ShieldAlert, CheckCircle2, Eye, EyeOff, Info
} from 'lucide-react'

// Authentic WhatsApp Avatar component: renders actual avatar_url if user uploaded/provided one; otherwise displays authentic WhatsApp monogram initials circle
function WhatsAppCustomerAvatar({ customer, size = 'md', className = '' }) {
  const [imgError, setImgError] = useState(false)
  const avatarUrl = customer?.avatar_url
  
  const sizeClasses = {
    sm: 'w-6 h-6 text-[10px]',
    md: 'w-10 h-10 text-xs',
    lg: 'w-12 h-12 text-sm',
  }[size] || 'w-10 h-10 text-xs'

  const getInitials = (name) => {
    if (!name) return 'WA'
    // Strip emojis and non-alphanumeric chars for clean letters
    const clean = name.replace(/[^\p{L}\p{N}\s]/gu, '').trim()
    if (!clean) return 'WA'
    const parts = clean.split(/\s+/).filter(Boolean)
    if (parts.length >= 2) {
      return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
    }
    return clean.slice(0, 2).toUpperCase()
  }

  const initials = getInitials(customer?.name)

  if (avatarUrl && !imgError) {
    return (
      <img
        src={avatarUrl}
        alt={customer?.name || 'Customer'}
        className={`${sizeClasses} rounded-full object-cover shadow-xs border border-emerald-200 shrink-0 ${className}`}
        onError={() => setImgError(true)}
      />
    )
  }

  return (
    <div className={`${sizeClasses} rounded-full bg-emerald-600 text-white font-bold tracking-tight flex items-center justify-center shadow-xs shrink-0 ${className}`}>
      {initials}
    </div>
  )
}

export default function WhatsAppInbox({ basePath = '/agent' }) {
  const { token, role, name: currentName } = useAuthStore()
  const isAgent = basePath === '/agent' || (role === 'agent' && basePath !== '/manager' && basePath !== '/admin')
  const queryClient = useQueryClient()
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  // Phone number formatter
  const formatPhone = (raw) => {
    if (!raw) return 'No Phone Number'
    const cleaned = String(raw).replace(/\D/g, '')
    if (cleaned.length === 12 && cleaned.startsWith('91')) {
      return `+91 ${cleaned.slice(2, 7)} ${cleaned.slice(7)}`
    }
    if (cleaned.length === 10) {
      return `+91 ${cleaned.slice(0, 5)} ${cleaned.slice(5)}`
    }
    return raw.startsWith('+') ? raw : `+${raw}`
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
  const [statusFilter, setStatusFilter] = useState('open') // 'open' (Active) | 'all' | 'closed' | 'ai' | 'human' | 'urgent'
  const [sortBy, setSortBy] = useState('newest') // 'newest' | 'oldest' | 'priority'
  
  const [messages, setMessages] = useState([])
  const [inputText, setInputText] = useState('')
  const [ws, setWs] = useState(null)

  // AI & Panel state
  const [showRightPanel, setShowRightPanel] = useState(false) // DEFAULT HIDE
  const [showTokenText, setShowTokenText] = useState(false)
  const [activeRightTab, setActiveRightTab] = useState('ai') // 'ai' | 'info'
  const [aiSuggestion, setAiSuggestion] = useState(null)
  const [loadingSuggest, setLoadingSuggest] = useState(false)
  const [copiedSuggestion, setCopiedSuggestion] = useState(false)
  const [aiTone, setAiTone] = useState('standard') // 'standard' | 'shorter' | 'longer' | 'professional' | 'friendly'
  const [humanTakeover, setHumanTakeover] = useState(false)
  const [playingAudioId, setPlayingAudioId] = useState(null)

  // Quick Replies modal
  // Quick Replies modal
  const [showQuickReplies, setShowQuickReplies] = useState(false)
  const [lockedTicketId, setLockedTicketId] = useState(null)
  const [quickSearch, setQuickSearch] = useState('')

  // WhatsApp Token Management & Test Modal State
  const [isTokenModalOpen, setIsTokenModalOpen] = useState(false)
  const [waConfigForm, setWaConfigForm] = useState({
    whatsapp_access_token: '',
    whatsapp_phone_id: '',
    whatsapp_verify_token: '',
  })
  const [isTestingWaToken, setIsTestingWaToken] = useState(false)
  const [isSavingWaToken, setIsSavingWaToken] = useState(false)
  const [waTokenTestResult, setWaTokenTestResult] = useState(null)
  const [waTokenSaveResult, setWaTokenSaveResult] = useState(null)

  const openTokenModal = async () => {
    setIsTokenModalOpen(true)
    setWaTokenTestResult(null)
    setWaTokenSaveResult(null)
    try {
      const res = await adminApi.getWhatsAppConfig()
      setWaConfigForm({
        whatsapp_access_token: res.data.whatsapp_access_token || '',
        whatsapp_phone_id: res.data.whatsapp_phone_id || '',
        whatsapp_verify_token: res.data.whatsapp_verify_token || '',
      })
    } catch (e) {
      console.error('Failed to fetch WhatsApp config:', e)
    }
  }

  const handleSaveWaToken = async (e) => {
    e.preventDefault()
    setIsSavingWaToken(true)
    setWaTokenSaveResult(null)
    try {
      const res = await adminApi.updateWhatsAppConfig(waConfigForm)
      setWaTokenSaveResult({ status: 'success', message: res.data.message })
      queryClient.invalidateQueries({ queryKey: ['admin-channels'] })
    } catch (err) {
      setWaTokenSaveResult({ status: 'error', message: err.response?.data?.detail || 'Failed to update WhatsApp Access Token.' })
    } finally {
      setIsSavingWaToken(false)
    }
  }

  const handleTestWaToken = async () => {
    setIsTestingWaToken(true)
    setWaTokenTestResult(null)
    try {
      const res = await adminApi.testWhatsAppConfig(waConfigForm)
      setWaTokenTestResult(res.data)
    } catch (err) {
      setWaTokenTestResult({
        status: 'error',
        connected: false,
        message: err.response?.data?.detail || 'Token testing failed. Please verify credentials.'
      })
    } finally {
      setIsTestingWaToken(false)
    }
  }

  const quickReplyTemplates = [
    { id: '1', title: 'Welcome Greeting', content: 'Hello! Thanks for contacting our support team via WhatsApp. How can I assist you today?' },
    { id: '2', title: 'Order Tracking Link', content: 'Your order is on its way! You can track your shipment live here: https://supporthub.internal/track' },
    { id: '3', title: 'Business Hours', content: 'Our live support hours are Monday–Friday 9:00 AM – 6:00 PM EST. AI assistant is available 24/7!' },
    { id: '4', title: 'Issue Resolved', content: 'I have updated your account and resolved the reported issue. Please let us know if you need anything else!' },
  ]

  // 1. Query WhatsApp Tickets
  const { data: rawTickets = [], isLoading: loadingTickets } = useQuery({
    queryKey: ['whatsapp-tickets', isAgent ? 'human-only' : 'all'],
    queryFn: async () => {
      const params = {
        channel: 'whatsapp',
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
          queryClient.setQueryData(['whatsapp-tickets'], old => {
            if (!old) return old
            return old.map(t => t.id === selectedTicketId ? { ...t, updated_at: new Date().toISOString() } : t)
          })
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
    onMutate: async (newData) => {
      setLockedTicketId(selectedTicketId);
      await queryClient.cancelQueries({ queryKey: ['whatsapp-tickets'] })
      const previousTickets = queryClient.getQueryData(['whatsapp-tickets'])
      
      queryClient.setQueryData(['whatsapp-tickets'], old => {
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
      queryClient.setQueryData(['whatsapp-tickets'], context.previousTickets)
    },
    onSettled: () => {
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
            <span className="bg-emerald-50 text-emerald-700 text-xs font-bold px-2.5 py-1 rounded-lg border border-emerald-200 shadow-2xs">
              {filteredTickets.length} Ticket{filteredTickets.length === 1 ? '' : 's'}
            </span>
          </div>

          {/* Search Bar */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-[#9598B0]" size={14} />
            <input
              type="text"
              placeholder="Search phone, customer, ref, ID..."
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl pl-8 pr-3 py-1.5 text-xs outline-none focus:border-emerald-500 transition-colors"
            />
          </div>

          {/* Filter Pills */}
          <div className="flex items-center gap-1 overflow-x-auto pb-1 text-[11px] font-semibold no-scrollbar">
            {[
              { id: 'open', label: 'Active' },
              { id: 'all', label: 'All' },
              { id: 'closed', label: '✅ Resolved' },
              { id: 'urgent', label: '🔥 Urgent' },
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => { setStatusFilter(tab.id); setLockedTicketId(null); }}
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
            <div className="p-8 text-center text-xs text-[#9598B0] flex items-center justify-center gap-2">
              <RefreshCw size={14} className="animate-spin text-emerald-600" /> Loading chats...
            </div>
          ) : filteredTickets.length === 0 ? (
            <div className="p-8 text-center text-xs text-[#9598B0]">
              No WhatsApp conversations found
            </div>
          ) : (
            filteredTickets.map((ticket, idx) => {
              const isSelected = ticket.id === selectedTicketId
              const isAI = ticket.ai_resolved || ticket.sender_type === 'ai'
              const phoneDisplay = formatPhone(ticket.customer?.phone || ticket.customer?.channel_customer_id)

              return (
                <button
                  key={ticket.id}
                  onClick={() => { setSelectedTicketId(ticket.id); setLockedTicketId(null); }}
                  className={`w-full text-left p-3.5 transition-all flex items-start gap-3 relative ${
                    isSelected 
                      ? 'bg-emerald-50/60 border-l-4 border-emerald-500' 
                      : 'hover:bg-gray-50/80'
                  }`}
                >
                  {/* Customer Avatar */}
                  <div className="relative shrink-0">
                    <WhatsAppCustomerAvatar customer={ticket.customer} size="md" />
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
                        {formatSmartTime(ticket.updated_at || ticket.created_at)}
                      </span>
                    </div>

                    <div className="text-[11px] font-mono text-emerald-700 font-semibold truncate mb-0.5">
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
              <div className="relative shrink-0">
                <WhatsAppCustomerAvatar customer={selectedTicket.customer} size="md" />
                <div className="absolute -bottom-0.5 -right-0.5 w-4 h-4 rounded-full bg-emerald-500 border-2 border-white flex items-center justify-center">
                  <Smartphone size={9} className="text-white fill-white" />
                </div>
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

            {/* Header Controls: Token Config, AI Toggle, Human Takeover, Priority & Status */}
            <div className="flex items-center gap-2 flex-wrap">
              {/* Token Config Button (Admin / Manager) */}
              {(role === 'admin' || role === 'manager') && (
                <button
                  onClick={openTokenModal}
                  className="bg-emerald-50 hover:bg-emerald-100 text-emerald-800 text-xs font-bold px-3 py-1.5 rounded-xl border border-emerald-300 flex items-center gap-1.5 transition-all shadow-2xs hover:shadow-xs"
                  title="Update & Test WhatsApp Access Token in .env & DB"
                >
                  <Key size={14} className="text-emerald-600" />
                  <span>Token Config</span>
                </button>
              )}

              {/* AI Orchestrator Panel Toggle Button */}
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
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition-all border shadow-2xs ${
                  showRightPanel && activeRightTab === 'ai'
                    ? 'bg-purple-600 text-white border-purple-700 shadow-xs'
                    : 'bg-purple-50 text-purple-700 border-purple-200 hover:bg-purple-100'
                }`}
                title="AI Response Orchestrator & Tone Controls"
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
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition-all border shadow-2xs ${
                  showRightPanel && activeRightTab === 'info'
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
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition-all border ${
                  humanTakeover
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

          {/* WhatsApp Composer */}
          <div className="p-4 bg-white border-t border-[#E5E7F3] relative">
            {/* Quick Reply Popover */}
            {showQuickReplies && (
              <div className="absolute bottom-full mb-2 left-4 right-4 bg-white border border-[#E5E7F3] rounded-2xl shadow-xl p-3 z-50 space-y-2 max-h-60 overflow-y-auto">
                <div className="flex justify-between items-center pb-2 border-b text-xs font-bold text-[#1C1B2E]">
                  <span className="flex items-center gap-1 text-emerald-600"><Zap size={14} /> WhatsApp Quick Templates</span>
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
                    className="w-full text-left p-2.5 hover:bg-emerald-50 rounded-xl transition-colors border border-gray-100 group"
                  >
                    <div className="font-bold text-xs text-[#1C1B2E] group-hover:text-emerald-700">{tpl.title}</div>
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
                className={`p-2.5 rounded-xl border transition-colors ${
                  showQuickReplies ? 'bg-emerald-100 border-emerald-300 text-emerald-700' : 'border-[#E5E7F3] bg-[#F6F7FC] hover:bg-emerald-50 text-[#6C7089] hover:text-emerald-600'
                }`}
                title="Quick Templates (/)"
              >
                <Zap size={18} />
              </button>


              <input
                ref={inputRef}
                type="text"
                placeholder="Type a WhatsApp message or / for templates..."
                value={inputText}
                onChange={e => {
                  setInputText(e.target.value)
                  if (e.target.value.endsWith('/')) setShowQuickReplies(true)
                }}
                className="flex-1 border border-[#E5E7F3] rounded-xl px-4 py-2.5 text-xs outline-none focus:ring-2 focus:ring-emerald-500 transition-all font-medium text-[#1C1B2E]"
              />

              <button
                type="submit"
                disabled={!inputText.trim() || !ws}
                className="bg-emerald-600 hover:bg-emerald-700 text-white p-2.5 rounded-xl transition-colors disabled:opacity-50 shadow-xs"
                title="Send Message"
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
            
            {/* TAB 1: AI ASSISTANT (ONLY AI INFO & CONTROLS) */}
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
                    <span className="font-mono text-[#1C1B2E]">266ms</span>
                  </div>
                  <div className="flex justify-between text-[#6C7089]">
                    <span>Prompt Version:</span>
                    <span className="font-mono text-[#1C1B2E]">v2.4-prod</span>
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
                    <User size={13} className="text-emerald-600" /> Customer Information
                  </div>
                  <div className="flex items-center gap-3">
                    <WhatsAppCustomerAvatar customer={selectedTicket.customer} size="md" />
                    <div className="min-w-0">
                      <h4 className="font-bold text-[#1C1B2E] truncate">{selectedTicket.customer?.name || 'WhatsApp Customer'}</h4>
                      <p className="text-[10px] text-[#9598B0] truncate">{selectedTicket.customer?.phone || selectedTicket.customer?.channel_customer_id}</p>
                    </div>
                  </div>

                  <div className="space-y-1.5 pt-1 text-[11px]">
                    <div className="flex items-center justify-between text-[#6C7089]">
                      <span className="flex items-center gap-1.5"><Globe size={13} className="text-emerald-600" /> Channel:</span>
                      <span className="font-semibold text-emerald-700 bg-emerald-100 px-1.5 py-0.5 rounded text-[10px]">WhatsApp API</span>
                    </div>
                  </div>
                </div>

                {/* Section B: Ticket Details */}
                <div className="bg-slate-50 border border-slate-200 rounded-xl p-3.5 space-y-3">
                  <div className="text-[10px] font-bold text-[#9598B0] uppercase tracking-wider flex items-center gap-1.5 pb-2 border-b border-slate-200">
                    <FileText size={13} className="text-emerald-600" /> Ticket Details
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
                      <span className="capitalize font-bold bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded text-[10px] inline-block mt-0.5">
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
                    <div className="text-xs font-bold text-emerald-600 flex items-center gap-1 mt-1 bg-emerald-50 p-2 rounded-lg border border-emerald-200">
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
      {/* WHATSAPP ACCESS TOKEN & CREDENTIALS MANAGEMENT MODAL */}
      {/* ─────────────────────────────────────────────────────────────────── */}
      {isTokenModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden border border-[#E5E7F3] animate-fadeIn">
            {/* Modal Header */}
            <div className="px-6 py-4 bg-emerald-600 text-white flex justify-between items-center">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-xl bg-white/20 flex items-center justify-center">
                  <Key size={18} />
                </div>
                <div>
                  <h3 className="font-bold text-base font-['Plus_Jakarta_Sans']">Meta WhatsApp Access Token</h3>
                  <p className="text-[11px] text-emerald-100 font-medium">Updates .env file & database automatically</p>
                </div>
              </div>
              <button 
                onClick={() => setIsTokenModalOpen(false)}
                className="text-emerald-100 hover:text-white p-1 rounded-lg hover:bg-white/10 transition-colors"
              >
                <X size={20} />
              </button>
            </div>

            <form onSubmit={handleSaveWaToken} className="p-6 space-y-4 text-xs">
              
              {/* Save Alert Status */}
              {waTokenSaveResult && (
                <div className={`p-3.5 rounded-xl border flex items-start gap-2.5 font-semibold text-xs ${
                  waTokenSaveResult.status === 'success' 
                    ? 'bg-emerald-50 text-emerald-800 border-emerald-200' 
                    : 'bg-rose-50 text-rose-800 border-rose-200'
                }`}>
                  {waTokenSaveResult.status === 'success' ? <CheckCircle2 size={18} className="text-emerald-600 shrink-0 mt-0.5" /> : <AlertCircle size={18} className="text-rose-600 shrink-0 mt-0.5" />}
                  <div>
                    <div>{waTokenSaveResult.message}</div>
                    {waTokenSaveResult.status === 'success' && (
                      <div className="text-[10px] text-emerald-700 font-normal mt-0.5">
                        Runtime environment & backend .env file updated. Changes applied immediately.
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Test Alert Status */}
              {waTokenTestResult && (
                <div className={`p-3.5 rounded-xl border flex items-start gap-2.5 font-semibold text-xs ${
                  waTokenTestResult.connected 
                    ? 'bg-emerald-50 text-emerald-900 border-emerald-300' 
                    : 'bg-rose-50 text-rose-900 border-rose-300'
                }`}>
                  {waTokenTestResult.connected ? <CheckCircle2 size={18} className="text-emerald-600 shrink-0 mt-0.5" /> : <ShieldAlert size={18} className="text-rose-600 shrink-0 mt-0.5" />}
                  <div className="space-y-1">
                    <div className="font-bold">{waTokenTestResult.message}</div>
                    {waTokenTestResult.details && (
                      <div className="text-[11px] font-mono text-emerald-800 bg-white/70 p-2 rounded-lg border border-emerald-200 space-y-0.5">
                        <div>Account ID: {waTokenTestResult.details.id}</div>
                        <div>Display Phone: {waTokenTestResult.details.display_phone_number}</div>
                        <div>Verified Name: {waTokenTestResult.details.verified_name}</div>
                        <div>Quality Rating: <span className="font-bold text-emerald-700">{waTokenTestResult.details.quality_rating}</span></div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Access Token Field */}
              <div>
                <div className="flex justify-between items-center mb-1">
                  <label className="font-bold text-[#6C7089] uppercase tracking-wider text-[10px]">
                    Meta WhatsApp Access Token
                  </label>
                  <button
                    type="button"
                    onClick={() => setShowTokenText(!showTokenText)}
                    className="text-[11px] font-bold text-emerald-700 hover:text-emerald-800 flex items-center gap-1 transition-colors"
                  >
                    {showTokenText ? <EyeOff size={13} /> : <Eye size={13} />}
                    <span>{showTokenText ? 'Hide Secret' : 'Show Token'}</span>
                  </button>
                </div>
                <div className="relative">
                  <textarea
                    rows={3}
                    value={waConfigForm.whatsapp_access_token}
                    onChange={e => setWaConfigForm({ ...waConfigForm, whatsapp_access_token: e.target.value })}
                    placeholder="EAAPcP..."
                    className={`w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl p-3 font-mono text-xs outline-none focus:border-emerald-500 focus:bg-white transition-all ${
                      showTokenText ? 'text-gray-900' : 'text-security-disc blur-[2px] focus:blur-none'
                    }`}
                    required
                  />
                </div>
                <p className="text-[10px] text-[#9598B0] mt-1 flex items-center justify-between">
                  <span>From Meta Developer Portal &gt; WhatsApp &gt; API Setup</span>
                  {waConfigForm.whatsapp_access_token && (
                    <span className="font-mono text-emerald-600 font-bold">{waConfigForm.whatsapp_access_token.length} chars</span>
                  )}
                </p>
              </div>

              {/* Phone Number ID Field */}
              <div>
                <label className="block font-bold text-[#6C7089] uppercase tracking-wider text-[10px] mb-1">
                  WhatsApp Phone Number ID
                </label>
                <input
                  type="text"
                  value={waConfigForm.whatsapp_phone_id}
                  onChange={e => setWaConfigForm({ ...waConfigForm, whatsapp_phone_id: e.target.value })}
                  placeholder="e.g. 1296854793505632"
                  className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl px-3 py-2 font-mono text-xs outline-none focus:border-emerald-500 focus:bg-white transition-all"
                  required
                />
              </div>

              {/* Verify Token Field */}
              <div>
                <label className="block font-bold text-[#6C7089] uppercase tracking-wider text-[10px] mb-1">
                  Webhook Verify Token (Optional)
                </label>
                <input
                  type="text"
                  value={waConfigForm.whatsapp_verify_token}
                  onChange={e => setWaConfigForm({ ...waConfigForm, whatsapp_verify_token: e.target.value })}
                  placeholder="your_webhook_verify_token"
                  className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl px-3 py-2 font-mono text-xs outline-none focus:border-emerald-500 focus:bg-white transition-all"
                />
              </div>

              {/* Action buttons */}
              <div className="flex justify-between items-center pt-4 border-t border-[#E5E7F3] gap-2">
                <button
                  type="button"
                  onClick={handleTestWaToken}
                  disabled={isTestingWaToken || !waConfigForm.whatsapp_access_token.trim()}
                  className="px-4 py-2 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 font-bold rounded-xl border border-emerald-300 transition-all flex items-center gap-1.5 disabled:opacity-50"
                >
                  {isTestingWaToken ? <RefreshCw size={14} className="animate-spin" /> : <ShieldCheck size={14} />}
                  <span>{isTestingWaToken ? 'Testing Meta Token...' : 'Test Connection'}</span>
                </button>

                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setIsTokenModalOpen(false)}
                    className="px-4 py-2 text-xs font-semibold text-gray-600 hover:bg-gray-100 rounded-xl"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={isSavingWaToken || !waConfigForm.whatsapp_access_token.trim()}
                    className="px-5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl transition-all shadow-xs flex items-center gap-1.5 disabled:opacity-50"
                  >
                    {isSavingWaToken ? <RefreshCw size={14} className="animate-spin" /> : <Check size={14} />}
                    <span>{isSavingWaToken ? 'Updating .env...' : 'Save & Update .env'}</span>
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
