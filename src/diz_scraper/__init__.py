"""
DIZ Scraper - A web scraper for the Didaktikzentrum website.

This package provides functionality to scrape seminar information from the
Didaktikzentrum website and process the scraped data.
"""

from diz_scraper.core.scraper import scrape_seminars
from diz_scraper.utils.read_csv import analyze_csv

__version__ = "0.1.0"
__all__ = ["scrape_seminars", "analyze_csv"]
