import { Badge } from "@/components/ui/badge"

const SUGGESTIONS = [
  { label: "Restaurant", keyword: "restaurant" },
  { label: "Cafe", keyword: "cafe" },
  { label: "Bar", keyword: "bar" },
  { label: "Hotel", keyword: "hotel" },
  { label: "Dentist", keyword: "dentist" },
  { label: "Pharmacy", keyword: "pharmacy" },
  { label: "Supermarket", keyword: "supermarket" },
  { label: "Bank", keyword: "bank" },
  { label: "Car Repair", keyword: "car_repair" },
  { label: "Hairdresser", keyword: "hairdresser" },
  { label: "Bakery", keyword: "bakery" },
  { label: "Gym", keyword: "fitness_centre" },
  { label: "Veterinary", keyword: "veterinary" },
  { label: "Clinic", keyword: "clinic" },
  { label: "Insurance", keyword: "insurance" },
]

interface SearchSuggestionsProps {
  onSelect: (keyword: string) => void
}

export function SearchSuggestions({ onSelect }: SearchSuggestionsProps) {
  return (
    <div className="space-y-1.5">
      <span className="text-xs text-muted-foreground">
        Popular keywords (click to use):
      </span>
      <div className="flex flex-wrap gap-1.5">
        {SUGGESTIONS.map((s) => (
          <Badge
            key={s.keyword}
            variant="outline"
            className="cursor-pointer hover:bg-accent transition-colors"
            onClick={() => onSelect(s.keyword)}
          >
            {s.label}
          </Badge>
        ))}
      </div>
    </div>
  )
}
