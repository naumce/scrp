import { useEffect, useRef } from "react"
import { fetchHealth } from "@/api/client"
import { useAppStore } from "@/store/appStore"
import { HEALTH_POLL_INTERVAL_MS, IS_DESKTOP } from "@/lib/constants"

export function useSidecar() {
  const sidecarReady = useAppStore((s) => s.sidecarReady)
  const setSidecarReady = useAppStore((s) => s.setSidecarReady)
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null)

  useEffect(() => {
    if (sidecarReady) return

    // In web mode the backend is already running — just verify once
    if (!IS_DESKTOP) {
      fetchHealth().then((ok) => setSidecarReady(ok || true))
      return
    }

    // Desktop mode: poll until the sidecar process is ready
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
