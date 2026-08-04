import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { adminApi } from '../../api/admin'
import { Mail, MessageSquare, Phone, Instagram, Facebook, Plus, X, AlertCircle, Settings2, Trash2, Key, Link2 } from 'lucide-react'

const CHANNEL_ICONS = {
  email: { icon: Mail, color: 'bg-blue-50 text-blue-500' },
  website_chat: { icon: MessageSquare, color: 'bg-indigo-50 text-indigo-500' },
  whatsapp: { icon: Phone, color: 'bg-emerald-50 text-emerald-500' },
  instagram: { icon: Instagram, color: 'bg-pink-50 text-pink-500' },
  facebook: { icon: Facebook, color: 'bg-blue-100 text-blue-600' },
}

const CHANNEL_TITLES = {
  email: 'Email Integration',
  website_chat: 'Website Chat Widget',
  whatsapp: 'WhatsApp Business API',
  instagram: 'Instagram Direct',
  facebook: 'Facebook Messenger',
}

const APP_PLACEHOLDERS = {
  email: 'support@yourdomain.com',
  website_chat: 'chat.yourdomain.com',
  whatsapp: '+1 (555) 019-2831',
  instagram: '@yourbrand_official',
  facebook: 'facebook.com/yourbrand',
}

export default function ChannelIntegrations() {
  const queryClient = useQueryClient()
  const [selectedChannel, setSelectedChannel] = useState(null)
  const [isConnectModalOpen, setIsConnectModalOpen] = useState(false)
  const [connectError, setConnectError] = useState('')

  // Form states for New Integration
  const [connectForm, setConnectForm] = useState({
    channel_type: 'email',
    display_name: '',
    credentials_encrypted: '',
  })

  // Form states for Managing Channel
  const [manageForm, setManageForm] = useState({
    status: 'connected',
    display_name: '',
    weekly_volume: 0,
  })

  // Fetch channels from backend
  const { data: channels = [], isLoading } = useQuery({
    queryKey: ['admin-channels'],
    queryFn: async () => {
      const res = await adminApi.listChannels()
      return res.data
    }
  })

  // Create channel mutation
  const createChannelMutation = useMutation({
    mutationFn: (data) => adminApi.createChannel(data),
    onSuccess: () => {
      queryClient.invalidateQueries(['admin-channels'])
      setIsConnectModalOpen(false)
      setConnectForm({ channel_type: 'email', display_name: '', credentials_encrypted: '' })
      setConnectError('')
    },
    onError: (err) => {
      setConnectError(err.response?.data?.detail || 'Failed to connect integration.')
    }
  })

  // Update channel mutation
  const updateChannelMutation = useMutation({
    mutationFn: ({ id, data }) => adminApi.updateChannel(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries(['admin-channels'])
      setSelectedChannel(null)
    }
  })

  // Delete channel mutation
  const deleteChannelMutation = useMutation({
    mutationFn: (id) => adminApi.deleteChannel(id),
    onSuccess: () => {
      queryClient.invalidateQueries(['admin-channels'])
      setSelectedChannel(null)
    }
  })

  const openConnectModal = () => {
    setConnectForm({ channel_type: 'email', display_name: '', credentials_encrypted: '' })
    setConnectError('')
    setIsConnectModalOpen(true)
  }

  const openManageModal = (channel) => {
    setSelectedChannel(channel)
    setManageForm({
      status: channel.status,
      display_name: channel.display_name || '',
      weekly_volume: channel.weekly_volume || 0,
    })
  }

  const handleConnectSubmit = (e) => {
    e.preventDefault()
    if (!connectForm.display_name.trim()) {
      setConnectError('Please enter a display identifier or address.')
      return
    }
    createChannelMutation.mutate(connectForm)
  }

  const handleSaveChannel = (e) => {
    e.preventDefault()
    if (!selectedChannel) return
    updateChannelMutation.mutate({ id: selectedChannel.id, data: manageForm })
  }

  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8 text-[#1C1B2E]">
      {/* Page Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">Channel Integrations</h1>
          <p className="text-[#6C7089] text-sm mt-1">Connect the real applications and platforms your customers use.</p>
        </div>
        <button
          onClick={openConnectModal}
          className="flex items-center gap-2 bg-[#4F46E5] hover:bg-[#4338CA] text-white px-4 py-2.5 rounded-xl font-medium text-sm transition-colors shadow-sm"
        >
          <Plus size={16} /> + Connect App
        </button>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-16">
          <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div>
        </div>
      ) : channels.length === 0 ? (
        /* Empty State */
        <div className="bg-white rounded-2xl border border-[#E5E7F3] p-12 text-center max-w-lg mx-auto shadow-sm my-8">
          <div className="w-16 h-16 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <Link2 size={32} />
          </div>
          <h3 className="font-bold text-lg text-[#1C1B2E]">No Connected App Integrations</h3>
          <p className="text-sm text-[#6C7089] mt-2 mb-6 leading-relaxed">
            Integrate your support channels (Email, WhatsApp, Chat Widget, Social) to start receiving live tickets.
          </p>
          <button
            onClick={openConnectModal}
            className="inline-flex items-center gap-2 bg-[#4F46E5] hover:bg-[#4338CA] text-white px-5 py-2.5 rounded-xl font-bold text-sm transition-all shadow-sm"
          >
            <Plus size={18} /> Connect First App
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {channels.map((channel) => {
            const info = CHANNEL_ICONS[channel.channel_type] || { icon: MessageSquare, color: 'bg-gray-100 text-gray-500' }
            const IconComponent = info.icon
            const title = CHANNEL_TITLES[channel.channel_type] || channel.channel_type

            const isConnected = channel.status === 'connected'
            const isAttention = channel.status === 'needs_attention'

            return (
              <div
                key={channel.id}
                className="bg-white rounded-2xl border border-[#E5E7F3] p-6 shadow-sm flex flex-col justify-between hover:shadow-md transition-shadow"
              >
                <div>
                  {/* Top row with icon & status badge */}
                  <div className="flex justify-between items-start mb-4">
                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${info.color}`}>
                      <IconComponent size={20} />
                    </div>
                    <span className={`px-2.5 py-1 rounded-md text-xs font-bold ${
                      isConnected ? 'text-emerald-600 bg-emerald-50' :
                      isAttention ? 'text-orange-600 bg-orange-50' : 'text-gray-500 bg-gray-100'
                    }`}>
                      {isConnected ? 'Connected' : isAttention ? 'Needs attention' : 'Disconnected'}
                    </span>
                  </div>

                  {/* Channel Details */}
                  <h3 className="font-bold text-base text-[#1C1B2E]">{title}</h3>
                  <p className="text-xs text-[#9598B0] mt-0.5 font-medium">{channel.display_name || 'Not configured'}</p>
                  <p className="text-xs text-[#6C7089] mt-2 font-medium">{channel.weekly_volume || 0} / week messages</p>
                </div>

                {/* Bottom Action Button */}
                <div className="mt-6 pt-4 border-t border-[#F3F4F6]">
                  <button
                    onClick={() => openManageModal(channel)}
                    className="w-full py-2 rounded-xl text-xs font-bold bg-gray-50 hover:bg-gray-100 text-[#1C1B2E] border border-[#E5E7F3] transition-colors"
                  >
                    Manage Integration
                  </button>
                </div>
              </div>
            )
          })}

          {/* Add a Channel Card */}
          <div
            onClick={openConnectModal}
            className="bg-white/60 border-2 border-dashed border-[#E5E7F3] rounded-2xl p-6 flex flex-col items-center justify-center text-center hover:border-indigo-300 transition-colors cursor-pointer group min-h-[180px]"
          >
            <div className="w-12 h-12 rounded-2xl bg-indigo-50 text-indigo-500 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
              <Plus size={24} />
            </div>
            <h3 className="font-bold text-sm text-[#1C1B2E]">Connect Another App</h3>
            <p className="text-xs text-[#9598B0] mt-1 max-w-[200px]">Email, WhatsApp, Chat, Webhooks</p>
          </div>
        </div>
      )}

      {/* Connect New App Modal */}
      {isConnectModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden border border-[#E5E7F3]">
            <div className="flex justify-between items-center px-6 py-4 border-b border-[#E5E7F3]">
              <div className="flex items-center gap-2">
                <Plus size={18} className="text-indigo-600" />
                <h3 className="font-bold text-lg text-[#1C1B2E]">Connect Application</h3>
              </div>
              <button onClick={() => setIsConnectModalOpen(false)} className="text-gray-400 hover:text-gray-600 p-1 rounded-lg">
                <X size={18} />
              </button>
            </div>
            <form onSubmit={handleConnectSubmit} className="p-6 space-y-4">
              {connectError && (
                <div className="flex items-center gap-2 p-3 bg-red-50 text-red-600 text-xs rounded-xl font-medium">
                  <AlertCircle size={16} />
                  <span>{connectError}</span>
                </div>
              )}

              <div>
                <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Select Integration Type</label>
                <select
                  value={connectForm.channel_type}
                  onChange={(e) => setConnectForm({ ...connectForm, channel_type: e.target.value })}
                  className="w-full px-3.5 py-2.5 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500 font-medium"
                >
                  <option value="email">Email Integration</option>
                  <option value="website_chat">Website Chat Widget</option>
                  <option value="whatsapp">WhatsApp Business API</option>
                  <option value="instagram">Instagram Direct</option>
                  <option value="facebook">Facebook Messenger</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Identifier / Address / Handle</label>
                <input
                  type="text"
                  value={connectForm.display_name}
                  onChange={(e) => setConnectForm({ ...connectForm, display_name: e.target.value })}
                  placeholder={`e.g. ${APP_PLACEHOLDERS[connectForm.channel_type] || 'support@brand.com'}`}
                  className="w-full px-3.5 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">API Token / Webhook Secret (Optional)</label>
                <input
                  type="password"
                  value={connectForm.credentials_encrypted}
                  onChange={(e) => setConnectForm({ ...connectForm, credentials_encrypted: e.target.value })}
                  placeholder="Enter secret token or key..."
                  className="w-full px-3.5 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="flex justify-end gap-3 pt-4 border-t border-[#E5E7F3]">
                <button
                  type="button"
                  onClick={() => setIsConnectModalOpen(false)}
                  className="px-4 py-2 text-sm font-semibold text-gray-600 hover:bg-gray-100 rounded-xl"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createChannelMutation.isPending}
                  className="px-4 py-2 text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl disabled:opacity-50"
                >
                  {createChannelMutation.isPending ? 'Connecting...' : 'Connect App'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Channel Management Modal */}
      {selectedChannel && (
        <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden border border-[#E5E7F3]">
            <div className="flex justify-between items-center px-6 py-4 border-b border-[#E5E7F3]">
              <div className="flex items-center gap-2">
                <Settings2 size={18} className="text-indigo-600" />
                <h3 className="font-bold text-lg text-[#1C1B2E]">
                  Manage {CHANNEL_TITLES[selectedChannel.channel_type] || selectedChannel.channel_type}
                </h3>
              </div>
              <button onClick={() => setSelectedChannel(null)} className="text-gray-400 hover:text-gray-600 p-1 rounded-lg">
                <X size={18} />
              </button>
            </div>
            <form onSubmit={handleSaveChannel} className="p-6 space-y-4">
              <div>
                <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Display Identifier / Address</label>
                <input
                  type="text"
                  value={manageForm.display_name}
                  onChange={(e) => setManageForm({ ...manageForm, display_name: e.target.value })}
                  placeholder="e.g. support@brand.com"
                  className="w-full px-3.5 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Connection Status</label>
                <select
                  value={manageForm.status}
                  onChange={(e) => setManageForm({ ...manageForm, status: e.target.value })}
                  className="w-full px-3 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-sm focus:outline-none focus:border-indigo-500"
                >
                  <option value="connected">Connected</option>
                  <option value="needs_attention">Needs attention</option>
                  <option value="disconnected">Disconnected</option>
                </select>
              </div>

              <div className="flex justify-between items-center pt-4 border-t border-[#E5E7F3]">
                <button
                  type="button"
                  onClick={() => {
                    if (confirm(`Are you sure you want to disconnect this ${selectedChannel.channel_type} integration?`)) {
                      deleteChannelMutation.mutate(selectedChannel.id)
                    }
                  }}
                  className="flex items-center gap-1.5 px-3 py-2 text-xs font-bold text-red-600 hover:bg-red-50 rounded-xl transition-colors"
                >
                  <Trash2 size={14} /> Disconnect App
                </button>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setSelectedChannel(null)}
                    className="px-4 py-2 text-sm font-semibold text-gray-600 hover:bg-gray-100 rounded-xl"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={updateChannelMutation.isPending}
                    className="px-4 py-2 text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl disabled:opacity-50"
                  >
                    {updateChannelMutation.isPending ? 'Saving...' : 'Save Settings'}
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
