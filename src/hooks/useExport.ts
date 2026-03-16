import { useMutation } from "@tanstack/react-query"
import { toast } from "sonner"
import { exportBusinesses, type ExportParams } from "@/api/exports"

function downloadBlob(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob)
  const a = document.createElement("a")
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  a.remove()
  URL.revokeObjectURL(url)
}

export function useExportBusinesses() {
  return useMutation({
    mutationFn: async (params: ExportParams) => {
      const blob = await exportBusinesses(params)
      const ext = params.format === "csv" ? "csv" : "xlsx"
      downloadBlob(blob, `businesses.${ext}`)
    },
    onSuccess: () => {
      toast.success("Export downloaded")
    },
    onError: (error) => {
      toast.error(`Export failed: ${error.message}`)
    },
  })
}
