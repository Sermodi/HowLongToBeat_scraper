#!/usr/bin/env python3
"""Script de prueba directo."""

import asyncio
import logging
from src.howlongtobeat_scraper.api import _get_game_data_with_fallback_async

# Configurar logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

async def test_direct():
    """Prueba directa."""
    result = await _get_game_data_with_fallback_async("Split Fiction")
    print(f"Resultado: {result}")
    if result:
        print(f"Solo: {getattr(result, 'solo', None)}")
        print(f"Co-Op: {getattr(result, 'co_op', None)}")

if __name__ == "__main__":
    asyncio.run(test_direct())