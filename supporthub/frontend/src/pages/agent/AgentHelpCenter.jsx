import { useState } from 'react'
import { Search, Bell, ExternalLink, Check, BookOpen, ShieldCheck, FileText, RefreshCw, Truck, ShieldAlert } from 'lucide-react'

export default function AgentHelpCenter() {
  const [searchTerm, setSearchTerm] = useState('')
  const [copiedId, setCopiedId] = useState(null)
  const [activeCategory, setActiveCategory] = useState('all')

  const companyPolicies = [
    {
      id: 'pol-1',
      code: 'POL-001',
      title: 'ShopKart Return & Refund Policy',
      category: 'Returns & Refunds',
      icon: RefreshCw,
      helpful: '98% helpful',
      summary: 'Comprehensive guidelines for returns, damaged item reporting within 48 hours, and 5-7 business days refund timelines.',
      content: `1. Report Within 48 Hours: Report damage immediately from My Orders → Item Damaged on Arrival. Attach clear photographs of the outer box and courier label.
2. Return Eligibility: Products must be in original condition with tags intact. Returns accepted within 30 days of delivery.
3. Refund Processing: Refunds are credited back to original payment method within 5-7 business days post quality inspection.`
    },
    {
      id: 'pol-2',
      code: 'POL-002',
      title: 'Order Cancellation & Shipping Policy',
      category: 'Shipping & Delivery',
      icon: Truck,
      helpful: '95% helpful',
      summary: 'Standard delivery timelines (3-5 days metro), free cancellation prior to dispatch, and courier tracking information.',
      content: `1. Order Cancellation: Orders can be cancelled free of charge before shipment dispatch directly from the orders page.
2. Shipping Timelines: Standard metro delivery takes 3-5 business days. Non-metro locations take 5-7 business days.
3. Courier Scan Updates: Live tracking is updated every 6 hours via Shadowfax and Delhivery integrations.`
    },
    {
      id: 'pol-3',
      code: 'POL-003',
      title: 'Payment Security & Refund Escalation Terms',
      category: 'Payments & Billing',
      icon: ShieldCheck,
      helpful: '96% helpful',
      summary: 'Automatic UPI and card refund timelines, failed payment resolution, and payment gateway security compliance.',
      content: `1. Failed Payments: Debited funds for failed transactions auto-refund within 24-48 hours.
2. Gateway Security: All transactions are processed through 256-bit SSL encrypted PCI-DSS compliant payment gateways.
3. Refund Escalations: Senior agent authorization required for goodwill store credit or manual bank transfer overrides.`
    },
    {
      id: 'pol-4',
      code: 'POL-004',
      title: 'Product Warranty & Replacement Policy',
      category: 'Warranty & Claims',
      icon: ShieldAlert,
      helpful: '92% helpful',
      summary: '1-year brand warranty on electronics, replacement request steps, and authorized service center claim procedures.',
      content: `1. Warranty Coverage: All electronic devices include 1-year brand warranty covering manufacturing defects.
2. Replacement Claim: Submit invoice copy and issue video to request an immediate door-step replacement pickup.
3. Non-Coverage: Physical damage, liquid exposure, or unauthorized repair voids brand warranty.`
    }
  ]

  const handleShare = (art) => {
    const textToCopy = `${art.title} (${art.code}):\n${art.content}`
    navigator.clipboard.writeText(textToCopy)
    setCopiedId(art.id)
    setTimeout(() => setCopiedId(null), 2000)
  }

  const categories = ['all', 'Returns & Refunds', 'Shipping & Delivery', 'Payments & Billing', 'Warranty & Claims']

  const filtered = companyPolicies.filter(a => {
    const matchesSearch = a.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      a.summary.toLowerCase().includes(searchTerm.toLowerCase()) ||
      a.code.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory = activeCategory === 'all' || a.category === activeCategory
    return matchesSearch && matchesCategory
  })

  return (
    <div className="flex-1 flex flex-col h-screen bg-[#F6F7FC] overflow-hidden text-[#1C1B2E]">
      {/* Top Header Bar */}
      <div className="h-16 bg-white border-b border-[#E5E7F3] px-8 flex items-center justify-between shrink-0 shadow-2xs">
        <div className="flex items-center gap-2">
          <BookOpen className="text-indigo-600" size={20} />
          <h1 className="text-lg font-extrabold font-['Plus_Jakarta_Sans'] text-[#1C1B2E]">
            Knowledge Base & Official Company Policies
          </h1>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-y-auto p-8 space-y-6">
        <div>
          <h2 className="text-2xl font-extrabold tracking-tight font-['Plus_Jakarta_Sans'] text-[#1C1B2E]">
            Company Policy Reference & Knowledge Base
          </h2>
          <p className="text-[#6C7089] text-xs mt-1 font-medium">
            Search official company guidelines, return timelines, and policy rules to answer customer queries with 100% accuracy.
          </p>
        </div>

        {/* Search & Category Filter Header */}
        <div className="bg-white p-5 rounded-3xl border border-[#E5E7F3] shadow-sm space-y-4">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-[#9598B0]" size={18} />
            <input
              type="text"
              placeholder="Search company policies by code (e.g. POL-001), keywords, or terms..."
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-2xl pl-11 pr-4 py-3.5 text-xs outline-none focus:border-indigo-500 focus:bg-white transition-all font-medium"
            />
          </div>

          <div className="flex flex-wrap gap-2 pt-1">
            {categories.map(cat => (
              <button
                key={cat}
                onClick={() => setActiveCategory(cat)}
                className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all ${
                  activeCategory === cat
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/20'
                    : 'bg-[#F6F7FC] text-[#6C7089] hover:bg-gray-100 hover:text-[#1C1B2E] border border-[#E5E7F3]'
                }`}
              >
                {cat === 'all' ? 'All Policies' : cat}
              </button>
            ))}
          </div>
        </div>

        {/* Policy Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filtered.map(art => {
            const IconComp = art.icon
            return (
              <div key={art.id} className="bg-white p-6 rounded-3xl border border-[#E5E7F3] shadow-sm flex flex-col justify-between space-y-5 hover:border-indigo-300 transition-all group">
                <div className="space-y-3">
                  <div className="flex justify-between items-start">
                    <div className="flex items-center gap-2.5">
                      <div className="w-10 h-10 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold shadow-2xs group-hover:bg-indigo-600 group-hover:text-white transition-colors">
                        <IconComp size={20} />
                      </div>
                      <div>
                        <span className="text-[10px] font-mono font-extrabold text-indigo-600 bg-indigo-50 border border-indigo-200 px-2 py-0.5 rounded-md">
                          {art.code}
                        </span>
                        <h3 className="font-extrabold text-sm text-[#1C1B2E] leading-snug mt-1">{art.title}</h3>
                      </div>
                    </div>
                    <span className="text-[10px] font-bold px-2.5 py-1 rounded-full bg-gray-100 text-[#6C7089]">
                      {art.category}
                    </span>
                  </div>

                  <p className="text-xs text-[#6C7089] leading-relaxed font-medium">
                    {art.summary}
                  </p>

                  <div className="p-3.5 bg-gray-50 border border-gray-200/80 rounded-2xl text-[11px] text-[#1C1B2E] leading-relaxed font-mono whitespace-pre-wrap">
                    {art.content}
                  </div>
                </div>

                <div className="flex justify-between items-center pt-2 border-t border-gray-100">
                  <span className="text-xs text-[#9598B0] font-semibold">{art.helpful}</span>
                  <button
                    onClick={() => handleShare(art)}
                    className={`inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-extrabold transition-all ${
                      copiedId === art.id 
                        ? 'bg-emerald-500 text-white shadow-sm' 
                        : 'bg-[#F6F7FC] hover:bg-indigo-50 text-indigo-700 border border-indigo-200/80 hover:border-indigo-300'
                    }`}
                  >
                    {copiedId === art.id ? (
                      <>
                        <Check size={14} /> Copy to Composer!
                      </>
                    ) : (
                      <>
                        <FileText size={14} /> Copy Policy Text
                      </>
                    )}
                  </button>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
