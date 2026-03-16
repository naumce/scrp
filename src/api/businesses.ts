import { get, post, patch, del as del_ } from "@/api/client"
import type { Business, ProjectStats } from "@/types/business"

interface SearchRequest {
  project_id: number
  keyword: string
  location: string
  radius: number
  max_results: number
}

export function getBusinesses(projectId: number): Promise<Business[]> {
  return get<Business[]>(`/api/businesses/?project_id=${projectId}`)
}

export function getBusiness(id: number): Promise<Business> {
  return get<Business>(`/api/businesses/${id}`)
}

export function getProjectStats(projectId: number): Promise<ProjectStats> {
  return get<ProjectStats>(`/api/businesses/stats?project_id=${projectId}`)
}

export function searchPlaces(data: SearchRequest): Promise<Business[]> {
  return post<Business[]>("/api/search/places", data)
}

export function toggleFavorite(id: number): Promise<Business> {
  return patch<Business>(`/api/businesses/${id}/favorite`)
}

export function updateBusinessNotes(
  id: number,
  notes: string,
): Promise<Business> {
  return patch<Business>(`/api/businesses/${id}/notes`, { notes })
}

export function deleteBusiness(id: number): Promise<{ deleted: boolean }> {
  return del_<{ deleted: boolean }>(`/api/businesses/${id}`)
}

export function bulkDeleteBusinesses(
  ids: number[],
): Promise<{ deleted: number }> {
  return post<{ deleted: number }>("/api/businesses/bulk-delete", { ids })
}
