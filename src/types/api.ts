export interface ApiResponse<T> {
  success: boolean
  data: T | null
  error: string | null
  meta: Record<string, unknown> | null
}
