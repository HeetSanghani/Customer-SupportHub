import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { ticketsApi } from '../../api/tickets'
import { Star, MessageSquare, ArrowRight, CheckCircle2 } from 'lucide-react'
import { formatDate } from '../../utils/dateUtils'

export default function CustomerReviews() {
  const navigate = useNavigate()

  const { data: reviews = [], isLoading } = useQuery({
    queryKey: ['my-csat-reviews'],
    queryFn: async () => {
      const res = await ticketsApi.getMyCsat()
      return res.data
    }
  })

  return (
    <div className="flex-1 overflow-auto bg-[#F9FAFB] p-8 text-[#1C1B2E]">
      <div className="mb-6 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">My Reviews & Feedback</h1>
          <p className="text-[#6C7089] text-sm">View all ratings and feedback submitted for your support tickets.</p>
        </div>
        <span className="bg-indigo-50 text-indigo-600 font-bold text-xs px-4 py-2 rounded-full border border-indigo-100 flex items-center gap-1.5">
          <Star size={14} className="fill-indigo-600 text-indigo-600" />
          {reviews.length} {reviews.length === 1 ? 'Review Submitted' : 'Reviews Submitted'}
        </span>
      </div>

      {isLoading ? (
        <div className="bg-white p-12 rounded-2xl border border-[#E5E7F3] text-center text-xs text-[#9598B0]">
          Loading your reviews...
        </div>
      ) : reviews.length === 0 ? (
        <div className="bg-white p-12 rounded-2xl border border-dashed border-[#E5E7F3] text-center space-y-3">
          <div className="w-12 h-12 rounded-full bg-amber-50 text-amber-500 mx-auto flex items-center justify-center">
            <Star size={24} />
          </div>
          <h3 className="font-bold text-base text-[#1C1B2E]">No reviews submitted yet</h3>
          <p className="text-xs text-[#6C7089] max-w-sm mx-auto">
            Once a support ticket is completed, you can rate your experience and provide feedback. Your reviews will appear here!
          </p>
          <button
            onClick={() => navigate('/customer')}
            className="mt-2 inline-flex items-center gap-2 bg-[#6366F1] text-white px-4 py-2 rounded-xl text-xs font-bold hover:bg-[#4F46E5] transition-colors"
          >
            <MessageSquare size={14} /> Go to Support Chat
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {reviews.map(rev => (
            <div
              key={rev.id}
              onClick={() => navigate(`/customer/chat/${rev.ticket_id}`)}
              className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm hover:shadow-md hover:border-indigo-200 transition-all cursor-pointer group flex flex-col justify-between space-y-4"
            >
              <div>
                {/* Header info */}
                <div className="flex justify-between items-start gap-4 mb-3">
                  <div>
                    <h3 className="font-bold text-base text-[#1C1B2E] group-hover:text-indigo-600 transition-colors flex items-center gap-2">
                      {rev.ticket_subject}
                      <ArrowRight size={14} className="opacity-0 group-hover:opacity-100 text-indigo-600 transition-opacity" />
                    </h3>
                    <span className="text-[11px] font-mono font-bold text-[#9598B0]">Ticket Ref: {rev.ticket_ref}</span>
                  </div>

                  {/* Rating Stars */}
                  <div className="flex items-center gap-1 bg-amber-50 border border-amber-200 px-3 py-1 rounded-xl shrink-0">
                    {[1, 2, 3, 4, 5].map(star => (
                      <Star
                        key={star}
                        size={14}
                        className={star <= rev.rating ? "fill-amber-400 text-amber-400" : "text-gray-300"}
                      />
                    ))}
                    <span className="text-xs font-bold text-amber-800 ml-1">{rev.rating}/5</span>
                  </div>
                </div>

                {/* Comment box */}
                {rev.comment ? (
                  <p className="text-xs text-[#4B5563] bg-[#F9FAFB] p-3.5 rounded-xl border border-[#E5E7F3] italic">
                    "{rev.comment}"
                  </p>
                ) : (
                  <p className="text-xs text-[#9598B0] italic">No text feedback provided.</p>
                )}
              </div>

              {/* Footer */}
              <div className="flex justify-between items-center text-[11px] text-[#9598B0] border-t border-[#E5E7F3] pt-3 font-medium">
                <span className="flex items-center gap-1 text-emerald-600 font-semibold">
                  <CheckCircle2 size={13} /> Completed & Reviewed
                </span>
                <span>{formatDate(rev.created_at)}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
