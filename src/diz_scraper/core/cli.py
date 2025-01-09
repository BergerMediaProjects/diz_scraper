"""Command line interface for the DIZ scraper."""

import logging

from ..core.scraper import scrape_seminars

def main():
    # Add more detailed logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    logger.info("Starting scraper...")
    seminars = scrape_seminars()
    
    if seminars:
        logger.info(f"Successfully scraped {len(seminars)} seminars")
        logger.info("Files saved in output/seminars.csv and output/seminars.xlsx")
    else:
        logger.error("No seminars were scraped")

if __name__ == "__main__":
    main() 