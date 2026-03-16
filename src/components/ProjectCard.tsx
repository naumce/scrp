import { useNavigate } from "react-router-dom"
import { MapPin, Search, Calendar, Trash2, Building2, Mail, Star } from "lucide-react"
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { useProjectStats } from "@/hooks/useBusinesses"
import type { Project } from "@/types/project"

interface ProjectCardProps {
  project: Project
  onDelete: (id: number) => void
}

export function ProjectCard({ project, onDelete }: ProjectCardProps) {
  const navigate = useNavigate()
  const { data: stats } = useProjectStats(project.id)

  const createdDate = new Date(project.created_at).toLocaleDateString()

  return (
    <Card
      className="cursor-pointer transition-colors hover:bg-accent/50"
      onClick={() => navigate(`/projects/${project.id}`)}
    >
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <CardTitle className="text-base">{project.name}</CardTitle>
          <Button
            variant="ghost"
            size="icon"
            className="h-8 w-8 text-muted-foreground hover:text-destructive"
            onClick={(e) => {
              e.stopPropagation()
              onDelete(project.id)
            }}
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
        <CardDescription className="flex items-center gap-1">
          <Search className="h-3 w-3" />
          {project.keyword}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="flex flex-wrap gap-2">
          <Badge variant="secondary" className="gap-1">
            <MapPin className="h-3 w-3" />
            {project.location}
          </Badge>
          <Badge variant="outline">{project.radius} km</Badge>
          <Badge variant="outline" className="gap-1">
            <Calendar className="h-3 w-3" />
            {createdDate}
          </Badge>
        </div>

        {stats && stats.total > 0 && (
          <div className="flex gap-3 text-xs text-muted-foreground border-t pt-2">
            <span className="flex items-center gap-1">
              <Building2 className="h-3 w-3" />
              {stats.total} businesses
            </span>
            {stats.enriched > 0 && (
              <span className="flex items-center gap-1">
                <Mail className="h-3 w-3" />
                {stats.enriched} enriched
              </span>
            )}
            {stats.with_emails > 0 && (
              <span className="text-green-500">
                {stats.with_emails} with emails
              </span>
            )}
            {stats.favorites > 0 && (
              <span className="flex items-center gap-1">
                <Star className="h-3 w-3 fill-yellow-400 text-yellow-400" />
                {stats.favorites}
              </span>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
