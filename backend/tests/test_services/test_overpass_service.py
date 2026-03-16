import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.overpass_service import (
    geocode,
    search_businesses,
    _extract_address,
    _extract_category,
    _parse_element,
    GeoLocation,
)


NOMINATIM_RESPONSE = [
    {
        "lat": "41.8781",
        "lon": "-87.6298",
        "display_name": "Chicago, Cook County, Illinois, USA",
    }
]

OVERPASS_RESPONSE = {
    "elements": [
        {
            "type": "node",
            "id": 123456,
            "lat": 41.88,
            "lon": -87.63,
            "tags": {
                "name": "ACME Manufacturing",
                "amenity": "factory",
                "phone": "+1-312-555-0100",
                "website": "https://acme-mfg.com",
                "addr:street": "Main Street",
                "addr:housenumber": "100",
                "addr:city": "Chicago",
                "addr:postcode": "60601",
            },
        },
        {
            "type": "way",
            "id": 789012,
            "center": {"lat": 41.87, "lon": -87.64},
            "tags": {
                "name": "Bob's Machine Shop",
                "craft": "metal_construction",
                "contact:phone": "+1-312-555-0200",
                "addr:city": "Chicago",
            },
        },
        {
            "type": "node",
            "id": 999,
            "lat": 41.89,
            "lon": -87.62,
            "tags": {},  # no name — should be filtered out
        },
    ]
}


def _mock_response(data, status_code=200):
    mock = MagicMock()
    mock.status_code = status_code
    mock.json.return_value = data
    mock.raise_for_status = MagicMock()
    return mock


@pytest.mark.asyncio
async def test_geocode_success():
    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get.return_value = _mock_response(NOMINATIM_RESPONSE)

    with patch("services.overpass_service.httpx.AsyncClient", return_value=mock_client):
        result = await geocode("Chicago")

    assert result is not None
    assert result.lat == 41.8781
    assert result.lon == -87.6298
    assert "Chicago" in result.display_name


@pytest.mark.asyncio
async def test_geocode_not_found():
    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get.return_value = _mock_response([])

    with patch("services.overpass_service.httpx.AsyncClient", return_value=mock_client):
        result = await geocode("NonexistentPlace12345")

    assert result is None


@pytest.mark.asyncio
async def test_search_businesses_success():
    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get.return_value = _mock_response(NOMINATIM_RESPONSE)
    mock_client.post.return_value = _mock_response(OVERPASS_RESPONSE)

    with patch("services.overpass_service.httpx.AsyncClient", return_value=mock_client):
        results = await search_businesses("Chicago", "manufacturing", 50.0, 60)

    # Should filter out the element with no name
    assert len(results) == 2
    assert results[0].name == "ACME Manufacturing"
    assert results[0].phone == "+1-312-555-0100"
    assert results[0].website == "https://acme-mfg.com"
    assert results[1].name == "Bob's Machine Shop"


@pytest.mark.asyncio
async def test_search_businesses_geocode_fails():
    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get.return_value = _mock_response([])

    with patch("services.overpass_service.httpx.AsyncClient", return_value=mock_client):
        with pytest.raises(ValueError, match="Could not geocode"):
            await search_businesses("BadLocation", "test")


def test_extract_address():
    tags = {
        "addr:housenumber": "100",
        "addr:street": "Main St",
        "addr:city": "Chicago",
        "addr:postcode": "60601",
    }
    assert _extract_address(tags) == "100 Main St, Chicago, 60601"


def test_extract_address_partial():
    assert _extract_address({"addr:city": "NYC"}) == "NYC"
    assert _extract_address({}) == ""


def test_extract_category():
    assert _extract_category({"amenity": "restaurant"}) == "Restaurant"
    assert _extract_category({"shop": "convenience"}) == "Convenience"
    assert _extract_category({"craft": "metal_construction"}) == "Metal Construction"
    assert _extract_category({}) == ""


def test_parse_element_node():
    element = {
        "type": "node",
        "id": 123,
        "lat": 41.88,
        "lon": -87.63,
        "tags": {
            "name": "Test Biz",
            "amenity": "cafe",
            "phone": "+1-555-0100",
        },
    }
    result = _parse_element(element)
    assert result.osm_id == "node/123"
    assert result.name == "Test Biz"
    assert result.phone == "+1-555-0100"
    assert result.category == "Cafe"
    assert result.lat == 41.88


def test_parse_element_way_with_center():
    element = {
        "type": "way",
        "id": 456,
        "center": {"lat": 41.87, "lon": -87.64},
        "tags": {"name": "Way Biz", "shop": "supermarket"},
    }
    result = _parse_element(element)
    assert result.lat == 41.87
    assert result.lon == -87.64
    assert result.osm_id == "way/456"
