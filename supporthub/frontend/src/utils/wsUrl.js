/**
 * Returns the correct WebSocket base URL for the current environment.
 *
 * - Development (Vite proxy): uses window.location.host so the dev proxy handles /ws/*
 * - Production (split deploy): uses VITE_API_URL (the Render backend URL) converted to wss://
 */
export function getWsBase() {
  let rawApiUrl = (import.meta.env.VITE_API_URL || '').trim()
  if (rawApiUrl && !rawApiUrl.includes('.')) {
    rawApiUrl = `${rawApiUrl}.onrender.com`
  }
  if (rawApiUrl) {
    const withProtocol = rawApiUrl.startsWith('http') ? rawApiUrl : `https://${rawApiUrl}`
    return withProtocol.replace(/\/+$/, '').replace(/^http/, 'ws')
  }
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  return `${protocol}//${window.location.host}`
}

/**
 * Builds a full WebSocket URL for a chat ticket.
 * @param {string|number} ticketId
 * @param {string} token  JWT access token
 */
export function buildTicketWsUrl(ticketId, token) {
  return `${getWsBase()}/ws/chat/${ticketId}?token=${token}`
}
