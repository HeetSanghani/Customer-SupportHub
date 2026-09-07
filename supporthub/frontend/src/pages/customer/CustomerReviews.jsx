import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { ordersApi } from '../../api/orders'
import { Star, MessageSquare, ArrowLeft, CheckCircle2, Sparkles, ShoppingBag } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function CustomerReviews() {
  const queryClient = useQueryClient()
  const [rating, setRating] = useState(5)
  const [hoverRating, setHoverRating] = useState(0)
  const [comment, setComment] = useState('')
  const [orderId, setOrderId] = useState('')
  const [activeFilter, setActiveFilter] = useState('ALL')
  const [submitSuccess, setSubmitSuccess] = useState(false)
  const [localReviews, setLocalReviews] = useState([])

  // Fetch logged in customer's purchased orders
  const { data: myOrders = [], isLoading: isLoadingOrders } = useQuery({
    queryKey: ['orders', 'me'],
    queryFn: async () => {
      const res = await ordersApi.getMyOrders()
      return res.data || []
    },
  })

  // Fetch reviews from server
  const { data: serverReviews = [], isLoading: isLoadingReviews } = useQuery({
    queryKey: ['reviews', 'me'],
    queryFn: async () => {
      const res = await ordersApi.getMyReviews()
      return res.data || []
    },
  })

  // Combine server and locally submitted reviews
  const allReviews = [...localReviews, ...serverReviews]

  const submitMutation = useMutation({
    mutationFn: async (payload) => {
      const res = await ordersApi.createReview(payload)
      return res.data || payload
    },
    onSuccess: (newReview, variables) => {
      const createdItem = {
        id: 'REV-' + Date.now(),
        review_id: 'REV-' + Date.now(),
        order_id: variables.order_id || orderId,
        rating: variables.rating,
        comment: variables.comment,
        created_at: new Date().toISOString(),
      }
      setLocalReviews(prev => [createdItem, ...prev])
      queryClient.invalidateQueries({ queryKey: ['reviews', 'me'] })
      setComment('')
      setOrderId('')
      setRating(5)
      setSubmitSuccess(true)
      setTimeout(() => setSubmitSuccess(false), 4000)
    },
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!comment.trim()) return
    submitMutation.mutate({
      order_id: orderId || (myOrders[0]?.order_id || 'ORD-001'),
      rating,
      comment,
    })
  }

  const filteredReviews = allReviews.filter(r => {
    if (activeFilter === '5STARS') return r.rating === 5
    if (activeFilter === 'CRITICAL') return r.rating <= 3
    return true
  })

  return (
    <div className="flex-1 h-full overflow-y-auto bg-[#F8FAFC] p-4 md:p-8 space-y-6 text-[#0F172A]">
      {/* Header */}
      <div className="bg-white p-6 rounded-3xl border border-[#E2E8F0] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <Link to="/customer" className="inline-flex items-center gap-1.5 text-xs font-extrabold text-indigo-600 hover:text-indigo-700 mb-2 transition-colors">
            <ArrowLeft size={14} /> Back to AI Chat
          </Link>
          <h1 className="text-2xl font-black text-[#0F172A] tracking-tight flex items-center gap-2">
            My Reviews & Feedback
            <span className="text-xs font-bold bg-amber-50 text-amber-700 px-2.5 py-0.5 rounded-full border border-amber-200">
              {allReviews.length} Published
            </span>
          </h1>
          <p className="text-xs md:text-sm text-[#64748B] mt-0.5">Share your experience, rate purchased products, and view feedback history.</p>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-2">
          {[
            { id: 'ALL', label: 'All Reviews' },
            { id: '5STARS', label: '5-Star Ratings' },
            { id: 'CRITICAL', label: 'Critical' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveFilter(tab.id)}
              className={`px-3.5 py-2 rounded-xl text-xs font-bold transition-all ${
                activeFilter === tab.id
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'bg-[#F8FAFC] text-[#64748B] hover:bg-gray-100 border border-[#E2E8F0]'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Submit Review Card */}
        <div className="lg:col-span-1 bg-white border border-[#E2E8F0] rounded-3xl p-6 shadow-2xs space-y-4 self-start">
          <h2 className="text-base font-extrabold text-[#0F172A] flex items-center gap-2 border-b border-[#F1F5F9] pb-3">
            <Sparkles size={18} className="text-amber-500" /> Write a Product Review
          </h2>

          {submitSuccess && (
            <div className="p-3.5 bg-emerald-50 text-emerald-800 border border-emerald-200 rounded-2xl text-xs font-bold flex items-center gap-2">
              <CheckCircle2 size={16} /> Thank you! Your review has been published.
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Purchased Order Dropdown Option */}
            <div>
              <label className="block text-xs font-bold text-[#0F172A] mb-1.5 flex items-center gap-1.5">
                <ShoppingBag size={14} className="text-indigo-600" />
                Select Purchased Order <span className="text-rose-500">*</span>
              </label>

              <select
                value={orderId}
                onChange={e => setOrderId(e.target.value)}
                className="w-full px-3.5 py-3 bg-[#F8FAFC] border border-[#E2E8F0] rounded-2xl text-xs font-mono font-bold focus:outline-none focus:border-indigo-500 text-[#0F172A]"
                required
              >
                <option value="">-- Choose a Purchased Order --</option>
                {isLoadingOrders ? (
                  <option disabled>Loading your orders...</option>
                ) : myOrders.length === 0 ? (
                  <option disabled>No purchased orders found</option>
                ) : (
                  myOrders.map(order => (
                    <option key={order.order_id || order.id} value={order.order_id}>
                      {order.order_id} ({order.status}) - ₹{Number(order.total_amount || 0).toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                    </option>
                  ))
                )}
              </select>
              <p className="text-[11px] text-[#64748B] mt-1">
                Reviews can only be submitted for orders associated with your account.
              </p>
            </div>

            <div>
              <label className="block text-xs font-bold text-[#0F172A] mb-1.5">Rating Score</label>
              <div className="flex items-center gap-1 bg-[#F8FAFC] p-3 rounded-2xl border border-[#E2E8F0]">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    onClick={() => setRating(star)}
                    onMouseEnter={() => setHoverRating(star)}
                    onMouseLeave={() => setHoverRating(0)}
                    className="p-1 transition-transform hover:scale-110"
                  >
                    <Star
                      size={22}
                      className={(hoverRating || rating) >= star ? 'fill-amber-400 text-amber-400' : 'text-gray-300'}
                    />
                  </button>
                ))}
                <span className="text-xs font-black text-[#0F172A] ml-2 font-mono">
                  {rating}.0 / 5.0
                </span>
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-[#0F172A] mb-1.5">Your Feedback</label>
              <textarea
                rows={4}
                value={comment}
                onChange={e => setComment(e.target.value)}
                placeholder="Describe your product experience, quality, fitting, or delivery service..."
                className="w-full px-3.5 py-2.5 bg-[#F8FAFC] border border-[#E2E8F0] rounded-2xl text-xs focus:outline-none focus:border-indigo-500 font-medium resize-none"
                required
              />
            </div>

            <button
              type="submit"
              disabled={submitMutation.isPending}
              className="w-full py-3.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl text-xs font-extrabold shadow-md transition-all active:scale-95 disabled:opacity-50"
            >
              {submitMutation.isPending ? 'Submitting Review...' : 'Publish Feedback'}
            </button>
          </form>
        </div>

        {/* Existing Reviews List */}
        <div className="lg:col-span-2 space-y-4">
          {isLoadingReviews ? (
            <div className="bg-white border border-[#E2E8F0] rounded-3xl p-12 text-center text-[#94A3B8] font-medium">
              Loading customer reviews...
            </div>
          ) : filteredReviews.length === 0 ? (
            <div className="bg-white border border-[#E2E8F0] rounded-3xl p-12 text-center shadow-2xs space-y-2">
              <MessageSquare size={36} className="mx-auto text-gray-300 mb-2" />
              <h3 className="font-bold text-[#0F172A] text-base">No Feedback Found</h3>
              <p className="text-xs text-[#64748B] max-w-sm mx-auto">
                No reviews match your selected filter criteria. Select an order from the dropdown on the left and publish your feedback.
              </p>
            </div>
          ) : (
            filteredReviews.map(r => (
              <div key={r.review_id || r.id} className="bg-white border border-[#E2E8F0] rounded-3xl p-6 shadow-2xs hover:border-indigo-200 transition-all space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-1">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <Star
                        key={star}
                        size={16}
                        className={r.rating >= star ? 'fill-amber-400 text-amber-400' : 'text-gray-200'}
                      />
                    ))}
                    <span className="text-xs font-black text-[#0F172A] ml-2">{r.rating}.0</span>
                  </div>
                  <span className="text-[10px] font-extrabold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200 flex items-center gap-1">
                    <CheckCircle2 size={12} /> Verified Purchase
                  </span>
                </div>

                <p className="text-xs md:text-sm text-[#334155] leading-relaxed font-medium bg-[#F8FAFC] p-4 rounded-2xl border border-[#F1F5F9]">
                  "{r.comment}"
                </p>

                <div className="flex items-center justify-between text-[11px] text-[#94A3B8] pt-1">
                  <span>Order Reference: <strong className="font-mono text-[#0F172A]">{r.order_id || 'N/A'}</strong></span>
                  <span>{r.created_at ? new Date(r.created_at).toLocaleDateString('en-IN', { dateStyle: 'medium' }) : 'Recently'}</span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}
