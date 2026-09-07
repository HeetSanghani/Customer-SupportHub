import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { ordersApi } from '../../api/orders'
import { RotateCcw, DollarSign, ArrowLeft, Sparkles, CreditCard, ShieldCheck, CheckCircle2, AlertCircle, ArrowRight, RefreshCw } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'

export default function CustomerReturnsRefunds() {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState('ALL')

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

  const { data: payments = [], isLoading: loadingPayments } = useQuery({
    queryKey: ['payments', 'me'],
    queryFn: async () => {
      const res = await ordersApi.getMyPayments()
      return res.data
    },
  })

  return (
    <div className="flex-1 h-full overflow-y-auto bg-[#F8FAFC] p-4 md:p-8 space-y-6 text-[#0F172A]">
      {/* Header Title */}
      <div className="bg-white p-6 rounded-3xl border border-[#E2E8F0] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <Link to="/customer" className="inline-flex items-center gap-1.5 text-xs font-extrabold text-indigo-600 hover:text-indigo-700 mb-2 transition-colors">
            <ArrowLeft size={14} /> Back to AI Chat
          </Link>
          <h1 className="text-2xl font-black text-[#0F172A] tracking-tight">Returns, Refunds & Payments</h1>
          <p className="text-xs md:text-sm text-[#64748B] mt-0.5">Track return request statuses, processed refunds, and safe payment transaction records.</p>
        </div>

        {/* Section Filter Tabs */}
        <div className="flex items-center gap-2">
          {[
            { id: 'ALL', label: 'Overview' },
            { id: 'RETURNS', label: `Returns (${returns.length})` },
            { id: 'REFUNDS', label: `Refunds (${refunds.length})` },
            { id: 'PAYMENTS', label: `Payments (${payments.length})` }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-3.5 py-2 rounded-xl text-xs font-bold transition-all ${
                activeTab === tab.id
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'bg-[#F8FAFC] text-[#64748B] hover:bg-gray-100 border border-[#E2E8F0]'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* AI Return Quick Start Banner */}
      <div className="bg-gradient-to-r from-indigo-900 via-indigo-800 to-purple-900 text-white rounded-3xl p-6 md:p-8 shadow-md flex flex-col md:flex-row items-center justify-between gap-6 relative overflow-hidden">
        <div className="space-y-1.5 relative z-10">
          <div className="text-amber-300 font-extrabold text-xs uppercase tracking-wider flex items-center gap-1.5">
            <Sparkles size={14} /> Need to Return an Item?
          </div>
          <div className="font-extrabold text-xl md:text-2xl tracking-tight">Instant AI Return Assistance</div>
          <div className="text-indigo-200 text-xs md:text-sm max-w-xl leading-relaxed">
            Initiate hassle-free returns, verify warranty eligibility, and receive instant return labels through our SupportHub AI Assistant.
          </div>
        </div>
        <button
          onClick={() => navigate('/customer/chat')}
          className="px-6 py-3 bg-amber-400 hover:bg-amber-300 text-indigo-950 rounded-2xl text-xs font-black shadow-lg transition-transform active:scale-95 shrink-0 flex items-center gap-2 relative z-10"
        >
          <Sparkles size={16} /> Start AI Return Chat <ArrowRight size={14} />
        </button>
      </div>

      {/* Section 1: Returns */}
      {(activeTab === 'ALL' || activeTab === 'RETURNS') && (
        <div className="bg-white border border-[#E2E8F0] rounded-3xl p-6 md:p-8 shadow-2xs space-y-6">
          <div className="flex items-center justify-between border-b border-[#F1F5F9] pb-4">
            <h2 className="text-lg font-extrabold text-[#0F172A] flex items-center gap-2.5">
              <div className="p-2 bg-amber-50 text-amber-600 rounded-xl">
                <RotateCcw size={20} />
              </div>
              Return Requests ({returns.length})
            </h2>
            <span className="text-xs text-[#94A3B8] font-semibold">Active & Processed Claims</span>
          </div>

          {loadingReturns ? (
            <div className="text-center py-8 text-[#94A3B8] text-xs font-medium">Loading return records...</div>
          ) : returns.length === 0 ? (
            <div className="text-center py-10 text-[#94A3B8] space-y-2">
              <RotateCcw size={32} className="mx-auto text-gray-300 mb-1" />
              <div className="text-sm font-bold text-[#0F172A]">No Return Requests</div>
              <p className="text-xs text-[#64748B] max-w-sm mx-auto">You have not submitted any return or replacement claims yet.</p>
            </div>
          ) : (
            <div className="space-y-3">
              {returns.map(r => (
                <div key={r.return_id} className="p-4 md:p-5 rounded-2xl border border-[#F1F5F9] bg-[#F8FAFC] flex flex-col md:flex-row items-start md:items-center justify-between gap-4 hover:border-indigo-200 transition-colors">
                  <div>
                    <div className="text-xs font-semibold text-[#64748B] flex items-center gap-2">
                      <span>Return ID: <strong className="font-mono text-[#0F172A]">{r.return_id}</strong></span>
                      <span>•</span>
                      <span>Order: <strong className="text-indigo-600 font-mono">{r.order_id}</strong></span>
                    </div>
                    <div className="text-sm font-bold text-[#0F172A] mt-1">Item ID: {r.order_item_id}</div>
                    <div className="text-xs text-[#64748B] mt-1 flex items-center gap-1.5">
                      <span className="font-semibold text-gray-700">Reason:</span>
                      <span className="bg-gray-100 text-gray-700 px-2 py-0.5 rounded text-[11px] font-medium">{r.reason}</span>
                    </div>
                  </div>
                  <div>
                    <span className={`inline-flex items-center gap-1.5 px-3.5 py-1 rounded-full text-xs font-bold ${
                      r.status === 'COMPLETED' || r.status === 'APPROVED' ? 'bg-emerald-100 text-emerald-800 border border-emerald-200' :
                      r.status === 'REJECTED' ? 'bg-rose-100 text-rose-800 border border-rose-200' : 'bg-amber-100 text-amber-800 border border-amber-200'
                    }`}>
                      {r.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Section 2: Refunds */}
      {(activeTab === 'ALL' || activeTab === 'REFUNDS') && (
        <div className="bg-white border border-[#E2E8F0] rounded-3xl p-6 md:p-8 shadow-2xs space-y-6">
          <div className="flex items-center justify-between border-b border-[#F1F5F9] pb-4">
            <h2 className="text-lg font-extrabold text-[#0F172A] flex items-center gap-2.5">
              <div className="p-2 bg-emerald-50 text-emerald-600 rounded-xl">
                <DollarSign size={20} />
              </div>
              Issued Refunds ({refunds.length})
            </h2>
            <span className="text-xs text-[#94A3B8] font-semibold">Credited to Account</span>
          </div>

          {loadingRefunds ? (
            <div className="text-center py-8 text-[#94A3B8] text-xs font-medium">Loading refund records...</div>
          ) : refunds.length === 0 ? (
            <div className="text-center py-10 text-[#94A3B8] space-y-2">
              <DollarSign size={32} className="mx-auto text-gray-300 mb-1" />
              <div className="text-sm font-bold text-[#0F172A]">No Processed Refunds</div>
              <p className="text-xs text-[#64748B] max-w-sm mx-auto">There are no issued refund records associated with your profile.</p>
            </div>
          ) : (
            <div className="space-y-3">
              {refunds.map(rf => (
                <div key={rf.refund_id} className="p-4 md:p-5 rounded-2xl border border-[#F1F5F9] bg-[#F8FAFC] flex flex-col md:flex-row items-start md:items-center justify-between gap-4 hover:border-emerald-200 transition-colors">
                  <div>
                    <div className="text-xs font-semibold text-[#64748B] flex items-center gap-2">
                      <span>Refund ID: <strong className="font-mono text-[#0F172A]">{rf.refund_id}</strong></span>
                      <span>•</span>
                      <span>Order: <strong className="text-indigo-600 font-mono">{rf.order_id}</strong></span>
                    </div>
                    <div className="text-xs text-[#64748B] mt-1 font-medium">Associated Return Claim: {rf.return_id}</div>
                  </div>
                  <div className="text-left md:text-right">
                    <div className="text-lg font-black text-emerald-600">
                      +₹{(rf.refund_amount || 0).toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                    </div>
                    <span className="inline-block text-[10px] uppercase font-extrabold px-2.5 py-0.5 rounded bg-emerald-100 text-emerald-800 mt-1">
                      {rf.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Section 3: Payment History */}
      {(activeTab === 'ALL' || activeTab === 'PAYMENTS') && (
        <div className="bg-white border border-[#E2E8F0] rounded-3xl p-6 md:p-8 shadow-2xs space-y-6">
          <div className="flex items-center justify-between border-b border-[#F1F5F9] pb-4">
            <h2 className="text-lg font-extrabold text-[#0F172A] flex items-center gap-2.5">
              <div className="p-2 bg-indigo-50 text-indigo-600 rounded-xl">
                <CreditCard size={20} />
              </div>
              Payment Transaction Summaries ({payments.length})
            </h2>
            <span className="text-xs text-[#94A3B8] font-semibold">SSL Encrypted Logs</span>
          </div>

          {loadingPayments ? (
            <div className="text-center py-8 text-[#94A3B8] text-xs font-medium">Loading payment records...</div>
          ) : payments.length === 0 ? (
            <div className="text-center py-10 text-[#94A3B8] space-y-2">
              <CreditCard size={32} className="mx-auto text-gray-300 mb-1" />
              <div className="text-sm font-bold text-[#0F172A]">No Payment Records</div>
              <p className="text-xs text-[#64748B] max-w-sm mx-auto">No transaction summaries found for this customer account.</p>
            </div>
          ) : (
            <div className="space-y-3">
              {payments.map(p => (
                <div key={p.payment_id} className="p-4 md:p-5 rounded-2xl border border-[#F1F5F9] bg-[#F8FAFC] flex flex-col md:flex-row items-start md:items-center justify-between gap-4 hover:border-indigo-200 transition-colors">
                  <div>
                    <div className="text-xs font-semibold text-[#64748B] flex items-center gap-2">
                      <span>Payment ID: <strong className="font-mono text-[#0F172A]">{p.payment_id}</strong></span>
                      <span>•</span>
                      <span>Order: <strong className="text-indigo-600 font-mono">{p.order_id}</strong></span>
                    </div>
                    <div className="text-xs text-[#64748B] mt-1 font-medium">Payment Method: <span className="font-bold text-gray-800 uppercase">{p.method}</span></div>
                  </div>
                  <div className="text-left md:text-right">
                    <div className="text-lg font-black text-[#0F172A]">
                      ₹{(p.amount || 0).toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                    </div>
                    <span className="inline-block text-[10px] uppercase font-extrabold px-2.5 py-0.5 rounded bg-blue-100 text-blue-800 mt-1">
                      {p.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

