# HowLongToBeat Scraper

[![PyPI version](https://badge.fury.io/py/howlongtobeat-scraper.svg)](https://badge.fury.io/py/howlongtobeat-scraper)
[![Python versions](https://img.shields.io/pypi/pyversions/howlongtobeat-scraper.svg)](https://pypi.org/project/howlongtobeat-scraper/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/howlongtobeat-scraper)](https://pepy.tech/project/howlongtobeat-scraper)

A Python package to get game completion times from [HowLongToBeat](https://howlongtobeat.com).

This package provides both a command-line tool and a Python API to look up a game and retrieve its estimated times for main story, extras, and 100% completion.

## Features

-   **Command-Line Interface (CLI)**: Get game times directly from your terminal.
-   **Python API**: Easily integrate HowLongToBeat functionality into your own Python scripts.
-   **Asynchronous**: Built on `asyncio` and `playwright` for efficient performance.
-   **Structured Data**: Returns data in a `dataclass` for easy access.

## Installation

### From PyPI (Official Release)

Install the package from the official Python Package Index:

```bash
pip install howlongtobeat-scraper
```

After installation, you need to install Playwright browsers:

```bash
playwright install
```

**Note**: The package is now officially available on PyPI at: https://pypi.org/project/howlongtobeat-scraper/

### From Source (for Development)

If you want to contribute or install the latest development version, you can clone the repository and install it in editable mode:

```bash
git clone https://github.com/Sermodi/HowLongToBeat_scraper.git
cd HowLongToBeat_scraper
pip install -e .
```

## Usage

### Command-Line Interface (CLI)

Once installed, you can run the package as a module:

```bash
python -m howlongtobeat_scraper "The Witcher 3: Wild Hunt"
```

**Note**: Use the module format above as it works consistently across all platforms.

**Example Output:**

```
Searching for "The Witcher 3: Wild Hunt"...
Title: The Witcher 3: Wild Hunt
- Main Story: 51.5 hours
- Main + Extras: 103 hours
- Completionist: 172 hours
```

### Python API

Import the `get_game_stats` function to use it in your code. It's a synchronous function that internally manages an `asyncio` event loop for the scraping process.

```python
from __future__ import annotations
from howlongtobeat_scraper.api import get_game_stats, GameData

def main():
    game_name = "Celeste"
    print(f"--- Fetching data for: {game_name} ---")

    try:
        game_data: GameData | None = get_game_stats(game_name)
        if game_data:
            print("API call successful. Data received:")
            print(f"  Title: {game_data.title}")
            print(f"  Main Story: {game_data.main_story} hours")
            print(f"  Main + Extras: {game_data.main_extra} hours")
            print(f"  Completionist: {game_data.completionist} hours")
        else:
            print("No data found for the game.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
```

## Spanish Documentation

A Spanish version of this README is available at [README.es.md](README.es.md).
