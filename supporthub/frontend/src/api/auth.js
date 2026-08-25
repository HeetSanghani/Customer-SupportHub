import client from './client'

export const authApi = {
  login: (data) =>
    client.post('/auth/login', new URLSearchParams({
      username: data.email,
      password: data.password,
    }), { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }),

  register: (data) =>
    client.post('/auth/register', data),

  refresh: (refreshToken) =>
    client.post('/auth/refresh', { refresh_token: refreshToken }),

  me: () => client.get('/auth/me'),
  updateMe: (data) => client.patch('/auth/me', data),
  changePassword: (data) => client.post('/auth/change-password', data),
  listUsers: () => client.get('/auth/users'),
  createUser: (data) => client.post('/auth/users', data),
  updateUser: (id, data) => client.patch(`/auth/users/${id}`, data),
  deleteUser: (id) => client.delete(`/auth/users/${id}`),
}

