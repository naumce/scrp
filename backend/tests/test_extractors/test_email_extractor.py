from extractors.email_extractor import extract_emails


def test_extract_mailto():
    html = '<a href="mailto:info@company.com">Contact</a>'
    assert extract_emails(html) == ["info@company.com"]


def test_extract_plain_text():
    html = "<p>Reach us at sales@company.com or support@company.com</p>"
    result = extract_emails(html)
    assert "sales@company.com" in result
    assert "support@company.com" in result


def test_deduplication():
    html = """
    <a href="mailto:info@test.com">info@test.com</a>
    <p>info@test.com</p>
    """
    assert extract_emails(html) == ["info@test.com"]


def test_filters_example_domains():
    html = "<p>user@example.com and real@company.com</p>"
    assert extract_emails(html) == ["real@company.com"]


def test_filters_image_files():
    html = "<p>logo@2x.png and info@company.com</p>"
    result = extract_emails(html)
    assert "info@company.com" in result
    assert not any("png" in e for e in result)


def test_case_insensitive():
    html = "<p>INFO@Company.COM</p>"
    assert extract_emails(html) == ["info@company.com"]


def test_empty_html():
    assert extract_emails("") == []
    assert extract_emails("<p>No emails here</p>") == []


def test_sample_page():
    with open("tests/fixtures/sample_html/business_page.html") as f:
        html = f.read()
    result = extract_emails(html)
    assert "info@acme-mfg.com" in result
    assert "sales@acme-mfg.com" in result
