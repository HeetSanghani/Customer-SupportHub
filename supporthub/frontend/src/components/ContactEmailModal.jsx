import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { ticketsApi } from '../api/tickets'
import { Mail, X, Send, CheckCircle2, AlertCircle, ArrowRight } from 'lucide-react'

export default function ContactEmailModal({ isOpen, onClose }) {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [subject, setSubject] = useState('')
  const [body, setBody] = useState('')
  const [category, setCategory] = useState('general')
  const [successTicket, setSuccessTicket] = useState(null)
  const [errorMsg, setErrorMsg] = useState('')

  const createEmailTicketMutation = useMutation({
    mutationFn: (data) => ticketsApi.create(data),
    onSuccess: (res) => {
      queryClient.invalidateQueries(['tickets'])
      setSuccessTicket(res.data)
      setSubject('')
      setBody('')
    },
    onError: (err) => {
      setErrorMsg(err.response?.data?.detail || 'Failed to submit email inquiry.')
    }
  })

  if (!isOpen) return null

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!subject.trim() || !body.trim()) return

    createEmailTicketMutation.mutate({
      subject,
      body,
      category,
      channel: 'email',
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

  return (
    <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden border border-[#E5E7F3] animate-scaleIn">
        {/* Header */}
        <div className="flex justify-between items-center px-6 py-4 border-b border-[#E5E7F3] bg-gradient-to-r from-blue-50 to-indigo-50">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-blue-600 text-white flex items-center justify-center font-bold">
              <Mail size={18} />
            </div>
            <div>
              <h3 className="font-bold text-base text-[#1C1B2E]">Contact via Email</h3>
              <p className="text-[11px] text-[#6C7089]">Send a direct inquiry to our email support desk</p>
            </div>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 p-1 rounded-lg">
            <X size={18} />
          </button>
        </div>

        {/* Content */}
        {successTicket ? (
          <div className="p-6 text-center space-y-4">
            <div className="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-2xl flex items-center justify-center mx-auto">
              <CheckCircle2 size={28} />
            </div>
            <h4 className="font-bold text-lg text-[#1C1B2E]">Email Inquiry Sent!</h4>
            <p className="text-xs text-[#6C7089] leading-relaxed">
              Your message has been converted to Email Support Ticket <span className="font-mono font-bold text-indigo-600">{successTicket.ref}</span>. An automated acknowledgement has been dispatched.
            </p>
            <button
              onClick={handleDone}
              className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-bold text-xs transition-colors shadow-sm flex items-center justify-center gap-1.5"
            >
              View Ticket Thread <ArrowRight size={14} />
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="p-6 space-y-4">
            {errorMsg && (
              <div className="flex items-center gap-2 p-3 bg-red-50 text-red-600 text-xs rounded-xl font-medium">
                <AlertCircle size={16} />
                <span>{errorMsg}</span>
              </div>
            )}

            <div>
              <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Subject</label>
              <input
                type="text"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                placeholder="Brief summary of your question or issue"
                className="w-full px-3.5 py-2.5 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-xs focus:outline-none focus:border-indigo-500 font-medium"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Category</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full px-3.5 py-2.5 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-xs focus:outline-none focus:border-indigo-500 font-medium capitalize"
              >
                <option value="general">General Support</option>
                <option value="billing">Billing & Refund</option>
                <option value="technical">Technical Support</option>
                <option value="account">Account Access</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Message Body</label>
              <textarea
                rows={4}
                value={body}
                onChange={(e) => setBody(e.target.value)}
                placeholder="Describe your inquiry in detail..."
                className="w-full px-3.5 py-2.5 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-xs focus:outline-none focus:border-indigo-500 font-medium"
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
                disabled={createEmailTicketMutation.isPending}
                className="px-5 py-2 text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl flex items-center gap-1.5 transition-colors disabled:opacity-50 shadow-sm"
              >
                <Send size={14} />
                {createEmailTicketMutation.isPending ? 'Sending...' : 'Send Inquiry'}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  )
}
