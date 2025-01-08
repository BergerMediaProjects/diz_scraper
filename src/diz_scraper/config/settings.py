"""Configuration settings for the DIZ scraper."""

from pathlib import Path

# Base URLs
BASE_URL = "https://didaktikzentrum.de"
PROGRAM_LIST_URL = f"{BASE_URL}/programm/aktuelles-programm/simplelist"

# File paths
OUTPUT_DIR = Path("output")
DEBUG_DIR = Path("debug")
DEFAULT_OUTPUT_FILE = OUTPUT_DIR / "seminars.csv"

# Scraping settings
REQUEST_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

# Logging settings
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE = OUTPUT_DIR / "scraper.log"

# Create output directory if it doesn't exist
OUTPUT_DIR.mkdir(exist_ok=True)
DEBUG_DIR.mkdir(exist_ok=True) 