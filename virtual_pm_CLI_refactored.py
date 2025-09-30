#!/usr/bin/env python3
"""
Virtual Power Meter - Versión Refactorizada y Mejorada
======================================================

Simulador de medidores de potencia virtuales que expone registros via Modbus TCP/RTU.
Esta versión incluye mejoras en:
- Estructura modular del código
- Mejor manejo de errores
- Logging mejorado
- Nuevos generadores de datos
- Validación de configuración
- Soporte para testing

Autor: Refactorizado desde versión original
Fecha: 2025-09-28
"""

import sys
import os

# Añadir el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config.cli_parser import parse_arguments
from src.modbus.server import ModbusServerManager


def main():
    """Función principal del programa."""
    try:
        # Parsear argumentos de línea de comandos
        args = parse_arguments()

        # Crear y iniciar el servidor
        server_manager = ModbusServerManager(args)
        server_manager.start_server()

    except KeyboardInterrupt:
        print("\n🛑 Programa interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
