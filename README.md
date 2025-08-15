# HowLongToBeat Scraper

## Descripción

Este proyecto contiene un script de Python para hacer scraping de los tiempos de juego (historia principal, extras, completista) desde el sitio web HowLongToBeat.com. La herramienta utiliza Playwright para controlar un navegador y BeautifulSoup para parsear el HTML.

## Instalación

1.  **Clonar el repositorio o descargar los archivos.**

2.  **Crear y activar un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Instalar los navegadores de Playwright:**
    ```bash
    playwright install
    ```

## Uso

El script se ejecuta desde la línea de comandos, aceptando uno o más nombres de juegos como argumentos.

### Sintaxis

```bash
python scraper.py "Nombre del Juego 1" "Nombre del Juego 2" ... [OPCIONES]
```

### Argumentos

*   `GAME`: (Requerido) El nombre de uno o más juegos a buscar. Deben ir entre comillas si contienen espacios.
*   `-v`, `--verbose`: (Opcional) Muestra logs detallados del proceso de scraping, útil para depuración.

### Ejemplos

**Buscar un solo juego:**

```bash
python scraper.py "The Witcher 3: Wild Hunt"
```

**Buscar múltiples juegos:**

```bash
python scraper.py "Hades" "Stardew Valley" "Cyberpunk 2077"
```

**Buscar con logs detallados:**

```bash
python scraper.py "Elden Ring" -v
```

## Dependencias

Las dependencias del proyecto se listan en el archivo `requirements.txt`:

*   `beautifulsoup4`
*   `lxml`
*   `playwright`