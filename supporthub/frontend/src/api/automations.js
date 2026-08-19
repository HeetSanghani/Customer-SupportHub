import client from './client'

export const getAutomations = async () => {
  const res = await client.get('/automations')
  return res.data
}

export const createAutomation = async (data) => {
  const res = await client.post('/automations', data)
  return res.data
}

export const updateAutomation = async (id, data) => {
  const res = await client.put(`/automations/${id}`, data)
  return res.data
}

export const deleteAutomation = async (id) => {
  const res = await client.delete(`/automations/${id}`)
  return res.data
}

export const toggleAutomation = async (id) => {
  const res = await client.patch(`/automations/${id}/toggle`)
  return res.data
}

export const testDryRun = async (data) => {
  const res = await client.post('/automations/test-dry-run', data)
  return res.data
}

export const seedDefaultAutomations = async () => {
  const res = await client.post('/automations/seed-defaults')
  return res.data
}
