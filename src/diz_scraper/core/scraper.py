"""Core scraping functionality for the DIZ scraper."""

import csv
import logging
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union

import requests
from bs4 import BeautifulSoup, Tag

from ..config import settings

logger = logging.getLogger(__name__)


def save_debug_response(response: requests.Response, filename_prefix: str) -> str:
    """Save raw HTML response to a debug file.
    
    Args:
        response: The response to save.
        filename_prefix: Prefix for the debug file name.
        
    Returns:
        Path to the saved debug file.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = settings.DEBUG_DIR / f"debug_response_{filename_prefix}_{timestamp}.html"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(response.text)
    logger.debug(f"Saved debug response to {filename}")
    return str(filename)


def extract_seminar_details(
    detail_url: str,
    session: requests.Session,
    timeout: int = settings.REQUEST_TIMEOUT,
    max_retries: int = settings.MAX_RETRIES,
) -> Optional[Dict[str, str]]:
    """Extract additional information from seminar detail pages.
    
    Args:
        detail_url: URL of the detail page.
        session: Requests session to use.
        timeout: Request timeout in seconds.
        max_retries: Maximum number of retries for failed requests.
        
    Returns:
        Dictionary containing description and debug file path, or None if extraction failed.
    """
    for attempt in range(max_retries):
        try:
            response = session.get(detail_url, timeout=timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            description = get_description_from_detail_page(soup)
            if description:
                logger.info(f"Found description for {detail_url}: {description[:100]}...")
            else:
                logger.warning(f"No description found for {detail_url}")

            filename = save_debug_response(
                response, detail_url.split("?")[-1].replace("=", "_").replace("/", "_")
            )

            return {"description": description or "", "debug_file": filename}
            
        except requests.RequestException as e:
            logger.warning(f"Attempt {attempt + 1}/{max_retries} failed for {detail_url}: {e}")
            if attempt < max_retries - 1:
                time.sleep(settings.RETRY_DELAY)
            continue
            
        except Exception as e:
            logger.error(f"Error processing detail page {detail_url}: {e}")
            return None
            
    logger.error(f"Failed to fetch detail page {detail_url} after {max_retries} attempts")
    return None


def clean_text(text: Optional[str]) -> str:
    """Clean text by removing extra whitespace and newlines.
    
    Args:
        text: Text to clean.
        
    Returns:
        Cleaned text.
    """
    if not text:
        return ""
    return " ".join(text.replace("\n", " ").split())


def extract_certificate_info(cell: Optional[Tag]) -> tuple[str, str]:
    """Extract structured certificate information.
    
    Args:
        cell: Table cell containing certificate information.
        
    Returns:
        Tuple of (certificate, area).
    """
    if not cell:
        return "", ""

    text = cell.get_text(strip=True)
    parts = text.split("Bereich:")

    certificate = clean_text(parts[0]) if parts else ""
    area = clean_text(parts[1]) if len(parts) > 1 else ""

    return certificate, area


def extract_regular_description(description_div: Optional[Tag]) -> Optional[str]:
    """Extract description from regular seminar page structure.
    
    Args:
        description_div: Div containing the description.
        
    Returns:
        Extracted description or None if not found.
    """
    if not description_div:
        return None

    description_divs = description_div.find_all("div")
    if len(description_divs) >= 2:
        description = description_divs[1].get_text(strip=True)
        if description:
            return clean_description(description)
    return None


def extract_neuberufene_description(content_div: Tag) -> Optional[str]:
    """Extract description from neuberufene seminar page structure.
    
    Args:
        content_div: Div containing the content.
        
    Returns:
        Extracted description or None if not found.
    """
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
    """Extract description from main content as a fallback.
    
    Args:
        main_content: Main content div.
        
    Returns:
        Extracted description or None if not found.
    """
    if not main_content:
        return None

    text_content = main_content.get_text(strip=True)
    if text_content:
        return clean_description(text_content)
    return None


def clean_description(description: str) -> str:
    """Clean up the description text.
    
    Args:
        description: Description text to clean.
        
    Returns:
        Cleaned description.
    """
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
    
    Args:
        detail_page_soup: BeautifulSoup object of the detail page.
        
    Returns:
        Extracted description or None if not found.
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


def scrape_seminars(
    output_file: Union[str, Path] = settings.DEFAULT_OUTPUT_FILE,
    debug_mode: bool = False,
    timeout: int = settings.REQUEST_TIMEOUT,
    max_retries: int = settings.MAX_RETRIES,
) -> Optional[List[Dict[str, str]]]:
    """Scrape seminar information from the website.
    
    Args:
        output_file: Path to save the CSV output.
        debug_mode: Whether to enable debug mode.
        timeout: Request timeout in seconds.
        max_retries: Maximum number of retries for failed requests.
        
    Returns:
        List of dictionaries containing seminar information, or None if scraping failed.
    """
    logger.info(f"Starting scraping from {settings.PROGRAM_LIST_URL}")

    # Create a session to maintain cookies
    session = requests.Session()

    try:
        # Fetch the main page
        response = session.get(settings.PROGRAM_LIST_URL, timeout=timeout)
        response.raise_for_status()
        logger.debug("Successfully fetched main page")

        if debug_mode:
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
                detail_url = f"{settings.BASE_URL}{detail_url}"

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
                details = extract_seminar_details(
                    detail_url,
                    session,
                    timeout=timeout,
                    max_retries=max_retries,
                )
                if details:
                    seminar.update(details)

            seminars.append(seminar)

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

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
        with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(
                f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL, escapechar="\\"
            )
            writer.writeheader()
            writer.writerows(seminars)

        logger.info(f"Successfully saved {len(seminars)} seminars to {output_file}")
        return seminars

    except Exception as e:
        logger.error(f"Error during scraping: {e}", exc_info=True)
        return None


if __name__ == "__main__":
    scrape_seminars(debug_mode=True)
