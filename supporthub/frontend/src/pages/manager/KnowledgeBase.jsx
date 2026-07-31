import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { knowledgeApi } from '../../api/knowledge'
import { BookOpen, Plus, Search, Edit3, Trash2, Eye } from 'lucide-react'

export default function KnowledgeBase() {
  const [isEditorOpen, setIsEditorOpen] = useState(false)
  const [editingArticle, setEditingArticle] = useState(null)
  
  const queryClient = useQueryClient()

  const { data: articles, isLoading } = useQuery({
    queryKey: ['kb-articles'],
    queryFn: async () => {
      const res = await knowledgeApi.list()
      return res.data
    }
  })

  const deleteMutation = useMutation({
    mutationFn: (id) => knowledgeApi.delete(id),
    onSuccess: () => queryClient.invalidateQueries(['kb-articles'])
  })

  const handleDelete = (id) => {
    if (confirm('Are you sure you want to delete this article?')) {
      deleteMutation.mutate(id)
    }
  }

  const openEditor = (article = null) => {
    setEditingArticle(article)
    setIsEditorOpen(true)
  }

  if (isEditorOpen) {
    return (
      <KnowledgeEditor 
        article={editingArticle} 
        onClose={() => setIsEditorOpen(false)} 
      />
    )
  }

  return (
    <div className="flex-1 flex flex-col h-full bg-white">
      <div className="px-8 py-6 border-b border-[#E5E7F3] flex justify-between items-center bg-white shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-[#1C1B2E]" style={{ fontFamily: 'Plus Jakarta Sans, sans-serif' }}>Knowledge Base</h1>
          <p className="text-[#6C7089] mt-1">Manage articles used by agents and AI chatbots.</p>
        </div>
        <button 
          onClick={() => openEditor()}
          className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg font-semibold flex items-center gap-2 transition-colors"
        >
          <Plus size={18} /> New Article
        </button>
      </div>

      <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8">
        <div className="max-w-5xl mx-auto">
          {isLoading ? (
            <div className="flex justify-center py-20"><div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div></div>
          ) : articles?.length === 0 ? (
            <div className="text-center py-20 bg-white rounded-xl border border-[#E5E7F3] shadow-sm">
              <BookOpen size={48} className="mx-auto mb-4 text-[#E5E7F3]" />
              <p className="font-bold text-[#1C1B2E] text-lg">No articles yet</p>
              <p className="text-[#6C7089] text-sm mt-1 mb-6">Create the first knowledge base article.</p>
              <button 
                onClick={() => openEditor()}
                className="bg-indigo-50 text-indigo-700 px-4 py-2 rounded-lg font-semibold hover:bg-indigo-100 transition-colors"
              >
                Create Article
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {articles?.map(article => (
                <div key={article.id} className="bg-white rounded-xl border border-[#E5E7F3] p-5 shadow-sm hover:shadow-md transition-shadow flex flex-col">
                  <div className="flex justify-between items-start mb-3">
                    <span className="px-2.5 py-1 bg-gray-100 rounded-md text-xs font-bold uppercase text-[#6C7089]">{article.category}</span>
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase ${article.published ? 'bg-green-100 text-green-700' : 'bg-orange-100 text-orange-700'}`}>
                      {article.published ? 'Published' : 'Draft'}
                    </span>
                  </div>
                  <h3 className="font-bold text-lg text-[#1C1B2E] mb-2 line-clamp-2">{article.title}</h3>
                  <p className="text-sm text-[#6C7089] mb-4 line-clamp-3 flex-1">{article.body}</p>
                  
                  <div className="pt-4 border-t border-[#E5E7F3] flex justify-between items-center mt-auto">
                    <div className="flex items-center gap-1 text-xs text-[#9598B0] font-medium">
                      <Eye size={14} /> {article.views} views
                    </div>
                    <div className="flex gap-2">
                      <button onClick={() => openEditor(article)} className="p-1.5 text-indigo-600 hover:bg-indigo-50 rounded-md transition-colors">
                        <Edit3 size={16} />
                      </button>
                      <button onClick={() => handleDelete(article.id)} className="p-1.5 text-red-600 hover:bg-red-50 rounded-md transition-colors">
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

function KnowledgeEditor({ article, onClose }) {
  const [title, setTitle] = useState(article?.title || '')
  const [category, setCategory] = useState(article?.category || 'General Inquiry')
  const [body, setBody] = useState(article?.body || '')
  const [published, setPublished] = useState(article?.published ?? true)

  const queryClient = useQueryClient()

  const saveMutation = useMutation({
    mutationFn: (data) => article ? knowledgeApi.update(article.id, data) : knowledgeApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries(['kb-articles'])
      onClose()
    }
  })

  const handleSave = (e) => {
    e.preventDefault()
    if (!title.trim() || !body.trim()) return
    saveMutation.mutate({ title, category, body, published })
  }

  return (
    <div className="flex-1 flex flex-col h-full bg-[#F6F7FC]">
      <div className="px-8 py-4 border-b border-[#E5E7F3] bg-white flex justify-between items-center shadow-sm">
        <h1 className="text-xl font-bold text-[#1C1B2E]">{article ? 'Edit Article' : 'New Article'}</h1>
        <div className="flex gap-3">
          <button onClick={onClose} className="px-4 py-2 border border-[#E5E7F3] text-[#6C7089] rounded-lg font-semibold hover:bg-gray-50">Cancel</button>
          <button onClick={handleSave} disabled={saveMutation.isPending} className="px-4 py-2 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 disabled:opacity-50">
            {saveMutation.isPending ? 'Saving...' : 'Save Article'}
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-auto p-8">
        <div className="max-w-4xl mx-auto bg-white rounded-xl shadow-sm border border-[#E5E7F3] p-8">
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-bold text-[#1C1B2E] mb-2">Article Title</label>
              <input type="text" value={title} onChange={e => setTitle(e.target.value)} placeholder="E.g. How to reset your password" 
                className="w-full border border-[#E5E7F3] rounded-lg px-4 py-3 text-lg font-semibold focus:ring-2 focus:ring-indigo-500 outline-none" />
            </div>

            <div className="flex gap-6">
              <div className="flex-1">
                <label className="block text-sm font-bold text-[#1C1B2E] mb-2">Category</label>
                <select value={category} onChange={e => setCategory(e.target.value)} className="w-full border border-[#E5E7F3] rounded-lg px-4 py-3 focus:ring-2 focus:ring-indigo-500 outline-none">
                  <option value="General Inquiry">General Inquiry</option>
                  <option value="Technical Support">Technical Support</option>
                  <option value="Billing & Subscriptions">Billing & Subscriptions</option>
                  <option value="Bug Report">Bug Report</option>
                </select>
              </div>
              <div className="flex-1">
                <label className="block text-sm font-bold text-[#1C1B2E] mb-2">Status</label>
                <select value={published ? 'published' : 'draft'} onChange={e => setPublished(e.target.value === 'published')} className="w-full border border-[#E5E7F3] rounded-lg px-4 py-3 focus:ring-2 focus:ring-indigo-500 outline-none">
                  <option value="published">Published</option>
                  <option value="draft">Draft</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-bold text-[#1C1B2E] mb-2">Article Body</label>
              <textarea value={body} onChange={e => setBody(e.target.value)} rows="15" placeholder="Write the content here... (Markdown support coming soon)" 
                className="w-full border border-[#E5E7F3] rounded-lg px-4 py-3 focus:ring-2 focus:ring-indigo-500 outline-none font-mono text-sm"></textarea>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
