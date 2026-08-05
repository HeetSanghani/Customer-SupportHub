import client from './client'

export const adminApi = {
  listChannels: () => client.get('/admin/channels'),
  createChannel: (data) => client.post('/admin/channels', data),
  updateChannel: (id, data) => client.patch(`/admin/channels/${id}`, data),
  updateChannelConfig: (id, data) => client.put(`/admin/channels/${id}/config`, data),
  deleteChannel: (id) => client.delete(`/admin/channels/${id}`),
  testEmailConnection: () => client.post('/admin/channels/test-email'),
  getAiSettings: () => client.get('/admin/ai-settings'),
  updateAiSettings: (data) => client.post('/admin/ai-settings', data),
  getSignature: () => client.get('/admin/signature'),
  updateSignature: (data) => client.put('/admin/signature', data),
  getEmailLogs: () => client.get('/admin/email-logs'),
  getEmailTemplates: () => client.get('/admin/email-templates'),
  updateEmailTemplate: (name, data) => client.put(`/admin/email-templates/${name}`, data),
  exportCsatCsv: () => client.get('/admin/reports/csat/export', { responseType: 'blob' }),
  exportPerformanceCsv: () => client.get('/admin/reports/performance/export', { responseType: 'blob' }),
}
