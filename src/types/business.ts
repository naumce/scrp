export interface Business {
  id: number
  project_id: number
  place_id: string
  name: string
  address: string
  phone: string
  website: string
  rating: number | null
  reviews: number | null
  category: string
  lat: number
  lon: number
  maps_url: string
  is_favorite: boolean
  notes: string
  created_at: string
}

export interface ProjectStats {
  total: number
  with_website: number
  with_phone: number
  favorites: number
  enriched: number
  with_emails: number
}

/** Business row with enrichment data merged in for display */
export interface BusinessWithEnrichment extends Business {
  enrichment_emails: string[]
  enrichment_phones: string[]
  enrichment_social: string[]
  enrichment_status: "pending" | "success" | "failed" | null
}
