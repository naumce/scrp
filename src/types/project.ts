export interface Project {
  id: number
  name: string
  keyword: string
  location: string
  radius: number
  max_results: number
  notes: string
  created_at: string
}

export interface CreateProjectInput {
  name: string
  keyword: string
  location: string
  radius: number
  max_results: number
  notes?: string
}
