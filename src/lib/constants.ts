export const SIDECAR_PORT = 8742

const isTauri = Boolean(
  globalThis.window !== undefined &&
    (globalThis as Record<string, unknown>).__TAURI_INTERNALS__,
)

export const API_BASE_URL: string =
  import.meta.env.VITE_API_URL ??
  (isTauri ? `http://127.0.0.1:${SIDECAR_PORT}` : "")

/** @deprecated Use API_BASE_URL instead */
export const SIDECAR_BASE_URL = API_BASE_URL

export const IS_DESKTOP = isTauri

export const HEALTH_POLL_INTERVAL_MS = 1000
export const ENRICHMENT_POLL_INTERVAL_MS = 2000
