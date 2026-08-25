import client from './client'

export const ordersApi = {
  getMyOrders: () => client.get('/orders/me'),
  getOrderDetail: (orderId) => client.get(`/orders/${orderId}`),
  getMyShipments: () => client.get('/orders/shipments/me'),
  getMyReturns: () => client.get('/orders/returns/me'),
  getMyRefunds: () => client.get('/orders/refunds/me'),
  getMyPayments: () => client.get('/orders/payments/me'),
}
