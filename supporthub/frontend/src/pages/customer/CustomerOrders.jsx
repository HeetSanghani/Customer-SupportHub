import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useNavigate, Link } from 'react-router-dom'
import { ordersApi } from '../../api/orders'
import { authApi } from '../../api/auth'
import { ticketsApi } from '../../api/tickets'
import { 
  ShoppingBag, Truck, PackageCheck, AlertCircle, Clock, Tag, 
  ArrowRight, ArrowLeft, Sparkles, Search, CheckCircle2, XCircle, 
  RefreshCw, Copy, Check, ExternalLink, ShieldCheck, ChevronRight
} from 'lucide-react'

export default function CustomerOrders() {
  const navigate = useNavigate()
  const [selectedOrderId, setSelectedOrderId] = useState(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [activeTab, setActiveTab] = useState('ALL')
  const [isAskingAI, setIsAskingAI] = useState(false)
  const [copiedTracking, setCopiedTracking] = useState(false)

  const { data: profile } = useQuery({
    queryKey: ['auth', 'me'],
    queryFn: async () => {
      const res = await authApi.me()
      return res.data
    }
  })

  const { data: orders = [], isLoading: ordersLoading, error: ordersError } = useQuery({
    queryKey: ['orders', 'me'],
    queryFn: async () => {
      const res = await ordersApi.getMyOrders()
      return res.data
    }
  })

  // Filter orders by tab and search query
  const filteredOrders = orders.filter(o => {
    const s = (o.status || '').toUpperCase()
    const matchesTab = 
      activeTab === 'ALL' ? true :
      activeTab === 'DELIVERED' ? (s === 'DELIVERED' || s === 'COMPLETED') :
      activeTab === 'TRANSIT' ? (s === 'SHIPPED' || s === 'IN_TRANSIT') :
      activeTab === 'PROCESSING' ? (s === 'PROCESSING' || s === 'PENDING') :
      activeTab === 'CANCELLED' ? (s === 'CANCELLED') : true

    if (!matchesTab) return false

    if (!searchQuery.trim()) return true
    const q = searchQuery.toLowerCase()
    return o.order_id?.toLowerCase().includes(q) || o.status?.toLowerCase().includes(q)
  })

  const { data: selectedOrderDetail, isLoading: detailLoading } = useQuery({
    queryKey: ['orders', selectedOrderId],
    queryFn: async () => {
      if (!selectedOrderId) return null
      const res = await ordersApi.getOrderDetail(selectedOrderId)
      return res.data
    },
    enabled: !!selectedOrderId
  })

  const handleAskAIAboutOrder = async (orderId) => {
    setIsAskingAI(true)
    try {
      const prompt = `give me the product info. of ${orderId}`
      const res = await ticketsApi.create({
        subject: prompt,
        category: 'billing',
        body: prompt,
        channel: 'website_chat'
      })
      navigate(`/customer/chat/${res.data.id}`)
    } catch (err) {
      alert(`Failed to connect with AI: ${err.message}`)
    } finally {
      setIsAskingAI(false)
    }
  }

  const handleCopyTracking = (trackingNum) => {
    if (!trackingNum) return
    navigator.clipboard.writeText(trackingNum)
    setCopiedTracking(true)
    setTimeout(() => setCopiedTracking(false), 2000)
  }

  const getStatusBadge = (status) => {
    const s = (status || '').toUpperCase()
    if (s === 'DELIVERED' || s === 'COMPLETED') {
      return (
        <span className="inline-flex items-center gap-1.5 bg-emerald-50 text-emerald-700 px-3 py-1 rounded-full text-xs font-bold border border-emerald-200 shadow-2xs">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
          DELIVERED
        </span>
      )
    }
    if (s === 'SHIPPED' || s === 'IN_TRANSIT') {
      return (
        <span className="inline-flex items-center gap-1.5 bg-indigo-50 text-indigo-700 px-3 py-1 rounded-full text-xs font-bold border border-indigo-200 shadow-2xs">
          <span className="w-1.5 h-1.5 rounded-full bg-indigo-500 animate-pulse"></span>
          IN TRANSIT
        </span>
      )
    }
    if (s === 'CANCELLED') {
      return (
        <span className="inline-flex items-center gap-1.5 bg-rose-50 text-rose-700 px-3 py-1 rounded-full text-xs font-bold border border-rose-200">
          <XCircle size={12} />
          CANCELLED
        </span>
      )
    }
    return (
      <span className="inline-flex items-center gap-1.5 bg-amber-50 text-amber-700 px-3 py-1 rounded-full text-xs font-bold border border-amber-200">
        <Clock size={12} />
        {s || 'PROCESSING'}
      </span>
    )
  }

  // Calculate order stats
  const totalOrdersCount = orders.length
  const deliveredCount = orders.filter(o => ['DELIVERED', 'COMPLETED'].includes((o.status || '').toUpperCase())).length
  const activeCount = orders.filter(o => ['SHIPPED', 'IN_TRANSIT', 'PROCESSING', 'PENDING'].includes((o.status || '').toUpperCase())).length
  const totalSpent = orders.reduce((sum, o) => sum + (o.total_amount || 0), 0)

  return (
    <div className="flex-1 h-full overflow-y-auto bg-[#F8FAFC] p-4 md:p-8 text-[#0F172A] space-y-6">
      {/* Top Header & Search Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-3xl border border-[#E2E8F0] shadow-sm">
        <div>
          <Link to="/customer" className="inline-flex items-center gap-1.5 text-xs font-extrabold text-indigo-600 hover:text-indigo-700 mb-2 transition-colors">
            <ArrowLeft size={14} /> Back to AI Chat
          </Link>
          <h1 className="text-2xl font-black text-[#0F172A] tracking-tight flex items-center gap-2">
            My Orders
            <span className="text-xs font-bold bg-indigo-50 text-indigo-600 px-2.5 py-0.5 rounded-full border border-indigo-100">
              {orders.length} Total
            </span>
          </h1>
          <p className="text-xs md:text-sm text-[#64748B] mt-0.5">View and track all your purchases, invoice summaries, and delivery updates.</p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <div className="relative flex-1 min-w-[200px]">
            <Search size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              placeholder="Search by Order ID or Status..."
              className="w-full pl-10 pr-4 py-2.5 bg-[#F8FAFC] border border-[#E2E8F0] rounded-2xl text-xs focus:outline-none focus:border-indigo-500 font-medium transition-colors"
            />
            {searchQuery && (
              <button onClick={() => setSearchQuery('')} className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-gray-400 hover:text-gray-600">
                Clear
              </button>
            )}
          </div>
          {profile?.customer_id ? (
            <div className="bg-indigo-50 text-indigo-700 px-3.5 py-2.5 rounded-2xl text-xs font-bold border border-indigo-100 flex items-center gap-2 shrink-0">
              <Tag size={14} /> Linked ID: <span className="font-mono">{profile.customer_id}</span>
            </div>
          ) : (
            <div className="bg-amber-50 text-amber-800 px-3.5 py-2.5 rounded-2xl text-xs font-bold border border-amber-200 flex items-center gap-2 shrink-0">
              <AlertCircle size={14} /> Account Unlinked
            </div>
          )}
        </div>
      </div>

      {/* Orders Stats Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white p-4 md:p-5 rounded-2xl border border-[#E2E8F0] shadow-2xs">
          <div className="text-xs font-semibold text-[#64748B]">Total Purchases</div>
          <div className="text-xl font-black text-[#0F172A] mt-1">{totalOrdersCount} Orders</div>
        </div>
        <div className="bg-white p-4 md:p-5 rounded-2xl border border-[#E2E8F0] shadow-2xs">
          <div className="text-xs font-semibold text-[#64748B]">Delivered</div>
          <div className="text-xl font-black text-emerald-600 mt-1">{deliveredCount} Items</div>
        </div>
        <div className="bg-white p-4 md:p-5 rounded-2xl border border-[#E2E8F0] shadow-2xs">
          <div className="text-xs font-semibold text-[#64748B]">Active / In Transit</div>
          <div className="text-xl font-black text-indigo-600 mt-1">{activeCount} Shipments</div>
        </div>
        <div className="bg-white p-4 md:p-5 rounded-2xl border border-[#E2E8F0] shadow-2xs">
          <div className="text-xs font-semibold text-[#64748B]">Total Lifetime Value</div>
          <div className="text-xl font-black text-[#0F172A] mt-1">₹{totalSpent.toLocaleString('en-IN', { minimumFractionDigits: 2 })}</div>
        </div>
      </div>

      {/* Status Filter Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1 no-scrollbar">
        {[
          { id: 'ALL', label: 'All Orders', count: orders.length },
          { id: 'DELIVERED', label: 'Delivered', count: deliveredCount },
          { id: 'TRANSIT', label: 'In Transit', count: activeCount },
          { id: 'CANCELLED', label: 'Cancelled', count: orders.filter(o => (o.status || '').toUpperCase() === 'CANCELLED').length }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all shrink-0 flex items-center gap-2 ${
              activeTab === tab.id
                ? 'bg-indigo-600 text-white shadow-md'
                : 'bg-white text-[#64748B] hover:bg-indigo-50/60 border border-[#E2E8F0]'
            }`}
          >
            <span>{tab.label}</span>
            <span className={`px-2 py-0.5 rounded-full text-[10px] ${activeTab === tab.id ? 'bg-white/20 text-white' : 'bg-gray-100 text-gray-600'}`}>
              {tab.count}
            </span>
          </button>
        ))}
      </div>

      {ordersLoading ? (
        <div className="bg-white p-12 rounded-3xl border border-[#E2E8F0] shadow-2xs text-center text-[#64748B] font-medium">
          <RefreshCw size={24} className="animate-spin mx-auto text-indigo-600 mb-3" />
          Loading your order history...
        </div>
      ) : ordersError ? (
        <div className="bg-rose-50 border border-rose-200 text-rose-700 p-6 rounded-3xl text-sm font-bold flex items-center gap-3">
          <AlertCircle size={18} /> Failed to load order history. Please refresh the page.
        </div>
      ) : filteredOrders.length === 0 ? (
        /* Empty State */
        <div className="bg-white p-12 rounded-3xl border border-[#E2E8F0] shadow-2xs text-center max-w-lg mx-auto my-8">
          <div className="w-16 h-16 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-inner">
            <ShoppingBag size={32} />
          </div>
          <h2 className="text-xl font-bold text-[#0F172A] mb-2">No Orders Found</h2>
          <p className="text-[#64748B] text-sm mb-6 leading-relaxed">
            {!profile?.customer_id 
              ? "Your account is currently unlinked from store purchasing history. Contact support to link your account." 
              : "No orders match your selected filters. Explore our catalog or ask SupportHub AI for assistance."}
          </p>
          <Link to="/customer" className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-xl font-bold text-xs transition-transform active:scale-95 shadow-md">
            <Sparkles size={14} className="text-amber-300" /> Chat with SupportHub AI <ArrowRight size={14} />
          </Link>
        </div>
      ) : (
        /* Orders List & Detail Layout */
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column: Order List */}
          <div className="lg:col-span-1 space-y-3">
            <div className="flex justify-between items-center px-1">
              <h2 className="text-xs font-extrabold uppercase tracking-wider text-[#94A3B8]">Orders List ({filteredOrders.length})</h2>
              <span className="text-[10px] text-[#94A3B8] font-bold">Click to view details</span>
            </div>
            {filteredOrders.map((order) => {
              const isSelected = selectedOrderId === order.order_id
              return (
                <div
                  key={order.order_id}
                  onClick={() => setSelectedOrderId(isSelected ? null : order.order_id)}
                  className={`bg-white p-4 rounded-2xl border cursor-pointer transition-all shadow-2xs ${
                    isSelected ? 'border-indigo-600 ring-2 ring-indigo-100 shadow-md scale-[1.01]' : 'border-[#E2E8F0] hover:border-indigo-200'
                  }`}
                >
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <div className="font-bold text-sm text-[#0F172A] flex items-center gap-1.5">
                        {order.order_id}
                        {isSelected && <ChevronRight size={14} className="text-indigo-600" />}
                      </div>
                      <div className="text-xs text-[#94A3B8] flex items-center gap-1 mt-0.5 font-medium">
                        <Clock size={12} /> {order.order_date ? new Date(order.order_date).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }) : 'N/A'}
                      </div>
                    </div>
                    {getStatusBadge(order.status)}
                  </div>
                  <div className="flex justify-between items-end border-t border-[#F1F5F9] pt-2.5 mt-2.5">
                    <div className="text-xs text-[#64748B]">Total Amount</div>
                    <div className="text-base font-black text-[#0F172A]">
                      ₹{order.total_amount?.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                    </div>
                  </div>
                </div>
              )
            })}
          </div>

          {/* Right Column: Selected Order Details */}
          <div className="lg:col-span-2">
            {!selectedOrderId ? (
              <div className="bg-white p-12 rounded-3xl border border-[#E2E8F0] shadow-2xs text-center text-[#94A3B8] space-y-3">
                <PackageCheck size={48} className="mx-auto text-indigo-300" />
                <h3 className="font-bold text-base text-[#0F172A]">Select an Order</h3>
                <p className="text-xs text-[#64748B] max-w-sm mx-auto">
                  Click any order from the left column to view purchased product details, shipment status, tracking info, and instant AI assistance.
                </p>
              </div>
            ) : detailLoading ? (
              <div className="bg-white p-12 rounded-3xl border border-[#E2E8F0] shadow-2xs text-center text-[#64748B]">
                <RefreshCw size={24} className="animate-spin mx-auto text-indigo-600 mb-3" />
                Loading order details...
              </div>
            ) : selectedOrderDetail ? (
              <div className="bg-white p-6 md:p-8 rounded-3xl border border-[#E2E8F0] shadow-2xs space-y-6">
                {/* Header */}
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center border-b border-[#E2E8F0] pb-6 gap-4">
                  <div>
                    <div className="flex items-center gap-2">
                      <h2 className="text-xl font-extrabold text-[#0F172A]">Order Details: {selectedOrderDetail.order.order_id}</h2>
                    </div>
                    <p className="text-xs text-[#94A3B8] mt-1 font-medium">
                      Placed on {new Date(selectedOrderDetail.order.order_date).toLocaleString('en-IN', { dateStyle: 'full', timeStyle: 'short' })}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    {getStatusBadge(selectedOrderDetail.order.status)}
                    <button
                      onClick={() => handleAskAIAboutOrder(selectedOrderDetail.order.order_id)}
                      disabled={isAskingAI}
                      className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-extrabold flex items-center gap-1.5 transition-all shadow-xs disabled:opacity-50 active:scale-95"
                    >
                      <Sparkles size={14} className="text-amber-300" />
                      <span>{isAskingAI ? 'Opening Chat...' : 'Ask AI About Order'}</span>
                    </button>
                  </div>
                </div>

                {/* Purchased Items Section */}
                <div>
                  <h3 className="font-bold text-sm text-[#0F172A] mb-3 flex items-center justify-between">
                    <span>Purchased Items ({selectedOrderDetail.items.length})</span>
                    <span className="text-xs text-[#94A3B8] font-normal">Verified Inventory</span>
                  </h3>
                  <div className="space-y-3">
                    {selectedOrderDetail.items.map((item) => (
                      <div key={item.order_item_id} className="flex flex-col sm:flex-row sm:items-center justify-between bg-[#F8FAFC] p-4 rounded-2xl border border-[#E2E8F0] gap-3">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold text-xs shrink-0 border border-indigo-100">
                            <ShoppingBag size={18} />
                          </div>
                          <div>
                            <div className="font-bold text-sm text-[#0F172A]">{item.product_name}</div>
                            <div className="text-xs text-[#64748B] mt-0.5 flex flex-wrap items-center gap-2">
                              <span>SKU: <code className="bg-indigo-50 text-indigo-700 font-mono text-[11px] px-1.5 py-0.5 rounded font-bold">{item.product_id}</code></span>
                              <span>•</span>
                              <span>Qty: <strong className="text-[#0F172A]">{item.quantity}</strong></span>
                              <span>•</span>
                              <span>Price: <strong className="text-[#0F172A]">₹{item.unit_price?.toLocaleString('en-IN', { minimumFractionDigits: 2 })}</strong></span>
                            </div>
                          </div>
                        </div>
                        <div className="text-right sm:text-right font-extrabold text-sm text-[#0F172A]">
                          ₹{item.total_price?.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Shipment Section */}
                {selectedOrderDetail.shipment && (
                  <div className="border-t border-[#E2E8F0] pt-6">
                    <h3 className="font-bold text-sm text-[#0F172A] mb-3 flex items-center gap-2">
                      <Truck size={18} className="text-indigo-600" /> Shipment & Real-time Tracking
                    </h3>
                    <div className="bg-indigo-50/50 p-5 rounded-2xl border border-indigo-100 grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
                      <div>
                        <span className="text-[#64748B] block font-medium">Logistics Partner / Carrier</span>
                        <span className="font-bold text-[#0F172A] text-sm mt-0.5 block">{selectedOrderDetail.shipment.carrier || 'Shadowfax Courier'}</span>
                      </div>
                      <div>
                        <span className="text-[#64748B] block font-medium">Tracking Reference Number</span>
                        <div className="flex items-center gap-2 mt-0.5">
                          <span className="font-bold text-indigo-700 font-mono text-xs">{selectedOrderDetail.shipment.tracking_number || 'N/A'}</span>
                          {selectedOrderDetail.shipment.tracking_number && (
                            <button
                              onClick={() => handleCopyTracking(selectedOrderDetail.shipment.tracking_number)}
                              className="p-1 hover:bg-indigo-100 rounded text-indigo-600 transition-colors flex items-center gap-1 text-[10px] font-bold"
                              title="Copy Tracking Number"
                            >
                              {copiedTracking ? <Check size={12} className="text-emerald-600" /> : <Copy size={12} />}
                              <span>{copiedTracking ? 'Copied' : 'Copy'}</span>
                            </button>
                          )}
                        </div>
                      </div>
                      <div>
                        <span className="text-[#64748B] block font-medium">Current Dispatch Status</span>
                        <span className="font-bold text-emerald-700 uppercase mt-0.5 block">{selectedOrderDetail.shipment.status}</span>
                      </div>
                      <div>
                        <span className="text-[#64748B] block font-medium">Estimated Arrival</span>
                        <span className="font-bold text-[#0F172A] text-xs mt-0.5 block">
                          {selectedOrderDetail.shipment.estimated_delivery_date ? new Date(selectedOrderDetail.shipment.estimated_delivery_date).toLocaleDateString('en-IN', { dateStyle: 'medium' }) : 'Pending Confirmation'}
                        </span>
                      </div>
                    </div>
                  </div>
                )}

                {/* Total Summary Footer */}
                <div className="border-t border-[#E2E8F0] pt-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                  <div className="text-xs text-[#64748B] space-y-1">
                    <div className="flex items-center gap-1.5 text-emerald-700 font-bold">
                      <ShieldCheck size={16} /> Safe & Verified Payment Transaction
                    </div>
                    <div>
                      Payment Status: <span className="font-bold text-[#0F172A] uppercase">{selectedOrderDetail.payment?.status || 'SUCCESS'}</span> ({selectedOrderDetail.payment?.method || 'DEBIT_CARD'})
                    </div>
                  </div>
                  <div className="text-left sm:text-right bg-gray-50 px-5 py-3 rounded-2xl border border-gray-200">
                    <span className="text-xs text-[#64748B] block font-medium">Grand Total</span>
                    <span className="text-2xl font-black text-[#0F172A]">₹{selectedOrderDetail.order.total_amount?.toLocaleString('en-IN', { minimumFractionDigits: 2 })}</span>
                  </div>
                </div>
              </div>
            ) : null}
          </div>
        </div>
      )}
    </div>
  )
}

