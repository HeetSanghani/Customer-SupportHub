import client from './client'

export const authApi = {
  login: (data) =>
    client.post('/auth/login', new URLSearchParams({
      username: data.email,
      password: data.password,
    }), { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }),

  register: (data) =>
    client.post('/auth/register', data),

  me: () => client.get('/auth/me'),
  listUsers: () => client.get('/auth/users'),
}
