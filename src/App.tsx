import { Routes, Route } from "react-router-dom"
import { Sidebar } from "@/components/Layout/Sidebar"
import { MainContent } from "@/components/Layout/MainContent"
import { DashboardPage } from "@/pages/DashboardPage"
import { ProjectPage } from "@/pages/ProjectPage"
import { SettingsPage } from "@/pages/SettingsPage"
import { useSidecar } from "@/hooks/useSidecar"
import { Loader2 } from "lucide-react"
import { Toaster } from "sonner"

function LoadingScreen() {
  return (
    <div className="flex h-screen items-center justify-center">
      <div className="flex flex-col items-center gap-4">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
        <p className="text-sm text-muted-foreground">
          Starting backend service...
        </p>
      </div>
    </div>
  )
}

function App() {
  const sidecarReady = useSidecar()

  if (!sidecarReady) {
    return <LoadingScreen />
  }

  return (
    <div className="flex h-screen">
      <Sidebar />
      <MainContent>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/projects/:id" element={<ProjectPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </MainContent>
      <Toaster position="bottom-right" richColors closeButton />
    </div>
  )
}

export default App
