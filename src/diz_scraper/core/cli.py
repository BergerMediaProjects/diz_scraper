"""Command-line interface for the DIZ scraper."""

import argparse
import logging
from pathlib import Path
from typing import Optional

from ..config import settings


def setup_logging(debug: bool = False) -> None:
    """Set up logging configuration.
    
    Args:
        debug: Whether to enable debug logging.
    """
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format=settings.LOG_FORMAT,
        datefmt=settings.LOG_DATE_FORMAT,
        handlers=[
            logging.FileHandler(settings.LOG_FILE),
            logging.StreamHandler(),
        ],
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.
    
    Returns:
        Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Scrape seminar information from the Didaktikzentrum website."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=settings.DEFAULT_OUTPUT_FILE,
        help="Output CSV file path (default: %(default)s)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode with additional logging and debug files",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=settings.REQUEST_TIMEOUT,
        help="Request timeout in seconds (default: %(default)s)",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=settings.MAX_RETRIES,
        help="Maximum number of retries for failed requests (default: %(default)s)",
    )
    
    return parser.parse_args()


def main() -> Optional[int]:
    """Main entry point for the scraper CLI.
    
    Returns:
        Exit code (0 for success, non-zero for error) or None.
    """
    args = parse_args()
    setup_logging(args.debug)
    
    try:
        from .scraper import scrape_seminars
        
        seminars = scrape_seminars(
            output_file=args.output,
            debug_mode=args.debug,
            timeout=args.timeout,
            max_retries=args.retries,
        )
        
        if seminars is None:
            logging.error("Scraping failed")
            return 1
            
        logging.info(f"Successfully scraped {len(seminars)} seminars")
        return 0
        
    except Exception as e:
        logging.exception("An error occurred during scraping")
        return 1


if __name__ == "__main__":
    exit(main()) 