from __future__ import annotations

import argparse
import asyncio
import logging
from dataclasses import dataclass
from typing import Final

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

# --- Constantes ---
BASE_URL: Final[str] = "https://howlongtobeat.com/?q={game_name}"
USER_AGENT: Final[str] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/91.0.4472.124 Safari/537.36"
)
GAME_CARD_SELECTOR: Final[str] = 'div[class*="GameCard_search_list_details"]'
TIME_CATEGORY_SELECTOR: Final[str] = 'div[class*="GameCard_search_list_tidbit__"]'
# Timeout para esperar selectores en la página (en milisegundos)
SELECTOR_TIMEOUT: Final[int] = 15000


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
    logging.debug(f"Iniciando scraper para: {game_name}")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(user_agent=USER_AGENT)
        page = await context.new_page()

        search_url = BASE_URL.format(game_name=game_name.replace(" ", "%20"))
        logging.debug(f"Navegando a: {search_url}")

        try:
            await page.goto(search_url)

            logging.debug("Esperando por el contenedor de resultados...")
            await page.wait_for_selector(GAME_CARD_SELECTOR, timeout=SELECTOR_TIMEOUT)
            logging.debug("Contenedor de resultados encontrado.")

            content = await page.content()
            soup = BeautifulSoup(content, "lxml")

            game_element = soup.select_one(GAME_CARD_SELECTOR)
            if not game_element:
                logging.warning(f"No se encontraron resultados para '{game_name}'.")
                return None

            logging.debug("Resultados encontrados. Extrayendo datos...")
            title = game_element.select_one("a").text.strip()

            tidbit_elements = game_element.select(TIME_CATEGORY_SELECTOR)

            times = {}
            for i in range(0, len(tidbit_elements), 2):
                category = tidbit_elements[i].text.strip()
                time_value = tidbit_elements[i + 1].text.strip()

                # Reemplaza la fracción ½ por .5 para un parseo correcto.
                time_value = time_value.replace("½", ".5")

                if "Hours" in time_value:
                    time_value = time_value.split(" ")[0]
                times[category] = time_value

            logging.debug("Datos extraídos con éxito.")
            return GameData(
                title=title,
                main_story=times.get("Main Story"),
                main_extra=times.get("Main + Extra"),
                completionist=times.get("Completionist"),
            )

        except Exception as e:
            logging.error(
                f"No se pudieron obtener los datos para '{game_name}'. Causa: {e}",
                exc_info=True,
            )
            return None
        finally:
            logging.debug("Cerrando el navegador.")
            await browser.close()


async def main():
    """Función principal que parsea argumentos y ejecuta el scraper."""
    parser = argparse.ArgumentParser(
        description="Obtener datos de HowLongToBeat para uno o más juegos."
    )
    parser.add_argument(
        "games",
        metavar="GAME",
        type=str,
        nargs="+",
        help="Nombre(s) del/de los juego(s) a buscar.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Muestra logs detallados del proceso de scraping.",
    )

    args = parser.parse_args()

    # Configuración del logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    for game_name in args.games:
        logging.info(f"--- Buscando: {game_name} ---")
        game_data = await get_game_data(game_name)

        if game_data:
            # La salida final se mantiene con print para una UI limpia
            print(f"Título: {game_data.title}")
            print(f"  Historia Principal: {game_data.main_story or 'N/A'}")
            print(f"  Historia + Extras: {game_data.main_extra or 'N/A'}")
            print(f"  Completista: {game_data.completionist or 'N/A'}")
        else:
            logging.warning(f"No se pudo obtener información para '{game_name}'.")


if __name__ == "__main__":
    asyncio.run(main())