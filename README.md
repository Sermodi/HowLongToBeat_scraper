# HowLongToBeat Scraper

A Python package to get game completion times from [HowLongToBeat](https://howlongtobeat.com).

This package provides both a command-line tool and a Python API to look up a game and retrieve its estimated times for main story, extras, and 100% completion.

## Features

-   **Command-Line Interface (CLI)**: Get game times directly from your terminal.
-   **Python API**: Easily integrate HowLongToBeat functionality into your own Python scripts.
-   **Asynchronous**: Built on `asyncio` and `playwright` for efficient performance.
-   **Structured Data**: Returns data in a `dataclass` for easy access.

## Installation

You can install the package directly from the Git repository:

```bash
pip install git+https://github.com/Sermodi/HowLongToBeat_scraper.git
```

Or, if you have cloned the repository locally, you can install it in editable mode for development:

```bash
git clone https://github.com/Sermodi/HowLongToBeat_scraper.git
cd HowLongToBeat_scraper
pip install -e .
```

## Usage

### Command-Line Interface (CLI)

Once installed, you can use the `howlongtobeat` command followed by the game's name in quotes.

```bash
howlongtobeat "The Witcher 3: Wild Hunt"
```

If the command is not found in your PATH (common on Windows), you can use:

```bash
python -m howlongtobeat_scraper "The Witcher 3: Wild Hunt"
```

**Example output:**

```
Searching for "The Witcher 3: Wild Hunt"...
Title: The Witcher 3: Wild Hunt
- Main Story: 51.5 hours
- Main + Extras: 103 hours
- Completionist: 172 hours
```

### Python API

Import the `get_game_stats` function to use it in your code. The function is synchronous and handles the `asyncio` event loop internally.

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

## Development

To install development dependencies and run tests, follow these steps:

1.  Clone the repository.
2.  Create and activate a virtual environment.
3.  Install the package in editable mode: `pip install -e .`

## Spanish Documentation

A Spanish version of this README is available at [README.es.md](README.es.md).