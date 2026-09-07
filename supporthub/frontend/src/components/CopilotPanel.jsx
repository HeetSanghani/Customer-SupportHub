import { useState } from 'react'
import { ticketsApi } from '../api/tickets'
import {
  Sparkles, FileText, Link2, Zap, User,
  RefreshCw, Copy, CheckCheck, Lightbulb,
  AlertTriangle, ChevronRight, Shield
} from 'lucide-react'

const TONE_OPTIONS = [
  { value: 'formal', label: 'Formal' },
  { value: 'empathetic', label: 'Empathetic' },
  { value: 'concise', label: 'Concise' },
]

const ACTION_TYPE_COLORS = {
  sla: 'bg-red-50 border-red-200 text-red-800',
  status_change: 'bg-indigo-50 border-indigo-200 text-indigo-800',
  reply: 'bg-emerald-50 border-emerald-200 text-emerald-800',
  info: 'bg-blue-50 border-blue-200 text-blue-800',
  escalate: 'bg-orange-50 border-orange-200 text-orange-800',
}

const ACTION_TYPE_BADGE = {
  sla: 'bg-red-100 text-red-700',
  status_change: 'bg-indigo-100 text-indigo-700',
  reply: 'bg-emerald-100 text-emerald-700',
  info: 'bg-blue-100 text-blue-700',
  escalate: 'bg-orange-100 text-orange-700',
}

const TABS = [
  { id: 'suggest', icon: Sparkles, label: 'Reply' },
  { id: 'nba', icon: Zap, label: 'Actions' },
  { id: 'summary', icon: FileText, label: 'Summary' },
  { id: 'similar', icon: Link2, label: 'Similar' },
]

export default function CopilotPanel({ ticketId, role, onUseSuggestion }) {
  const [tab, setTab] = useState('suggest')

  // Suggest Reply state
  const [tone, setTone] = useState('formal')
  const [suggestion, setSuggestion] = useState(null)
  const [groundingScore, setGroundingScore] = useState(null)
  const [groundingViolations, setGroundingViolations] = useState([])
  const [isGrounded, setIsGrounded] = useState(true)
  const [loadingSuggest, setLoadingSuggest] = useState(false)
  const [copied, setCopied] = useState(false)

  // Summary state
  const [summary, setSummary] = useState(null)
  const [loadingSummary, setLoadingSummary] = useState(false)

  // Similar tickets state
  const [similar, setSimilar] = useState([])
  const [loadingSimilar, setLoadingSimilar] = useState(false)

  // NBA state
  const [actions, setActions] = useState([])
  const [loadingNBA, setLoadingNBA] = useState(false)

  const handleSuggest = async () => {
    setLoadingSuggest(true)
    setSuggestion(null)
    try {
      const res = await ticketsApi.suggestReplyWithTone(ticketId, tone)
      setSuggestion(res.data.suggestion)
      setGroundingScore(res.data.grounding_score ?? null)
      setGroundingViolations(res.data.grounding_violations ?? [])
      setIsGrounded(res.data.is_grounded ?? true)
    } catch {
      setSuggestion('Unable to generate suggestion right now. Please try again.')
      setGroundingScore(null)
      setGroundingViolations([])
      setIsGrounded(true)
    } finally {
      setLoadingSuggest(false)
    }
  }

  const handleUse = () => {
    if (!suggestion) return
    onUseSuggestion?.(suggestion)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleSummarize = async () => {
    setLoadingSummary(true)
    setSummary(null)
    try {
      const res = await ticketsApi.summarize(ticketId)
      setSummary(res.data.summary)
    } catch {
      setSummary('Unable to generate summary right now.')
    } finally {
      setLoadingSummary(false)
    }
  }

  const handleSimilar = async () => {
    setLoadingSimilar(true)
    setSimilar([])
    try {
      const res = await ticketsApi.getSimilar(ticketId)
      setSimilar(res.data)
    } catch {
      setSimilar([])
    } finally {
      setLoadingSimilar(false)
    }
  }

  const handleNBA = async () => {
    setLoadingNBA(true)
    setActions([])
    try {
      const res = await ticketsApi.getNextAction(ticketId)
      setActions(res.data.actions || [])
    } catch {
      setActions([])
    } finally {
      setLoadingNBA(false)
    }
  }

  if (!['agent', 'admin', 'manager'].includes(role)) return null

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* HITL Safety Banner */}
      <div className="flex items-center gap-2 px-3 py-2 bg-amber-50 border-b border-amber-200">
        <Shield size={12} className="text-amber-600 shrink-0" />
        <p className="text-[10px] text-amber-700 font-medium leading-tight">
          AI Copilot — suggestions are for your review only, never sent automatically.
        </p>
      </div>

      {/* Tab Bar */}
      <div className="flex border-b border-[#E5E7F3] bg-[#F8FAFC]">
        {TABS.map(t => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`flex-1 flex items-center justify-center gap-1 py-2.5 text-[10px] font-bold uppercase tracking-wide transition-colors ${
              tab === t.id
                ? 'text-indigo-600 border-b-2 border-indigo-500 bg-white'
                : 'text-[#9598B0] hover:text-[#6C7089]'
            }`}
          >
            <t.icon size={11} /> {t.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">

        {/* ── Suggest Reply ── */}
        {tab === 'suggest' && (
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <div className="p-1.5 bg-indigo-100 rounded-lg"><Sparkles size={13} className="text-indigo-600" /></div>
              <div>
                <div className="text-xs font-bold text-[#1C1B2E]">AI Suggested Reply</div>
                <div className="text-[10px] text-[#9598B0]">Context-aware draft with grounding validation</div>
              </div>
            </div>

            {/* Tone Selector */}
            <div>
              <div className="text-[10px] font-bold text-[#6C7089] mb-1.5 uppercase tracking-wide">Tone</div>
              <div className="flex gap-1.5">
                {TONE_OPTIONS.map(opt => (
                  <button
                    key={opt.value}
                    onClick={() => setTone(opt.value)}
                    className={`flex-1 py-1.5 rounded-lg text-[10px] font-bold border transition-all ${
                      tone === opt.value
                        ? 'bg-indigo-600 text-white border-indigo-600 shadow-sm'
                        : 'bg-white text-[#6C7089] border-[#E5E7F3] hover:border-indigo-300'
                    }`}
                  >
                    {opt.label}
                  </button>
                ))}
              </div>
            </div>

            <button
              onClick={handleSuggest}
              disabled={loadingSuggest}
              className="w-full flex items-center justify-center gap-2 py-2.5 bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white text-xs font-bold rounded-xl transition-all shadow-sm disabled:opacity-60"
            >
              {loadingSuggest
                ? <><RefreshCw size={12} className="animate-spin" /> Generating...</>
                : <><Sparkles size={12} /> Generate AI Reply</>}
            </button>

            {suggestion && (
              <div className="space-y-2">
                {/* Grounding Badge */}
                {groundingScore !== null && (
                  <div className={`flex items-center gap-1.5 px-2 py-1 rounded-lg text-[10px] font-bold ${
                    isGrounded ? 'bg-emerald-50 text-emerald-700' : 'bg-red-50 text-red-700'
                  }`}>
                    <Shield size={10} />
                    {isGrounded
                      ? `Grounded · ${Math.round(groundingScore * 100)}% confidence`
                      : `Grounding issues · ${Math.round(groundingScore * 100)}% confidence`}
                  </div>
                )}

                {/* Violations */}
                {groundingViolations.length > 0 && (
                  <div className="bg-orange-50 border border-orange-200 rounded-xl p-2.5 space-y-1">
                    <div className="flex items-center gap-1 text-[10px] font-bold text-orange-700">
                      <AlertTriangle size={10} /> Grounding Warnings
                    </div>
                    {groundingViolations.slice(0, 2).map((v, i) => (
                      <p key={i} className="text-[10px] text-orange-700 leading-snug">{v}</p>
                    ))}
                  </div>
                )}

                {/* Suggestion Text */}
                <div className="bg-indigo-50 border border-indigo-200 rounded-xl p-3">
                  <p className="text-xs text-[#1C1B2E] leading-relaxed whitespace-pre-wrap">{suggestion}</p>
                </div>

                <button
                  onClick={handleUse}
                  className={`w-full flex items-center justify-center gap-1.5 py-2 text-[10px] font-bold rounded-lg transition-all ${
                    copied
                      ? 'bg-emerald-500 text-white'
                      : 'bg-white border border-indigo-200 text-indigo-700 hover:bg-indigo-50'
                  }`}
                >
                  {copied
                    ? <><CheckCheck size={11} /> Pasted to Composer!</>
                    : <><Copy size={11} /> Use in Composer</>}
                </button>
              </div>
            )}

            {!suggestion && !loadingSuggest && (
              <div className="bg-amber-50 border border-amber-100 rounded-xl p-3">
                <div className="flex items-center gap-1.5 mb-1">
                  <Lightbulb size={11} className="text-amber-500" />
                  <span className="text-[10px] font-bold text-amber-700">Pro Tip</span>
                </div>
                <p className="text-[10px] text-amber-700 leading-relaxed">
                  Select a tone, then click Generate. Click <strong>"Use in Composer"</strong> to paste into the reply box — you must send it manually.
                </p>
              </div>
            )}
          </div>
        )}

        {/* ── Next-Best-Action ── */}
        {tab === 'nba' && (
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <div className="p-1.5 bg-orange-100 rounded-lg"><Zap size={13} className="text-orange-600" /></div>
              <div>
                <div className="text-xs font-bold text-[#1C1B2E]">Next Best Actions</div>
                <div className="text-[10px] text-[#9598B0]">Prioritised recommendations based on ticket state</div>
              </div>
            </div>

            <button
              onClick={handleNBA}
              disabled={loadingNBA}
              className="w-full flex items-center justify-center gap-2 py-2.5 bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white text-xs font-bold rounded-xl transition-all shadow-sm disabled:opacity-60"
            >
              {loadingNBA
                ? <><RefreshCw size={12} className="animate-spin" /> Analysing...</>
                : <><Zap size={12} /> Get Recommendations</>}
            </button>

            {actions.length > 0 && (
              <div className="space-y-2">
                {actions.map(action => (
                  <div
                    key={action.id}
                    className={`border rounded-xl p-3 space-y-1.5 ${ACTION_TYPE_COLORS[action.action_type] || 'bg-gray-50 border-gray-200 text-gray-800'}`}
                  >
                    <div className="flex items-center justify-between gap-2">
                      <div className="flex items-center gap-1.5">
                        <span className="w-5 h-5 rounded-full bg-white/70 flex items-center justify-center text-[10px] font-black shrink-0">
                          {action.priority}
                        </span>
                        <span className="text-xs font-bold leading-tight">{action.label}</span>
                      </div>
                      <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded-md uppercase tracking-wide shrink-0 ${ACTION_TYPE_BADGE[action.action_type] || 'bg-gray-100 text-gray-600'}`}>
                        {action.action_type.replace('_', ' ')}
                      </span>
                    </div>
                    <p className="text-[10px] leading-relaxed opacity-80 pl-7">{action.rationale}</p>
                  </div>
                ))}
              </div>
            )}

            {actions.length === 0 && !loadingNBA && (
              <div className="text-center py-6 text-[#9598B0] text-[10px]">
                <Zap size={26} className="mx-auto mb-2 opacity-25" />
                Click above to get AI-powered action recommendations.
              </div>
            )}
          </div>
        )}

        {/* ── Summary ── */}
        {tab === 'summary' && (
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <div className="p-1.5 bg-blue-100 rounded-lg"><FileText size={13} className="text-blue-600" /></div>
              <div>
                <div className="text-xs font-bold text-[#1C1B2E]">AI Ticket Summary</div>
                <div className="text-[10px] text-[#9598B0]">Condenses the full conversation</div>
              </div>
            </div>

            <button
              onClick={handleSummarize}
              disabled={loadingSummary}
              className="w-full flex items-center justify-center gap-2 py-2.5 bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white text-xs font-bold rounded-xl transition-all shadow-sm disabled:opacity-60"
            >
              {loadingSummary
                ? <><RefreshCw size={12} className="animate-spin" /> Summarising...</>
                : <><FileText size={12} /> Generate Summary</>}
            </button>

            {summary && (
              <div className="bg-blue-50 border border-blue-200 rounded-xl p-3">
                <p className="text-xs text-[#1C1B2E] leading-relaxed">{summary}</p>
              </div>
            )}

            {!summary && !loadingSummary && (
              <div className="text-center py-6 text-[#9598B0] text-[10px]">
                <FileText size={26} className="mx-auto mb-2 opacity-25" />
                Click above to generate an AI summary of this ticket.
              </div>
            )}
          </div>
        )}

        {/* ── Similar Cases ── */}
        {tab === 'similar' && (
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <div className="p-1.5 bg-emerald-100 rounded-lg"><Link2 size={13} className="text-emerald-600" /></div>
              <div>
                <div className="text-xs font-bold text-[#1C1B2E]">Similar Past Cases</div>
                <div className="text-[10px] text-[#9598B0]">Resolved tickets with similar context</div>
              </div>
            </div>

            <button
              onClick={handleSimilar}
              disabled={loadingSimilar}
              className="w-full flex items-center justify-center gap-2 py-2.5 bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600 text-white text-xs font-bold rounded-xl transition-all shadow-sm disabled:opacity-60"
            >
              {loadingSimilar
                ? <><RefreshCw size={12} className="animate-spin" /> Searching...</>
                : <><Link2 size={12} /> Find Similar Cases</>}
            </button>

            {similar.length > 0 && (
              <div className="space-y-2">
                {similar.map(t => (
                  <div key={t.id} className="bg-emerald-50 border border-emerald-100 rounded-xl p-3 space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-bold text-emerald-700 font-mono">{t.ref}</span>
                      <span className="text-[10px] bg-emerald-200 text-emerald-800 px-2 py-0.5 rounded-full font-bold">
                        {Math.round(t.similarity * 100)}% match
                        {t.is_fallback && ' (approx)'}
                      </span>
                    </div>
                    <p className="text-xs font-semibold text-[#1C1B2E] line-clamp-2">{t.subject}</p>
                    <div className="flex items-center gap-1.5">
                      <span className="text-[9px] bg-gray-100 text-gray-600 px-2 py-0.5 rounded-md font-semibold uppercase">{t.category}</span>
                      <span className="text-[9px] bg-green-100 text-green-700 px-2 py-0.5 rounded-md font-semibold capitalize">✓ {t.status}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {similar.length === 0 && !loadingSimilar && (
              <div className="text-center py-6 text-[#9598B0] text-[10px]">
                <Link2 size={26} className="mx-auto mb-2 opacity-25" />
                Search for resolved cases that may contain relevant solutions.
              </div>
            )}
          </div>
        )}

      </div>
    </div>
  )
}
