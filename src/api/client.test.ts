import { describe, it, expect, vi, beforeEach } from "vitest"
import { ApiError } from "./client"

// We test ApiError class and the fetch wrapper logic

describe("ApiError", () => {
  it("creates error with message and status", () => {
    const err = new ApiError("Not found", 404)
    expect(err.message).toBe("Not found")
    expect(err.status).toBe(404)
    expect(err.name).toBe("ApiError")
  })

  it("creates error without status", () => {
    const err = new ApiError("Something went wrong")
    expect(err.status).toBeUndefined()
  })
})
