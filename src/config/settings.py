"""
Configuración general del simulador de medidores virtuales.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class ModbusConfig:
    """Configuración para el servidor Modbus."""

    protocol: str = "tcp"
    host: str = "0.0.0.0"
    port: int = 502
    port_serial: Optional[str] = None
    baudrate: int = 9600
    unit_id: int = 1
    slave_id: int = 1


@dataclass
class SimulatorConfig:
    """Configuración general del simulador."""

    devices: int = 1
    update_interval: int = 60
    verbose: bool = False
    register_tables_dir: str = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "config")
    )


# Configuración por defecto
DEFAULT_CONFIG = SimulatorConfig()
DEFAULT_MODBUS_CONFIG = ModbusConfig()

# Rutas de archivos de registros
REGISTER_FILES = {1: "register_table_PM21XX.json", 2: "register_table_generic.json"}
