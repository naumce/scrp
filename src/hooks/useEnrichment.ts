import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"
import {
  startEnrichment,
  getEnrichmentStatus,
  getEnrichmentResults,
} from "@/api/enrichment"
import { ENRICHMENT_POLL_INTERVAL_MS } from "@/lib/constants"

const statusKey = (projectId: number) =>
  ["enrichment-status", projectId] as const
const resultsKey = (projectId: number) =>
  ["enrichment-results", projectId] as const

export function useEnrichmentStatus(projectId: number) {
  return useQuery({
    queryKey: statusKey(projectId),
    queryFn: () => getEnrichmentStatus(projectId),
    enabled: projectId > 0,
    refetchInterval: (query) => {
      const data = query.state.data
      if (data && data.running) {
        return ENRICHMENT_POLL_INTERVAL_MS
      }
      return false
    },
  })
}

export function useEnrichmentResults(projectId: number) {
  return useQuery({
    queryKey: resultsKey(projectId),
    queryFn: () => getEnrichmentResults(projectId),
    enabled: projectId > 0,
  })
}

export function useStartEnrichment(projectId: number) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (businessIds: number[]) =>
      startEnrichment(projectId, businessIds),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: statusKey(projectId) })
      queryClient.invalidateQueries({ queryKey: resultsKey(projectId) })
      toast.success("Enrichment started")
    },
    onError: (error) => {
      toast.error(`Enrichment failed: ${error.message}`)
    },
  })
}
