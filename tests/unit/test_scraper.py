"""Unit tests for the scraper module."""

from bs4 import BeautifulSoup

from src.diz_scraper.core.scraper import (
    clean_text,
    extract_certificate_info,
    extract_fallback_description,
    extract_neuberufene_description,
    extract_regular_description,
    get_description_from_detail_page,
)


def test_clean_text():
    """Test text cleaning functionality."""
    # Test basic cleaning
    assert clean_text("  test  text\n") == "test text"
    
    # Test multiple spaces and newlines
    assert clean_text("multiple   spaces\nand\nnewlines") == "multiple spaces and newlines"
    
    # Test None input
    assert clean_text(None) == ""
    
    # Test empty string
    assert clean_text("") == ""


def test_extract_certificate_info(sample_seminar_list_soup: BeautifulSoup):
    """Test certificate information extraction."""
    # Test with valid certificate cell
    cert_cell = sample_seminar_list_soup.find("td", class_="d-md-none d-none d-lg-table-cell")
    certificate, area = extract_certificate_info(cert_cell)
    assert certificate == "Certificate Type"
    assert area == "Test Area"
    
    # Test with None input
    certificate, area = extract_certificate_info(None)
    assert certificate == ""
    assert area == ""


def test_extract_regular_description(sample_seminar_detail_soup: BeautifulSoup):
    """Test regular seminar description extraction."""
    # Test with valid description div
    desc_div = sample_seminar_detail_soup.find("div", class_="diz-event-details")
    description = extract_regular_description(desc_div)
    assert description == "This is a test seminar description with important details about the content and objectives."
    
    # Test with None input
    assert extract_regular_description(None) is None


def test_extract_neuberufene_description(sample_seminar_detail_soup: BeautifulSoup):
    """Test neuberufene seminar description extraction."""
    # Test with valid content div
    content_div = sample_seminar_detail_soup.find("div", class_="sppb-addon-content")
    description = extract_neuberufene_description(content_div)
    assert description == "This is a test description for neuberufene seminar format. It contains multiple paragraphs of information."
    
    # Test with None input
    assert extract_neuberufene_description(None) is None


def test_extract_fallback_description(sample_seminar_detail_soup: BeautifulSoup):
    """Test fallback description extraction."""
    # Test with valid main content
    main_content = sample_seminar_detail_soup.find("div", id="sp-component")
    description = extract_fallback_description(main_content)
    assert description == "This is fallback content that should only be used if other structures are not found."
    
    # Test with None input
    assert extract_fallback_description(None) is None


def test_get_description_from_detail_page(sample_seminar_detail_soup: BeautifulSoup):
    """Test the complete description extraction process."""
    # Test regular seminar structure
    description = get_description_from_detail_page(sample_seminar_detail_soup)
    assert description == "This is a test seminar description with important details about the content and objectives."
    
    # Test with modified soup to simulate different scenarios
    # Remove regular structure to test neuberufene format
    regular_div = sample_seminar_detail_soup.find("div", class_="diz-event-details")
    if regular_div:
        regular_div.decompose()
    description = get_description_from_detail_page(sample_seminar_detail_soup)
    assert "This is a test description for neuberufene seminar format" in description 