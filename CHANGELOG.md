# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto adhiere al [Versionado Semántico](https://semver.org/lang/es/).

## [1.0.4] - 2024-01-XX

### Añadido
- **Nueva función `get_game_stats_smart()`**: Implementa estrategia de fallback automático
- Fallback automático: intenta modo headless primero, luego modo visible si falla
- Logging detallado para rastrear intentos de fallback y éxito/fallo de cada modo
- Exportación de `get_game_stats_smart` en el módulo principal

### Mejorado
- **Funcionalidad restaurada**: Revertido a configuraciones estables de la versión 0.2.1
- Eliminadas configuraciones anti-detección problemáticas que causaban detección de bots
- User-Agent simplificado para mejor compatibilidad
- `BrowserManager` simplificado con soporte para parámetro `headless`
- Documentación actualizada con ejemplos de la nueva función recomendada

### Corregido
- **Problema crítico**: Resuelto fallo de detección de bots en modo headless
- Configuraciones de navegador revertidas a versión funcional
- Eliminados flags `--disable-*` que causaban detección como bot

### Técnico
- Nueva función `_get_game_data_with_fallback_async()` para lógica de fallback
- `BrowserManager` actualizado con soporte para parámetro `headless`
- Método `new_page()` actualizado para aceptar `user_agent` opcional
- Tests de integración para verificar estrategia de fallback

### Notas de migración
- **Recomendado**: Usar `get_game_stats_smart()` en lugar de `get_game_stats()`
- `get_game_stats()` mantiene compatibilidad hacia atrás
- La nueva función minimiza la visibilidad del navegador automáticamente

## [1.0.3] - 2024-01-XX (DEPRECATED - Problemas de detección de bots)

### Añadido
- Parámetro `headless` en `get_game_stats()` para controlar la visibilidad del navegador
- Configuraciones anti-detección avanzadas para evitar bloqueos por detección de bots
- Soporte para modo no-headless como alternativa cuando el modo headless falla
- Documentación actualizada con ejemplos de uso del parámetro `headless`

### Mejorado
- User-Agent actualizado a Chrome 120.0.0.0 para mayor compatibilidad
- Configuraciones del navegador optimizadas con flags anti-detección
- Headers HTTP adicionales para simular navegación humana
- Scripts de inicialización para ocultar propiedades de automatización
- Tiempo de espera adicional para carga completa de páginas

### Técnico
- Refactorización de `BrowserManager` con opciones de lanzamiento avanzadas
- Mejoras en el método `search` con configuraciones de página anti-detección
- Tests actualizados para soportar la nueva signatura de funciones
- Documentación técnica expandida sobre detección de bots

### Notas de migración
- La función `get_game_stats()` ahora acepta un parámetro opcional `headless=True`
- El comportamiento por defecto permanece igual (modo headless)
- Para mayor confiabilidad, se recomienda usar `headless=False` si se experimentan timeouts

## [1.0.0] - 2024-01-XX

### Añadido
- Primera versión estable del HowLongToBeat Scraper
- API Python completa para obtener tiempos de juego desde HowLongToBeat.com
- Interfaz de línea de comandos (CLI) funcional
- Soporte para búsqueda de múltiples juegos
- Manejo robusto de errores y excepciones personalizadas
- Documentación completa con docstrings
- Tests comprehensivos con 97% de cobertura
- Soporte para Python 3.8+
- Configuración de herramientas de desarrollo (black, ruff, pytest)

### Características principales
- **Scraping asíncrono**: Utiliza Playwright para un rendimiento eficiente
- **Datos estructurados**: Retorna datos en dataclass para fácil acceso
- **CLI intuitiva**: Herramienta de línea de comandos fácil de usar
- **Manejo de errores**: Excepciones específicas para diferentes tipos de errores
- **Logging**: Sistema de logging configurable para debugging
- **Type hints**: Código completamente tipado para mejor desarrollo

### Técnico
- Arquitectura limpia con separación de responsabilidades
- Context managers para gestión automática de recursos
- Parsing robusto de HTML con BeautifulSoup
- Configuración moderna con pyproject.toml
- Pre-commit hooks para calidad de código
- Integración continua con pytest y coverage

## [0.2.2] - 2024-01-XX

### Cambiado
- Mejoras en la estabilidad del scraper
- Optimizaciones en el manejo de timeouts

## [0.2.1] - 2024-01-XX

### Añadido
- Versión inicial beta del proyecto
- Funcionalidad básica de scraping
- Tests iniciales

[1.0.0]: https://github.com/Sermodi/HowLongToBeat_scraper/compare/v0.2.2...v1.0.0
[0.2.2]: https://github.com/Sermodi/HowLongToBeat_scraper/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/Sermodi/HowLongToBeat_scraper/releases/tag/v0.2.1