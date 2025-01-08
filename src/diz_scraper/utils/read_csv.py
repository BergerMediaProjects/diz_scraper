"""Utility for analyzing scraped seminar data."""

import logging
from pathlib import Path
from typing import Optional, Union

import pandas as pd

from diz_scraper.config import settings
from diz_scraper.utils.helpers import format_file_size, get_file_size

logger = logging.getLogger(__name__)


def analyze_csv(csv_file: Union[str, Path] = settings.DEFAULT_OUTPUT_FILE) -> Optional[pd.DataFrame]:
    """Analyze the contents of a CSV file containing seminar data.
    
    Args:
        csv_file: Path to the CSV file to analyze.
        
    Returns:
        DataFrame containing the seminar data, or None if analysis failed.
    """
    try:
        df = pd.read_csv(csv_file, encoding="utf-8-sig")
        
        # Print basic statistics
        print("\nDescription field analysis:")
        with_desc = df[df["description"].notna() & (df["description"] != "")].shape[0]
        without_desc = df[df["description"].isna() | (df["description"] == "")].shape[0]
        print(f"Number of seminars with description: {with_desc}")
        print(f"Number of seminars without description: {without_desc}")
        
        # Show an example description
        if with_desc > 0:
            example = df[df["description"].notna() & (df["description"] != "")].iloc[0]
            print("\nExample of a description:\n")
            print(f"Title: {example['title']}")
            print(f"Description: {example['description'][:100]}...")
            
        # Analyze debug files
        debug_files = df[df["debug_file"].notna() & (df["debug_file"] != "")]
        print("\nDebug files:")
        print(f"Number of seminars with debug files: {len(debug_files)}")
        
        if not debug_files.empty:
            print("\nExample debug files:")
            print(debug_files["debug_file"].head())
            
            # Check debug file sizes
            total_size = 0
            for file in debug_files["debug_file"]:
                size = get_file_size(file)
                if size:
                    total_size += size
            
            if total_size > 0:
                print(f"\nTotal size of debug files: {format_file_size(total_size)}")
        
        return df
        
    except Exception as e:
        logger.error(f"Error analyzing CSV file: {e}")
        return None


if __name__ == "__main__":
    analyze_csv()
