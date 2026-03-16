import { useState } from "react"
import { Plus, FolderOpen, Search, Zap, Download } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ProjectCard } from "@/components/ProjectCard"
import { CreateProjectDialog } from "@/components/CreateProjectDialog"
import { useProjects, useCreateProject, useDeleteProject } from "@/hooks/useProjects"
import type { CreateProjectInput } from "@/types/project"

export function DashboardPage() {
  const [dialogOpen, setDialogOpen] = useState(false)
  const { data: projects, isLoading } = useProjects()
  const createMutation = useCreateProject()
  const deleteMutation = useDeleteProject()

  const handleCreate = (data: CreateProjectInput) => {
    createMutation.mutate(data, {
      onSuccess: () => setDialogOpen(false),
    })
  }

  const handleDelete = (id: number) => {
    deleteMutation.mutate(id)
  }

  const showOnboarding = !isLoading && (!projects || projects.length === 0)

  return (
    <div>
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Projects</h2>
          <p className="text-muted-foreground">
            Create a project to start searching for businesses.
          </p>
        </div>
        <Button onClick={() => setDialogOpen(true)} className="gap-2">
          <Plus className="h-4 w-4" />
          New Project
        </Button>
      </div>

      {showOnboarding && (
        <div className="mt-8 space-y-6">
          <div className="rounded-lg border border-blue-500/20 bg-blue-500/5 p-6 space-y-4">
            <h3 className="text-lg font-semibold">Getting Started</h3>
            <p className="text-sm text-muted-foreground">
              This app helps you find local businesses, scrape their contact info, and export clean lead lists. Here's how:
            </p>
            <div className="grid gap-4 sm:grid-cols-3">
              <div className="flex gap-3 rounded-md border bg-background p-3">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary">
                  <Search className="h-4 w-4" />
                </div>
                <div>
                  <div className="text-sm font-medium">1. Search</div>
                  <div className="text-xs text-muted-foreground">
                    Create a project, enter a keyword (e.g. "restaurant", "manufacturing") and a city. We search OpenStreetMap for matching businesses.
                  </div>
                </div>
              </div>
              <div className="flex gap-3 rounded-md border bg-background p-3">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary">
                  <Zap className="h-4 w-4" />
                </div>
                <div>
                  <div className="text-sm font-medium">2. Enrich</div>
                  <div className="text-xs text-muted-foreground">
                    Select businesses and click Enrich. We'll scrape their websites for emails, phone numbers, and social media links.
                  </div>
                </div>
              </div>
              <div className="flex gap-3 rounded-md border bg-background p-3">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary">
                  <Download className="h-4 w-4" />
                </div>
                <div>
                  <div className="text-sm font-medium">3. Export</div>
                  <div className="text-xs text-muted-foreground">
                    Download your enriched lead list as CSV or Excel. All contact info, addresses, and social links included.
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="flex flex-col items-center gap-4 text-muted-foreground py-8">
            <FolderOpen className="h-12 w-12" />
            <p>No projects yet. Click <strong className="text-foreground">New Project</strong> above to get started.</p>
          </div>
        </div>
      )}

      {isLoading && (
        <div className="mt-8 grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              className="h-36 animate-pulse rounded-lg border bg-muted"
            />
          ))}
        </div>
      )}

      {!isLoading && projects && projects.length > 0 && (
        <div className="mt-8 grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          {projects.map((project) => (
            <ProjectCard
              key={project.id}
              project={project}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}

      <CreateProjectDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        onSubmit={handleCreate}
        isPending={createMutation.isPending}
      />
    </div>
  )
}
