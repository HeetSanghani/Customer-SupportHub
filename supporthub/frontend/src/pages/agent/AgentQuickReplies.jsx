import { useState } from 'react'
import { Search, Bell, Copy, Check, Zap } from 'lucide-react'

export default function AgentQuickReplies() {
  const [searchTerm, setSearchTerm] = useState('')
  const [copiedId, setCopiedId] = useState(null)

  const quickReplies = [
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

  const handleCopy = (reply) => {
    navigator.clipboard.writeText(reply.content)
    setCopiedId(reply.id)
    setTimeout(() => setCopiedId(null), 2000)
  }

  const filtered = quickReplies.filter(r => 
    r.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    r.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
    r.content.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="flex-1 flex flex-col h-screen bg-[#F6F7FC] overflow-hidden text-[#1C1B2E]">
      {/* Top Header Bar */}
      <div className="h-16 bg-white border-b border-[#E5E7F3] px-8 flex items-center justify-between shrink-0">
        <h1 className="text-xl font-bold font-['Plus_Jakarta_Sans']">Quick Replies</h1>
        <div className="flex items-center gap-4">
          <div className="relative w-80">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-[#9598B0]" size={16} />
            <input
              type="text"
              placeholder="Search tickets, customers, articles..."
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl pl-9 pr-4 py-2 text-xs outline-none focus:border-indigo-500 transition-colors"
            />
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-y-auto p-8">
        <div className="mb-6">
          <h2 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">Quick Replies</h2>
          <p className="text-[#6C7089] text-xs mt-0.5">Pre-written replies to answer common questions faster.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map(reply => (
            <div key={reply.id} className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm flex flex-col justify-between space-y-4 hover:border-indigo-200 transition-all">
              <div>
                <div className="flex justify-between items-start mb-3">
                  <h3 className="font-bold text-sm text-[#1C1B2E]">{reply.title}</h3>
                  <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-gray-100 text-[#6C7089]">
                    {reply.category}
                  </span>
                </div>
                <p className="text-xs text-[#6C7089] italic bg-[#F9FAFB] p-3.5 rounded-xl border border-[#E5E7F3] leading-relaxed">
                  "{reply.content}"
                </p>
              </div>

              <button
                onClick={() => handleCopy(reply)}
                className={`w-full py-2 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-1.5 ${
                  copiedId === reply.id 
                    ? 'bg-emerald-500 text-white' 
                    : 'bg-[#F6F7FC] hover:bg-indigo-50 text-[#1C1B2E] hover:text-indigo-600 border border-[#E5E7F3]'
                }`}
              >
                {copiedId === reply.id ? (
                  <>
                    <Check size={14} /> Copied to clipboard!
                  </>
                ) : (
                  'Insert into reply'
                )}
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
