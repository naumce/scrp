import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"
import { getSettings, updateSettings, type AppSettings } from "@/api/settings"

const SETTINGS_KEY = ["settings"] as const

export function useSettings() {
  return useQuery({
    queryKey: SETTINGS_KEY,
    queryFn: getSettings,
  })
}

export function useUpdateSettings() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: Partial<AppSettings>) => updateSettings(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: SETTINGS_KEY })
      toast.success("Settings saved")
    },
    onError: (error) => {
      toast.error(`Failed to save settings: ${error.message}`)
    },
  })
}
