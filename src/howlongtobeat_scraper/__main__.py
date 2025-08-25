from __future__ import annotations

import argparse
import logging

# Hacemos una importación relativa desde el mismo paquete
from .api import get_game_stats


def main():
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
        # Llamamos a la nueva función síncrona de la API
        game_data = get_game_stats(game_name)

        if game_data:
            # La salida final se mantiene con print para una UI limpia
            print(f"Título: {game_data.title}")
            print(f"  Historia Principal: {game_data.main_story or 'N/A'}")
            print(f"  Historia + Extras: {game_data.main_extra or 'N/A'}")
            print(f"  Completista: {game_data.completionist or 'N/A'}")
        else:
            logging.warning(f"No se pudo obtener información para '{game_name}'.")


if __name__ == "__main__":
    main()
