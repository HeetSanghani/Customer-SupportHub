import { useQuery } from '@tanstack/react-query'
import { ordersApi } from '../../api/orders'
import { RotateCcw, DollarSign, ArrowLeft } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function CustomerReturnsRefunds() {
  const { data: returns = [], isLoading: loadingReturns } = useQuery({
    queryKey: ['returns', 'me'],
    queryFn: async () => {
      const res = await ordersApi.getMyReturns()
      return res.data
    },
  })

  const { data: refunds = [], isLoading: loadingRefunds } = useQuery({
    queryKey: ['refunds', 'me'],
    queryFn: async () => {
      const res = await ordersApi.getMyRefunds()
      return res.data
    },
  })

  const { data: payments = [] } = useQuery({
    queryKey: ['payments', 'me'],
    queryFn: async () => {
      const res = await ordersApi.getMyPayments()
      return res.data
    },
  })

  return (
    <div className="flex-1 overflow-y-auto bg-[#F6F7FC] p-8 space-y-8">
      <div>
        <div className="flex items-center gap-2 text-xs text-[#6C7089] mb-1">
          <Link to="/customer" className="hover:text-indigo-600 flex items-center gap-1"><ArrowLeft size={12}/> Dashboard</Link> / Returns & Refunds
        </div>
        <h1 className="text-2xl font-bold text-[#1C1B2E]">Returns, Refunds & Payments</h1>
        <p className="text-sm text-[#6C7089]">Track return request statuses, processed refunds, and safe payment transaction records.</p>
      </div>

      {/* Section 1: Returns */}
      <div className="bg-white border border-[#E5E7F3] rounded-2xl p-6 shadow-sm space-y-6">
        <h2 className="text-lg font-bold text-[#1C1B2E] flex items-center gap-2">
          <RotateCcw size={20} className="text-amber-600" /> Return Requests ({returns.length})
        </h2>
        {returns.length === 0 ? (
          <div className="text-center py-8 text-[#9598B0] text-sm">No return requests on record.</div>
        ) : (
          <div className="space-y-4">
            {returns.map(r => (
              <div key={r.return_id} className="p-4 rounded-xl border border-[#F0F1F7] bg-[#FAFAFE] flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                <div>
                  <div className="text-xs font-semibold text-[#6C7089]">Return ID: <span className="font-bold text-[#1C1B2E]">{r.return_id}</span></div>
                  <div className="text-sm font-bold text-[#1C1B2E] mt-0.5">Order: {r.order_id} — Item: {r.order_item_id}</div>
                  <div className="text-xs text-[#6C7089] mt-1"><span className="font-semibold">Reason:</span> {r.reason}</div>
                </div>
                <div>
                  <span className={`inline-block px-3 py-1 rounded-full text-xs font-bold ${
                    r.status === 'COMPLETED' || r.status === 'APPROVED' ? 'bg-emerald-100 text-emerald-800' :
                    r.status === 'REJECTED' ? 'bg-rose-100 text-rose-800' : 'bg-amber-100 text-amber-800'
                  }`}>
                    {r.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Section 2: Refunds */}
      <div className="bg-white border border-[#E5E7F3] rounded-2xl p-6 shadow-sm space-y-6">
        <h2 className="text-lg font-bold text-[#1C1B2E] flex items-center gap-2">
          <DollarSign size={20} className="text-emerald-600" /> Issued Refunds ({refunds.length})
        </h2>
        {refunds.length === 0 ? (
          <div className="text-center py-8 text-[#9598B0] text-sm">No processed refunds on record.</div>
        ) : (
          <div className="space-y-4">
            {refunds.map(rf => (
              <div key={rf.refund_id} className="p-4 rounded-xl border border-[#F0F1F7] bg-[#FAFAFE] flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                <div>
                  <div className="text-xs font-semibold text-[#6C7089]">Refund ID: <span className="font-bold text-[#1C1B2E]">{rf.refund_id}</span></div>
                  <div className="text-sm font-bold text-[#1C1B2E] mt-0.5">Order: {rf.order_id} — Return: {rf.return_id}</div>
                </div>
                <div className="text-right">
                  <div className="text-base font-bold text-emerald-600">+${(rf.refund_amount || 0).toFixed(2)}</div>
                  <span className="inline-block text-[10px] uppercase font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 mt-0.5">
                    {rf.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Section 3: Safe Payment History */}
      <div className="bg-white border border-[#E5E7F3] rounded-2xl p-6 shadow-sm space-y-6">
        <h2 className="text-lg font-bold text-[#1C1B2E] flex items-center gap-2">
          <DollarSign size={20} className="text-indigo-600" /> Payment Transaction Summaries ({payments.length})
        </h2>
        {payments.length === 0 ? (
          <div className="text-center py-8 text-[#9598B0] text-sm">No payment records found.</div>
        ) : (
          <div className="space-y-4">
            {payments.map(p => (
              <div key={p.payment_id} className="p-4 rounded-xl border border-[#F0F1F7] bg-[#FAFAFE] flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                <div>
                  <div className="text-xs font-semibold text-[#6C7089]">Payment ID: <span className="font-bold text-[#1C1B2E]">{p.payment_id}</span></div>
                  <div className="text-sm font-bold text-[#1C1B2E] mt-0.5">Order: {p.order_id} — Method: {p.method}</div>
                </div>
                <div className="text-right">
                  <div className="text-base font-bold text-[#1C1B2E]">${(p.amount || 0).toFixed(2)}</div>
                  <span className="inline-block text-[10px] uppercase font-bold px-2 py-0.5 rounded bg-blue-100 text-blue-800 mt-0.5">
                    {p.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
