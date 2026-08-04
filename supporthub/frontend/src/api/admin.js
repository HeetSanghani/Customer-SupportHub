import client from './client'

export const adminApi = {
  listChannels: () => client.get('/admin/channels'),
  createChannel: (data) => client.post('/admin/channels', data),
  updateChannel: (id, data) => client.patch(`/admin/channels/${id}`, data),
  deleteChannel: (id) => client.delete(`/admin/channels/${id}`),
  getAiSettings: () => client.get('/admin/ai-settings'),
  updateAiSettings: (data) => client.post('/admin/ai-settings', data),
}
