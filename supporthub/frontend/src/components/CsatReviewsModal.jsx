import React from 'react'
import { X, Star, MessageSquare, ExternalLink, User } from 'lucide-react'
import { formatDate } from '../utils/dateUtils'
import { useNavigate } from 'react-router-dom'

export default function CsatReviewsModal({ isOpen, onClose, reviews = [], role = 'agent' }) {
  const navigate = useNavigate()
  if (!isOpen) return null

  const sortedReviews = [...reviews].sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0))

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-in fade-in duration-200">
      <div className="bg-white w-full max-w-2xl rounded-2xl shadow-2xl border border-[#E5E7F3] flex flex-col max-h-[85vh] overflow-hidden">
        
        {/* Modal Header */}
        <div className="p-6 border-b border-[#E5E7F3] flex items-center justify-between bg-[#F8FAFC]">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-50 text-amber-500 border border-amber-200 flex items-center justify-center font-bold">
              <Star size={20} className="fill-amber-400 text-amber-400" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-[#1C1B2E]">Customer CSAT Reviews & Feedback</h2>
              <p className="text-xs text-[#6C7089]">Verified customer ratings ({reviews.length} total reviews)</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-lg hover:bg-gray-200/60 flex items-center justify-center text-[#6C7089] hover:text-[#1C1B2E] transition-colors"
          >
            <X size={18} />
          </button>
        </div>

        {/* Reviews List */}
        <div className="p-6 overflow-y-auto space-y-4 bg-[#F9FAFB] flex-1">
          {sortedReviews.length === 0 ? (
            <div className="text-center py-12 bg-white rounded-xl border border-dashed border-[#E5E7F3]">
              <MessageSquare size={32} className="mx-auto text-gray-300 mb-2" />
              <p className="text-sm font-semibold text-[#6C7089]">No customer reviews found yet.</p>
            </div>
          ) : (
            sortedReviews.map((rev, i) => {
              const stars = rev.rating || 5
              return (
                <div key={rev.id || i} className="bg-white p-5 rounded-xl border border-[#E5E7F3] shadow-xs hover:border-indigo-200 transition-all">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <div className="flex text-amber-400 gap-0.5">
                        {[1, 2, 3, 4, 5].map(s => (
                          <Star
                            key={s}
                            size={14}
                            className={s <= stars ? "fill-amber-400 text-amber-400" : "text-gray-200"}
                          />
                        ))}
                      </div>
                      <span className="text-xs font-bold text-[#1C1B2E] bg-amber-50 border border-amber-200 px-2 py-0.5 rounded-md">
                        {stars} / 5
                      </span>
                    </div>

                    <span className="text-xs font-mono text-[#9598B0]">
                      {rev.created_at ? formatDate(rev.created_at) : 'Recently'}
                    </span>
                  </div>

                  {/* Comment */}
                  <p className="text-xs text-[#374151] bg-[#F8FAFC] p-3 rounded-lg border border-[#E5E7F3] my-2 italic leading-relaxed">
                    "{rev.comment || 'No text feedback provided.'}"
                  </p>

                  <div className="flex items-center justify-between text-[11px] text-[#6C7089] mt-3 pt-2 border-t border-[#F1F5F9]">
                    <span className="font-semibold text-indigo-600 flex items-center gap-1">
                      Ticket Ref: <code className="bg-indigo-50 px-1.5 py-0.5 rounded text-indigo-700 font-mono">{rev.ticket_ref || rev.ticket_id?.slice(0, 8) || 'TCK-70849'}</code>
                    </span>
                    
                    <button
                      onClick={() => {
                        onClose()
                        const path = role === 'admin' 
                          ? `/admin/tickets/${rev.ticket_id}` 
                          : role === 'manager' 
                          ? `/manager/tickets/${rev.ticket_id}` 
                          : `/agent/inbox?id=${rev.ticket_id}`
                        navigate(path)
                      }}
                      className="inline-flex items-center gap-1 text-xs font-bold text-indigo-600 hover:text-indigo-800 transition-colors"
                    >
                      View Ticket Thread <ExternalLink size={12} />
                    </button>
                  </div>
                </div>
              )
            })
          )}
        </div>

        {/* Modal Footer */}
        <div className="p-4 border-t border-[#E5E7F3] bg-white flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2 bg-[#6366F1] text-white rounded-xl text-xs font-bold hover:bg-[#4F46E5] transition-colors"
          >
            Close
          </button>
        </div>

      </div>
    </div>
  )
}
