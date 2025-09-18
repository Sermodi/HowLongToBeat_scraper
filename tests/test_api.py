"""Tests de integración para las funciones públicas de la API."""

from unittest.mock import AsyncMock, patch

import pytest

from src.howlongtobeat_scraper.api import (
    GameData,
    GameNotFoundError,
    ScraperError,
    _get_game_data_async,
    get_game_stats,
)


class TestPublicAPI:
    """Tests para las funciones públicas de la API."""

    @pytest.mark.asyncio
    async def test_get_game_data_async_success(self):
        """Test de función asíncrona exitosa."""
        mock_game_data = GameData(
            title="Test Game", main_story="10", main_extra="15", completionist="20"
        )

        with patch(
            "src.howlongtobeat_scraper.api.BrowserManager"
        ) as mock_browser_manager:
            mock_page = AsyncMock()
            mock_browser = AsyncMock()
            mock_browser.__aenter__.return_value = mock_browser
            mock_browser.__aexit__.return_value = None
            mock_browser.new_page.return_value = mock_page
            mock_browser_manager.return_value = mock_browser

            with patch(
                "src.howlongtobeat_scraper.api.HowLongToBeatScraper"
            ) as mock_scraper_class:
                mock_scraper = AsyncMock()
                mock_scraper.search.return_value = mock_game_data
                mock_scraper_class.return_value = mock_scraper

                result = await _get_game_data_async("Test Game")

                assert result == mock_game_data
                mock_scraper.search.assert_called_once_with("Test Game")

    @pytest.mark.asyncio
    async def test_get_game_data_async_browser_error(self):
        """Test de error del navegador."""
        with patch(
            "src.howlongtobeat_scraper.api.BrowserManager"
        ) as mock_browser_manager:
            mock_browser_manager.side_effect = ScraperError("Browser error")

            result = await _get_game_data_async("Test Game")
            assert result is None

    @pytest.mark.asyncio
    async def test_get_game_data_async_scraper_error(self):
        """Test de error del scraper."""
        with patch(
            "src.howlongtobeat_scraper.api.BrowserManager"
        ) as mock_browser_manager:
            AsyncMock()
            mock_browser = AsyncMock()
            mock_page = AsyncMock()

            mock_browser_manager.return_value.__aenter__.return_value = mock_browser
            mock_browser.new_page.return_value = mock_page

            with patch(
                "src.howlongtobeat_scraper.api.HowLongToBeatScraper"
            ) as mock_scraper:
                mock_scraper.return_value.search.side_effect = GameNotFoundError(
                    "Game not found"
                )

                result = await _get_game_data_async("Test Game")
                assert result is None

    def test_get_game_stats_success(self):
        """Test de función síncrona exitosa."""
        mock_game_data = GameData(
            title="Test Game", main_story="10", main_extra="15", completionist="20"
        )

        with patch("asyncio.run") as mock_asyncio_run:
            mock_asyncio_run.return_value = mock_game_data

            result = get_game_stats("Test Game")

            assert result == mock_game_data
            mock_asyncio_run.assert_called_once()

    def test_get_game_stats_invalid_input(self):
        """Test de entrada inválida."""
        with pytest.raises(TypeError, match="game_name debe ser una cadena de texto"):
            get_game_stats(123)  # type: ignore

    def test_get_game_stats_game_not_found(self):
        """Test de juego no encontrado."""
        with patch("src.howlongtobeat_scraper.api._get_game_data_async") as mock_async:
            mock_async.return_value = None

            result = get_game_stats("Nonexistent Game")
            assert result is None

    def test_get_game_stats_scraper_error(self):
        """Test de error del scraper."""
        with patch("src.howlongtobeat_scraper.api._get_game_data_async") as mock_async:
            mock_async.return_value = None

            result = get_game_stats("Test Game")
            assert result is None

    def test_get_game_stats_unexpected_error(self):
        """Test de error inesperado."""
        with patch("src.howlongtobeat_scraper.api._get_game_data_async") as mock_async:
            mock_async.return_value = None

            result = get_game_stats("Test Game")
            assert result is None

    def test_get_game_stats_exception_error(self):
        """Test de excepción general."""
        with patch("src.howlongtobeat_scraper.api._get_game_data_async") as mock_async:
            mock_async.return_value = None

            result = get_game_stats("Test Game")
            assert result is None


@pytest.mark.integration
class TestIntegrationAPI:
    """Tests de integración más realistas (requieren conexión)."""

    @pytest.mark.skip(reason="Requiere conexión a internet y es lento")
    def test_real_game_search(self):
        """Test con un juego real (solo para desarrollo)."""
        # Este test se puede ejecutar manualmente para verificar
        # que la integración funciona con el sitio real
        result = get_game_stats("The Witcher 3")

        assert isinstance(result, GameData)
        assert result.title
        assert result.main_story

    @pytest.mark.skip(reason="Requiere conexión a internet")
    def test_real_game_not_found(self):
        """Test con un juego que no existe (solo para desarrollo)."""
        with pytest.raises(GameNotFoundError):
            get_game_stats("ThisGameDoesNotExist12345")
