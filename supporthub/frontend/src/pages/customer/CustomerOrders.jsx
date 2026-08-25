import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { ordersApi } from '../../api/orders'
import { authApi } from '../../api/auth'
import { ShoppingBag, Truck, PackageCheck, AlertCircle, Clock, ChevronDown, ChevronUp, Tag, ArrowRight } from 'lucide-react'

export default function CustomerOrders() {
  const [selectedOrderId, setSelectedOrderId] = useState(null)

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

  const { data: selectedOrderDetail, isLoading: detailLoading } = useQuery({
    queryKey: ['orders', selectedOrderId],
    queryFn: async () => {
      if (!selectedOrderId) return null
      const res = await ordersApi.getOrderDetail(selectedOrderId)
      return res.data
    },
    enabled: !!selectedOrderId
  })

  const getStatusBadge = (status) => {
    const s = (status || '').toUpperCase()
    if (s === 'DELIVERED' || s === 'COMPLETED') {
      return <span className="bg-emerald-50 text-emerald-600 px-3 py-1 rounded-full text-xs font-bold border border-emerald-200">DELIVERED</span>
    }
    if (s === 'SHIPPED' || s === 'IN_TRANSIT') {
      return <span className="bg-indigo-50 text-indigo-600 px-3 py-1 rounded-full text-xs font-bold border border-indigo-200">IN TRANSIT</span>
    }
    if (s === 'CANCELLED') {
      return <span className="bg-rose-50 text-rose-600 px-3 py-1 rounded-full text-xs font-bold border border-rose-200">CANCELLED</span>
    }
    return <span className="bg-amber-50 text-amber-600 px-3 py-1 rounded-full text-xs font-bold border border-amber-200">{s || 'PROCESSING'}</span>
  }

  return (
    <div className="flex-1 overflow-auto bg-[#F9FAFB] p-8 text-[#1C1B2E]">
      {/* Header */}
      <div className="mb-6 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">My Orders</h1>
          <p className="text-[#6C7089] text-sm">View and track all your purchases and delivery updates.</p>
        </div>
        {profile?.customer_id ? (
          <div className="bg-indigo-50 text-indigo-600 px-4 py-2 rounded-xl text-xs font-bold border border-indigo-100 flex items-center gap-2">
            <Tag size={14} /> Linked ID: {profile.customer_id}
          </div>
        ) : (
          <div className="bg-amber-50 text-amber-700 px-4 py-2 rounded-xl text-xs font-bold border border-amber-200 flex items-center gap-2">
            <AlertCircle size={14} /> Account Unlinked
          </div>
        )}
      </div>

      {ordersLoading ? (
        <div className="bg-white p-12 rounded-2xl border border-[#E5E7F3] shadow-sm text-center text-[#6C7089] font-medium">
          Loading your order history...
        </div>
      ) : ordersError ? (
        <div className="bg-rose-50 border border-rose-200 text-rose-600 p-6 rounded-2xl text-sm font-bold flex items-center gap-3">
          <AlertCircle size={18} /> Failed to load order history. Please refresh the page.
        </div>
      ) : orders.length === 0 ? (
        /* Empty State */
        <div className="bg-white p-12 rounded-2xl border border-[#E5E7F3] shadow-sm text-center max-w-lg mx-auto my-12">
          <div className="w-16 h-16 bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center mx-auto mb-4">
            <ShoppingBag size={32} />
          </div>
          <h2 className="text-xl font-bold text-[#1C1B2E] mb-2">No Orders Found</h2>
          <p className="text-[#6C7089] text-sm mb-6">
            {!profile?.customer_id 
              ? "Your account is currently unlinked from store purchasing history. Contact support or make a purchase to link your account." 
              : "You haven't placed any orders yet. Explore our store or contact support if you need assistance."}
          </p>
          <a href="/customer/chat" className="inline-flex items-center gap-2 bg-[#6366F1] hover:bg-[#4F46E5] text-white px-6 py-3 rounded-xl font-bold text-sm transition-colors shadow-sm">
            Chat with Support <ArrowRight size={16} />
          </a>
        </div>
      ) : (
        /* Orders List & Detail Layout */
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column: Order List */}
          <div className="lg:col-span-1 space-y-4">
            <h2 className="text-xs font-bold uppercase tracking-wider text-[#9598B0] px-1">Order History ({orders.length})</h2>
            {orders.map((order) => {
              const isSelected = selectedOrderId === order.order_id
              return (
                <div
                  key={order.order_id}
                  onClick={() => setSelectedOrderId(isSelected ? null : order.order_id)}
                  className={`bg-white p-5 rounded-2xl border cursor-pointer transition-all shadow-sm ${
                    isSelected ? 'border-[#6366F1] ring-2 ring-indigo-100' : 'border-[#E5E7F3] hover:border-indigo-200'
                  }`}
                >
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <div className="font-bold text-base text-[#1C1B2E]">{order.order_id}</div>
                      <div className="text-xs text-[#9598B0] flex items-center gap-1 mt-0.5">
                        <Clock size={12} /> {order.order_date ? new Date(order.order_date).toLocaleDateString() : 'N/A'}
                      </div>
                    </div>
                    {getStatusBadge(order.status)}
                  </div>
                  <div className="flex justify-between items-end border-t border-[#F3F4F6] pt-3 mt-3">
                    <div className="text-xs text-[#6C7089]">Total Amount</div>
                    <div className="text-base font-extrabold text-[#1C1B2E]">${order.total_amount?.toFixed(2)}</div>
                  </div>
                </div>
              )
            })}
          </div>

          {/* Right Column: Selected Order Details */}
          <div className="lg:col-span-2">
            {!selectedOrderId ? (
              <div className="bg-white p-12 rounded-2xl border border-[#E5E7F3] shadow-sm text-center text-[#9598B0]">
                <PackageCheck size={40} className="mx-auto mb-3 text-[#9598B0]" />
                <p className="font-semibold text-sm">Select an order from the left to view items, tracking, and delivery details.</p>
              </div>
            ) : detailLoading ? (
              <div className="bg-white p-12 rounded-2xl border border-[#E5E7F3] shadow-sm text-center text-[#6C7089]">
                Loading order details...
              </div>
            ) : selectedOrderDetail ? (
              <div className="bg-white p-8 rounded-2xl border border-[#E5E7F3] shadow-sm space-y-6">
                <div className="flex justify-between items-start border-b border-[#E5E7F3] pb-6">
                  <div>
                    <h2 className="text-xl font-bold text-[#1C1B2E]">Order Details: {selectedOrderDetail.order.order_id}</h2>
                    <p className="text-xs text-[#9598B0] mt-1">Placed on {new Date(selectedOrderDetail.order.order_date).toLocaleString()}</p>
                  </div>
                  {getStatusBadge(selectedOrderDetail.order.status)}
                </div>

                {/* Items Section */}
                <div>
                  <h3 className="font-bold text-sm text-[#1C1B2E] mb-4">Purchased Items</h3>
                  <div className="space-y-3">
                    {selectedOrderDetail.items.map((item) => (
                      <div key={item.order_item_id} className="flex justify-between items-center bg-[#F9FAFB] p-4 rounded-xl border border-[#E5E7F3]">
                        <div>
                          <div className="font-bold text-sm text-[#1C1B2E]">{item.product_name}</div>
                          <div className="text-xs text-[#9598B0]">Product ID: {item.product_id} | Qty: {item.quantity}</div>
                        </div>
                        <div className="text-sm font-bold text-[#1C1B2E]">
                          ${item.total_price?.toFixed(2)}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Shipment Section */}
                {selectedOrderDetail.shipment && (
                  <div className="border-t border-[#E5E7F3] pt-6">
                    <h3 className="font-bold text-sm text-[#1C1B2E] mb-3 flex items-center gap-2">
                      <Truck size={16} className="text-indigo-600" /> Shipment & Tracking
                    </h3>
                    <div className="bg-indigo-50/50 p-5 rounded-xl border border-indigo-100 grid grid-cols-2 gap-4 text-xs">
                      <div>
                        <span className="text-[#9598B0] block">Carrier</span>
                        <span className="font-bold text-[#1C1B2E]">{selectedOrderDetail.shipment.carrier || 'Standard Courier'}</span>
                      </div>
                      <div>
                        <span className="text-[#9598B0] block">Tracking Number</span>
                        <span className="font-bold text-[#1C1B2E] font-mono">{selectedOrderDetail.shipment.tracking_number || 'N/A'}</span>
                      </div>
                      <div>
                        <span className="text-[#9598B0] block">Delivery Status</span>
                        <span className="font-bold text-indigo-600">{selectedOrderDetail.shipment.status}</span>
                      </div>
                      <div>
                        <span className="text-[#9598B0] block">Estimated Delivery</span>
                        <span className="font-bold text-[#1C1B2E]">{selectedOrderDetail.shipment.estimated_delivery_date ? new Date(selectedOrderDetail.shipment.estimated_delivery_date).toLocaleDateString() : 'N/A'}</span>
                      </div>
                    </div>
                  </div>
                )}

                {/* Total Summary */}
                <div className="border-t border-[#E5E7F3] pt-6 flex justify-between items-center">
                  <div className="text-xs text-[#9598B0]">
                    Payment Status: <span className="font-bold text-[#1C1B2E] uppercase">{selectedOrderDetail.payment?.status || 'PAID'}</span> ({selectedOrderDetail.payment?.method || 'CARD'})
                  </div>
                  <div className="text-right">
                    <span className="text-xs text-[#6C7089] block font-medium">Grand Total</span>
                    <span className="text-xl font-black text-[#1C1B2E]">${selectedOrderDetail.order.total_amount?.toFixed(2)}</span>
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
