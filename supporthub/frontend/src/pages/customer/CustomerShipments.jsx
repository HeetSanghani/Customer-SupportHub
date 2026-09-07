import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { ordersApi } from '../../api/orders'
import { ticketsApi } from '../../api/tickets'
import { Truck, PackageCheck, Calendar, ArrowLeft, Sparkles, Copy, Check, Clock, CheckCircle2, ArrowRight, ShieldCheck } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'

export default function CustomerShipments() {
  const navigate = useNavigate()
  const [copiedId, setCopiedId] = useState(null)
  const [filterStatus, setFilterStatus] = useState('ALL')

  const { data: shipments = [], isLoading } = useQuery({
    queryKey: ['shipments', 'me'],
    queryFn: async () => {
      const res = await ordersApi.getMyShipments()
      return res.data
    },
  })

  const handleCopyTracking = (id, trackingNum) => {
    if (!trackingNum) return
    navigator.clipboard.writeText(trackingNum)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 2000)
  }

  const handleTrackWithAI = async (orderId, trackingNum) => {
    try {
      const prompt = `What is the delivery status of order ${orderId} with tracking ${trackingNum}?`
      const res = await ticketsApi.create({
        subject: `Tracking inquiry for ${orderId}`,
        category: 'billing',
        body: prompt,
        channel: 'website_chat'
      })
      navigate(`/customer/chat/${res.data.id}`)
    } catch (err) {
      navigate('/customer/chat')
    }
  }

  const filteredShipments = shipments.filter(s => {
    const status = (s.status || '').toUpperCase()
    if (filterStatus === 'DELIVERED') return status === 'DELIVERED' || status === 'COMPLETED'
    if (filterStatus === 'ACTIVE') return status === 'SHIPPED' || status === 'IN_TRANSIT' || status === 'PROCESSING'
    return true
  })

  // Delivery progress helper
  const getProgressStep = (status) => {
    const s = (status || '').toUpperCase()
    if (s === 'DELIVERED' || s === 'COMPLETED') return 4
    if (s === 'IN_TRANSIT' || s === 'OUT_FOR_DELIVERY') return 3
    if (s === 'SHIPPED') return 2
    return 1
  }

  return (
    <div className="flex-1 h-full overflow-y-auto bg-[#F8FAFC] p-4 md:p-8 space-y-6 text-[#0F172A]">
      {/* Header Banner */}
      <div className="bg-white p-6 rounded-3xl border border-[#E2E8F0] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <Link to="/customer" className="inline-flex items-center gap-1.5 text-xs font-extrabold text-indigo-600 hover:text-indigo-700 mb-2 transition-colors">
            <ArrowLeft size={14} /> Back to AI Chat
          </Link>
          <h1 className="text-2xl font-black text-[#0F172A] tracking-tight flex items-center gap-2">
            My Shipments & Tracking
            <span className="text-xs font-bold bg-indigo-50 text-indigo-600 px-2.5 py-0.5 rounded-full border border-indigo-100">
              {shipments.length} Active
            </span>
          </h1>
          <p className="text-xs md:text-sm text-[#64748B] mt-0.5">View real-time courier updates, carrier dispatch logs, and estimated delivery dates.</p>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-2">
          {[
            { id: 'ALL', label: 'All Shipments' },
            { id: 'ACTIVE', label: 'In Transit' },
            { id: 'DELIVERED', label: 'Delivered' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setFilterStatus(tab.id)}
              className={`px-3.5 py-2 rounded-xl text-xs font-bold transition-all ${
                filterStatus === tab.id
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'bg-[#F8FAFC] text-[#64748B] hover:bg-gray-100 border border-[#E2E8F0]'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {isLoading ? (
        <div className="bg-white border border-[#E2E8F0] rounded-3xl p-12 text-center text-[#94A3B8] font-medium">
          Loading shipment tracking updates...
        </div>
      ) : filteredShipments.length === 0 ? (
        <div className="bg-white border border-[#E2E8F0] rounded-3xl p-12 text-center shadow-2xs max-w-lg mx-auto my-8 space-y-3">
          <div className="w-16 h-16 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-2 shadow-inner">
            <Truck size={32} />
          </div>
          <h3 className="text-lg font-bold text-[#0F172A]">No Shipments Found</h3>
          <p className="text-xs text-[#64748B] max-w-md mx-auto leading-relaxed">
            You currently have no shipments matching your filter criteria. Ask SupportHub AI if you need assistance tracking a recent purchase.
          </p>
          <button
            onClick={() => navigate('/customer/chat')}
            className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2.5 rounded-xl font-bold text-xs transition-all shadow-md active:scale-95 mt-2"
          >
            <Sparkles size={14} className="text-amber-300" /> Ask SupportHub AI <ArrowRight size={14} />
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6">
          {filteredShipments.map(s => {
            const currentStep = getProgressStep(s.status)
            const isDelivered = (s.status || '').toUpperCase() === 'DELIVERED'

            return (
              <div key={s.shipment_id} className="bg-white border border-[#E2E8F0] rounded-3xl p-6 md:p-8 shadow-2xs hover:shadow-md transition-all space-y-6">
                {/* Top Info Bar */}
                <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-[#F1F5F9] pb-4 gap-4">
                  <div>
                    <div className="text-xs font-semibold text-[#64748B] flex items-center gap-2">
                      <span>Shipment ID: <strong className="font-mono text-[#0F172A]">{s.shipment_id}</strong></span>
                      <span>•</span>
                      <span>Order Reference: <strong className="text-indigo-600 font-mono">{s.order_id}</strong></span>
                    </div>
                    <div className="text-lg font-extrabold text-[#0F172A] mt-1 flex items-center gap-2">
                      Carrier: {s.carrier || 'Shadowfax Express'}
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className={`inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-xs font-extrabold border ${
                      isDelivered 
                        ? 'bg-emerald-50 text-emerald-700 border-emerald-200' 
                        : 'bg-indigo-50 text-indigo-700 border-indigo-200'
                    }`}>
                      <span className={`w-2 h-2 rounded-full ${isDelivered ? 'bg-emerald-500' : 'bg-indigo-500 animate-pulse'}`}></span>
                      {s.status}
                    </span>
                    <button
                      onClick={() => handleTrackWithAI(s.order_id, s.tracking_number)}
                      className="px-3.5 py-1.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 rounded-xl text-xs font-bold flex items-center gap-1.5 transition-all active:scale-95"
                    >
                      <Sparkles size={14} className="text-amber-500" />
                      <span>Track with AI</span>
                    </button>
                  </div>
                </div>

                {/* Progress Step Bar */}
                <div className="bg-[#F8FAFC] p-5 rounded-2xl border border-[#E2E8F0]">
                  <div className="text-xs font-bold text-[#64748B] mb-4 uppercase tracking-wider">
                    Delivery Progress Lifecycle
                  </div>
                  <div className="grid grid-cols-4 gap-2 text-center relative">
                    {[
                      { step: 1, label: 'Order Placed' },
                      { step: 2, label: 'Dispatched' },
                      { step: 3, label: 'In Transit' },
                      { step: 4, label: 'Delivered' }
                    ].map(st => {
                      const isActive = currentStep >= st.step
                      return (
                        <div key={st.step} className="flex flex-col items-center space-y-2 z-10">
                          <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs transition-all ${
                            isActive 
                              ? 'bg-indigo-600 text-white shadow-md ring-4 ring-indigo-100' 
                              : 'bg-gray-200 text-gray-500'
                          }`}>
                            {isActive ? <CheckCircle2 size={16} /> : st.step}
                          </div>
                          <span className={`text-xs font-bold ${isActive ? 'text-[#0F172A]' : 'text-gray-400'}`}>
                            {st.label}
                          </span>
                        </div>
                      )
                    })}
                  </div>
                </div>

                {/* Tracking Details Grid */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
                  <div className="p-4 bg-[#F8FAFC] rounded-2xl border border-[#F1F5F9]">
                    <div className="text-xs text-[#94A3B8] font-medium">Logistics Partner</div>
                    <div className="font-bold text-[#0F172A] text-sm mt-1">{s.carrier || 'Shadowfax Courier'}</div>
                  </div>
                  <div className="p-4 bg-[#F8FAFC] rounded-2xl border border-[#F1F5F9]">
                    <div className="text-xs text-[#94A3B8] font-medium">Tracking Number</div>
                    <div className="font-bold text-indigo-700 font-mono text-sm mt-1 flex items-center justify-between">
                      <span>{s.tracking_number || 'N/A'}</span>
                      {s.tracking_number && (
                        <button
                          onClick={() => handleCopyTracking(s.shipment_id, s.tracking_number)}
                          className="px-2 py-1 bg-indigo-50 hover:bg-indigo-100 rounded text-indigo-600 transition-colors flex items-center gap-1 text-[11px] font-bold"
                        >
                          {copiedId === s.shipment_id ? <Check size={12} className="text-emerald-600" /> : <Copy size={12} />}
                          <span>{copiedId === s.shipment_id ? 'Copied' : 'Copy'}</span>
                        </button>
                      )}
                    </div>
                  </div>
                  <div className="p-4 bg-[#F8FAFC] rounded-2xl border border-[#F1F5F9]">
                    <div className="text-xs text-[#94A3B8] font-medium">Estimated Delivery</div>
                    <div className="font-bold text-[#0F172A] text-sm mt-1 flex items-center gap-1.5">
                      <Calendar size={14} className="text-indigo-600" />
                      {s.estimated_delivery_date ? new Date(s.estimated_delivery_date).toLocaleDateString('en-IN', { dateStyle: 'medium' }) : 'Pending Confirmation'}
                    </div>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

