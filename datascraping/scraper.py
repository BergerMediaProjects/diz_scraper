import csv
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Union

import requests
from bs4 import BeautifulSoup, Tag

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def save_debug_response(response: requests.Response, filename_prefix: str) -> str:
    """Save raw HTML response to a debug file."""
    if not os.path.exists("debug"):
        os.makedirs("debug")
        logger.debug("Created debug directory")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"debug/debug_response_{filename_prefix}_{timestamp}.html"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(response.text)
    logger.debug(f"Saved debug response to {filename}")
    return filename


def extract_seminar_details(detail_url: str, session: requests.Session) -> Optional[Dict[str, str]]:
    """Extract additional information from seminar detail pages."""
    try:
        response = session.get(detail_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract description using the improved function
        description = get_description_from_detail_page(soup)
        if description:
            logger.info(f"Found description for {detail_url}: {description[:100]}...")
        else:
            logger.warning(f"No description found for {detail_url}")

        # Save the raw response to a debug file
        filename = save_debug_response(
            response, detail_url.split("?")[-1].replace("=", "_").replace("/", "_")
        )

        return {"description": description or "", "debug_file": filename}
    except Exception as e:
        logger.error(f"Error fetching detail page {detail_url}: {e}")
        return None


def clean_text(text: Optional[str]) -> str:
    """Clean text by removing extra whitespace and newlines."""
    if not text:
        return ""
    return " ".join(text.replace("\n", " ").split())


def extract_certificate_info(cell: Optional[Tag]) -> tuple[str, str]:
    """Extract structured certificate information."""
    if not cell:
        return "", ""

    text = cell.get_text(strip=True)
    parts = text.split("Bereich:")

    certificate = clean_text(parts[0]) if parts else ""
    area = clean_text(parts[1]) if len(parts) > 1 else ""

    return certificate, area


def extract_regular_description(description_div: Optional[Tag]) -> Optional[str]:
    """Extract description from regular seminar page structure."""
    if not description_div:
        return None

    description_divs = description_div.find_all("div")
    if len(description_divs) >= 2:
        description = description_divs[1].get_text(strip=True)
        if description:
            return clean_description(description)
    return None


def extract_neuberufene_description(content_div: Tag) -> Optional[str]:
    """Extract description from neuberufene seminar page structure."""
    if not content_div:
        return None

    inhalt_h4 = content_div.find("h4", string="Inhalt")
    if not inhalt_h4:
        return None

    description = ""
    next_element = inhalt_h4.find_next()
    while next_element and next_element.name != "h4":
        if next_element.name == "p":
            description += next_element.get_text(strip=True) + " "
        next_element = next_element.find_next()

    if description:
        return clean_description(description)
    return None


def extract_fallback_description(main_content: Optional[Tag]) -> Optional[str]:
    """Extract description from main content as a fallback."""
    if not main_content:
        return None

    text_content = main_content.get_text(strip=True)
    if text_content:
        return clean_description(text_content)
    return None


def clean_description(description: str) -> str:
    """Clean up the description text."""
    description = description.strip()
    if description.startswith("INHALT"):
        description = description[6:].strip()
    return description


def get_description_from_detail_page(detail_page_soup: BeautifulSoup) -> Optional[str]:
    """Extract description from a seminar detail page.

    Tries different page structures in order:
    1. Regular seminar page structure
    2. Neuberufene seminar page structure
    3. Fallback to main content
    """
    try:
        # Try regular seminar page structure
        description_div = detail_page_soup.find("div", class_="diz-event-details")
        if isinstance(description_div, Tag):
            description = extract_regular_description(description_div)
            if description:
                logger.debug("Found description in regular seminar structure")
                return description

        # Try neuberufene seminar page structure
        content_divs = detail_page_soup.find_all("div", class_="sppb-addon-content")
        for content_div in content_divs:
            description = extract_neuberufene_description(content_div)
            if description:
                logger.debug("Found description in neuberufene structure")
                return description

        # Fallback to main content
        main_content = detail_page_soup.find("div", id="sp-component")
        if isinstance(main_content, Tag):
            description = extract_fallback_description(main_content)
            if description:
                logger.debug("Found description in main content")
                return description

        logger.debug("No description found in any structure")

    except Exception as e:
        logger.error(f"Error extracting description: {str(e)}")
        return None

    return None


def scrape_seminars(debug_mode: bool = False) -> Optional[List[Dict[str, str]]]:
    """Scrape seminar information from the website."""
    url = "https://didaktikzentrum.de/programm/aktuelles-programm/simplelist"
    logger.info(f"Starting scraping from {url}")

    # Create a session to maintain cookies
    session = requests.Session()

    try:
        # Fetch the main page
        response = session.get(url)
        response.raise_for_status()
        logger.debug("Successfully fetched main page")

        if debug_mode:
            # Save raw response
            save_debug_response(response, "raw_response")
            logger.debug("Saved raw response in debug mode")

        soup = BeautifulSoup(response.text, "html.parser")

        # Find all seminar rows
        seminar_rows = soup.find_all("tr", itemtype="http://schema.org/Event")
        logger.info(f"Found {len(seminar_rows)} seminars to process")

        seminars: List[Dict[str, str]] = []
        for i, row in enumerate(seminar_rows, 1):
            logger.debug(f"Processing seminar {i}/{len(seminar_rows)}")
            
            # Extract status
            status_img = row.find("img", class_="hasTip")
            status = status_img["title"] if status_img else "Unknown"

            # Extract date
            date_cell = row.find("td", class_="re_startdate")
            date = clean_text(date_cell.get_text()) if date_cell else ""

            # Extract title and link
            title_cell = row.find("td", class_="re_title")
            title_link = title_cell.find("a") if title_cell else None
            title = clean_text(title_link.get_text()) if title_link else ""
            detail_url = title_link["href"] if title_link else ""
            if detail_url and not detail_url.startswith("http"):
                detail_url = "https://didaktikzentrum.de" + detail_url

            # Extract location
            location_cell = row.find("td", class_="re_location")
            location = clean_text(location_cell.get_text()) if location_cell else ""

            # Extract certificate info
            cert_cell = row.find("td", class_="d-md-none d-none d-lg-table-cell")
            certificate, area = extract_certificate_info(cert_cell)

            seminar = {
                "status": status,
                "date": date,
                "title": title,
                "location": location,
                "certificate": certificate,
                "area": area,
                "detail_url": detail_url,
                "description": "",
                "debug_file": "",
            }

            # Fetch details for all seminars with a detail URL
            if detail_url:
                logger.debug(f"Fetching details for seminar: {title}")
                details = extract_seminar_details(detail_url, session)
                if details:
                    seminar.update(details)

            seminars.append(seminar)

        # Save to CSV with proper escaping
        fieldnames = [
            "status",
            "date",
            "title",
            "location",
            "certificate",
            "area",
            "detail_url",
            "description",
            "debug_file",
        ]
        with open("seminars.csv", "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(
                f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL, escapechar="\\"
            )
            writer.writeheader()
            writer.writerows(seminars)

        logger.info(f"Successfully saved {len(seminars)} seminars to seminars.csv")
        return seminars

    except Exception as e:
        logger.error(f"Error during scraping: {e}", exc_info=True)
        return None


if __name__ == "__main__":
    scrape_seminars(debug_mode=True)
