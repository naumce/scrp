import { Loader2, CheckCircle2, XCircle, Zap } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
  useEnrichmentStatus,
  useEnrichmentResults,
  useStartEnrichment,
} from "@/hooks/useEnrichment"
import type { EnrichmentResult } from "@/types/enrichment"

interface EnrichmentProgressProps {
  projectId: number
  selectedBusinessIds: number[]
  allBusinessIds: number[]
}

export function EnrichmentProgress({
  projectId,
  selectedBusinessIds,
  allBusinessIds,
}: EnrichmentProgressProps) {
  const { data: status } = useEnrichmentStatus(projectId)
  const { data: results } = useEnrichmentResults(projectId)
  const startMutation = useStartEnrichment(projectId)

  const idsToEnrich =
    selectedBusinessIds.length > 0 ? selectedBusinessIds : allBusinessIds

  const handleStart = () => {
    startMutation.mutate(idsToEnrich)
  }

  const isRunning = status?.running ?? false
  const progressPercent =
    status && status.total > 0
      ? Math.round(((status.completed + status.failed) / status.total) * 100)
      : 0

  return (
    <div className="space-y-4 rounded-lg border p-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">Enrichment</h3>
        <Button
          onClick={handleStart}
          disabled={isRunning || idsToEnrich.length === 0}
          className="gap-2"
          size="sm"
        >
          {isRunning ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <Zap className="h-4 w-4" />
          )}
          {isRunning
            ? "Enriching..."
            : `Enrich ${idsToEnrich.length} businesses`}
        </Button>
      </div>

      {status && status.total > 0 && (
        <div className="space-y-2">
          <div className="h-2 overflow-hidden rounded-full bg-secondary">
            <div
              className="h-full rounded-full bg-primary transition-all duration-300"
              style={{ width: `${progressPercent}%` }}
            />
          </div>
          <div className="flex gap-4 text-sm text-muted-foreground">
            <span className="flex items-center gap-1">
              <CheckCircle2 className="h-3 w-3 text-green-500" />
              {status.completed} completed
            </span>
            <span className="flex items-center gap-1">
              <XCircle className="h-3 w-3 text-red-500" />
              {status.failed} failed
            </span>
            {isRunning && (
              <span className="flex items-center gap-1">
                <Loader2 className="h-3 w-3 animate-spin" />
                {status.in_progress} in progress
              </span>
            )}
          </div>
        </div>
      )}

      {results && results.length > 0 && (
        <div className="max-h-64 space-y-2 overflow-auto">
          {results.map((r: EnrichmentResult) => (
            <EnrichmentResultRow key={r.id} result={r} />
          ))}
        </div>
      )}
    </div>
  )
}

function EnrichmentResultRow({ result }: { result: EnrichmentResult }) {
  return (
    <div className="flex items-start gap-3 rounded-md border p-2 text-sm">
      <Badge
        variant={result.status === "success" ? "default" : "destructive"}
        className="mt-0.5"
      >
        {result.status}
      </Badge>
      <div className="flex-1 space-y-1">
        {result.emails.length > 0 && (
          <div className="text-muted-foreground">
            Emails: {result.emails.join(", ")}
          </div>
        )}
        {result.phones.length > 0 && (
          <div className="text-muted-foreground">
            Phones: {result.phones.join(", ")}
          </div>
        )}
        {result.social_links.length > 0 && (
          <div className="text-muted-foreground">
            Social: {result.social_links.length} links
          </div>
        )}
        {result.status === "failed" && result.error_message && (
          <div className="text-destructive">{result.error_message}</div>
        )}
      </div>
    </div>
  )
}
