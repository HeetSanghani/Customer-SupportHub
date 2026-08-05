import client from './client'

export const knowledgeApi = {
  list: (params) => 
    client.get('/knowledge/', { params }),

  get: (id) =>
    client.get(`/knowledge/${id}`),

  create: (data) =>
    client.post('/knowledge/', data),

  update: (id, data) =>
    client.patch(`/knowledge/${id}`, data),

  delete: (id) =>
    client.delete(`/knowledge/${id}`),

  markHelpful: (id) =>
    client.post(`/knowledge/${id}/helpful`)
}
