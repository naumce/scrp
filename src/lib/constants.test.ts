import { describe, it, expect } from "vitest"
import {
  SIDECAR_PORT,
  SIDECAR_BASE_URL,
  HEALTH_POLL_INTERVAL_MS,
  ENRICHMENT_POLL_INTERVAL_MS,
} from "./constants"

describe("constants", () => {
  it("has correct sidecar port", () => {
    expect(SIDECAR_PORT).toBe(8742)
  })

  it("builds base URL from port", () => {
    expect(SIDECAR_BASE_URL).toBe(`http://127.0.0.1:${SIDECAR_PORT}`)
  })

  it("has positive poll intervals", () => {
    expect(HEALTH_POLL_INTERVAL_MS).toBeGreaterThan(0)
    expect(ENRICHMENT_POLL_INTERVAL_MS).toBeGreaterThan(0)
  })
})
