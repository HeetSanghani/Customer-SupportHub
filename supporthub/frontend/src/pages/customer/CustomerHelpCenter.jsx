import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate, Link } from 'react-router-dom'
import { 
  Search, BookOpen, ThumbsUp, Eye, MessageSquare, 
  HelpCircle, ChevronDown, ChevronUp, Sparkles, CheckCircle2,
  ShieldCheck, CreditCard, Wrench, User, ArrowLeft
} from 'lucide-react'
import { knowledgeApi } from '../../api/knowledge'

export default function CustomerHelpCenter() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('All')
  const [expandedId, setExpandedId] = useState(null)
  const [votedIds, setVotedIds] = useState(new Set())

  // Fetch published articles
  const { data: articles = [], isLoading } = useQuery({
    queryKey: ['customer-kb-articles'],
    queryFn: async () => {
      const res = await knowledgeApi.list({ published_only: true, limit: 100 })
      return res.data
    }
  })

  // Helpful vote mutation
  const voteMutation = useMutation({
    mutationFn: async (id) => {
      const res = await knowledgeApi.markHelpful(id)
      return res.data
    },
    onSuccess: (data) => {
      setVotedIds(prev => new Set(prev).add(data.id))
      queryClient.invalidateQueries({ queryKey: ['customer-kb-articles'] })
    }
  })

  // Categories metadata
  const categories = [
    { id: 'All', label: 'All Articles', icon: BookOpen },
    { id: 'Billing', label: 'Billing & Invoices', icon: CreditCard },
    { id: 'Technical', label: 'Technical & Chat', icon: Wrench },
    { id: 'Account', label: 'Account & Security', icon: User },
    { id: 'General', label: 'General & Policies', icon: HelpCircle },
  ]

  // Filter articles based on category and search query
  const filteredArticles = articles.filter(a => {
    const matchesCategory = selectedCategory === 'All' || a.category?.toLowerCase() === selectedCategory.toLowerCase()
    const query = searchQuery.toLowerCase().trim()
    const matchesSearch = !query || 
      a.title?.toLowerCase().includes(query) || 
      a.body?.toLowerCase().includes(query) ||
      a.category?.toLowerCase().includes(query)

    return matchesCategory && matchesSearch
  })

  const toggleExpand = (id) => {
    setExpandedId(prev => prev === id ? null : id)
  }

  return (
    <div className="flex-1 h-full bg-[#F8FAFC] overflow-y-auto text-[#0F172A]">
      {/* Hero Header */}
      <div className="relative bg-gradient-to-r from-indigo-700 via-indigo-600 to-purple-600 text-white px-6 md:px-8 py-10 shadow-md">
        <div className="max-w-4xl mx-auto space-y-4">
          <Link to="/customer" className="inline-flex items-center gap-1.5 text-xs font-extrabold text-indigo-100 hover:text-white mb-2 transition-colors">
            <ArrowLeft size={14} /> Back to AI Chat
          </Link>
          <div className="text-center space-y-3">
            <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-md px-3.5 py-1 rounded-full text-xs font-semibold tracking-wide border border-white/20">
              <Sparkles size={14} className="text-amber-300" /> SupportHub Help Center
            </div>
            <h1 className="text-2xl md:text-4xl font-black tracking-tight">
              How can we help you today?
            </h1>
            <p className="text-indigo-100 text-xs md:text-sm max-w-xl mx-auto font-medium">
              Search our knowledge base, guides, and FAQs for instant answers to common questions.
            </p>

            {/* Search Input */}
            <div className="relative max-w-2xl mx-auto mt-6">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="text"
                placeholder="Search by keyword, billing, live chat, 2FA..."
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                className="w-full pl-12 pr-4 py-3.5 rounded-2xl bg-white text-[#0F172A] placeholder-gray-400 text-sm font-medium shadow-xl border-0 focus:ring-4 focus:ring-indigo-300 outline-none transition-all"
              />
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery('')}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-xs text-gray-400 hover:text-gray-600 bg-gray-100 px-2 py-1 rounded-md"
                >
                  Clear
                </button>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="max-w-5xl mx-auto px-6 py-8 space-y-8">
        
        {/* Category Pills */}
        <div className="flex flex-wrap items-center justify-center gap-2.5">
          {categories.map(cat => {
            const Icon = cat.icon
            const isSelected = selectedCategory === cat.id
            const count = cat.id === 'All' 
              ? articles.length 
              : articles.filter(a => a.category?.toLowerCase() === cat.id.toLowerCase()).length

            return (
              <button
                key={cat.id}
                onClick={() => setSelectedCategory(cat.id)}
                className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-bold transition-all shadow-xs ${
                  isSelected 
                    ? 'bg-indigo-600 text-white shadow-md scale-105' 
                    : 'bg-white text-[#64748B] hover:bg-indigo-50/60 hover:text-indigo-600 border border-[#E2E8F0]'
                }`}
              >
                <Icon size={16} />
                <span>{cat.label}</span>
                <span className={`px-2 py-0.5 rounded-full text-[10px] ${isSelected ? 'bg-white/20 text-white' : 'bg-gray-100 text-gray-600'}`}>
                  {count}
                </span>
              </button>
            )
          })}
        </div>

        {/* FAQs List */}
        <div className="space-y-4">
          <div className="flex items-center justify-between px-1">
            <h2 className="text-lg font-bold text-[#0F172A] flex items-center gap-2">
              <BookOpen size={18} className="text-indigo-600" />
              {selectedCategory === 'All' ? 'Frequently Asked Questions' : `${selectedCategory} Articles`}
            </h2>
            <span className="text-xs text-[#94A3B8] font-semibold">
              Showing {filteredArticles.length} article{filteredArticles.length === 1 ? '' : 's'}
            </span>
          </div>

          {isLoading ? (
            <div className="bg-white rounded-3xl p-12 text-center text-gray-400 font-medium border border-gray-200">
              Loading knowledge base articles...
            </div>
          ) : filteredArticles.length === 0 ? (
            <div className="bg-white rounded-3xl p-12 text-center space-y-3 border border-gray-200 shadow-2xs">
              <HelpCircle size={40} className="mx-auto text-gray-300" />
              <h3 className="text-base font-bold text-gray-700">No matching articles found</h3>
              <p className="text-xs text-gray-500 max-w-md mx-auto">
                We couldn't find any articles matching "{searchQuery}". Try searching with different keywords or connect with our support team.
              </p>
              <button
                onClick={() => navigate('/customer/chat')}
                className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold px-5 py-2.5 rounded-xl transition-colors mt-2"
              >
                <MessageSquare size={16} /> Ask SupportHub AI
              </button>
            </div>
          ) : (
            <div className="space-y-3">
              {filteredArticles.map(article => {
                const isExpanded = expandedId === article.id
                const hasVoted = votedIds.has(article.id)

                return (
                  <div
                    key={article.id}
                    className={`bg-white rounded-3xl border transition-all overflow-hidden ${
                      isExpanded ? 'border-indigo-300 shadow-md ring-2 ring-indigo-50/50' : 'border-[#E2E8F0] hover:border-indigo-200 shadow-2xs'
                    }`}
                  >
                    {/* Header Bar */}
                    <button
                      onClick={() => toggleExpand(article.id)}
                      className="w-full p-5 text-left flex items-center justify-between gap-4 focus:outline-none"
                    >
                      <div className="flex items-start gap-3 flex-1">
                        <div className="mt-0.5 p-2 bg-indigo-50 text-indigo-600 rounded-xl">
                          <HelpCircle size={18} />
                        </div>
                        <div>
                          <h3 className="text-sm font-bold text-[#0F172A] group-hover:text-indigo-600 transition-colors">
                            {article.title}
                          </h3>
                          <div className="flex items-center gap-3 mt-1.5 text-xs text-[#94A3B8]">
                            <span className="bg-slate-100 text-slate-700 font-semibold px-2 py-0.5 rounded-md text-[10px] uppercase">
                              {article.category}
                            </span>
                            <span className="flex items-center gap-1">
                              <Eye size={12} /> {article.views} views
                            </span>
                            <span className="flex items-center gap-1 text-emerald-600 font-semibold">
                              <ThumbsUp size={12} /> {article.helpful_count} helpful votes
                            </span>
                          </div>
                        </div>
                      </div>
                      <div className="text-gray-400 p-1 rounded-lg hover:bg-gray-100">
                        {isExpanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                      </div>
                    </button>

                    {/* Article Body */}
                    {isExpanded && (
                      <div className="px-6 pb-6 pt-2 border-t border-gray-100 space-y-4">
                        <div className="text-sm text-gray-700 leading-relaxed whitespace-pre-line bg-gray-50/70 p-4 rounded-2xl border border-gray-100 font-normal">
                          {article.body}
                        </div>

                        {/* Article Footer & Feedback */}
                        <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-2">
                          <div className="flex items-center gap-2">
                            <span className="text-xs font-semibold text-gray-500">Was this article helpful?</span>
                            <button
                              disabled={hasVoted || voteMutation.isPending}
                              onClick={() => voteMutation.mutate(article.id)}
                              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                                hasVoted
                                  ? 'bg-emerald-100 text-emerald-700 border border-emerald-200'
                                  : 'bg-indigo-50 hover:bg-indigo-100 text-indigo-600 border border-indigo-100'
                              }`}
                            >
                              {hasVoted ? (
                                <>
                                  <CheckCircle2 size={14} /> Thank you for voting!
                                </>
                              ) : (
                                <>
                                  <ThumbsUp size={14} /> Yes ({article.helpful_count})
                                </>
                              )}
                            </button>
                          </div>

                          <button
                            onClick={() => navigate('/customer/chat')}
                            className="text-xs font-bold text-indigo-600 hover:text-indigo-800 flex items-center gap-1 hover:underline"
                          >
                            Still need help with this? Chat now &rarr;
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          )}
        </div>

        {/* Support Banners: Live Chat & WhatsApp */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Live Chat Banner */}
          <div className="bg-gradient-to-r from-slate-900 to-indigo-950 text-white rounded-3xl p-6 shadow-xl flex flex-col justify-between space-y-4 border border-slate-800">
            <div className="space-y-1.5">
              <div className="inline-flex items-center gap-1.5 text-[10px] font-bold text-[#818CF8] bg-indigo-500/10 border border-indigo-500/20 px-2.5 py-0.5 rounded-full uppercase tracking-wider">
                <Sparkles size={12} /> Live Web Chat
              </div>
              <h3 className="text-lg font-extrabold tracking-tight">
                Didn't find your answer?
              </h3>
              <p className="text-slate-300 text-xs leading-relaxed">
                Chat directly with our web AI Assistant and live support agent team in real time.
              </p>
            </div>
            <button
              onClick={() => navigate('/customer/chat')}
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2.5 rounded-xl text-xs font-bold shadow-md transition-all flex items-center justify-center gap-2"
            >
              <MessageSquare size={16} /> Open Web Live Chat
            </button>
          </div>

          {/* WhatsApp Support Banner */}
          <div className="bg-gradient-to-r from-emerald-900 via-teal-950 to-emerald-950 text-white rounded-3xl p-6 shadow-xl flex flex-col justify-between space-y-4 border border-emerald-800/50">
            <div className="space-y-1.5">
              <div className="inline-flex items-center gap-1.5 text-[10px] font-bold text-emerald-300 bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-0.5 rounded-full uppercase tracking-wider">
                <Sparkles size={12} /> WhatsApp 24/7 Bot
              </div>
              <h3 className="text-lg font-extrabold tracking-tight">
                Prefer WhatsApp on Mobile?
              </h3>
              <p className="text-emerald-100 text-xs leading-relaxed">
                Send a message to <span className="font-mono font-bold text-emerald-300">+1 555-204-1051</span> to chat with our automated WhatsApp Support Assistant.
              </p>
            </div>
            <a
              href="https://wa.me/15552041051?text=Hi%20SupportHub%20AI%20Assistant,%20I%20need%20help."
              target="_blank"
              rel="noopener noreferrer"
              className="bg-emerald-500 hover:bg-emerald-600 text-white px-5 py-2.5 rounded-xl text-xs font-bold shadow-md transition-all flex items-center justify-center gap-2"
            >
              <span>Launch WhatsApp Chat</span>
            </a>
          </div>
        </div>

      </div>
    </div>
  )
}
