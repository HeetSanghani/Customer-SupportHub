import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { ticketsApi } from '../api/tickets'
import { ordersApi } from '../api/orders'
import { useAuthStore } from '../store/authStore'
import { 
  ArrowLeft, Send, Clock, Zap, X, Search, 
  User, ShoppingBag, Sparkles, ChevronRight, CheckCircle2, 
  Package, ExternalLink, ShieldCheck, FileText, Tag, Phone, 
  Mail, Calendar, AlertCircle, Eye, Truck, CheckCircle,
  PanelRightClose, PanelRightOpen
} from 'lucide-react'
import client from '../api/client'
import { formatDateTime, formatSmartTime } from '../utils/dateUtils'
import CopilotPanel from './CopilotPanel'

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
  const [selectedOrderModal, setSelectedOrderModal] = useState(null)
  const [knowledgeSearch, setKnowledgeSearch] = useState('')
  const [sidebarOpen, setSidebarOpen] = useState(() => {
    const saved = localStorage.getItem('agentTicketSidebarOpen')
    return saved !== null ? JSON.parse(saved) : true
  })

  useEffect(() => {
    localStorage.setItem('agentTicketSidebarOpen', JSON.stringify(sidebarOpen))
  }, [sidebarOpen])

  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'b') {
        e.preventDefault()
        setSidebarOpen(prev => !prev)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  const quickReplyTemplates = [
    {
      id: '1',
      title: 'Refund Processed',
      category: 'Billing',
      content: 'Your refund has been processed and should appear in 5-7 business days.'
    },
    {
      id: '2',
      title: 'Order Status & Tracking',
      category: 'Orders',
      content: 'I checked your order status — it is currently in transit. You can track your shipment live under the Orders tab in your dashboard.'
    },
    {
      id: '3',
      title: 'Return Instructions',
      category: 'Returns',
      content: 'To initiate a return, visit your Orders page, select your order, and click Request Return. Items can be returned within 30 days of delivery.'
    },
    {
      id: '4',
      title: 'Delivery Timeframe',
      category: 'Shipping',
      content: 'Standard delivery takes 3–5 business days for metro areas and 5–7 business days for non-metro locations.'
    },
    {
      id: '5',
      title: 'Refund Policy',
      category: 'Billing',
      content: 'Refunds are automatically issued to your original payment method within 5-7 business days once returned items pass quality inspection.'
    },
    {
      id: '6',
      title: 'Payment Troubleshooting',
      category: 'Billing',
      content: 'If your payment failed, please check your card/UPI limits or retry with another payment method. Failed attempts auto-refund within 24-48 hours.'
    },
    {
      id: '7',
      title: 'Address Change Guide',
      category: 'Shipping',
      content: 'Delivery address changes can be made before dispatch. If already shipped, we will request an address update directly with the courier.'
    },
    {
      id: '8',
      title: 'Escalation Notice',
      category: 'General',
      content: "I'm looping in a specialist who can dig deeper into this for you — you'll hear back within 2 hours."
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

    if (wsRef.current) {
      if (
        wsRef.current.readyState === WebSocket.OPEN ||
        wsRef.current.readyState === WebSocket.CONNECTING
      ) {
        wsRef.current.close()
      }
      wsRef.current = null
      setWsConnected(false)
    }

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = window.location.host
    const wsUrl = `${protocol}//${host}/ws/chat/${id}?token=${token}`
    
    const socket = new WebSocket(wsUrl)
    wsRef.current = socket

    socket.onopen = () => {
      if (!isSubscribed) {
        socket.close()
        return
      }
      setWsConnected(true)
    }
    
    socket.onmessage = (event) => {
      if (!isSubscribed) return
      try {
        const data = JSON.parse(event.data)
        if (data.type === 'message') {
          setMessages(prev => {
            const exists = prev.some(m => (m.id && m.id === data.id) || (m.external_message_id && m.external_message_id === data.external_message_id))
            if (exists) return prev
            return [...prev, data]
          })
        } else if (data.type === 'ticket_update' || data.type === 'inbox_update') {
          queryClient.invalidateQueries({ queryKey: ['ticket', id] })
          queryClient.invalidateQueries({ queryKey: ['tickets'] })
        }
      } catch (err) {
        console.error('[WS CLIENT] Error parsing WebSocket message:', err)
      }
    }
    
    socket.onclose = () => {
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

  const handleUseSuggestion = (text) => {
    setInputText(text)
    inputRef.current?.focus()
  }

  // Derive customer details
  const customerName = ticket?.customer?.name || 
    messages.find(m => m.sender_type === 'customer')?.sender_name || 
    'Aarav Sharma'
  
  const customerEmail = ticket?.customer?.email || 'customer@supporthub.com'
  const customerPhone = ticket?.customer?.phone || '+91 98204 41120'
  const customerInitials = customerName.split(' ').filter(Boolean).map(n => n[0]).join('').substring(0, 2).toUpperCase() || 'CU'
  const customerSince = ticket?.customer?.created_at
    ? new Date(ticket.customer.created_at).toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
    : ticket?.created_at
    ? new Date(ticket.created_at).toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
    : 'March 2023'

  // Fetch real orders for this ticket's customer (staff-only endpoint)
  const customerId = ticket?.customer_id
  const { data: relevantOrders = [], isLoading: ordersLoading } = useQuery({
    queryKey: ['customer-orders', customerId],
    queryFn: async () => {
      const res = await ordersApi.getOrdersByCustomerUserId(customerId)
      // Sort by order_date descending (most recent first)
      return (res.data || []).sort((a, b) => {
        if (!a.order_date && !b.order_date) return 0
        if (!a.order_date) return 1
        if (!b.order_date) return -1
        return new Date(b.order_date) - new Date(a.order_date)
      })
    },
    enabled: !!(customerId && (role === 'agent' || role === 'manager' || role === 'admin') && ticket),
    staleTime: 30_000,
  })

  // Track manual order override by agent
  const [manuallySelectedOrderId, setManuallySelectedOrderId] = useState(null)

  // Scan messages and ticket subject for explicit order mentions (ORD-xxx)
  const detectedOrderId = (() => {
    const orderRegex = /\b(ORD-[A-Za-z0-9]+)\b/i
    for (let i = messages.length - 1; i >= 0; i--) {
      const match = messages[i]?.body?.match(orderRegex)
      if (match) return match[1].toUpperCase()
    }
    const subjMatch = ticket?.subject?.match(orderRegex)
    if (subjMatch) return subjMatch[1].toUpperCase()
    return null
  })()

  // Active Order ID: manual choice -> detected from chat/subject -> first order of customer -> null
  const activeOrderId = manuallySelectedOrderId || detectedOrderId || (relevantOrders[0]?.order_id) || null

  // Check if activeOrderId exists in relevantOrders
  const matchedRelevantOrder = relevantOrders.find(
    o => o.order_id?.toUpperCase() === activeOrderId?.toUpperCase()
  )

  // If order was mentioned in chat (e.g. ORD-003 or customer order not in list yet), fetch its full details directly
  const { data: directFetchedOrder } = useQuery({
    queryKey: ['order-detail', activeOrderId],
    queryFn: async () => {
      if (!activeOrderId) return null
      try {
        const res = await ordersApi.getOrderDetail(activeOrderId)
        const d = res.data
        return {
          order_id: d.order?.order_id || activeOrderId,
          status: d.order?.status,
          order_date: d.order?.order_date,
          total_amount: d.order?.total_amount,
          shipping_address: d.order?.shipping_address,
          items: d.items || [],
          shipment_status: d.shipment?.status,
          shipment_carrier: d.shipment?.carrier,
          estimated_delivery_date: d.shipment?.estimated_delivery_date,
          actual_delivery_date: d.shipment?.actual_delivery_date,
          payment_status: d.payment?.status,
        }
      } catch (err) {
        console.warn('Could not fetch direct order details:', err)
        return null
      }
    },
    enabled: !!(activeOrderId && !matchedRelevantOrder && (role === 'agent' || role === 'manager' || role === 'admin')),
    staleTime: 60_000,
  })

  // Full active order object
  const activeOrder = matchedRelevantOrder || directFetchedOrder || (activeOrderId ? { order_id: activeOrderId } : null)


  // Knowledge base articles sample
  const kbArticles = [
    {
      id: 'kb-1',
      title: 'ShopKart Return & Refund Policy (POL-001)',
      snippet: 'Eligibility windows, processing time, damaged item reporting (within 48 hrs), and payment method rules.',
      updated: '3 days ago'
    },
    {
      id: 'kb-2',
      title: 'Order Cancellation & Refund Timelines (POL-002)',
      snippet: 'Cancellation rules before dispatch and automatic UPI/Card refund timelines (5-7 business days).',
      updated: '1 week ago'
    }
  ].filter(a => a.title.toLowerCase().includes(knowledgeSearch.toLowerCase()) || a.snippet.toLowerCase().includes(knowledgeSearch.toLowerCase()))

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
                <span className={`px-2.5 py-0.5 rounded-full text-xs font-extrabold uppercase tracking-wide border ${
                  ticket.status === 'escalated' ? 'bg-red-50 text-red-700 border-red-200' :
                  ticket.status === 'resolved' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' :
                  'bg-indigo-50 text-indigo-700 border-indigo-200'
                }`}>
                  {ticket.status}
                </span>
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
          <button 
            onClick={() => setSidebarOpen(prev => !prev)}
            className="p-2 rounded-xl text-[#9598B0] hover:text-[#1C1B2E] hover:bg-gray-100 transition-colors"
            title={sidebarOpen ? "Close sidebar (Ctrl+B)" : "Open sidebar (Ctrl+B)"}
          >
            {sidebarOpen ? <PanelRightClose size={20} /> : <PanelRightOpen size={20} />}
          </button>
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
                      {isCustomer ? (msg.sender_name || customerName) : isAI ? '✨ AI Agent' : (msg.sender_name || 'Agent User')}
                    </span>
                    <span className="text-[10px] opacity-70">
                      {formatSmartTime(msg.created_at)}
                    </span>
                  </div>
                  {msg.body_html ? (
                    <div
                      className="text-sm leading-relaxed prose prose-sm max-w-none dark:prose-invert"
                      dangerouslySetInnerHTML={{ __html: msg.body_html }}
                    />
                  ) : (
                    <p className="text-sm whitespace-pre-wrap leading-relaxed">{msg.body}</p>
                  )}
                </div>
              </div>
            )
          })}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="relative p-4 bg-white border-t border-[#E5E7F3]">
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
                  placeholder="Search templates..."
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
              </div>
            </div>
          )}

          {ticket.status === 'closed' || ticket.status === 'resolved' ? (
            <div className="text-center p-4 text-[#9598B0] bg-gray-50 rounded-xl border border-[#E5E7F3] font-medium text-xs flex items-center justify-center gap-2">
              <span className="w-2 h-2 rounded-full bg-gray-400"></span>
              This ticket is <span className="font-bold capitalize">{ticket.status}</span>.
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
                title="Insert Quick Reply"
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
                  if (val === '/') setShowQuickReplies(true)
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

      {/* Right Sidebar — Full Agent Intelligence & Context Panel */}
      {sidebarOpen && (
        <div className="w-96 bg-white border-l border-[#E5E7F3] flex flex-col overflow-y-auto shrink-0">
          <div className="p-5 space-y-6">
          
          {/* 1. CUSTOMER PROFILE HEADER */}
          <div className="flex items-center gap-3 border-b border-gray-100 pb-4">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500 text-white flex items-center justify-center font-extrabold text-base shadow-sm shrink-0">
              {customerInitials}
            </div>
            <div>
              <h2 className="text-base font-extrabold text-[#1C1B2E] tracking-tight">{customerName}</h2>
              <p className="text-xs text-[#6C7089] font-medium mt-0.5">
                {relevantOrders.length > 1 ? 'Returning customer' : relevantOrders.length === 1 ? 'Verified customer' : 'Customer'} · customer since {customerSince}
              </p>
            </div>
          </div>

          {/* 2. ✨ AI HANDOFF SUMMARY CARD */}
          <div className="bg-gradient-to-br from-indigo-50/70 via-purple-50/50 to-white border border-indigo-200/80 rounded-2xl p-4 space-y-2.5 shadow-2xs">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-1.5 text-xs font-extrabold text-indigo-900 tracking-wider uppercase">
                <Sparkles size={14} className="text-indigo-600 animate-pulse" />
                <span>AI Handoff Summary</span>
              </div>
              <span className="text-[9px] font-extrabold bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full border border-indigo-200 uppercase">
                Copilot Context
              </span>
            </div>

            <p className="text-xs text-[#1C1B2E] leading-relaxed font-medium">
              {ticket.ai_summary || (
                activeOrder?.order_id
                  ? `Customer is inquiring regarding Order #${activeOrder.order_id}${ticket.subject ? ` (${ticket.subject})` : ''} and requested a transfer to a human support agent for resolution.`
                  : ticket.subject
                  ? `Customer inquiry regarding "${ticket.subject}". Transferred to a human support agent for resolution.`
                  : "Customer is inquiring about order & product info / return policy and explicitly requested a transfer to a human support agent for custom resolution."
              )}
            </p>

            <div className="pt-2 border-t border-indigo-100/80 space-y-2 text-[11px]">
              {/* Dynamic Order Reference Row & Actual Info */}
              <div>
                <div className="flex justify-between items-center">
                  <span className="text-[#6C7089]">Order Reference:</span>
                  {activeOrder?.order_id ? (
                    <button
                      type="button"
                      onClick={() => setSelectedOrderModal(activeOrder)}
                      className="inline-flex items-center gap-1 font-extrabold text-indigo-700 hover:text-indigo-900 bg-indigo-100/80 hover:bg-indigo-200/80 border border-indigo-200 px-2 py-0.5 rounded-md font-mono text-xs transition-colors group cursor-pointer"
                      title="Click to view full order details"
                    >
                      <span>#{activeOrder.order_id}</span>
                      <ExternalLink size={11} className="opacity-70 group-hover:opacity-100" />
                    </button>
                  ) : (
                    <span className="text-gray-400 font-medium italic">No order linked</span>
                  )}
                </div>

                {/* Actual Order Reference Details Box */}
                {activeOrder?.order_id && (
                  <div className="mt-2 bg-white/90 border border-indigo-100/90 rounded-xl p-2.5 space-y-1.5 shadow-2xs">
                    <div className="flex items-center justify-between text-[10px]">
                      <span className="text-[#6C7089] font-medium">Order Status:</span>
                      <span className={`font-bold px-1.5 py-0.5 rounded border uppercase tracking-wider text-[9px] ${
                        activeOrder.status?.toLowerCase() === 'delivered' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' :
                        activeOrder.status?.toLowerCase() === 'cancelled' ? 'bg-red-50 text-red-700 border-red-200' :
                        'bg-blue-50 text-blue-700 border-blue-200'
                      }`}>
                        {(activeOrder.shipment_status || activeOrder.status || 'Active').replace(/_/g, ' ')}
                      </span>
                    </div>

                    {activeOrder.total_amount !== undefined && activeOrder.total_amount !== null && (
                      <div className="flex items-center justify-between text-[10px]">
                        <span className="text-[#6C7089] font-medium">Order Total:</span>
                        <span className="font-extrabold text-indigo-900 font-mono">
                          ₹{Number(activeOrder.total_amount).toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                        </span>
                      </div>
                    )}

                    {activeOrder.items && activeOrder.items.length > 0 && (
                      <div className="flex items-center justify-between text-[10px]">
                        <span className="text-[#6C7089] font-medium">Purchased Item:</span>
                        <span className="font-semibold text-gray-800 truncate max-w-[150px]" title={activeOrder.items.map(i => i.product_name).join(', ')}>
                          {activeOrder.items[0]?.product_name}
                          {activeOrder.items.length > 1 && ` (+${activeOrder.items.length - 1} more)`}
                        </span>
                      </div>
                    )}

                    {activeOrder.order_date && (
                      <div className="flex items-center justify-between text-[10px]">
                        <span className="text-[#6C7089] font-medium">Placed Date:</span>
                        <span className="text-gray-600 font-medium">
                          {activeOrder.order_date.split(' ')[0] || activeOrder.order_date}
                        </span>
                      </div>
                    )}

                    <button
                      type="button"
                      onClick={() => setSelectedOrderModal(activeOrder)}
                      className="w-full text-center text-[10px] font-bold text-indigo-600 hover:text-indigo-800 hover:underline pt-1 flex items-center justify-center gap-1 cursor-pointer border-t border-indigo-50 mt-1"
                    >
                      <Eye size={11} /> View Full Order & Tracking Details
                    </button>
                  </div>
                )}

                {/* Multiple customer orders switcher if customer has > 1 orders */}
                {relevantOrders.length > 1 && (
                  <div className="flex items-center justify-between pt-1.5 text-[10px]">
                    <span className="text-[#6C7089] font-medium">Switch Order:</span>
                    <div className="flex flex-wrap gap-1 justify-end">
                      {relevantOrders.map(o => (
                        <button
                          key={o.order_id}
                          type="button"
                          onClick={() => setManuallySelectedOrderId(o.order_id)}
                          className={`px-1.5 py-0.5 rounded font-mono text-[9px] font-bold transition-all cursor-pointer ${
                            activeOrderId === o.order_id
                              ? 'bg-indigo-600 text-white shadow-xs'
                              : 'bg-indigo-50 text-indigo-700 hover:bg-indigo-100 border border-indigo-200/60'
                          }`}
                          title={`Select #${o.order_id}`}
                        >
                          #{o.order_id}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              <div className="flex justify-between">
                <span className="text-[#6C7089]">Primary Issue:</span>
                <span className="font-bold text-gray-800 capitalize">{ticket.category || ticket.subject || 'Return & Product Info'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#6C7089]">AI Action Taken:</span>
                <span className="font-semibold text-gray-700">
                  {activeOrder?.order_id 
                    ? `Checked order #${activeOrder.order_id} history & support policies` 
                    : 'Checked shipment scan history & return policy (POL-001)'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#6C7089]">Handoff Reason:</span>
                <span className="font-bold text-amber-700">
                  {ticket.status === 'escalated' ? 'Escalated by AI: human assistance requested' : 'Human assistance requested by customer'}
                </span>
              </div>
            </div>
          </div>

          {/* 3. CUSTOMER INFORMATION */}
          <div className="space-y-3 pt-1 border-t border-gray-100">
            <div className="text-[10px] font-extrabold text-[#9598B0] uppercase tracking-wider">
              CUSTOMER
            </div>
            
            <div className="space-y-2 text-xs">
              <div className="flex justify-between items-center">
                <span className="text-[#6C7089] flex items-center gap-1.5">
                  <Mail size={13} className="text-gray-400" /> Email
                </span>
                <span className="font-bold text-[#1C1B2E] truncate max-w-[190px]">{customerEmail}</span>
              </div>

              <div className="flex justify-between items-center">
                <span className="text-[#6C7089] flex items-center gap-1.5">
                  <Phone size={13} className="text-gray-400" /> Phone
                </span>
                <span className="font-bold text-[#1C1B2E] font-mono">{customerPhone}</span>
              </div>

              <div className="flex justify-between items-center">
                <span className="text-[#6C7089] flex items-center gap-1.5">
                  <Calendar size={13} className="text-gray-400" /> Customer since
                </span>
                <span className="font-semibold text-gray-700">{customerSince}</span>
              </div>

              <div className="flex justify-between items-center">
                <span className="text-[#6C7089]">Account Status</span>
                <span className="font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">
                  {relevantOrders.length > 1 ? 'Returning' : relevantOrders.length === 1 ? 'Customer (1 order)' : 'Active'}
                </span>
              </div>

              <div className="flex justify-between items-center">
                <span className="text-[#6C7089]">Sentiment</span>
                <span className="font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded-md border border-amber-200 capitalize">
                  {ticket.sentiment || 'Concerned'}
                </span>
              </div>
            </div>
          </div>

          {/* 4. CURRENT TICKET DETAILS & CONTROLS */}
          <div className="space-y-3 pt-2 border-t border-gray-100">
            <div className="flex items-center justify-between">
              <div className="text-[10px] font-extrabold text-[#9598B0] uppercase tracking-wider">
                CURRENT TICKET
              </div>
              <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full capitalize flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> {ticket.status}
              </span>
            </div>

            <div className="space-y-2.5 text-xs">
              <div className="flex justify-between items-center">
                <span className="text-[#6C7089]">Ticket ID</span>
                <span className="font-extrabold font-mono text-[#1C1B2E]">#{ticket.ref}</span>
              </div>

              <div className="flex justify-between items-center">
                <span className="text-[#6C7089]">Category</span>
                <span className="font-bold bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded-md capitalize">{ticket.category}</span>
              </div>

              <div className="flex justify-between items-center">
                <span className="text-[#6C7089]">Created</span>
                <span className="font-semibold text-gray-700">{formatSmartTime(ticket.created_at)}</span>
              </div>

              {/* Status Control Dropdown */}
              <div>
                <label className="text-[11px] font-bold text-[#6C7089] block mb-1">Status</label>
                <select
                  className="w-full text-xs font-bold border border-[#E5E7F3] rounded-xl p-2.5 bg-gray-50 focus:bg-white outline-none focus:border-indigo-500 transition-colors capitalize"
                  value={ticket.status}
                  onChange={e => updateMutation.mutate({ status: e.target.value })}
                >
                  <option value="open">Open</option>
                  <option value="waiting">Snooze / Waiting</option>
                  <option value="escalated">Escalated</option>
                  <option value="resolved">Resolved</option>
                  <option value="closed">Closed</option>
                </select>
              </div>

              {/* Priority Control Dropdown */}
              <div>
                <label className="text-[11px] font-bold text-[#6C7089] block mb-1">Priority</label>
                <select
                  className="w-full text-xs font-bold border border-[#E5E7F3] rounded-xl p-2.5 bg-gray-50 focus:bg-white outline-none focus:border-indigo-500 transition-colors capitalize"
                  value={ticket.priority}
                  onChange={e => updateMutation.mutate({ priority: e.target.value })}
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="urgent">Urgent</option>
                </select>
              </div>

              {/* Assignee */}
              <div>
                <label className="text-[11px] font-bold text-[#6C7089] block mb-1">Assignee</label>
                <select
                  className="w-full text-xs font-bold border border-[#E5E7F3] rounded-xl p-2.5 bg-gray-50 focus:bg-white outline-none focus:border-indigo-500 transition-colors"
                  value={ticket.agent_id ? 'you' : 'unassigned'}
                  onChange={e => updateMutation.mutate({ agent_id: e.target.value === 'you' ? 'current' : null })}
                >
                  <option value="you">You ({currentName || 'Agent User'})</option>
                  <option value="unassigned">Unassigned</option>
                </select>
              </div>
            </div>
          </div>

          {/* 5. RELEVANT ORDERS SECTION */}
          <div className="space-y-3 pt-2 border-t border-gray-100">
            <div className="flex items-center justify-between">
              <div className="text-[10px] font-extrabold text-[#9598B0] uppercase tracking-wider flex items-center gap-1.5">
                <ShoppingBag size={13} className="text-indigo-600" />
                <span>RELEVANT ORDERS</span>
              </div>
              <span className="text-[10px] font-bold text-gray-500">
                {ordersLoading ? '...' : `${relevantOrders.length} Order${relevantOrders.length !== 1 ? 's' : ''}`}
              </span>
            </div>

            <div className="space-y-3">
              {ordersLoading ? (
                <div className="space-y-2">
                  {[1, 2].map(n => (
                    <div key={n} className="border border-[#E5E7F3] rounded-2xl p-3.5 space-y-2 bg-gray-50/50 animate-pulse">
                      <div className="h-3 bg-gray-200 rounded w-1/3" />
                      <div className="h-3 bg-gray-200 rounded w-2/3" />
                      <div className="h-3 bg-gray-200 rounded w-1/2" />
                    </div>
                  ))}
                </div>
              ) : relevantOrders.length === 0 ? (
                <div className="text-center py-4 text-[11px] text-gray-400">
                  No orders found for this customer.
                </div>
              ) : (
                relevantOrders.map(order => {
                  const statusColor = {
                    'delivered': 'bg-emerald-50 text-emerald-700 border-emerald-200',
                    'in_transit': 'bg-blue-50 text-blue-700 border-blue-200',
                    'shipped': 'bg-blue-50 text-blue-700 border-blue-200',
                    'pending': 'bg-yellow-50 text-yellow-700 border-yellow-200',
                    'cancelled': 'bg-red-50 text-red-600 border-red-200',
                    'returned': 'bg-purple-50 text-purple-700 border-purple-200',
                  }[order.status?.toLowerCase()] || 'bg-gray-100 text-gray-700 border-gray-200'

                  const deliveryLabel = order.actual_delivery_date
                    ? `Delivered ${order.actual_delivery_date}`
                    : order.estimated_delivery_date
                    ? `Est. ${order.estimated_delivery_date}`
                    : null

                  return (
                    <div key={order.order_id} className="border border-[#E5E7F3] hover:border-indigo-300 rounded-2xl p-3.5 space-y-2.5 bg-gray-50/50 hover:bg-white transition-all shadow-2xs group">
                      <div className="flex items-center justify-between">
                        <span className="font-extrabold text-xs text-[#1C1B2E] font-mono">#{order.order_id}</span>
                        <span className="font-black text-xs text-indigo-700">₹{Number(order.total_amount).toLocaleString('en-IN', { minimumFractionDigits: 2 })}</span>
                      </div>

                      {order.items?.slice(0, 2).map((item, idx) => (
                        <div key={idx} className="space-y-0.5">
                          <div className="text-xs font-bold text-gray-800 line-clamp-2 group-hover:text-indigo-600 transition-colors">
                            {item.product_name}
                          </div>
                          <div className="text-[10px] text-[#6C7089] font-medium">
                            Qty {item.quantity} · Placed {order.order_date || '—'}
                          </div>
                        </div>
                      ))}
                      {order.items?.length > 2 && (
                        <div className="text-[10px] text-indigo-500 font-semibold">+{order.items.length - 2} more item{order.items.length - 2 !== 1 ? 's' : ''}</div>
                      )}

                      <div className="flex flex-wrap gap-1.5 pt-1">
                        {order.payment_status && (
                          <span className="text-[9px] font-bold px-2 py-0.5 rounded-md bg-white border border-gray-200 text-gray-700">
                            Payment: {order.payment_status.charAt(0).toUpperCase() + order.payment_status.slice(1)}
                          </span>
                        )}
                        <span className={`text-[9px] font-bold px-2 py-0.5 rounded-md border ${statusColor}`}>
                          {order.shipment_status
                            ? order.shipment_status.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
                            : order.status.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}
                        </span>
                        {deliveryLabel && (
                          <span className="text-[9px] font-semibold px-2 py-0.5 rounded-md bg-gray-100 text-gray-600">
                            {deliveryLabel}
                          </span>
                        )}
                      </div>

                      <button
                        onClick={() => setSelectedOrderModal(order)}
                        className="w-full py-1.5 bg-white hover:bg-indigo-50 border border-gray-200 hover:border-indigo-300 text-indigo-600 font-bold text-xs rounded-xl transition-colors flex items-center justify-center gap-1.5 shadow-2xs mt-1"
                      >
                        <Eye size={13} /> View Order Details
                      </button>
                    </div>
                  )
                })
              )}
            </div>
          </div>

          {/* 6. SEARCH SUPPORT KNOWLEDGE BASE */}
          <div className="space-y-3 pt-2 border-t border-gray-100">
            <div className="text-[10px] font-extrabold text-[#9598B0] uppercase tracking-wider">
              SEARCH SUPPORT KNOWLEDGE
            </div>

            <div className="relative">
              <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#9598B0]" />
              <input
                type="text"
                placeholder="e.g. refund eligibility..."
                value={knowledgeSearch}
                onChange={e => setKnowledgeSearch(e.target.value)}
                className="w-full bg-gray-50 border border-[#E5E7F3] rounded-xl pl-8 pr-3 py-2 text-xs outline-none focus:border-indigo-500 focus:bg-white transition-all"
              />
            </div>

            <div className="space-y-2">
              {kbArticles.map(art => (
                <div key={art.id} className="p-3 bg-indigo-50/40 border border-indigo-100 rounded-xl space-y-1">
                  <div className="flex items-center gap-1.5 text-xs font-bold text-indigo-900">
                    <FileText size={13} className="text-indigo-600 shrink-0" />
                    <span className="line-clamp-1">{art.title}</span>
                  </div>
                  <p className="text-[10px] text-[#6C7089] leading-snug line-clamp-2">{art.snippet}</p>
                  <div className="flex items-center justify-between pt-1">
                    <span className="text-[9px] text-gray-400">Updated {art.updated}</span>
                    <button 
                      onClick={() => {
                        setInputText(`Reference: ${art.title} - ${art.snippet}`)
                        inputRef.current?.focus()
                      }}
                      className="text-[10px] font-bold text-indigo-600 hover:text-indigo-800 underline"
                    >
                      Use article
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* 7. AI COPILOT REPLY & ACTIONS PANEL */}
          {(role === 'agent' || role === 'manager' || role === 'admin') && (
            <div className="pt-2 border-t border-gray-100">
              <CopilotPanel
                ticketId={id}
                role={role}
                onUseSuggestion={handleUseSuggestion}
              />
            </div>
          )}

        </div>
      </div>
      )}

      {/* ORDER DETAILS MODAL */}
      {selectedOrderModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4 z-50 animate-fadeIn">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 space-y-5 shadow-2xl border border-gray-100">
            <div className="flex items-center justify-between border-b border-gray-100 pb-4">
              <div className="flex items-center gap-2.5">
                <div className="w-10 h-10 rounded-2xl bg-indigo-100 text-indigo-600 flex items-center justify-center font-bold">
                  <Package size={20} />
                </div>
                <div>
                  <h3 className="font-extrabold text-base text-[#1C1B2E]">Order Details (#{selectedOrderModal.order_id})</h3>
                  <p className="text-xs text-[#6C7089]">Placed on {selectedOrderModal.order_date || '—'}</p>
                </div>
              </div>
              <button
                onClick={() => setSelectedOrderModal(null)}
                className="p-1.5 text-gray-400 hover:text-gray-600 rounded-xl hover:bg-gray-100 transition-colors"
              >
                <X size={20} />
              </button>
            </div>

            {/* Shipment & Tracking Info */}
            <div className="bg-gray-50 border border-gray-200/80 rounded-2xl p-4 space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-[#6C7089] font-medium">Order Status:</span>
                <span className="font-extrabold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">
                  {(selectedOrderModal.shipment_status || selectedOrderModal.status || '—').replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}
                </span>
              </div>
              {selectedOrderModal.shipment_carrier && (
                <div className="flex justify-between">
                  <span className="text-[#6C7089] font-medium">Courier Partner:</span>
                  <span className="font-bold text-gray-800">{selectedOrderModal.shipment_carrier}</span>
                </div>
              )}
              {selectedOrderModal.payment_status && (
                <div className="flex justify-between">
                  <span className="text-[#6C7089] font-medium">Payment:</span>
                  <span className="font-bold text-gray-800">{selectedOrderModal.payment_status.charAt(0).toUpperCase() + selectedOrderModal.payment_status.slice(1)}</span>
                </div>
              )}
              <div className="flex justify-between">
                <span className="text-[#6C7089] font-medium">Delivery Date:</span>
                <span className="font-semibold text-gray-800">
                  {selectedOrderModal.actual_delivery_date
                    ? selectedOrderModal.actual_delivery_date
                    : selectedOrderModal.estimated_delivery_date
                    ? `Est. ${selectedOrderModal.estimated_delivery_date}`
                    : '—'}
                </span>
              </div>
            </div>

            {/* Purchased Items List */}
            <div className="space-y-3">
              <h4 className="text-xs font-extrabold text-[#9598B0] uppercase tracking-wider">Purchased Item(s)</h4>
              {(selectedOrderModal.items || []).map((item, idx) => (
                <div key={idx} className="flex justify-between items-center p-3 border border-gray-200 rounded-2xl bg-white shadow-2xs">
                  <div>
                    <div className="text-xs font-extrabold text-[#1C1B2E]">{item.product_name}</div>
                    <div className="text-[10px] text-[#6C7089] font-mono mt-0.5">SKU: {item.product_id} · Qty: {item.quantity}</div>
                  </div>
                  <div className="font-black text-xs text-indigo-700">₹{Number(item.total_price).toLocaleString('en-IN', { minimumFractionDigits: 2 })}</div>
                </div>
              ))}
            </div>

            {/* Total Footer */}
            <div className="flex justify-between items-center pt-3 border-t border-gray-100">
              <span className="text-xs font-bold text-gray-600">Total Order Amount</span>
              <span className="text-base font-black text-[#1C1B2E]">₹{Number(selectedOrderModal.total_amount).toLocaleString('en-IN', { minimumFractionDigits: 2 })}</span>
            </div>

            <button
              onClick={() => setSelectedOrderModal(null)}
              className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-extrabold text-xs rounded-2xl transition-colors shadow-md"
            >
              Close Order View
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
