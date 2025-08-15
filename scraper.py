from __future__ import annotations

import asyncio
from dataclasses import dataclass

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


@dataclass
class GameData:
    """Representa los datos de tiempo de juego para un videojuego."""
    title: str
    main_story: str | None = None
    main_extra: str | None = None
    completionist: str | None = None


async def get_game_data(game_name: str) -> GameData | None:
    """
    Obtiene los datos de tiempo de juego para un juego específico desde HowLongToBeat.

    Args:
        game_name: El nombre del juego a buscar.

    Returns:
        Un objeto GameData si se encuentra el juego, de lo contrario None.
    """
    print(f"Iniciando scraper para: {game_name}")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # Definimos un User-Agent para simular un navegador real
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = await context.new_page()
        
        search_url = f"https://howlongtobeat.com/?q={game_name.replace(' ', '%20')}"
        print(f"Navegando a: {search_url}")
        
        try:
            await page.goto(search_url, timeout=60000)
            
            print("Esperando por el contenedor de resultados...")
            await page.wait_for_selector('div[class*="GameCard_search_list_details"]', timeout=30000)
            print("Contenedor encontrado.")

            content = await page.content()
            soup = BeautifulSoup(content, "lxml")
            
            game_element = soup.select_one('div[class*="GameCard_search_list_details"]')
            if not game_element:
                print(f"No se encontraron resultados para '{game_name}'.")
                return None

            print("Resultados encontrados. Extrayendo datos...")
            title = game_element.select_one("a").text.strip()
            
            tidbit_elements = game_element.select('div[class*="GameCard_search_list_tidbit__"]')
            
            times = {}
            for i in range(0, len(tidbit_elements), 2):
                category = tidbit_elements[i].text.strip()
                time_value = tidbit_elements[i+1].text.strip()
                
                if "Hours" in time_value:
                    time_value = time_value.split(" ")[0]
                times[category] = time_value

            print("Datos extraídos con éxito.")
            return GameData(
                title=title,
                main_story=times.get("Main Story"),
                main_extra=times.get("Main + Extra"),
                completionist=times.get("Completionist"),
            )

        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            # En caso de error, guardamos artefactos para depuración
            await page.screenshot(path="error_screenshot.png")
            error_content = await page.content()
            with open("error_page.html", "w", encoding="utf-8") as f:
                f.write(error_content)
            print("Artefactos de depuración guardados.")
            return None
        finally:
            print("Cerrando el navegador.")
            await browser.close()


import argparse

# ... (código de GameData y get_game_data sin cambios) ...

async def get_game_data(game_name: str, verbose: bool = False) -> GameData | None:
    """
    Obtiene los datos de tiempo de juego para un juego específico desde HowLongToBeat.

    Args:
        game_name: El nombre del juego a buscar.
        verbose: Si es True, imprime logs detallados.

    Returns:
        Un objeto GameData si se encuentra el juego, de lo contrario None.
    """
    if verbose:
        print(f"Iniciando scraper para: {game_name}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = await context.new_page()
        
        search_url = f"https://howlongtobeat.com/?q={game_name.replace(' ', '%20')}"
        if verbose:
            print(f"Navegando a: {search_url}")
        
        try:
            await page.goto(search_url, timeout=60000)
            
            if verbose:
                print("Esperando por el contenedor de resultados...")
            await page.wait_for_selector('div[class*="GameCard_search_list_details"]', timeout=10000) # Reducimos timeout
            if verbose:
                print("Contenedor encontrado.")

            content = await page.content()
            soup = BeautifulSoup(content, "lxml")
            
            game_element = soup.select_one('div[class*="GameCard_search_list_details"]')
            if not game_element:
                if verbose:
                    print(f"No se encontraron resultados para '{game_name}'.")
                return None

            if verbose:
                print("Resultados encontrados. Extrayendo datos...")
            title = game_element.select_one("a").text.strip()
            
            tidbit_elements = game_element.select('div[class*="GameCard_search_list_tidbit__"]')
            
            times = {}
            for i in range(0, len(tidbit_elements), 2):
                category = tidbit_elements[i].text.strip()
                time_value = tidbit_elements[i+1].text.strip()
                
                if "Hours" in time_value:
                    time_value = time_value.split(" ")[0]
                times[category] = time_value

            if verbose:
                print("Datos extraídos con éxito.")
            return GameData(
                title=title,
                main_story=times.get("Main Story"),
                main_extra=times.get("Main + Extra"),
                completionist=times.get("Completionist"),
            )

        except Exception:
            if verbose:
                print(f"No se encontraron datos para '{game_name}' (posiblemente no existe o no tiene entradas).")
            return None
        finally:
            if verbose:
                print("Cerrando el navegador.")
            await browser.close()


async def main():
    """Función principal que parsea argumentos y ejecuta el scraper."""
    parser = argparse.ArgumentParser(description="Obtener datos de HowLongToBeat para uno o más juegos.")
    parser.add_argument("games", metavar="GAME", type=str, nargs="+", help="Nombre(s) del/de los juego(s) a buscar.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Muestra logs detallados del proceso de scraping.")
    
    args = parser.parse_args()

    for game_name in args.games:
        print(f"\n--- Buscando: {game_name} ---")
        game_data = await get_game_data(game_name, verbose=args.verbose)

        if game_data:
            print(f"Título: {game_data.title}")
            print(f"  Historia Principal: {game_data.main_story or 'N/A'}")
            print(f"  Historia + Extras: {game_data.main_extra or 'N/A'}")
            print(f"  Completista: {game_data.completionist or 'N/A'}")
        else:
            print(f"No se encontraron datos para '{game_name}'.")


if __name__ == "__main__":
    asyncio.run(main())