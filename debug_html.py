#!/usr/bin/env python3
"""Script de debug para inspeccionar el HTML de HowLongToBeat."""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def debug_split_fiction():
    """Inspecciona el HTML de Split Fiction para debug."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Navegar a la búsqueda de Split Fiction
        search_url = "https://howlongtobeat.com/?q=Split%20Fiction"
        await page.goto(search_url, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        
        # Esperar a que aparezcan los resultados
        try:
            await page.wait_for_selector('div[class*="GameCard_search_list_details"]', timeout=15000)
        except:
            print("No se encontraron elementos de juego")
            await browser.close()
            return
        
        # Obtener el HTML
        content = await page.content()
        soup = BeautifulSoup(content, "lxml")
        
        # Buscar el primer resultado
        game_element = soup.select_one('div[class*="GameCard_search_list_details"]')
        if game_element:
            print("=== HTML del primer resultado ===")
            print(game_element.prettify())
            print("\n=== Elementos con tidbit_short ===")
            short_elements = game_element.select('div[class*="GameCard_search_list_tidbit_short__"]')
            for i, elem in enumerate(short_elements):
                print(f"{i}: {elem.get('class')} -> '{elem.text.strip()}'")
            
            print("\n=== Elementos con tidbit_long ===")
            long_elements = game_element.select('div[class*="GameCard_search_list_tidbit_long__"]')
            for i, elem in enumerate(long_elements):
                print(f"{i}: {elem.get('class')} -> '{elem.text.strip()}'")
        else:
            print("No se encontró el elemento del juego")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_split_fiction())