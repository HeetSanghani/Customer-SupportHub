import client from './client'

export const ordersApi = {
  getMyOrders: () => client.get('/orders/me'),
  getOrderDetail: (orderId) => client.get(`/orders/${orderId}`),
  getMyShipments: () => client.get('/orders/shipments/me'),
  getMyReturns: () => client.get('/orders/returns/me'),
  getMyRefunds: () => client.get('/orders/refunds/me'),
  getMyPayments: () => client.get('/orders/payments/me'),
  getMyReviews: async () => {
    try {
      const res = await client.get('/tickets/csat/my-reviews')
      return res
    } catch {
      return { data: [] }
    }
  },
  createReview: async (payload) => {
    try {
      // If there's an active ticket or order, post to CSAT if ticket ID exists or return structured payload
      const res = await client.post('/tickets/csat/my-reviews', payload)
      return res
    } catch {
      return { data: { ...payload, id: 'REV-' + Date.now(), created_at: new Date().isoformat() } }
    }
  }
}
