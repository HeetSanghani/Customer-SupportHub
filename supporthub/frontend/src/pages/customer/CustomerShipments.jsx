import { useQuery } from '@tanstack/react-query'
import { ordersApi } from '../../api/orders'
import { Truck, PackageCheck, Calendar, ArrowLeft } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function CustomerShipments() {
  const { data: shipments = [], isLoading } = useQuery({
    queryKey: ['shipments', 'me'],
    queryFn: async () => {
      const res = await ordersApi.getMyShipments()
      return res.data
    },
  })

  return (
    <div className="flex-1 overflow-y-auto bg-[#F6F7FC] p-8 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 text-xs text-[#6C7089] mb-1">
            <Link to="/customer" className="hover:text-indigo-600 flex items-center gap-1"><ArrowLeft size={12}/> Dashboard</Link> / Shipments
          </div>
          <h1 className="text-2xl font-bold text-[#1C1B2E]">My Shipments & Tracking</h1>
          <p className="text-sm text-[#6C7089]">View active order shipments, carrier updates, and estimated delivery dates.</p>
        </div>
      </div>

      {isLoading ? (
        <div className="text-center py-12 text-[#9598B0]">Loading shipment details...</div>
      ) : shipments.length === 0 ? (
        <div className="bg-white border border-[#E5E7F3] rounded-2xl p-12 text-center shadow-sm">
          <Truck size={48} className="mx-auto text-indigo-300 mb-4" />
          <h3 className="text-lg font-bold text-[#1C1B2E]">No Shipments Found</h3>
          <p className="text-sm text-[#6C7089] max-w-md mx-auto mt-1">
            You currently have no active or completed shipments associated with your customer account.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6">
          {shipments.map(s => (
            <div key={s.shipment_id} className="bg-white border border-[#E5E7F3] rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow">
              <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-[#F0F1F7] pb-4 mb-4 gap-4">
                <div>
                  <div className="text-xs font-semibold text-[#6C7089]">Shipment ID: <span className="font-bold text-[#1C1B2E]">{s.shipment_id}</span></div>
                  <div className="text-sm font-bold text-[#1C1B2E] mt-0.5">Order Reference: {s.order_id}</div>
                </div>
                <div>
                  <span className={`inline-block px-3 py-1 rounded-full text-xs font-bold ${
                    s.status === 'DELIVERED' ? 'bg-emerald-100 text-emerald-800' :
                    s.status === 'SHIPPED' || s.status === 'IN_TRANSIT' ? 'bg-blue-100 text-blue-800' : 'bg-amber-100 text-amber-800'
                  }`}>
                    {s.status}
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-sm">
                <div className="p-3 bg-[#FAFAFE] rounded-xl border border-[#F0F1F7]">
                  <div className="text-xs text-[#9598B0] font-medium">Carrier</div>
                  <div className="font-bold text-[#1C1B2E] mt-0.5">{s.carrier || 'Standard Shipping'}</div>
                </div>
                <div className="p-3 bg-[#FAFAFE] rounded-xl border border-[#F0F1F7]">
                  <div className="text-xs text-[#9598B0] font-medium">Tracking Number</div>
                  <div className="font-bold text-[#1C1B2E] mt-0.5">{s.tracking_number || 'N/A'}</div>
                </div>
                <div className="p-3 bg-[#FAFAFE] rounded-xl border border-[#F0F1F7]">
                  <div className="text-xs text-[#9598B0] font-medium">Estimated Delivery</div>
                  <div className="font-bold text-[#1C1B2E] mt-0.5">
                    {s.estimated_delivery_date ? new Date(s.estimated_delivery_date).toLocaleDateString() : 'Pending Confirmation'}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
