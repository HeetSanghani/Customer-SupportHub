import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { Star, CheckCircle2 } from 'lucide-react'
import { ticketsApi } from '../../api/tickets'

export default function CsatWidget({ ticketId }) {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [rating, setRating] = useState(0)
  const [hover, setHover] = useState(0)
  const [comment, setComment] = useState('')
  const [submitted, setSubmitted] = useState(false)

  useEffect(() => {
    setRating(0); setHover(0); setComment(''); setSubmitted(false)
  }, [ticketId])

  const { data: existing, isLoading } = useQuery({
    queryKey: ['csat', ticketId],
    queryFn: async () => { const r = await ticketsApi.getCsat(ticketId); return r.data },
    enabled: !!ticketId, staleTime: 0,
  })

  const mut = useMutation({
    mutationFn: d => ticketsApi.submitCsat(ticketId, d),
    onSuccess: () => {
      setSubmitted(true)
      queryClient.invalidateQueries({ queryKey: ['csat', ticketId] })
      queryClient.invalidateQueries({ queryKey: ['my-csat-reviews'] })
    }
  })

  if (isLoading) return null

  const displayRating = existing?.rating || rating
  const displayComment = existing?.comment || comment

  if (existing || submitted) return (
    <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-4 text-center space-y-1.5 animate-slideUp">
      <div className="flex justify-center gap-1">
        {[1,2,3,4,5].map(s => <Star key={s} size={16} className={s<=displayRating?'fill-amber-400 text-amber-400':'text-gray-300'} />)}
      </div>
      <p className="text-xs font-bold text-emerald-800">You rated this {displayRating}/5 stars</p>
      {displayComment && <p className="text-[11px] text-emerald-700 italic">"{displayComment}"</p>}
      <button onClick={() => navigate('/customer/reviews')}
        className="text-[11px] font-bold text-emerald-700 bg-emerald-100 hover:bg-emerald-200 px-3 py-1 rounded-lg transition-colors">
        View in My Reviews →
      </button>
    </div>
  )

  return (
    <form onSubmit={e => { e.preventDefault(); if (rating) mut.mutate({ rating, comment }) }}
      className="bg-indigo-50 border border-indigo-100 rounded-xl p-4 text-center space-y-3 animate-slideUp">
      <p className="text-xs font-bold text-indigo-900">How satisfied were you with this support?</p>
      <div className="flex justify-center gap-1">
        {[1,2,3,4,5].map(s => (
          <button key={s} type="button"
            onClick={() => setRating(s)} onMouseEnter={() => setHover(s)} onMouseLeave={() => setHover(0)}
            className="p-1 transition-transform hover:scale-110">
            <Star size={22} className={(hover||rating)>=s?'fill-amber-400 text-amber-400':'text-gray-300'} />
          </button>
        ))}
      </div>
      {rating > 0 && (
        <div className="space-y-2 max-w-xs mx-auto">
          <input value={comment} onChange={e => setComment(e.target.value)}
            placeholder="Optional comment..." className="w-full border border-indigo-200 rounded-lg px-3 py-1.5 text-xs focus:ring-2 focus:ring-indigo-400 outline-none" />
          <button type="submit" disabled={mut.isPending}
            className="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold px-4 py-1.5 rounded-lg transition-colors disabled:opacity-50">
            {mut.isPending ? 'Submitting…' : 'Submit Feedback'}
          </button>
        </div>
      )}
    </form>
  )
}
