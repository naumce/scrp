import { useMemo, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import { ArrowLeft, Download, Map as MapIcon, TableIcon } from "lucide-react"
import type { RowSelectionState } from "@tanstack/react-table"
import { Button } from "@/components/ui/button"
import { SearchForm } from "@/components/SearchForm"
import { DataTable } from "@/components/DataTable/DataTable"
import { createColumns } from "@/components/DataTable/columns"
import { EnrichmentProgress } from "@/components/EnrichmentProgress"
import { ExportDialog } from "@/components/ExportDialog"
import { BulkActionsBar } from "@/components/BulkActionsBar"
import { BusinessDetailPanel } from "@/components/BusinessDetailPanel"
import { MapView } from "@/components/MapView"
import {
  useBusinesses,
  useSearchPlaces,
  useToggleFavorite,
  useBulkDelete,
  useUpdateNotes,
} from "@/hooks/useBusinesses"
import { useEnrichmentResults, useStartEnrichment } from "@/hooks/useEnrichment"
import { getProject } from "@/api/projects"
import type { BusinessWithEnrichment } from "@/types/business"

export function ProjectPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const projectId = Number(id)

  const [rowSelection, setRowSelection] = useState<RowSelectionState>({})
  const [exportOpen, setExportOpen] = useState(false)
  const [detailBusiness, setDetailBusiness] =
    useState<BusinessWithEnrichment | null>(null)
  const [viewMode, setViewMode] = useState<"table" | "map">("table")

  const { data: project } = useQuery({
    queryKey: ["project", projectId],
    queryFn: () => getProject(projectId),
    enabled: projectId > 0,
  })

  const { data: businesses = [], isLoading: businessesLoading } =
    useBusinesses(projectId)

  const { data: enrichmentResults = [] } = useEnrichmentResults(projectId)

  const searchMutation = useSearchPlaces(projectId)
  const favoriteMutation = useToggleFavorite(projectId)
  const bulkDeleteMutation = useBulkDelete(projectId)
  const notesMutation = useUpdateNotes(projectId)
  const startEnrichmentMutation = useStartEnrichment(projectId)

  // Merge enrichment results into business rows
  const mergedData: BusinessWithEnrichment[] = useMemo(() => {
    const enrichmentMap = new Map(
      enrichmentResults.map((r) => [r.business_id, r]),
    )
    return businesses.map((b) => {
      const e = enrichmentMap.get(b.id)
      return {
        ...b,
        enrichment_emails: e?.emails ?? [],
        enrichment_phones: e?.phones ?? [],
        enrichment_social: e?.social_links ?? [],
        enrichment_status: e?.status ?? null,
      }
    })
  }, [businesses, enrichmentResults])

  const columns = useMemo(
    () =>
      createColumns({
        onToggleFavorite: (bizId) => favoriteMutation.mutate(bizId),
      }),
    [favoriteMutation],
  )

  const handleSearch = (params: {
    keyword: string
    location: string
    radius: number
    max_results: number
  }) => {
    searchMutation.mutate({
      project_id: projectId,
      ...params,
    })
  }

  const selectedBusinessIds = Object.keys(rowSelection)
    .filter((key) => rowSelection[key])
    .map((idx) => businesses[Number(idx)]?.id)
    .filter(Boolean)

  const allBusinessIds = businesses.map((b) => b.id)
  const hasResults = businesses.length > 0

  const handleBulkDelete = () => {
    if (selectedBusinessIds.length === 0) return
    bulkDeleteMutation.mutate(selectedBusinessIds, {
      onSuccess: () => setRowSelection({}),
    })
  }

  const handleBulkEnrich = () => {
    startEnrichmentMutation.mutate(selectedBusinessIds)
  }

  const handleRowClick = (row: BusinessWithEnrichment) => {
    setDetailBusiness(row)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => navigate("/")}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <div className="flex-1">
          <h2 className="text-2xl font-bold tracking-tight">
            {project?.name ?? "Loading..."}
          </h2>
          {project && (
            <p className="text-sm text-muted-foreground">
              {project.keyword} near {project.location} ({project.radius} km)
            </p>
          )}
        </div>
      </div>

      {/* Step-by-step guide */}
      {!hasResults && !searchMutation.isPending && (
        <div className="rounded-lg border border-blue-500/20 bg-blue-500/5 p-4 space-y-3">
          <h3 className="font-semibold text-sm">How to use this project</h3>
          <ol className="text-sm text-muted-foreground space-y-2 list-decimal list-inside">
            <li>
              <strong className="text-foreground">Search</strong> — Enter a
              keyword and location below, then hit Search. Try the suggested
              keywords for best results.
            </li>
            <li>
              <strong className="text-foreground">Review</strong> — Browse the
              results table. Star your favorites, click a row for details.
            </li>
            <li>
              <strong className="text-foreground">Enrich</strong> — Select
              businesses (or leave blank for all), then click Enrich to scrape
              their websites for emails, phones, and social links.
            </li>
            <li>
              <strong className="text-foreground">Export</strong> — Download your
              leads as CSV or Excel with all data included.
            </li>
          </ol>
        </div>
      )}

      <SearchForm
        defaultKeyword={project?.keyword ?? ""}
        defaultLocation={project?.location ?? ""}
        defaultRadius={project?.radius ?? 50}
        defaultMaxResults={project?.max_results ?? 60}
        onSearch={handleSearch}
        isPending={searchMutation.isPending}
      />

      {searchMutation.isError && (
        <div className="rounded-md border border-destructive/50 bg-destructive/10 p-3 text-sm text-destructive">
          Search failed: {searchMutation.error?.message ?? "Unknown error"}
        </div>
      )}

      {hasResults && (
        <EnrichmentProgress
          projectId={projectId}
          selectedBusinessIds={selectedBusinessIds}
          allBusinessIds={allBusinessIds}
        />
      )}

      {businessesLoading ? (
        <div className="h-64 animate-pulse rounded-lg border bg-muted" />
      ) : (
        <div>
          <div className="mb-4 flex items-center justify-between">
            <h3 className="text-lg font-semibold">
              Results ({businesses.length})
            </h3>
            <div className="flex items-center gap-2">
              {hasResults && (
                <>
                  <div className="flex rounded-md border">
                    <Button
                      variant={viewMode === "table" ? "secondary" : "ghost"}
                      size="sm"
                      className="rounded-r-none gap-1.5"
                      onClick={() => setViewMode("table")}
                    >
                      <TableIcon className="h-3.5 w-3.5" />
                      Table
                    </Button>
                    <Button
                      variant={viewMode === "map" ? "secondary" : "ghost"}
                      size="sm"
                      className="rounded-l-none gap-1.5"
                      onClick={() => setViewMode("map")}
                    >
                      <MapIcon className="h-3.5 w-3.5" />
                      Map
                    </Button>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    className="gap-2"
                    onClick={() => setExportOpen(true)}
                  >
                    <Download className="h-4 w-4" />
                    Export
                  </Button>
                </>
              )}
            </div>
          </div>

          {viewMode === "map" ? (
            <MapView
              businesses={mergedData}
              onSelectBusiness={setDetailBusiness}
            />
          ) : (
            <DataTable
              columns={columns}
              data={mergedData}
              filterPlaceholder="Filter businesses..."
              rowSelection={rowSelection}
              onRowSelectionChange={setRowSelection}
              onRowClick={handleRowClick}
            />
          )}
        </div>
      )}

      <BulkActionsBar
        selectedCount={selectedBusinessIds.length}
        onDelete={handleBulkDelete}
        onEnrich={handleBulkEnrich}
        onExport={() => setExportOpen(true)}
        onClearSelection={() => setRowSelection({})}
        isDeleting={bulkDeleteMutation.isPending}
      />

      <ExportDialog
        projectId={projectId}
        selectedBusinessIds={selectedBusinessIds}
        allBusinessIds={allBusinessIds}
        open={exportOpen}
        onOpenChange={setExportOpen}
      />

      {detailBusiness && (
        <BusinessDetailPanel
          business={detailBusiness}
          onClose={() => setDetailBusiness(null)}
          onToggleFavorite={(bizId) => {
            favoriteMutation.mutate(bizId)
          }}
          onSaveNotes={(bizId, notes) => {
            notesMutation.mutate({ id: bizId, notes })
          }}
        />
      )}
    </div>
  )
}
