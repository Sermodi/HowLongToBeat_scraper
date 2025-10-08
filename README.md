# HowLongToBeat Scraper

[![PyPI version](https://badge.fury.io/py/howlongtobeat-scraper.svg)](https://badge.fury.io/py/howlongtobeat-scraper)
[![Python versions](https://img.shields.io/pypi/pyversions/howlongtobeat-scraper.svg)](https://pypi.org/project/howlongtobeat-scraper/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/howlongtobeat-scraper)](https://pepy.tech/project/howlongtobeat-scraper)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python package to get game completion times from [HowLongToBeat](https://howlongtobeat.com).

This package provides both a command-line tool and a Python API to look up a game and retrieve its estimated times for main story, extras, and 100% completion.

## Features

-   **Command-Line Interface (CLI)**: Get game times directly from your terminal.
-   **Python API**: Easily integrate HowLongToBeat functionality into your own Python scripts.
-   **Co-Op Game Support**: Automatically detects and extracts both Solo and Co-Op playtimes for cooperative games.
-   **Traditional Game Support**: Handles standard games with Main Story, Main + Extras, and Completionist times.
-   **Asynchronous**: Built on `asyncio` and `playwright` for efficient performance.
-   **Structured Data**: Returns data in a `dataclass` for easy access.
-   **Robust Parsing**: Updated selectors ensure compatibility with HowLongToBeat's current website structure.

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

**Example Output (Traditional Game):**

```
Searching for "The Witcher 3: Wild Hunt"...
Title: The Witcher 3: Wild Hunt
- Main Story: 51.5 hours
- Main + Extras: 103 hours
- Completionist: 172 hours
```

**Example Output (Co-Op Game):**

```
Searching for "It Takes Two"...
Title: It Takes Two
- Solo: 14 hours
- Co-Op: 14 hours
```

### Python API

The package provides two main functions for retrieving game data:

#### Recommended: `get_game_stats_smart` (with automatic fallback)

This is the **recommended** function that automatically handles browser visibility for you:

```python
from __future__ import annotations
from howlongtobeat_scraper.api import get_game_stats_smart, GameData

def main():
    # Example with traditional game
    game_name = "Celeste"
    print(f"--- Fetching data for: {game_name} ---")

    try:
        # Smart function with automatic fallback
        # Tries headless first, falls back to visible mode if needed
        game_data: GameData | None = get_game_stats_smart(game_name)
        
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

    # Example with Co-Op game
    coop_game = "It Takes Two"
    print(f"\n--- Fetching data for: {coop_game} ---")
    
    try:
        coop_data: GameData | None = get_game_stats_smart(coop_game)
        
        if coop_data:
            print("API call successful. Data received:")
            print(f"  Title: {coop_data.title}")
            print(f"  Solo: {coop_data.solo} hours")
            print(f"  Co-Op: {coop_data.coop} hours")
        else:
            print("No data found for the game.")
    except Exception as e:
        print(f"An error occurred: {e}")
```

#### Manual control: `get_game_stats`

For manual control over browser visibility, you can use the original function:

```python
from howlongtobeat_scraper.api import get_game_stats

# Always headless (invisible browser)
game_data = get_game_stats("Game Name")

# Always visible browser (for debugging or when headless fails)
game_data = get_game_stats("Game Name", headless=False)
```

### Browser Visibility and Fallback Strategy

#### Automatic Fallback (Recommended)

The `get_game_stats_smart` function implements an intelligent fallback strategy:

1. **First attempt**: Tries headless mode (invisible browser) for better performance
2. **Automatic fallback**: If headless fails due to bot detection, automatically retries with visible browser
3. **User-friendly**: Minimizes browser visibility while ensuring reliability

```python
# Recommended: automatic fallback strategy
data = get_game_stats_smart("Game Name")
```

#### Manual Control

For specific use cases, you can manually control browser visibility with `get_game_stats`:

- **`get_game_stats("Game Name")`**: Always uses headless mode (invisible)
- **`get_game_stats("Game Name", headless=False)`**: Always shows browser window

```python
# Always headless (faster but may fail on some sites)
data = get_game_stats("Game Name")

# Always visible (more reliable but shows browser window)
data = get_game_stats("Game Name", headless=False)
```

**Recommendation**: Use `get_game_stats_smart()` for the best balance of performance and reliability.

## Spanish Documentation

A Spanish version of this README is available at [README.es.md](README.es.md).