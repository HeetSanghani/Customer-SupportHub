import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { authApi } from '../../api/auth'
import { Search, UserPlus, Edit2, Trash2, X, Check, Shield, UserCheck, AlertCircle } from 'lucide-react'

export default function UserManagement() {
  const queryClient = useQueryClient()
  const [searchTerm, setSearchTerm] = useState('')
  const [isInviteModalOpen, setIsInviteModalOpen] = useState(false)
  const [editingUser, setEditingUser] = useState(null)

  // Form states for Invite Modal
  const [inviteForm, setInviteForm] = useState({
    name: '',
    email: '',
    role: 'agent',
    status: 'active'
  })
  const [inviteError, setInviteError] = useState('')

  // Form states for Edit Modal
  const [editForm, setEditForm] = useState({
    name: '',
    email: '',
    role: '',
    status: ''
  })

  // Data fetching
  const { data: users = [], isLoading } = useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const res = await authApi.listUsers()
      return res.data
    }
  })

  // Create/Invite User Mutation
  const inviteMutation = useMutation({
    mutationFn: (data) => authApi.createUser(data),
    onSuccess: () => {
      queryClient.invalidateQueries(['users'])
      setIsInviteModalOpen(false)
      setInviteForm({ name: '', email: '', role: 'agent', status: 'active' })
      setInviteError('')
    },
    onError: (err) => {
      setInviteError(err.response?.data?.detail || 'Failed to create user')
    }
  })

  // Update User Mutation
  const updateMutation = useMutation({
    mutationFn: ({ id, data }) => authApi.updateUser(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries(['users'])
      setEditingUser(null)
    }
  })

  // Delete User Mutation
  const deleteMutation = useMutation({
    mutationFn: (id) => authApi.deleteUser(id),
    onSuccess: () => {
      queryClient.invalidateQueries(['users'])
      setEditingUser(null)
    }
  })

  // Filter users by search term
  const filteredUsers = users.filter(user =>
    user.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.role?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    String(user.id).includes(searchTerm)
  )

  const handleInviteSubmit = (e) => {
    e.preventDefault()
    if (!inviteForm.name || !inviteForm.email) {
      setInviteError('Please fill in all required fields.')
      return
    }
    inviteMutation.mutate(inviteForm)
  }

  const handleEditSubmit = (e) => {
    e.preventDefault()
    if (!editingUser) return
    updateMutation.mutate({ id: editingUser.id, data: editForm })
  }

  const openEditModal = (user) => {
    setEditingUser(user)
    setEditForm({
      name: user.name,
      email: user.email,
      role: user.role,
      status: user.status
    })
  }

  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8 text-[#1C1B2E]">
      {/* Top Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">User Management</h1>
          <p className="text-[#6C7089] text-sm mt-1">Manage everyone who can access SupportHub.</p>
        </div>
        <button
          onClick={() => {
            setIsInviteModalOpen(true)
            setInviteError('')
          }}
          className="flex items-center gap-2 bg-[#4F46E5] hover:bg-[#4338CA] text-white px-4 py-2.5 rounded-xl font-medium text-sm transition-colors shadow-sm"
        >
          <UserPlus size={16} /> + Invite User
        </button>
      </div>

      {/* Search Bar */}
      <div className="mb-6">
        <div className="relative max-w-md">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#9598B0]" size={16} />
          <input
            type="text"
            placeholder="Search by ID, name, email, or role..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 bg-white border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500 shadow-sm"
          />
        </div>
      </div>

      {/* Users Table */}
      {isLoading ? (
        <div className="flex justify-center items-center py-16">
          <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div>
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-[#E5E7F3] shadow-sm overflow-hidden">
          <table className="w-full text-left text-sm text-[#6C7089]">
            <thead className="bg-[#F9FAFB] border-b border-[#E5E7F3] text-xs uppercase font-bold text-[#9598B0]">
              <tr>
                <th className="px-6 py-4">Name</th>
                <th className="px-6 py-4">Email</th>
                <th className="px-6 py-4">Role</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4">Last Active</th>
                <th className="px-6 py-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E5E7F3]">
              {filteredUsers.length === 0 ? (
                <tr>
                  <td colSpan="6" className="text-center py-10 text-sm text-[#9598B0]">
                    No users found matching your search.
                  </td>
                </tr>
              ) : (
                filteredUsers.map(user => {
                  const initial = user.name ? user.name.charAt(0).toUpperCase() : 'U'
                  const roleBg =
                    user.role === 'admin' ? 'bg-purple-50 text-purple-700' :
                    user.role === 'manager' ? 'bg-blue-50 text-blue-700' :
                    user.role === 'agent' ? 'bg-indigo-50 text-indigo-700' : 'bg-gray-100 text-gray-700'

                  return (
                    <tr key={user.id} className="hover:bg-gray-50/80 transition-colors">
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <div className="w-9 h-9 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold text-xs shadow-sm">
                            {initial}
                          </div>
                          <span className="font-bold text-[#1C1B2E]">{user.name}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 font-medium text-[#6C7089]">{user.email}</td>
                      <td className="px-6 py-4">
                        <span className={`px-2.5 py-1 rounded-lg text-xs font-bold capitalize ${roleBg}`}>
                          {user.role === 'agent' ? 'Support Agent' : user.role === 'manager' ? 'Support Manager' : user.role}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-semibold ${
                          user.status === 'active' ? 'bg-emerald-50 text-emerald-600' :
                          user.status === 'invited' ? 'bg-amber-50 text-amber-600' :
                          'bg-red-50 text-red-600'
                        }`}>
                          <span className={`w-1.5 h-1.5 rounded-full ${
                            user.status === 'active' ? 'bg-emerald-500' :
                            user.status === 'invited' ? 'bg-amber-500' : 'bg-red-500'
                          }`}></span>
                          <span className="capitalize">{user.status}</span>
                        </span>
                      </td>
                      <td className="px-6 py-4 text-xs text-[#9598B0]">Just now</td>
                      <td className="px-6 py-4 text-right">
                        <button
                          onClick={() => openEditModal(user)}
                          className="px-3 py-1.5 text-xs font-semibold text-[#4F46E5] hover:bg-indigo-50 rounded-lg transition-colors border border-transparent hover:border-indigo-100"
                        >
                          Edit
                        </button>
                      </td>
                    </tr>
                  )
                })
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* Invite User Modal */}
      {isInviteModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden border border-[#E5E7F3]">
            <div className="flex justify-between items-center px-6 py-4 border-b border-[#E5E7F3]">
              <h3 className="font-bold text-lg text-[#1C1B2E]">Invite New User</h3>
              <button onClick={() => setIsInviteModalOpen(false)} className="text-gray-400 hover:text-gray-600 p-1 rounded-lg">
                <X size={18} />
              </button>
            </div>
            <form onSubmit={handleInviteSubmit} className="p-6 space-y-4">
              {inviteError && (
                <div className="flex items-center gap-2 p-3 bg-red-50 text-red-600 text-xs rounded-xl font-medium">
                  <AlertCircle size={16} />
                  <span>{inviteError}</span>
                </div>
              )}
              <div>
                <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Full Name</label>
                <input
                  type="text"
                  placeholder="e.g. Nina Cole"
                  value={inviteForm.name}
                  onChange={(e) => setInviteForm({ ...inviteForm, name: e.target.value })}
                  className="w-full px-3.5 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                  required
                />
              </div>
              <div>
                <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Email Address</label>
                <input
                  type="email"
                  placeholder="nina.cole@supporthub.com"
                  value={inviteForm.email}
                  onChange={(e) => setInviteForm({ ...inviteForm, email: e.target.value })}
                  className="w-full px-3.5 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                  required
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Role</label>
                  <select
                    value={inviteForm.role}
                    onChange={(e) => setInviteForm({ ...inviteForm, role: e.target.value })}
                    className="w-full px-3 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                  >
                    <option value="agent">Support Agent</option>
                    <option value="manager">Support Manager</option>
                    <option value="admin">Admin</option>
                    <option value="customer">Customer</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Status</label>
                  <select
                    value={inviteForm.status}
                    onChange={(e) => setInviteForm({ ...inviteForm, status: e.target.value })}
                    className="w-full px-3 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                  >
                    <option value="active">Active</option>
                    <option value="invited">Invited</option>
                    <option value="suspended">Suspended</option>
                  </select>
                </div>
              </div>
              <div className="flex justify-end gap-3 pt-4 border-t border-[#E5E7F3]">
                <button
                  type="button"
                  onClick={() => setIsInviteModalOpen(false)}
                  className="px-4 py-2 text-sm font-semibold text-gray-600 hover:bg-gray-100 rounded-xl"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={inviteMutation.isPending}
                  className="px-4 py-2 text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl disabled:opacity-50"
                >
                  {inviteMutation.isPending ? 'Sending Invite...' : 'Send Invite'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit User Modal */}
      {editingUser && (
        <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden border border-[#E5E7F3]">
            <div className="flex justify-between items-center px-6 py-4 border-b border-[#E5E7F3]">
              <h3 className="font-bold text-lg text-[#1C1B2E]">Edit User</h3>
              <button onClick={() => setEditingUser(null)} className="text-gray-400 hover:text-gray-600 p-1 rounded-lg">
                <X size={18} />
              </button>
            </div>
            <form onSubmit={handleEditSubmit} className="p-6 space-y-4">
              <div>
                <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Full Name</label>
                <input
                  type="text"
                  value={editForm.name}
                  onChange={(e) => setEditForm({ ...editForm, name: e.target.value })}
                  className="w-full px-3.5 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                  required
                />
              </div>
              <div>
                <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Email Address</label>
                <input
                  type="email"
                  value={editForm.email}
                  onChange={(e) => setEditForm({ ...editForm, email: e.target.value })}
                  className="w-full px-3.5 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                  required
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Role</label>
                  <select
                    value={editForm.role}
                    onChange={(e) => setEditForm({ ...editForm, role: e.target.value })}
                    className="w-full px-3 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                  >
                    <option value="agent">Support Agent</option>
                    <option value="manager">Support Manager</option>
                    <option value="admin">Admin</option>
                    <option value="customer">Customer</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Status</label>
                  <select
                    value={editForm.status}
                    onChange={(e) => setEditForm({ ...editForm, status: e.target.value })}
                    className="w-full px-3 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                  >
                    <option value="active">Active</option>
                    <option value="invited">Invited</option>
                    <option value="suspended">Suspended</option>
                  </select>
                </div>
              </div>
              <div className="flex justify-between items-center pt-4 border-t border-[#E5E7F3]">
                <button
                  type="button"
                  onClick={() => {
                    if (confirm(`Are you sure you want to delete ${editingUser.name}?`)) {
                      deleteMutation.mutate(editingUser.id)
                    }
                  }}
                  className="flex items-center gap-1.5 px-3 py-2 text-xs font-bold text-red-600 hover:bg-red-50 rounded-xl transition-colors"
                >
                  <Trash2 size={14} /> Delete User
                </button>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setEditingUser(null)}
                    className="px-4 py-2 text-sm font-semibold text-gray-600 hover:bg-gray-100 rounded-xl"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={updateMutation.isPending}
                    className="px-4 py-2 text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl disabled:opacity-50"
                  >
                    {updateMutation.isPending ? 'Saving...' : 'Save Changes'}
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
