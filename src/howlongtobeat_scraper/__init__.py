"""
HowLongToBeat Scraper - Un scraper robusto para obtener datos de HowLongToBeat.

Este paquete proporciona herramientas para extraer información de videojuegos
desde el sitio web HowLongToBeat, incluyendo tiempos de juego, géneros,
plataformas y más.
"""

from __future__ import annotations

from .api import (
    GameData,
    HowLongToBeatScraper,
    get_game_stats,
    get_game_stats_smart,
    ScraperError,
    GameNotFoundError,
)

__version__ = "1.0.4"
__author__ = "Sermodi"
__email__ = "sermodsoftware@gmail.com"

__all__ = [
    "HowLongToBeatScraper",
    "get_game_stats",
    "get_game_stats_smart",
    "GameData",
    "ScraperError",
    "GameNotFoundError",
]