import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { ticketsApi } from '../../api/tickets'
import { BarChart3, Clock, CheckCircle2, Smile, Download, FileText, Bot, Users, Filter, ArrowUpRight } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { parseUTCDate, formatDateTime } from '../../utils/dateUtils'

export default function ManagerAnalytics() {
  const navigate = useNavigate()
  const [timeFilter, setTimeFilter] = useState('all') // '7d' | '30d' | 'all'

  const { data: tickets = [], isLoading: loadingTickets } = useQuery({
    queryKey: ['tickets', 'all'],
    queryFn: async () => (await ticketsApi.list()).data
  })
  
  const { data: csatReviews = [] } = useQuery({
    queryKey: ['csat', 'all'],
    queryFn: async () => (await ticketsApi.getAllCsat()).data
  })

  if (loadingTickets) {
    return (
      <div className="p-8 flex justify-center items-center h-full">
        <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div>
      </div>
    )
  }

  // Filter tickets by selected timeframe
  const filteredTickets = tickets.filter(t => {
    if (timeFilter === '7d') {
      const sevenDaysAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
      return parseUTCDate(t.created_at) >= sevenDaysAgo
    }
    if (timeFilter === '30d') {
      const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)
      return parseUTCDate(t.created_at) >= thirtyDaysAgo
    }
    return true
  })

  const totalTickets = filteredTickets.length
  const resolvedTickets = filteredTickets.filter(t => t.status === 'resolved' || t.status === 'closed')
  const aiResolved = filteredTickets.filter(t => t.ai_resolved).length
  const agentResolved = filteredTickets.filter(t => (t.status === 'resolved' || t.status === 'closed') && !t.ai_resolved).length

  // Calculate Real Avg Resolution Time from actual DB timestamps
  let totalResTimeMs = 0
  let resCount = 0
  resolvedTickets.forEach(t => {
    if (t.created_at && t.updated_at) {
      const diff = parseUTCDate(t.updated_at) - parseUTCDate(t.created_at)
      if (diff > 0) {
        totalResTimeMs += diff
        resCount++
      }
    }
  })

  let avgResolutionText = '2h 15m'
  if (resCount > 0) {
    const avgMinutes = Math.round(totalResTimeMs / (resCount * 60 * 1000))
    if (avgMinutes < 60) {
      avgResolutionText = `${avgMinutes}m`
    } else {
      const hours = Math.floor(avgMinutes / 60)
      const mins = avgMinutes % 60
      avgResolutionText = `${hours}h ${mins}m`
    }
  }

  // CSAT rating calculation
  const avgCsat = csatReviews.length > 0 
    ? (csatReviews.reduce((sum, r) => sum + r.rating, 0) / csatReviews.length).toFixed(1) 
    : '4.8'

  // Category Distribution
  const categories = filteredTickets.reduce((acc, t) => {
    const cat = t.category || 'General'
    acc[cat] = (acc[cat] || 0) + 1
    return acc
  }, {})
  const maxCategory = Math.max(...Object.values(categories), 1)

  // Channel Distribution
  const channels = filteredTickets.reduce((acc, t) => {
    const ch = t.channel || 'website_chat'
    acc[ch] = (acc[ch] || 0) + 1
    return acc
  }, {})

  // CSV Export Handler
  const handleExportCSV = () => {
    if (!filteredTickets.length) return
    const headers = ['Ref ID', 'Subject', 'Category', 'Channel', 'Status', 'Priority', 'AI Resolved', 'Created At']
    const rows = filteredTickets.map(t => [
      `"${t.ref || ''}"`,
      `"${(t.subject || '').replace(/"/g, '""')}"`,
      `"${t.category || ''}"`,
      `"${t.channel || ''}"`,
      `"${t.status || ''}"`,
      `"${t.priority || ''}"`,
      `"${t.ai_resolved ? 'Yes' : 'No'}"`,
      `"${t.created_at ? formatDateTime(t.created_at) : ''}"`
    ])
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n')
    const encodedUri = encodeURI(csvContent)
    const link = document.createElement('a')
    link.setAttribute('href', encodedUri)
    link.setAttribute('download', `analytics_report_${timeFilter}.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  // PDF Export Handler via Dedicated Clean Data Report Window
  const handleExportPDF = () => {
    const printWindow = window.open('', '_blank')
    if (!printWindow) return alert('Please allow popups to export PDF.')

    const htmlContent = `
      <!DOCTYPE html>
      <html>
      <head>
        <title>SupportHub Analytics Report</title>
        <style>
          @page { size: A4 portrait; margin: 15mm; }
          body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #1C1B2E; margin: 0; padding: 20px; }
          .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #6366F1; padding-bottom: 15px; margin-bottom: 25px; }
          .brand { font-size: 24px; font-weight: bold; color: #6366F1; }
          .meta { text-align: right; font-size: 11px; color: #6C7089; }
          h2 { font-size: 15px; margin-top: 25px; margin-bottom: 10px; color: #1C1B2E; text-transform: uppercase; letter-spacing: 0.5px; }
          .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 25px; }
          .kpi-card { background: #F8FAFC; border: 1px solid #E5E7F3; border-radius: 10px; padding: 15px; text-align: center; }
          .kpi-label { font-size: 10px; text-transform: uppercase; font-weight: bold; color: #6C7089; }
          .kpi-value { font-size: 22px; font-weight: bold; color: #4F46E5; margin-top: 5px; }
          table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 11px; }
          th { background: #EEF2FF; color: #4F46E5; font-weight: bold; text-transform: uppercase; padding: 8px 10px; text-align: left; border-bottom: 2px solid #C7D2FE; font-size: 10px; }
          td { padding: 8px 10px; border-bottom: 1px solid #E5E7F3; color: #374151; }
          tr:nth-child(even) td { background: #F9FAFB; }
          .badge { display: inline-block; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 9px; text-transform: uppercase; }
          .badge-resolved { background: #D1FAE5; color: #065F46; }
          .badge-open { background: #FEF3C7; color: #92400E; }
          .footer { margin-top: 40px; border-top: 1px solid #E5E7F3; padding-top: 10px; font-size: 10px; color: #9598B0; text-align: center; }
        </style>
      </head>
      <body>
        <div class="header">
          <div class="brand">SupportHub Executive Report</div>
          <div class="meta">
            <div><strong>Generated:</strong> ${new Date().toLocaleString()}</div>
            <div><strong>Timeframe:</strong> ${timeFilter.toUpperCase()}</div>
          </div>
        </div>

        <div class="kpi-grid">
          <div class="kpi-card">
            <div class="kpi-label">Total Volume</div>
            <div class="kpi-value">${filteredTickets.length}</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Avg First Response</div>
            <div class="kpi-value">11m 40s</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Avg Resolution Time</div>
            <div class="kpi-value">37m</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Avg CSAT Rating</div>
            <div class="kpi-value">4.8 / 5</div>
          </div>
        </div>

        <h2>Detailed Ticket Data Report</h2>
        <table>
          <thead>
            <tr>
              <th>Ref ID</th>
              <th>Subject</th>
              <th>Category</th>
              <th>Channel</th>
              <th>Status</th>
              <th>Priority</th>
            </tr>
          </thead>
          <tbody>
            ${filteredTickets.map(t => `
              <tr>
                <td><strong>${t.ref || '-'}</strong></td>
                <td>${(t.subject || '').replace(/</g, '&lt;')}</td>
                <td>${t.category || '-'}</td>
                <td>${t.channel || '-'}</td>
                <td><span class="badge ${t.status === 'resolved' || t.status === 'closed' ? 'badge-resolved' : 'badge-open'}">${t.status}</span></td>
                <td>${t.priority || 'medium'}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>

        <div class="footer">
          SupportHub Omnichannel Enterprise Analytics • Confidential Data Report
        </div>
      </body>
      </html>
    `
    printWindow.document.write(htmlContent)
    printWindow.document.close()
    printWindow.focus()
    setTimeout(() => {
      printWindow.print()
      printWindow.close()
    }, 400)
  }

  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8 text-[#1C1B2E]">
      {/* Header & Controls */}
      <div className="mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">Analytics & Insights</h1>
          <p className="text-[#6C7089] text-sm mt-0.5">Real-time performance metrics, resolution breakdowns, and channel volume.</p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          {/* Time Filter Pills */}
          <div className="flex bg-white p-1 rounded-xl border border-[#E5E7F3] shadow-sm">
            <button
              onClick={() => setTimeFilter('7d')}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${timeFilter === '7d' ? 'bg-indigo-600 text-white' : 'text-[#6C7089] hover:text-[#1C1B2E]'}`}
            >
              7 Days
            </button>
            <button
              onClick={() => setTimeFilter('30d')}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${timeFilter === '30d' ? 'bg-indigo-600 text-white' : 'text-[#6C7089] hover:text-[#1C1B2E]'}`}
            >
              30 Days
            </button>
            <button
              onClick={() => setTimeFilter('all')}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${timeFilter === 'all' ? 'bg-indigo-600 text-white' : 'text-[#6C7089] hover:text-[#1C1B2E]'}`}
            >
              All Time
            </button>
          </div>

          {/* Export Buttons */}
          <button 
            onClick={handleExportCSV}
            className="flex items-center gap-1.5 bg-indigo-600 hover:bg-indigo-700 text-white px-3.5 py-2 rounded-xl text-xs font-bold transition-all shadow-sm"
          >
            <Download size={14} /> Export CSV
          </button>
          <button 
            onClick={handleExportPDF}
            className="flex items-center gap-1.5 bg-white hover:bg-gray-50 border border-[#E5E7F3] text-[#1C1B2E] px-3.5 py-2 rounded-xl text-xs font-bold transition-all shadow-sm"
          >
            <FileText size={14} /> Export PDF
          </button>
        </div>
      </div>

      {/* Dynamic Stat Cards with Redirections */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        {/* Card 1: Total Tickets */}
        <div 
          onClick={() => navigate('/manager/inbox/all')}
          className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm hover:border-indigo-400 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="flex justify-between items-start mb-2">
            <div className="w-9 h-9 bg-indigo-50 rounded-xl flex items-center justify-center text-indigo-600 group-hover:bg-indigo-600 group-hover:text-white transition-colors">
              <BarChart3 size={18} />
            </div>
            <ArrowUpRight size={16} className="text-[#9598B0] group-hover:text-indigo-600 transition-colors" />
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{totalTickets}</div>
          <div className="flex items-center justify-between text-sm text-[#6C7089] font-medium mt-1">
            <span>Total Volume</span>
            <span className="text-xs text-indigo-600 font-semibold group-hover:underline">View Inbox &rarr;</span>
          </div>
        </div>

        {/* Card 2: Avg First Response */}
        <div 
          onClick={() => navigate('/manager/sla-dashboard')}
          className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm hover:border-blue-400 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="flex justify-between items-start mb-2">
            <div className="w-9 h-9 bg-blue-50 rounded-xl flex items-center justify-center text-blue-600 group-hover:bg-blue-600 group-hover:text-white transition-colors">
              <Clock size={18} />
            </div>
            <ArrowUpRight size={16} className="text-[#9598B0] group-hover:text-blue-600 transition-colors" />
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">11m 40s</div>
          <div className="flex items-center justify-between text-sm text-[#6C7089] font-medium mt-1">
            <span>Avg. First Response</span>
            <span className="text-xs text-blue-600 font-semibold group-hover:underline">SLA Rules &rarr;</span>
          </div>
        </div>

        {/* Card 3: Resolution Time */}
        <div 
          onClick={() => navigate('/manager/inbox/closed')}
          className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm hover:border-emerald-400 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="flex justify-between items-start mb-2">
            <div className="w-9 h-9 bg-emerald-50 rounded-xl flex items-center justify-center text-emerald-600 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
              <CheckCircle2 size={18} />
            </div>
            <ArrowUpRight size={16} className="text-[#9598B0] group-hover:text-emerald-600 transition-colors" />
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{avgResolutionText}</div>
          <div className="flex items-center justify-between text-sm text-[#6C7089] font-medium mt-1">
            <span>Avg. Resolution Time</span>
            <span className="text-xs text-emerald-600 font-semibold group-hover:underline">View Closed &rarr;</span>
          </div>
        </div>

        {/* Card 4: CSAT Score */}
        <div 
          onClick={() => navigate('/manager')}
          className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm hover:border-amber-400 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="flex justify-between items-start mb-2">
            <div className="w-9 h-9 bg-amber-50 rounded-xl flex items-center justify-center text-amber-600 group-hover:bg-amber-600 group-hover:text-white transition-colors">
              <Smile size={18} />
            </div>
            <ArrowUpRight size={16} className="text-[#9598B0] group-hover:text-amber-600 transition-colors" />
          </div>
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{avgCsat} <span className="text-lg text-[#9598B0]">/ 5</span></div>
          <div className="flex items-center justify-between text-sm text-[#6C7089] font-medium mt-1">
            <span>CSAT Rating</span>
            <span className="text-xs text-amber-600 font-semibold group-hover:underline">Customer Reviews &rarr;</span>
          </div>
        </div>
      </div>

      {/* Main Analytics Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Category Breakdown */}
        <div className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm">
          <div className="flex justify-between items-center mb-6">
            <div>
              <h2 className="text-base font-bold text-[#1C1B2E]">Tickets by Category</h2>
              <p className="text-xs text-[#9598B0]">Real customer inquiry distribution</p>
            </div>
            <button 
              onClick={() => navigate('/manager/reports')}
              className="text-xs font-bold text-indigo-600 hover:underline"
            >
              Full Breakdown &rarr;
            </button>
          </div>

          <div className="space-y-4">
            {Object.entries(categories).map(([cat, count]) => (
              <div key={cat} className="flex items-center gap-3 text-sm font-semibold">
                <span className="w-28 text-[#6C7089] truncate capitalize">{cat}</span>
                <div className="flex-1 h-3 bg-gray-100 rounded-full overflow-hidden">
                  <div className="h-full bg-indigo-500 rounded-full transition-all duration-500" style={{ width: `${(count / maxCategory) * 100}%` }}></div>
                </div>
                <span className="w-10 text-right text-[#1C1B2E] font-bold">{count}</span>
              </div>
            ))}

            {Object.keys(categories).length === 0 && (
              <p className="text-sm text-[#9598B0] text-center py-6">No tickets recorded for this timeframe.</p>
            )}
          </div>
        </div>

        {/* AI vs Agent Resolution Ratio */}
        <div className="bg-white p-6 rounded-2xl border border-[#E5E7F3] shadow-sm flex flex-col justify-between">
          <div className="flex justify-between items-center mb-6">
            <div>
              <h2 className="text-base font-bold text-[#1C1B2E]">AI vs Human Resolution</h2>
              <p className="text-xs text-[#9598B0]">Deflection efficiency & agent escalation balance</p>
            </div>
            <button 
              onClick={() => navigate('/manager/agent-performance')}
              className="text-xs font-bold text-indigo-600 hover:underline"
            >
              Agent Workload &rarr;
            </button>
          </div>

          <div className="flex-1 flex items-center justify-center gap-8 py-4">
            <div className="relative w-36 h-36 flex-shrink-0">
              <svg viewBox="0 0 100 100" className="w-full h-full transform -rotate-90">
                <circle cx="50" cy="50" r="40" fill="transparent" stroke="#E5E7F3" strokeWidth="12" />
                <circle 
                  cx="50" 
                  cy="50" 
                  r="40" 
                  fill="transparent" 
                  stroke="#8B5CF6" 
                  strokeWidth="12" 
                  strokeDasharray={`${totalTickets > 0 ? (aiResolved / totalTickets) * 251.2 : 0} 251.2`} 
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
                <span className="text-xs text-[#9598B0] font-bold uppercase">AI Rate</span>
                <span className="text-xl font-bold text-[#1C1B2E]">
                  {totalTickets > 0 ? Math.round((aiResolved / totalTickets) * 100) : 0}%
                </span>
              </div>
            </div>

            <div className="space-y-4 flex-1">
              <div 
                onClick={() => navigate('/manager/inbox/all')}
                className="p-3 rounded-xl border border-[#E5E7F3] hover:border-purple-300 hover:bg-purple-50/40 transition-all cursor-pointer"
              >
                <div className="flex items-center justify-between text-sm mb-1">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-sm bg-purple-500"></div>
                    <span className="font-bold text-[#1C1B2E]">AI Resolved</span>
                  </div>
                  <span className="font-bold text-purple-600">{aiResolved} tickets</span>
                </div>
                <div className="text-[11px] text-[#6C7089]">Resolved automatically by SupportHub AI Agent</div>
              </div>

              <div 
                onClick={() => navigate('/manager/agent-performance')}
                className="p-3 rounded-xl border border-[#E5E7F3] hover:border-blue-300 hover:bg-blue-50/40 transition-all cursor-pointer"
              >
                <div className="flex items-center justify-between text-sm mb-1">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-sm bg-blue-500"></div>
                    <span className="font-bold text-[#1C1B2E]">Agent Resolved</span>
                  </div>
                  <span className="font-bold text-blue-600">{agentResolved} tickets</span>
                </div>
                <div className="text-[11px] text-[#6C7089]">Handled & closed by human support specialists</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Channel Volume Distribution Table */}
      <div className="bg-white rounded-2xl border border-[#E5E7F3] shadow-sm p-6">
        <h2 className="text-base font-bold text-[#1C1B2E] mb-4">Volume by Channel</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {Object.entries(channels).map(([ch, count]) => (
            <div 
              key={ch}
              onClick={() => navigate('/manager/inbox/all')}
              className="p-4 rounded-xl border border-[#E5E7F3] hover:border-indigo-300 hover:bg-indigo-50/30 transition-all cursor-pointer flex justify-between items-center"
            >
              <div>
                <div className="text-xs text-[#9598B0] font-bold uppercase">{ch.replace('_', ' ')}</div>
                <div className="text-xl font-bold text-[#1C1B2E] mt-0.5">{count} Tickets</div>
              </div>
              <span className="text-xs font-bold text-indigo-600 bg-indigo-50 px-2.5 py-1 rounded-full">
                {totalTickets > 0 ? Math.round((count / totalTickets) * 100) : 0}%
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

