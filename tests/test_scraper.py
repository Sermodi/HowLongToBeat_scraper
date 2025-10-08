"""Tests para la clase HowLongToBeatScraper."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from bs4 import BeautifulSoup
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from src.howlongtobeat_scraper.api import (
    GameData,
    GameNotFoundError,
    HowLongToBeatScraper,
    ScraperError,
)


class TestHowLongToBeatScraper:
    """Tests para la clase HowLongToBeatScraper."""

    def test_scraper_init(self):
        """Test de inicialización del scraper."""
        mock_page = MagicMock()
        scraper = HowLongToBeatScraper(mock_page)

        assert scraper._page is mock_page

    @pytest.mark.asyncio
    async def test_search_empty_game_name(self):
        """Test de búsqueda con nombre vacío."""
        mock_page = AsyncMock()
        scraper = HowLongToBeatScraper(mock_page)

        with pytest.raises(
            ValueError, match="El nombre del juego no puede estar vacío"
        ):
            await scraper.search("")

        with pytest.raises(
            ValueError, match="El nombre del juego no puede estar vacío"
        ):
            await scraper.search("   ")

    @pytest.mark.asyncio
    async def test_search_success(self):
        """Test de búsqueda exitosa."""
        mock_page = AsyncMock()
        mock_page.content.return_value = self._create_mock_html()

        scraper = HowLongToBeatScraper(mock_page)
        result = await scraper.search("Test Game")

        assert isinstance(result, GameData)
        assert result.title == "Test Game"
        assert result.main_story == "10"
        assert result.main_extra == "15"
        assert result.completionist == "20"

        mock_page.goto.assert_called_once()
        mock_page.wait_for_selector.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_timeout(self):
        """Test de timeout en búsqueda."""
        mock_page = AsyncMock()
        mock_page.wait_for_selector.side_effect = PlaywrightTimeoutError("Timeout")
        scraper = HowLongToBeatScraper(mock_page)

        with pytest.raises(
            GameNotFoundError, match="No se pudo cargar la página de resultados"
        ):
            await scraper.search("Test Game")

    @pytest.mark.asyncio
    async def test_search_no_results(self):
        """Test de búsqueda sin resultados."""
        mock_page = AsyncMock()
        mock_page.content.return_value = "<html><body></body></html>"

        scraper = HowLongToBeatScraper(mock_page)

        with pytest.raises(GameNotFoundError, match="No se encontraron resultados"):
            await scraper.search("Nonexistent Game")

    @pytest.mark.asyncio
    async def test_search_unexpected_error(self):
        """Test de error inesperado durante la búsqueda."""
        mock_page = AsyncMock()
        mock_page.goto.side_effect = Exception("Network error")

        scraper = HowLongToBeatScraper(mock_page)

        with pytest.raises(ScraperError, match="Fallo al obtener datos"):
            await scraper.search("Test Game")

    def test_parse_game_data_success(self):
        """Test de parsing exitoso de datos del juego."""
        html = self._create_mock_html()
        soup = BeautifulSoup(html, "lxml")
        game_element = soup.select_one('div[class*="GameCard_search_list_details"]')

        mock_page = MagicMock()
        scraper = HowLongToBeatScraper(mock_page)

        result = scraper._parse_game_data(game_element)

        assert isinstance(result, GameData)
        assert result.title == "Test Game"
        assert result.main_story == "10"
        assert result.main_extra == "15"
        assert result.completionist == "20"

    def test_parse_game_data_with_half_hours(self):
        """Test de parsing con medias horas."""
        html = self._create_mock_html_with_half_hours()
        soup = BeautifulSoup(html, "lxml")
        game_element = soup.select_one('div[class*="GameCard_search_list_details"]')

        mock_page = MagicMock()
        scraper = HowLongToBeatScraper(mock_page)

        result = scraper._parse_game_data(game_element)

        assert result.main_story == "10.5"

    def test_parse_game_data_missing_title(self):
        """Test de parsing sin título."""
        html = """
        <div class="GameCard_search_list_details">
            <div class="GameCard_search_list_tidbit__">Main Story</div>
            <div class="GameCard_search_list_tidbit__">10 Hours</div>
        </div>
        """
        soup = BeautifulSoup(html, "lxml")
        game_element = soup.select_one('div[class*="GameCard_search_list_details"]')

        mock_page = MagicMock()
        scraper = HowLongToBeatScraper(mock_page)

        result = scraper._parse_game_data(game_element)

        assert result.title == "Título no encontrado"

    def test_parse_game_data_odd_elements(self):
        """Test de parsing con número impar de elementos."""
        html = """
        <div class="GameCard_search_list_details">
            <a>Test Game</a>
            <div class="GameCard_search_list_tidbit__">Main Story</div>
            <div class="GameCard_search_list_tidbit__">10 Hours</div>
            <div class="GameCard_search_list_tidbit__">Orphan Element</div>
        </div>
        """
        soup = BeautifulSoup(html, "lxml")
        game_element = soup.select_one('div[class*="GameCard_search_list_details"]')

        mock_page = MagicMock()
        scraper = HowLongToBeatScraper(mock_page)

        result = scraper._parse_game_data(game_element)

        assert result.title == "Test Game"
        assert result.main_story == "10"

    def test_parse_game_data_with_modes(self):
        """Test de parsing con categorías adicionales Solo y Co-Op."""
        html = """
        <div class="GameCard_search_list_details">
            <a>Modes Test Game</a>
            <div class="GameCard_search_list_tidbit__">Solo</div>
            <div class="GameCard_search_list_tidbit__">14½ Hours</div>
            <div class="GameCard_search_list_tidbit__">Co-Op</div>
            <div class="GameCard_search_list_tidbit__">4 Hours</div>
        </div>
        """
        soup = BeautifulSoup(html, "lxml")
        game_element = soup.select_one('div[class*="GameCard_search_list_details"]')

        mock_page = MagicMock()
        scraper = HowLongToBeatScraper(mock_page)

        result = scraper._parse_game_data(game_element)

        assert isinstance(result, GameData)
        assert result.title == "Modes Test Game"
        assert result.solo == "14.5"
        assert result.co_op == "4"

    def test_parse_game_data_error(self):
        """Test de error en el parsing."""
        mock_page = MagicMock()
        scraper = HowLongToBeatScraper(mock_page)

        # Simular un elemento que cause error
        mock_element = MagicMock()
        mock_element.select_one.side_effect = Exception("Parse error")

        with pytest.raises(ScraperError, match="Error al parsear los datos del juego"):
            scraper._parse_game_data(mock_element)

    def _create_mock_html(self) -> str:
        """Crea HTML mock para tests."""
        return """
        <html>
            <body>
                <div class="GameCard_search_list_details__yJrue">
                    <a>Test Game</a>
                    <div class="GameCard_search_list_tidbit__0r_OP">Main Story</div>
                    <div class="GameCard_search_list_tidbit__0r_OP">10 Hours</div>
                    <div class="GameCard_search_list_tidbit__0r_OP">Main + Extra</div>
                    <div class="GameCard_search_list_tidbit__0r_OP">15 Hours</div>
                    <div class="GameCard_search_list_tidbit__0r_OP">Completionist</div>
                    <div class="GameCard_search_list_tidbit__0r_OP">20 Hours</div>
                </div>
            </body>
        </html>
        """

    def _create_mock_html_with_half_hours(self) -> str:
        """Crea HTML mock con medias horas."""
        return """
        <html>
            <body>
                <div class="GameCard_search_list_details__yJrue">
                    <a>Test Game</a>
                    <div class="GameCard_search_list_tidbit__0r_OP">Main Story</div>
                    <div class="GameCard_search_list_tidbit__0r_OP">10½ Hours</div>
                </div>
            </body>
        </html>
        """
