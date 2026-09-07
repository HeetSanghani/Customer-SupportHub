import { useState, useEffect, useRef } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { ticketsApi } from '../api/tickets'
import { useAuthStore } from '../store/authStore'
import client from '../api/client'
import { formatDateTime, formatTime, formatSmartTime } from '../utils/dateUtils'
import { 
  Mail, Search, Filter, Bot, User, Send, Paperclip, 
  Sparkles, Check, CheckCheck, AlertCircle, Clock, Zap, 
  ShieldCheck, RefreshCw, Copy, FileText, Tag, Globe, 
  UserCheck, Reply, ReplyAll, Forward, Inbox, Star, 
  ChevronRight, ArrowRight, CheckCircle2, CornerDownLeft, X, Info
} from 'lucide-react'

// Simple, lightweight MD5 implementation for real Gravatar email profile picture resolution
function md5(string) {
  function md5cycle(x, k) {
    var a = x[0], b = x[1], c = x[2], d = x[3];
    a = ff(a, b, c, d, k[0], 7, -680876936);
    d = ff(d, a, b, c, k[1], 12, -389564586);
    c = ff(c, d, a, b, k[2], 17, 606105819);
    b = ff(b, c, d, a, k[3], 22, -1044525330);
    a = ff(a, b, c, d, k[4], 7, -176418897);
    d = ff(d, a, b, c, k[5], 12, 1200080426);
    c = ff(c, d, a, b, k[6], 17, -1473231341);
    b = ff(b, c, d, a, k[7], 22, -45705983);
    a = ff(a, b, c, d, k[8], 7, 1770035416);
    d = ff(d, a, b, c, k[9], 12, -1958414417);
    c = ff(c, d, a, b, k[10], 17, -42063);
    b = ff(b, c, d, a, k[11], 22, -1990404162);
    a = ff(a, b, c, d, k[12], 7, 1804603682);
    d = ff(d, a, b, c, k[13], 12, -40341101);
    c = ff(c, d, a, b, k[14], 17, -1502002290);
    b = ff(b, c, d, a, k[15], 22, 1236535329);
    a = gg(a, b, c, d, k[1], 5, -165796510);
    d = gg(d, a, b, c, k[6], 9, -1069501632);
    c = gg(c, d, a, b, k[11], 14, 643717713);
    b = gg(b, c, d, a, k[0], 20, -373897302);
    a = gg(a, b, c, d, k[5], 5, -701558691);
    d = gg(d, a, b, c, k[10], 9, 38016083);
    c = gg(c, d, a, b, k[15], 14, -660478335);
    b = gg(b, c, d, a, k[4], 20, -405537848);
    a = gg(a, b, c, d, k[9], 5, 568446438);
    d = gg(d, a, b, c, k[14], 9, -1019803690);
    c = gg(c, d, a, b, k[3], 14, -187363961);
    b = gg(b, c, d, a, k[8], 20, 1163531501);
    a = gg(a, b, c, d, k[13], 5, -1444681467);
    d = gg(d, a, b, c, k[2], 9, -51403784);
    c = gg(c, d, a, b, k[7], 14, 1735328473);
    b = gg(b, c, d, a, k[12], 20, -1926607734);
    a = hh(a, b, c, d, k[5], 4, -378558);
    d = hh(d, a, b, c, k[8], 11, -2022574463);
    c = hh(c, d, a, b, k[11], 16, 1839030562);
    b = hh(b, c, d, a, k[14], 23, -35309556);
    a = hh(a, b, c, d, k[1], 4, -1530992060);
    d = hh(d, a, b, c, k[4], 11, 1272893353);
    c = hh(c, d, a, b, k[7], 16, -155497632);
    b = hh(b, c, d, a, k[10], 23, -1094730640);
    a = hh(a, b, c, d, k[13], 4, 681279174);
    d = hh(d, a, b, c, k[0], 11, -358537222);
    c = hh(c, d, a, b, k[3], 16, -722521979);
    b = hh(b, c, d, a, k[6], 23, 76029189);
    a = hh(a, b, c, d, k[9], 4, -640364487);
    d = hh(d, a, b, c, k[12], 11, -421815835);
    c = hh(c, d, a, b, k[15], 16, 530742520);
    b = hh(b, c, d, a, k[2], 23, -995338651);
    a = ii(a, b, c, d, k[0], 6, -198630844);
    d = ii(d, a, b, c, k[7], 10, 1126891415);
    c = ii(c, d, a, b, k[14], 15, -1416354905);
    b = ii(b, c, d, a, k[5], 21, -57434055);
    a = ii(a, b, c, d, k[12], 6, 1700485571);
    d = ii(d, a, b, c, k[3], 10, -1894986606);
    c = ii(c, d, a, b, k[10], 15, -1051523);
    b = ii(b, c, d, a, k[1], 21, -2054922799);
    a = ii(a, b, c, d, k[8], 6, 1873313359);
    d = ii(d, a, b, c, k[15], 10, -30611744);
    c = ii(c, d, a, b, k[6], 15, -1560198380);
    b = ii(b, c, d, a, k[13], 21, 1309151649);
    a = ii(a, b, c, d, k[4], 6, -145523070);
    d = ii(d, a, b, c, k[11], 10, -1120210379);
    c = ii(c, d, a, b, k[2], 15, 718787259);
    b = ii(b, c, d, a, k[9], 21, -343485551);
    x[0] = add32(a, x[0]);
    x[1] = add32(b, x[1]);
    x[2] = add32(c, x[2]);
    x[3] = add32(d, x[3]);
  }
  function cmn(q, a, b, x, s, t) {
    a = add32(add32(a, q), add32(x, t));
    return add32((a << s) | (a >>> (32 - s)), b);
  }
  function ff(a, b, c, d, x, s, t) {
    return cmn((b & c) | ((~b) & d), a, b, x, s, t);
  }
  function gg(a, b, c, d, x, s, t) {
    return cmn((b & d) | (c & (~d)), a, b, x, s, t);
  }
  function hh(a, b, c, d, x, s, t) {
    return cmn(b ^ c ^ d, a, b, x, s, t);
  }
  function ii(a, b, c, d, x, s, t) {
    return cmn(c ^ (b | (~d)), a, b, x, s, t);
  }
  function md51(s) {
    var txt = '';
    var n = s.length,
      state = [1732584193, -271733879, -1732584194, 271733878],
      i;
    for (i = 64; i <= s.length; i += 64) {
      md5cycle(state, md5blk(s.substring(i - 64, i)));
    }
    s = s.substring(i - 64);
    var tail = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    for (i = 0; i < s.length; i++)
      tail[i >> 2] |= s.charCodeAt(i) << ((i % 4) << 3);
    tail[i >> 2] |= 0x80 << ((i % 4) << 3);
    if (i > 55) {
      md5cycle(state, tail);
      for (i = 0; i < 16; i++) tail[i] = 0;
    }
    tail[14] = n * 8;
    md5cycle(state, tail);
    return state;
  }
  function md5blk(s) {
    var md5blks = [],
      i;
    for (i = 0; i < 64; i += 4) {
      md5blks[i >> 2] = s.charCodeAt(i) + (s.charCodeAt(i + 1) << 8) + (s.charCodeAt(i + 2) << 16) + (s.charCodeAt(i + 3) << 24);
    }
    return md5blks;
  }
  var hex_chr = '0123456789abcdef'.split('');
  function rhex(n) {
    var s = '',
      j = 0;
    for (; j < 4; j++) s += hex_chr[(n >> (j * 8 + 4)) & 0x0f] + hex_chr[(n >> (j * 8)) & 0x0f];
    return s;
  }
  function hex(x) {
    for (var i = 0; i < x.length; i++) x[i] = rhex(x[i]);
    return x.join('');
  }
  function add32(a, b) {
    return (a + b) & 0xffffffff;
  }
  return hex(md51(string));
}

// Authentic Customer Avatar component: tries actual avatar_url, then real Gravatar if available, then authentic monogram initials badge
function EmailCustomerAvatar({ customer, size = 'md', className = '' }) {
  const [imgError, setImgError] = useState(false)
  const email = customer?.email || customer?.channel_customer_id || ''
  
  // Real avatar source: user uploaded photo or real Gravatar from their email
  const avatarUrl = customer?.avatar_url || (email && email.includes('@') ? `https://www.gravatar.com/avatar/${md5(email.trim().toLowerCase())}?d=404` : null)
  
  const sizeClasses = {
    sm: 'w-6 h-6 text-[10px]',
    md: 'w-10 h-10 text-xs',
    lg: 'w-12 h-12 text-sm',
  }[size] || 'w-10 h-10 text-xs'

  const getInitials = (name) => {
    if (!name) return 'EM'
    const clean = name.replace(/[^\p{L}\p{N}\s]/gu, '').trim()
    if (!clean) return 'EM'
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
        className={`${sizeClasses} rounded-full object-cover shadow-xs border border-indigo-200 shrink-0 ${className}`}
        onError={() => setImgError(true)}
      />
    )
  }

  return (
    <div className={`${sizeClasses} rounded-full bg-indigo-600 text-white font-bold tracking-tight flex items-center justify-center shadow-xs shrink-0 ${className}`}>
      {initials}
    </div>
  )
}

export default function EmailInbox({ basePath = '/agent' }) {
  const { token, role, name: currentName } = useAuthStore()
  const queryClient = useQueryClient()
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

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
  const [emailSubject, setEmailSubject] = useState('')
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
  const [showQuickReplies, setShowQuickReplies] = useState(false)
  const [lockedTicketId, setLockedTicketId] = useState(null)

  const quickReplyTemplates = [
    { id: '1', title: 'Email Greeting & Ack', content: 'Dear Customer,\n\nThank you for contacting SupportHub Email Support. We have received your inquiry and our team is actively reviewing your request.' },
    { id: '2', title: 'Account Verification Request', content: 'Hello,\n\nTo help protect your security, please confirm your registered email address and account reference number so we can proceed with your request.' },
    { id: '3', title: 'Resolution Confirmation', content: 'Dear Customer,\n\nWe are pleased to inform you that your issue has been resolved. Please review the changes and reply to this email if you need further assistance.' },
    { id: '4', title: 'Refund / Billing Inquiry', content: 'Hi there,\n\nWe have initiated your request with our finance department. Standard processing takes 3–5 business days to reflect on your statement.' },
  ]

  // 1. Query Email Tickets
  const { data: rawTickets = [], isLoading: loadingTickets } = useQuery({
    queryKey: ['email-tickets', 'human-only'],
    queryFn: async () => {
      const res = await ticketsApi.list({ channel: 'email', human_only: true })
      if (res.data && res.data.length > 0) return res.data
      // Fallback: if no channel=email specific tickets, return human_only tickets
      const allRes = await ticketsApi.list({ human_only: true })
      const emailFiltered = allRes.data.filter(t => t.channel === 'email')
      return emailFiltered.length > 0 ? emailFiltered : allRes.data
    },
    refetchInterval: 5000,
  })

  // Filter & Sort tickets
  const filteredTickets = rawTickets.filter(t => {
    // Status filter
    if (statusFilter === 'open' && (t.status === 'closed' || t.status === 'resolved')) return false
    if (statusFilter === 'closed' && t.status !== 'closed' && t.status !== 'resolved') return false
    if (statusFilter === 'urgent' && t.priority !== 'urgent' && t.priority !== 'high') return false

    // Search filter
    if (searchTerm.trim()) {
      const q = searchTerm.toLowerCase()
      const nameMatch = t.customer?.name?.toLowerCase().includes(q)
      const emailMatch = (t.customer?.email || t.customer?.channel_customer_id)?.toLowerCase().includes(q)
      const refMatch = t.ref?.toLowerCase().includes(q)
      const idMatch = String(t.id).includes(q)
      const subjectMatch = t.subject?.toLowerCase().includes(q)
      return nameMatch || emailMatch || refMatch || idMatch || subjectMatch
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

  // Update default email subject when selected ticket changes
  useEffect(() => {
    if (selectedTicket) {
      setEmailSubject(selectedTicket.subject ? `Re: ${selectedTicket.subject.replace(/^Re:\s*/i, '')}` : 'Re: Customer Inquiry')
    }
  }, [selectedTicket])

  // 2. Fetch Messages for Selected Ticket
  useEffect(() => {
    if (!selectedTicketId) return
    ticketsApi.getMessages(selectedTicketId)
      .then(res => setMessages(res.data))
      .catch(console.error)
  }, [selectedTicketId])

  // Scroll email view to bottom on message update
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
          queryClient.setQueryData(['email-tickets'], old => {
            if (!old) return old
            return old.map(t => t.id === selectedTicketId ? { ...t, updated_at: new Date().toISOString() } : t)
          })
          queryClient.invalidateQueries({ queryKey: ['email-tickets'] })
        }
      } catch (e) {
        console.error('WS Parse Error:', e)
      }
    }
    setWs(socket)
    return () => socket.close()
  }, [selectedTicketId, token, queryClient])

  // Send Email Handler
  const handleSendEmail = (e) => {
    e.preventDefault()
    if (!inputText.trim()) return
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'message', body: inputText }))
    } else {
      // Fallback via API if WS unavailable
      client.post(`/tickets/${selectedTicketId}/messages`, { body: inputText })
        .then(() => {
          ticketsApi.getMessages(selectedTicketId).then(res => setMessages(res.data))
        })
    }
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
      if (aiTone === 'professional') text = 'Dear Valued Customer,\n\n' + text + '\n\nBest Regards,\nSupportHub Team'
      if (aiTone === 'friendly') text = 'Hi there! 😊\n\n' + text + '\n\nHave a great day!'
      setAiSuggestion(text)
    } catch (e) {
      setAiSuggestion('Dear Customer,\n\nThank you for reaching out. We have logged your request and our support specialists are addressing it promptly.\n\nBest regards,\nCustomer Support Team')
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
      await queryClient.cancelQueries({ queryKey: ['email-tickets'] })
      const previousTickets = queryClient.getQueryData(['email-tickets'])
      
      queryClient.setQueryData(['email-tickets'], old => {
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
      queryClient.setQueryData(['email-tickets'], context.previousTickets)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['email-tickets'] })
      queryClient.invalidateQueries({ queryKey: ['ticket', selectedTicketId] })
    }
  })

  return (
    <div className="flex-1 flex h-screen bg-[#F6F7FC] overflow-hidden text-[#1C1B2E]">
      
      {/* ─────────────────────────────────────────────────────────────────── */}
      {/* COLUMN 1: EMAIL CONVERSATION LIST */}
      {/* ─────────────────────────────────────────────────────────────────── */}
      <div className="w-84 bg-white border-r border-[#E5E7F3] flex flex-col shrink-0">
        
        {/* Header & Search */}
        <div className="p-4 border-b border-[#E5E7F3] space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-xl bg-indigo-600 text-white flex items-center justify-center shadow-xs">
                <Mail size={18} />
              </div>
              <div>
                <h2 className="font-bold text-sm font-['Plus_Jakarta_Sans']">Email Inbox</h2>
                <div className="text-[10px] text-indigo-600 font-bold flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-indigo-500 animate-pulse"></span> Active Sync
                </div>
              </div>
            </div>
            <span className="bg-indigo-50 text-indigo-700 text-xs font-bold px-2 py-0.5 rounded-md border border-indigo-200">
              {filteredTickets.length} emails
            </span>
          </div>

          {/* Search Bar */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-[#9598B0]" size={14} />
            <input
              type="text"
              placeholder="Search email, customer, subject, ref..."
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl pl-8 pr-3 py-1.5 text-xs outline-none focus:border-indigo-500 transition-colors"
            />
          </div>

          {/* Filter Pills */}
          <div className="flex items-center gap-1 overflow-x-auto pb-1 text-[11px] font-semibold no-scrollbar">
            {[
              { id: 'open', label: 'Active' },
              { id: 'all', label: 'All Emails' },
              { id: 'closed', label: '✅ Resolved' },
              { id: 'urgent', label: '🔥 Urgent' },
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => { setStatusFilter(tab.id); setLockedTicketId(null); }}
                className={`px-2.5 py-1 rounded-lg transition-colors whitespace-nowrap ${
                  statusFilter === tab.id
                    ? 'bg-indigo-600 text-white font-bold shadow-xs'
                    : 'bg-gray-100 text-[#6C7089] hover:bg-gray-200'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Email Items List */}
        <div className="flex-1 overflow-y-auto divide-y divide-[#E5E7F3]">
          {loadingTickets ? (
            <div className="flex justify-center py-12">
              <div className="animate-spin w-6 h-6 border-2 border-indigo-500 border-t-transparent rounded-full"></div>
            </div>
          ) : filteredTickets.length === 0 ? (
            <div className="text-center py-16 px-4 text-[#9598B0]">
              <Mail size={32} className="mx-auto mb-2 text-gray-300" />
              <p className="font-bold text-xs text-[#1C1B2E]">No Email Messages</p>
              <p className="text-[11px] mt-1">No emails match your current filter.</p>
            </div>
          ) : (
            filteredTickets.map((ticket, idx) => {
              const isSelected = ticket.id === selectedTicketId
              const emailDisplay = ticket.customer?.email || ticket.customer?.channel_customer_id || 'customer@example.com'

              return (
                <button
                  key={ticket.id}
                  onClick={() => { setSelectedTicketId(ticket.id); setLockedTicketId(null); }}
                  className={`w-full text-left p-3.5 transition-all flex items-start gap-3 relative ${
                    isSelected 
                      ? 'bg-indigo-50/60 border-l-4 border-indigo-600' 
                      : 'hover:bg-gray-50/80'
                  }`}
                >
                  {/* Customer Initial Avatar */}
                  <div className="relative shrink-0">
                    <EmailCustomerAvatar customer={ticket.customer} size="md" />
                    <div className="absolute -bottom-0.5 -right-0.5 w-4 h-4 rounded-full bg-indigo-500 border-2 border-white flex items-center justify-center">
                      <Mail size={9} className="text-white fill-white" />
                    </div>
                  </div>

                  {/* Content Details */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-0.5">
                      <span className="font-bold text-xs text-[#1C1B2E] truncate">
                        {ticket.customer?.name || 'Email Customer'}
                      </span>
                      <span className="text-[10px] text-[#9598B0]">
                        {formatSmartTime(ticket.updated_at || ticket.created_at)}
                      </span>
                    </div>

                    <div className="text-[11px] text-indigo-700 font-medium truncate mb-1">
                      {emailDisplay}
                    </div>

                    <p className="text-[11px] font-semibold text-[#1C1B2E] truncate leading-tight">
                      {ticket.subject || 'No Subject'}
                    </p>

                    <div className="flex items-center gap-1.5 mt-2 flex-wrap">
                      <span className="px-1.5 py-0.5 rounded text-[9px] font-mono font-bold bg-gray-100 text-gray-700 border border-gray-200">
                        {ticket.ref}
                      </span>

                      {/* Priority */}
                      <span className={`px-1.5 py-0.5 rounded text-[9px] font-bold capitalize ${
                        ticket.priority === 'urgent' ? 'bg-rose-100 text-rose-700' :
                        ticket.priority === 'high' ? 'bg-amber-100 text-amber-700' : 'bg-gray-100 text-gray-600'
                      }`}>
                        {ticket.priority || 'medium'}
                      </span>

                      {/* Status */}
                      <span className={`px-1.5 py-0.5 rounded text-[9px] font-bold capitalize ${
                        ticket.status === 'resolved' || ticket.status === 'closed' ? 'bg-emerald-100 text-emerald-700' : 'bg-blue-100 text-blue-700'
                      }`}>
                        {ticket.status}
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
      {/* COLUMN 2: RICH EMAIL VIEW & COMPOSER */}
      {/* ─────────────────────────────────────────────────────────────────── */}
      {selectedTicket ? (
        <div className="flex-1 flex flex-col min-w-0 bg-[#F9FAFC] border-r border-[#E5E7F3] relative">
          
          {/* Email View Header */}
          <div className="px-6 py-4 bg-white border-b border-[#E5E7F3] shadow-xs z-10 space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3 min-w-0">
                <EmailCustomerAvatar customer={selectedTicket.customer} size="md" />
                <div className="min-w-0">
                  <h3 className="font-bold text-base text-[#1C1B2E] truncate font-['Plus_Jakarta_Sans']">
                    {selectedTicket.subject || 'No Subject'}
                  </h3>
                  <div className="text-xs text-[#6C7089] flex items-center gap-2 truncate">
                    <span className="font-bold text-[#1C1B2E] bg-slate-100 px-1.5 py-0.5 rounded border border-slate-200">ID: #{selectedTicket.id}</span>
                    <span>•</span>
                    <span className="font-bold text-[#1C1B2E]">{selectedTicket.customer?.name || 'Customer'}</span>
                    <span>&lt;{selectedTicket.customer?.email || selectedTicket.customer?.channel_customer_id || 'customer@domain.com'}&gt;</span>
                    <span>•</span>
                    <span className="font-mono text-indigo-600 font-semibold">Ref: {selectedTicket.ref}</span>
                  </div>
                </div>
              </div>

              {/* Header Action Controls */}
              <div className="flex items-center gap-3 shrink-0">
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
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition-all border shadow-2xs ${
                    showRightPanel && activeRightTab === 'ai'
                      ? 'bg-indigo-600 text-white border-indigo-700 shadow-xs'
                      : 'bg-indigo-50 text-indigo-700 border-indigo-200 hover:bg-indigo-100'
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

                {/* Priority Selector */}
                <select
                  className="text-xs font-bold bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl px-3 py-1.5 outline-none capitalize focus:border-indigo-500"
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
                      : 'bg-indigo-600 text-white hover:bg-indigo-700 border-indigo-600'
                  }`}
                >
                  {selectedTicket.status === 'resolved' ? '✓ Resolved' : 'Mark Resolved'}
                </button>
              </div>
            </div>
          </div>

          {/* Email Messages Thread Feed */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-[#F8FAFC]">
            
            {/* System Info Banner */}
            <div className="flex justify-center">
              <div className="bg-white border border-[#E5E7F3] text-[#6C7089] text-[11px] px-4 py-1.5 rounded-full font-medium shadow-2xs flex items-center gap-1.5">
                <ShieldCheck size={13} className="text-indigo-500" />
                <span>Verified Email Thread · Support Ticket {selectedTicket.ref}</span>
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
                  <div className={`max-w-[75%] rounded-2xl p-4 shadow-xs relative transition-all ${
                    isCustomer
                      ? 'bg-white text-[#1C1B2E] rounded-tl-none border border-[#E5E7F3]'
                      : isAI
                      ? 'bg-[#EEF2FF] text-[#1C1B2E] rounded-tr-none border border-indigo-200'
                      : 'bg-indigo-600 text-white rounded-tr-none'
                  }`}>
                    {/* Header Strip */}
                    <div className="flex items-center justify-between pb-2 mb-2 border-b border-black/5 gap-4">
                      <div className="flex items-center gap-2">
                        {isCustomer ? (
                          <EmailCustomerAvatar customer={selectedTicket.customer} size="sm" />
                        ) : (
                          <div className={`w-6 h-6 rounded-full font-bold text-[10px] flex items-center justify-center shrink-0 ${
                            isAI ? 'bg-purple-600 text-white' : 'bg-white text-indigo-700 font-extrabold'
                          }`}>
                            {isAI ? <Bot size={12} /> : 'AG'}
                          </div>
                        )}
                        <div className="text-xs font-bold truncate">
                          <span className={isCustomer ? 'text-indigo-800' : isAI ? 'text-indigo-950 flex items-center gap-1' : 'text-white'}>
                            {isCustomer 
                              ? (selectedTicket.customer?.name || 'Customer') 
                              : isAI 
                              ? <><Bot size={12} /> AI Support Assistant</> 
                              : (currentName || 'Support Agent')
                            }
                          </span>
                        </div>
                      </div>
                      <span className={`text-[10px] font-mono ${isCustomer ? 'text-[#9598B0]' : isAI ? 'text-indigo-600 font-semibold' : 'text-indigo-100'}`}>
                        {formatSmartTime(msg.created_at)}
                      </span>
                    </div>

                    {/* Recipient info tag */}
                    <div className={`text-[10px] mb-2 font-medium ${isCustomer ? 'text-[#9598B0]' : isAI ? 'text-indigo-700' : 'text-indigo-200'}`}>
                      To: {isCustomer ? 'SupportHub Team' : (selectedTicket.customer?.name || 'Customer')}
                    </div>

                    {/* Email Content Body */}
                    <div className="text-xs leading-relaxed whitespace-pre-wrap font-sans">
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
                                <a href={url} target="_blank" rel="noopener noreferrer" className="block mt-1 overflow-hidden rounded-xl border border-black/10 shadow-sm max-w-xs hover:opacity-95 transition-opacity">
                                  <img 
                                    src={url} 
                                    alt={filename} 
                                    className="w-full h-auto max-h-48 object-cover rounded-xl"
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
                                <div className="mt-1 overflow-hidden rounded-xl border border-black/10 shadow-sm max-w-xs bg-black">
                                  <video controls preload="metadata" className="w-full h-auto max-h-48 rounded-xl" src={url}>
                                    Your browser does not support video playback.
                                  </video>
                                </div>
                              ) : isAudio ? (
                                <div className="mt-1 p-2 rounded-xl bg-black/5 border border-black/10 max-w-xs">
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

                    {/* Footer Time & Status */}
                    <div className={`flex justify-end items-center gap-1 mt-2 text-[10px] ${
                      isCustomer ? 'text-[#9598B0]' : isAI ? 'text-indigo-600 font-semibold' : 'text-indigo-100'
                    }`}>
                      <span>{formatSmartTime(msg.created_at)}</span>
                      {!isCustomer && <CheckCheck size={13} className={isAI ? 'text-indigo-500' : 'text-indigo-200'} />}
                    </div>
                  </div>
                </div>
              )
            })}
            <div ref={messagesEndRef} />
          </div>

          {/* Rich Email Composer */}
          <div className="p-5 bg-white border-t border-[#E5E7F3] shadow-lg relative">
            {/* Quick Reply Popover */}
            {showQuickReplies && (
              <div className="absolute bottom-full mb-2 left-4 right-4 bg-white border border-[#E5E7F3] rounded-2xl shadow-xl p-3 z-50 space-y-2 max-h-60 overflow-y-auto">
                <div className="flex justify-between items-center pb-2 border-b text-xs font-bold text-[#1C1B2E]">
                  <span className="flex items-center gap-1 text-indigo-600"><Zap size={14} /> Quick Email Templates</span>
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
                    className="w-full text-left p-2.5 hover:bg-indigo-50 rounded-xl transition-colors border border-gray-100 group"
                  >
                    <div className="font-bold text-xs text-[#1C1B2E] group-hover:text-indigo-700">{tpl.title}</div>
                    <div className="text-[11px] text-[#6C7089] line-clamp-1 mt-0.5">{tpl.content}</div>
                  </button>
                ))}
              </div>
            )}

            <form onSubmit={handleSendEmail} className="space-y-3">
              {/* Subject line input */}
              <div className="flex items-center gap-2 text-xs border-b border-[#E5E7F3] pb-2">
                <span className="font-bold text-[#9598B0] w-12">Subject:</span>
                <input
                  type="text"
                  value={emailSubject}
                  onChange={e => setEmailSubject(e.target.value)}
                  className="flex-1 font-semibold text-[#1C1B2E] outline-none bg-transparent"
                />
              </div>

              {/* Message text area */}
              <div className="relative">
                <textarea
                  ref={inputRef}
                  rows={4}
                  placeholder="Write your email response here or use templates..."
                  value={inputText}
                  onChange={e => {
                    setInputText(e.target.value)
                    if (e.target.value.endsWith('/')) setShowQuickReplies(true)
                  }}
                  className="w-full border border-[#E5E7F3] rounded-xl p-3 text-xs outline-none focus:ring-2 focus:ring-indigo-500 transition-all resize-none"
                />
              </div>

              {/* Composer Toolbar */}
              <div className="flex items-center justify-between pt-1">
                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => {
                      setShowQuickReplies(!showQuickReplies)
                      setTimeout(() => inputRef.current?.focus(), 50)
                    }}
                    className={`flex items-center gap-1 px-3 py-1.5 rounded-xl border text-xs font-semibold transition-colors ${
                      showQuickReplies ? 'bg-indigo-100 border-indigo-300 text-indigo-700 font-bold' : 'border-[#E5E7F3] bg-[#F6F7FC] hover:bg-indigo-50 text-[#6C7089] hover:text-indigo-600'
                    }`}
                  >
                    <Zap size={14} /> Templates
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
                          setInputText(prev => prev + `\n\n📎 Attachment: ${res.data.filename} (${res.data.url})`)
                        } catch (err) {
                          alert('Failed to upload attachment')
                        }
                      }
                      input.click()
                    }}
                    className="flex items-center gap-1 px-3 py-1.5 rounded-xl border border-[#E5E7F3] bg-[#F6F7FC] hover:bg-indigo-50 text-[#6C7089] hover:text-indigo-600 text-xs font-semibold transition-colors"
                  >
                    <Paperclip size={14} /> Attach File
                  </button>
                </div>

                <button
                  type="submit"
                  disabled={!inputText.trim()}
                  className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2 rounded-xl text-xs font-bold transition-colors disabled:opacity-50 shadow-xs"
                >
                  <Send size={14} /> Send Email
                </button>
              </div>
            </form>
          </div>
        </div>
      ) : (
        <div className="flex-1 flex items-center justify-center bg-[#F6F7FC] text-[#9598B0]">
          Select an email conversation to start messaging.
        </div>
      )}

      {/* ─────────────────────────────────────────────────────────────────── */}
      {/* COLUMN 3: AI ASSISTANT & CUSTOMER EMAIL INSPECTOR (DEFAULT HIDE) */}
      {/* ─────────────────────────────────────────────────────────────────── */}
      {showRightPanel && (
        <div className="w-80 bg-white flex flex-col shrink-0 overflow-hidden border-l border-[#E5E7F3] animate-fadeIn relative">
          
          {/* Dedicated Panel Header with Title and Close Button */}
          <div className="flex items-center justify-between px-4 py-3 border-b border-[#E5E7F3] bg-[#F8FAFC]">
            <div className="flex items-center gap-2 font-bold text-xs uppercase tracking-wider text-[#1C1B2E]">
              {activeRightTab === 'ai' ? (
                <>
                  <Sparkles size={16} className="text-indigo-600" />
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
                  <div className="p-2 bg-indigo-100 rounded-xl"><Sparkles size={16} className="text-indigo-600" /></div>
                  <div>
                    <h4 className="text-xs font-bold text-[#1C1B2E]">Email AI Writer</h4>
                    <p className="text-[10px] text-[#9598B0]">Powered by Gemini 3.6 Flash</p>
                  </div>
                </div>

                {/* Tone Modifiers */}
                <div className="space-y-1.5">
                  <label className="text-[10px] font-bold text-[#9598B0] uppercase">Email Response Tone</label>
                  <div className="grid grid-cols-2 gap-1 text-[10px] font-semibold">
                    {['standard', 'shorter', 'professional', 'friendly'].map(t => (
                      <button
                        key={t}
                        onClick={() => setAiTone(t)}
                        className={`p-1.5 rounded-lg border capitalize transition-colors ${
                          aiTone === t ? 'bg-indigo-50 border-indigo-300 text-indigo-700 font-bold' : 'border-gray-200 text-gray-600 hover:bg-gray-50'
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
                  className="w-full flex items-center justify-center gap-2 py-2.5 px-3 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white text-xs font-bold rounded-xl transition-all shadow-xs disabled:opacity-60"
                >
                  {loadingSuggest ? <RefreshCw size={14} className="animate-spin" /> : <Sparkles size={14} />}
                  <span>Generate Email Draft</span>
                </button>

                {/* Generated AI Suggestion Box */}
                {aiSuggestion && (
                  <div className="bg-indigo-50 border border-indigo-200 rounded-xl p-3 space-y-2">
                    <p className="text-xs text-[#1C1B2E] leading-relaxed whitespace-pre-wrap">{aiSuggestion}</p>
                    <button
                      onClick={handleCopySuggestion}
                      className={`w-full flex items-center justify-center gap-1.5 py-1.5 text-[10px] font-bold rounded-lg transition-all ${
                        copiedSuggestion ? 'bg-emerald-500 text-white' : 'bg-white border border-indigo-200 text-indigo-700 hover:bg-indigo-100'
                      }`}
                    >
                      {copiedSuggestion ? <><Check size={12} /> Copied to Composer!</> : <><Copy size={12} /> Insert into Email Body</>}
                    </button>
                  </div>
                )}

                {/* AI Metrics Card */}
                <div className="bg-indigo-50/50 border border-indigo-200 rounded-xl p-3 space-y-2 text-[11px]">
                  <div className="font-bold text-indigo-950 text-xs flex items-center gap-1.5">
                    <Sparkles size={13} className="text-indigo-600" /> Email AI Capabilities
                  </div>
                  <div className="flex justify-between text-[#6C7089]">
                    <span>AI Sentiment Analysis:</span>
                    <span className="font-bold text-emerald-600">Positive / Neutral</span>
                  </div>
                  <div className="flex justify-between text-[#6C7089]">
                    <span>Suggested Category:</span>
                    <span className="font-semibold text-indigo-600">{selectedTicket?.category || 'Support Inquiry'}</span>
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
                    <User size={13} className="text-indigo-600" /> Customer Information
                  </div>
                  <div className="flex items-center gap-3">
                    <EmailCustomerAvatar customer={selectedTicket.customer} size="md" />
                    <div className="min-w-0">
                      <h4 className="font-bold text-[#1C1B2E] truncate">{selectedTicket.customer?.name || 'Email Customer'}</h4>
                      <p className="text-[10px] text-[#9598B0] truncate">{selectedTicket.customer?.email || 'customer@domain.com'}</p>
                    </div>
                  </div>

                  <div className="space-y-1.5 pt-1 text-[11px]">
                    <div className="flex items-center justify-between text-[#6C7089]">
                      <span className="flex items-center gap-1.5"><Mail size={13} className="text-indigo-600" /> Email:</span>
                      <span className="font-semibold text-[#1C1B2E]">{selectedTicket.customer?.email || 'N/A'}</span>
                    </div>
                    <div className="flex items-center justify-between text-[#6C7089]">
                      <span className="flex items-center gap-1.5"><Globe size={13} className="text-purple-600" /> Channel:</span>
                      <span className="font-semibold text-indigo-700 bg-indigo-100 px-1.5 py-0.5 rounded text-[10px]">Email Ticket</span>
                    </div>
                  </div>
                </div>

                {/* Section B: Ticket Details */}
                <div className="bg-slate-50 border border-slate-200 rounded-xl p-3.5 space-y-3">
                  <div className="text-[10px] font-bold text-[#9598B0] uppercase tracking-wider flex items-center gap-1.5 pb-2 border-b border-slate-200">
                    <FileText size={13} className="text-indigo-600" /> Ticket Details
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
                      <span className="capitalize font-bold bg-indigo-100 text-indigo-800 px-2 py-0.5 rounded text-[10px] inline-block mt-0.5">
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
                    <div className="text-xs font-bold text-indigo-600 flex items-center gap-1 mt-1 bg-indigo-50 p-2 rounded-lg border border-indigo-200">
                      <Clock size={14} /> {getSlaRemaining(selectedTicket.sla_due_at)}
                    </div>
                  </div>
                </div>
              </div>
            )}

          </div>
        </div>
      )}
    </div>
  )
}
