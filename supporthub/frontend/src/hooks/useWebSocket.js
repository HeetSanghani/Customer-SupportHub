import { useEffect, useRef, useCallback } from 'react'
import { useAuthStore } from '../store/authStore'
import { buildTicketWsUrl } from '../utils/wsUrl'

export function useWebSocket(ticketId, onMessage) {
  const wsRef = useRef(null)
  const token = useAuthStore((s) => s.token)
  const retryRef = useRef(0)
  const maxRetries = 5

  const connect = useCallback(() => {
    if (!ticketId || !token) return

    const url = buildTicketWsUrl(ticketId, token)
    const ws = new WebSocket(url)
    wsRef.current = ws

    ws.onopen = () => {
      retryRef.current = 0
      console.log('[WS] Connected to ticket', ticketId)
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        onMessage(data)
      } catch {}
    }

    ws.onclose = (e) => {
      if (e.code !== 1000 && retryRef.current < maxRetries) {
        const delay = Math.min(1000 * 2 ** retryRef.current, 30000)
        retryRef.current++
        console.log(`[WS] Reconnecting in ${delay}ms (attempt ${retryRef.current})`)
        setTimeout(connect, delay)
      }
    }

    ws.onerror = () => ws.close()
  }, [ticketId, token, onMessage])

  useEffect(() => {
    connect()
    return () => {
      wsRef.current?.close(1000, 'unmount')
    }
  }, [connect])

  const send = useCallback((data) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data))
    }
  }, [])

  return { send }
}
