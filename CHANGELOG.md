# Changelog

## [5.0.0] - 2025-01-16 🌐

### 🎉 NUEVA INTERFAZ WEB COMPLETA
- **Interfaz web moderna**: Dashboard completo con Bootstrap 5 y diseño responsive
- **Panel de control visual**: Iniciar/detener simulador sin línea de comandos
- **Configuración gráfica**: Formularios web para todos los parámetros (TCP/RTU, dispositivos, intervalos)
- **Monitoreo en tiempo real**: WebSocket con gráficos interactivos de corrientes, voltajes y potencias
- **Editor visual de registros**: Modificación de archivos JSON con validación automática

### 🔌 API REST Y CONECTIVIDAD
- **API REST completa**: Endpoints para control, configuración y datos
- **WebSocket en tiempo real**: Actualizaciones automáticas cada 2 segundos
- **Múltiples clientes**: Soporte para varios navegadores simultáneos
- **Reconexión automática**: Manejo robusto de desconexiones de red

### 📱 EXPERIENCIA DE USUARIO
- **Accesible desde navegador**: Compatible con Chrome, Firefox, Safari, Edge
- **Diseño responsive**: Funciona en móviles y tablets
- **Tema adaptivo**: Soporte automático para modo oscuro/claro
- **Contraste mejorado**: Colores optimizados para accesibilidad

### 🛠️ NUEVOS ARCHIVOS
- **web_ui.py**: Servidor web principal con FastAPI
- **run_web_ui.bat/.ps1**: Scripts de lanzamiento para Windows
- **web/templates/**: 4 páginas HTML modernas (dashboard, config, monitor, registers)
- **web/static/**: CSS y JavaScript con paleta de colores mejorada

### ✅ COMPATIBILIDAD TOTAL
- **CLI original 100% funcional**: Todos los comandos inalterados
- **Tests pasan**: 16/16 sin modificaciones
- **Funcionalidades preservadas**: Simulación Modbus completa

## [4.0.0] - 2025-09-28 🚀

### 🎉 Refactorización Completa
- **Arquitectura modular**: Código organizado en módulos especializados (`src/`)
- **Estructura profesional**: Separación clara de responsabilidades
- **Documentación mejorada**: README completamente actualizado con ejemplos

### ✨ Nuevas Características
- **Generadores avanzados**: 6 tipos de generadores incluyendo ondas senoidales y ruido
- **Thread safety**: Generación segura de datos con locks
- **Logging mejorado**: Mensajes informativos con emojis y mejor formato
- **Configuración flexible**: Archivos JSON con validación y campos adicionales (unit, category)
- **Scripts de utilidad**: Demo, instalación y Makefile para desarrollo

### 🧪 Testing y Calidad
- **Tests unitarios completos**: Cobertura para generadores y funcionalidad core
- **Tests de integración**: Validación de carga de archivos y configuración
- **Herramientas de desarrollo**: Black, flake8, mypy, pytest
- **CI/CD ready**: pyproject.toml configurado para herramientas modernas

### 🛠️ Herramientas de Desarrollo
- **Makefile completo**: Comandos para desarrollo, testing y ejecución
- **Scripts de instalación**: Automatización de setup
- **Validación de configuración**: Verificación automática de archivos JSON
- **Formateo automático**: Estilo consistente con Black

### 🔧 Mejoras Técnicas
- **Manejo de errores mejorado**: Try-catch específicos y mensajes informativos
- **Compatibilidad Windows**: 3 alternativas a Make (Batch, PowerShell, Python)
- **Performance optimizada**: Estructuras de datos eficientes
- **Extensibilidad**: Arquitectura preparada para nuevas funcionalidades

### 📦 Nuevos Archivos y Reorganización
- **src/**: Nuevo directorio con código modular
- **tests/**: Suite completa de tests unitarios
- **config/**: Archivos JSON con ejemplos mejorados
- **make.bat/make.ps1**: Scripts Windows alternativos
- **requirements-dev.txt**: Dependencias de desarrollo
- **pyproject.toml**: Configuración moderna del proyecto

### 🔄 Compatibilidad y Migración
- **virtual_pm_CLI.py**: Versión original preservada
- **virtual_pm_CLI_refactored.py**: Nueva versión refactorizada
- **Configuración JSON**: Compatible con archivos existentes
- **API Modbus**: Misma interfaz externa

## [3.0.0] - 2025-09-27

### 🌟 Mejoras Significativas
- **Compatibilidad Windows mejorada**: Scripts batch y PowerShell
- **Generadores de datos**: uniform, sine, noise, fixed, timestamp, randint
- **Configuración JSON**: Sistema flexible de configuración
- **Logging detallado**: Información clara sobre el estado del simulador

### 🐛 Correcciones
- **Compatibilidad Python 3.9+**: Soporte para versiones recientes
- **Manejo de errores**: Gestión robusta de archivos y conexiones
- **Documentación**: README mejorado con ejemplos detallados

## [2.0.0] - 2025-09-26

### 🚀 Funcionalidades Principales
- **Simulación dual**: Soporte para 1 o 2 medidores simultáneos
- **Protocolo Modbus RTU**: Además del TCP existente
- **Generación automática**: Valores realistas de medidores de potencia
- **Configuración flexible**: Parámetros personalizables

### 📊 Registros Soportados
- **Corrientes trifásicas**: Fases A, B, C
- **Voltajes**: Línea-neutro y línea-línea
- **Potencias**: Activa, reactiva, aparente
- **Factor de potencia**: Por fase y total
- **Frecuencia**: Con variación realista
- **Energía**: Contadores acumulativos

## [1.0.0] - 2025-09-25

### 🎯 Versión Inicial
- **Simulador Modbus TCP**: Funcionalidad básica
- **Registros configurables**: Definición via código
- **Generación de valores**: Algoritmos básicos
- **CLI simple**: Configuración por línea de comandos

---

## 📋 Notas de Versiones

### Versión 5.0.0 - Interfaz Web
- **NUEVO**: Primera versión con interfaz web completa
- **NUEVO**: API REST para integración con otros sistemas
- **NUEVO**: WebSocket para datos en tiempo real
- **MEJORA**: Tema adaptivo con modo oscuro/claro
- **COMPATIBLE**: 100% compatible con CLI existente

### Versión 4.0.0 - Refactorización
- **REFACTOR**: Arquitectura completamente modular
- **NUEVO**: Suite de tests unitarios (16 tests)
- **NUEVO**: Generadores avanzados (sine, noise)
- **MEJORA**: Herramientas de desarrollo completas
- **COMPATIBLE**: Versión original preservada

### Versión 3.0.0 - Estabilización
- **MEJORA**: Compatibilidad Windows mejorada
- **NUEVO**: Sistema de configuración JSON
- **MEJORA**: Logging detallado y colorizado
- **CORRECCIÓN**: Manejo robusto de errores

### Versión 2.0.0 - Expansión
- **NUEVO**: Soporte para protocolo Modbus RTU
- **NUEVO**: Simulación de múltiples dispositivos
- **NUEVO**: Generadores de datos avanzados
- **MEJORA**: Configuración más flexible

### Versión 1.0.0 - Base
- **INICIAL**: Simulador Modbus TCP básico
- **INICIAL**: Registros de medidor de potencia
- **INICIAL**: CLI funcional

### 🎉 Refactorización Completa
- **Arquitectura modular**: Código organizado en módulos especializados (`src/`)
- **Estructura profesional**: Separación clara de responsabilidades
- **Documentación mejorada**: README completamente actualizado con ejemplos

### ✨ Nuevas Características
- **Generadores avanzados**: 6 tipos de generadores incluyendo ondas senoidales y ruido
- **Thread safety**: Generación segura de datos con locks
- **Logging mejorado**: Mensajes informativos con emojis y mejor formato
- **Configuración flexible**: Archivos JSON con validación y campos adicionales (unit, category)
- **Scripts de utilidad**: Demo, instalación y Makefile para desarrollo

### 🧪 Testing y Calidad
- **Tests unitarios completos**: Cobertura para generadores y funcionalidad core
- **Tests de integración**: Validación de carga de archivos y configuración
- **Herramientas de desarrollo**: Black, flake8, mypy, pytest
- **CI/CD ready**: pyproject.toml configurado para herramientas modernas

### 🛠️ Herramientas de Desarrollo
- **Makefile completo**: Comandos para desarrollo, testing y ejecución
- **Scripts de instalación**: Automatización de setup
- **Validación de configuración**: Verificación automática de archivos JSON
- **Formateo automático**: Estilo consistente con Black

### 🔧 Mejoras Técnicas
- **Manejo de errores mejorado**: Try-catch específicos y mensajes informativos
- **Configuración centralizada**: Settings consolidados en módulos dedicados
- **CLI parsing mejorado**: Validación de argumentos y mejor ayuda
- **Generación de estadísticas**: Métricas de rendimiento y estado

### 📊 Nuevos Generadores de Datos
| Generador | Descripción |
|-----------|-------------|
| `sine` | Ondas senoidales para simular valores periódicos |
| `noise` | Valores base con ruido añadido |
| Enhanced configs | Archivos JSON con metadatos adicionales |

### 🐛 Correcciones
- Validación de tipos de datos mejorada
- Manejo de archivos inexistentes
- Thread safety en actualización de registros
- Memory leaks en generación continua

## [3.0.0] - 2025-09-28

### Changed
-   Se refactorizó `MeterDataGenerator` para que sea completamente dirigido por datos, simplificando el código y mejorando la mantenibilidad.
-   Se migraron las definiciones de registros de un formato `.txt` personalizado a archivos `.json` (`register_table_PM21XX.json`, `register_table_generic.json`).
-   La lógica de generación de datos ahora se carga dinámicamente desde los archivos JSON, haciendo que el simulador sea altamente configurable.
-   Se mejoró el manejo de errores en la función `decode_register_value`.

### Removed
-   Se eliminaron los antiguos archivos de definición de registros en formato `.txt` (`register_table_PM21XX.txt`, `register_table_generic.txt`).

## [2.0.0] - 2025-09-28

### Added
-   Option to simulate a second device with a generic register map.
-   `--devices` command-line argument to specify the number of devices.
-   `parse_register_table` function to load register maps from files.
-   `README.md` file.
-   `requirements.txt` file.

### Changed
-   `MeterDataGenerator` now uses external files for register maps.
-   `run_modbus_server` now supports multiple devices.
-   Updated help message with the new `--devices` option.

### Fixed
-   Fixed a bug where `generate_registers` was defined in the wrong scope.

## [1.0.0] - 2025-09-28

### Added
-   Initial version of the virtual power meter.
-   Supports Modbus TCP and RTU.
-   Simulates a single device with a hardcoded register map.