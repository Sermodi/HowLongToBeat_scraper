# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto adhiere al [Versionado Semántico](https://semver.org/lang/es/).

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