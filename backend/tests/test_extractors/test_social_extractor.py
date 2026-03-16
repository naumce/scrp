from extractors.social_extractor import extract_social_links


def test_extract_facebook():
    html = '<a href="https://facebook.com/mycompany">FB</a>'
    result = extract_social_links(html)
    assert "https://facebook.com/mycompany" in result


def test_extract_linkedin():
    html = '<a href="https://www.linkedin.com/company/acme">LI</a>'
    result = extract_social_links(html)
    assert "https://www.linkedin.com/company/acme" in result


def test_extract_twitter():
    html = '<a href="https://twitter.com/acme">Twitter</a>'
    result = extract_social_links(html)
    assert "https://twitter.com/acme" in result


def test_extract_x_com():
    html = '<a href="https://x.com/acme">X</a>'
    result = extract_social_links(html)
    assert "https://x.com/acme" in result


def test_filters_share_links():
    html = '<a href="https://facebook.com/share">Share</a>'
    assert extract_social_links(html) == []


def test_removes_tracking_params():
    html = '<a href="https://linkedin.com/company/acme?utm_source=web">LI</a>'
    result = extract_social_links(html)
    assert "https://linkedin.com/company/acme" in result


def test_deduplication():
    html = """
    <a href="https://facebook.com/acme">FB1</a>
    <a href="https://facebook.com/acme/">FB2</a>
    """
    result = extract_social_links(html)
    assert len(result) == 1


def test_empty():
    assert extract_social_links("") == []
    assert extract_social_links("<p>No links</p>") == []


def test_sample_page():
    with open("tests/fixtures/sample_html/business_page.html") as f:
        html = f.read()
    result = extract_social_links(html)
    assert len(result) == 3  # facebook, linkedin, twitter
