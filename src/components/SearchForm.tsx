import { useState } from "react"
import { Search, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { SearchSuggestions } from "@/components/SearchSuggestions"

interface SearchFormProps {
  defaultKeyword: string
  defaultLocation: string
  defaultRadius: number
  defaultMaxResults: number
  onSearch: (params: {
    keyword: string
    location: string
    radius: number
    max_results: number
  }) => void
  isPending: boolean
}

export function SearchForm({
  defaultKeyword,
  defaultLocation,
  defaultRadius,
  defaultMaxResults,
  onSearch,
  isPending,
}: SearchFormProps) {
  const [keyword, setKeyword] = useState(defaultKeyword)
  const [location, setLocation] = useState(defaultLocation)
  const [radius, setRadius] = useState(defaultRadius)
  const [maxResults, setMaxResults] = useState(defaultMaxResults)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSearch({ keyword, location, radius, max_results: maxResults })
  }

  const isValid = keyword.trim() && location.trim()

  return (
    <form onSubmit={handleSubmit} className="space-y-4 rounded-lg border p-4">
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <div className="space-y-2">
          <Label htmlFor="search-keyword">Keyword</Label>
          <Input
            id="search-keyword"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            placeholder="e.g. restaurant"
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="search-location">Location</Label>
          <Input
            id="search-location"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="e.g. Chicago"
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="search-radius">Radius (km)</Label>
          <Input
            id="search-radius"
            type="number"
            min={1}
            max={500}
            value={radius}
            onChange={(e) => setRadius(Number(e.target.value))}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="search-max">Max Results</Label>
          <Input
            id="search-max"
            type="number"
            min={1}
            max={200}
            value={maxResults}
            onChange={(e) => setMaxResults(Number(e.target.value))}
          />
        </div>
      </div>

      <SearchSuggestions onSelect={setKeyword} />

      <Button type="submit" disabled={!isValid || isPending} className="gap-2">
        {isPending ? (
          <Loader2 className="h-4 w-4 animate-spin" />
        ) : (
          <Search className="h-4 w-4" />
        )}
        {isPending ? "Searching..." : "Search Businesses"}
      </Button>
    </form>
  )
}
