# DIZ Seminar Scraper

A Python tool to scrape seminar information from the Didaktikzentrum (DIZ) website. The scraper collects comprehensive information about seminars including titles, dates, locations, and full descriptions.

## Features

- Scrapes seminar listings from the DIZ website
- Extracts detailed information including:
  - Seminar status
  - Date
  - Title
  - Location
  - Certificate information
  - Area of study
  - Full seminar descriptions
- Saves data in CSV format
- Includes debug mode for troubleshooting
- Handles both regular and "Neuberufene" seminar page formats

## Project Structure

```
.
├── datascraping/
│   ├── __init__.py
│   ├── scraper.py      # Main scraping logic
│   ├── read_csv.py     # CSV analysis tool
│   └── debug_tool.py   # Debug utilities
├── debug/              # Debug output directory
├── pyproject.toml      # Project dependencies
└── README.md
```

## Installation

1. Ensure you have Python 3.8+ installed
2. Install dependencies using uv:
   ```bash
   uv pip install -r pyproject.toml
   ```

## Usage

### Running the Scraper

```bash
uv run datascraping/scraper.py
```

This will:
- Scrape all seminars from the DIZ website
- Save the results to `seminars.csv`
- Create debug files in the `debug/` directory

### Analyzing Results

```bash
uv run datascraping/read_csv.py
```

This will display:
- Number of seminars with/without descriptions
- Example of a seminar description
- Debug file information

## Output Format

The scraper generates a CSV file (`seminars.csv`) with the following columns:
- status: Current seminar status
- date: Seminar date
- title: Seminar title
- location: Location information
- certificate: Certificate type
- area: Area of study
- detail_url: URL to seminar details
- description: Full seminar description
- debug_file: Path to debug file (if any)
