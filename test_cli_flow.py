#!/usr/bin/env python3
"""Script que simula el flujo del CLI."""

import logging
from src.howlongtobeat_scraper.api import get_game_stats_smart

# Configurar logging igual que en el CLI
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def test_cli_flow():
    """Simula el flujo del CLI."""
    game_name = "Split Fiction"
    print(f"--- Buscando: {game_name} ---")
    
    game_data = get_game_stats_smart(game_name)
    
    if game_data:
        print(f"Título: {game_data.title}")
        print(f"  Historia Principal: {game_data.main_story or 'N/A'}")
        print(f"  Historia + Extras: {game_data.main_extra or 'N/A'}")
        print(f"  Completista: {game_data.completionist or 'N/A'}")
        # Campos adicionales cuando existan en la tarjeta del juego
        if getattr(game_data, "solo", None):
            print(f"  Solo: {game_data.solo}")
        if getattr(game_data, "co_op", None):
            print(f"  Co-Op: {game_data.co_op}")
    else:
        print(f"No se encontraron datos para '{game_name}'.")

if __name__ == "__main__":
    test_cli_flow()