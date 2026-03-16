import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"
import {
  getBusinesses,
  getProjectStats,
  searchPlaces,
  toggleFavorite,
  deleteBusiness,
  bulkDeleteBusinesses,
  updateBusinessNotes,
} from "@/api/businesses"

const businessesKey = (projectId: number) =>
  ["businesses", projectId] as const

const statsKey = (projectId: number) =>
  ["project-stats", projectId] as const

export function useBusinesses(projectId: number) {
  return useQuery({
    queryKey: businessesKey(projectId),
    queryFn: () => getBusinesses(projectId),
    enabled: projectId > 0,
  })
}

export function useProjectStats(projectId: number) {
  return useQuery({
    queryKey: statsKey(projectId),
    queryFn: () => getProjectStats(projectId),
    enabled: projectId > 0,
  })
}

export function useSearchPlaces(projectId: number) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: searchPlaces,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: businessesKey(projectId) })
      queryClient.invalidateQueries({ queryKey: statsKey(projectId) })
      toast.success(`Found ${Array.isArray(data) ? data.length : 0} businesses`)
    },
    onError: (error) => {
      toast.error(`Search failed: ${error.message}`)
    },
  })
}

export function useToggleFavorite(projectId: number) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (businessId: number) => toggleFavorite(businessId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: businessesKey(projectId) })
      queryClient.invalidateQueries({ queryKey: statsKey(projectId) })
    },
  })
}

export function useDeleteBusiness(projectId: number) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (businessId: number) => deleteBusiness(businessId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: businessesKey(projectId) })
      queryClient.invalidateQueries({ queryKey: statsKey(projectId) })
      toast.success("Business deleted")
    },
  })
}

export function useBulkDelete(projectId: number) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (ids: number[]) => bulkDeleteBusinesses(ids),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: businessesKey(projectId) })
      queryClient.invalidateQueries({ queryKey: statsKey(projectId) })
      toast.success(`Deleted ${data.deleted} businesses`)
    },
    onError: (error) => {
      toast.error(`Delete failed: ${error.message}`)
    },
  })
}

export function useUpdateNotes(projectId: number) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, notes }: { id: number; notes: string }) =>
      updateBusinessNotes(id, notes),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: businessesKey(projectId) })
    },
  })
}
