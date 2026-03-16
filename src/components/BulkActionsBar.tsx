import { Trash2, Zap, Download, X } from "lucide-react"
import { Button } from "@/components/ui/button"

interface BulkActionsBarProps {
  selectedCount: number
  onDelete: () => void
  onEnrich: () => void
  onExport: () => void
  onClearSelection: () => void
  isDeleting?: boolean
}

export function BulkActionsBar({
  selectedCount,
  onDelete,
  onEnrich,
  onExport,
  onClearSelection,
  isDeleting,
}: BulkActionsBarProps) {
  if (selectedCount === 0) return null

  return (
    <div className="sticky bottom-4 z-40 flex items-center justify-between gap-3 rounded-lg border bg-background/95 px-4 py-3 shadow-lg backdrop-blur-sm">
      <div className="flex items-center gap-2">
        <span className="text-sm font-medium">
          {selectedCount} selected
        </span>
        <Button variant="ghost" size="sm" onClick={onClearSelection}>
          <X className="mr-1 h-3 w-3" />
          Clear
        </Button>
      </div>
      <div className="flex items-center gap-2">
        <Button variant="outline" size="sm" className="gap-1.5" onClick={onEnrich}>
          <Zap className="h-3.5 w-3.5" />
          Enrich
        </Button>
        <Button variant="outline" size="sm" className="gap-1.5" onClick={onExport}>
          <Download className="h-3.5 w-3.5" />
          Export
        </Button>
        <Button
          variant="destructive"
          size="sm"
          className="gap-1.5"
          onClick={onDelete}
          disabled={isDeleting}
        >
          <Trash2 className="h-3.5 w-3.5" />
          Delete
        </Button>
      </div>
    </div>
  )
}
