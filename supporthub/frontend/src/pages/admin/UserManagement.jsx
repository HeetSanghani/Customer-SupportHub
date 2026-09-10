import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { authApi } from '../../api/auth'
import { 
  Search, 
  UserPlus, 
  Edit2, 
  Trash2, 
  X, 
  Check, 
  Shield, 
  UserCheck, 
  AlertCircle, 
  Filter, 
  Users, 
  Phone, 
  Hash, 
  RotateCcw 
} from 'lucide-react'

export default function UserManagement() {
  const queryClient = useQueryClient()
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedRole, setSelectedRole] = useState('all')
  const [isInviteModalOpen, setIsInviteModalOpen] = useState(false)
  const [editingUser, setEditingUser] = useState(null)

  // Form states for Invite Modal
  const [inviteForm, setInviteForm] = useState({
    name: '',
    email: '',
    role: 'agent',
    status: 'active',
    phone: '',
    customer_id: ''
  })
  const [inviteError, setInviteError] = useState('')

  // Form states for Edit Modal
  const [editForm, setEditForm] = useState({
    name: '',
    email: '',
    role: '',
    status: '',
    phone: '',
    customer_id: ''
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
      setInviteForm({ name: '', email: '', role: 'agent', status: 'active', phone: '', customer_id: '' })
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

  // Compute Role Counts
  const roleCounts = {
    all: users.length,
    customer: users.filter(u => u.role === 'customer').length,
    agent: users.filter(u => u.role === 'agent').length,
    manager: users.filter(u => u.role === 'manager').length,
    admin: users.filter(u => u.role === 'admin').length,
  }

  // Filter users by role and search term
  const filteredUsers = users.filter(user => {
    // 1. Role filter
    if (selectedRole !== 'all' && user.role !== selectedRole) {
      return false
    }

    // 2. Search query filter
    const query = searchTerm.trim().toLowerCase()
    if (!query) return true

    const name = (user.name || '').toLowerCase()
    const email = (user.email || '').toLowerCase()
    const role = (user.role || '').toLowerCase()
    const customerId = (user.customer_id || '').toLowerCase()
    const id = String(user.id || '').toLowerCase()
    const phone = (user.phone || '').toLowerCase()
    const city = (user.city || '').toLowerCase()
    const state = (user.state || '').toLowerCase()

    // Plain text matching
    if (
      name.includes(query) ||
      email.includes(query) ||
      role.includes(query) ||
      customerId.includes(query) ||
      id.includes(query) ||
      phone.includes(query) ||
      city.includes(query) ||
      state.includes(query)
    ) {
      return true
    }

    // Normalized phone/digit matching: only when search term doesn't contain letters
    // (e.g. searching "9811987654", "9876", "555-010-0001", "555010")
    const hasLetters = /[a-zA-Z]/.test(query)
    if (!hasLetters) {
      const cleanQueryDigits = query.replace(/\D/g, '')
      const userPhoneDigits = (user.phone || '').replace(/\D/g, '')
      if (cleanQueryDigits.length >= 3 && userPhoneDigits.includes(cleanQueryDigits)) {
        return true
      }
    }

    return false
  })

  const isFiltered = searchTerm !== '' || selectedRole !== 'all'

  const resetFilters = () => {
    setSearchTerm('')
    setSelectedRole('all')
  }

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
      name: user.name || '',
      email: user.email || '',
      role: user.role || 'customer',
      status: user.status || 'active',
      phone: user.phone || '',
      customer_id: user.customer_id || ''
    })
  }

  const roleTabs = [
    { id: 'all', label: 'All Users', count: roleCounts.all },
    { id: 'customer', label: 'Customers', count: roleCounts.customer },
    { id: 'agent', label: 'Agents', count: roleCounts.agent },
    { id: 'manager', label: 'Managers', count: roleCounts.manager },
    { id: 'admin', label: 'Admins', count: roleCounts.admin },
  ]

  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8 text-[#1C1B2E]">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans'] text-[#1C1B2E] tracking-tight">
            User Management
          </h1>
          <p className="text-[#6C7089] text-sm mt-1">
            Manage everyone who can access SupportHub ({users.length} active users).
          </p>
        </div>
        <button
          onClick={() => {
            setIsInviteModalOpen(true)
            setInviteError('')
          }}
          className="flex items-center gap-2 bg-[#4F46E5] hover:bg-indigo-700 text-white px-4 py-2.5 rounded-xl font-semibold text-sm shadow-sm transition-all hover:shadow-indigo-100"
        >
          <UserPlus size={16} />
          <span>Add New User</span>
        </button>
      </div>

      {/* Role Filter Tabs */}
      <div className="flex flex-wrap items-center gap-2 mb-4">
        {roleTabs.map(tab => {
          const isActive = selectedRole === tab.id
          return (
            <button
              key={tab.id}
              onClick={() => setSelectedRole(tab.id)}
              className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold transition-all ${
                isActive
                  ? 'bg-indigo-600 text-white shadow-sm shadow-indigo-200'
                  : 'bg-white text-[#6C7089] hover:text-[#1C1B2E] hover:bg-gray-50 border border-[#E5E7F3]'
              }`}
            >
              <span>{tab.label}</span>
              <span
                className={`px-1.5 py-0.5 rounded-md text-[11px] font-semibold ${
                  isActive ? 'bg-white/20 text-white' : 'bg-slate-100 text-slate-600'
                }`}
              >
                {tab.count}
              </span>
            </button>
          )
        })}
      </div>

      {/* Search & Filter Controls Bar */}
      <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3 mb-6">
        {/* Search Bar with Clear Button */}
        <div className="relative flex-1 max-w-lg">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#9598B0]" size={16} />
          <input
            type="text"
            placeholder="Search by name, ID (CUST-001), mobile no, email, role, city..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-10 py-2.5 bg-white border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500 shadow-sm transition-colors placeholder:text-gray-400"
          />
          {searchTerm && (
            <button
              onClick={() => setSearchTerm('')}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 p-0.5 rounded-full hover:bg-gray-100"
              title="Clear search"
            >
              <X size={14} />
            </button>
          )}
        </div>

        {/* Role Select Dropdown & Clear Filter */}
        <div className="flex items-center gap-2 self-start md:self-auto">
          <div className="flex items-center gap-2 bg-white border border-[#E5E7F3] rounded-xl px-3 py-2 shadow-sm text-xs font-semibold text-[#6C7089]">
            <Filter size={14} className="text-indigo-600" />
            <span className="text-gray-400">Role:</span>
            <select
              value={selectedRole}
              onChange={(e) => setSelectedRole(e.target.value)}
              className="bg-transparent text-[#1C1B2E] font-bold focus:outline-none cursor-pointer"
            >
              <option value="all">All Users ({roleCounts.all})</option>
              <option value="customer">Customer ({roleCounts.customer})</option>
              <option value="agent">Agent ({roleCounts.agent})</option>
              <option value="manager">Manager ({roleCounts.manager})</option>
              <option value="admin">Admin ({roleCounts.admin})</option>
            </select>
          </div>

          {isFiltered && (
            <button
              onClick={resetFilters}
              className="flex items-center gap-1.5 px-3 py-2 text-xs font-semibold text-gray-600 hover:text-indigo-600 bg-white hover:bg-indigo-50/50 border border-[#E5E7F3] rounded-xl transition-all shadow-sm"
              title="Reset all filters"
            >
              <RotateCcw size={13} />
              <span>Reset</span>
            </button>
          )}
        </div>
      </div>

      {/* Result Count Indicator when filtering */}
      {isFiltered && (
        <div className="flex items-center justify-between text-xs text-[#6C7089] mb-3 px-1">
          <div>
            Showing <strong className="text-[#1C1B2E] font-bold">{filteredUsers.length}</strong> of{' '}
            <span>{users.length} users</span>
            {selectedRole !== 'all' && (
              <span className="ml-2 inline-flex items-center gap-1 px-2 py-0.5 bg-indigo-50 text-indigo-700 rounded-md font-medium capitalize">
                Role: {selectedRole}
              </span>
            )}
            {searchTerm && (
              <span className="ml-2 inline-flex items-center gap-1 px-2 py-0.5 bg-gray-100 text-gray-700 rounded-md font-medium">
                "{searchTerm}"
              </span>
            )}
          </div>
          <button
            onClick={resetFilters}
            className="text-xs text-indigo-600 hover:underline font-semibold"
          >
            Clear filters
          </button>
        </div>
      )}

      {/* Users Table */}
      {isLoading ? (
        <div className="flex justify-center items-center py-16 bg-white rounded-2xl border border-[#E5E7F3]">
          <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div>
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-[#E5E7F3] shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-[#6C7089] min-w-[760px]">
              <thead className="bg-[#F9FAFB] border-b border-[#E5E7F3] text-xs uppercase font-bold text-[#9598B0] whitespace-nowrap">
                <tr>
                  <th className="px-6 py-4">Name</th>
                  <th className="px-6 py-4">Email</th>
                  <th className="px-6 py-4">Role</th>
                  <th className="px-6 py-4">Customer ID</th>
                  <th className="px-6 py-4">Phone</th>
                  <th className="px-6 py-4">Status</th>
                  <th className="px-6 py-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E5E7F3]">
              {filteredUsers.length === 0 ? (
                <tr>
                  <td colSpan="7" className="text-center py-16 text-sm text-[#9598B0]">
                    <div className="flex flex-col items-center justify-center gap-2">
                      <div className="w-12 h-12 rounded-full bg-gray-100 flex items-center justify-center text-gray-400 mb-1">
                        <Search size={22} />
                      </div>
                      <p className="font-semibold text-gray-700 text-base">No users found</p>
                      <p className="text-xs text-gray-500 max-w-sm text-center">
                        No user matched "{searchTerm || selectedRole}". Try adjusting your search or role filter.
                      </p>
                      {isFiltered && (
                        <button
                          onClick={resetFilters}
                          className="mt-3 px-4 py-2 text-xs font-bold text-indigo-600 hover:text-white bg-indigo-50 hover:bg-indigo-600 rounded-xl transition-all"
                        >
                          Reset all filters
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ) : (
                filteredUsers.map(user => {
                  const initial = user.name ? user.name.charAt(0).toUpperCase() : 'U'
                  const roleBg =
                    user.role === 'admin' ? 'bg-purple-50 text-purple-700 border border-purple-200' :
                    user.role === 'manager' ? 'bg-blue-50 text-blue-700 border border-blue-200' :
                    user.role === 'agent' ? 'bg-indigo-50 text-indigo-700 border border-indigo-200' : 
                    'bg-slate-50 text-slate-700 border border-slate-200'

                  return (
                    <tr key={user.id} className="hover:bg-gray-50/80 transition-colors">
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <div className="w-9 h-9 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold text-xs shadow-sm">
                            {initial}
                          </div>
                          <div>
                            <span className="font-bold text-[#1C1B2E] block">{user.name}</span>
                            {user.city && (
                              <span className="text-[11px] text-gray-400">{user.city}{user.state ? `, ${user.state}` : ''}</span>
                            )}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 font-medium text-[#6C7089]">{user.email}</td>
                      <td className="px-6 py-4">
                        <span className={`px-2.5 py-1 rounded-lg text-xs font-bold capitalize ${roleBg}`}>
                          {user.role === 'agent' ? 'Agent' : user.role === 'manager' ? 'Manager' : user.role === 'admin' ? 'Admin' : 'Customer'}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {user.customer_id ? (
                          <span className="font-mono text-xs font-semibold px-2 py-0.5 bg-slate-100 text-slate-800 rounded border border-slate-200">
                            {user.customer_id}
                          </span>
                        ) : (
                          <span className="text-slate-400 text-xs">N/A</span>
                        )}
                      </td>
                      <td className="px-6 py-4 text-xs font-medium text-[#6C7089] whitespace-nowrap">
                        {user.phone || <span className="text-slate-400">N/A</span>}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
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
                      <td className="px-6 py-4 text-right whitespace-nowrap">
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
        </div>
      )}

      {/* Invite User Modal */}
      {isInviteModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden border border-[#E5E7F3]">
            <div className="flex justify-between items-center px-6 py-4 border-b border-[#E5E7F3]">
              <h3 className="font-bold text-lg text-[#1C1B2E]">Add New User</h3>
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
                  <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Phone / Mobile</label>
                  <input
                    type="text"
                    placeholder="+91-9876543210"
                    value={inviteForm.phone}
                    onChange={(e) => setInviteForm({ ...inviteForm, phone: e.target.value })}
                    className="w-full px-3.5 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Customer ID (optional)</label>
                  <input
                    type="text"
                    placeholder="CUST-026"
                    value={inviteForm.customer_id}
                    onChange={(e) => setInviteForm({ ...inviteForm, customer_id: e.target.value })}
                    className="w-full px-3.5 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500 font-mono"
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Role</label>
                  <select
                    value={inviteForm.role}
                    onChange={(e) => setInviteForm({ ...inviteForm, role: e.target.value })}
                    className="w-full px-3 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                  >
                    <option value="customer">Customer</option>
                    <option value="agent">Support Agent</option>
                    <option value="manager">Support Manager</option>
                    <option value="admin">Admin</option>
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
                  {inviteMutation.isPending ? 'Saving...' : 'Add User'}
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
                  <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Phone / Mobile</label>
                  <input
                    type="text"
                    value={editForm.phone}
                    onChange={(e) => setEditForm({ ...editForm, phone: e.target.value })}
                    className="w-full px-3.5 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Customer ID</label>
                  <input
                    type="text"
                    value={editForm.customer_id}
                    onChange={(e) => setEditForm({ ...editForm, customer_id: e.target.value })}
                    className="w-full px-3.5 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500 font-mono"
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Role</label>
                  <select
                    value={editForm.role}
                    onChange={(e) => setEditForm({ ...editForm, role: e.target.value })}
                    className="w-full px-3 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                  >
                    <option value="customer">Customer</option>
                    <option value="agent">Support Agent</option>
                    <option value="manager">Support Manager</option>
                    <option value="admin">Admin</option>
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
