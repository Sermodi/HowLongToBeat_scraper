#!/usr/bin/env python3
"""Script para probar el scraper con diferentes modos headless."""

import asyncio
import logging
from src.howlongtobeat_scraper.api import get_game_stats_smart, _get_game_data_with_fallback_async

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

async def test_headless_modes():
    """Probar ambos modos headless."""
    game_name = "Split Fiction"
    
    print("=== Probando con headless=True ===")
    try:
        result_headless = await _get_game_data_with_fallback_async(game_name)
        if result_headless:
            print(f"Título: {result_headless.title}")
            print(f"Solo: {getattr(result_headless, 'solo', 'N/A')}")
            print(f"Co-Op: {getattr(result_headless, 'co_op', 'N/A')}")
        else:
            print("No se encontraron datos")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n=== Probando con get_game_stats_smart ===")
    try:
        result_smart = get_game_stats_smart(game_name)
        if result_smart:
            print(f"Título: {result_smart.title}")
            print(f"Solo: {getattr(result_smart, 'solo', 'N/A')}")
            print(f"Co-Op: {getattr(result_smart, 'co_op', 'N/A')}")
        else:
            print("No se encontraron datos")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_headless_modes())