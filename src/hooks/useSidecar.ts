import { useEffect, useRef } from "react"
import { fetchHealth } from "@/api/client"
import { useAppStore } from "@/store/appStore"
import { HEALTH_POLL_INTERVAL_MS } from "@/lib/constants"

export function useSidecar() {
  const sidecarReady = useAppStore((s) => s.sidecarReady)
  const setSidecarReady = useAppStore((s) => s.setSidecarReady)
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null)

  useEffect(() => {
    if (sidecarReady) return

    const checkHealth = async () => {
      const healthy = await fetchHealth()
      if (healthy) {
        setSidecarReady(true)
        if (intervalRef.current) {
          clearInterval(intervalRef.current)
          intervalRef.current = null
        }
      }
    }

    checkHealth()
    intervalRef.current = setInterval(checkHealth, HEALTH_POLL_INTERVAL_MS)

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }
  }, [sidecarReady, setSidecarReady])

  return sidecarReady
}
