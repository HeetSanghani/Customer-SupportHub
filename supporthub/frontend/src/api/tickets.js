import client from './client'

export const ticketsApi = {
  list: (params) =>
    client.get('/tickets/', { params }),

  get: (id) =>
    client.get(`/tickets/${id}`),

  getMessages: (id) =>
    client.get(`/tickets/${id}/messages`),

  create: (data) =>
    client.post('/tickets/', data),

  update: (id, data) =>
    client.patch(`/tickets/${id}`, data),

  delete: (id) =>
    client.delete(`/tickets/${id}`),

  submitCsat: (id, data) =>
    client.post(`/tickets/${id}/csat`, data),

  getCsat: (id) =>
    client.get(`/tickets/${id}/csat`),

  getMyCsat: () =>
    client.get('/tickets/csat/my-reviews'),

  getAllCsat: () =>
    client.get('/tickets/csat/all'),
}
