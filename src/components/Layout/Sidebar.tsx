import { NavLink } from "react-router-dom"
import { LayoutDashboard, Settings, FolderOpen } from "lucide-react"
import { useProjects } from "@/hooks/useProjects"

export function Sidebar() {
  const { data: projects } = useProjects()

  return (
    <aside className="flex h-screen w-56 flex-col border-r bg-muted/40">
      <div className="flex h-14 items-center border-b px-4">
        <h1 className="text-lg font-semibold">LocalBiz</h1>
      </div>
      <nav className="flex-1 overflow-auto p-2">
        <div className="space-y-1">
          <NavLink
            to="/"
            end
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors ${
                isActive
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
              }`
            }
          >
            <LayoutDashboard className="h-4 w-4" />
            Dashboard
          </NavLink>

          {projects && projects.length > 0 && (
            <div className="pt-4">
              <span className="px-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Projects
              </span>
              <div className="mt-2 space-y-1">
                {projects.map((p) => (
                  <NavLink
                    key={p.id}
                    to={`/projects/${p.id}`}
                    className={({ isActive }) =>
                      `flex items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors ${
                        isActive
                          ? "bg-primary text-primary-foreground"
                          : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                      }`
                    }
                  >
                    <FolderOpen className="h-4 w-4" />
                    <span className="truncate">{p.name}</span>
                  </NavLink>
                ))}
              </div>
            </div>
          )}
        </div>
      </nav>
      <div className="border-t p-2">
        <NavLink
          to="/settings"
          className={({ isActive }) =>
            `flex items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors ${
              isActive
                ? "bg-primary text-primary-foreground"
                : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
            }`
          }
        >
          <Settings className="h-4 w-4" />
          Settings
        </NavLink>
      </div>
    </aside>
  )
}
