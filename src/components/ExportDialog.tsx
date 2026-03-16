import { FileSpreadsheet, FileText, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { useExportBusinesses } from "@/hooks/useExport"

interface ExportDialogProps {
  projectId: number
  selectedBusinessIds: number[]
  allBusinessIds: number[]
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function ExportDialog({
  projectId,
  selectedBusinessIds,
  allBusinessIds,
  open,
  onOpenChange,
}: ExportDialogProps) {
  const exportMutation = useExportBusinesses()

  const count =
    selectedBusinessIds.length > 0
      ? selectedBusinessIds.length
      : allBusinessIds.length

  const businessIds =
    selectedBusinessIds.length > 0 ? selectedBusinessIds : undefined

  const handleExport = (format: "csv" | "excel") => {
    exportMutation.mutate(
      {
        project_id: projectId,
        format,
        business_ids: businessIds,
      },
      {
        onSuccess: () => onOpenChange(false),
      },
    )
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Export Businesses</DialogTitle>
        </DialogHeader>

        <p className="text-sm text-muted-foreground">
          {selectedBusinessIds.length > 0
            ? `Export ${count} selected businesses`
            : `Export all ${count} businesses`}
        </p>

        {exportMutation.isError && (
          <div className="rounded-md border border-destructive/50 bg-destructive/10 p-2 text-sm text-destructive">
            {exportMutation.error?.message ?? "Export failed"}
          </div>
        )}

        <div className="flex gap-3">
          <Button
            variant="outline"
            className="flex-1 gap-2"
            onClick={() => handleExport("csv")}
            disabled={exportMutation.isPending}
          >
            {exportMutation.isPending ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <FileText className="h-4 w-4" />
            )}
            CSV
          </Button>
          <Button
            variant="outline"
            className="flex-1 gap-2"
            onClick={() => handleExport("excel")}
            disabled={exportMutation.isPending}
          >
            {exportMutation.isPending ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <FileSpreadsheet className="h-4 w-4" />
            )}
            Excel
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}
