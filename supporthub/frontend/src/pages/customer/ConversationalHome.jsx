import { useState, useEffect, useRef, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { ticketsApi } from '../../api/tickets'
import { useAuthStore } from '../../store/authStore'
import { authApi } from '../../api/auth'
import client from '../../api/client'
import { formatSmartTime } from '../../utils/dateUtils'
import {
  Plus, Send, Star, X, HelpCircle, CreditCard,
  Wrench, User as UserIcon, MessageSquare, Sparkles, AlertTriangle,
  RefreshCw, ShoppingBag, Truck, CheckCircle2, Clock, Zap, ChevronRight,
  RotateCcw, DollarSign, PackageSearch, ArrowLeft, ShieldAlert,
  PanelLeftClose, PanelLeftOpen
} from 'lucide-react'

// ── CsatWidget ────────────────────────────────────────────────
function CsatWidget({ ticketId }) {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [rating, setRating] = useState(0)
  const [hover, setHover] = useState(0)
  const [comment, setComment] = useState('')
  const [submitted, setSubmitted] = useState(false)

  useEffect(() => { setRating(0); setHover(0); setComment(''); setSubmitted(false) }, [ticketId])

  const { data: existing, isLoading } = useQuery({
    queryKey: ['csat', ticketId],
    queryFn: async () => { const r = await ticketsApi.getCsat(ticketId); return r.data },
    enabled: !!ticketId, staleTime: 0,
  })
  const mut = useMutation({
    mutationFn: d => ticketsApi.submitCsat(ticketId, d),
    onSuccess: () => {
      setSubmitted(true)
      queryClient.invalidateQueries({ queryKey: ['csat', ticketId] })
      queryClient.invalidateQueries({ queryKey: ['my-csat-reviews'] })
    }
  })

  if (isLoading) return null
  const dr = existing?.rating || rating
  const dc = existing?.comment || comment

  if (existing || submitted) return (
    <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-4 text-center space-y-2 animate-fadeIn">
      <div className="flex justify-center gap-1">
        {[1,2,3,4,5].map(s => <Star key={s} size={18} className={s<=dr?'fill-amber-400 text-amber-400':'text-gray-300'} />)}
      </div>
      <p className="text-xs font-bold text-emerald-800">You rated this service {dr}/5 ★</p>
      {dc && <p className="text-[11px] text-emerald-700 italic">"{dc}"</p>}
      <button onClick={() => navigate('/customer/reviews')}
        className="text-[11px] font-bold text-emerald-700 bg-emerald-100 hover:bg-emerald-200 px-3 py-1 rounded-lg transition-colors">
        View in My Reviews →
      </button>
    </div>
  )

  return (
    <form onSubmit={e => { e.preventDefault(); if (rating) mut.mutate({ rating, comment }) }}
      className="bg-indigo-50/80 border border-indigo-100 rounded-2xl p-4 text-center space-y-3 animate-fadeIn">
      <p className="text-xs font-bold text-indigo-900">How satisfied were you with this resolution?</p>
      <div className="flex justify-center gap-1">
        {[1,2,3,4,5].map(s => (
          <button key={s} type="button" onClick={() => setRating(s)}
            onMouseEnter={() => setHover(s)} onMouseLeave={() => setHover(0)}
            className="p-1 transition-transform hover:scale-110">
            <Star size={24} className={(hover||rating)>=s?'fill-amber-400 text-amber-400':'text-gray-300'} />
          </button>
        ))}
      </div>
      {rating > 0 && (
        <div className="space-y-2 max-w-xs mx-auto">
          <input value={comment} onChange={e => setComment(e.target.value)}
            placeholder="Optional comment…"
            className="w-full border border-indigo-200 rounded-xl px-3 py-1.5 text-xs focus:ring-2 focus:ring-indigo-400 outline-none" />
          <button type="submit" disabled={mut.isPending}
            className="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold px-4 py-1.5 rounded-xl transition-colors disabled:opacity-50 shadow-sm">
            {mut.isPending ? 'Submitting…' : 'Submit Feedback'}
          </button>
        </div>
      )}
    </form>
  )
}

function renderFormattedContent(text, isCustomer = false) {
  if (!text) return null

  const lines = text.split('\n')

  return (
    <div className="space-y-1 leading-relaxed">
      {lines.map((line, lineIdx) => {
        const trimmed = line.trim()
        if (!trimmed) {
          return <div key={lineIdx} className="h-1.5" />
        }

        const isBullet = /^[•\-*]\s+/.test(trimmed)
        const lineContent = isBullet ? trimmed.replace(/^[•\-*]\s+/, '') : line

        const parseInline = (str) => {
          const parts = []
          let lastIdx = 0
          const regex = /(\*\*(.*?)\*\*|\*(.*?)\*|`([^`]+)`)/g
          let match

          while ((match = regex.exec(str)) !== null) {
            if (match.index > lastIdx) {
              parts.push(str.substring(lastIdx, match.index))
            }

            if (match[2] !== undefined) {
              parts.push(
                <strong key={match.index} className="font-extrabold text-inherit">
                  {match[2]}
                </strong>
              )
            } else if (match[3] !== undefined) {
              parts.push(
                <em key={match.index} className="italic text-inherit">
                  {match[3]}
                </em>
              )
            } else if (match[4] !== undefined) {
              parts.push(
                <code
                  key={match.index}
                  className={`px-1.5 py-0.5 mx-0.5 rounded font-mono text-[11px] font-bold inline-block border ${
                    isCustomer
                      ? 'bg-white/20 text-white border-white/30'
                      : 'bg-indigo-50 text-indigo-700 border-indigo-200/80'
                  }`}
                >
                  {match[4]}
                </code>
              )
            }
            lastIdx = regex.lastIndex
          }

          if (lastIdx < str.length) {
            parts.push(str.substring(lastIdx))
          }

          return parts.length > 0 ? parts : str
        }

        if (isBullet) {
          return (
            <div key={lineIdx} className="flex items-start gap-2 my-0.5 pl-0.5">
              <span className={`font-bold shrink-0 mt-0.5 text-xs ${isCustomer ? 'text-white' : 'text-indigo-500'}`}>•</span>
              <span className="flex-1">{parseInline(lineContent)}</span>
            </div>
          )
        }

        return (
          <div key={lineIdx} className="leading-relaxed">
            {parseInline(line)}
          </div>
        )
      })}
    </div>
  )
}

// ── MessageBody ────────────────────────────────────────────────
function MessageBody({ msg }) {
  const sType = msg.sender_type || msg.sender_role || msg.sender
  const isCustomer = sType === 'customer'
  const body = msg.body || ''
  const match = body.match(/📎\s*\[Attachment:\s*([^\]]+)\]\(([^)]+)\)/i) ||
                body.match(/📎\s*Attachment:\s*([^\s(]+)\s*\(([^)]+)\)/i)
  if (match) {
    const fn = match[1], rawUrl = match[2]
    const base = (window.location.port==='5173'||window.location.port==='3000') ? 'http://localhost:8000' : ''
    const url = rawUrl.startsWith('http') ? rawUrl : `${base}${rawUrl.startsWith('/')?'':'/'}${rawUrl}`
    const isImg   = /\.(jpg|jpeg|png|gif|webp|svg|bmp)(\?.*)?$/i.test(fn+url) || /(fbsbx|fbcdn|cdninstagram)/i.test(url)
    const isVid   = /\.(mp4|webm|ogg|mov|avi)(\?.*)?$/i.test(fn+url)
    const isAudio = /\.(mp3|wav|ogg|m4a|aac)(\?.*)?$/i.test(fn+url)
    const isPdf   = /\.pdf(\?.*)?$/i.test(fn+url)
    const rest    = body.replace(match[0],'').trim()
    return (
      <div className="space-y-2">
        {isImg && <a href={url} target="_blank" rel="noopener noreferrer" className="block max-w-xs rounded-xl overflow-hidden border border-white/20">
          <img src={url} alt={fn} className="w-full h-auto max-h-48 object-cover" onError={e=>{e.target.style.display='none'}} /></a>}
        {isVid && <div className="max-w-xs rounded-xl overflow-hidden bg-black"><video controls preload="metadata" className="w-full max-h-48" src={url} /></div>}
        {isAudio && <div className="max-w-xs p-2 rounded-xl bg-black/10"><audio controls className="w-full h-8" src={url} /><div className="text-[10px] opacity-70 mt-1 truncate">🎵 {fn}</div></div>}
        {isPdf && <a href={url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 px-3 py-2 bg-rose-50 hover:bg-rose-100 border border-rose-200 text-rose-800 rounded-xl text-xs font-bold">📄 {fn}</a>}
        {!isImg&&!isVid&&!isAudio&&!isPdf && <a href={url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 px-3 py-1.5 bg-black/10 hover:bg-black/20 rounded-xl text-xs font-bold underline">📎 {fn}</a>}
        {rest && <div className="text-sm leading-relaxed">{renderFormattedContent(rest, isCustomer)}</div>}
      </div>
    )
  }
  if (msg.body_html) return <div className="text-sm leading-relaxed prose prose-sm max-w-none" dangerouslySetInnerHTML={{__html:msg.body_html}} />
  return <div className="text-sm leading-relaxed">{renderFormattedContent(body, isCustomer)}</div>
}

// ── LifecycleBanner ───────────────────────────────────────────
function LifecycleBanner({ status, agentName, hasAgent }) {
  if (!status || status === 'open') return null
  const cfg = {
    escalated: {
      bg: hasAgent ? 'bg-emerald-50 border-emerald-200' : 'bg-amber-50 border-amber-200',
      dot: hasAgent ? 'bg-emerald-500' : 'bg-amber-500',
      text: hasAgent ? 'text-emerald-800' : 'text-amber-800',
      label: hasAgent ? `You're chatting with ${agentName || 'a support agent'}.` : "You've been connected to our support team. A human support agent will join shortly."
    },
    resolved: { bg: 'bg-emerald-50 border-emerald-200', dot: 'bg-emerald-500', text: 'text-emerald-800', label: 'Your issue has been resolved. Glad we could help!' },
    closed:   { bg: 'bg-gray-100 border-gray-200', dot: 'bg-gray-400', text: 'text-gray-700', label: 'This conversation is closed.' },
    reopened: { bg: 'bg-blue-50 border-blue-200', dot: 'bg-blue-500', text: 'text-blue-800', label: 'Conversation reopened.' }
  }[status]
  if (!cfg) return null
  return (
    <div className={`mx-4 mt-3 flex items-center gap-2.5 px-4 py-2.5 rounded-2xl border text-xs font-semibold animate-slideDown ${cfg.bg} ${cfg.text}`} role="status">
      <span className={`w-2 h-2 rounded-full animate-pulse ${cfg.dot}`} />
      <span>{cfg.label}</span>
    </div>
  )
}

// ── WSDisconnectBanner ────────────────────────────────────────
function WSDisconnectBanner({ wsStatus, onReconnect }) {
  if (wsStatus === 'connected' || wsStatus === 'connecting') return null
  return (
    <div className="mx-4 mt-2 flex items-center justify-between gap-2 px-3 py-2 bg-rose-50 border border-rose-200 rounded-xl text-xs font-semibold text-rose-700 animate-slideDown" role="alert">
      <div className="flex items-center gap-2"><AlertTriangle size={14} /> Connection lost. Live chat re-establishing…</div>
      <button onClick={onReconnect} className="flex items-center gap-1 bg-rose-100 hover:bg-rose-200 px-2.5 py-1 rounded-lg transition-colors text-xs font-bold">
        <RefreshCw size={12} /> Reconnect
      </button>
    </div>
  )
}

// ── TypingIndicator ───────────────────────────────────────────
function TypingIndicator() {
  return (
    <div className="flex flex-col items-start my-2">
      <div className="bg-[#F1F3F9] border border-[#E2E8F0] rounded-2xl rounded-bl-sm px-4 py-2.5 flex items-center gap-3 shadow-xs">
        <span className="text-xs font-semibold text-[#64748B]">SupportHub AI is typing</span>
        <div className="flex items-center gap-1">
          {[0, 150, 300].map(d => (
            <div key={d} className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: `${d}ms` }} />
          ))}
        </div>
      </div>
    </div>
  )
}

// ── EmptyState: Clean, Conversation-First Initial Screen ─────
function EmptyState({ profile, onQuickAction, sidebarOpen, onToggleSidebar, onNewChat }) {
  const commonQuestions = [
    "Where is my order?",
    "How do I return an item?",
    "How long does delivery take?",
    "What is your refund policy?",
    "Why hasn't my payment gone through?",
    "Can I change my delivery address?"
  ]

  return (
    <div className="relative flex-1 overflow-y-auto px-4 py-8 md:px-12 md:py-12 flex flex-col items-center justify-center w-full animate-fadeIn">
      {/* Collapsed Sidebar Toggle (Floating Top Left) */}
      {!sidebarOpen && (
        <div className="absolute top-4 left-4 z-20 hidden md:flex items-center gap-1.5">
          <button
            onClick={onToggleSidebar}
            className="p-2 rounded-xl text-[#64748B] hover:text-[#0F172A] hover:bg-[#F1F5F9] bg-white border border-[#E2E8F0] transition-all group relative cursor-pointer shadow-2xs"
            title="Open sidebar (Ctrl+B)"
            aria-label="Open sidebar"
          >
            <PanelLeftOpen size={18} />
            <span className="pointer-events-none absolute left-0 top-full mt-1.5 z-50 whitespace-nowrap rounded-lg bg-slate-900/95 backdrop-blur-xs px-2.5 py-1 text-[11px] font-medium text-white opacity-0 shadow-lg transition-all duration-150 group-hover:opacity-100 group-hover:translate-y-0.5">
              Open sidebar <span className="text-[10px] text-slate-400 ml-1">Ctrl+B</span>
            </span>
          </button>
          {onNewChat && (
            <button
              onClick={onNewChat}
              className="p-2 rounded-xl text-[#64748B] hover:text-indigo-600 hover:bg-indigo-50 bg-white border border-[#E2E8F0] hover:border-indigo-200 transition-all group relative cursor-pointer shadow-2xs"
              title="New conversation"
              aria-label="New conversation"
            >
              <Plus size={18} />
              <span className="pointer-events-none absolute left-0 top-full mt-1.5 z-50 whitespace-nowrap rounded-lg bg-slate-900/95 backdrop-blur-xs px-2.5 py-1 text-[11px] font-medium text-white opacity-0 shadow-lg transition-all duration-150 group-hover:opacity-100 group-hover:translate-y-0.5">
                New conversation
              </span>
            </button>
          )}
        </div>
      )}

      {/* AI Assistant Hero */}
      <div className="text-center space-y-3 mb-8">
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-600 to-purple-600 flex items-center justify-center mx-auto shadow-lg shadow-indigo-200">
          <Sparkles size={32} className="text-white" />
        </div>
        <h1 className="text-2xl md:text-3xl font-extrabold text-[#0F172A] tracking-tight">
          SupportHub AI Assistant
        </h1>
        <p className="text-lg font-bold text-indigo-600">
          How can we help?
        </p>
        <p className="text-xs md:text-sm text-[#64748B] max-w-lg mx-auto">
          Ask about orders, delivery, returns, refunds, payments, products, or anything else.
        </p>
      </div>

      {/* COMMON QUESTIONS */}
      <div className="w-full space-y-3">
        <div className="text-[11px] font-extrabold text-[#94A3B8] uppercase tracking-wider text-center">
          Common Questions
        </div>
        <div className="flex flex-wrap gap-2 justify-center">
          {commonQuestions.map(q => (
            <button
              key={q}
              onClick={() => onQuickAction(q)}
              className="px-4 py-2 bg-white border border-[#E2E8F0] hover:border-indigo-400 hover:bg-indigo-50/50 rounded-full text-xs font-semibold text-[#334155] hover:text-indigo-700 transition-all shadow-2xs"
            >
              "{q}"
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

// ── ChatView: Active Ticket Conversation ──────────────────────
function ChatView({ ticketId, onBack, onQuickAction, sidebarOpen, onToggleSidebar, onNewChat }) {
  const token = useAuthStore(s => s.token)
  const queryClient = useQueryClient()
  const messagesEndRef = useRef(null)
  const wsRef = useRef(null)
  const [msgs, setMsgs] = useState([])
  const [typing, setTyping] = useState(false)
  const [wsStatus, setWsStatus] = useState('connecting')
  const [text, setText] = useState('')
  const [escalating, setEscalating] = useState(false)

  const { data: ticket, isLoading: ticketLoading } = useQuery({
    queryKey: ['ticket', ticketId],
    queryFn: async () => { const r = await ticketsApi.get(ticketId); return r.data },
    enabled: !!ticketId, staleTime: 5000,
  })
  const { data: history = [], isLoading: histLoading } = useQuery({
    queryKey: ['ticket-msgs', ticketId],
    queryFn: async () => { const r = await ticketsApi.getMessages(ticketId); return r.data },
    enabled: !!ticketId,
    staleTime: 0,
    refetchInterval: 8000,   // WS is primary; polling is a fallback safety net
  })

  // Reset initializedRef and clear msgs when switching conversations
  const initializedRef = useRef(false)
  useEffect(() => {
    initializedRef.current = false
    setMsgs([])
    setTyping(false)
  }, [ticketId])

  // Seed msgs from history on initial load and merge in any DB-committed msgs the WS may have missed
  useEffect(() => {
    if (!history.length) return
    if (!initializedRef.current) {
      // First load: replace completely so we have the correct DB order
      initializedRef.current = true
      setMsgs(history)
      return
    }
    // Subsequent polls: merge in any new messages by id that aren't in local state yet
    setMsgs(prev => {
      const existingIds = new Set(prev.map(m => m.id).filter(Boolean))
      const newFromDB = history.filter(m => m.id && !existingIds.has(m.id))
      if (!newFromDB.length) return prev
      // Merge: combine and re-sort by created_at
      const merged = [...prev, ...newFromDB]
      merged.sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
      return merged
    })
    const last = history[history.length - 1]
    if (last && (last.sender_type === 'ai' || last.sender_type === 'agent' || last.sender_role === 'ai')) {
      setTyping(false)
    }
  }, [history])

  // WebSocket connection management
  const connectWS = useCallback(() => {
    if (!ticketId || !token) return
    setWsStatus('connecting')
    const wsUrl = `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://${window.location.host === 'localhost:5173' ? 'localhost:8000' : window.location.host}/ws/chat/${ticketId}?token=${token}`
    const ws = new WebSocket(wsUrl)
    wsRef.current = ws
    ws.onopen  = () => setWsStatus('connected')
    ws.onerror = () => setWsStatus('error')
    ws.onclose = () => setWsStatus('disconnected')
    ws.onmessage = e => {
      try {
        const d = JSON.parse(e.data)
        if (d.type === 'message' || d.type === 'ai_response') {
          setTyping(false)
          const msgObj = d.data || d
          const normalized = {
            ...msgObj,
            sender_type: msgObj.sender_type || msgObj.sender_role || msgObj.sender
          }
          setMsgs(p => {
            const exists = p.some(m => (m.id && m.id === normalized.id) || (m.created_at === normalized.created_at && m.body === normalized.body))
            if (exists) return p
            const optIndex = p.findIndex(m => typeof m.id === 'string' && m.id.startsWith('user-opt-') && m.body === normalized.body)
            if (optIndex !== -1) {
              const updated = [...p]
              updated[optIndex] = normalized
              return updated
            }
            return [...p, normalized]
          })
          // Trigger a background poll so next refetch picks up the committed DB state
          queryClient.invalidateQueries({ queryKey: ['ticket-msgs', ticketId] })
        } else if (d.type === 'typing') {
          setTyping(true)
          setTimeout(() => setTyping(false), 4000)
        } else if (d.type === 'agent_joined') {
          queryClient.invalidateQueries({ queryKey: ['ticket', ticketId] })
          setMsgs(p => [...p, { id: `sys-${Date.now()}`, sender_type: 'system', body: `👤 Agent ${d.agent_name || 'Support'} joined the conversation.` }])
        } else if (d.type === 'ticket_update') {
          queryClient.invalidateQueries({ queryKey: ['ticket', ticketId] })
          queryClient.invalidateQueries({ queryKey: ['tickets', 'customer'] })
        }
      } catch {}
    }
    return ws
  }, [ticketId, token, queryClient])

  useEffect(() => {
    const ws = connectWS()
    return () => { ws?.close() }
  }, [connectWS])

  useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [msgs, typing])

  const send = e => {
    if (e) e.preventDefault()
    if (!text.trim() || !wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) return
    const outgoing = text.trim()
    wsRef.current.send(JSON.stringify({ type: 'message', body: outgoing }))
    setText('')
    setTyping(true)
    // Add optimistic user message to thread immediately
    setMsgs(p => {
      const optimisticId = `user-opt-${Date.now()}`
      return [...p, { id: optimisticId, sender_type: 'customer', body: outgoing, created_at: new Date().toISOString() }]
    })
  }


  const escalate = async () => {
    setEscalating(true)
    try {
      await ticketsApi.escalate(ticketId)
      queryClient.invalidateQueries({ queryKey: ['ticket', ticketId] })
      queryClient.invalidateQueries({ queryKey: ['tickets', 'customer'] })
    } finally { setEscalating(false) }
  }

  const reopenMut = useMutation({
    mutationFn: () => ticketsApi.reopen(ticketId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ticket', ticketId] })
      queryClient.invalidateQueries({ queryKey: ['tickets', 'customer'] })
    }
  })

  if (ticketLoading || histLoading) return (
    <div className="flex-1 flex items-center justify-center">
      <div className="space-y-3 text-center animate-pulse">
        <div className="w-12 h-12 bg-indigo-100 rounded-2xl mx-auto flex items-center justify-center">
          <Sparkles className="text-indigo-600" size={24} />
        </div>
        <p className="text-xs font-semibold text-[#64748B]">Loading conversation…</p>
      </div>
    </div>
  )

  if (!ticket) return (
    <div className="flex-1 flex items-center justify-center text-[#64748B] text-sm font-semibold">
      Conversation not found.
    </div>
  )

  const isOpen = !['resolved', 'closed'].includes(ticket.status)
  const hasAgent = !!ticket.agent_id

  // Dynamic ticket state presentation
  let statusBadge = { label: '✨ AI Active', style: 'bg-indigo-100 text-indigo-700' }
  if (ticket.status === 'escalated') {
    statusBadge = hasAgent
      ? { label: `👤 Chatting with ${ticket.agent_name || 'Agent'}`, style: 'bg-emerald-100 text-emerald-800 font-bold' }
      : { label: '⏳ Waiting for Agent', style: 'bg-amber-100 text-amber-800 font-bold' }
  } else if (ticket.status === 'resolved') {
    statusBadge = { label: '✅ Resolved', style: 'bg-emerald-100 text-emerald-800' }
  } else if (ticket.status === 'closed') {
    statusBadge = { label: '🔒 Closed', style: 'bg-gray-100 text-gray-700' }
  } else if (ticket.status === 'reopened') {
    statusBadge = { label: '🔄 Reopened', style: 'bg-blue-100 text-blue-700' }
  }

  // Show "Talk to Human" ONLY when AI is active (not when agent assigned or resolved)
  const showTalkToHuman = isOpen && ticket.status === 'open' && !hasAgent

  return (
    <div className="flex-1 flex flex-col min-h-0 bg-white">
      {/* Active Conversation Header */}
      <div className="flex items-center justify-between px-5 py-3.5 border-b border-[#E2E8F0] bg-white shrink-0 shadow-2xs">
        <div className="flex items-center gap-3 min-w-0">
          {/* Desktop sidebar toggle button when sidebar is collapsed */}
          {!sidebarOpen && (
            <div className="hidden md:flex items-center gap-1.5 shrink-0">
              <button
                onClick={onToggleSidebar}
                className="p-2 rounded-xl text-[#64748B] hover:text-[#0F172A] hover:bg-[#F1F5F9] border border-[#E2E8F0] transition-all group relative cursor-pointer shadow-2xs"
                title="Open sidebar (Ctrl+B)"
                aria-label="Open sidebar"
              >
                <PanelLeftOpen size={18} />
                <span className="pointer-events-none absolute left-0 top-full mt-1.5 z-50 whitespace-nowrap rounded-lg bg-slate-900/95 backdrop-blur-xs px-2.5 py-1 text-[11px] font-medium text-white opacity-0 shadow-lg transition-all duration-150 group-hover:opacity-100 group-hover:translate-y-0.5">
                  Open sidebar <span className="text-[10px] text-slate-400 ml-1">Ctrl+B</span>
                </span>
              </button>
              {onNewChat && (
                <button
                  onClick={onNewChat}
                  className="p-2 rounded-xl text-[#64748B] hover:text-indigo-600 hover:bg-indigo-50 border border-[#E2E8F0] hover:border-indigo-200 transition-all group relative cursor-pointer shadow-2xs"
                  title="New conversation"
                  aria-label="New conversation"
                >
                  <Plus size={18} />
                  <span className="pointer-events-none absolute left-0 top-full mt-1.5 z-50 whitespace-nowrap rounded-lg bg-slate-900/95 backdrop-blur-xs px-2.5 py-1 text-[11px] font-medium text-white opacity-0 shadow-lg transition-all duration-150 group-hover:opacity-100 group-hover:translate-y-0.5">
                    New conversation
                  </span>
                </button>
              )}
            </div>
          )}

          {onBack && (
            <button onClick={onBack} className="md:hidden p-1.5 rounded-xl hover:bg-gray-100 text-[#64748B]" aria-label="Back to conversations">
              <ArrowLeft size={18} />
            </button>
          )}
          <div className="min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              <h2 className="font-bold text-[#0F172A] text-sm truncate max-w-sm">{ticket.subject}</h2>
              <span className={`text-[10px] font-extrabold px-2.5 py-0.5 rounded-full shrink-0 ${statusBadge.style}`}>
                {statusBadge.label}
              </span>
            </div>
            <p className="text-[11px] text-[#94A3B8] font-mono mt-0.5">{ticket.ref} · {ticket.category}</p>
          </div>
        </div>

        {showTalkToHuman && (
          <button
            onClick={escalate}
            disabled={escalating}
            className="shrink-0 text-xs font-bold text-amber-800 bg-amber-50 border border-amber-200 hover:bg-amber-100 px-3.5 py-1.5 rounded-xl transition-colors disabled:opacity-50 flex items-center gap-1.5 shadow-2xs"
            aria-label="Request human agent"
          >
            <UserIcon size={14} />
            <span>{escalating ? 'Connecting…' : 'Talk to Human'}</span>
          </button>
        )}
      </div>

      <LifecycleBanner status={ticket.status} hasAgent={hasAgent} agentName={ticket.agent_name} />
      <WSDisconnectBanner wsStatus={wsStatus} onReconnect={() => { wsRef.current?.close(); connectWS() }} />

      {/* Messages Thread */}
      <div className="flex-1 overflow-y-auto px-4 md:px-8 py-5 space-y-4 min-h-0" role="log" aria-live="polite" aria-label="Messages">
        {msgs.map((m, i) => {
            const sType      = m.sender_type || m.sender_role || m.sender
            const isCustomer = sType === 'customer'
            const isSystem   = sType === 'system'
            const isAgent    = sType === 'agent'

            if (isSystem) {
              return (
                <div key={m.id || i} className="text-center my-2">
                  <span className="text-[11px] font-semibold text-[#64748B] bg-[#F1F5F9] px-3.5 py-1 rounded-full inline-block border border-[#E2E8F0]">
                    {m.body}
                  </span>
                </div>
              )
            }

            return (
              <div key={m.id || i} className={`flex flex-col msg-enter ${isCustomer ? 'items-end' : 'items-start'}`}>
                {!isCustomer && (
                  <div className="flex items-center gap-1.5 mb-1 px-1">
                    {isAgent ? (
                      <span className="text-[11px] font-bold text-emerald-700 flex items-center gap-1">
                        <UserIcon size={12} /> 👤 {m.sender_name || 'Support Agent'}
                      </span>
                    ) : (
                      <span className="text-[11px] font-bold text-indigo-600 flex items-center gap-1">
                        <Sparkles size={12} className="text-amber-400" /> ✨ SupportHub AI
                      </span>
                    )}
                  </div>
                )}

                <div className={`max-w-[85%] md:max-w-[75%] px-4 py-3 rounded-2xl shadow-2xs ${
                  isCustomer
                    ? 'bg-gradient-to-r from-indigo-600 to-indigo-700 text-white rounded-br-xs'
                    : isAgent
                    ? 'bg-emerald-50/90 text-[#0F172A] border border-emerald-200 rounded-bl-xs'
                    : 'bg-[#F8FAFC] text-[#0F172A] border border-[#E2E8F0] rounded-bl-xs'
                }`}>
                  <MessageBody msg={m} />
                </div>
                <span className="text-[10px] text-[#94A3B8] mt-1 px-1">{formatSmartTime(m.created_at)}</span>
              </div>
            )
          })}
          {typing && <TypingIndicator />}
          <div ref={messagesEndRef} />
      </div>

      {/* Sticky Bottom Composer */}
      <div className="px-4 md:px-8 py-3.5 border-t border-[#E2E8F0] bg-white shrink-0 space-y-3">
          {['resolved', 'closed'].includes(ticket.status) ? (
            <div className="space-y-3">
              <CsatWidget ticketId={ticketId} />
              <button
                onClick={() => reopenMut.mutate()}
                disabled={reopenMut.isPending}
                className="w-full py-2.5 border-2 border-dashed border-[#E2E8F0] hover:border-indigo-400 hover:bg-indigo-50/50 text-[#64748B] hover:text-indigo-600 rounded-2xl text-xs font-bold transition-all cursor-pointer"
              >
                {reopenMut.isPending ? 'Reopening…' : '↺ Reopen Conversation'}
              </button>
            </div>
          ) : (
            <form onSubmit={send} className="flex items-center gap-2 bg-[#F8FAFC] border border-[#E2E8F0] focus-within:border-indigo-500 focus-within:ring-2 focus-within:ring-indigo-100 rounded-2xl p-1.5 transition-all">

              <input
                value={text}
                onChange={e => setText(e.target.value)}
                placeholder="Ask anything about your order, delivery, refund or account..."
                className="flex-1 bg-transparent px-2 py-1.5 text-sm text-[#0F172A] placeholder-[#94A3B8] outline-none"
                aria-label="Message composer input"
              />

              <button
                type="submit"
                disabled={!text.trim() || wsStatus !== 'connected'}
                className="bg-indigo-600 hover:bg-indigo-700 text-white p-2.5 rounded-xl font-bold text-xs flex items-center gap-1.5 transition-colors disabled:opacity-40 shrink-0 shadow-sm cursor-pointer"
                aria-label="Send message"
              >
                <Send size={16} />
                <span className="hidden sm:inline">Send</span>
              </button>
            </form>
          )}
      </div>
    </div>
  )
}

// ── New Ticket Creation Modal ──────────────────────────────────
function NewChatModal({ isOpen, onClose, onCreated }) {
  const queryClient = useQueryClient()
  const [category, setCategory] = useState('general')

  const categories = [
    { id: 'general',   label: 'General Support', icon: HelpCircle, desc: 'General questions & platform help' },
    { id: 'billing',   label: 'Billing & Orders',  icon: CreditCard, desc: 'Order status, invoices & payment issues' },
    { id: 'technical', label: 'Technical Issue',   icon: Wrench,     desc: 'Bug reports, login & technical problems' },
    { id: 'account',   label: 'Account & Access',  icon: UserIcon,   desc: 'Password reset & profile management' },
  ]

  const createMut = useMutation({
    mutationFn: d => ticketsApi.create(d),
    onSuccess: res => {
      queryClient.invalidateQueries({ queryKey: ['tickets', 'customer'] })
      onCreated(res.data.id)
      onClose()
    }
  })

  if (!isOpen) return null

  const handleStart = (catId) => {
    const targetCat = catId || category
    const catObj = categories.find(c => c.id === targetCat) || categories[0]
    createMut.mutate({
      subject: `${catObj.label} Query`,
      category: targetCat,
      channel: 'website_chat'
    })
  }

  return (
    <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl shadow-2xl w-full max-w-md overflow-hidden border border-[#E2E8F0] animate-scaleIn">
        <div className="flex justify-between items-center px-6 py-4 border-b border-[#E2E8F0] bg-gradient-to-r from-indigo-600 to-purple-600 text-white">
          <div className="flex items-center gap-2">
            <Sparkles size={18} className="text-amber-300" />
            <h3 className="font-bold text-base">New AI Support Conversation</h3>
          </div>
          <button onClick={onClose} className="p-1 text-white/80 hover:text-white rounded-lg"><X size={18} /></button>
        </div>

        <div className="p-6 space-y-4">
          <div>
            <label className="block text-xs font-bold text-[#0F172A] mb-3 uppercase tracking-wider">Select Category</label>
            <div className="grid grid-cols-2 gap-3">
              {categories.map(c => (
                <button type="button" key={c.id} onClick={() => setCategory(c.id)}
                  className={`p-3.5 rounded-2xl border text-left transition-all ${category === c.id ? 'border-indigo-600 bg-indigo-50/60 ring-2 ring-indigo-500/20' : 'border-[#E2E8F0] hover:border-indigo-200 bg-white'}`}>
                  <c.icon size={18} className={category === c.id ? 'text-indigo-600' : 'text-[#64748B]'} />
                  <div className="text-xs font-bold text-[#0F172A] mt-1.5">{c.label}</div>
                  <div className="text-[11px] text-[#64748B] mt-0.5 leading-tight">{c.desc}</div>
                </button>
              ))}
            </div>
          </div>

          <div className="flex justify-end gap-2 pt-3 border-t border-[#E2E8F0]">
            <button type="button" onClick={onClose} className="px-4 py-2 text-xs font-semibold text-[#64748B] hover:bg-gray-100 rounded-xl">Cancel</button>
            <button type="button" onClick={() => handleStart()} disabled={createMut.isPending}
              className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition-colors disabled:opacity-50 flex items-center gap-1.5 shadow-sm">
              <Send size={14} />
              {createMut.isPending ? 'Starting…' : 'Start Conversation'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

// ── Main ConversationalHome Component ──────────────────────────
export default function ConversationalHome() {
  const { id: routeTicketId } = useParams()
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const [selectedId, setSelectedId] = useState(routeTicketId || null)
  const [filter, setSelectedFilter] = useState('active') // active | completed | all
  const [search, setSearch]          = useState('')
  const [showModal, setShowModal]    = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)

  useEffect(() => {
    try {
      localStorage.setItem('supporthub_customer_sidebar', String(sidebarOpen))
    } catch {}
  }, [sidebarOpen])

  useEffect(() => {
    const handleKeyDown = (e) => {
      // Ctrl+B or Cmd+B to toggle sidebar like ChatGPT / IDEs
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'b') {
        e.preventDefault()
        setSidebarOpen(prev => !prev)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  // Fetch customer profile
  const { data: profile } = useQuery({
    queryKey: ['auth', 'me'],
    queryFn: async () => { const r = await authApi.me(); return r.data }
  })

  // Fetch tickets
  const { data: tickets = [], isLoading: ticketsLoading } = useQuery({
    queryKey: ['tickets', 'customer'],
    queryFn: async () => { const r = await ticketsApi.list(); return r.data },
    staleTime: 5000,
    refetchInterval: 10000
  })

  useEffect(() => {
    if (routeTicketId) {
      setSelectedId(routeTicketId)
    }
  }, [routeTicketId])

  // Filter tickets
  const filteredTickets = tickets.filter(t => {
    const isClosed = ['resolved', 'closed'].includes(t.status)
    if (filter === 'active' && isClosed) return false
    if (filter === 'completed' && !isClosed) return false
    if (search.trim()) {
      const q = search.toLowerCase()
      const matchSub = t.subject?.toLowerCase().includes(q)
      const matchRef = t.ref?.toLowerCase().includes(q)
      const matchCat = t.category?.toLowerCase().includes(q)
      if (!matchSub && !matchRef && !matchCat) return false
    }
    return true
  })

  const selectTicket = (id) => {
    setSelectedId(id)
    navigate(`/customer/chat/${id}`)
  }

  const handleQuickAction = async (promptText) => {
    try {
      let cat = 'General Support'
      const lower = promptText.toLowerCase()
      if (lower.includes('payment') || lower.includes('billing')) cat = 'Billing & Orders'
      else if (lower.includes('delivery') || lower.includes('order') || lower.includes('address')) cat = 'Shipping & Delivery'
      else if (lower.includes('return') || lower.includes('refund')) cat = 'Returns & Refunds'

      const res = await ticketsApi.create({
        subject: promptText,
        category: cat,
        body: promptText,
        channel: 'website_chat'
      })
      queryClient.invalidateQueries({ queryKey: ['tickets', 'customer'] })
      selectTicket(res.data.id)
    } catch (err) {
      alert(`Failed to start conversation: ${err.message}`)
    }
  }

  return (
    <div className="flex-1 flex flex-col md:flex-row h-full overflow-hidden bg-[#F8FAFC]">
      {/* LEFT: Collapsible Conversation Sidebar */}
      <div
        className={`
          bg-white flex flex-col shrink-0 h-full z-10
          transition-all duration-300 ease-in-out overflow-hidden
          ${selectedId ? (sidebarOpen ? 'hidden md:flex' : 'hidden') : 'flex'}
          ${sidebarOpen ? 'w-full md:w-80 border-r border-[#E2E8F0] opacity-100' : 'w-0 md:w-0 border-r-0 opacity-0 pointer-events-none'}
        `}
        style={{ width: sidebarOpen ? undefined : 0 }}
      >
        <div className="w-full md:w-80 flex flex-col h-full shrink-0">
          {/* New Conversation + Search + Close Sidebar Toggle */}
          <div className="p-3.5 border-b border-[#E2E8F0] space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <MessageSquare size={16} className="text-indigo-600" />
                <span className="text-xs font-bold text-[#0F172A] uppercase tracking-wider">Conversations</span>
                <span className="text-[10px] bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded-full font-mono font-semibold">
                  {filteredTickets.length}
                </span>
              </div>
              <button
                onClick={() => setSidebarOpen(false)}
                className="p-1.5 rounded-xl text-[#64748B] hover:text-[#0F172A] hover:bg-[#F1F5F9] transition-all group relative cursor-pointer"
                title="Close sidebar (Ctrl+B)"
                aria-label="Close sidebar"
              >
                <PanelLeftClose size={18} />
                <span className="pointer-events-none absolute right-0 top-full mt-1.5 z-50 whitespace-nowrap rounded-lg bg-slate-900/95 backdrop-blur-xs px-2.5 py-1 text-[11px] font-medium text-white opacity-0 shadow-lg transition-all duration-150 group-hover:opacity-100 group-hover:translate-y-0.5">
                  Close sidebar <span className="text-[10px] text-slate-400 ml-1">Ctrl+B</span>
                </span>
              </button>
            </div>

            <button
              onClick={() => setShowModal(true)}
              className="w-full py-2.5 px-4 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white rounded-xl text-xs font-extrabold flex items-center justify-center gap-2 transition-all shadow-md shadow-indigo-100 cursor-pointer"
            >
              <Plus size={16} />
              <span>New conversation</span>
            </button>

            {/* Search conversations */}
            <input
              type="text"
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Search conversations…"
              className="w-full px-3.5 py-2 bg-[#F8FAFC] border border-[#E2E8F0] rounded-xl text-xs focus:outline-none focus:border-indigo-500 font-medium"
            />

            {/* Conversation filters */}
            <div className="flex bg-[#F1F5F9] p-1 rounded-xl border border-[#E2E8F0] text-xs font-bold">
              {['active', 'completed', 'all'].map(f => (
                <button
                  key={f}
                  onClick={() => setSelectedFilter(f)}
                  className={`flex-1 py-1 rounded-lg capitalize transition-all cursor-pointer ${filter === f ? 'bg-white text-indigo-600 shadow-xs' : 'text-[#64748B] hover:text-[#0F172A]'}`}
                >
                  {f}
                </button>
              ))}
            </div>
          </div>

          {/* Conversation List Cards */}
          <div className="flex-1 overflow-y-auto p-3 space-y-2">
            {ticketsLoading ? (
              <div className="p-6 text-center text-xs text-[#94A3B8]">Loading conversations…</div>
            ) : filteredTickets.length === 0 ? (
              <div className="p-8 text-center space-y-3">
                <MessageSquare size={32} className="mx-auto text-gray-300" />
                <p className="text-xs font-semibold text-[#64748B]">No conversations found</p>
                <button onClick={() => setShowModal(true)} className="text-xs font-bold text-indigo-600 hover:underline">
                  + Start a new chat
                </button>
              </div>
            ) : (
              filteredTickets.map(t => {
                const isSelected = selectedId === t.id
                const isClosed   = ['resolved', 'closed'].includes(t.status)
                
                let statusLabel = 'AI Active'
                let statusStyle = 'bg-indigo-50 text-indigo-700 border-indigo-200'

                if (t.status === 'escalated') {
                  if (t.agent_id) {
                    statusLabel = 'Agent Joined'
                    statusStyle = 'bg-emerald-50 text-emerald-700 border-emerald-200'
                  } else {
                    statusLabel = 'Escalated'
                    statusStyle = 'bg-amber-50 text-amber-700 border-amber-200'
                  }
                } else if (isClosed) {
                  statusLabel = t.status === 'resolved' ? 'Resolved' : 'Closed'
                  statusStyle = 'bg-gray-100 text-gray-600 border-gray-200'
                }

                return (
                  <div
                    key={t.id}
                    onClick={() => selectTicket(t.id)}
                    className={`p-3.5 rounded-2xl border transition-all cursor-pointer space-y-1.5 ${
                      isSelected
                        ? 'bg-indigo-50/80 border-indigo-300 shadow-xs ring-1 ring-indigo-200'
                        : 'bg-white border-[#E2E8F0] hover:border-indigo-200 hover:bg-gray-50/50'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <span className="font-bold text-xs text-[#0F172A] line-clamp-1 flex-1">{t.subject}</span>
                      <span className={`text-[10px] font-extrabold px-2 py-0.5 rounded-full border shrink-0 ${statusStyle}`}>
                        {statusLabel}
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-[10px] text-[#94A3B8]">
                      <span className="font-mono">{t.ref}</span>
                      <span>{formatSmartTime(t.updated_at || t.created_at)}</span>
                    </div>
                  </div>
                )
              })
            )}
          </div>
        </div>
      </div>

      {/* RIGHT: Main Workspace (Empty state or active ChatView) */}
      <div className={`flex-1 flex flex-col h-full overflow-hidden ${!selectedId ? 'flex' : (sidebarOpen ? 'hidden md:flex' : 'flex')}`}>
        {selectedId ? (
          <ChatView
            ticketId={selectedId}
            onBack={() => { setSelectedId(null); navigate('/customer/chat') }}
            onQuickAction={handleQuickAction}
            sidebarOpen={sidebarOpen}
            onToggleSidebar={() => setSidebarOpen(prev => !prev)}
            onNewChat={() => setShowModal(true)}
          />
        ) : (
          <EmptyState
            profile={profile}
            onQuickAction={handleQuickAction}
            sidebarOpen={sidebarOpen}
            onToggleSidebar={() => setSidebarOpen(prev => !prev)}
            onNewChat={() => setShowModal(true)}
          />
        )}
      </div>

      {/* New Ticket Modal */}
      <NewChatModal isOpen={showModal} onClose={() => setShowModal(false)} onCreated={selectTicket} />
    </div>
  )
}
