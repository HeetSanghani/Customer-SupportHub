import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { authApi } from '../../api/auth'
import { ordersApi } from '../../api/orders'
import { ticketsApi } from '../../api/tickets'
import {
  User,
  ShoppingBag,
  Truck,
  RotateCcw,
  MessageSquare,
  ShieldCheck,
  ArrowRight,
  Clock,
  CheckCircle2,
  AlertCircle,
  ArrowLeft,
  Sparkles
} from 'lucide-react'

export default function CustomerDashboard() {
  const { data: profile } = useQuery({
    queryKey: ['auth', 'me'],
    queryFn: async () => {
      const res = await authApi.me()
      return res.data
    },
  })

  const { data: orders = [] } = useQuery({
    queryKey: ['orders', 'me'],
    queryFn: async () => {
      const res = await ordersApi.getMyOrders()
      return res.data
    },
  })

  const { data: shipments = [] } = useQuery({
    queryKey: ['shipments', 'me'],
    queryFn: async () => {
      const res = await ordersApi.getMyShipments()
      return res.data
    },
  })

  const { data: returns = [] } = useQuery({
    queryKey: ['returns', 'me'],
    queryFn: async () => {
      const res = await ordersApi.getMyReturns()
      return res.data
    },
  })

  const { data: refunds = [] } = useQuery({
    queryKey: ['refunds', 'me'],
    queryFn: async () => {
      const res = await ordersApi.getMyRefunds()
      return res.data
    },
  })

  const { data: tickets = [] } = useQuery({
    queryKey: ['tickets', 'customer'],
    queryFn: async () => {
      const res = await ticketsApi.list()
      return res.data
    },
  })

  const activeTickets = tickets.filter(t => t.status !== 'resolved' && t.status !== 'closed')
  const totalRefundAmount = refunds.reduce((acc, r) => acc + (r.refund_amount || 0), 0)

  return (
    <div className="flex-1 overflow-y-auto bg-[#F8FAFC] p-4 md:p-8 space-y-6">
      {/* Welcome Banner */}
      <div className="bg-white border border-[#E2E8F0] rounded-3xl p-6 shadow-2xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <Link to="/customer" className="inline-flex items-center gap-1.5 text-xs font-extrabold text-indigo-600 hover:text-indigo-700 mb-2 transition-colors">
            <ArrowLeft size={14} /> Back to AI Chat
          </Link>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-black text-[#0F172A] tracking-tight">
              Welcome back, {profile?.name || 'Customer'}!
            </h1>
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
              <ShieldCheck size={14} className="text-emerald-500" />
              Verified Account ({profile?.customer_id || 'CUST-001'})
            </span>
          </div>
          <p className="text-xs md:text-sm text-[#64748B] mt-1">
            Manage your account transactions, track shipments, check return statuses, and review support history.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Link
            to="/customer/chat"
            className="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-extrabold shadow-xs transition-colors flex items-center gap-2"
          >
            <Sparkles size={14} className="text-amber-300" /> Live AI Assistant
          </Link>
        </div>
      </div>

      {/* KPI Cards Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Total Orders Card */}
        <div className="bg-white border border-[#E2E8F0] rounded-3xl p-6 shadow-2xs hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between mb-4">
            <div className="w-10 h-10 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold">
              <ShoppingBag size={20} />
            </div>
            <Link to="/customer/orders" className="text-xs font-bold text-indigo-600 hover:text-indigo-800 flex items-center gap-1">
              View all <ArrowRight size={12} />
            </Link>
          </div>
          <div className="text-2xl font-bold text-[#0F172A]">{orders.length}</div>
          <div className="text-xs text-[#64748B] font-medium mt-1">Total Account Orders</div>
        </div>

        {/* Active Shipments Card */}
        <div className="bg-white border border-[#E2E8F0] rounded-3xl p-6 shadow-2xs hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between mb-4">
            <div className="w-10 h-10 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center font-bold">
              <Truck size={20} />
            </div>
            <Link to="/customer/shipments" className="text-xs font-bold text-blue-600 hover:text-blue-800 flex items-center gap-1">
              View all <ArrowRight size={12} />
            </Link>
          </div>
          <div className="text-2xl font-bold text-[#0F172A]">{shipments.length}</div>
          <div className="text-xs text-[#64748B] font-medium mt-1">Shipment Records</div>
        </div>

        {/* Returns & Refunds Card */}
        <div className="bg-white border border-[#E2E8F0] rounded-3xl p-6 shadow-2xs hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between mb-4">
            <div className="w-10 h-10 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center font-bold">
              <RotateCcw size={20} />
            </div>
            <Link to="/customer/returns" className="text-xs font-bold text-amber-600 hover:text-amber-800 flex items-center gap-1">
              View all <ArrowRight size={12} />
            </Link>
          </div>
          <div className="text-2xl font-bold text-[#0F172A]">{returns.length}</div>
          <div className="text-xs text-[#64748B] font-medium mt-1">Returns (${totalRefundAmount.toFixed(2)} refunded)</div>
        </div>

        {/* Support History Card */}
        <div className="bg-white border border-[#E2E8F0] rounded-3xl p-6 shadow-2xs hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between mb-4">
            <div className="w-10 h-10 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold">
              <MessageSquare size={20} />
            </div>
            <Link to="/customer/support" className="text-xs font-bold text-emerald-600 hover:text-emerald-800 flex items-center gap-1">
              View all <ArrowRight size={12} />
            </Link>
          </div>
          <div className="text-2xl font-bold text-[#0F172A]">{tickets.length}</div>
          <div className="text-xs text-[#64748B] font-medium mt-1">{activeTickets.length} active tickets</div>
        </div>
      </div>

      {/* Main Section Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column (2 cols): Recent Orders & Shipments */}
        <div className="lg:col-span-2 space-y-6">
          {/* Recent Orders Card */}
          <div className="bg-white border border-[#E2E8F0] rounded-3xl p-6 shadow-2xs">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-bold text-[#0F172A] flex items-center gap-2">
                <ShoppingBag size={20} className="text-indigo-600" /> Recent Account Orders
              </h2>
              <Link to="/customer/orders" className="text-xs font-bold text-indigo-600 hover:underline">
                View All Orders
              </Link>
            </div>
            {orders.length === 0 ? (
              <div className="text-center py-8 text-[#94A3B8] text-sm font-semibold">No recent orders found.</div>
            ) : (
              <div className="space-y-3">
                {orders.slice(0, 3).map(order => (
                  <div key={order.order_id} className="flex items-center justify-between p-4 rounded-2xl border border-[#F1F5F9] hover:border-indigo-100 bg-[#F8FAFC] transition-colors">
                    <div>
                      <div className="text-sm font-bold text-[#0F172A]">{order.order_id}</div>
                      <div className="text-xs text-[#64748B] mt-0.5">{order.order_date ? new Date(order.order_date).toLocaleDateString() : 'Date N/A'}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-bold text-[#0F172A]">${(order.total_amount || 0).toFixed(2)}</div>
                      <span className={`inline-block text-[10px] font-bold px-2 py-0.5 rounded-full mt-0.5 ${
                        order.status === 'DELIVERED' ? 'bg-emerald-100 text-emerald-800' :
                        order.status === 'SHIPPED' ? 'bg-blue-100 text-blue-800' :
                        order.status === 'CANCELLED' ? 'bg-rose-100 text-rose-800' : 'bg-amber-100 text-amber-800'
                      }`}>
                        {order.status}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Active Shipments Card */}
          <div className="bg-white border border-[#E2E8F0] rounded-3xl p-6 shadow-2xs">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-bold text-[#0F172A] flex items-center gap-2">
                <Truck size={20} className="text-blue-600" /> Active Shipments
              </h2>
              <Link to="/customer/shipments" className="text-xs font-bold text-indigo-600 hover:underline">
                Track Shipments
              </Link>
            </div>
            {shipments.length === 0 ? (
              <div className="text-center py-8 text-[#94A3B8] text-sm font-semibold">No shipments currently active.</div>
            ) : (
              <div className="space-y-3">
                {shipments.slice(0, 3).map(s => (
                  <div key={s.shipment_id} className="p-4 rounded-2xl border border-[#F1F5F9] bg-[#F8FAFC] flex items-center justify-between">
                    <div>
                      <div className="text-xs font-semibold text-[#64748B]">Order: <span className="text-[#0F172A] font-bold">{s.order_id}</span></div>
                      <div className="text-sm font-bold text-[#0F172A] mt-1">{s.carrier || 'Carrier'} — {s.tracking_number || 'N/A'}</div>
                    </div>
                    <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2.5 py-1 rounded-lg">
                      {s.status}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right Column (1 col): Profile Summary & Support History */}
        <div className="space-y-6">
          {/* Profile Card */}
          <div className="bg-white border border-[#E2E8F0] rounded-3xl p-6 shadow-2xs">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold text-[#0F172A] flex items-center gap-2">
                <User size={20} className="text-indigo-600" /> Profile Summary
              </h2>
              <Link to="/customer/profile" className="text-xs font-bold text-indigo-600 hover:underline">
                Edit Profile
              </Link>
            </div>
            <div className="space-y-3 text-sm">
              <div>
                <div className="text-xs text-[#94A3B8] font-medium">Full Name</div>
                <div className="font-semibold text-[#0F172A]">{profile?.name}</div>
              </div>
              <div>
                <div className="text-xs text-[#94A3B8] font-medium">Email Address</div>
                <div className="font-semibold text-[#0F172A]">{profile?.email}</div>
              </div>
              <div>
                <div className="text-xs text-[#94A3B8] font-medium">Phone Number</div>
                <div className="font-semibold text-[#0F172A]">{profile?.phone || 'Not configured'}</div>
              </div>
              <div>
                <div className="text-xs text-[#94A3B8] font-medium">Shipping Address</div>
                <div className="font-semibold text-[#0F172A]">{profile?.address ? `${profile.address}, ${profile.city || ''} ${profile.state || ''}` : 'Not configured'}</div>
              </div>
            </div>
          </div>

          {/* Support History Summary Card */}
          <div className="bg-white border border-[#E2E8F0] rounded-3xl p-6 shadow-2xs">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold text-[#0F172A] flex items-center gap-2">
                <MessageSquare size={20} className="text-emerald-600" /> Active Support Conversations
              </h2>
              <Link to="/customer/support" className="text-xs font-bold text-indigo-600 hover:underline">
                View Support
              </Link>
            </div>
            {tickets.length === 0 ? (
              <div className="text-center py-6 text-[#94A3B8] text-sm font-semibold">No support tickets submitted.</div>
            ) : (
              <div className="space-y-3">
                {tickets.slice(0, 3).map(t => (
                  <div key={t.id} className="p-3 rounded-2xl border border-[#F1F5F9] bg-[#F8FAFC]">
                    <div className="flex items-center justify-between text-xs mb-1">
                      <span className="font-bold text-indigo-600 font-mono">{t.ref}</span>
                      <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded-full bg-gray-100 text-gray-700">{t.status}</span>
                    </div>
                    <div className="text-xs font-semibold text-[#0F172A] truncate">{t.subject}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
