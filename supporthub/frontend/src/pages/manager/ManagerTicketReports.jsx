import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { ticketsApi } from '../../api/tickets'
import { Download, FileText, Search, Filter, ArrowUpRight, Calendar, RotateCcw } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { parseUTCDate, formatDate, formatDateTime } from '../../utils/dateUtils'

export default function ManagerTicketReports() {
  const navigate = useNavigate()
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [presetFilter, setPresetFilter] = useState('all') // 'all' | 'today' | '7d' | '30d' | 'custom'

  const { data: tickets = [], isLoading } = useQuery({
    queryKey: ['tickets', 'all'],
    queryFn: async () => (await ticketsApi.list()).data
  })

  if (isLoading) {
    return (
      <div className="p-8 flex justify-center items-center h-full">
        <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></div>
      </div>
    )
  }

  // Handle Preset Date selection
  const handlePresetSelect = (preset) => {
    setPresetFilter(preset)
    const now = new Date()
    
    if (preset === 'all') {
      setStartDate('')
      setEndDate('')
    } else if (preset === 'today') {
      const todayStr = now.toISOString().split('T')[0]
      setStartDate(todayStr)
      setEndDate(todayStr)
    } else if (preset === '7d') {
      const sevenDaysAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
      setStartDate(sevenDaysAgo.toISOString().split('T')[0])
      setEndDate(now.toISOString().split('T')[0])
    } else if (preset === '30d') {
      const thirtyDaysAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000)
      setStartDate(thirtyDaysAgo.toISOString().split('T')[0])
      setEndDate(now.toISOString().split('T')[0])
    }
  }

  const handleCustomDateChange = (start, end) => {
    setPresetFilter('custom')
    if (start !== undefined) setStartDate(start)
    if (end !== undefined) setEndDate(end)
  }

  const resetDateFilters = () => {
    setPresetFilter('all')
    setStartDate('')
    setEndDate('')
  }

  // Filter tickets by search, status, AND custom date range
  const filteredTickets = tickets.filter(t => {
    // 1. Search Filter
    const matchesSearch = (t.subject || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
                          (t.ref || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
                          (t.category || '').toLowerCase().includes(searchTerm.toLowerCase())
    if (!matchesSearch) return false

    // 2. Status Filter
    if (statusFilter === 'active' && (t.status === 'resolved' || t.status === 'closed')) return false
    if (statusFilter === 'closed' && t.status !== 'resolved' && t.status !== 'closed') return false
    if (statusFilter === 'escalated' && t.status !== 'escalated' && t.priority !== 'urgent') return false

    // 3. Custom Date Range Filter
    if (t.created_at) {
      const ticketDate = parseUTCDate(t.created_at)
      if (startDate) {
        const start = new Date(startDate)
        start.setHours(0, 0, 0, 0)
        if (ticketDate < start) return false
      }
      if (endDate) {
        const end = new Date(endDate)
        end.setHours(23, 59, 59, 999)
        if (ticketDate > end) return false
      }
    }

    return true
  })

  const totalCount = filteredTickets.length
  const resolvedCount = filteredTickets.filter(t => t.status === 'resolved' || t.status === 'closed').length
  const activeCount = filteredTickets.filter(t => t.status !== 'resolved' && t.status !== 'closed').length
  const resolutionRate = totalCount > 0 ? Math.round((resolvedCount / totalCount) * 100) : 0

  // Export CSV Handler
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
    link.setAttribute('download', `ticket_report_${startDate || 'all'}_to_${endDate || 'all'}.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  // Export PDF / Print Handler
  const handleExportPDF = () => {
    window.print()
  }

  const getStatusBadge = (status) => {
    switch (status) {
      case 'resolved':
      case 'closed':
        return <span className="bg-emerald-50 text-emerald-600 border border-emerald-200 px-2.5 py-0.5 rounded-full text-xs font-bold capitalize">● Resolved</span>
      case 'open':
        return <span className="bg-indigo-50 text-indigo-600 border border-indigo-200 px-2.5 py-0.5 rounded-full text-xs font-bold capitalize">● Open</span>
      case 'waiting':
      case 'pending':
        return <span className="bg-amber-50 text-amber-600 border border-amber-200 px-2.5 py-0.5 rounded-full text-xs font-bold capitalize">● Waiting</span>
      case 'escalated':
        return <span className="bg-rose-50 text-rose-600 border border-rose-200 px-2.5 py-0.5 rounded-full text-xs font-bold capitalize">● Escalated</span>
      default:
        return <span className="bg-gray-50 text-gray-600 border border-gray-200 px-2.5 py-0.5 rounded-full text-xs font-bold capitalize">{status}</span>
    }
  }

  return (
    <div className="flex-1 overflow-auto bg-[#F6F7FC] p-8 text-[#1C1B2E]">
      {/* Header Bar */}
      <div className="mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold font-['Plus_Jakarta_Sans']">Ticket Reports</h1>
          <p className="text-[#6C7089] text-sm mt-0.5">Generate, filter by custom date ranges, and export detailed ticket performance reports.</p>
        </div>
        <div className="flex items-center gap-2">
          <button 
            onClick={handleExportCSV}
            className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-sm"
          >
            <Download size={15} /> Export CSV
          </button>
          <button 
            onClick={handleExportPDF}
            className="flex items-center gap-2 bg-white hover:bg-gray-50 border border-[#E5E7F3] text-[#1C1B2E] px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-sm"
          >
            <FileText size={15} /> Export PDF
          </button>
        </div>
      </div>

      {/* Dynamic Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div 
          onClick={() => navigate('/manager/inbox/all')}
          className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm hover:border-indigo-400 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{totalCount}</div>
          <div className="flex items-center justify-between text-sm text-[#6C7089] font-medium mt-1">
            <span>Filtered Created</span>
            <span className="text-xs text-indigo-600 font-semibold group-hover:underline">View All &rarr;</span>
          </div>
        </div>
        <div 
          onClick={() => navigate('/manager/inbox/closed')}
          className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm hover:border-emerald-400 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{resolvedCount}</div>
          <div className="flex items-center justify-between text-sm text-[#6C7089] font-medium mt-1">
            <span>Filtered Resolved ({resolutionRate}%)</span>
            <span className="text-xs text-emerald-600 font-semibold group-hover:underline">View Closed &rarr;</span>
          </div>
        </div>
        <div 
          onClick={() => navigate('/manager/inbox/active')}
          className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm hover:border-amber-400 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="text-3xl font-bold font-['Plus_Jakarta_Sans']">{activeCount}</div>
          <div className="flex items-center justify-between text-sm text-[#6C7089] font-medium mt-1">
            <span>Active In Progress</span>
            <span className="text-xs text-amber-600 font-semibold group-hover:underline">View Active &rarr;</span>
          </div>
        </div>
      </div>

      {/* Date Range Picker & Filter Bar */}
      <div className="bg-white p-5 rounded-2xl border border-[#E5E7F3] shadow-sm mb-6 space-y-4">
        {/* Row 1: Search & Quick Date Range Presets */}
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          {/* Search Box */}
          <div className="relative w-full lg:w-80">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-[#9598B0]" size={16} />
            <input
              type="text"
              placeholder="Search ref ID, subject, or category..."
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              className="w-full bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl pl-9 pr-4 py-2 text-xs outline-none focus:border-indigo-500 transition-colors"
            />
          </div>

          {/* Quick Date Range Presets */}
          <div className="flex items-center gap-2 overflow-x-auto pb-1 lg:pb-0">
            <span className="text-xs font-bold text-[#9598B0] flex items-center gap-1 shrink-0">
              <Calendar size={14} /> Quick Range:
            </span>
            <div className="flex bg-[#F6F7FC] p-1 rounded-xl border border-[#E5E7F3] shrink-0">
              <button
                onClick={() => handlePresetSelect('all')}
                className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${presetFilter === 'all' ? 'bg-indigo-600 text-white' : 'text-[#6C7089] hover:text-[#1C1B2E]'}`}
              >
                All Time
              </button>
              <button
                onClick={() => handlePresetSelect('today')}
                className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${presetFilter === 'today' ? 'bg-indigo-600 text-white' : 'text-[#6C7089] hover:text-[#1C1B2E]'}`}
              >
                Today
              </button>
              <button
                onClick={() => handlePresetSelect('7d')}
                className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${presetFilter === '7d' ? 'bg-indigo-600 text-white' : 'text-[#6C7089] hover:text-[#1C1B2E]'}`}
              >
                Last 7 Days
              </button>
              <button
                onClick={() => handlePresetSelect('30d')}
                className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${presetFilter === '30d' ? 'bg-indigo-600 text-white' : 'text-[#6C7089] hover:text-[#1C1B2E]'}`}
              >
                Last 30 Days
              </button>
            </div>
          </div>
        </div>

        {/* Row 2: Custom Start / End Date Pickers & Status Filters */}
        <div className="pt-3 border-t border-[#E5E7F3] flex flex-col md:flex-row md:items-center justify-between gap-4">
          {/* Custom Date Pickers */}
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold text-[#6C7089]">From:</span>
              <input
                type="date"
                value={startDate}
                onChange={e => handleCustomDateChange(e.target.value, undefined)}
                className="bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl px-3 py-1.5 text-xs text-[#1C1B2E] font-medium outline-none focus:border-indigo-500 transition-colors"
              />
            </div>

            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold text-[#6C7089]">To:</span>
              <input
                type="date"
                value={endDate}
                onChange={e => handleCustomDateChange(undefined, e.target.value)}
                className="bg-[#F6F7FC] border border-[#E5E7F3] rounded-xl px-3 py-1.5 text-xs text-[#1C1B2E] font-medium outline-none focus:border-indigo-500 transition-colors"
              />
            </div>

            {(startDate || endDate) && (
              <button
                onClick={resetDateFilters}
                className="flex items-center gap-1 text-xs font-bold text-rose-600 hover:bg-rose-50 px-2.5 py-1.5 rounded-lg transition-colors"
                title="Reset Date Filters"
              >
                <RotateCcw size={12} /> Reset
              </button>
            )}
          </div>

          {/* Status Tabs */}
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-[#9598B0] flex items-center gap-1">
              <Filter size={14} /> Status:
            </span>
            <div className="flex bg-[#F6F7FC] p-1 rounded-xl border border-[#E5E7F3]">
              <button
                onClick={() => setStatusFilter('all')}
                className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${statusFilter === 'all' ? 'bg-indigo-600 text-white' : 'text-[#6C7089] hover:text-[#1C1B2E]'}`}
              >
                All
              </button>
              <button
                onClick={() => setStatusFilter('active')}
                className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${statusFilter === 'active' ? 'bg-indigo-600 text-white' : 'text-[#6C7089] hover:text-[#1C1B2E]'}`}
              >
                Active
              </button>
              <button
                onClick={() => setStatusFilter('closed')}
                className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${statusFilter === 'closed' ? 'bg-indigo-600 text-white' : 'text-[#6C7089] hover:text-[#1C1B2E]'}`}
              >
                Closed
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Ticket Table */}
      <div className="bg-white rounded-2xl border border-[#E5E7F3] shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-[#6C7089]">
            <thead className="text-xs uppercase font-bold text-[#9598B0] border-b border-[#E5E7F3] bg-gray-50/50">
              <tr>
                <th className="px-6 py-4">Ticket</th>
                <th className="px-6 py-4">Category</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4">Priority</th>
                <th className="px-6 py-4">Created Date</th>
                <th className="px-6 py-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E5E7F3]">
              {filteredTickets.map(ticket => (
                <tr 
                  key={ticket.id} 
                  onClick={() => navigate(`/manager/tickets/${ticket.id}`)}
                  className="hover:bg-indigo-50/30 transition-colors cursor-pointer group"
                >
                  <td className="px-6 py-4">
                    <div className="font-bold text-[#1C1B2E] group-hover:text-indigo-600 transition-colors">{ticket.subject}</div>
                    <div className="text-[10px] font-mono text-[#9598B0]">{ticket.ref}</div>
                  </td>
                  <td className="px-6 py-4 capitalize font-medium">{ticket.category}</td>
                  <td className="px-6 py-4">{getStatusBadge(ticket.status)}</td>
                  <td className="px-6 py-4 capitalize font-semibold">
                    <span className={ticket.priority === 'urgent' ? 'text-red-600 font-bold' : ticket.priority === 'high' ? 'text-amber-600' : 'text-gray-600'}>
                      {ticket.priority || 'medium'}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-xs font-mono text-[#1C1B2E]">
                    {ticket.created_at ? formatDate(ticket.created_at) : 'N/A'}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <span className="text-xs font-bold text-indigo-600 opacity-0 group-hover:opacity-100 transition-opacity inline-flex items-center gap-0.5">
                      Open Ticket <ArrowUpRight size={14} />
                    </span>
                  </td>
                </tr>
              ))}

              {filteredTickets.length === 0 && (
                <tr>
                  <td colSpan="6" className="px-6 py-12 text-center text-[#9598B0] text-xs">
                    No tickets match the selected date range and filter criteria.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}


