import { useState } from 'react'
import { Search, Bell, ExternalLink, Check, BookOpen } from 'lucide-react'

export default function AgentHelpCenter() {
  const [searchTerm, setSearchTerm] = useState('')
  const [copiedId, setCopiedId] = useState(null)

  const articles = [
    {
      id: '1',
      title: 'How to reset your account password',
      views: '12.4k views',
      helpful: '96% helpful',
      category: 'Account',
      link: 'https://supporthub.help/reset-password'
    },
    {
      id: '2',
      title: 'Understanding your monthly invoice',
      views: '9.8k views',
      helpful: '92% helpful',
      category: 'Billing',
      link: 'https://supporthub.help/monthly-invoice'
    },
    {
      id: '3',
      title: 'Tracking your order shipment',
      views: '15.1k views',
      helpful: '94% helpful',
      category: 'Orders',
      link: 'https://supporthub.help/order-tracking'
    },
    {
      id: '4',
      title: 'Refund policy and processing timelines',
      views: '11.2k views',
      helpful: '89% helpful',
      category: 'Refunds',
      link: 'https://supporthub.help/refund-policy'
    },
    {
      id: '5',
      title: 'Updating your payment method',
      views: '7.5k views',
      helpful: '91% helpful',
      category: 'Billing',
      link: 'https://supporthub.help/update-payment'
    },
    {
      id: '6',
      title: 'Troubleshooting login issues',
      views: '13.9k views',
      helpful: '95% helpful',
      category: 'Account',
      link: 'https://supporthub.help/troubleshoot-login'
    }
  ]

  const handleShare = (art) => {
    navigator.clipboard.writeText(art.link)
    setCopiedId(art.id)
    setTimeout(() => setCopiedId(null), 2000)
  }

  const filtered = articles.filter(a =>
    a.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    a.category.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="flex-1 flex flex-col h-screen bg-[#F6F7FC] overflow-hidden text-[#1C1B2E]">
      {/* Top Header Bar */}
      <div className="h-16 bg-white border-b border-[#E5E7F3] px-8 flex items-center justify-between shrink-0">
        <h1 className="text-xl font-bold font-['Plus_Jakarta_Sans']">Help Center</h1>
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
          <div className="relative cursor-pointer p-2 rounded-xl hover:bg-gray-100 transition-colors text-[#6C7089]">
            <Bell size={18} />
            <span className="absolute top-1 right-1 w-4 h-4 bg-rose-500 text-white font-bold text-[9px] rounded-full flex items-center justify-center">4</span>
          </div>
          <div className="w-8 h-8 rounded-full bg-indigo-600 text-white font-bold text-xs flex items-center justify-center">
            EW
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-y-auto p-8 space-y-6">
        <div>
          <h2 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">Help Center Search</h2>
          <p className="text-[#6C7089] text-xs mt-0.5">Search articles to answer customers faster, or share a link directly in a reply.</p>
        </div>

        {/* Search Bar Input */}
        <div className="bg-white p-4 rounded-2xl border border-[#E5E7F3] shadow-sm">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-[#9598B0]" size={18} />
            <input
              type="text"
              placeholder="Search articles..."
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl pl-11 pr-4 py-3 text-xs outline-none focus:border-indigo-500 transition-colors"
            />
          </div>
        </div>

        {/* Articles Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filtered.map(art => (
            <div key={art.id} className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm flex flex-col justify-between space-y-4 hover:border-indigo-200 transition-all">
              <div>
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-bold text-sm text-[#1C1B2E] max-w-[75%] leading-snug">{art.title}</h3>
                  <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-gray-100 text-[#6C7089]">
                    {art.category}
                  </span>
                </div>
                <div className="text-xs text-[#9598B0]">
                  {art.views} · <span className="text-emerald-600 font-semibold">{art.helpful}</span>
                </div>
              </div>

              <div>
                <button
                  onClick={() => handleShare(art)}
                  className={`inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                    copiedId === art.id 
                      ? 'bg-emerald-500 text-white' 
                      : 'bg-[#F6F7FC] hover:bg-indigo-50 text-[#1C1B2E] hover:text-indigo-600 border border-[#E5E7F3]'
                  }`}
                >
                  {copiedId === art.id ? (
                    <>
                      <Check size={14} /> Link copied!
                    </>
                  ) : (
                    <>
                      <ExternalLink size={14} /> Share with customer
                    </>
                  )}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
