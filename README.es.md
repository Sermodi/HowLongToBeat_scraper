# HowLongToBeat Scraper

Un paquete de Python para obtener los tiempos de juego de [HowLongToBeat](https://howlongtobeat.com).

Este paquete proporciona tanto una herramienta de línea de comandos como una API de Python para buscar un juego y obtener sus tiempos estimados para completar la historia principal, extras y completarlo al 100%.

## Características

-   **Interfaz de Línea de Comandos (CLI)**: Obtén los tiempos de juego directamente desde tu terminal.
-   **API de Python**: Integra fácilmente la funcionalidad de HowLongToBeat en tus propios scripts de Python.
-   **Asíncrono**: Construido sobre `asyncio` y `playwright` para un rendimiento eficiente.
-   **Datos Estructurados**: Devuelve los datos en un `dataclass` para un fácil acceso.

## Instalación

### Desde PyPI (Recomendado)

Una vez que el paquete esté disponible en el Índice de Paquetes de Python oficial, podrás instalarlo usando `pip`:

```bash
pip install howlongtobeat-scraper
```

*Nota: Este es el método de instalación previsto para el futuro.*

### Desde TestPyPI

Actualmente, el paquete está disponible en TestPyPI para evaluación. Puedes instalarlo con el siguiente comando:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple howlongtobeat-scraper
```

### Desde el Código Fuente (para Desarrollo)

Si quieres contribuir o instalar la última versión de desarrollo, puedes clonar el repositorio e instalarlo en modo editable:

```bash
git clone https://github.com/Sermodi/HowLongToBeat_scraper.git
cd HowLongToBeat_scraper
pip install -e .
```

## Uso

### Interfaz de Línea de Comandos (CLI)

Una vez instalado, puedes usar el comando `howlongtobeat` seguido del nombre del juego.

```bash
howlongtobeat "The Witcher 3: Wild Hunt"
```

Si el comando no se encuentra en tu PATH (un problema común en Windows), puedes ejecutar el paquete como un módulo:

```bash
python -m howlongtobeat_scraper "The Witcher 3: Wild Hunt"
```

**Salida de Ejemplo:**

```
Buscando "The Witcher 3: Wild Hunt"...
Título: The Witcher 3: Wild Hunt
- Historia Principal: 51.5 horas
- Principal + Extras: 103 horas
- Completista: 172 horas
```

### API de Python

Importa la función `get_game_stats` para usarla en tu código. Es una función síncrona que gestiona internamente un bucle de eventos `asyncio` para el proceso de scraping.

```python
from __future__ import annotations
from howlongtobeat_scraper.api import get_game_stats, GameData

def main():
    game_name = "Celeste"
    print(f"--- Buscando datos para: {game_name} ---")

    try:
        game_data: GameData | None = get_game_stats(game_name)
        if game_data:
            print("Llamada a la API exitosa. Datos recibidos:")
            print(f"  Título: {game_data.title}")
            print(f"  Historia Principal: {game_data.main_story} horas")
            print(f"  Principal + Extras: {game_data.main_extra} horas")
            print(f"  Completista: {game_data.completionist} horas")
        else:
            print("No se encontraron datos para el juego.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()
```