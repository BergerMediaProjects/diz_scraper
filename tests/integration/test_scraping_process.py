"""Integration tests for the complete scraping process."""

import os
from pathlib import Path

import pandas as pd
import pytest
import requests

from src.diz_scraper.core.scraper import scrape_seminars


def test_complete_scraping_process(mock_session, tmp_path: Path):
    """Test the complete scraping process from start to finish."""
    # Set up test environment
    output_file = tmp_path / "test_seminars.csv"
    
    # Run the scraper with mock session
    seminars = scrape_seminars(
        output_file=output_file,
        debug_mode=True,
        session=mock_session,
    )
    
    # Verify the results
    assert seminars is not None
    assert len(seminars) == 2  # Based on our sample data
    
    # Check if CSV file was created
    assert output_file.exists()
    
    # Read and verify CSV contents
    df = pd.read_csv(output_file, encoding="utf-8-sig")
    assert len(df) == 2
    
    # Verify first seminar data
    first_seminar = df.iloc[0]
    assert first_seminar["title"] == "Test Seminar Title"
    assert first_seminar["date"] == "01.02.2024"
    assert first_seminar["location"] == "Test Location"
    assert first_seminar["certificate"] == "Certificate Type"
    assert first_seminar["area"] == "Test Area"
    assert "test-seminar" in first_seminar["detail_url"]
    assert first_seminar["status"] == "Available"
    
    # Verify second seminar data
    second_seminar = df.iloc[1]
    assert second_seminar["title"] == "Neuberufene Seminar"
    assert second_seminar["date"] == "15.02.2024"
    assert second_seminar["location"] == "Another Location"
    assert second_seminar["certificate"] == "Another Certificate"
    assert second_seminar["area"] == "Another Area"
    assert "rechtsgrundlagen" in second_seminar["detail_url"]
    assert second_seminar["status"] == "Full"


def test_scraping_with_network_error(tmp_path: Path):
    """Test scraping process handling of network errors."""
    class FailingSession:
        def get(self, *args, **kwargs):
            raise requests.RequestException("Network error")
    
    output_file = tmp_path / "error_test.csv"
    
    # Run scraper with failing session
    result = scrape_seminars(
        output_file=output_file,
        debug_mode=True,
        session=FailingSession(),
    )
    
    assert result is None
    assert not output_file.exists()


def test_scraping_with_invalid_html(tmp_path: Path):
    """Test scraping process handling of invalid HTML."""
    class InvalidHTMLSession:
        def get(self, *args, **kwargs):
            class MockResponse:
                text = "<invalid>html<"
                def raise_for_status(self):
                    pass
            return MockResponse()
    
    output_file = tmp_path / "invalid_html_test.csv"
    
    # Run scraper with invalid HTML session
    result = scrape_seminars(
        output_file=output_file,
        debug_mode=True,
        session=InvalidHTMLSession(),
    )
    
    assert result is None
    assert not output_file.exists()


@pytest.mark.skipif(not os.getenv("RUN_LIVE_TESTS"), reason="Live tests disabled")
def test_live_scraping():
    """Test scraping against the live website.
    
    This test is disabled by default and only runs when RUN_LIVE_TESTS is set.
    """
    output_file = Path("live_test_seminars.csv")
    
    # Run scraper against live site
    seminars = scrape_seminars(
        output_file=output_file,
        debug_mode=True,
    )
    
    assert seminars is not None
    assert len(seminars) > 0
    
    # Clean up
    if output_file.exists():
        output_file.unlink() 