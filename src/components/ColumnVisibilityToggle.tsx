import { useState } from "react"
import { Settings2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import type { Table } from "@tanstack/react-table"

interface ColumnVisibilityToggleProps<T> {
  table: Table<T>
}

const COLUMN_LABELS: Record<string, string> = {
  name: "Company Name",
  address: "Address",
  phone: "Phone",
  website: "Website",
  category: "Category",
  rating: "Rating",
  reviews: "Reviews",
  enrichment_emails: "Emails",
  enrichment_phones: "Found Phones",
  enrichment_social: "Social Links",
}

export function ColumnVisibilityToggle<T>({
  table,
}: ColumnVisibilityToggleProps<T>) {
  const [open, setOpen] = useState(false)

  const toggleableColumns = table
    .getAllLeafColumns()
    .filter((col) => col.getCanHide())

  return (
    <div className="relative">
      <Button
        variant="outline"
        size="sm"
        className="gap-1.5"
        onClick={() => setOpen((p) => !p)}
      >
        <Settings2 className="h-3.5 w-3.5" />
        Columns
      </Button>

      {open && (
        <>
          <div
            className="fixed inset-0 z-40"
            onClick={() => setOpen(false)}
          />
          <div className="absolute right-0 top-full z-50 mt-1 w-52 rounded-md border bg-popover p-2 shadow-lg">
            {toggleableColumns.map((col) => {
              const label =
                COLUMN_LABELS[col.id] ?? col.id
              return (
                <label
                  key={col.id}
                  className="flex items-center gap-2 rounded px-2 py-1.5 text-sm hover:bg-accent cursor-pointer"
                >
                  <input
                    type="checkbox"
                    checked={col.getIsVisible()}
                    onChange={col.getToggleVisibilityHandler()}
                    className="rounded"
                  />
                  {label}
                </label>
              )
            })}
          </div>
        </>
      )}
    </div>
  )
}
