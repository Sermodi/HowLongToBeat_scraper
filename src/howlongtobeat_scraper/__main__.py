"""Interfaz de línea de comandos para HowLongToBeat Scraper.

Este módulo proporciona una CLI para buscar tiempos de juego desde
HowLongToBeat.com usando argumentos de línea de comandos.
"""

from __future__ import annotations

import argparse
import logging
import sys
from typing import NoReturn

from .api import get_game_stats


def setup_logging(verbose: bool) -> None:
    """Configura el sistema de logging.

    Args:
        verbose: Si debe mostrar logs detallados (DEBUG) o solo INFO.
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def print_game_data(game_name: str, game_data: object) -> None:
    """Imprime los datos del juego de forma formateada.

    Args:
        game_name: Nombre del juego buscado.
        game_data: Datos del juego o None si no se encontró.
    """
    if game_data:
        print(f"Título: {game_data.title}")
        print(f"  Historia Principal: {game_data.main_story or 'N/A'}")
        print(f"  Historia + Extras: {game_data.main_extra or 'N/A'}")
        print(f"  Completista: {game_data.completionist or 'N/A'}")
    else:
        print(f"No se encontraron datos para '{game_name}'.")
    print()  # Línea en blanco para separar resultados


def create_parser() -> argparse.ArgumentParser:
    """Crea y configura el parser de argumentos.

    Returns:
        Parser de argumentos configurado.
    """
    parser = argparse.ArgumentParser(
        description="Obtener datos de HowLongToBeat para uno o más juegos.",
        epilog="Ejemplo: howlongtobeat 'The Witcher 3' 'Cyberpunk 2077'",
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
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0",
        help="Muestra la versión del programa.",
    )
    return parser


def main() -> NoReturn:
    """Función principal que parsea argumentos y ejecuta el scraper.

    Esta función no retorna normalmente, siempre termina con sys.exit().
    """
    parser = create_parser()
    args = parser.parse_args()

    setup_logging(args.verbose)

    success_count = 0
    total_count = len(args.games)

    for game_name in args.games:
        logging.info(f"--- Buscando: {game_name} ---")

        try:
            game_data = get_game_stats(game_name)
            print_game_data(game_name, game_data)

            if game_data:
                success_count += 1

        except KeyboardInterrupt:
            print("\nOperación cancelada por el usuario.")
            sys.exit(1)
        except Exception as e:
            logging.error(f"Error inesperado al procesar '{game_name}': {e}")
            print(f"Error al procesar '{game_name}'. Ver logs para detalles.")
            print()

    # Resumen final
    if total_count > 1:
        print(f"Procesados {success_count}/{total_count} juegos exitosamente.")

    # Código de salida: 0 si todos exitosos, 1 si algunos fallaron
    exit_code = 0 if success_count == total_count else 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
