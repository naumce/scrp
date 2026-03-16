import { get, post, put, del as del_ } from "@/api/client"
import type { Project, CreateProjectInput } from "@/types/project"

export function getProjects(): Promise<Project[]> {
  return get<Project[]>("/api/projects/")
}

export function getProject(id: number): Promise<Project> {
  return get<Project>(`/api/projects/${id}`)
}

export function createProject(data: CreateProjectInput): Promise<Project> {
  return post<Project>("/api/projects/", data)
}

export function updateProject(
  id: number,
  data: Partial<CreateProjectInput>,
): Promise<Project> {
  return put<Project>(`/api/projects/${id}`, data)
}

export function deleteProject(id: number): Promise<{ deleted: boolean }> {
  return del_<{ deleted: boolean }>(`/api/projects/${id}`)
}
