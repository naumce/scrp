from extractors.contact_page_finder import find_contact_pages


BASE_URL = "https://acme-mfg.com"


def test_finds_contact_by_href():
    html = '<a href="/contact">Contact Us</a>'
    result = find_contact_pages(html, BASE_URL)
    assert "https://acme-mfg.com/contact" in result


def test_finds_about_by_href():
    html = '<a href="/about-us">About</a>'
    result = find_contact_pages(html, BASE_URL)
    assert "https://acme-mfg.com/about-us" in result


def test_finds_by_link_text():
    html = '<a href="/reach">Contact our team</a>'
    result = find_contact_pages(html, BASE_URL)
    assert "https://acme-mfg.com/reach" in result


def test_ignores_external_links():
    html = '<a href="https://other.com/contact">Contact</a>'
    result = find_contact_pages(html, BASE_URL)
    assert len(result) == 0


def test_max_pages_limit():
    html = """
    <a href="/contact">C1</a>
    <a href="/about">C2</a>
    <a href="/team">C3</a>
    <a href="/company">C4</a>
    """
    result = find_contact_pages(html, BASE_URL, max_pages=2)
    assert len(result) <= 2


def test_strips_fragments_and_params():
    html = '<a href="/contact?ref=nav#form">Contact</a>'
    result = find_contact_pages(html, BASE_URL)
    assert "https://acme-mfg.com/contact" in result


def test_empty():
    assert find_contact_pages("", BASE_URL) == []
    assert find_contact_pages("<p>No links</p>", BASE_URL) == []


def test_sample_page():
    with open("tests/fixtures/sample_html/business_page.html") as f:
        html = f.read()
    result = find_contact_pages(html, BASE_URL)
    assert len(result) >= 2  # /contact, /about-us, /team
