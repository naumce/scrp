from dataclasses import dataclass, field
from typing import Optional

import httpx

from config import settings

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
]

# OSM tags that represent businesses (keep small for fast Overpass queries)
BUSINESS_TAGS = ["amenity", "shop", "office", "craft", "industrial", "tourism", "healthcare"]


@dataclass(frozen=True)
class GeoLocation:
    lat: float
    lon: float
    display_name: str


@dataclass(frozen=True)
class BusinessResult:
    osm_id: str
    name: str
    address: str = ""
    phone: str = ""
    website: str = ""
    category: str = ""
    lat: float = 0.0
    lon: float = 0.0
    tags: dict = field(default_factory=dict)


async def geocode(location: str) -> Optional[GeoLocation]:
    """Convert a location string to lat/lon using Nominatim."""
    async with httpx.AsyncClient(http1=True, http2=False) as client:
        response = await client.get(
            NOMINATIM_URL,
            params={
                "q": location,
                "format": "json",
                "limit": 1,
            },
            headers={"User-Agent": settings.nominatim_user_agent},
            timeout=10,
        )
        response.raise_for_status()
        results = response.json()

    if not results:
        return None

    first = results[0]
    return GeoLocation(
        lat=float(first["lat"]),
        lon=float(first["lon"]),
        display_name=first.get("display_name", location),
    )


def _build_overpass_query(
    lat: float, lon: float, radius: float, keyword: str, max_results: int
) -> str:
    """Build an Overpass QL query for businesses near a location.

    Uses exact tag value match (fast, indexed) to avoid timeouts.
    Examples: amenity=restaurant, shop=bakery, craft=brewery, office=insurance.
    """
    radius_m = min(int(radius * 1000), 50_000)  # Cap at 50km
    kw_lower = keyword.lower().replace(" ", "_")

    exact_clauses = []
    for tag in BUSINESS_TAGS:
        exact_clauses.append(
            f'  node["{tag}"="{kw_lower}"]["name"](around:{radius_m},{lat},{lon});'
        )

    all_clauses = "\n".join(exact_clauses)
    return f"""[out:json][timeout:25];
(
{all_clauses}
);
out {max_results};
"""


def _extract_address(tags: dict) -> str:
    """Build address string from OSM tags."""
    parts = []
    street = tags.get("addr:street", "")
    housenumber = tags.get("addr:housenumber", "")
    if street:
        parts.append(f"{housenumber} {street}".strip())
    city = tags.get("addr:city", "")
    if city:
        parts.append(city)
    postcode = tags.get("addr:postcode", "")
    if postcode:
        parts.append(postcode)
    country = tags.get("addr:country", "")
    if country:
        parts.append(country)
    return ", ".join(parts)


def _extract_category(tags: dict) -> str:
    """Extract the primary business category from OSM tags."""
    for tag in BUSINESS_TAGS:
        value = tags.get(tag)
        if value:
            return value.replace("_", " ").title()
    return ""


def _parse_element(element: dict) -> BusinessResult:
    """Parse an Overpass API element into a BusinessResult."""
    tags = element.get("tags", {})

    # For ways, coordinates are in center
    lat = element.get("lat", 0.0)
    lon = element.get("lon", 0.0)
    center = element.get("center")
    if center:
        lat = center.get("lat", lat)
        lon = center.get("lon", lon)

    return BusinessResult(
        osm_id=f"{element.get('type', 'node')}/{element.get('id', '')}",
        name=tags.get("name", "Unknown"),
        address=_extract_address(tags),
        phone=tags.get("phone", tags.get("contact:phone", "")),
        website=tags.get("website", tags.get("contact:website", "")),
        category=_extract_category(tags),
        lat=lat,
        lon=lon,
        tags=tags,
    )


async def _search_overpass(
    geo: GeoLocation,
    keyword: str,
    radius: float,
    max_results: int,
) -> list[BusinessResult]:
    """Search using Overpass API exact tag match. Fast but only works for
    standard OSM tag values like 'restaurant', 'bakery', 'dentist'."""
    query = _build_overpass_query(
        geo.lat, geo.lon, radius, keyword, max_results
    )

    last_error = None
    data = None
    async with httpx.AsyncClient(http1=True, http2=False) as client:
        for url in OVERPASS_URLS:
            try:
                response = await client.post(
                    url,
                    data={"data": query},
                    timeout=30,
                    headers={"User-Agent": settings.nominatim_user_agent},
                )
                response.raise_for_status()
                data = response.json()
                if data.get("remark") and "timed out" in data["remark"]:
                    last_error = Exception(f"Overpass query timed out on {url}")
                    continue
                break
            except Exception as e:
                last_error = e
                continue

    if data is None or (data.get("remark") and "timed out" in data.get("remark", "")):
        raise last_error or Exception("All Overpass servers failed")

    elements = data.get("elements", [])
    return [_parse_element(el) for el in elements if el.get("tags", {}).get("name")]


async def _search_nominatim(
    geo: GeoLocation,
    keyword: str,
    radius: float,
    max_results: int,
) -> list[BusinessResult]:
    """Fallback search using Nominatim free-text POI search.

    Nominatim has a pre-built search index, so free-text queries like
    'manufacturing near Chicago' work fast. This catches keywords that
    aren't standard OSM tag values.
    """
    # Nominatim viewbox: left,top,right,bottom (bounded=1 restricts to box)
    # Convert radius km to rough degree offset
    deg_offset = radius / 111.0  # ~111km per degree
    viewbox = (
        f"{geo.lon - deg_offset},{geo.lat + deg_offset},"
        f"{geo.lon + deg_offset},{geo.lat - deg_offset}"
    )

    async with httpx.AsyncClient(http1=True, http2=False) as client:
        response = await client.get(
            NOMINATIM_URL,
            params={
                "q": keyword,
                "format": "json",
                "limit": min(max_results, 50),  # Nominatim max is 50
                "viewbox": viewbox,
                "bounded": 1,
                "addressdetails": 1,
                "extratags": 1,
            },
            headers={"User-Agent": settings.nominatim_user_agent},
            timeout=15,
        )
        response.raise_for_status()
        results = response.json()

    businesses = []
    seen_ids = set()
    for item in results:
        osm_id = f"{item.get('osm_type', 'node')}/{item.get('osm_id', '')}"
        if osm_id in seen_ids:
            continue
        seen_ids.add(osm_id)

        addr = item.get("address", {})
        address_parts = []
        road = addr.get("road", "")
        house = addr.get("house_number", "")
        if road:
            address_parts.append(f"{house} {road}".strip())
        city = addr.get("city", addr.get("town", addr.get("village", "")))
        if city:
            address_parts.append(city)
        postcode = addr.get("postcode", "")
        if postcode:
            address_parts.append(postcode)

        extra = item.get("extratags") or {}
        businesses.append(BusinessResult(
            osm_id=osm_id,
            name=item.get("display_name", "").split(",")[0],
            address=", ".join(address_parts),
            phone=extra.get("phone", extra.get("contact:phone", "")),
            website=extra.get("website", extra.get("contact:website", "")),
            category=item.get("type", "").replace("_", " ").title(),
            lat=float(item.get("lat", 0)),
            lon=float(item.get("lon", 0)),
            tags=extra,
        ))

    return businesses


async def search_businesses(
    location: str,
    keyword: str,
    radius: float = 50.0,
    max_results: int = 60,
) -> list[BusinessResult]:
    """Search for businesses using Overpass API, with Nominatim fallback.

    Strategy:
    1. Try Overpass exact tag match (fast, reliable for standard keywords)
    2. If 0 results, fall back to Nominatim free-text search (handles
       arbitrary keywords like 'manufacturing', 'logistics', etc.)
    """
    geo = await geocode(location)
    if geo is None:
        raise ValueError(f"Could not geocode location: {location}")

    # Try Overpass first (best for standard OSM tag values)
    try:
        results = await _search_overpass(geo, keyword, radius, max_results)
        if results:
            return results
    except Exception:
        pass  # Fall through to Nominatim

    # Fallback: Nominatim free-text search
    return await _search_nominatim(geo, keyword, radius, max_results)
