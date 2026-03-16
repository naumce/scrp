import csv
import io
from copy import copy
from dataclasses import dataclass
from typing import Dict, List, Optional

from openpyxl import Workbook
from openpyxl.styles import Font

from db.models import Business, EnrichmentResult


COLUMNS = [
    ("Name", "name"),
    ("Address", "address"),
    ("Phone", "phone"),
    ("Website", "website"),
    ("Category", "category"),
    ("Rating", "rating"),
    ("Reviews", "reviews"),
    ("Favorite", "is_favorite"),
    ("Emails", "emails"),
    ("Phones (Enriched)", "enriched_phones"),
    ("Social Links", "social_links"),
    ("Contact Page", "contact_page"),
    ("Enrichment Status", "enrichment_status"),
    ("Maps URL", "maps_url"),
]


@dataclass(frozen=True)
class ExportRow:
    name: str
    address: str
    phone: str
    website: str
    category: str
    rating: str
    reviews: str
    is_favorite: str
    emails: str
    enriched_phones: str
    social_links: str
    contact_page: str
    enrichment_status: str
    maps_url: str


def _build_row(
    business: Business,
    enrichment: Optional[EnrichmentResult],
) -> ExportRow:
    return ExportRow(
        name=business.name,
        address=business.address,
        phone=business.phone,
        website=business.website,
        category=business.category,
        rating=str(business.rating) if business.rating is not None else "",
        reviews=str(business.reviews) if business.reviews is not None else "",
        is_favorite="Yes" if business.is_favorite else "No",
        emails=", ".join(enrichment.emails) if enrichment else "",
        enriched_phones=", ".join(enrichment.phones) if enrichment else "",
        social_links=", ".join(enrichment.social_links) if enrichment else "",
        contact_page=enrichment.contact_page if enrichment else "",
        enrichment_status=enrichment.status if enrichment else "",
        maps_url=business.maps_url,
    )


def _build_rows(
    businesses: List[Business],
    enrichment_map: Dict[int, EnrichmentResult],
) -> List[ExportRow]:
    return [
        _build_row(biz, enrichment_map.get(biz.id))  # type: ignore[arg-type]
        for biz in businesses
    ]


def export_csv(
    businesses: List[Business],
    enrichment_map: Dict[int, EnrichmentResult],
) -> bytes:
    """Generate CSV file contents as bytes."""
    rows = _build_rows(businesses, enrichment_map)
    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([col[0] for col in COLUMNS])

    # Data rows
    for row in rows:
        writer.writerow([getattr(row, col[1]) for col in COLUMNS])

    return output.getvalue().encode("utf-8")


def export_excel(
    businesses: List[Business],
    enrichment_map: Dict[int, EnrichmentResult],
) -> bytes:
    """Generate Excel file contents as bytes."""
    rows = _build_rows(businesses, enrichment_map)
    wb = Workbook()
    ws = wb.active
    ws.title = "Businesses"  # type: ignore[union-attr]

    # Header
    headers = [col[0] for col in COLUMNS]
    ws.append(headers)  # type: ignore[union-attr]

    # Style header row bold
    for cell in ws[1]:  # type: ignore[index]
        cell.font = Font(bold=True)

    # Data rows
    for row in rows:
        ws.append([getattr(row, col[1]) for col in COLUMNS])  # type: ignore[union-attr]

    # Auto-width columns
    for col_cells in ws.columns:  # type: ignore[union-attr]
        max_len = 0
        col_letter = col_cells[0].column_letter
        for cell in col_cells:
            val = str(cell.value) if cell.value else ""
            max_len = max(max_len, len(val))
        ws.column_dimensions[col_letter].width = min(max_len + 2, 50)  # type: ignore[union-attr]

    output = io.BytesIO()
    wb.save(output)
    return output.getvalue()
