import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { adminApi } from '../../api/admin'
import { Mail, MessageSquare, Phone, Instagram, Facebook, Plus, X, AlertCircle, Settings2, Trash2, Key, Link2, ShieldCheck, CheckCircle2, ShieldAlert, RefreshCw, Check } from 'lucide-react'

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
    smtp_host: 'smtp.mailgun.org',
    smtp_port: '587',
    api_key: '',
    auto_reply_template: 'Thank you for reaching out! We received your ticket [TCK-REF] and our team will respond shortly.',
  })

  const [activeTab, setActiveTab] = useState('general')
  const [copySuccess, setCopySuccess] = useState(false)
  const [testResult, setTestResult] = useState(null)

  // WhatsApp Access Token Modal State
  const [isWaTokenModalOpen, setIsWaTokenModalOpen] = useState(false)
  const [waConfigForm, setWaConfigForm] = useState({
    whatsapp_access_token: '',
    whatsapp_phone_id: '',
    whatsapp_verify_token: '',
  })
  const [isTestingWaToken, setIsTestingWaToken] = useState(false)
  const [isSavingWaToken, setIsSavingWaToken] = useState(false)
  const [waTokenTestResult, setWaTokenTestResult] = useState(null)
  const [waTokenSaveResult, setWaTokenSaveResult] = useState(null)

  const openWhatsAppTokenModal = async () => {
    setIsWaTokenModalOpen(true)
    setWaTokenTestResult(null)
    setWaTokenSaveResult(null)
    try {
      const res = await adminApi.getWhatsAppConfig()
      setWaConfigForm({
        whatsapp_access_token: res.data.whatsapp_access_token || '',
        whatsapp_phone_id: res.data.whatsapp_phone_id || '',
        whatsapp_verify_token: res.data.whatsapp_verify_token || '',
      })
    } catch (e) {
      console.error('Failed to fetch WhatsApp config:', e)
    }
  }

  const handleSaveWaToken = async (e) => {
    e.preventDefault()
    setIsSavingWaToken(true)
    setWaTokenSaveResult(null)
    try {
      const res = await adminApi.updateWhatsAppConfig(waConfigForm)
      setWaTokenSaveResult({ status: 'success', message: res.data.message })
      queryClient.invalidateQueries(['admin-channels'])
    } catch (err) {
      setWaTokenSaveResult({ status: 'error', message: err.response?.data?.detail || 'Failed to update WhatsApp Access Token.' })
    } finally {
      setIsSavingWaToken(false)
    }
  }

  const handleTestWaToken = async () => {
    setIsTestingWaToken(true)
    setWaTokenTestResult(null)
    try {
      const res = await adminApi.testWhatsAppConfig(waConfigForm)
      setWaTokenTestResult(res.data)
    } catch (err) {
      setWaTokenTestResult({
        status: 'error',
        connected: false,
        message: err.response?.data?.detail || 'Token testing failed. Please verify credentials.'
      })
    } finally {
      setIsTestingWaToken(false)
    }
  }

  // Instagram Access Token Modal State
  const [isIgTokenModalOpen, setIsIgTokenModalOpen] = useState(false)
  const [igConfigForm, setIgConfigForm] = useState({
    instagram_access_token: '',
    instagram_account_id: '',
    instagram_verify_token: '',
  })
  const [isTestingIgToken, setIsTestingIgToken] = useState(false)
  const [isSavingIgToken, setIsSavingIgToken] = useState(false)
  const [igTokenTestResult, setIgTokenTestResult] = useState(null)
  const [igTokenSaveResult, setIgTokenSaveResult] = useState(null)

  const openInstagramTokenModal = async () => {
    setIsIgTokenModalOpen(true)
    setIgTokenTestResult(null)
    setIgTokenSaveResult(null)
    try {
      const res = await adminApi.getInstagramConfig()
      setIgConfigForm({
        instagram_access_token: res.data.instagram_access_token || '',
        instagram_account_id: res.data.instagram_account_id || '',
        instagram_verify_token: res.data.instagram_verify_token || '',
      })
    } catch (e) {
      console.error('Failed to fetch Instagram config:', e)
    }
  }

  const handleSaveIgToken = async (e) => {
    e.preventDefault()
    setIsSavingIgToken(true)
    setIgTokenSaveResult(null)
    try {
      const res = await adminApi.updateInstagramConfig(igConfigForm)
      setIgTokenSaveResult({ status: 'success', message: res.data.message })
      queryClient.invalidateQueries(['admin-channels'])
    } catch (err) {
      setIgTokenSaveResult({ status: 'error', message: err.response?.data?.detail || 'Failed to update Instagram Access Token.' })
    } finally {
      setIsSavingIgToken(false)
    }
  }

  const handleTestIgToken = async () => {
    setIsTestingIgToken(true)
    setIgTokenTestResult(null)
    try {
      const res = await adminApi.testInstagramConfig(igConfigForm)
      setIgTokenTestResult(res.data)
    } catch (err) {
      setIgTokenTestResult({
        status: 'error',
        connected: false,
        message: err.response?.data?.detail || 'Token testing failed. Please verify credentials.'
      })
    } finally {
      setIsTestingIgToken(false)
    }
  }

  // Facebook Access Token Modal State
  const [isFbTokenModalOpen, setIsFbTokenModalOpen] = useState(false)
  const [fbConfigForm, setFbConfigForm] = useState({
    facebook_page_access_token: '',
    facebook_access_token: '',
    facebook_page_id: '',
    facebook_verify_token: '',
  })
  const [isTestingFbToken, setIsTestingFbToken] = useState(false)
  const [isSavingFbToken, setIsSavingFbToken] = useState(false)
  const [fbTokenTestResult, setFbTokenTestResult] = useState(null)
  const [fbTokenSaveResult, setFbTokenSaveResult] = useState(null)

  const openFacebookTokenModal = async () => {
    setIsFbTokenModalOpen(true)
    setFbTokenTestResult(null)
    setFbTokenSaveResult(null)
    try {
      const res = await adminApi.getFacebookConfig()
      const token = res.data.facebook_page_access_token || res.data.facebook_access_token || ''
      setFbConfigForm({
        facebook_page_access_token: token,
        facebook_access_token: token,
        facebook_page_id: res.data.facebook_page_id || '',
        facebook_verify_token: res.data.facebook_verify_token || '',
      })
    } catch (e) {
      console.error('Failed to fetch Facebook config:', e)
    }
  }

  const handleSaveFbToken = async (e) => {
    e.preventDefault()
    setIsSavingFbToken(true)
    setFbTokenSaveResult(null)
    try {
      const tokenVal = (fbConfigForm.facebook_page_access_token || fbConfigForm.facebook_access_token || '').trim()
      const payload = {
        facebook_access_token: tokenVal,
        facebook_page_access_token: tokenVal,
        facebook_page_id: (fbConfigForm.facebook_page_id || '').trim(),
        facebook_verify_token: (fbConfigForm.facebook_verify_token || '').trim(),
      }
      const res = await adminApi.updateFacebookConfig(payload)
      setFbTokenSaveResult({ status: 'success', message: res.data.message })
      queryClient.invalidateQueries(['admin-channels'])
    } catch (err) {
      setFbTokenSaveResult({ status: 'error', message: err.response?.data?.detail || 'Failed to update Facebook Access Token.' })
    } finally {
      setIsSavingFbToken(false)
    }
  }

  const handleTestFbToken = async () => {
    setIsTestingFbToken(true)
    setFbTokenTestResult(null)
    try {
      const tokenVal = (fbConfigForm.facebook_page_access_token || fbConfigForm.facebook_access_token || '').trim()
      const payload = {
        facebook_access_token: tokenVal,
        facebook_page_access_token: tokenVal,
        facebook_page_id: (fbConfigForm.facebook_page_id || '').trim(),
        facebook_verify_token: (fbConfigForm.facebook_verify_token || '').trim(),
      }
      const res = await adminApi.testFacebookConfig(payload)
      setFbTokenTestResult(res.data)
    } catch (err) {
      setFbTokenTestResult({
        status: 'error',
        connected: false,
        message: err.response?.data?.detail || 'Token testing failed. Please verify credentials.'
      })
    } finally {
      setIsTestingFbToken(false)
    }
  }

  // Fetch channels from backend
  const { data: channels = [], isLoading } = useQuery({
    queryKey: ['admin-channels'],
    queryFn: async () => {
      const res = await adminApi.listChannels()
      return res.data
    }
  })

  const { data: emailLogs = [] } = useQuery({
    queryKey: ['admin-email-logs'],
    queryFn: async () => (await adminApi.getEmailLogs()).data,
    enabled: selectedChannel?.channel_type === 'email' && activeTab === 'logs'
  })

  const { data: emailTemplates = [] } = useQuery({
    queryKey: ['admin-email-templates'],
    queryFn: async () => (await adminApi.getEmailTemplates()).data,
    enabled: selectedChannel?.channel_type === 'email' && activeTab === 'templates'
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

  // Test Email mutation
  const testEmailMutation = useMutation({
    mutationFn: () => adminApi.testEmailConnection(),
    onSuccess: (res) => {
      queryClient.invalidateQueries(['admin-channels'])
      queryClient.invalidateQueries(['tickets'])
      setTestResult(res.data)
      setTimeout(() => setTestResult(null), 6000)
    },
    onError: (err) => {
      setTestResult({ status: 'error', message: err.response?.data?.detail || 'Test connection failed.' })
    }
  })

  const openConnectModal = () => {
    setConnectForm({ channel_type: 'email', display_name: '', credentials_encrypted: '' })
    setConnectError('')
    setIsConnectModalOpen(true)
  }

  const openManageModal = (channel) => {
    setSelectedChannel(channel)
    setActiveTab('general')
    setManageForm({
      status: channel.status,
      display_name: channel.display_name || '',
      weekly_volume: channel.weekly_volume || 0,
      smtp_host: 'smtp.mailgun.org',
      smtp_port: '587',
      api_key: '',
      auto_reply_template: 'Thank you for reaching out! We received your ticket and our team will respond shortly.',
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

  const copyWebhookUrl = () => {
    const webhookUrl = `${window.location.origin}/api/v1/webhooks/email`
    navigator.clipboard.writeText(webhookUrl)
    setCopySuccess(true)
    setTimeout(() => setCopySuccess(false), 3000)
  }

  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8 text-[#1C1B2E]">
      {/* Page Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">Channel Integrations</h1>
          <p className="text-[#6C7089] text-sm mt-1">Connect the real applications and platforms your customers use.</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => testEmailMutation.mutate()}
            disabled={testEmailMutation.isPending}
            className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2.5 rounded-xl font-medium text-sm transition-colors shadow-sm disabled:opacity-50"
          >
            <Key size={16} />
            {testEmailMutation.isPending ? 'Testing...' : 'Test Email Connection'}
          </button>
          <button
            onClick={openConnectModal}
            className="flex items-center gap-2 bg-[#4F46E5] hover:bg-[#4338CA] text-white px-4 py-2.5 rounded-xl font-medium text-sm transition-colors shadow-sm"
          >
            <Plus size={16} /> + Connect App
          </button>
        </div>
      </div>

      {testResult && (
        <div className={`mb-6 p-4 rounded-2xl border flex items-center justify-between text-sm font-semibold animate-fadeIn ${
          testResult.status === 'error' ? 'bg-red-50 text-red-700 border-red-200' : 'bg-emerald-50 text-emerald-700 border-emerald-200'
        }`}>
          <div className="flex items-center gap-2">
            <AlertCircle size={18} />
            <span>{testResult.message} {testResult.ticket_ref ? `(Ticket Ref: ${testResult.ticket_ref})` : ''}</span>
          </div>
          <button onClick={() => setTestResult(null)} className="text-xs hover:underline">Dismiss</button>
        </div>
      )}

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

                {/* Bottom Action Buttons */}
                <div className="mt-6 pt-4 border-t border-[#F3F4F6] flex gap-2">
                  <button
                    onClick={() => openManageModal(channel)}
                    className="flex-1 py-2 rounded-xl text-xs font-bold bg-gray-50 hover:bg-gray-100 text-[#1C1B2E] border border-[#E5E7F3] transition-colors"
                  >
                    Manage Integration
                  </button>
                  {channel.channel_type === 'email' && (
                    <button
                      onClick={() => testEmailMutation.mutate()}
                      title="Test Email Connection"
                      className="px-3 py-2 rounded-xl text-xs font-bold bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 transition-colors flex items-center gap-1"
                    >
                      <Key size={14} /> Test
                    </button>
                  )}
                  {channel.channel_type === 'whatsapp' && (
                    <button
                      onClick={() => openWhatsAppTokenModal()}
                      title="Update & Test WhatsApp Access Token"
                      className="px-3 py-2 rounded-xl text-xs font-bold bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 transition-colors flex items-center gap-1"
                    >
                      <Key size={14} /> Token & Test
                    </button>
                  )}
                  {channel.channel_type === 'instagram' && (
                    <button
                      onClick={() => openInstagramTokenModal()}
                      title="Update & Test Instagram Access Token"
                      className="px-3 py-2 rounded-xl text-xs font-bold bg-pink-50 hover:bg-pink-100 text-pink-700 border border-pink-200 transition-colors flex items-center gap-1"
                    >
                      <Key size={14} /> Token & Test
                    </button>
                  )}
                  {channel.channel_type === 'facebook' && (
                    <button
                      onClick={() => openFacebookTokenModal()}
                      title="Update & Test Facebook Page Access Token"
                      className="px-3 py-2 rounded-xl text-xs font-bold bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 transition-colors flex items-center gap-1"
                    >
                      <Key size={14} /> Token & Test
                    </button>
                  )}
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
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-lg overflow-hidden border border-[#E5E7F3]">
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

            {/* Tabs for Email Integration */}
            {selectedChannel.channel_type === 'email' && (
              <div className="flex border-b border-[#E5E7F3] bg-gray-50 px-6 gap-6 text-xs font-bold">
                <button
                  type="button"
                  onClick={() => setActiveTab('general')}
                  className={`py-3 border-b-2 transition-colors ${
                    activeTab === 'general' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-[#6C7089]'
                  }`}
                >
                  General
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab('smtp')}
                  className={`py-3 border-b-2 transition-colors ${
                    activeTab === 'smtp' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-[#6C7089]'
                  }`}
                >
                  SMTP / Mailgun Config
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab('webhook')}
                  className={`py-3 border-b-2 transition-colors ${
                    activeTab === 'webhook' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-[#6C7089]'
                  }`}
                >
                  Inbound Webhook
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab('logs')}
                  className={`py-3 border-b-2 transition-colors ${
                    activeTab === 'logs' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-[#6C7089]'
                  }`}
                >
                  Delivery Logs
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab('templates')}
                  className={`py-3 border-b-2 transition-colors ${
                    activeTab === 'templates' ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-[#6C7089]'
                  }`}
                >
                  Templates
                </button>
              </div>
            )}

            <form onSubmit={handleSaveChannel} className="p-6 space-y-4">
              {activeTab === 'general' && (
                <>
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
                </>
              )}

              {activeTab === 'smtp' && (
                <>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">SMTP Host</label>
                      <input
                        type="text"
                        value={manageForm.smtp_host}
                        onChange={(e) => setManageForm({ ...manageForm, smtp_host: e.target.value })}
                        className="w-full px-3 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-xs"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">SMTP Port</label>
                      <input
                        type="text"
                        value={manageForm.smtp_port}
                        onChange={(e) => setManageForm({ ...manageForm, smtp_port: e.target.value })}
                        className="w-full px-3 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-xs"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Mailgun / Postmark API Key</label>
                    <input
                      type="password"
                      value={manageForm.api_key}
                      onChange={(e) => setManageForm({ ...manageForm, api_key: e.target.value })}
                      placeholder="key-xxxxxxxxxxxxxxxx"
                      className="w-full px-3 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-xs"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-[#6C7089] uppercase mb-1">Auto-Acknowledgement Template</label>
                    <textarea
                      rows={3}
                      value={manageForm.auto_reply_template}
                      onChange={(e) => setManageForm({ ...manageForm, auto_reply_template: e.target.value })}
                      className="w-full px-3 py-2 bg-[#F9FAFB] border border-[#E5E7F3] rounded-xl text-xs focus:outline-none focus:border-indigo-500"
                    />
                  </div>
                </>
              )}

              {activeTab === 'webhook' && (
                <div className="space-y-3">
                  <label className="block text-xs font-bold text-[#6C7089] uppercase">Inbound Webhook URL</label>
                  <p className="text-xs text-[#9598B0]">
                    Configure this endpoint in your Mailgun, Postmark, or SendGrid dashboard to receive real emails directly into SupportHub.
                  </p>
                  <div className="flex items-center gap-2 p-3 bg-gray-50 border border-[#E5E7F3] rounded-xl font-mono text-xs text-indigo-600 break-all">
                    <span>{`${window.location.origin}/api/v1/webhooks/email`}</span>
                  </div>
                  <button
                    type="button"
                    onClick={copyWebhookUrl}
                    className="w-full py-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-bold text-xs rounded-xl border border-indigo-200 transition-colors flex items-center justify-center gap-2"
                  >
                    <Link2 size={14} />
                    {copySuccess ? 'Copied to Clipboard!' : 'Copy Inbound Webhook URL'}
                  </button>
                </div>
              )}

              {activeTab === 'logs' && (
                <div className="space-y-3 max-h-60 overflow-y-auto">
                  <h4 className="text-xs font-bold text-[#6C7089] uppercase">Outbound Email Audit Trail</h4>
                  {emailLogs.length === 0 ? (
                    <p className="text-xs text-gray-400 italic">No delivery logs recorded yet.</p>
                  ) : (
                    emailLogs.map((log, i) => (
                      <div key={log.id || i} className="p-3 bg-gray-50 rounded-xl border border-gray-100 text-xs flex justify-between items-center">
                        <div>
                          <div className="font-bold text-[#1C1B2E]">{log.subject}</div>
                          <div className="text-[11px] text-[#6C7089]">{log.recipient_email}</div>
                        </div>
                        <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase ${
                          log.status === 'delivered' ? 'bg-emerald-100 text-emerald-700' : log.status === 'sent' ? 'bg-blue-100 text-blue-700' : 'bg-red-100 text-red-700'
                        }`}>
                          {log.status}
                        </span>
                      </div>
                    ))
                  )}
                </div>
              )}

              {activeTab === 'templates' && (
                <div className="space-y-3 max-h-64 overflow-y-auto">
                  <h4 className="text-xs font-bold text-[#6C7089] uppercase mb-1">System Email Templates</h4>
                  {emailTemplates.map(tmpl => (
                    <div key={tmpl.id || tmpl.name} className="p-3 bg-[#F8FAFC] border border-[#E5E7F3] rounded-xl text-xs space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="font-bold font-mono text-indigo-600 uppercase">{tmpl.name}</span>
                        <span className="text-[10px] text-gray-400">Dynamic Template</span>
                      </div>
                      <div className="text-[11px] text-[#6C7089]">
                        <strong>Subject Pattern:</strong> <code className="bg-white px-1 border rounded">{tmpl.subject_pattern}</code>
                      </div>
                      <div className="text-[11px] text-gray-500 font-mono bg-white p-2 rounded border max-h-20 overflow-hidden line-clamp-2">
                        {tmpl.body_html}
                      </div>
                    </div>
                  ))}
                </div>
              )}

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

      {/* WHATSAPP ACCESS TOKEN & CREDENTIALS MANAGEMENT MODAL */}
      {isWaTokenModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden border border-[#E5E7F3] animate-fadeIn">
            <div className="px-6 py-4 bg-emerald-600 text-white flex justify-between items-center">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-xl bg-white/20 flex items-center justify-center">
                  <Key size={18} />
                </div>
                <div>
                  <h3 className="font-bold text-base font-['Plus_Jakarta_Sans']">Meta WhatsApp Access Token</h3>
                  <p className="text-[11px] text-emerald-100 font-medium">Auto-updates backend .env file & database</p>
                </div>
              </div>
              <button 
                onClick={() => setIsWaTokenModalOpen(false)}
                className="text-emerald-100 hover:text-white p-1 rounded-lg hover:bg-white/10 transition-colors"
              >
                <X size={20} />
              </button>
            </div>

            <form onSubmit={handleSaveWaToken} className="p-6 space-y-4 text-xs">
              {waTokenSaveResult && (
                <div className={`p-3.5 rounded-xl border flex items-start gap-2.5 font-semibold text-xs ${
                  waTokenSaveResult.status === 'success' 
                    ? 'bg-emerald-50 text-emerald-800 border-emerald-200' 
                    : 'bg-rose-50 text-rose-800 border-rose-200'
                }`}>
                  {waTokenSaveResult.status === 'success' ? <CheckCircle2 size={18} className="text-emerald-600 shrink-0 mt-0.5" /> : <AlertCircle size={18} className="text-rose-600 shrink-0 mt-0.5" />}
                  <div>
                    <div>{waTokenSaveResult.message}</div>
                    {waTokenSaveResult.status === 'success' && (
                      <div className="text-[10px] text-emerald-700 font-normal mt-0.5">
                        Runtime environment & backend .env file updated. Changes applied immediately.
                      </div>
                    )}
                  </div>
                </div>
              )}

              {waTokenTestResult && (
                <div className={`p-3.5 rounded-xl border flex items-start gap-2.5 font-semibold text-xs ${
                  waTokenTestResult.connected 
                    ? 'bg-emerald-50 text-emerald-900 border-emerald-300' 
                    : 'bg-rose-50 text-rose-900 border-rose-300'
                }`}>
                  {waTokenTestResult.connected ? <CheckCircle2 size={18} className="text-emerald-600 shrink-0 mt-0.5" /> : <ShieldAlert size={18} className="text-rose-600 shrink-0 mt-0.5" />}
                  <div className="space-y-1">
                    <div className="font-bold">{waTokenTestResult.message}</div>
                    {waTokenTestResult.details && (
                      <div className="text-[11px] font-mono text-emerald-800 bg-white/70 p-2 rounded-lg border border-emerald-200 space-y-0.5">
                        <div>Account ID: {waTokenTestResult.details.id}</div>
                        <div>Display Phone: {waTokenTestResult.details.display_phone_number}</div>
                        <div>Verified Name: {waTokenTestResult.details.verified_name}</div>
                        <div>Quality Rating: <span className="font-bold text-emerald-700">{waTokenTestResult.details.quality_rating}</span></div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              <div>
                <label className="block font-bold text-[#6C7089] uppercase tracking-wider text-[10px] mb-1">
                  WhatsApp Access Token
                </label>
                <textarea
                  rows={3}
                  value={waConfigForm.whatsapp_access_token}
                  onChange={e => setWaConfigForm({ ...waConfigForm, whatsapp_access_token: e.target.value })}
                  placeholder="EAAPcP..."
                  className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl p-3 font-mono text-xs outline-none focus:border-emerald-500 focus:bg-white transition-all"
                  required
                />
                <p className="text-[10px] text-[#9598B0] mt-1">
                  Get token from Meta Developer Portal &gt; WhatsApp &gt; API Setup.
                </p>
              </div>

              <div>
                <label className="block font-bold text-[#6C7089] uppercase tracking-wider text-[10px] mb-1">
                  WhatsApp Phone Number ID
                </label>
                <input
                  type="text"
                  value={waConfigForm.whatsapp_phone_id}
                  onChange={e => setWaConfigForm({ ...waConfigForm, whatsapp_phone_id: e.target.value })}
                  placeholder="e.g. 1296854793505632"
                  className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl px-3 py-2 font-mono text-xs outline-none focus:border-emerald-500 focus:bg-white transition-all"
                  required
                />
              </div>

              <div>
                <label className="block font-bold text-[#6C7089] uppercase tracking-wider text-[10px] mb-1">
                  Webhook Verify Token (Optional)
                </label>
                <input
                  type="text"
                  value={waConfigForm.whatsapp_verify_token}
                  onChange={e => setWaConfigForm({ ...waConfigForm, whatsapp_verify_token: e.target.value })}
                  placeholder="your_webhook_verify_token"
                  className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl px-3 py-2 font-mono text-xs outline-none focus:border-emerald-500 focus:bg-white transition-all"
                />
              </div>

              <div className="flex justify-between items-center pt-4 border-t border-[#E5E7F3] gap-2">
                <button
                  type="button"
                  onClick={handleTestWaToken}
                  disabled={isTestingWaToken || !waConfigForm.whatsapp_access_token.trim()}
                  className="px-4 py-2 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 font-bold rounded-xl border border-emerald-300 transition-all flex items-center gap-1.5 disabled:opacity-50"
                >
                  {isTestingWaToken ? <RefreshCw size={14} className="animate-spin" /> : <ShieldCheck size={14} />}
                  <span>{isTestingWaToken ? 'Testing Meta Token...' : 'Test Connection'}</span>
                </button>

                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setIsWaTokenModalOpen(false)}
                    className="px-4 py-2 text-xs font-semibold text-gray-600 hover:bg-gray-100 rounded-xl"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={isSavingWaToken || !waConfigForm.whatsapp_access_token.trim()}
                    className="px-5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl transition-all shadow-xs flex items-center gap-1.5 disabled:opacity-50"
                  >
                    {isSavingWaToken ? <RefreshCw size={14} className="animate-spin" /> : <Check size={14} />}
                    <span>{isSavingWaToken ? 'Updating .env...' : 'Save & Update .env'}</span>
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      )}
      {/* Instagram Access Token & Credentials Modal */}
      {isIgTokenModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden border border-[#E5E7F3] animate-fadeIn">
            {/* Modal Header */}
            <div className="px-6 py-4 bg-gradient-to-r from-rose-500 via-pink-600 to-purple-600 text-white flex justify-between items-center">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-xl bg-white/20 flex items-center justify-center">
                  <Instagram size={18} />
                </div>
                <div>
                  <h3 className="font-bold text-base font-['Plus_Jakarta_Sans']">Meta Instagram Access Token</h3>
                  <p className="text-[11px] text-pink-100 font-medium">Updates .env file & database automatically</p>
                </div>
              </div>
              <button 
                onClick={() => setIsIgTokenModalOpen(false)}
                className="text-pink-100 hover:text-white p-1 rounded-lg hover:bg-white/10 transition-colors"
              >
                <X size={20} />
              </button>
            </div>

            <form onSubmit={handleSaveIgToken} className="p-6 space-y-4 text-xs">
              {/* Save Alert Status */}
              {igTokenSaveResult && (
                <div className={`p-3.5 rounded-xl border flex items-start gap-2.5 font-semibold text-xs ${
                  igTokenSaveResult.status === 'success' 
                    ? 'bg-emerald-50 text-emerald-800 border-emerald-200' 
                    : 'bg-rose-50 text-rose-800 border-rose-200'
                }`}>
                  {igTokenSaveResult.status === 'success' ? <CheckCircle2 size={18} className="text-emerald-600 shrink-0 mt-0.5" /> : <AlertCircle size={18} className="text-rose-600 shrink-0 mt-0.5" />}
                  <div>
                    <div>{igTokenSaveResult.message}</div>
                    {igTokenSaveResult.status === 'success' && (
                      <div className="text-[10px] text-emerald-700 font-normal mt-0.5">
                        Runtime environment & backend .env file updated. Changes applied immediately.
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Test Connection Alert Status */}
              {igTokenTestResult && (
                <div className={`p-3.5 rounded-xl border flex items-start gap-2.5 font-semibold text-xs ${
                  igTokenTestResult.connected 
                    ? 'bg-pink-50 text-pink-900 border-pink-300' 
                    : 'bg-rose-50 text-rose-900 border-rose-300'
                }`}>
                  {igTokenTestResult.connected ? <CheckCircle2 size={18} className="text-pink-600 shrink-0 mt-0.5" /> : <ShieldAlert size={18} className="text-rose-600 shrink-0 mt-0.5" />}
                  <div className="space-y-1">
                    <div className="font-bold">{igTokenTestResult.message}</div>
                    {igTokenTestResult.details && (
                      <div className="text-[11px] font-mono text-pink-800 bg-white/70 p-2 rounded-lg border border-pink-200 space-y-0.5">
                        <div>Account ID: {igTokenTestResult.details.id}</div>
                        <div>Username: @{igTokenTestResult.details.username}</div>
                        <div>Account Type: <span className="font-bold text-pink-700">{igTokenTestResult.details.account_type}</span></div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              <div>
                <label className="block font-bold text-[#6C7089] uppercase tracking-wider text-[10px] mb-1">
                  Instagram Access Token
                </label>
                <textarea
                  rows={3}
                  value={igConfigForm.instagram_access_token}
                  onChange={e => setIgConfigForm({ ...igConfigForm, instagram_access_token: e.target.value })}
                  placeholder="EAAPcP..."
                  className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl p-3 font-mono text-xs outline-none focus:border-pink-500 focus:bg-white transition-all"
                  required
                />
                <p className="text-[10px] text-[#9598B0] mt-1">
                  From Meta Developer Portal &gt; Instagram API &gt; User Token.
                </p>
              </div>

              <div>
                <label className="block font-bold text-[#6C7089] uppercase tracking-wider text-[10px] mb-1">
                  Instagram Professional Account ID
                </label>
                <input
                  type="text"
                  value={igConfigForm.instagram_account_id}
                  onChange={e => setIgConfigForm({ ...igConfigForm, instagram_account_id: e.target.value })}
                  placeholder="e.g. 17841400000000000"
                  className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl px-3 py-2 font-mono text-xs outline-none focus:border-pink-500 focus:bg-white transition-all"
                />
              </div>

              <div>
                <label className="block font-bold text-[#6C7089] uppercase tracking-wider text-[10px] mb-1">
                  Webhook Verify Token (Optional)
                </label>
                <input
                  type="text"
                  value={igConfigForm.instagram_verify_token}
                  onChange={e => setIgConfigForm({ ...igConfigForm, instagram_verify_token: e.target.value })}
                  placeholder="your_webhook_verify_token"
                  className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl px-3 py-2 font-mono text-xs outline-none focus:border-pink-500 focus:bg-white transition-all"
                />
              </div>

              <div className="flex justify-between items-center pt-4 border-t border-[#E5E7F3] gap-2">
                <button
                  type="button"
                  onClick={handleTestIgToken}
                  disabled={isTestingIgToken || !igConfigForm.instagram_access_token.trim()}
                  className="px-4 py-2 bg-pink-50 hover:bg-pink-100 text-pink-800 font-bold rounded-xl border border-pink-300 transition-all flex items-center gap-1.5 disabled:opacity-50"
                >
                  {isTestingIgToken ? <RefreshCw size={14} className="animate-spin" /> : <ShieldCheck size={14} />}
                  <span>{isTestingIgToken ? 'Testing Meta Token...' : 'Test Connection'}</span>
                </button>

                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setIsIgTokenModalOpen(false)}
                    className="px-4 py-2 text-xs font-semibold text-gray-600 hover:bg-gray-100 rounded-xl"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={isSavingIgToken || !igConfigForm.instagram_access_token.trim()}
                    className="px-5 py-2 bg-gradient-to-r from-rose-500 to-purple-600 hover:opacity-90 text-white font-bold rounded-xl transition-all shadow-xs flex items-center gap-1.5 disabled:opacity-50"
                  >
                    {isSavingIgToken ? <RefreshCw size={14} className="animate-spin" /> : <Check size={14} />}
                    <span>{isSavingIgToken ? 'Updating .env...' : 'Save & Update .env'}</span>
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      )}
      {/* Facebook Access Token Modal */}
      {isFbTokenModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-lg overflow-hidden border border-[#E5E7F3] animate-fadeIn">
            {/* Header */}
            <div className="px-6 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white flex justify-between items-center">
              <div className="flex items-center gap-2">
                <Facebook size={20} />
                <div>
                  <h3 className="font-bold text-base">Meta Facebook Page Access Token</h3>
                  <p className="text-[11px] text-blue-100">Updates .env file & database settings immediately</p>
                </div>
              </div>
              <button
                onClick={() => setIsFbTokenModalOpen(false)}
                className="text-blue-100 hover:text-white p-1 rounded-lg hover:bg-white/10"
              >
                <X size={20} />
              </button>
            </div>

            {/* Form Body */}
            <form onSubmit={handleSaveFbToken} className="p-6 space-y-4 text-xs">
              {/* Save Alert Status */}
              {fbTokenSaveResult && (
                <div className={`p-3.5 rounded-xl border flex items-start gap-2.5 font-semibold text-xs ${fbTokenSaveResult.status === 'success'
                    ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
                    : 'bg-rose-50 text-rose-800 border-rose-200'
                  }`}>
                  {fbTokenSaveResult.status === 'success' ? <CheckCircle2 size={18} className="text-emerald-600 shrink-0 mt-0.5" /> : <AlertCircle size={18} className="text-rose-600 shrink-0 mt-0.5" />}
                  <div>
                    <div>{fbTokenSaveResult.message}</div>
                    {fbTokenSaveResult.status === 'success' && (
                      <div className="text-[10px] text-emerald-700 font-normal mt-0.5">
                        Runtime environment & backend .env file updated. Changes applied immediately.
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Test Connection Alert Status */}
              {fbTokenTestResult && (
                <div className={`p-3.5 rounded-xl border flex items-start gap-2.5 font-semibold text-xs ${fbTokenTestResult.connected
                    ? 'bg-blue-50 text-blue-900 border-blue-300'
                    : 'bg-rose-50 text-rose-900 border-rose-300'
                  }`}>
                  {fbTokenTestResult.connected ? <CheckCircle2 size={18} className="text-blue-600 shrink-0 mt-0.5" /> : <ShieldAlert size={18} className="text-rose-600 shrink-0 mt-0.5" />}
                  <div className="space-y-1">
                    <div className="font-bold">{fbTokenTestResult.message}</div>
                    {fbTokenTestResult.details && (
                      <div className="text-[11px] font-mono text-blue-800 bg-white/70 p-2 rounded-lg border border-blue-200 space-y-0.5">
                        <div>App / Page ID: {fbTokenTestResult.details.id}</div>
                        <div>Name: {fbTokenTestResult.details.name}</div>
                        {fbTokenTestResult.details.scopes && (
                          <div>Permissions: <span className="font-bold text-blue-700">{fbTokenTestResult.details.scopes.join(', ')}</span></div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              )}

              <div>
                <label className="block font-bold text-[#6C7089] uppercase tracking-wider text-[10px] mb-1">
                  Facebook Page Access Token
                </label>
                <textarea
                  rows={3}
                  value={fbConfigForm.facebook_page_access_token || fbConfigForm.facebook_access_token || ''}
                  onChange={e => setFbConfigForm({
                    ...fbConfigForm,
                    facebook_page_access_token: e.target.value,
                    facebook_access_token: e.target.value
                  })}
                  placeholder="EAAPcP..."
                  className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl p-3 font-mono text-xs outline-none focus:border-blue-500 focus:bg-white transition-all"
                  required
                />
                <p className="text-[10px] text-[#9598B0] mt-1">
                  From Meta Developer Portal &gt; Facebook Messenger API &gt; Page Access Token.
                </p>
              </div>

              <div>
                <label className="block font-bold text-[#6C7089] uppercase tracking-wider text-[10px] mb-1">
                  Facebook Page ID (Optional)
                </label>
                <input
                  type="text"
                  value={fbConfigForm.facebook_page_id || ''}
                  onChange={e => setFbConfigForm({ ...fbConfigForm, facebook_page_id: e.target.value })}
                  placeholder="e.g. 17841400000000000"
                  className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl px-3 py-2 font-mono text-xs outline-none focus:border-blue-500 focus:bg-white transition-all"
                />
              </div>

              <div>
                <label className="block font-bold text-[#6C7089] uppercase tracking-wider text-[10px] mb-1">
                  Webhook Verify Token (Optional)
                </label>
                <input
                  type="text"
                  value={fbConfigForm.facebook_verify_token || ''}
                  onChange={e => setFbConfigForm({ ...fbConfigForm, facebook_verify_token: e.target.value })}
                  placeholder="your_webhook_verify_token"
                  className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl px-3 py-2 font-mono text-xs outline-none focus:border-blue-500 focus:bg-white transition-all"
                />
              </div>

              <div className="flex justify-between items-center pt-4 border-t border-[#E5E7F3] gap-2">
                <button
                  type="button"
                  onClick={handleTestFbToken}
                  disabled={isTestingFbToken || !(fbConfigForm.facebook_page_access_token || fbConfigForm.facebook_access_token || '').trim()}
                  className="px-4 py-2 bg-blue-50 hover:bg-blue-100 text-blue-800 font-bold rounded-xl border border-blue-300 transition-all flex items-center gap-1.5 disabled:opacity-50"
                >
                  {isTestingFbToken ? <RefreshCw size={14} className="animate-spin" /> : <ShieldCheck size={14} />}
                  <span>{isTestingFbToken ? 'Testing Meta Token...' : 'Test Connection'}</span>
                </button>

                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setIsFbTokenModalOpen(false)}
                    className="px-4 py-2 text-xs font-semibold text-gray-600 hover:bg-gray-100 rounded-xl"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={isSavingFbToken || !(fbConfigForm.facebook_page_access_token || fbConfigForm.facebook_access_token || '').trim()}
                    className="px-5 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:opacity-90 text-white font-bold rounded-xl transition-all shadow-xs flex items-center gap-1.5 disabled:opacity-50"
                  >
                    {isSavingFbToken ? <RefreshCw size={14} className="animate-spin" /> : <Check size={14} />}
                    <span>{isSavingFbToken ? 'Updating .env...' : 'Save & Update .env'}</span>
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
