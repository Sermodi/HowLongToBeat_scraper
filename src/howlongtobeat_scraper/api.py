"""Scraper para obtener tiempos de juego desde HowLongToBeat.com.

Este módulo proporciona una API para extraer información de tiempos de juego
desde el sitio web HowLongToBeat.com utilizando web scraping con Playwright.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Final

from bs4 import BeautifulSoup, Tag
from playwright.async_api import (
    Browser,
    Page,
    Playwright,
    TimeoutError,
    async_playwright,
)

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
    """Representa los datos de tiempo de juego para un videojuego.

    Attributes:
        title: El título del juego.
        main_story: Tiempo para completar la historia principal (en horas).
        main_extra: Tiempo para completar historia + extras (en horas).
        completionist: Tiempo para completar al 100% (en horas).

    Example:
        >>> game = GameData(
        ...     title="The Witcher 3",
        ...     main_story="51.5",
        ...     main_extra="103",
        ...     completionist="173"
        ... )
        >>> print(f"{game.title}: {game.main_story}h")
        The Witcher 3: 51.5h
    """

    title: str
    main_story: str | None = None
    main_extra: str | None = None
    completionist: str | None = None


class ScraperError(Exception):
    """Excepción base para errores del scraper.

    Esta es la excepción base de la cual heredan todas las demás
    excepciones específicas del scraper.
    """


class GameNotFoundError(ScraperError):
    """Excepción lanzada cuando un juego no se encuentra en HowLongToBeat.

    Se lanza cuando la búsqueda no devuelve resultados para el juego especificado.
    """


# --- Lógica del Scraper ---


class BrowserManager:
    """Gestiona el ciclo de vida del navegador Playwright."""

    def __init__(self, user_agent: str = USER_AGENT, headless: bool = True):
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._user_agent = user_agent
        self._headless = headless

    async def __aenter__(self) -> Browser:
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(headless=self._headless)
        return self._browser

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    async def new_page(self, user_agent: str = None) -> Page:
        if not self._browser:
            raise ScraperError("El navegador no ha sido inicializado.")
        ua = user_agent or self._user_agent
        return await self._browser.new_page(user_agent=ua)


class HowLongToBeatScraper:
    """Encapsula la lógica para obtener datos de HowLongToBeat.

    Esta clase maneja el proceso de scraping de la página web de HowLongToBeat,
    incluyendo la navegación, extracción de datos y parsing del HTML.

    Args:
        page: Instancia de página de Playwright para realizar el scraping.

    Example:
        >>> async with BrowserManager() as browser:
        ...     page = await browser.new_page()
        ...     scraper = HowLongToBeatScraper(page)
        ...     data = await scraper.search("The Witcher 3")
        ...     print(f"{data.title}: {data.main_story}h")
    """

    def __init__(self, page: Page) -> None:
        self._page = page

    async def search(self, game_name: str) -> GameData:
        """Busca un juego y extrae sus datos de tiempo.

        Args:
            game_name: Nombre del juego a buscar.

        Returns:
            Datos del juego encontrado.

        Raises:
            GameNotFoundError: Si no se encuentra el juego o no se puede cargar la página.
            ScraperError: Si ocurre un error durante el scraping.
        """
        if not game_name.strip():
            raise ValueError("El nombre del juego no puede estar vacío")

        logging.debug(f"Iniciando scraper para: {game_name}")
        search_url = BASE_URL.format(game_name=game_name.replace(" ", "%20"))

        try:
            # Configuraciones anti-detección para la página
            await self._page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en'],
                });
                
                window.chrome = {
                    runtime: {},
                };
            """)
            
            # Navegar con configuraciones adicionales
            await self._page.goto(search_url, wait_until="domcontentloaded")
            
            # Esperar un poco para que la página se cargue completamente
            await self._page.wait_for_timeout(1000)
            
            await self._page.wait_for_selector(
                GAME_CARD_SELECTOR, timeout=SELECTOR_TIMEOUT
            )

            content = await self._page.content()
            soup = BeautifulSoup(content, "lxml")

            game_element = soup.select_one(GAME_CARD_SELECTOR)
            if not game_element:
                raise GameNotFoundError(
                    f"No se encontraron resultados para '{game_name}'."
                )

            return self._parse_game_data(game_element)

        except TimeoutError:
            logging.warning(f"Timeout esperando los resultados para '{game_name}'.")
            raise GameNotFoundError(
                f"No se pudo cargar la página de resultados para '{game_name}'."
            ) from None
        except (GameNotFoundError, ValueError):
            raise
        except Exception as e:
            logging.error(
                f"Error inesperado durante el scraping de '{game_name}': {e}",
                exc_info=True,
            )
            raise ScraperError(f"Fallo al obtener datos para '{game_name}'.") from e

    def _parse_game_data(self, game_element: Tag) -> GameData:
        """Parsea el elemento HTML de la tarjeta del juego para extraer los datos.

        Args:
            game_element: Elemento HTML que contiene los datos del juego.

        Returns:
            Datos parseados del juego.

        Raises:
            ScraperError: Si no se pueden parsear los datos correctamente.
        """
        try:
            title_element = game_element.select_one("a")
            title = (
                title_element.text.strip() if title_element else "Título no encontrado"
            )

            tidbit_elements = game_element.select(TIME_CATEGORY_SELECTOR)
            times: dict[str, str] = {}

            for i in range(0, len(tidbit_elements), 2):
                if i + 1 < len(tidbit_elements):
                    category = tidbit_elements[i].text.strip()
                    time_value = tidbit_elements[i + 1].text.strip().replace("½", ".5")
                    if "Hours" in time_value:
                        time_value = time_value.split(" ")[0]
                    times[category] = time_value

            logging.debug(f"Datos extraídos para '{title}': {times}")
            return GameData(
                title=title,
                main_story=times.get("Main Story"),
                main_extra=times.get("Main + Extra"),
                completionist=times.get("Completionist"),
            )
        except Exception as e:
            logging.error(f"Error al parsear datos del juego: {e}", exc_info=True)
            raise ScraperError("Error al parsear los datos del juego") from e


# --- API Pública ---


async def _get_game_data_with_fallback_async(game_name: str) -> GameData | None:
    """Intenta obtener datos del juego con estrategia de fallback automático.
    
    Primero intenta en modo headless (invisible). Si falla, reintenta en modo
    no-headless (visible) para evitar detección de bots.
    
    Args:
        game_name: Nombre del juego a buscar.
        
    Returns:
        Datos del juego si se encuentra, None en caso contrario.
    """
    # Primer intento: modo headless (invisible)
    logging.debug(f"Intentando búsqueda en modo headless para: {game_name}")
    try:
        async with BrowserManager(headless=True) as browser:
            page = await browser.new_page(user_agent=USER_AGENT)
            scraper = HowLongToBeatScraper(page)
            result = await scraper.search(game_name)
            logging.info(f"Búsqueda exitosa en modo headless para: {game_name}")
            return result
    except (GameNotFoundError, ScraperError) as e:
        logging.warning(f"Falló búsqueda headless para '{game_name}': {e}")
    
    # Segundo intento: modo no-headless (visible) como fallback
    logging.debug(f"Intentando búsqueda en modo visible para: {game_name}")
    try:
        async with BrowserManager(headless=False) as browser:
            page = await browser.new_page(user_agent=USER_AGENT)
            scraper = HowLongToBeatScraper(page)
            result = await scraper.search(game_name)
            logging.info(f"Búsqueda exitosa en modo visible para: {game_name}")
            return result
    except GameNotFoundError:
        logging.warning(f"El juego '{game_name}' no fue encontrado en ningún modo.")
        return None
    except ScraperError as e:
        logging.error(f"Error en ambos modos para '{game_name}': {e}")
        return None


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
        logging.error(
            f"No se pudieron obtener los datos para '{game_name}'. Causa: {e}"
        )
        return None
    except Exception as e:
        logging.error(
            f"Error inesperado al obtener datos para '{game_name}': {e}",
            exc_info=True,
        )
        return None


def get_game_stats(game_name: str) -> GameData | None:
    """Punto de entrada síncrono para obtener datos de un juego.

    Esta función es un wrapper que ejecuta la lógica asíncrona del scraper
    y devuelve el resultado. Es ideal para ser usada como una API de biblioteca.

    Args:
        game_name: El nombre del juego a buscar.

    Returns:
        Un objeto GameData si se encuentra, None en caso contrario.

    Example:
        >>> data = get_game_stats("The Witcher 3")
        >>> if data:
        ...     print(f"{data.title}: {data.main_story}h")
        ... else:
        ...     print("Juego no encontrado")
    """
    if not isinstance(game_name, str):
        raise TypeError("game_name debe ser una cadena de texto")

    return asyncio.run(_get_game_data_async(game_name))


def get_game_stats_smart(game_name: str) -> GameData | None:
    """Punto de entrada síncrono con estrategia de fallback automático.

    Esta función intenta primero en modo headless (invisible) y si falla,
    automáticamente reintenta en modo visible para evitar detección de bots.
    Esto minimiza la molestia al usuario mientras mantiene la funcionalidad.

    Args:
        game_name: El nombre del juego a buscar.

    Returns:
        Un objeto GameData si se encuentra, None en caso contrario.

    Example:
        >>> data = get_game_stats_smart("The Witcher 3")
        >>> if data:
        ...     print(f"{data.title}: {data.main_story}h")
        ... else:
        ...     print("Juego no encontrado")

    Note:
        Esta función es recomendada sobre get_game_stats() ya que reduce
        la necesidad de mostrar el navegador al usuario en la mayoría de casos.
    """
    if not isinstance(game_name, str):
        raise TypeError("game_name debe ser una cadena de texto")

    return asyncio.run(_get_game_data_with_fallback_async(game_name))
