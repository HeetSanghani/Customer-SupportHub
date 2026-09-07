import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { ticketsApi } from '../../api/tickets'
import { useAuthStore } from '../../store/authStore'
import { Plus, Send, Star, CheckCircle, X, HelpCircle, CreditCard, Wrench, User as UserIcon, Paperclip } from 'lucide-react'
import client from '../../api/client'
import { formatTime, formatDate, formatSmartTime } from '../../utils/dateUtils'

function CsatWidget({ ticketId }) {
  const navigate = useNavigate()
  const [rating, setRating] = useState(0)
  const [hoverRating, setHoverRating] = useState(0)
  const [comment, setComment] = useState('')
  const [submitted, setSubmitted] = useState(false)
  const queryClient = useQueryClient()

  // Reset widget internal state whenever ticketId changes
  useEffect(() => {
    setRating(0)
    setHoverRating(0)
    setComment('')
    setSubmitted(false)
  }, [ticketId])

  const { data: existingCsat, isLoading } = useQuery({
    queryKey: ['csat', ticketId],
    queryFn: async () => {
      const res = await ticketsApi.getCsat(ticketId)
      return res.data
    },
    enabled: !!ticketId,
    staleTime: 0,
  })

  const csatMutation = useMutation({
    mutationFn: async (data) => {
      const res = await ticketsApi.submitCsat(ticketId, data)
      return res.data
    },
    onSuccess: (data) => {
      setSubmitted(true)
      queryClient.invalidateQueries({ queryKey: ['csat', ticketId] })
      queryClient.invalidateQueries({ queryKey: ['my-csat-reviews'] })
    }
  })

  if (isLoading) return null

  if (existingCsat || submitted) {
    const displayRating = existingCsat?.rating || rating
    const displayComment = existingCsat?.comment || comment
    return (
      <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-4 text-center text-emerald-800 space-y-1.5">
        <div className="flex justify-center items-center gap-1 mb-1">
          {[1, 2, 3, 4, 5].map(star => (
            <Star key={star} size={18} className={star <= displayRating ? "fill-amber-400 text-amber-400" : "text-gray-300"} />
          ))}
        </div>
        <p className="text-xs font-bold">You reviewed this support experience ({displayRating}/5 stars)</p>
        {displayComment && (
          <p className="text-[11px] text-emerald-700 italic font-medium">"{displayComment}"</p>
        )}
        <div>
          <button
            onClick={() => navigate('/customer/reviews')}
            className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-700 hover:text-emerald-900 bg-emerald-100 hover:bg-emerald-200 px-3 py-1 rounded-lg transition-colors mt-1 cursor-pointer"
          >
            View in My Reviews →
          </button>
        </div>
      </div>
    )
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!rating) return
    csatMutation.mutate({ rating, comment })
  }

  return (
    <form onSubmit={handleSubmit} className="bg-indigo-50 border border-indigo-100 rounded-xl p-4 text-center text-indigo-900 space-y-3">
      <div className="text-xs font-bold">How satisfied were you with this support interaction?</div>
      <div className="flex justify-center items-center gap-2">
        {[1, 2, 3, 4, 5].map(star => (
          <button
            key={star}
            type="button"
            onClick={() => setRating(star)}
            onMouseEnter={() => setHoverRating(star)}
            onMouseLeave={() => setHoverRating(0)}
            className="p-1 focus:outline-none transition-transform hover:scale-110"
          >
            <Star
              size={22}
              className={(hoverRating || rating) >= star ? "fill-amber-400 text-amber-400" : "text-gray-300"}
            />
          </button>
        ))}
      </div>

      {rating > 0 && (
        <div className="space-y-2 max-w-sm mx-auto">
          <input
            type="text"
            placeholder="Optional comment..."
            value={comment}
            onChange={e => setComment(e.target.value)}
            className="w-full border border-indigo-200 rounded-lg px-3 py-1.5 text-xs focus:ring-2 focus:ring-indigo-500 outline-none"
          />
          <button
            type="submit"
            disabled={csatMutation.isPending}
            className="bg-[#6366F1] hover:bg-[#4F46E5] text-white text-xs font-bold px-4 py-1.5 rounded-lg transition-colors"
          >
            Submit Feedback
          </button>
        </div>
      )}
    </form>
  )
}

function ChatPane({ ticketId }) {
  const { token } = useAuthStore()
  const messagesEndRef = useRef(null)
  
  const [messages, setMessages] = useState([])
  const [inputText, setInputText] = useState('')
  const [ws, setWs] = useState(null)
  const [ticketStatus, setTicketStatus] = useState(null)
  const [isTyping, setIsTyping] = useState(false)

  const { data: ticket } = useQuery({
    queryKey: ['ticket', ticketId],
    queryFn: async () => {
      const res = await ticketsApi.get(ticketId)
      return res.data
    },
    enabled: !!ticketId,
    staleTime: 0,
  })

  useEffect(() => {
    setTicketStatus(null)
    setMessages([])
    setIsTyping(false)
  }, [ticketId])

  useEffect(() => {
    if (!ticketId) return
    ticketsApi.getMessages(ticketId).then(res => setMessages(res.data)).catch(console.error)
  }, [ticketId])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isTyping])

  const queryClient = useQueryClient()

  useEffect(() => {
    if (!token || !ticketId) return

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = window.location.host
    const wsUrl = `${protocol}//${host}/ws/chat/${ticketId}?token=${token}`
    const socket = new WebSocket(wsUrl)
    
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'message') {
        setIsTyping(false)
        setMessages(prev => {
          const exists = prev.some(m => (m.id && m.id === data.id) || (m.external_message_id && m.external_message_id === data.external_message_id))
          if (exists) return prev
          return [...prev, {
            ...data,
            sender_type: data.sender_type || data.sender_role
          }]
        })
      } else if (data.type === 'agent_joined') {
        queryClient.invalidateQueries({ queryKey: ['ticket', ticketId] })
        queryClient.invalidateQueries({ queryKey: ['tickets'] })
        setMessages(prev => [
          ...prev,
          {
            id: `system-joined-${Date.now()}`,
            sender_type: 'system',
            body: `AGENT CONNECTED: Agent ${data.agent_name || 'Support Agent'} has joined the conversation.`,
            created_at: data.joined_at || new Date().toISOString()
          }
        ])
      } else if (data.type === 'ticket_update') {
        if (data.status) {
          setTicketStatus(data.status)
        } else {
          queryClient.fetchQuery({
            queryKey: ['ticket', ticketId],
            queryFn: async () => {
              const res = await ticketsApi.get(ticketId)
              return res.data
            }
          }).then(fresh => {
            if (fresh?.status) setTicketStatus(fresh.status)
          })
        }
        queryClient.invalidateQueries({ queryKey: ['tickets'] })
        queryClient.invalidateQueries({ queryKey: ['ticket', ticketId] })
      }
    }
    
    setWs(socket)
    return () => socket.close()
  }, [ticketId, token, queryClient])

  const currentStatus = ticketStatus || ticket?.status
  const isClosed = currentStatus === 'closed' || currentStatus === 'resolved'
  const isEscalated = currentStatus === 'escalated'
  const hasAgent = !!ticket?.agent_id

  const sendMessage = (e) => {
    e.preventDefault()
    if (!inputText.trim() || !ws || isClosed) return
    
    ws.send(JSON.stringify({ type: 'message', body: inputText }))
    setInputText('')
    setIsTyping(true)
  }

  if (!ticketId) {
    return (
      <div className="flex-1 bg-white rounded-r-xl border border-l-0 border-[#E5E7F3] flex flex-col items-center justify-center text-center p-8">
        <h3 className="font-bold text-[#1C1B2E] text-lg mb-2">Select a chat</h3>
        <p className="text-sm text-[#6C7089]">Choose a conversation from the left or start a new chat.</p>
      </div>
    )
  }

  return (
    <div className="flex-1 flex flex-col bg-white rounded-r-xl border border-l-0 border-[#E5E7F3]">
      {/* Header */}
      <div className="px-6 py-3.5 border-b border-[#E5E7F3] flex items-center justify-between shrink-0 bg-white">
        <div className="flex items-center gap-3">
          <div className={`w-9 h-9 rounded-xl flex items-center justify-center text-white text-xs font-bold ${ticket?.channel === 'email' ? 'bg-blue-600' : 'bg-indigo-600'}`}>
            {ticket?.channel === 'email' ? '✉️' : 'ST'}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <div className="font-bold text-sm text-[#1C1B2E]">{ticket?.subject || 'Support Conversation'}</div>
              {ticket?.channel === 'email' && (
                <span className="px-2 py-0.5 bg-blue-50 text-blue-700 font-bold text-[10px] rounded-md border border-blue-200 uppercase">
                  Email Inquiry
                </span>
              )}
            </div>
            <div className="text-[10px] text-[#9598B0] flex items-center gap-2 mt-0.5">
              <span>Category: <strong className="capitalize text-[#6C7089]">{ticket?.category || 'General'}</strong></span>
              <span>•</span>
              {hasAgent ? (
                <div className="text-emerald-600 font-bold uppercase flex items-center gap-1">
                  <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse"></div> Agent Connected ({ticket?.agent?.name || 'Live Agent'})
                </div>
              ) : isEscalated ? (
                <div className="text-amber-600 font-bold uppercase flex items-center gap-1">
                  <div className="w-1.5 h-1.5 bg-amber-500 rounded-full animate-pulse"></div> Waiting for Human Agent
                </div>
              ) : (
                <div className="text-indigo-600 font-bold uppercase flex items-center gap-1">
                  <div className="w-1.5 h-1.5 bg-indigo-500 rounded-full"></div> AI Assistant Active
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {!isEscalated && !hasAgent && !isClosed && (
            <button
              onClick={async () => {
                try {
                  await ticketsApi.escalate(ticketId)
                  setTicketStatus('escalated')
                  queryClient.invalidateQueries({ queryKey: ['ticket', ticketId] })
                  queryClient.invalidateQueries({ queryKey: ['tickets'] })
                } catch (err) {
                  console.error('Escalation error:', err)
                }
              }}
              className="inline-flex items-center gap-1 bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-300 font-bold text-xs px-3 py-1.5 rounded-lg transition-colors cursor-pointer"
              title="Escalate chat directly to a human support agent"
            >
              <UserIcon size={14} /> Talk to Human
            </button>
          )}

          <div className="text-right">
            <div className="text-[10px] font-bold text-[#9598B0] uppercase">Ticket Ref</div>
            <div className="text-xs font-mono font-bold bg-gray-100 px-2 py-0.5 rounded text-[#1C1B2E] mt-0.5">
              {ticket?.ref || '...'}
            </div>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((msg, idx) => {
          const isMe = msg.sender_type === 'customer'
          return (
            <div key={idx} className={`flex flex-col ${isMe ? 'items-end' : 'items-start'}`}>
              <div className={`max-w-[80%] rounded-2xl px-5 py-3 ${isMe ? 'bg-[#6366F1] text-white rounded-br-sm shadow-sm' : 'bg-[#F6F7FC] text-[#1C1B2E] rounded-bl-sm border border-[#E5E7F3] shadow-xs'}`}>
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
                    const isVideo = /\.(mp4|webm|ogg|mov|avi)(\?.*)?$/i.test(filename) ||
                                    /\.(mp4|webm|ogg|mov|avi)(\?.*)?$/i.test(url) ||
                                    /video/i.test(filename)
                    const isAudio = /\.(mp3|wav|ogg|m4a|aac)(\?.*)?$/i.test(filename) || 
                                    /\.(mp3|wav|ogg|m4a|aac)(\?.*)?$/i.test(url) || 
                                    /audio|voice/i.test(filename)
                    const isPdf = /\.pdf(\?.*)?$/i.test(filename) || /\.pdf(\?.*)?$/i.test(url)
                    const textWithoutLink = msg.body.replace(match[0], '').trim()

                    return (
                      <div className="space-y-2">
                        {isImage ? (
                          <a href={url} target="_blank" rel="noopener noreferrer" className="block mt-1 overflow-hidden rounded-xl border border-white/20 shadow-sm max-w-xs hover:opacity-95 transition-opacity">
                            <img 
                              src={url} 
                              alt={filename} 
                              className="w-full h-auto max-h-48 object-cover rounded-xl"
                              onError={(e) => {
                                e.target.onerror = null
                                e.target.style.display = 'none'
                                if (e.target.parentElement) {
                                  e.target.parentElement.className = 'inline-flex items-center gap-2 px-3 py-1.5 bg-black/10 hover:bg-black/20 rounded-xl text-xs font-bold transition-colors underline'
                                  e.target.parentElement.innerText = `📎 ${filename || 'Image Attachment'}`
                                }
                              }}
                            />
                          </a>
                        ) : isVideo ? (
                          <div className="mt-1 overflow-hidden rounded-xl border border-white/20 shadow-sm max-w-xs bg-black">
                            <video controls preload="metadata" className="w-full h-auto max-h-48 rounded-xl" src={url}>
                              Your browser does not support video playback.
                            </video>
                          </div>
                        ) : isAudio ? (
                          <div className="mt-1 p-2 rounded-xl bg-black/10 border border-white/20 max-w-xs">
                            <audio controls className="w-full h-8" src={url}>
                              Your browser does not support audio playback.
                            </audio>
                            <div className="text-[10px] opacity-80 mt-1 truncate">🎵 {filename}</div>
                          </div>
                        ) : isPdf ? (
                          <a href={url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 px-3 py-2 bg-rose-50 hover:bg-rose-100 border border-rose-200 text-rose-800 rounded-xl font-bold transition-colors text-xs">
                            <span className="truncate max-w-[180px]">{filename}</span>
                            <span className="text-[10px] uppercase px-1.5 py-0.5 bg-rose-200/60 rounded text-rose-900 ml-1">PDF</span>
                          </a>
                        ) : (
                          <a href={url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 px-3 py-1.5 bg-black/10 hover:bg-black/20 rounded-xl text-xs font-bold transition-colors underline">
                            📎 {filename}
                          </a>
                        )}
                        {textWithoutLink && <p className="text-sm whitespace-pre-wrap leading-relaxed">{textWithoutLink}</p>}
                      </div>
                    )
                  }
                  if (msg.body_html) {
                    return (
                      <div
                        className="text-sm leading-relaxed prose prose-sm max-w-none"
                        dangerouslySetInnerHTML={{ __html: msg.body_html }}
                      />
                    )
                  }
                  return <div className="text-sm whitespace-pre-wrap leading-relaxed">{msg.body}</div>
                })()}
              </div>
              <div className="text-[10px] text-[#9598B0] mt-1.5 px-1 flex gap-2 font-medium">
                {isMe ? 'You' : (msg.sender_type === 'ai' ? '✨ SupportHub AI' : 'Agent User')} · {formatSmartTime(msg.created_at)}
              </div>
            </div>
          )
        })}

        {isTyping && (
          <div className="flex flex-col items-start">
            <div className="bg-[#F6F7FC] border border-[#E5E7F3] rounded-2xl rounded-bl-sm px-4 py-3 flex items-center gap-3 shadow-sm">
              <span className="text-xs font-semibold text-[#6C7089]">
                AI Assistant is typing
              </span>
              <div className="flex items-center gap-1">
                <div className="w-1.5 h-1.5 bg-[#6366F1] rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-1.5 h-1.5 bg-[#6366F1] rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-1.5 h-1.5 bg-[#6366F1] rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input or CSAT */}
      <div className="p-4 border-t border-[#E5E7F3] space-y-3">
        {isClosed ? (
          <>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-xl border border-[#E5E7F3]">
              <span className="text-xs font-semibold text-[#6C7089]">
                This conversation is resolved. Need further help?
              </span>
              <button
                onClick={async () => {
                  try {
                    await ticketsApi.reopen(ticketId)
                    setTicketStatus('open')
                    queryClient.invalidateQueries({ queryKey: ['ticket', ticketId] })
                    queryClient.invalidateQueries({ queryKey: ['tickets'] })
                  } catch (err) {
                    console.error('Reopen error:', err)
                  }
                }}
                className="px-3 py-1.5 bg-[#6366F1] hover:bg-[#4F46E5] text-white text-xs font-bold rounded-lg transition-colors cursor-pointer"
              >
                Reopen Conversation
              </button>
            </div>
            <CsatWidget ticketId={ticketId} />
          </>
        ) : (
          <form onSubmit={sendMessage} className="flex gap-2">
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
                    const res = await client.post(`/tickets/${ticketId}/upload`, formData, {
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
              title="Attach screenshot or file"
            >
              <Paperclip size={18} />
            </button>

            <input 
              type="text" 
              placeholder="Type a message..." 
              className="flex-1 border border-[#E5E7F3] rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
              value={inputText}
              onChange={e => setInputText(e.target.value)}
            />
            <button 
              type="submit" 
              disabled={!inputText.trim() || !ws}
              className="bg-[#6366F1] hover:bg-[#4F46E5] text-white px-5 rounded-xl transition-colors disabled:opacity-50 font-bold text-sm flex items-center gap-2"
            >
              <Send size={16} /> Send
            </button>
          </form>
        )}
      </div>
    </div>
  )
}

export default function CustomerLiveChat() {
  const navigate = useNavigate()
  const { id } = useParams()
  const queryClient = useQueryClient()

  // Feature 5: Ticket Filtering (Default: active)
  const [filter, setFilter] = useState('active') // 'active' | 'completed' | 'all'

  // Feature 6: Category Modal
  const [showCategoryModal, setShowCategoryModal] = useState(false)

  const { data: tickets = [], isLoading } = useQuery({
    queryKey: ['tickets', 'customer'],
    queryFn: async () => {
      const res = await ticketsApi.list()
      return res.data
    },
  })

  const newChatMutation = useMutation({
    mutationFn: async (category = "general") => {
      const res = await ticketsApi.create({
        subject: `${category.toUpperCase()} Support Query`,
        category: category,
        priority: "medium",
        channel: "website_chat",
        metadata: {}
      })
      return res.data
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries(['tickets'])
      setShowCategoryModal(false)
      navigate(`/customer/chat/${data.id}`)
    }
  })

  const filteredTickets = tickets.filter(t => {
    if (filter === 'active') return t.status !== 'resolved' && t.status !== 'closed'
    if (filter === 'completed') return t.status === 'resolved' || t.status === 'closed'
    return true
  })

  const handleFilterChange = (newFilter) => {
    setFilter(newFilter)
    navigate('/customer')
  }

  useEffect(() => {
    if (id && tickets.length > 0) {
      const selected = tickets.find(t => t.id === id)
      if (selected) {
        const isCompleted = selected.status === 'resolved' || selected.status === 'closed'
        if (isCompleted && filter === 'active') {
          setFilter('completed')
        }
      }
    }
  }, [id, tickets])

  const categories = [
    { id: 'billing', label: 'Billing & Payments', icon: CreditCard, color: 'bg-emerald-50 text-emerald-600 border-emerald-200' },
    { id: 'technical', label: 'Technical Issue', icon: Wrench, color: 'bg-indigo-50 text-indigo-600 border-indigo-200' },
    { id: 'account', label: 'Account & Profile', icon: UserIcon, color: 'bg-purple-50 text-purple-600 border-purple-200' },
    { id: 'general', label: 'General Question', icon: HelpCircle, color: 'bg-gray-50 text-gray-600 border-gray-200' },
  ]

  return (
    <div className="flex-1 flex flex-col p-8 overflow-hidden bg-[#F9FAFB] relative">
      <div className="mb-6 shrink-0">
        <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans'] text-[#1C1B2E]">Live Chat</h1>
        <p className="text-[#6C7089] text-sm">You're connected with our support team in real time.</p>
      </div>

      <div className="flex-1 flex min-h-0 drop-shadow-sm">
        {/* Left Pane - Chat History */}
        <div className="w-80 bg-white border border-[#E5E7F3] rounded-l-xl flex flex-col z-10 shrink-0">
          <div className="p-4 border-b border-[#E5E7F3]">
            <button 
              onClick={() => setShowCategoryModal(true)}
              className="w-full bg-[#A855F7] hover:bg-[#9333EA] text-white py-2.5 rounded-lg text-sm font-bold flex justify-center items-center gap-2 transition-colors"
            >
              <Plus size={16} /> New Chat
            </button>
          </div>

          {/* Ticket List Filters (Order: 1. Active, 2. Completed, 3. All) */}
          <div className="p-3 border-b border-[#E5E7F3] flex gap-1 bg-gray-50/50">
            {['active', 'completed', 'all'].map(f => (
              <button
                key={f}
                onClick={() => handleFilterChange(f)}
                className={`flex-1 py-1 rounded-md text-[11px] font-bold capitalize transition-colors ${
                  filter === f ? 'bg-white text-indigo-600 shadow-sm border border-indigo-100' : 'text-[#9598B0] hover:text-[#1C1B2E]'
                }`}
              >
                {f}
              </button>
            ))}
          </div>

          <div className="p-3 uppercase text-[10px] font-bold text-[#9598B0] tracking-wider">
            Chat History ({filteredTickets.length})
          </div>

          <div className="flex-1 overflow-y-auto px-2 pb-4 space-y-1">
            {isLoading ? (
              <div className="text-center py-4 text-sm text-[#9598B0]">Loading chats...</div>
            ) : filteredTickets.length === 0 ? (
              <div className="text-center py-4 text-sm text-[#9598B0]">No chats found.</div>
            ) : (
              filteredTickets.map(t => {
                const isActive = t.id.toString() === id
                return (
                  <div 
                    key={t.id} 
                    onClick={() => navigate(`/customer/chat/${t.id}`)}
                    className={`p-3 rounded-lg cursor-pointer transition-colors border-l-2 ${isActive ? 'bg-indigo-50/50 border-indigo-500' : 'border-transparent hover:bg-gray-50'}`}
                  >
                    <div className="flex justify-between items-start mb-1">
                      <div className={`text-sm font-bold truncate pr-2 ${isActive ? 'text-[#1C1B2E]' : 'text-[#6C7089]'}`}>
                        {t.subject}
                      </div>
                      <div className={`text-[9px] font-bold px-1.5 py-0.5 rounded uppercase shrink-0 ${
                        t.status === 'resolved' || t.status === 'closed' ? 'bg-gray-100 text-gray-500' : 'bg-emerald-100 text-emerald-600'
                      }`}>
                        {t.status === 'resolved' || t.status === 'closed' ? 'Completed' : 'Active'}
                      </div>
                    </div>
                    <div className="flex justify-between items-center text-[10px] text-[#9598B0] font-semibold mt-2">
                      <div>Linked: <span className="font-mono">{t.ref}</span></div>
                      <div>{formatSmartTime(t.updated_at || t.created_at)}</div>
                    </div>
                  </div>
                )
              })
            )}
          </div>
        </div>

        {/* Right Pane - Active Chat */}
        <ChatPane ticketId={id} />
      </div>

      {/* Feature 6: Category Picker Modal */}
      {showCategoryModal && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl p-6 max-w-md w-full border border-[#E5E7F3] shadow-xl">
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-bold text-[#1C1B2E] text-base">Select Support Category</h3>
              <button 
                onClick={() => setShowCategoryModal(false)}
                className="text-[#9598B0] hover:text-[#1C1B2E] p-1"
              >
                <X size={18} />
              </button>
            </div>
            <p className="text-xs text-[#6C7089] mb-6">Choose what you need help with so our AI can assist you better.</p>
            
            <div className="grid grid-cols-2 gap-3 mb-4">
              {categories.map(cat => {
                const IconComponent = cat.icon
                return (
                  <button
                    key={cat.id}
                    disabled={newChatMutation.isPending}
                    onClick={() => newChatMutation.mutate(cat.id)}
                    className={`p-4 rounded-xl border text-left flex flex-col justify-between hover:shadow-md transition-all ${cat.color}`}
                  >
                    <IconComponent size={20} className="mb-2" />
                    <span className="font-bold text-xs text-[#1C1B2E]">{cat.label}</span>
                  </button>
                )
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

