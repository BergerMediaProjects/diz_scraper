import csv
import logging
import requests
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse, unquote

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_sample_urls(csv_file='seminars.csv'):
    """Get a representative sample of URLs with missing content"""
    try:
        urls = set()  # Using set to avoid duplicates
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row['content'] or row['content'].strip() == '':
                    urls.add(row['url'])
        
        # Get unique base paths
        unique_paths = set()
        sample_urls = []
        for url in urls:
            parsed = urlparse(url)
            path = parsed.path
            if path not in unique_paths:
                unique_paths.add(path)
                sample_urls.append(url)
        
        logger.info(f"Found {len(sample_urls)} unique URL patterns to investigate:")
        for url in sample_urls:
            logger.info(f"URL: {url}")
        
        return sample_urls
    
    except FileNotFoundError:
        logger.error(f"Could not find {csv_file}")
        return []
    except Exception as e:
        logger.error(f"Error reading CSV: {e}")
        return []

def fetch_and_save_responses(urls):
    """Fetch and save HTML responses for the given URLs"""
    debug_dir = Path("debug")
    debug_dir.mkdir(exist_ok=True)
    
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            # Create a filename from the URL path
            parsed = urlparse(url)
            path_parts = parsed.path.strip('/').split('/')
            filename = f"debug_response_{path_parts[-1]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            
            # Save the response
            debug_file = debug_dir / filename
            debug_file.write_text(response.text, encoding='utf-8')
            logger.info(f"Saved response for {url} to {filename}")
            
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
        except Exception as e:
            logger.error(f"Error saving response for {url}: {e}")

def main():
    # Get sample URLs
    sample_urls = get_sample_urls()
    if sample_urls:
        # Fetch and save responses
        fetch_and_save_responses(sample_urls)

if __name__ == "__main__":
    main() 