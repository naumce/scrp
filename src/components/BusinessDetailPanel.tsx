import { useState, useEffect } from "react"
import {
  X,
  ExternalLink,
  Star,
  Mail,
  Phone,
  Globe,
  MapPin,
  Share2,
  StickyNote,
  Map,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import type { BusinessWithEnrichment } from "@/types/business"

interface BusinessDetailPanelProps {
  business: BusinessWithEnrichment | null
  onClose: () => void
  onToggleFavorite: (id: number) => void
  onSaveNotes: (id: number, notes: string) => void
}

export function BusinessDetailPanel({
  business,
  onClose,
  onToggleFavorite,
  onSaveNotes,
}: BusinessDetailPanelProps) {
  const [notes, setNotes] = useState("")

  useEffect(() => {
    setNotes(business?.notes ?? "")
  }, [business?.id, business?.notes])

  if (!business) return null

  const handleNotesBlur = () => {
    if (notes !== (business.notes ?? "")) {
      onSaveNotes(business.id, notes)
    }
  }

  return (
    <div className="fixed inset-y-0 right-0 z-50 w-full max-w-md border-l bg-background shadow-2xl overflow-y-auto">
      <div className="sticky top-0 z-10 flex items-center justify-between border-b bg-background px-4 py-3">
        <h3 className="font-semibold truncate pr-2">{business.name}</h3>
        <Button variant="ghost" size="icon" onClick={onClose}>
          <X className="h-4 w-4" />
        </Button>
      </div>

      <div className="space-y-6 p-4">
        {/* Actions */}
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            className="gap-1.5"
            onClick={() => onToggleFavorite(business.id)}
          >
            <Star
              className={`h-3.5 w-3.5 ${
                business.is_favorite
                  ? "fill-yellow-400 text-yellow-400"
                  : ""
              }`}
            />
            {business.is_favorite ? "Unfavorite" : "Favorite"}
          </Button>
          {business.maps_url && (
            <a href={business.maps_url} target="_blank" rel="noopener noreferrer">
              <Button variant="outline" size="sm" className="gap-1.5">
                <Map className="h-3.5 w-3.5" />
                View on Map
              </Button>
            </a>
          )}
        </div>

        {/* Basic Info */}
        <Section title="Business Info">
          {business.category && (
            <Badge variant="secondary" className="mb-2">
              {business.category}
            </Badge>
          )}
          <InfoRow icon={MapPin} label="Address" value={business.address} />
          <InfoRow icon={Phone} label="Phone" value={business.phone} />
          <InfoRow
            icon={Globe}
            label="Website"
            value={business.website}
            href={business.website}
          />
        </Section>

        {/* Enrichment Data */}
        {business.enrichment_status && (
          <Section title="Enrichment Results">
            <div className="mb-2">
              <Badge
                variant={
                  business.enrichment_status === "success"
                    ? "default"
                    : "destructive"
                }
              >
                {business.enrichment_status}
              </Badge>
            </div>

            {business.enrichment_emails.length > 0 && (
              <div className="space-y-1">
                <span className="text-xs font-medium text-muted-foreground flex items-center gap-1">
                  <Mail className="h-3 w-3" /> Emails
                </span>
                {business.enrichment_emails.map((email) => (
                  <a
                    key={email}
                    href={`mailto:${email}`}
                    className="block text-sm text-primary hover:underline"
                  >
                    {email}
                  </a>
                ))}
              </div>
            )}

            {business.enrichment_phones.length > 0 && (
              <div className="space-y-1 mt-3">
                <span className="text-xs font-medium text-muted-foreground flex items-center gap-1">
                  <Phone className="h-3 w-3" /> Discovered Phones
                </span>
                {business.enrichment_phones.map((phone) => (
                  <div key={phone} className="text-sm">{phone}</div>
                ))}
              </div>
            )}

            {business.enrichment_social.length > 0 && (
              <div className="space-y-1 mt-3">
                <span className="text-xs font-medium text-muted-foreground flex items-center gap-1">
                  <Share2 className="h-3 w-3" /> Social Links
                </span>
                {business.enrichment_social.map((link) => {
                  let label = link
                  try {
                    label = new URL(link).hostname.replace("www.", "")
                  } catch { /* use raw */ }
                  return (
                    <a
                      key={link}
                      href={link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-1 text-sm text-primary hover:underline"
                    >
                      {label}
                      <ExternalLink className="h-3 w-3" />
                    </a>
                  )
                })}
              </div>
            )}
          </Section>
        )}

        {/* Notes */}
        <Section title="Notes">
          <div className="flex items-start gap-2">
            <StickyNote className="mt-2 h-4 w-4 shrink-0 text-muted-foreground" />
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              onBlur={handleNotesBlur}
              placeholder="Add notes about this business..."
              className="w-full resize-none rounded-md border bg-transparent px-3 py-2 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring"
              rows={4}
            />
          </div>
        </Section>
      </div>
    </div>
  )
}

function Section({
  title,
  children,
}: {
  title: string
  children: React.ReactNode
}) {
  return (
    <div>
      <h4 className="mb-2 text-sm font-medium text-muted-foreground">
        {title}
      </h4>
      <div className="space-y-1">{children}</div>
    </div>
  )
}

function InfoRow({
  icon: Icon,
  label,
  value,
  href,
}: {
  icon: React.ComponentType<{ className?: string }>
  label: string
  value: string
  href?: string
}) {
  if (!value) return null

  return (
    <div className="flex items-start gap-2 text-sm">
      <Icon className="mt-0.5 h-3.5 w-3.5 shrink-0 text-muted-foreground" />
      <div>
        <span className="text-xs text-muted-foreground">{label}</span>
        {href ? (
          <a
            href={href.startsWith("http") ? href : `https://${href}`}
            target="_blank"
            rel="noopener noreferrer"
            className="block text-primary hover:underline"
          >
            {value}
          </a>
        ) : (
          <div>{value}</div>
        )}
      </div>
    </div>
  )
}
