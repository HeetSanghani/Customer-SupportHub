/**
 * Returns the correct WebSocket base URL for the current environment.
 *
 * - Development (Vite proxy): uses window.location.host so the dev proxy handles /ws/*
 * - Production (split deploy): uses VITE_API_URL (the Render backend URL) converted to wss://
 */
export function getWsBase() {
  if (import.meta.env.VITE_API_URL) {
    // e.g. "https://supporthub-backend.onrender.com" → "wss://supporthub-backend.onrender.com"
    return import.meta.env.VITE_API_URL.replace(/^http/, 'ws')
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
