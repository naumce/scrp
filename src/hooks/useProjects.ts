import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"
import {
  getProjects,
  createProject,
  deleteProject,
} from "@/api/projects"
import type { CreateProjectInput } from "@/types/project"

const PROJECTS_KEY = ["projects"] as const

export function useProjects() {
  return useQuery({
    queryKey: PROJECTS_KEY,
    queryFn: getProjects,
  })
}

export function useCreateProject() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: CreateProjectInput) => createProject(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: PROJECTS_KEY })
      toast.success("Project created")
    },
    onError: (error) => {
      toast.error(`Failed to create project: ${error.message}`)
    },
  })
}

export function useDeleteProject() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => deleteProject(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: PROJECTS_KEY })
      toast.success("Project deleted")
    },
    onError: (error) => {
      toast.error(`Failed to delete project: ${error.message}`)
    },
  })
}
