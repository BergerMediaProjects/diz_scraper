# DIZ Scraper

A Python web scraper for extracting seminar information from the Didaktikzentrum website.

## Features

- Scrapes seminar listings from the Didaktikzentrum website
- Extracts detailed information including titles, dates, locations, and descriptions
- Handles multiple seminar page formats (regular and neuberufene)
- Saves results in CSV format with proper UTF-8 encoding
- Comprehensive logging with configurable debug mode
- Debug file generation for troubleshooting
- Command-line interface with customizable options

## Project Structure

```
diz-scraper/
├── src/
│   └── diz_scraper/
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── cli.py
│       │   └── scraper.py
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── helpers.py
│       │   └── read_csv.py
│       └── config/
│           ├── __init__.py
│           └── settings.py
├── pyproject.toml
├── .flake8
├── .gitignore
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd diz-scraper
```

2. Install the package using `uv`:
```bash
uv pip install -e .
```

For development, install additional dependencies:
```bash
uv pip install -e ".[dev]"
```

## Usage

### Basic Usage

Run the scraper with default settings:
```bash
uv run python -m src.diz_scraper.core.cli
```

### Advanced Options

- Enable debug mode:
```bash
uv run python -m src.diz_scraper.core.cli --debug
```

- Specify output file:
```bash
uv run python -m src.diz_scraper.core.cli -o custom_output.csv
```

- Configure request timeout and retries:
```bash
uv run python -m src.diz_scraper.core.cli --timeout 30 --retries 3
```

### Analyzing Results

View statistics about the scraped data:
```bash
uv run python -m src.diz_scraper.utils.read_csv
```

## Output Format

The scraper generates a CSV file with the following columns:

- `status`: Current status of the seminar
- `date`: Date and time of the seminar
- `title`: Title of the seminar
- `location`: Location where the seminar is held
- `certificate`: Certificate information
- `area`: Subject area of the seminar
- `detail_url`: URL to the seminar's detail page
- `description`: Detailed description of the seminar
- `debug_file`: Path to debug file (if debug mode is enabled)

## Development

### Code Style

The project uses:
- `black` for code formatting
- `isort` for import sorting
- `flake8` for linting
- `mypy` for type checking

Run formatters:
```bash
black src/
isort src/
```

Run linters:
```bash
flake8 src/
mypy src/
```

### Testing

Run tests with pytest:
```bash
pytest tests/
```

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]
