#!/usr/bin/env python3
"""Script de prueba para verificar el parsing."""

import asyncio
import logging
from src.howlongtobeat_scraper.api import BrowserManager, HowLongToBeatScraper, USER_AGENT

# Configurar logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

async def test_split_fiction():
    """Prueba el parsing de Split Fiction."""
    async with BrowserManager(headless=False) as browser:
        page = await browser.new_page(user_agent=USER_AGENT)
        scraper = HowLongToBeatScraper(page)
        
        try:
            result = await scraper.search("Split Fiction")
            print(f"Resultado: {result}")
            print(f"Solo: {getattr(result, 'solo', None)}")
            print(f"Co-Op: {getattr(result, 'co_op', None)}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_split_fiction())