import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useSettings } from "@/hooks/useSettings"
import type { CreateProjectInput } from "@/types/project"

interface CreateProjectDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSubmit: (data: CreateProjectInput) => void
  isPending: boolean
}

export function CreateProjectDialog({
  open,
  onOpenChange,
  onSubmit,
  isPending,
}: CreateProjectDialogProps) {
  const { data: settings } = useSettings()

  const [form, setForm] = useState<CreateProjectInput>({
    name: "",
    keyword: "",
    location: "",
    radius: 50,
    max_results: 60,
  })

  // Update defaults when settings load
  useEffect(() => {
    if (settings) {
      setForm((prev) => ({
        ...prev,
        radius: Number(settings.default_radius) || 50,
        max_results: Number(settings.default_max_results) || 60,
      }))
    }
  }, [settings])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(form)
    setForm({
      name: "",
      keyword: "",
      location: "",
      radius: Number(settings?.default_radius) || 50,
      max_results: Number(settings?.default_max_results) || 60,
    })
  }

  const updateField = <K extends keyof CreateProjectInput>(
    key: K,
    value: CreateProjectInput[K],
  ) => {
    setForm((prev) => ({ ...prev, [key]: value }))
  }

  const isValid = form.name.trim() && form.keyword.trim() && form.location.trim()

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent onClose={() => onOpenChange(false)}>
        <DialogHeader>
          <DialogTitle>New Project</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="mt-4 space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name">Project Name</Label>
            <Input
              id="name"
              placeholder="e.g. Chicago Manufacturers"
              value={form.name}
              onChange={(e) => updateField("name", e.target.value)}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="keyword">Keyword</Label>
            <Input
              id="keyword"
              placeholder="e.g. manufacturing"
              value={form.keyword}
              onChange={(e) => updateField("keyword", e.target.value)}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="location">Location</Label>
            <Input
              id="location"
              placeholder="e.g. Chicago"
              value={form.location}
              onChange={(e) => updateField("location", e.target.value)}
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="radius">Radius (km)</Label>
              <Input
                id="radius"
                type="number"
                min={1}
                max={500}
                value={form.radius}
                onChange={(e) => updateField("radius", Number(e.target.value))}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="max_results">Max Results</Label>
              <Input
                id="max_results"
                type="number"
                min={1}
                max={200}
                value={form.max_results}
                onChange={(e) =>
                  updateField("max_results", Number(e.target.value))
                }
              />
            </div>
          </div>
          <div className="flex justify-end gap-2 pt-2">
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={!isValid || isPending}>
              {isPending ? "Creating..." : "Create Project"}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  )
}
