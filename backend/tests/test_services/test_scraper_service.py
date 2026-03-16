from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import httpx

from services.scraper_service import fetch_page, scrape_business


def _mock_response(text="<html></html>", status_code=200):
    resp = MagicMock()
    resp.text = text
    resp.status_code = status_code
    resp.raise_for_status = MagicMock()
    if status_code >= 400:
        resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "error", request=MagicMock(), response=resp,
        )
    return resp


@pytest.mark.asyncio
async def test_fetch_page_success():
    client = AsyncMock()
    client.get.return_value = _mock_response("<html>Hello</html>")

    result = await fetch_page("https://test.com", client, timeout=5, max_retries=0)
    assert result == "<html>Hello</html>"


@pytest.mark.asyncio
async def test_fetch_page_retry_then_success():
    client = AsyncMock()
    client.get.side_effect = [
        Exception("timeout"),
        _mock_response("<html>OK</html>"),
    ]

    result = await fetch_page("https://test.com", client, timeout=5, max_retries=1)
    assert result == "<html>OK</html>"
    assert client.get.call_count == 2


@pytest.mark.asyncio
async def test_fetch_page_all_retries_fail():
    client = AsyncMock()
    client.get.side_effect = Exception("timeout")

    result = await fetch_page("https://test.com", client, timeout=5, max_retries=2)
    assert result is None
    assert client.get.call_count == 3


@pytest.mark.asyncio
async def test_scrape_business_no_website():
    client = AsyncMock()
    result = await scrape_business("", client)
    assert result.status == "failed"
    assert "No website" in result.error_message


@pytest.mark.asyncio
async def test_scrape_business_homepage_fails():
    client = AsyncMock()
    client.get.side_effect = Exception("timeout")

    result = await scrape_business("https://test.com", client)
    assert result.status == "failed"
    assert "Could not fetch" in result.error_message


@pytest.mark.asyncio
async def test_scrape_business_success():
    homepage = """
    <html>
    <body>
        <p>Email: info@testbiz.com</p>
        <p>Phone: +1-555-123-4567</p>
        <a href="https://facebook.com/testbiz">FB</a>
        <a href="/contact">Contact</a>
    </body>
    </html>
    """
    contact_page = """
    <html>
    <body>
        <p>Sales: sales@testbiz.com</p>
    </body>
    </html>
    """

    client = AsyncMock()
    client.get.side_effect = [
        _mock_response(homepage),
        _mock_response(contact_page),
    ]

    result = await scrape_business("https://testbiz.com", client)
    assert result.status == "success"
    assert "info@testbiz.com" in result.emails
    assert "sales@testbiz.com" in result.emails
    assert len(result.phones) >= 1
    assert len(result.social_links) >= 1
    assert "testbiz.com/contact" in result.contact_page


@pytest.mark.asyncio
async def test_scrape_business_adds_https():
    client = AsyncMock()
    client.get.return_value = _mock_response("<html><p>info@test.com</p></html>")

    result = await scrape_business("test.com", client)
    assert result.status == "success"
    # Verify HTTPS was prepended
    call_url = client.get.call_args_list[0].args[0]
    assert call_url.startswith("https://")
