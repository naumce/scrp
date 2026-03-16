import { describe, it, expect } from "vitest"
import {
  SIDECAR_PORT,
  API_BASE_URL,
  IS_DESKTOP,
  HEALTH_POLL_INTERVAL_MS,
  ENRICHMENT_POLL_INTERVAL_MS,
} from "./constants"

describe("constants", () => {
  it("has correct sidecar port", () => {
    expect(SIDECAR_PORT).toBe(8742)
  })

  it("API_BASE_URL is a string", () => {
    expect(typeof API_BASE_URL).toBe("string")
  })

  it("IS_DESKTOP is false in test environment", () => {
    expect(IS_DESKTOP).toBe(false)
  })

  it("has positive poll intervals", () => {
    expect(HEALTH_POLL_INTERVAL_MS).toBeGreaterThan(0)
    expect(ENRICHMENT_POLL_INTERVAL_MS).toBeGreaterThan(0)
  })
})
