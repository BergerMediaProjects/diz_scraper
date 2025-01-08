"""Test configuration and shared fixtures."""

import os
from pathlib import Path
from typing import Generator

import pytest
import requests
from bs4 import BeautifulSoup

# Constants for testing
TEST_DATA_DIR = Path(__file__).parent / "fixtures"
TEST_OUTPUT_DIR = Path(__file__).parent / "output"


@pytest.fixture(autouse=True)
def setup_test_env() -> Generator[None, None, None]:
    """Set up test environment variables and directories."""
    # Create test output directory
    TEST_OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Store original environment
    original_env = dict(os.environ)
    
    # Set test environment variables
    os.environ["DIZ_OUTPUT_DIR"] = str(TEST_OUTPUT_DIR)
    os.environ["DIZ_DEBUG_MODE"] = "true"
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def sample_seminar_list_html() -> str:
    """Load sample seminar list HTML from fixture file."""
    with open(TEST_DATA_DIR / "sample_seminar_list.html", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def sample_seminar_detail_html() -> str:
    """Load sample seminar detail HTML from fixture file."""
    with open(TEST_DATA_DIR / "sample_seminar_detail.html", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def mock_session(sample_seminar_list_html: str, sample_seminar_detail_html: str) -> Generator:
    """Create a mock requests session that returns fixture data."""
    class MockResponse:
        def __init__(self, text: str, status_code: int = 200):
            self.text = text
            self.status_code = status_code

        def raise_for_status(self) -> None:
            if self.status_code >= 400:
                raise requests.HTTPError(f"HTTP Error: {self.status_code}")

    class MockSession:
        def __init__(self) -> None:
            self.calls = []

        def get(self, url: str, **kwargs) -> MockResponse:
            self.calls.append({"url": url, "kwargs": kwargs})
            if "programm/aktuelles-programm/simplelist" in url:
                return MockResponse(sample_seminar_list_html)
            elif "details" in url:
                return MockResponse(sample_seminar_detail_html)
            return MockResponse("", 404)

    session = MockSession()
    yield session


@pytest.fixture
def sample_seminar_list_soup(sample_seminar_list_html: str) -> BeautifulSoup:
    """Create BeautifulSoup object from sample seminar list HTML."""
    return BeautifulSoup(sample_seminar_list_html, "html.parser")


@pytest.fixture
def sample_seminar_detail_soup(sample_seminar_detail_html: str) -> BeautifulSoup:
    """Create BeautifulSoup object from sample seminar detail HTML."""
    return BeautifulSoup(sample_seminar_detail_html, "html.parser") 