import type { ColumnDef } from "@tanstack/react-table"
import { Star, ExternalLink, Mail, Phone, Share2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { Badge } from "@/components/ui/badge"
import type { BusinessWithEnrichment } from "@/types/business"

interface ColumnOptions {
  onToggleFavorite: (id: number) => void
}

export function createColumns(options: ColumnOptions): ColumnDef<BusinessWithEnrichment>[] {
  return [
    {
      id: "select",
      header: ({ table }) => (
        <Checkbox
          checked={table.getIsAllPageRowsSelected()}
          onCheckedChange={(value) =>
            table.toggleAllPageRowsSelected(!!value)
          }
        />
      ),
      cell: ({ row }) => (
        <Checkbox
          checked={row.getIsSelected()}
          onCheckedChange={(value) => row.toggleSelected(!!value)}
        />
      ),
      enableSorting: false,
      size: 40,
    },
    {
      id: "favorite",
      header: "",
      cell: ({ row }) => (
        <Button
          variant="ghost"
          size="icon"
          className="h-8 w-8"
          onClick={(e) => {
            e.stopPropagation()
            options.onToggleFavorite(row.original.id)
          }}
        >
          <Star
            className={`h-4 w-4 ${
              row.original.is_favorite
                ? "fill-yellow-400 text-yellow-400"
                : "text-muted-foreground"
            }`}
          />
        </Button>
      ),
      enableSorting: false,
      size: 40,
    },
    {
      accessorKey: "name",
      header: "Company Name",
      size: 200,
    },
    {
      accessorKey: "address",
      header: "Address",
      size: 200,
    },
    {
      accessorKey: "phone",
      header: "Phone",
      size: 140,
    },
    {
      accessorKey: "website",
      header: "Website",
      size: 180,
      cell: ({ getValue }) => {
        const url = getValue<string>()
        if (!url) return <span className="text-muted-foreground">—</span>
        try {
          return (
            <a
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 text-primary hover:underline"
              onClick={(e) => e.stopPropagation()}
            >
              {new URL(url).hostname.replace("www.", "")}
              <ExternalLink className="h-3 w-3" />
            </a>
          )
        } catch {
          return <span className="text-muted-foreground">{url}</span>
        }
      },
    },
    {
      accessorKey: "category",
      header: "Category",
      size: 120,
      cell: ({ getValue }) => {
        const val = getValue<string>()
        return val ? (
          <Badge variant="secondary">{val}</Badge>
        ) : (
          <span className="text-muted-foreground">—</span>
        )
      },
    },
    {
      id: "enrichment_emails",
      header: () => (
        <span className="inline-flex items-center gap-1">
          <Mail className="h-3 w-3" /> Emails
        </span>
      ),
      accessorFn: (row) => row.enrichment_emails?.join(", ") ?? "",
      size: 200,
      cell: ({ row }) => {
        const emails = row.original.enrichment_emails
        if (!emails || emails.length === 0) {
          return <span className="text-muted-foreground">—</span>
        }
        return (
          <div className="space-y-0.5">
            {emails.map((email) => (
              <a
                key={email}
                href={`mailto:${email}`}
                className="block text-primary hover:underline text-xs"
                onClick={(e) => e.stopPropagation()}
              >
                {email}
              </a>
            ))}
          </div>
        )
      },
    },
    {
      id: "enrichment_phones",
      header: () => (
        <span className="inline-flex items-center gap-1">
          <Phone className="h-3 w-3" /> Found Phones
        </span>
      ),
      accessorFn: (row) => row.enrichment_phones?.join(", ") ?? "",
      size: 140,
      cell: ({ row }) => {
        const phones = row.original.enrichment_phones
        if (!phones || phones.length === 0) {
          return <span className="text-muted-foreground">—</span>
        }
        return (
          <div className="space-y-0.5 text-xs">
            {phones.map((phone) => (
              <div key={phone}>{phone}</div>
            ))}
          </div>
        )
      },
    },
    {
      id: "enrichment_social",
      header: () => (
        <span className="inline-flex items-center gap-1">
          <Share2 className="h-3 w-3" /> Social
        </span>
      ),
      accessorFn: (row) => row.enrichment_social?.join(", ") ?? "",
      size: 160,
      cell: ({ row }) => {
        const links = row.original.enrichment_social
        if (!links || links.length === 0) {
          return <span className="text-muted-foreground">—</span>
        }
        return (
          <div className="space-y-0.5">
            {links.map((link) => {
              let label = link
              try {
                label = new URL(link).hostname.replace("www.", "")
              } catch { /* use raw link */ }
              return (
                <a
                  key={link}
                  href={link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block text-primary hover:underline text-xs"
                  onClick={(e) => e.stopPropagation()}
                >
                  {label}
                </a>
              )
            })}
          </div>
        )
      },
    },
  ]
}
