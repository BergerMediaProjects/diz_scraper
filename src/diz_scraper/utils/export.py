"""Module for exporting scraped data to different formats."""

import logging
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd

logger = logging.getLogger(__name__)

def export_to_excel(data: List[Dict[Any, Any]], output_path: str | Path) -> bool:
    """
    Export scraped data to an Excel file.
    
    Args:
        data: List of dictionaries containing the scraped data
        output_path: Path where the Excel file should be saved
        
    Returns:
        bool: True if export was successful, False otherwise
    """
    try:
        output_path = Path(output_path)
        
        # Create directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not data:
            logger.error("No data to export to Excel")
            return False
        
        # Convert to DataFrame and export
        df = pd.DataFrame(data)
        df.to_excel(output_path, index=False)
        logger.info(f"Successfully exported data to Excel: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to export to Excel: {e}")
        return False 