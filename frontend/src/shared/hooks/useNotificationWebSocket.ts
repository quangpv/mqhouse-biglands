import { useEffect, useRef } from "react"
import { useQueryClient } from "@tanstack/react-query"
import { useAuthStore } from "@/shared/context/auth-store"
import { notificationQueries } from "@/data/queries/notification.queries"

const WS_BASE = `${window.location.protocol === "https:" ? "wss:" : "ws:"}//${window.location.host}/api/v1/ws`

export function useNotificationWebSocket() {
  const token = useAuthStore((s) => s.token)
  const user = useAuthStore((s) => s.user)
  const queryClient = useQueryClient()
  const wsRef = useRef<WebSocket | null>(null)
  const timerRef = useRef<ReturnType<typeof setTimeout>>()

  useEffect(() => {
    if (!token || !user) return

    let reconnectDelay = 1000

    function connect() {
      const ws = new WebSocket(`${WS_BASE}?token=${token}`)
      wsRef.current = ws

      ws.onopen = () => {
        console.log("[WS] connected")
        reconnectDelay = 1000
      }

      ws.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data)
          if (msg.type === "notification_created") {
            queryClient.invalidateQueries({ queryKey: notificationQueries.lists() })
            queryClient.invalidateQueries({ queryKey: notificationQueries.unreadCount() })
          }
        } catch {
          // ignore parse errors
        }
      }

      ws.onclose = () => {
        wsRef.current = null
        timerRef.current = setTimeout(connect, reconnectDelay)
        reconnectDelay = Math.min(reconnectDelay * 2, 30000)
      }

      ws.onerror = (err) => {
        console.error("[WS] connection error", err)
        ws.close()
      }
    }

    connect()

    return () => {
      clearTimeout(timerRef.current)
      wsRef.current?.close()
    }
  }, [token, user, queryClient])
}
