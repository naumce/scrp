import { useEffect, useRef } from "react"
import L from "leaflet"
import "leaflet/dist/leaflet.css"
import type { BusinessWithEnrichment } from "@/types/business"

// Fix default marker icon (leaflet assets issue with bundlers)
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png"
import markerIcon from "leaflet/dist/images/marker-icon.png"
import markerShadow from "leaflet/dist/images/marker-shadow.png"

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
})

interface MapViewProps {
  businesses: BusinessWithEnrichment[]
  onSelectBusiness?: (business: BusinessWithEnrichment) => void
}

export function MapView({ businesses, onSelectBusiness }: MapViewProps) {
  const mapRef = useRef<L.Map | null>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  const mappable = businesses.filter(
    (b) => b.lat !== 0 && b.lon !== 0,
  )

  useEffect(() => {
    if (!containerRef.current) return

    if (!mapRef.current) {
      mapRef.current = L.map(containerRef.current).setView([41.88, -87.63], 11)
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        maxZoom: 19,
      }).addTo(mapRef.current)
    }

    const map = mapRef.current

    // Clear existing markers
    map.eachLayer((layer) => {
      if (layer instanceof L.Marker) {
        map.removeLayer(layer)
      }
    })

    // Add markers
    const markers: L.Marker[] = []
    for (const biz of mappable) {
      const marker = L.marker([biz.lat, biz.lon])
        .addTo(map)
        .bindPopup(
          `<strong>${biz.name}</strong>` +
            (biz.category ? `<br/><em>${biz.category}</em>` : "") +
            (biz.address ? `<br/>${biz.address}` : ""),
        )

      if (onSelectBusiness) {
        marker.on("click", () => onSelectBusiness(biz))
      }
      markers.push(marker)
    }

    if (markers.length > 0) {
      const group = L.featureGroup(markers)
      map.fitBounds(group.getBounds().pad(0.1))
    }
  }, [mappable.length, onSelectBusiness])

  useEffect(() => {
    return () => {
      if (mapRef.current) {
        mapRef.current.remove()
        mapRef.current = null
      }
    }
  }, [])

  if (mappable.length === 0) {
    return (
      <div className="flex h-64 items-center justify-center rounded-lg border bg-muted text-sm text-muted-foreground">
        No businesses with coordinates to display on map.
      </div>
    )
  }

  return (
    <div
      ref={containerRef}
      className="h-80 w-full rounded-lg border overflow-hidden"
    />
  )
}
