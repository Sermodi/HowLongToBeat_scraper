"""Tests para la clase BrowserManager."""

from unittest.mock import AsyncMock, patch

import pytest

from src.howlongtobeat_scraper.api import BrowserManager, ScraperError


class TestBrowserManager:
    """Tests para la clase BrowserManager."""

    def test_browser_manager_init(self):
        """Test de inicialización de BrowserManager."""
        manager = BrowserManager()

        assert manager._playwright is None
        assert manager._browser is None
        assert manager._user_agent is not None
        assert manager._headless is True
        assert manager._timeout == 30000

    def test_browser_manager_init_with_params(self):
        """Test de inicialización con parámetros personalizados."""
        custom_user_agent = "Custom Agent"
        manager = BrowserManager(
            user_agent=custom_user_agent,
            headless=False,
            timeout=60000,
        )

        assert manager._user_agent == custom_user_agent
        assert manager._headless is False
        assert manager._timeout == 60000

    @pytest.mark.asyncio
    async def test_browser_manager_context_success(self):
        """Test de uso exitoso del context manager."""
        with patch("src.howlongtobeat_scraper.api.async_playwright") as mock_playwright:
            mock_playwright_instance = AsyncMock()
            mock_browser = AsyncMock()
            mock_playwright_instance.chromium.launch.return_value = mock_browser

            # Crear un mock que tenga un método start() awaitable
            mock_playwright_context = AsyncMock()
            mock_playwright_context.start.return_value = mock_playwright_instance
            mock_playwright.return_value = mock_playwright_context

            browser_manager = BrowserManager()
            browser = await browser_manager.__aenter__()
            await browser_manager.__aexit__(None, None, None)

            # Verificar que se llamó a chromium.launch
            mock_playwright_instance.chromium.launch.assert_called_once()
            assert browser is mock_browser

    @pytest.mark.asyncio
    async def test_browser_manager_context_failure(self):
        """Test de fallo en la inicialización del context manager."""
        with patch("src.howlongtobeat_scraper.api.async_playwright") as mock_playwright:
            mock_playwright.return_value.start.side_effect = Exception("Init failed")

            browser_manager = BrowserManager()
            with pytest.raises(ScraperError, match="Error al inicializar el navegador"):
                await browser_manager.__aenter__()

    @pytest.mark.asyncio
    async def test_new_page_success(self):
        """Test de creación exitosa de página."""
        mock_browser = AsyncMock()
        mock_page = AsyncMock()
        mock_browser.new_page.return_value = mock_page

        browser_manager = BrowserManager()
        browser_manager._browser = mock_browser

        page = await browser_manager.new_page()

        assert page is mock_page
        mock_browser.new_page.assert_called_once()
        mock_page.set_default_timeout.assert_called_once_with(30000)

    @pytest.mark.asyncio
    async def test_new_page_no_browser(self):
        """Test de error al crear página sin navegador inicializado."""
        manager = BrowserManager()

        with pytest.raises(ScraperError, match="El navegador no ha sido inicializado"):
            await manager.new_page()

    @pytest.mark.asyncio
    async def test_cleanup_success(self):
        """Test de limpieza exitosa de recursos."""
        mock_browser = AsyncMock()
        mock_playwright = AsyncMock()

        browser_manager = BrowserManager()
        browser_manager._browser = mock_browser
        browser_manager._playwright = mock_playwright

        await browser_manager._cleanup()

        mock_browser.close.assert_called_once()
        mock_playwright.stop.assert_called_once()

    @pytest.mark.asyncio
    async def test_cleanup_with_errors(self):
        """Test de limpieza con errores."""
        mock_browser = AsyncMock()
        mock_playwright = AsyncMock()
        mock_browser.close.side_effect = Exception("Close error")
        mock_playwright.stop.side_effect = Exception("Stop error")

        browser_manager = BrowserManager()
        browser_manager._browser = mock_browser
        browser_manager._playwright = mock_playwright

        # No debe lanzar excepción
        await browser_manager._cleanup()

    @pytest.mark.asyncio
    async def test_cleanup_partial_resources(self):
        """Test de limpieza con recursos parciales."""
        browser_manager = BrowserManager()
        browser_manager._browser = None
        browser_manager._playwright = AsyncMock()

        # No debe lanzar excepción
        await browser_manager._cleanup()

    @pytest.mark.asyncio
    async def test_context_manager_cleanup_on_exception(self):
        """Test de limpieza en caso de excepción."""
        with patch("src.howlongtobeat_scraper.api.async_playwright") as mock_playwright:
            mock_playwright_instance = AsyncMock()
            mock_playwright_instance.chromium.launch.side_effect = Exception(
                "Launch failed"
            )

            # Crear un mock que tenga un método start() awaitable
            mock_playwright_context = AsyncMock()
            mock_playwright_context.start.return_value = mock_playwright_instance
            mock_playwright.return_value = mock_playwright_context

            browser_manager = BrowserManager()

            with pytest.raises(ScraperError, match="Error al inicializar el navegador"):
                await browser_manager.__aenter__()
