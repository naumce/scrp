import { get, post } from "@/api/client"
import type { EnrichmentResult, EnrichmentStatus } from "@/types/enrichment"

export function startEnrichment(
  projectId: number,
  businessIds: number[],
): Promise<{ project_id: number; total: number; message: string }> {
  return post("/api/enrichment/start", {
    project_id: projectId,
    business_ids: businessIds,
  })
}

export function getEnrichmentStatus(
  projectId: number,
): Promise<EnrichmentStatus & { running: boolean }> {
  return get(`/api/enrichment/status/${projectId}`)
}

export function getEnrichmentResults(
  projectId: number,
): Promise<EnrichmentResult[]> {
  return get(`/api/enrichment/results/${projectId}`)
}
