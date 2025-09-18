"""Tests para las clases de datos y excepciones."""

import pytest

from src.howlongtobeat_scraper.api import GameData, GameNotFoundError, ScraperError


class TestGameData:
    """Tests para la clase GameData."""

    def test_game_data_creation(self):
        """Test de creación básica de GameData."""
        game = GameData(
            title="The Witcher 3",
            main_story="51.5",
            main_extra="103",
            completionist="173",
        )
        
        assert game.title == "The Witcher 3"
        assert game.main_story == "51.5"
        assert game.main_extra == "103"
        assert game.completionist == "173"

    def test_game_data_with_none_values(self):
        """Test de GameData con valores None."""
        game = GameData(title="Test Game")
        
        assert game.title == "Test Game"
        assert game.main_story is None
        assert game.main_extra is None
        assert game.completionist is None

    def test_game_data_partial_data(self):
        """Test de GameData con datos parciales."""
        game = GameData(
            title="Indie Game",
            main_story="5",
            main_extra=None,
            completionist="10",
        )
        
        assert game.title == "Indie Game"
        assert game.main_story == "5"
        assert game.main_extra is None
        assert game.completionist == "10"

    def test_game_data_equality(self):
        """Test de igualdad entre instancias de GameData."""
        game1 = GameData(title="Test", main_story="10")
        game2 = GameData(title="Test", main_story="10")
        game3 = GameData(title="Different", main_story="10")
        
        assert game1 == game2
        assert game1 != game3

    def test_game_data_repr(self):
        """Test de representación string de GameData."""
        game = GameData(title="Test Game", main_story="10")
        repr_str = repr(game)
        
        assert "GameData" in repr_str
        assert "Test Game" in repr_str
        assert "10" in repr_str


class TestExceptions:
    """Tests para las excepciones personalizadas."""

    def test_scraper_error_inheritance(self):
        """Test de herencia de ScraperError."""
        error = ScraperError("Test error")
        
        assert isinstance(error, Exception)
        assert str(error) == "Test error"

    def test_game_not_found_error_inheritance(self):
        """Test de herencia de GameNotFoundError."""
        error = GameNotFoundError("Game not found")
        
        assert isinstance(error, ScraperError)
        assert isinstance(error, Exception)
        assert str(error) == "Game not found"

    def test_exception_chaining(self):
        """Test de encadenamiento de excepciones."""
        original_error = ValueError("Original error")
        
        with pytest.raises(ScraperError) as exc_info:
            try:
                raise original_error
            except ValueError as e:
                raise ScraperError("Wrapped error") from e
        
        assert exc_info.value.__cause__ is original_error