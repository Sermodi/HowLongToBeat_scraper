from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Final

from bs4 import BeautifulSoup, Tag
from playwright.async_api import Browser, Page, Playwright, async_playwright
from playwright.async_api import TimeoutError

# --- Constantes ---
BASE_URL: Final[str] = "https://howlongtobeat.com/?q={game_name}"
USER_AGENT: Final[str] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/91.0.4472.124 Safari/537.36"
)
GAME_CARD_SELECTOR: Final[str] = 'div[class*="GameCard_search_list_details"]'
TIME_CATEGORY_SELECTOR: Final[str] = 'div[class*="GameCard_search_list_tidbit__"]'
SELECTOR_TIMEOUT: Final[int] = 15000

# --- Clases de Datos y Excepciones ---

@dataclass
class GameData:
    """Representa los datos de tiempo de juego para un videojuego."""
    title: str
    main_story: str | None = None
    main_extra: str | None = None
    completionist: str | None = None

class ScraperError(Exception):
    """Excepción base para errores del scraper."""

class GameNotFoundError(ScraperError):
    """Excepción para cuando un juego no se encuentra."""

# --- Lógica del Scraper ---

class BrowserManager:
    """Gestiona el ciclo de vida del navegador Playwright."""

    def __init__(self, user_agent: str = USER_AGENT):
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._user_agent = user_agent

    async def __aenter__(self) -> Browser:
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch()
        return self._browser

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    async def new_page(self) -> Page:
        if not self._browser:
            raise ScraperError("El navegador no ha sido inicializado.")
        return await self._browser.new_page(user_agent=self._user_agent)


class HowLongToBeatScraper:
    """Encapsula la lógica para obtener datos de HowLongToBeat."""

    def __init__(self, page: Page):
        self._page = page

    async def search(self, game_name: str) -> GameData:
        """Busca un juego y extrae sus datos de tiempo."""
        logging.debug(f"Iniciando scraper para: {game_name}")
        search_url = BASE_URL.format(game_name=game_name.replace(" ", "%20"))
        
        try:
            await self._page.goto(search_url)
            await self._page.wait_for_selector(GAME_CARD_SELECTOR, timeout=SELECTOR_TIMEOUT)
            
            content = await self._page.content()
            soup = BeautifulSoup(content, "lxml")
            
            game_element = soup.select_one(GAME_CARD_SELECTOR)
            if not game_element:
                raise GameNotFoundError(f"No se encontraron resultados para '{game_name}'.")

            return self._parse_game_data(game_element)

        except TimeoutError:
            logging.warning(f"Timeout esperando los resultados para '{game_name}'.")
            raise GameNotFoundError(f"No se pudo cargar la página de resultados para '{game_name}'.")
        except Exception as e:
            logging.error(f"Error inesperado durante el scraping de '{game_name}': {e}", exc_info=True)
            raise ScraperError(f"Fallo al obtener datos para '{game_name}'.") from e

    def _parse_game_data(self, game_element: Tag) -> GameData:
        """Parsea el elemento HTML de la tarjeta del juego para extraer los datos."""
        title_element = game_element.select_one("a")
        title = title_element.text.strip() if title_element else "Título no encontrado"

        tidbit_elements = game_element.select(TIME_CATEGORY_SELECTOR)
        times = {}
        for i in range(0, len(tidbit_elements), 2):
            category = tidbit_elements[i].text.strip()
            time_value = tidbit_elements[i+1].text.strip().replace("½", ".5")
            if "Hours" in time_value:
                time_value = time_value.split(" ")[0]
            times[category] = time_value
        
        logging.debug(f"Datos extraídos para '{title}'.")
        return GameData(
            title=title,
            main_story=times.get("Main Story"),
            main_extra=times.get("Main + Extra"),
            completionist=times.get("Completionist"),
        )

# --- API Pública ---

async def _get_game_data_async(game_name: str) -> GameData | None:
    """Wrapper asíncrono para la lógica del scraper."""
    try:
        async with BrowserManager() as browser:
            page = await browser.new_page(user_agent=USER_AGENT)
            scraper = HowLongToBeatScraper(page)
            return await scraper.search(game_name)
    except GameNotFoundError:
        logging.warning(f"El juego '{game_name}' no fue encontrado.")
        return None
    except ScraperError as e:
        logging.error(f"No se pudieron obtener los datos para '{game_name}'. Causa: {e}")
        return None


def get_game_stats(game_name: str) -> GameData | None:
    """
    Punto de entrada síncrono para obtener datos de un juego.

    Esta función es un 'wrapper' que ejecuta la lógica asíncrona del scraper
    y devuelve el resultado. Es ideal para ser usada como una API de biblioteca.

    Args:
        game_name: El nombre del juego a buscar.

    Returns:
        Un objeto GameData si se encuentra, de lo contrario None.
    """
    return asyncio.run(_get_game_data_async(game_name))