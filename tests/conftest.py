"""Configuración y fixtures para pytest."""

from typing import Generator
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.howlongtobeat_scraper.api import GameData


@pytest.fixture
def sample_game_data() -> GameData:
    """Fixture con datos de juego de ejemplo."""
    return GameData(
        title="The Witcher 3: Wild Hunt",
        main_story="51",
        main_extra="103",
        completionist="173",
    )


@pytest.fixture
def mock_page() -> Generator[AsyncMock, None, None]:
    """Fixture con página mock para tests."""
    page = AsyncMock()
    page.goto = AsyncMock()
    page.wait_for_selector = AsyncMock()
    page.content = AsyncMock()
    page.close = AsyncMock()
    page.set_default_timeout = MagicMock()
    yield page


@pytest.fixture
def mock_browser() -> Generator[AsyncMock, None, None]:
    """Fixture con navegador mock para tests."""
    browser = AsyncMock()
    browser.new_page = AsyncMock()
    browser.close = AsyncMock()
    yield browser


@pytest.fixture
def mock_playwright() -> Generator[AsyncMock, None, None]:
    """Fixture con playwright mock para tests."""
    playwright = AsyncMock()
    playwright.chromium.launch = AsyncMock()
    yield playwright


def pytest_configure(config):
    """Configuración de pytest."""
    config.addinivalue_line(
        "markers", "integration: marca tests de integración que requieren conexión"
    )
    config.addinivalue_line(
        "markers", "slow: marca tests lentos que pueden omitirse en desarrollo"
    )


def pytest_collection_modifyitems(config, items):
    """Modifica la colección de tests para añadir marcadores automáticamente."""
    for item in items:
        # Marca tests que contengan 'integration' en el nombre
        if "integration" in item.nodeid.lower():
            item.add_marker(pytest.mark.integration)

        # Marca tests que contengan 'real' en el nombre como lentos
        if "real" in item.nodeid.lower():
            item.add_marker(pytest.mark.slow)
