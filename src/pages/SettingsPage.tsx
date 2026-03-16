import { useState, useEffect } from "react"
import { Save, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card } from "@/components/ui/card"
import { useSettings, useUpdateSettings } from "@/hooks/useSettings"

export function SettingsPage() {
  const { data: settings, isLoading } = useSettings()
  const updateMutation = useUpdateSettings()

  const [form, setForm] = useState({
    default_radius: "50",
    default_max_results: "60",
    scrape_timeout: "10",
    scrape_concurrency: "5",
  })

  useEffect(() => {
    if (settings) {
      setForm({
        default_radius: settings.default_radius,
        default_max_results: settings.default_max_results,
        scrape_timeout: settings.scrape_timeout,
        scrape_concurrency: settings.scrape_concurrency,
      })
    }
  }, [settings])

  const handleChange = (key: string, value: string) => {
    setForm((prev) => ({ ...prev, [key]: value }))
  }

  const handleSave = () => {
    updateMutation.mutate(form)
  }

  if (isLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">Settings</h2>
        <p className="text-sm text-muted-foreground">
          These settings apply to new projects and enrichment runs.
        </p>
      </div>

      <Card className="space-y-6 p-6">
        <div>
          <h3 className="text-lg font-semibold">Search Defaults</h3>
          <p className="text-xs text-muted-foreground mt-1">
            Pre-filled when you create a new project. You can still override per project.
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="default_radius">Default Radius (km)</Label>
            <Input
              id="default_radius"
              type="number"
              min="1"
              max="500"
              value={form.default_radius}
              onChange={(e) => handleChange("default_radius", e.target.value)}
            />
            <p className="text-xs text-muted-foreground">
              How far from the location to search (1-500 km).
            </p>
          </div>
          <div className="space-y-2">
            <Label htmlFor="default_max_results">Default Max Results</Label>
            <Input
              id="default_max_results"
              type="number"
              min="1"
              max="500"
              value={form.default_max_results}
              onChange={(e) =>
                handleChange("default_max_results", e.target.value)
              }
            />
            <p className="text-xs text-muted-foreground">
              Maximum businesses returned per search.
            </p>
          </div>
        </div>
      </Card>

      <Card className="space-y-6 p-6">
        <div>
          <h3 className="text-lg font-semibold">Enrichment</h3>
          <p className="text-xs text-muted-foreground mt-1">
            Controls how the scraper fetches contact info from business websites.
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="scrape_timeout">
              Scrape Timeout (seconds)
            </Label>
            <Input
              id="scrape_timeout"
              type="number"
              min="1"
              max="60"
              value={form.scrape_timeout}
              onChange={(e) => handleChange("scrape_timeout", e.target.value)}
            />
            <p className="text-xs text-muted-foreground">
              How long to wait for each website before giving up.
            </p>
          </div>
          <div className="space-y-2">
            <Label htmlFor="scrape_concurrency">
              Concurrent Scrape Workers
            </Label>
            <Input
              id="scrape_concurrency"
              type="number"
              min="1"
              max="20"
              value={form.scrape_concurrency}
              onChange={(e) =>
                handleChange("scrape_concurrency", e.target.value)
              }
            />
            <p className="text-xs text-muted-foreground">
              How many websites to scrape simultaneously. Higher = faster but more aggressive.
            </p>
          </div>
        </div>
      </Card>

      <Button
        onClick={handleSave}
        disabled={updateMutation.isPending}
        className="gap-2"
      >
        {updateMutation.isPending ? (
          <Loader2 className="h-4 w-4 animate-spin" />
        ) : (
          <Save className="h-4 w-4" />
        )}
        Save Settings
      </Button>
    </div>
  )
}
