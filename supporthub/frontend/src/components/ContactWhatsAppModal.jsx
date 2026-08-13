import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { ticketsApi } from '../api/tickets'
import { Phone, X, Send, CheckCircle2, AlertCircle, ArrowRight, ExternalLink, MessageCircle, Bot } from 'lucide-react'

export default function ContactWhatsAppModal({ isOpen, onClose }) {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [subject, setSubject] = useState('')
  const [body, setBody] = useState('')
  const [category, setCategory] = useState('general')
  const [activeTab, setActiveTab] = useState('direct') // 'direct' | 'ticket'
  const [successTicket, setSuccessTicket] = useState(null)
  const [errorMsg, setErrorMsg] = useState('')

  const createWhatsAppTicketMutation = useMutation({
    mutationFn: (data) => ticketsApi.create(data),
    onSuccess: (res) => {
      queryClient.invalidateQueries(['tickets'])
      setSuccessTicket(res.data)
      setSubject('')
      setBody('')
    },
    onError: (err) => {
      setErrorMsg(err.response?.data?.detail || 'Failed to submit WhatsApp ticket inquiry.')
    }
  })

  if (!isOpen) return null

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!subject.trim() || !body.trim()) return

    createWhatsAppTicketMutation.mutate({
      subject,
      body,
      category,
      channel: 'whatsapp',
      priority: 'medium'
    })
  }

  const handleDone = () => {
    const createdId = successTicket?.id
    setSuccessTicket(null)
    setErrorMsg('')
    onClose()
    if (createdId) {
      navigate(`/customer/chat/${createdId}`)
    }
  }

  const waPhoneNumber = '+1 555-204-1051'
  const waDirectUrl = `https://wa.me/15552041051?text=${encodeURIComponent('Hi SupportHub AI Assistant, I need help with my account.')}`

  return (
    <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden border border-[#E5E7F3] animate-scaleIn">
        
        {/* Header */}
        <div className="flex justify-between items-center px-6 py-4 border-b border-[#E5E7F3] bg-gradient-to-r from-emerald-600 to-teal-700 text-white">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-white/20 flex items-center justify-center font-bold">
              <Phone size={20} />
            </div>
            <div>
              <h3 className="font-bold text-base font-['Plus_Jakarta_Sans']">Connect on WhatsApp</h3>
              <p className="text-[11px] text-emerald-100 font-medium">Instant 24/7 AI & Agent Support</p>
            </div>
          </div>
          <button 
            onClick={onClose} 
            className="text-emerald-100 hover:text-white p-1 rounded-lg hover:bg-white/10 transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* Modal Navigation Tabs */}
        {!successTicket && (
          <div className="flex border-b border-[#E5E7F3] bg-emerald-50/50 p-1 text-xs font-bold">
            <button
              type="button"
              onClick={() => setActiveTab('direct')}
              className={`flex-1 py-2 rounded-lg transition-all flex items-center justify-center gap-1.5 ${
                activeTab === 'direct' ? 'bg-white text-emerald-800 shadow-xs' : 'text-gray-600 hover:text-emerald-700'
              }`}
            >
              <MessageCircle size={14} /> Open WhatsApp Directly
            </button>
            <button
              type="button"
              onClick={() => setActiveTab('ticket')}
              className={`flex-1 py-2 rounded-lg transition-all flex items-center justify-center gap-1.5 ${
                activeTab === 'ticket' ? 'bg-white text-emerald-800 shadow-xs' : 'text-gray-600 hover:text-emerald-700'
              }`}
            >
              <Bot size={14} /> Submit WhatsApp Ticket
            </button>
          </div>
        )}

        {/* Content Body */}
        {successTicket ? (
          <div className="p-6 text-center space-y-4">
            <div className="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-2xl flex items-center justify-center mx-auto border border-emerald-200">
              <CheckCircle2 size={28} />
            </div>
            <h4 className="font-bold text-lg text-[#1C1B2E]">WhatsApp Ticket Created!</h4>
            <p className="text-xs text-[#6C7089] leading-relaxed">
              Your inquiry has been assigned WhatsApp Ticket <span className="font-mono font-bold text-emerald-600">{successTicket.ref}</span>. Our AI Support Assistant has dispatched an immediate response.
            </p>
            <button
              onClick={handleDone}
              className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold text-xs transition-colors shadow-xs flex items-center justify-center gap-1.5"
            >
              View Ticket Conversation <ArrowRight size={14} />
            </button>
          </div>
        ) : activeTab === 'direct' ? (
          <div className="p-6 space-y-5 text-center">
            <div className="bg-emerald-50 rounded-2xl p-5 border border-emerald-200 space-y-3">
              <div className="w-14 h-14 bg-emerald-600 text-white rounded-2xl flex items-center justify-center mx-auto shadow-md">
                <Phone size={28} />
              </div>
              <div>
                <h4 className="font-bold text-base text-[#1C1B2E]">SupportHub Official WhatsApp</h4>
                <p className="text-xs text-emerald-700 font-mono font-bold mt-1">{waPhoneNumber}</p>
              </div>
              <p className="text-[11px] text-[#6C7089] leading-relaxed">
                Scan or click below to start a live WhatsApp chat on your smartphone or desktop. AI response guaranteed within 3 seconds.
              </p>
            </div>

            <a
              href={waDirectUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="w-full py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold text-xs transition-all shadow-md flex items-center justify-center gap-2"
            >
              <span>Launch WhatsApp Chat</span>
              <ExternalLink size={15} />
            </a>

            <div className="text-[10px] text-[#9598B0]">
              Available 24/7 • Automatic SLA ticket generation enabled
            </div>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="p-6 space-y-4 text-xs">
            {errorMsg && (
              <div className="flex items-center gap-2 p-3 bg-rose-50 text-rose-600 text-xs rounded-xl font-medium">
                <AlertCircle size={16} />
                <span>{errorMsg}</span>
              </div>
            )}

            <div>
              <label className="block font-bold text-[#6C7089] uppercase text-[10px] mb-1">Subject</label>
              <input
                type="text"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                placeholder="What do you need assistance with?"
                className="w-full px-3.5 py-2.5 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-xs focus:outline-none focus:border-emerald-500 font-medium"
                required
              />
            </div>

            <div>
              <label className="block font-bold text-[#6C7089] uppercase text-[10px] mb-1">Category</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full px-3.5 py-2.5 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-xs focus:outline-none focus:border-emerald-500 font-medium capitalize"
              >
                <option value="general">General Inquiry</option>
                <option value="billing">Billing & Orders</option>
                <option value="technical">Technical Support</option>
                <option value="account">Account & Login</option>
              </select>
            </div>

            <div>
              <label className="block font-bold text-[#6C7089] uppercase text-[10px] mb-1">Message Detail</label>
              <textarea
                rows={4}
                value={body}
                onChange={(e) => setBody(e.target.value)}
                placeholder="Write your issue details here. Our WhatsApp AI bot will process it immediately..."
                className="w-full px-3.5 py-2.5 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-xs focus:outline-none focus:border-emerald-500 font-medium"
                required
              />
            </div>

            <div className="flex justify-end gap-2 pt-2 border-t border-[#E5E7F3]">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-xs font-semibold text-gray-600 hover:bg-gray-100 rounded-xl"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={createWhatsAppTicketMutation.isPending}
                className="px-5 py-2 text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-xl flex items-center gap-1.5 transition-colors disabled:opacity-50 shadow-xs"
              >
                <Send size={14} />
                {createWhatsAppTicketMutation.isPending ? 'Submitting...' : 'Submit Ticket'}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  )
}
