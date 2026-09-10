import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  GitBranch,
  Play,
  Plus,
  Zap,
  CheckCircle2,
  AlertTriangle,
  Flame,
  Layers,
  ArrowRight,
  RefreshCw,
  Trash2,
  Edit2,
  ToggleLeft,
  ToggleRight,
  ShieldCheck,
  Bot,
  Mail,
  Smartphone,
  Instagram,
  Sparkles,
  Search,
  Filter,
  Check,
  X,
  Sliders,
  Send,
  MessageSquare
} from 'lucide-react'
import {
  getAutomations,
  createAutomation,
  updateAutomation,
  deleteAutomation,
  toggleAutomation,
  testDryRun,
  seedDefaultAutomations,
} from '../../api/automations'

export default function ManagerWorkflowAutomation() {
  const queryClient = useQueryClient()
  const [activeTab, setActiveTab] = useState('canvas') // 'canvas' | 'table'
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [editingRule, setEditingRule] = useState(null)
  const [isSimulatorOpen, setIsSimulatorOpen] = useState(false)
  const [selectedRuleDetail, setSelectedRuleDetail] = useState(null)

  // Simulator state
  const [simSubject, setSimSubject] = useState('Critical outage: our production database is down')
  const [simMessage, setSimMessage] = useState('The app is completely unavailable and users are losing data. Need emergency fix!')
  const [simChannel, setSimChannel] = useState('email')
  const [simSentiment, setSimSentiment] = useState('frustrated')
  const [simPriority, setSimPriority] = useState('medium')
  const [simResult, setSimResult] = useState(null)

  // Query automations
  const { data: automations = [], isLoading, isFetching, refetch } = useQuery({
    queryKey: ['automations'],
    queryFn: getAutomations,
  })

  // Mutations
  const toggleMutation = useMutation({
    mutationFn: toggleAutomation,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['automations'] }),
  })

  const deleteMutation = useMutation({
    mutationFn: deleteAutomation,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['automations'] })
      setSelectedRuleDetail(null)
    },
  })

  const seedMutation = useMutation({
    mutationFn: seedDefaultAutomations,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['automations'] }),
  })

  const dryRunMutation = useMutation({
    mutationFn: testDryRun,
    onSuccess: (data) => setSimResult(data),
  })

  const handleRunSimulation = () => {
    dryRunMutation.mutate({
      subject: simSubject,
      message_body: simMessage,
      channel: simChannel,
      sentiment: simSentiment,
      priority: simPriority,
    })
  }

  const activeCount = automations.filter((a) => a.is_active).length
  const totalCount = automations.length
  const escalationRulesCount = automations.filter((a) => {
    const act = a.action_json || {}
    return act.set_priority === 'urgent' || act.set_status === 'escalated'
  }).length

  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] text-[#1C1B2E] flex flex-col min-h-screen">
      {/* Header */}
      <header className="bg-white border-b border-[#E5E7F3] px-8 py-6 sticky top-0 z-10">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600 shadow-sm">
                <GitBranch size={22} />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h1 className="text-xl font-bold font-['Plus_Jakarta_Sans']">Workflow Automation Engine</h1>
                  <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
                    <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                    Live Engine Active
                  </span>
                </div>
                <p className="text-xs text-[#6C7089] mt-0.5">
                  Configure automated condition-action pipelines, auto-routing, sentiment triggers, and escalation rules.
                </p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2.5">
            <button
              onClick={() => {
                setSimResult(null)
                setIsSimulatorOpen(true)
              }}
              className="inline-flex items-center gap-2 px-3.5 py-2 text-xs font-bold rounded-xl bg-purple-50 text-purple-700 border border-purple-200 hover:bg-purple-100 transition shadow-sm"
            >
              <Play size={14} className="fill-current" /> Test Sandbox Simulator
            </button>

            <button
              onClick={() => {
                setEditingRule(null)
                setIsCreateModalOpen(true)
              }}
              className="inline-flex items-center gap-2 px-4 py-2 text-xs font-bold text-white rounded-xl bg-indigo-600 hover:bg-indigo-700 transition shadow-sm"
            >
              <Plus size={15} /> New Automation Rule
            </button>
          </div>
        </div>

        {/* Metrics Row */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
          <div className="bg-[#F8FAFC] border border-[#E2E8F0] rounded-xl p-3.5">
            <div className="text-xs text-[#64748B] font-medium flex items-center gap-1.5">
              <Layers size={14} className="text-indigo-500" /> Total Rules
            </div>
            <div className="text-xl font-bold text-[#0F172A] mt-1">{totalCount}</div>
            <div className="text-[11px] text-[#94A3B8] mt-0.5">In database pipeline</div>
          </div>

          <div className="bg-[#F8FAFC] border border-[#E2E8F0] rounded-xl p-3.5">
            <div className="text-xs text-[#64748B] font-medium flex items-center gap-1.5">
              <Zap size={14} className="text-emerald-500" /> Active Automations
            </div>
            <div className="text-xl font-bold text-emerald-600 mt-1">{activeCount} / {totalCount}</div>
            <div className="text-[11px] text-emerald-700 mt-0.5">Evaluating incoming tickets</div>
          </div>

          <div className="bg-[#F8FAFC] border border-[#E2E8F0] rounded-xl p-3.5">
            <div className="text-xs text-[#64748B] font-medium flex items-center gap-1.5">
              <Flame size={14} className="text-rose-500" /> Priority Escalations
            </div>
            <div className="text-xl font-bold text-rose-600 mt-1">
              {escalationRulesCount} Rules
            </div>
            <div className="text-[11px] text-[#94A3B8] mt-0.5">Urgent SLA dispatch</div>
          </div>

          <div className="bg-[#F8FAFC] border border-[#E2E8F0] rounded-xl p-3.5">
            <div className="text-xs text-[#64748B] font-medium flex items-center gap-1.5">
              <ShieldCheck size={14} className="text-blue-500" /> Engine Health
            </div>
            <div className="text-xl font-bold text-blue-600 mt-1">100% Operational</div>
            <div className="text-[11px] text-blue-700 mt-0.5">Real-time sync enabled</div>
          </div>
        </div>

        {/* View Switcher Bar */}
        <div className="flex items-center justify-between mt-6 pt-4 border-t border-[#F1F5F9]">
          <div className="flex items-center gap-1 bg-[#F1F5F9] p-1 rounded-xl">
            <button
              onClick={() => setActiveTab('canvas')}
              className={`flex items-center gap-2 px-3.5 py-1.5 text-xs font-semibold rounded-lg transition ${
                activeTab === 'canvas' ? 'bg-white text-indigo-600 shadow-sm' : 'text-[#64748B] hover:text-[#0F172A]'
              }`}
            >
              <GitBranch size={14} /> Visual Pipeline Canvas
            </button>
            <button
              onClick={() => setActiveTab('table')}
              className={`flex items-center gap-2 px-3.5 py-1.5 text-xs font-semibold rounded-lg transition ${
                activeTab === 'table' ? 'bg-white text-indigo-600 shadow-sm' : 'text-[#64748B] hover:text-[#0F172A]'
              }`}
            >
              <Sliders size={14} /> Rules Management Table ({totalCount})
            </button>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => refetch()}
              disabled={isFetching}
              className="p-2 text-xs text-[#64748B] hover:text-indigo-600 hover:bg-[#F1F5F9] rounded-lg transition"
              title="Refresh rules"
            >
              <RefreshCw size={15} className={isFetching ? 'animate-spin' : ''} />
            </button>

            <button
              onClick={() => seedMutation.mutate()}
              disabled={seedMutation.isPending}
              className="text-xs font-medium text-[#64748B] hover:text-indigo-600 hover:bg-[#F1F5F9] px-2.5 py-1.5 rounded-lg transition"
            >
              Reset Default Rules
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 p-8 max-w-7xl mx-auto w-full">
        {isLoading ? (
          <div className="flex flex-col items-center justify-center py-24 text-center">
            <RefreshCw size={32} className="text-indigo-600 animate-spin mb-3" />
            <p className="text-sm font-semibold text-[#64748B]">Loading automation pipeline...</p>
          </div>
        ) : activeTab === 'canvas' ? (
          /* Visual Pipeline Canvas View */
          <div className="space-y-6">
            {/* Pipeline Stage Architecture */}
            <div className="bg-gradient-to-r from-indigo-900 via-slate-900 to-slate-950 text-white rounded-2xl p-6 shadow-md border border-slate-800">
              <div className="flex flex-col lg:flex-row items-center justify-between gap-6">
                {/* Step 1 */}
                <div className="flex-1 text-center lg:text-left bg-white/5 border border-white/10 rounded-xl p-4 w-full">
                  <div className="flex items-center justify-center lg:justify-start gap-2 text-indigo-400 font-bold text-xs uppercase tracking-wider mb-1">
                    <MessageSquare size={14} /> Step 1: Ingestion
                  </div>
                  <div className="font-semibold text-sm">Omnichannel Webhook</div>
                  <p className="text-xs text-slate-400 mt-0.5">Email, WhatsApp, Instagram, Facebook, Web</p>
                </div>

                <ArrowRight size={24} className="text-indigo-400 shrink-0 hidden lg:block" />

                {/* Step 2 */}
                <div className="flex-1 text-center lg:text-left bg-white/5 border border-white/10 rounded-xl p-4 w-full">
                  <div className="flex items-center justify-center lg:justify-start gap-2 text-purple-400 font-bold text-xs uppercase tracking-wider mb-1">
                    <Sparkles size={14} /> Step 2: Evaluation Engine
                  </div>
                  <div className="font-semibold text-sm">Rule Evaluation</div>
                  <p className="text-xs text-slate-400 mt-0.5">{activeCount} active rules checked by priority</p>
                </div>

                <ArrowRight size={24} className="text-purple-400 shrink-0 hidden lg:block" />

                {/* Step 3 */}
                <div className="flex-1 text-center lg:text-left bg-white/5 border border-white/10 rounded-xl p-4 w-full">
                  <div className="flex items-center justify-center lg:justify-start gap-2 text-emerald-400 font-bold text-xs uppercase tracking-wider mb-1">
                    <CheckCircle2 size={14} /> Step 3: Action Execution
                  </div>
                  <div className="font-semibold text-sm">Real-Time Dispatch</div>
                  <p className="text-xs text-slate-400 mt-0.5">Priority, Agent Routing, Canned Replies</p>
                </div>
              </div>
            </div>

            {/* Visual Node Rule Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {automations.map((rule) => {
                const conditions = rule.trigger_json?.conditions || {}
                const actions = rule.action_json || {}
                const keywords = conditions.keywords || conditions.keyword || []
                const channels = conditions.channels || conditions.channel || []
                const sentiments = conditions.sentiments || conditions.sentiment || []

                return (
                  <div
                    key={rule.id}
                    className={`bg-white rounded-2xl border transition-all shadow-sm hover:shadow-md p-5 flex flex-col justify-between ${
                      rule.is_active ? 'border-[#E2E8F0]' : 'border-dashed border-gray-300 opacity-60'
                    }`}
                  >
                    <div>
                      {/* Top Header */}
                      <div className="flex items-start justify-between gap-3 mb-3">
                        <div className="flex items-center gap-2.5">
                          <span className="w-6 h-6 rounded-lg bg-indigo-50 text-indigo-700 text-xs font-bold flex items-center justify-center border border-indigo-100">
                            #{rule.priority}
                          </span>
                          <h3 className="font-bold text-sm text-[#0F172A]">{rule.name}</h3>
                        </div>

                        <button
                          onClick={() => toggleMutation.mutate(rule.id)}
                          className={`text-xs font-semibold px-2.5 py-1 rounded-full transition flex items-center gap-1.5 ${
                            rule.is_active
                              ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                              : 'bg-gray-100 text-gray-500 border border-gray-200'
                          }`}
                        >
                          {rule.is_active ? (
                            <>
                              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> Active
                            </>
                          ) : (
                            'Inactive'
                          )}
                        </button>
                      </div>

                      {/* Trigger Conditions Section */}
                      <div className="bg-[#F8FAFC] border border-[#F1F5F9] rounded-xl p-3 mb-3">
                        <div className="text-[11px] font-bold uppercase tracking-wider text-[#64748B] mb-2 flex items-center gap-1.5">
                          <Filter size={12} className="text-indigo-500" /> Triggers & Conditions
                        </div>

                        <div className="flex flex-wrap gap-1.5">
                          {rule.trigger_json?.event_type && (
                            <span className="px-2 py-0.5 text-[11px] font-semibold bg-white border border-slate-200 rounded-md text-slate-700">
                              Event: {rule.trigger_json.event_type}
                            </span>
                          )}

                          {channels.length > 0 && (
                            <span className="px-2 py-0.5 text-[11px] font-semibold bg-blue-50 border border-blue-200 rounded-md text-blue-700">
                              Channels: {Array.isArray(channels) ? channels.join(', ') : channels}
                            </span>
                          )}

                          {keywords.length > 0 && (
                            <span className="px-2 py-0.5 text-[11px] font-semibold bg-purple-50 border border-purple-200 rounded-md text-purple-700">
                              Keywords: {Array.isArray(keywords) ? keywords.slice(0, 3).join(', ') + (keywords.length > 3 ? '...' : '') : keywords}
                            </span>
                          )}

                          {sentiments.length > 0 && (
                            <span className="px-2 py-0.5 text-[11px] font-semibold bg-rose-50 border border-rose-200 rounded-md text-rose-700">
                              Sentiment: {Array.isArray(sentiments) ? sentiments.join(', ') : sentiments}
                            </span>
                          )}

                          {conditions.priorities && (
                            <span className="px-2 py-0.5 text-[11px] font-semibold bg-amber-50 border border-amber-200 rounded-md text-amber-700">
                              Priority is {Array.isArray(conditions.priorities) ? conditions.priorities.join('/') : conditions.priorities}
                            </span>
                          )}
                        </div>
                      </div>

                      {/* Resulting Actions Section */}
                      <div className="bg-[#FAF5FF] border border-[#F3E8FF] rounded-xl p-3">
                        <div className="text-[11px] font-bold uppercase tracking-wider text-purple-700 mb-2 flex items-center gap-1.5">
                          <Zap size={12} className="text-purple-600" /> Automated Actions
                        </div>

                        <div className="space-y-1.5">
                          {actions.set_priority && (
                            <div className="flex items-center gap-2 text-xs text-purple-950 font-medium">
                              <span className="w-1.5 h-1.5 rounded-full bg-purple-500"></span>
                              Set Priority: <span className="font-bold uppercase text-rose-600">{actions.set_priority}</span>
                            </div>
                          )}

                          {actions.set_status && (
                            <div className="flex items-center gap-2 text-xs text-purple-950 font-medium">
                              <span className="w-1.5 h-1.5 rounded-full bg-purple-500"></span>
                              Set Status: <span className="font-bold capitalize text-indigo-600">{actions.set_status}</span>
                            </div>
                          )}

                          {actions.set_category && (
                            <div className="flex items-center gap-2 text-xs text-purple-950 font-medium">
                              <span className="w-1.5 h-1.5 rounded-full bg-purple-500"></span>
                              Tag Category: <span className="font-bold text-slate-800">{actions.set_category}</span>
                            </div>
                          )}

                          {actions.send_canned_reply && (
                            <div className="flex items-start gap-2 text-xs text-purple-950 font-medium">
                              <span className="w-1.5 h-1.5 rounded-full bg-purple-500 mt-1"></span>
                              <span className="italic text-slate-600 line-clamp-1">Auto-Reply: "{actions.send_canned_reply}"</span>
                            </div>
                          )}
                          {actions.assign_agent && (
                            <div className="flex items-center gap-2 text-xs text-purple-950 font-medium">
                              <span className="w-1.5 h-1.5 rounded-full bg-blue-500"></span>
                              Assign Agent: <span className="font-bold text-blue-700 capitalize">{actions.assign_agent === 'round_robin' ? 'Round-Robin' : actions.assign_agent}</span>
                            </div>
                          )}
                          {actions.auto_resolve && (
                            <div className="flex items-center gap-2 text-xs text-purple-950 font-medium">
                              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                              <span className="font-bold text-emerald-700">Auto-Resolve Ticket</span>
                            </div>
                          )}
                          {actions.stop_further_evaluation && (
                            <div className="flex items-center gap-2 text-xs text-orange-700 font-medium">
                              <span className="w-1.5 h-1.5 rounded-full bg-orange-400"></span>
                              <span className="font-bold">Stop pipeline after this rule</span>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>

                    {/* Card Actions Footer */}
                    <div className="flex items-center justify-between border-t border-[#F1F5F9] pt-3 mt-4 text-xs">
                      <span className="text-[#94A3B8] text-[11px]">
                        Last updated {new Date(rule.updated_at).toLocaleDateString()}
                      </span>

                      <div className="flex items-center gap-1.5">
                        <button
                          onClick={() => {
                            setEditingRule(rule)
                            setIsCreateModalOpen(true)
                          }}
                          className="p-1.5 text-slate-500 hover:text-indigo-600 hover:bg-slate-100 rounded-lg transition"
                          title="Edit rule"
                        >
                          <Edit2 size={14} />
                        </button>
                        <button
                          onClick={() => {
                            if (confirm(`Delete automation rule "${rule.name}"?`)) {
                              deleteMutation.mutate(rule.id)
                            }
                          }}
                          className="p-1.5 text-slate-500 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition"
                          title="Delete rule"
                        >
                          <Trash2 size={14} />
                        </button>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        ) : (
          /* Rules Management Table View */
          <div className="bg-white rounded-2xl border border-[#E2E8F0] shadow-sm overflow-hidden">
            <div className="px-6 py-4 border-b border-[#E2E8F0] flex items-center justify-between">
              <h3 className="font-bold text-sm text-[#0F172A]">All Configured Automation Rules</h3>
              <span className="text-xs text-[#64748B]">Sorted by evaluation priority (lower executes first)</span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-[#F8FAFC] border-b border-[#E2E8F0] text-[#64748B] uppercase font-bold text-[10px] tracking-wider">
                  <tr>
                    <th className="py-3 px-4">Priority</th>
                    <th className="py-3 px-4">Rule Name</th>
                    <th className="py-3 px-4">Trigger Criteria</th>
                    <th className="py-3 px-4">Actions Executed</th>
                    <th className="py-3 px-4">Status</th>
                    <th className="py-3 px-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#F1F5F9]">
                  {automations.map((rule) => {
                    const conditions = rule.trigger_json?.conditions || {}
                    const actions = rule.action_json || {}
                    const keywords = conditions.keywords || conditions.keyword || []

                    return (
                      <tr key={rule.id} className="hover:bg-[#F8FAFC] transition">
                        <td className="py-3 px-4 font-bold text-indigo-600">#{rule.priority}</td>
                        <td className="py-3 px-4 font-semibold text-[#0F172A]">{rule.name}</td>
                        <td className="py-3 px-4">
                          <div className="flex flex-wrap gap-1 max-w-xs">
                            {conditions.channels && (
                              <span className="px-1.5 py-0.5 bg-blue-50 text-blue-700 rounded text-[10px] font-semibold">
                                {Array.isArray(conditions.channels) ? conditions.channels.join(', ') : conditions.channels}
                              </span>
                            )}
                            {keywords.length > 0 && (
                              <span className="px-1.5 py-0.5 bg-purple-50 text-purple-700 rounded text-[10px] font-semibold">
                                {keywords.length} keywords
                              </span>
                            )}
                            {conditions.sentiments && (
                              <span className="px-1.5 py-0.5 bg-rose-50 text-rose-700 rounded text-[10px] font-semibold">
                                {Array.isArray(conditions.sentiments) ? conditions.sentiments.join(', ') : conditions.sentiments}
                              </span>
                            )}
                          </div>
                        </td>
                        <td className="py-3 px-4">
                          <div className="flex flex-wrap gap-1">
                            {actions.set_priority && (
                              <span className="px-1.5 py-0.5 bg-rose-100 text-rose-800 rounded text-[10px] font-bold">
                                {actions.set_priority}
                              </span>
                            )}
                            {actions.set_status && (
                              <span className="px-1.5 py-0.5 bg-indigo-100 text-indigo-800 rounded text-[10px] font-bold">
                                {actions.set_status}
                              </span>
                            )}
                            {actions.set_category && (
                              <span className="px-1.5 py-0.5 bg-slate-100 text-slate-800 rounded text-[10px] font-medium">
                                {actions.set_category}
                              </span>
                            )}
                            {actions.send_canned_reply && (
                              <span className="px-1.5 py-0.5 bg-purple-100 text-purple-800 rounded text-[10px] font-medium">
                                auto-reply
                              </span>
                            )}
                            {actions.assign_agent && (
                              <span className="px-1.5 py-0.5 bg-blue-100 text-blue-800 rounded text-[10px] font-medium">
                                {actions.assign_agent === 'round_robin' ? 'round-robin' : 'assign'}
                              </span>
                            )}
                            {actions.auto_resolve && (
                              <span className="px-1.5 py-0.5 bg-emerald-100 text-emerald-800 rounded text-[10px] font-medium">
                                auto-resolve
                              </span>
                            )}
                            {actions.stop_further_evaluation && (
                              <span className="px-1.5 py-0.5 bg-orange-100 text-orange-800 rounded text-[10px] font-medium">
                                stop-pipeline
                              </span>
                            )}
                          </div>

                        </td>
                        <td className="py-3 px-4">
                          <button
                            onClick={() => toggleMutation.mutate(rule.id)}
                            className="cursor-pointer"
                            title={rule.is_active ? 'Disable rule' : 'Enable rule'}
                          >
                            {rule.is_active ? (
                              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                                <Check size={10} /> Active
                              </span>
                            ) : (
                              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-bold bg-gray-100 text-gray-500 border border-gray-200">
                                <X size={10} /> Inactive
                              </span>
                            )}
                          </button>
                        </td>
                        <td className="py-3 px-4 text-right">
                          <div className="inline-flex items-center gap-1">
                            <button
                              onClick={() => {
                                setEditingRule(rule)
                                setIsCreateModalOpen(true)
                              }}
                              className="p-1 text-slate-500 hover:text-indigo-600 rounded transition"
                              title="Edit"
                            >
                              <Edit2 size={14} />
                            </button>
                            <button
                              onClick={() => {
                                if (confirm(`Delete "${rule.name}"?`)) {
                                  deleteMutation.mutate(rule.id)
                                }
                              }}
                              className="p-1 text-slate-500 hover:text-rose-600 rounded transition"
                              title="Delete"
                            >
                              <Trash2 size={14} />
                            </button>
                          </div>
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>

      {/* Simulator Sandbox Modal */}
      {isSimulatorOpen && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white rounded-3xl border border-slate-200 shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 animate-in fade-in zoom-in-95 duration-200">
            <div className="flex items-center justify-between border-b border-slate-100 pb-4 mb-4">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-purple-100 text-purple-700 flex items-center justify-center font-bold">
                  <Play size={16} className="fill-current" />
                </div>
                <div>
                  <h3 className="font-bold text-base text-[#0F172A]">Live Sandbox Rule Simulator</h3>
                  <p className="text-xs text-[#64748B]">Dry-run tickets through the engine without persisting database changes.</p>
                </div>
              </div>
              <button onClick={() => setIsSimulatorOpen(false)} className="text-slate-400 hover:text-slate-600 p-1.5">
                <X size={18} />
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Ticket Subject</label>
                <input
                  type="text"
                  value={simSubject}
                  onChange={(e) => setSimSubject(e.target.value)}
                  className="w-full px-3.5 py-2 text-xs border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="e.g. Critical database outage"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Inbound Message Body</label>
                <textarea
                  rows={2}
                  value={simMessage}
                  onChange={(e) => setSimMessage(e.target.value)}
                  className="w-full px-3.5 py-2 text-xs border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="e.g. System is completely unavailable and users are losing data"
                />
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Channel</label>
                  <select
                    value={simChannel}
                    onChange={(e) => setSimChannel(e.target.value)}
                    className="w-full px-3 py-2 text-xs border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  >
                    <option value="email">Email</option>
                    <option value="whatsapp">WhatsApp</option>
                    <option value="instagram">Instagram</option>
                    <option value="facebook">Facebook</option>
                    <option value="web">Web Chat</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Initial Priority</label>
                  <select
                    value={simPriority}
                    onChange={(e) => setSimPriority(e.target.value)}
                    className="w-full px-3 py-2 text-xs border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="urgent">Urgent</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Sentiment</label>
                  <select
                    value={simSentiment}
                    onChange={(e) => setSimSentiment(e.target.value)}
                    className="w-full px-3 py-2 text-xs border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  >
                    <option value="neutral">Neutral</option>
                    <option value="frustrated">Frustrated</option>
                    <option value="negative">Negative</option>
                    <option value="positive">Positive</option>
                  </select>
                </div>
              </div>

              <div className="flex justify-end pt-2">
                <button
                  onClick={handleRunSimulation}
                  disabled={dryRunMutation.isPending}
                  className="inline-flex items-center gap-2 px-5 py-2.5 text-xs font-bold text-white rounded-xl bg-purple-600 hover:bg-purple-700 transition shadow-md"
                >
                  <Sparkles size={14} /> {dryRunMutation.isPending ? 'Simulating Engine...' : 'Run Simulation'}
                </button>
              </div>

              {/* Simulation Results Display */}
              {simResult && (
                <div className="bg-slate-50 border border-slate-200 rounded-2xl p-4 mt-4 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold uppercase tracking-wider text-slate-700">Evaluation Outcomes</span>
                    <span className="text-[11px] font-semibold text-emerald-600">
                      {simResult.results.filter((r) => r.matched).length} Rule(s) Matched
                    </span>
                  </div>

                  {/* Matched Rules List */}
                  <div className="space-y-2">
                    {simResult.results.map((r, i) => (
                      <div
                        key={i}
                        className={`p-3 rounded-xl border text-xs ${
                          r.matched ? 'bg-emerald-50/70 border-emerald-200 text-emerald-950' : 'bg-white border-slate-200 text-slate-500 opacity-60'
                        }`}
                      >
                        <div className="flex items-center justify-between font-bold">
                          <span>{r.rule_name}</span>
                          <span className={`px-2 py-0.5 rounded text-[10px] ${r.matched ? 'bg-emerald-200 text-emerald-900' : 'bg-slate-100 text-slate-600'}`}>
                            {r.matched ? 'TRIGGERED' : 'SKIPPED'}
                          </span>
                        </div>
                        {r.actions.length > 0 && (
                          <div className="mt-1.5 pl-2 border-l-2 border-emerald-400 space-y-0.5 text-[11px]">
                            {r.actions.map((act, actIdx) => (
                              <div key={actIdx} className="font-semibold text-emerald-800">
                                ➔ {act}
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>

                  {/* Before vs After State Comparison */}
                  <div className="grid grid-cols-2 gap-3 pt-2 border-t border-slate-200 text-xs">
                    <div className="bg-white p-3 rounded-xl border border-slate-200">
                      <div className="font-bold text-slate-500 mb-1 text-[11px] uppercase">Original State</div>
                      <div>Priority: <span className="font-semibold uppercase">{simResult.simulated_ticket.priority}</span></div>
                      <div>Category: <span className="font-semibold">{simResult.simulated_ticket.category || 'None'}</span></div>
                      <div>Status: <span className="font-semibold">{simResult.simulated_ticket.status}</span></div>
                    </div>

                    <div className="bg-purple-50 p-3 rounded-xl border border-purple-200">
                      <div className="font-bold text-purple-700 mb-1 text-[11px] uppercase">Resulting State</div>
                      <div>Priority: <span className="font-bold uppercase text-rose-600">{simResult.final_ticket_state.priority}</span></div>
                      <div>Category: <span className="font-bold text-purple-900">{simResult.final_ticket_state.category || 'None'}</span></div>
                      <div>Status: <span className="font-bold text-indigo-700">{simResult.final_ticket_state.status}</span></div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Rule Creator / Editor Modal */}
      {isCreateModalOpen && (
        <RuleEditorModal
          rule={editingRule}
          onClose={() => {
            setIsCreateModalOpen(false)
            setEditingRule(null)
          }}
          onSave={() => {
            queryClient.invalidateQueries({ queryKey: ['automations'] })
            setIsCreateModalOpen(false)
            setEditingRule(null)
          }}
        />
      )}
    </div>
  )
}

// ─── Subcomponent: Rule Editor Modal ─────────────────────────────────────────

function RuleEditorModal({ rule, onClose, onSave }) {
  const [name, setName] = useState(rule?.name || '')
  const [priority, setPriority] = useState(rule?.priority || 10)
  const [eventType, setEventType] = useState(rule?.trigger_json?.event_type || 'ticket_created')

  // Trigger conditions
  const initialConds = rule?.trigger_json?.conditions || {}
  const [keywords, setKeywords] = useState(
    Array.isArray(initialConds.keywords) ? initialConds.keywords.join(', ') : initialConds.keywords || ''
  )
  const [channels, setChannels] = useState(
    Array.isArray(initialConds.channels) ? initialConds.channels : initialConds.channels ? [initialConds.channels] : []
  )
  const [sentiments, setSentiments] = useState(
    Array.isArray(initialConds.sentiments) ? initialConds.sentiments : initialConds.sentiments ? [initialConds.sentiments] : []
  )

  // Actions
  const initialActions = rule?.action_json || {}
  const [setPriorityAction, setSetPriorityAction] = useState(initialActions.set_priority || '')
  const [setStatusAction, setSetStatusAction] = useState(initialActions.set_status || '')
  const [setCategoryAction, setSetCategoryAction] = useState(initialActions.set_category || '')
  const [sendCannedReply, setSendCannedReply] = useState(initialActions.send_canned_reply || '')
  const [assignAgent, setAssignAgent] = useState(initialActions.assign_agent || '')
  const [autoResolve, setAutoResolve] = useState(initialActions.auto_resolve || false)
  const [stopFurtherEval, setStopFurtherEval] = useState(initialActions.stop_further_evaluation || false)

  const mutation = useMutation({
    mutationFn: async (payload) => {
      if (rule?.id) {
        return updateAutomation(rule.id, payload)
      } else {
        return createAutomation(payload)
      }
    },
    onSuccess: () => onSave(),
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!name.trim()) return

    const conditions = {}
    if (keywords.trim()) {
      conditions.keywords = keywords.split(',').map((k) => k.trim()).filter(Boolean)
    }
    if (channels.length > 0) {
      conditions.channels = channels
    }
    if (sentiments.length > 0) {
      conditions.sentiments = sentiments
    }

    const action_json = {}
    if (setPriorityAction) action_json.set_priority = setPriorityAction
    if (setStatusAction) action_json.set_status = setStatusAction
    if (setCategoryAction.trim()) action_json.set_category = setCategoryAction.trim()
    if (sendCannedReply.trim()) action_json.send_canned_reply = sendCannedReply.trim()
    if (assignAgent.trim() && assignAgent !== 'none') action_json.assign_agent = assignAgent.trim()
    if (autoResolve) action_json.auto_resolve = true
    if (stopFurtherEval) action_json.stop_further_evaluation = true

    mutation.mutate({
      name: name.trim(),
      priority: Number(priority),
      trigger_json: {
        event_type: eventType,
        conditions,
      },
      action_json,
      is_active: rule ? rule.is_active : true,
    })
  }

  const toggleChannel = (ch) => {
    if (channels.includes(ch)) {
      setChannels(channels.filter((c) => c !== ch))
    } else {
      setChannels([...channels, ch])
    }
  }

  const toggleSentiment = (st) => {
    if (sentiments.includes(st)) {
      setSentiments(sentiments.filter((s) => s !== st))
    } else {
      setSentiments([...sentiments, st])
    }
  }

  return (
    <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-white rounded-3xl border border-slate-200 shadow-2xl max-w-xl w-full max-h-[90vh] overflow-y-auto p-6 animate-in fade-in zoom-in-95 duration-200">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4 mb-4">
          <h3 className="font-bold text-base text-[#0F172A]">
            {rule ? 'Edit Automation Rule' : 'Create New Automation Rule'}
          </h3>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 p-1.5">
            <X size={18} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-3 gap-3">
            <div className="col-span-2">
              <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Rule Name</label>
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g. VIP Urgent Ticket Routing"
                className="w-full px-3 py-2 text-xs border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Priority (Order)</label>
              <input
                type="number"
                value={priority}
                onChange={(e) => setPriority(e.target.value)}
                className="w-full px-3 py-2 text-xs border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>

          {/* Trigger Builder */}
          <div className="bg-[#F8FAFC] p-3.5 rounded-2xl border border-slate-200 space-y-3">
            <div className="text-xs font-bold text-indigo-700 uppercase flex items-center gap-1.5">
              <Filter size={14} /> 1. Trigger Criteria
            </div>

            <div>
              <label className="block text-[11px] font-semibold text-slate-600 mb-1">Trigger Event</label>
              <select
                value={eventType}
                onChange={(e) => setEventType(e.target.value)}
                className="w-full px-3 py-1.5 text-xs border border-slate-200 rounded-lg focus:outline-none"
              >
                <option value="ticket_created">When a New Ticket is Created</option>
                <option value="message_received">When a Message is Received</option>
                <option value="any">On Any Ticket Update</option>
              </select>
            </div>

            <div>
              <label className="block text-[11px] font-semibold text-slate-600 mb-1">
                Keyword Matches (comma-separated)
              </label>
              <input
                type="text"
                value={keywords}
                onChange={(e) => setKeywords(e.target.value)}
                placeholder="e.g. outage, refund, billing error, cancel"
                className="w-full px-3 py-1.5 text-xs border border-slate-200 rounded-lg focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-[11px] font-semibold text-slate-600 mb-1">Filter by Channels</label>
              <div className="flex flex-wrap gap-1.5">
                {['email', 'whatsapp', 'instagram', 'facebook', 'web'].map((ch) => (
                  <button
                    key={ch}
                    type="button"
                    onClick={() => toggleChannel(ch)}
                    className={`px-2.5 py-1 rounded-lg text-xs font-semibold capitalize transition ${
                      channels.includes(ch)
                        ? 'bg-indigo-600 text-white shadow-sm'
                        : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-100'
                    }`}
                  >
                    {ch}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text[11px] font-semibold text-slate-600 mb-1">Filter by Sentiment</label>
              <div className="flex flex-wrap gap-1.5">
                {['frustrated', 'negative', 'angry', 'neutral', 'positive'].map((st) => (
                  <button
                    key={st}
                    type="button"
                    onClick={() => toggleSentiment(st)}
                    className={`px-2.5 py-1 rounded-lg text-xs font-semibold capitalize transition ${
                      sentiments.includes(st)
                        ? 'bg-rose-600 text-white shadow-sm'
                        : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-100'
                    }`}
                  >
                    {st}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Action Builder */}
          <div className="bg-[#FAF5FF] p-3.5 rounded-2xl border border-purple-200 space-y-3">
            <div className="text-xs font-bold text-purple-700 uppercase flex items-center gap-1.5">
              <Zap size={14} /> 2. Resulting Actions
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-[11px] font-semibold text-slate-600 mb-1">Set Priority</label>
                <select
                  value={setPriorityAction}
                  onChange={(e) => setSetPriorityAction(e.target.value)}
                  className="w-full px-3 py-1.5 text-xs border border-purple-200 rounded-lg focus:outline-none"
                >
                  <option value="">No change</option>
                  <option value="urgent">Urgent</option>
                  <option value="high">High</option>
                  <option value="medium">Medium</option>
                  <option value="low">Low</option>
                </select>
              </div>

              <div>
                <label className="block text-[11px] font-semibold text-slate-600 mb-1">Set Status</label>
                <select
                  value={setStatusAction}
                  onChange={(e) => setSetStatusAction(e.target.value)}
                  className="w-full px-3 py-1.5 text-xs border border-purple-200 rounded-lg focus:outline-none"
                >
                  <option value="">No change</option>
                  <option value="escalated">Escalated</option>
                  <option value="open">Open</option>
                  <option value="pending">Pending</option>
                  <option value="resolved">Resolved</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-[11px] font-semibold text-slate-600 mb-1">Tag Category</label>
              <input
                type="text"
                value={setCategoryAction}
                onChange={(e) => setSetCategoryAction(e.target.value)}
                placeholder="e.g. Emergency Outage, VIP Support, Billing"
                className="w-full px-3 py-1.5 text-xs border border-purple-200 rounded-lg focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-[11px] font-semibold text-slate-600 mb-1">Automated Canned Reply</label>
              <textarea
                rows={2}
                value={sendCannedReply}
                onChange={(e) => setSendCannedReply(e.target.value)}
                placeholder="e.g. We have received your emergency ticket and escalated to senior support..."
                className="w-full px-3 py-1.5 text-xs border border-purple-200 rounded-lg focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-[11px] font-semibold text-slate-600 mb-1">Assign Agent</label>
              <select
                value={assignAgent}
                onChange={(e) => setAssignAgent(e.target.value)}
                className="w-full px-3 py-1.5 text-xs border border-purple-200 rounded-lg focus:outline-none"
              >
                <option value="none">No assignment</option>
                <option value="round_robin">Round-Robin (auto-pick available agent)</option>
              </select>
            </div>

            <div className="flex items-center gap-4 pt-1">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={autoResolve}
                  onChange={(e) => setAutoResolve(e.target.checked)}
                  className="w-4 h-4 rounded accent-emerald-600"
                />
                <span className="text-xs font-semibold text-slate-700">Auto-resolve ticket</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={stopFurtherEval}
                  onChange={(e) => setStopFurtherEval(e.target.checked)}
                  className="w-4 h-4 rounded accent-orange-500"
                />
                <span className="text-xs font-semibold text-slate-700">Stop pipeline after this rule</span>
              </label>
            </div>
          </div>

          <div className="flex justify-end gap-2 pt-3 border-t border-slate-100">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-xl transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={mutation.isPending}
              className="px-5 py-2 text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl transition shadow-md"
            >
              {mutation.isPending ? 'Saving...' : rule ? 'Update Rule' : 'Create Automation'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
