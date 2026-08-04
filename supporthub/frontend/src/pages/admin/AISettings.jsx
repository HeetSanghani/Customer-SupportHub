import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { adminApi } from '../../api/admin'
import { knowledgeApi } from '../../api/knowledge'
import { ticketsApi } from '../../api/tickets'
import { Bot, BookOpen, MessageSquare, FileText, CheckCircle2, Save } from 'lucide-react'

export default function AISettings() {
  const queryClient = useQueryClient()
  const [saveSuccess, setSaveSuccess] = useState(false)

  // Local state for form controls
  const [settings, setSettings] = useState({
    enable_ai_assistant: true,
    auto_resolve: true,
    ai_reply_suggestions: true,
    ai_summaries: true,
    sentiment_detection: true,
    confidence_threshold: 85,
  })

  // Fetch AI settings
  const { data: fetchedSettings, isLoading: isLoadingSettings } = useQuery({
    queryKey: ['admin-ai-settings'],
    queryFn: async () => {
      const res = await adminApi.getAiSettings()
      return res.data
    }
  })

  // Fetch real KB Articles count
  const { data: articles = [] } = useQuery({
    queryKey: ['kb-articles'],
    queryFn: async () => {
      const res = await knowledgeApi.list()
      return res.data
    }
  })

  // Fetch real Tickets count
  const { data: tickets = [] } = useQuery({
    queryKey: ['tickets', 'all'],
    queryFn: async () => {
      const res = await ticketsApi.list()
      return res.data
    }
  })

  useEffect(() => {
    if (fetchedSettings) {
      setSettings(fetchedSettings)
    }
  }, [fetchedSettings])

  // Save Settings Mutation
  const saveMutation = useMutation({
    mutationFn: (data) => adminApi.updateAiSettings(data),
    onSuccess: () => {
      queryClient.invalidateQueries(['admin-ai-settings'])
      setSaveSuccess(true)
      setTimeout(() => setSaveSuccess(false), 3000)
    }
  })

  const handleToggle = (key) => {
    setSettings(prev => ({ ...prev, [key]: !prev[key] }))
  }

  const handleSliderChange = (e) => {
    setSettings(prev => ({ ...prev, confidence_threshold: parseInt(e.target.value) || 0 }))
  }

  const handleSave = (e) => {
    e.preventDefault()
    saveMutation.mutate(settings)
  }

  const resolvedTicketsCount = tickets.filter(t => t.status === 'resolved' || t.status === 'closed').length || tickets.length

  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8 text-[#1C1B2E]">
      {/* Top Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">AI Settings</h1>
          <p className="text-[#6C7089] text-sm mt-1">Control how the AI Assistant responds, escalates and learns.</p>
        </div>
        <button
          onClick={handleSave}
          disabled={saveMutation.isPending}
          className="flex items-center gap-2 bg-[#4F46E5] hover:bg-[#4338CA] text-white px-5 py-2.5 rounded-xl font-medium text-sm transition-colors shadow-sm disabled:opacity-50"
        >
          <Save size={16} />
          {saveMutation.isPending ? 'Saving...' : 'Save Settings'}
        </button>
      </div>

      {saveSuccess && (
        <div className="mb-6 flex items-center gap-2 bg-emerald-50 text-emerald-700 p-4 rounded-2xl border border-emerald-200 text-sm font-semibold animate-fadeIn">
          <CheckCircle2 size={18} />
          <span>AI Settings updated successfully!</span>
        </div>
      )}

      {isLoadingSettings ? (
        <div className="flex justify-center py-16">
          <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column: Behavior Toggles & Threshold */}
          <div className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm lg:col-span-2 space-y-6">
            <h2 className="text-base font-bold text-[#1C1B2E]">Behavior</h2>

            {/* Toggle 1: Enable AI Assistant */}
            <div className="flex items-center justify-between py-2 border-b border-[#F3F4F6]">
              <div>
                <div className="font-bold text-sm text-[#1C1B2E]">Enable AI Assistant</div>
                <div className="text-xs text-[#9598B0] mt-0.5">Let customers get instant AI answers</div>
              </div>
              <button
                type="button"
                onClick={() => handleToggle('enable_ai_assistant')}
                className={`w-12 h-6 flex items-center rounded-full p-1 transition-colors ${
                  settings.enable_ai_assistant ? 'bg-indigo-600' : 'bg-gray-300'
                }`}
              >
                <div
                  className={`bg-white w-4 h-4 rounded-full shadow-md transform transition-transform ${
                    settings.enable_ai_assistant ? 'translate-x-6' : 'translate-x-0'
                  }`}
                />
              </button>
            </div>

            {/* Toggle 2: Auto-resolve high-confidence answers */}
            <div className="flex items-center justify-between py-2 border-b border-[#F3F4F6]">
              <div>
                <div className="font-bold text-sm text-[#1C1B2E]">Auto-resolve high-confidence answers</div>
                <div className="text-xs text-[#9598B0] mt-0.5">Close tickets automatically above the confidence threshold</div>
              </div>
              <button
                type="button"
                onClick={() => handleToggle('auto_resolve')}
                className={`w-12 h-6 flex items-center rounded-full p-1 transition-colors ${
                  settings.auto_resolve ? 'bg-indigo-600' : 'bg-gray-300'
                }`}
              >
                <div
                  className={`bg-white w-4 h-4 rounded-full shadow-md transform transition-transform ${
                    settings.auto_resolve ? 'translate-x-6' : 'translate-x-0'
                  }`}
                />
              </button>
            </div>

            {/* Toggle 3: AI reply suggestions */}
            <div className="flex items-center justify-between py-2 border-b border-[#F3F4F6]">
              <div>
                <div className="font-bold text-sm text-[#1C1B2E]">AI reply suggestions for agents</div>
                <div className="text-xs text-[#9598B0] mt-0.5">Show suggested replies inside ticket details</div>
              </div>
              <button
                type="button"
                onClick={() => handleToggle('ai_reply_suggestions')}
                className={`w-12 h-6 flex items-center rounded-full p-1 transition-colors ${
                  settings.ai_reply_suggestions ? 'bg-indigo-600' : 'bg-gray-300'
                }`}
              >
                <div
                  className={`bg-white w-4 h-4 rounded-full shadow-md transform transition-transform ${
                    settings.ai_reply_suggestions ? 'translate-x-6' : 'translate-x-0'
                  }`}
                />
              </button>
            </div>

            {/* Toggle 4: AI ticket summaries */}
            <div className="flex items-center justify-between py-2 border-b border-[#F3F4F6]">
              <div>
                <div className="font-bold text-sm text-[#1C1B2E]">AI ticket summaries</div>
                <div className="text-xs text-[#9598B0] mt-0.5">Summarize conversations for agents automatically</div>
              </div>
              <button
                type="button"
                onClick={() => handleToggle('ai_summaries')}
                className={`w-12 h-6 flex items-center rounded-full p-1 transition-colors ${
                  settings.ai_summaries ? 'bg-indigo-600' : 'bg-gray-300'
                }`}
              >
                <div
                  className={`bg-white w-4 h-4 rounded-full shadow-md transform transition-transform ${
                    settings.ai_summaries ? 'translate-x-6' : 'translate-x-0'
                  }`}
                />
              </button>
            </div>

            {/* Toggle 5: Sentiment detection */}
            <div className="flex items-center justify-between py-2 border-b border-[#F3F4F6]">
              <div>
                <div className="font-bold text-sm text-[#1C1B2E]">Sentiment detection</div>
                <div className="text-xs text-[#9598B0] mt-0.5">Flag frustrated customers for priority handling</div>
              </div>
              <button
                type="button"
                onClick={() => handleToggle('sentiment_detection')}
                className={`w-12 h-6 flex items-center rounded-full p-1 transition-colors ${
                  settings.sentiment_detection ? 'bg-indigo-600' : 'bg-gray-300'
                }`}
              >
                <div
                  className={`bg-white w-4 h-4 rounded-full shadow-md transform transition-transform ${
                    settings.sentiment_detection ? 'translate-x-6' : 'translate-x-0'
                  }`}
                />
              </button>
            </div>

            {/* Slider: Confidence threshold */}
            <div className="pt-4">
              <div className="flex justify-between items-center mb-2">
                <label className="font-bold text-sm text-[#1C1B2E]">Confidence threshold to auto-resolve</label>
                <span className="text-sm font-bold text-indigo-600 bg-indigo-50 px-3 py-1 rounded-lg">
                  {settings.confidence_threshold}%
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                value={settings.confidence_threshold}
                onChange={handleSliderChange}
                className="w-full accent-indigo-600 cursor-pointer h-2 bg-gray-200 rounded-lg"
              />
              <div className="flex justify-between text-xs text-[#9598B0] mt-1 font-medium">
                <span>0%</span>
                <span>85%</span>
                <span>100%</span>
              </div>
            </div>
          </div>

          {/* Right Column: Model & Sources */}
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm space-y-4">
              <h2 className="text-base font-bold text-[#1C1B2E]">Model & Sources</h2>
              <p className="text-xs text-[#9598B0]">The AI answers using content from your connected sources.</p>

              <div className="space-y-3">
                <div className="flex items-center gap-3 p-3 bg-[#F9FAFB] rounded-xl border border-[#E5E7F3]">
                  <BookOpen size={18} className="text-indigo-500" />
                  <span className="text-xs font-semibold text-[#1C1B2E]">
                    Help Center — {articles.length} articles
                  </span>
                </div>

                <div className="flex items-center gap-3 p-3 bg-[#F9FAFB] rounded-xl border border-[#E5E7F3]">
                  <MessageSquare size={18} className="text-indigo-500" />
                  <span className="text-xs font-semibold text-[#1C1B2E]">
                    Past resolved tickets — {resolvedTicketsCount}
                  </span>
                </div>
              </div>
            </div>

            {/* Escalation Rule Card */}
            <div className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm space-y-2">
              <h3 className="text-xs font-bold text-[#6C7089] uppercase tracking-wider">Escalation rule</h3>
              <p className="text-xs text-[#6C7089] leading-relaxed">
                If confidence is below threshold, or the customer says "talk to a human", route to the next available agent.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
