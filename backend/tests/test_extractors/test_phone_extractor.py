from extractors.phone_extractor import extract_phones


def test_extract_tel_link():
    html = '<a href="tel:+13125550100">Call</a>'
    result = extract_phones(html)
    assert "+13125550100" in result


def test_extract_us_format():
    html = "<p>Phone: +1 (312) 555-0100</p>"
    result = extract_phones(html)
    assert any("13125550100" in p for p in result)


def test_extract_dot_format():
    html = "<p>312.555.0100</p>"
    result = extract_phones(html)
    assert any("3125550100" in p for p in result)


def test_extract_dash_format():
    html = "<p>312-555-0100</p>"
    result = extract_phones(html)
    assert any("3125550100" in p for p in result)


def test_filters_short_numbers():
    html = "<p>123 and 456789</p>"
    assert extract_phones(html) == []


def test_deduplication():
    html = """
    <a href="tel:+13125550100">+1 (312) 555-0100</a>
    <p>312-555-0100</p>
    """
    result = extract_phones(html)
    # All normalize to same number
    unique_digits = set(p.replace("+", "") for p in result)
    assert len(unique_digits) <= 2


def test_empty_html():
    assert extract_phones("") == []


def test_sample_page():
    with open("tests/fixtures/sample_html/business_page.html") as f:
        html = f.read()
    result = extract_phones(html)
    assert len(result) >= 1
