import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { knowledgeApi } from '../../api/knowledge'
import { Search, Plus, Edit2, Trash2, X, BookOpen, AlertCircle, Eye, ThumbsUp } from 'lucide-react'

export default function HelpCenterMgmt() {
  const queryClient = useQueryClient()
  const [searchTerm, setSearchTerm] = useState('')
  const [isArticleModalOpen, setIsArticleModalOpen] = useState(false)
  const [editingArticle, setEditingArticle] = useState(null)

  // Article Form State
  const [articleForm, setArticleForm] = useState({
    title: '',
    category: 'Account',
    body: '',
  })
  const [formError, setFormError] = useState('')

  // Fetch KB Articles from backend
  const { data: articles = [], isLoading } = useQuery({
    queryKey: ['kb-articles'],
    queryFn: async () => {
      const res = await knowledgeApi.list()
      return res.data
    }
  })

  // Create Mutation
  const createMutation = useMutation({
    mutationFn: (data) => knowledgeApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries(['kb-articles'])
      setIsArticleModalOpen(false)
      setArticleForm({ title: '', category: 'Account', body: '' })
      setFormError('')
    },
    onError: (err) => {
      setFormError(err.response?.data?.detail || 'Failed to create article')
    }
  })

  // Update Mutation
  const updateMutation = useMutation({
    mutationFn: ({ id, data }) => knowledgeApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries(['kb-articles'])
      setEditingArticle(null)
      setFormError('')
    }
  })

  // Delete Mutation
  const deleteMutation = useMutation({
    mutationFn: (id) => knowledgeApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries(['kb-articles'])
      setEditingArticle(null)
    }
  })

  // Filter articles
  const filteredArticles = articles.filter(a =>
    a.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    a.category?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const handleCreateSubmit = (e) => {
    e.preventDefault()
    if (!articleForm.title || !articleForm.body) {
      setFormError('Title and body content are required.')
      return
    }
    createMutation.mutate(articleForm)
  }

  const handleEditSubmit = (e) => {
    e.preventDefault()
    if (!editingArticle) return
    updateMutation.mutate({ id: editingArticle.id, data: articleForm })
  }

  const openCreateModal = () => {
    setArticleForm({ title: '', category: 'Account', body: '' })
    setFormError('')
    setIsArticleModalOpen(true)
  }

  const openEditModal = (article) => {
    setEditingArticle(article)
    setArticleForm({
      title: article.title,
      category: article.category,
      body: article.body || '',
    })
    setFormError('')
  }

  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8 text-[#1C1B2E]">
      {/* Page Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">Help Center Management</h1>
          <p className="text-[#6C7089] text-sm mt-1">Create and maintain the articles your AI and agents rely on.</p>
        </div>
        <button
          onClick={openCreateModal}
          className="flex items-center gap-2 bg-[#4F46E5] hover:bg-[#4338CA] text-white px-4 py-2.5 rounded-xl font-medium text-sm transition-colors shadow-sm"
        >
          <Plus size={16} /> + New Article
        </button>
      </div>

      {/* Search Bar */}
      <div className="mb-6">
        <div className="relative max-w-md">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#9598B0]" size={16} />
          <input
            type="text"
            placeholder="Search articles..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 bg-white border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500 shadow-sm"
          />
        </div>
      </div>

      {/* Articles Table */}
      {isLoading ? (
        <div className="flex justify-center py-16">
          <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div>
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-[#E5E7F3] shadow-sm overflow-hidden">
          <table className="w-full text-left text-sm text-[#6C7089]">
            <thead className="bg-[#F9FAFB] border-b border-[#E5E7F3] text-xs uppercase font-bold text-[#9598B0]">
              <tr>
                <th className="px-6 py-4">Article</th>
                <th className="px-6 py-4">Category</th>
                <th className="px-6 py-4">Views</th>
                <th className="px-6 py-4">Helpful</th>
                <th className="px-6 py-4">Updated</th>
                <th className="px-6 py-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E5E7F3]">
              {filteredArticles.length === 0 ? (
                <tr>
                  <td colSpan="6" className="text-center py-10 text-sm text-[#9598B0]">
                    No help articles found. Click "+ New Article" to create one.
                  </td>
                </tr>
              ) : (
                filteredArticles.map(article => {
                  const viewsFormatted = article.views ? (article.views > 1000 ? `${(article.views / 1000).toFixed(1)}k` : article.views) : 0
                  const helpfulPct = article.helpful_count !== undefined && article.helpful_count !== null ? `${Math.round(article.helpful_count)}%` : '100%'

                  return (
                    <tr key={article.id} className="hover:bg-gray-50/80 transition-colors">
                      <td className="px-6 py-4">
                        <div className="font-bold text-[#1C1B2E]">{article.title}</div>
                      </td>
                      <td className="px-6 py-4">
                        <span className="px-3 py-1 rounded-full text-xs font-bold bg-indigo-50 text-indigo-700">
                          {article.category}
                        </span>
                      </td>
                      <td className="px-6 py-4 font-semibold text-[#1C1B2E]">{viewsFormatted}</td>
                      <td className="px-6 py-4 font-semibold text-emerald-600">{helpfulPct}</td>
                      <td className="px-6 py-4 text-xs text-[#9598B0]">
                        {article.updated_at ? new Date(article.updated_at).toLocaleDateString() : 'Recently'}
                      </td>
                      <td className="px-6 py-4 text-right">
                        <button
                          onClick={() => openEditModal(article)}
                          className="px-3 py-1.5 text-xs font-semibold text-[#4F46E5] hover:bg-indigo-50 rounded-lg transition-colors border border-transparent hover:border-indigo-100"
                        >
                          Edit
                        </button>
                      </td>
                    </tr>
                  )
                })
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* Create Article Modal */}
      {isArticleModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-lg overflow-hidden border border-[#E5E7F3]">
            <div className="flex justify-between items-center px-6 py-4 border-b border-[#E5E7F3]">
              <h3 className="font-bold text-lg text-[#1C1B2E]">New Knowledge Article</h3>
              <button onClick={() => setIsArticleModalOpen(false)} className="text-gray-400 hover:text-gray-600 p-1 rounded-lg">
                <X size={18} />
              </button>
            </div>
            <form onSubmit={handleCreateSubmit} className="p-6 space-y-4">
              {formError && (
                <div className="flex items-center gap-2 p-3 bg-red-50 text-red-600 text-xs rounded-xl font-medium">
                  <AlertCircle size={16} />
                  <span>{formError}</span>
                </div>
              )}
              <div>
                <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Article Title</label>
                <input
                  type="text"
                  placeholder="e.g. How to reset your account password"
                  value={articleForm.title}
                  onChange={(e) => setArticleForm({ ...articleForm, title: e.target.value })}
                  className="w-full px-3.5 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                  required
                />
              </div>
              <div>
                <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Category</label>
                <select
                  value={articleForm.category}
                  onChange={(e) => setArticleForm({ ...articleForm, category: e.target.value })}
                  className="w-full px-3 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                >
                  <option value="Account">Account</option>
                  <option value="Billing">Billing</option>
                  <option value="Orders">Orders</option>
                  <option value="Refunds">Refunds</option>
                  <option value="Technical">Technical</option>
                </select>
              </div>
              <div>
                <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Content Body</label>
                <textarea
                  rows={5}
                  placeholder="Enter detailed help article instructions..."
                  value={articleForm.body}
                  onChange={(e) => setArticleForm({ ...articleForm, body: e.target.value })}
                  className="w-full px-3.5 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                  required
                />
              </div>
              <div className="flex justify-end gap-3 pt-4 border-t border-[#E5E7F3]">
                <button
                  type="button"
                  onClick={() => setIsArticleModalOpen(false)}
                  className="px-4 py-2 text-sm font-semibold text-gray-600 hover:bg-gray-100 rounded-xl"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createMutation.isPending}
                  className="px-4 py-2 text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl disabled:opacity-50"
                >
                  {createMutation.isPending ? 'Publishing...' : 'Publish Article'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit Article Modal */}
      {editingArticle && (
        <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-lg overflow-hidden border border-[#E5E7F3]">
            <div className="flex justify-between items-center px-6 py-4 border-b border-[#E5E7F3]">
              <h3 className="font-bold text-lg text-[#1C1B2E]">Edit Article</h3>
              <button onClick={() => setEditingArticle(null)} className="text-gray-400 hover:text-gray-600 p-1 rounded-lg">
                <X size={18} />
              </button>
            </div>
            <form onSubmit={handleEditSubmit} className="p-6 space-y-4">
              <div>
                <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Article Title</label>
                <input
                  type="text"
                  value={articleForm.title}
                  onChange={(e) => setArticleForm({ ...articleForm, title: e.target.value })}
                  className="w-full px-3.5 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                  required
                />
              </div>
              <div>
                <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Category</label>
                <select
                  value={articleForm.category}
                  onChange={(e) => setArticleForm({ ...articleForm, category: e.target.value })}
                  className="w-full px-3 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                >
                  <option value="Account">Account</option>
                  <option value="Billing">Billing</option>
                  <option value="Orders">Orders</option>
                  <option value="Refunds">Refunds</option>
                  <option value="Technical">Technical</option>
                </select>
              </div>
              <div>
                <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Content Body</label>
                <textarea
                  rows={5}
                  value={articleForm.body}
                  onChange={(e) => setArticleForm({ ...articleForm, body: e.target.value })}
                  className="w-full px-3.5 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                  required
                />
              </div>
              <div className="flex justify-between items-center pt-4 border-t border-[#E5E7F3]">
                <button
                  type="button"
                  onClick={() => {
                    if (confirm(`Delete article "${editingArticle.title}"?`)) {
                      deleteMutation.mutate(editingArticle.id)
                    }
                  }}
                  className="flex items-center gap-1.5 px-3 py-2 text-xs font-bold text-red-600 hover:bg-red-50 rounded-xl transition-colors"
                >
                  <Trash2 size={14} /> Delete Article
                </button>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setEditingArticle(null)}
                    className="px-4 py-2 text-sm font-semibold text-gray-600 hover:bg-gray-100 rounded-xl"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={updateMutation.isPending}
                    className="px-4 py-2 text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl disabled:opacity-50"
                  >
                    {updateMutation.isPending ? 'Saving...' : 'Save Changes'}
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
