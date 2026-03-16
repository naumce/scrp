import { get, put } from "@/api/client"

export interface AppSettings {
  default_radius: string
  default_max_results: string
  scrape_timeout: string
  scrape_concurrency: string
}

export function getSettings(): Promise<AppSettings> {
  return get("/api/settings")
}

export function updateSettings(
  data: Partial<AppSettings>,
): Promise<AppSettings> {
  return put("/api/settings", data)
}
