import { SIDECAR_BASE_URL } from "@/lib/constants"
import type { ApiResponse } from "@/types/api"

export class ApiError extends Error {
  status?: number

  constructor(message: string, status?: number) {
    super(message)
    this.name = "ApiError"
    this.status = status
  }
}

async function request<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const url = `${SIDECAR_BASE_URL}${path}`

  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  })

  if (!response.ok) {
    throw new ApiError(
      `Request failed: ${response.statusText}`,
      response.status,
    )
  }

  const body: ApiResponse<T> = await response.json()

  if (!body.success) {
    throw new ApiError(body.error ?? "Unknown error")
  }

  return body.data as T
}

export function get<T>(path: string): Promise<T> {
  return request<T>(path)
}

export function post<T>(path: string, data?: unknown): Promise<T> {
  return request<T>(path, {
    method: "POST",
    body: data ? JSON.stringify(data) : undefined,
  })
}

export function put<T>(path: string, data?: unknown): Promise<T> {
  return request<T>(path, {
    method: "PUT",
    body: data ? JSON.stringify(data) : undefined,
  })
}

export function patch<T>(path: string, data?: unknown): Promise<T> {
  return request<T>(path, {
    method: "PATCH",
    body: data ? JSON.stringify(data) : undefined,
  })
}

export function del<T>(path: string): Promise<T> {
  return request<T>(path, { method: "DELETE" })
}

export async function fetchHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${SIDECAR_BASE_URL}/health`)
    return response.ok
  } catch {
    return false
  }
}
