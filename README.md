# HowLongToBeat Scraper

## Descripción

Este proyecto contiene un script de Python para hacer scraping de los tiempos de juego (historia principal, extras, completista) desde el sitio web [HowLongToBeat.com](https://howlongtobeat.com). La herramienta utiliza `playwright` para controlar un navegador de forma asíncrona y `BeautifulSoup` para parsear el HTML de manera eficiente.

## Características

- **Búsqueda de Múltiples Juegos**: Permite buscar uno o varios juegos en una sola ejecución.
- **Scraping Asíncrono**: Utiliza `asyncio` y `playwright` para realizar las peticiones de forma no bloqueante.
- **Manejo de Errores**: Controla casos donde un juego no se encuentra y notifica al usuario.
- **Normalización de Datos**: Convierte automáticamente tiempos fraccionarios (ej. "4½ Hours") a formato decimal (ej. "4.5").
- **Logging Detallado**: Ofrece un modo `--verbose` para seguir paso a paso el proceso de scraping, ideal para depuración.
- **Código Limpio y Modular**: Estructurado con constantes, funciones bien definidas y tipado estático para facilitar su mantenimiento.

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

*   `juegos`: (Requerido) El nombre de uno o más juegos a buscar. Deben ir entre comillas si contienen espacios.
*   `-v`, `--verbose`: (Opcional) Activa el logging detallado (`DEBUG`). Muestra cada paso del proceso de scraping, como la navegación, la espera de elementos y la extracción de datos. Es muy útil para depurar si algo no funciona como se espera.

### Ejemplos

**Buscar un solo juego:**
```bash
python scraper.py "The Witcher 3: Wild Hunt"
```

**Buscar múltiples juegos:**
```bash
python scraper.py "Hades" "Stardew Valley" "Cyberpunk 2077"
```

**Buscar con logs detallados para depuración:**
```bash
python scraper.py "Elden Ring" -v
```

## Dependencias

Las dependencias del proyecto se listan en el archivo `requirements.txt`:

*   `beautifulsoup4`
*   `lxml`
*   `playwright`

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar este proyecto, por favor, abre un *issue* para discutir los cambios o envía una *pull request*.