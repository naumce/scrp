export interface EnrichmentResult {
  id: number
  business_id: number
  emails: string[]
  phones: string[]
  contact_page: string
  social_links: string[]
  status: "pending" | "success" | "failed"
  error_message: string
  created_at: string
}

export interface EnrichmentStatus {
  project_id: number
  total: number
  completed: number
  failed: number
  in_progress: number
}
