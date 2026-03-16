import { SIDECAR_BASE_URL } from "@/lib/constants"
import { ApiError } from "@/api/client"

export interface ExportParams {
  project_id: number
  format: "csv" | "excel"
  business_ids?: number[]
}

export async function exportBusinesses(params: ExportParams): Promise<Blob> {
  const url = `${SIDECAR_BASE_URL}/api/export`

  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  })

  if (!response.ok) {
    throw new ApiError(
      `Export failed: ${response.statusText}`,
      response.status,
    )
  }

  // If response is JSON, it's an error envelope
  const contentType = response.headers.get("content-type") ?? ""
  if (contentType.includes("application/json")) {
    const body = await response.json()
    throw new ApiError(body.error ?? "Export failed")
  }

  return response.blob()
}
