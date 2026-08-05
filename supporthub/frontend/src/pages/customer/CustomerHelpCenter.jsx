import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { 
  Search, BookOpen, ThumbsUp, Eye, MessageSquare, 
  HelpCircle, ChevronDown, ChevronUp, Sparkles, CheckCircle2,
  ShieldCheck, CreditCard, Wrench, User
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
    <div className="flex-1 bg-[#F8FAFC] min-h-screen overflow-y-auto text-[#1C1B2E]">
      {/* Hero Header */}
      <div className="relative bg-gradient-to-r from-[#4F46E5] via-[#6366F1] to-[#818CF8] text-white px-8 py-12 shadow-md">
        <div className="max-w-4xl mx-auto text-center space-y-4">
          <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-md px-3.5 py-1 rounded-full text-xs font-semibold tracking-wide border border-white/20">
            <Sparkles size={14} className="text-amber-300" /> SupportHub Help Center
          </div>
          <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight">
            How can we help you today?
          </h1>
          <p className="text-indigo-100 text-sm md:text-base max-w-xl mx-auto font-medium">
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
              className="w-full pl-12 pr-4 py-4 rounded-2xl bg-white text-[#1C1B2E] placeholder-gray-400 text-sm font-medium shadow-xl border-0 focus:ring-4 focus:ring-indigo-300 outline-none transition-all"
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

      {/* Main Content Area */}
      <div className="max-w-5xl mx-auto px-6 py-10 space-y-8">
        
        {/* Category Pills */}
        <div className="flex flex-wrap items-center justify-center gap-3">
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
                    ? 'bg-[#6366F1] text-white shadow-md scale-105' 
                    : 'bg-white text-[#6C7089] hover:bg-indigo-50/60 hover:text-indigo-600 border border-[#E5E7F3]'
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
            <h2 className="text-lg font-bold text-[#1C1B2E] flex items-center gap-2">
              <BookOpen size={18} className="text-indigo-600" />
              {selectedCategory === 'All' ? 'Frequently Asked Questions' : `${selectedCategory} Articles`}
            </h2>
            <span className="text-xs text-[#9598B0] font-semibold">
              Showing {filteredArticles.length} article{filteredArticles.length === 1 ? '' : 's'}
            </span>
          </div>

          {isLoading ? (
            <div className="bg-white rounded-2xl p-12 text-center text-gray-400 font-medium border border-gray-200">
              Loading knowledge base articles...
            </div>
          ) : filteredArticles.length === 0 ? (
            <div className="bg-white rounded-2xl p-12 text-center space-y-3 border border-gray-200 shadow-xs">
              <HelpCircle size={40} className="mx-auto text-gray-300" />
              <h3 className="text-base font-bold text-gray-700">No matching articles found</h3>
              <p className="text-xs text-gray-500 max-w-md mx-auto">
                We couldn't find any articles matching "{searchQuery}". Try searching with different keywords or connect with our support team.
              </p>
              <button
                onClick={() => navigate('/customer/chat')}
                className="inline-flex items-center gap-2 bg-[#6366F1] hover:bg-[#4F46E5] text-white text-xs font-bold px-5 py-2.5 rounded-xl transition-colors mt-2"
              >
                <MessageSquare size={16} /> Ask AI Assistant / Support Agent
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
                    className={`bg-white rounded-2xl border transition-all overflow-hidden ${
                      isExpanded ? 'border-indigo-300 shadow-md ring-2 ring-indigo-50/50' : 'border-[#E5E7F3] hover:border-indigo-200 shadow-xs'
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
                          <h3 className="text-sm font-bold text-[#1C1B2E] group-hover:text-indigo-600 transition-colors">
                            {article.title}
                          </h3>
                          <div className="flex items-center gap-3 mt-1.5 text-xs text-[#9598B0]">
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
                        <div className="text-sm text-gray-700 leading-relaxed whitespace-pre-line bg-gray-50/70 p-4 rounded-xl border border-gray-100 font-normal">
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

        {/* Live Chat CTA Banner */}
        <div className="bg-gradient-to-r from-slate-900 to-indigo-950 text-white rounded-3xl p-8 shadow-xl flex flex-col md:flex-row items-center justify-between gap-6 border border-slate-800">
          <div className="space-y-1.5 text-center md:text-left">
            <div className="inline-flex items-center gap-1.5 text-xs font-bold text-[#818CF8] bg-indigo-500/10 border border-indigo-500/20 px-3 py-1 rounded-full">
              <Sparkles size={14} /> 24/7 AI & Human Live Support
            </div>
            <h3 className="text-xl font-extrabold tracking-tight">
              Didn't find what you were looking for?
            </h3>
            <p className="text-slate-300 text-xs max-w-lg">
              Our AI Assistant and live support team are available 24/7 to resolve your inquiries instantly.
            </p>
          </div>
          <button
            onClick={() => navigate('/customer/chat')}
            className="bg-[#6366F1] hover:bg-[#4F46E5] text-white px-6 py-3 rounded-2xl text-xs font-bold shadow-lg hover:shadow-indigo-500/30 transition-all flex items-center gap-2 whitespace-nowrap"
          >
            <MessageSquare size={16} /> Open Live Support Chat
          </button>
        </div>

      </div>
    </div>
  )
}
