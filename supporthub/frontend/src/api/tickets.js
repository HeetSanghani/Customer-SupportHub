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

  // Phase 6 — AI Agent Tools
  suggestReply: (id) =>
    client.post(`/tickets/${id}/suggest-reply`),

  summarize: (id) =>
    client.post(`/tickets/${id}/summarize`),

  getSimilar: (id) =>
    client.get(`/tickets/${id}/similar`),

  // Phase 15.5 — Action Lifecycle Endpoints
  escalate: (id) =>
    client.post(`/tickets/${id}/escalate`),

  accept: (id) =>
    client.post(`/tickets/${id}/accept`),

  resolve: (id) =>
    client.post(`/tickets/${id}/resolve`),

  reopen: (id) =>
    client.post(`/tickets/${id}/reopen`),
}

