"""
Generador de datos mejorado para medidores de potencia virtuales.
"""

import os
import time
import threading
from typing import Dict, List, Any
from datetime import datetime, timezone

from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.constants import Endian

from src.data_generation.register_loader import load_register_table
from src.data_generation.generators import get_generator


class MeterDataGenerator:
    """
    Generador de datos para un medidor específico con su propia configuración de registros.
    Versión mejorada con mejor manejo de errores y logging.
    """

    def __init__(self, device_id: int, register_file: str, update_interval: int = 60):
        """
        Inicializa el generador de datos del medidor.

        Args:
            device_id: ID del dispositivo
            register_file: Ruta al archivo de definiciones de registros
            update_interval: Intervalo de actualización en segundos
        """
        self.device_id = device_id
        self.update_interval = update_interval
        self._lock = threading.Lock()
        self._last_update = 0

        # Inicializar bloque de datos Modbus
        self.block = ModbusSequentialDataBlock(0x00, [0] * 5000)

        # Cargar definiciones de registros
        try:
            self.register_definitions = load_register_table(register_file)
            print(
                f"[Device {device_id}] ✅ Cargados {len(self.register_definitions)} registros desde {os.path.basename(register_file)}"
            )
        except FileNotFoundError:
            print(f"[Device {device_id}] ❌ Archivo no encontrado: {register_file}")
            self.register_definitions = []
        except Exception as e:
            print(f"[Device {device_id}] ❌ Error cargando registros: {e}")
            self.register_definitions = []

    def generate_registers(self) -> bool:
        """
        Genera los datos simulados para el medidor.

        Returns:
            True si la generación fue exitosa, False en caso contrario
        """
        with self._lock:
            try:
                current_time = time.time()

                # Para la primera ejecución o si no hay registros, generar inmediatamente
                if self._last_update == 0 or not self.register_definitions:
                    # Solo actualizar si hay definiciones de registros
                    if not self.register_definitions:
                        return False
                else:
                    # Verificar si necesita actualización
                    if current_time - self._last_update < self.update_interval:
                        return True

                builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)
                successful_updates = 0

                for reg_def in self.register_definitions:
                    try:
                        success = self._generate_single_register(reg_def, builder)
                        if success:
                            successful_updates += 1
                    except Exception as e:
                        print(
                            f"[Device {self.device_id}] ❌ Error generando registro {reg_def.get('address', 'unknown')}: {e}"
                        )
                        continue

                self._last_update = current_time

                if successful_updates > 0:
                    print(
                        f"[Device {self.device_id}] 🔄 Actualizados {successful_updates}/{len(self.register_definitions)} registros"
                    )

                return successful_updates > 0

            except Exception as e:
                print(f"[Device {self.device_id}] ❌ Error general en generación de registros: {e}")
                return False

    def _generate_single_register(
        self, reg_def: Dict[str, Any], builder: BinaryPayloadBuilder
    ) -> bool:
        """
        Genera un solo registro.

        Args:
            reg_def: Definición del registro
            builder: Builder para construir datos binarios

        Returns:
            True si la generación fue exitosa
        """
        try:
            address = reg_def["address"]
            gen_info = reg_def.get("generation")

            if not gen_info:
                return False

            # Obtener generador y parámetros
            gen_type = gen_info.get("type", "fixed")
            params = gen_info.get("params", [])

            # Generar valor
            generator = get_generator(gen_type)
            value = generator.generate(params)

            # Codificar según el tipo de datos
            data_type = reg_def["data_type"]
            builder.reset()

            if data_type in ["FLOAT32", "4Q_FP_PF"]:
                builder.add_32bit_float(float(value))
            elif data_type == "INT16":
                builder.add_16bit_int(int(value))
            elif data_type == "INT16U":
                builder.add_16bit_uint(int(value))
            elif data_type == "INT64":
                builder.add_64bit_int(int(value))
            elif data_type == "DATETIME":
                builder.add_64bit_uint(int(value))
            else:
                print(f"[Device {self.device_id}] Tipo de datos no soportado: {data_type}")
                return False

            # Escribir al bloque de datos
            built_regs = builder.to_registers()
            if built_regs:
                self.block.setValues(address, built_regs)
                return True

        except Exception as e:
            print(f"[Device {self.device_id}] Error en registro {address}: {e}")

        return False

    def get_register_value(self, address: int, data_type: str) -> Any:
        """
        Obtiene el valor actual de un registro específico.

        Args:
            address: Dirección del registro
            data_type: Tipo de datos del registro

        Returns:
            Valor decodificado del registro
        """
        with self._lock:
            try:
                return self._decode_register_value(address, data_type)
            except Exception as e:
                return f"Error: {e}"

    def _decode_register_value(self, address: int, data_type: str) -> Any:
        """
        Decodifica un valor de registro según su tipo de datos.

        Args:
            address: Dirección del registro
            data_type: Tipo de datos

        Returns:
            Valor decodificado
        """
        try:
            if data_type in ["FLOAT32", "4Q_FP_PF"]:
                regs = self.block.getValues(address, 2)
                decoder = BinaryPayloadDecoder.fromRegisters(
                    regs, byteorder=Endian.BIG, wordorder=Endian.LITTLE
                )
                return decoder.decode_32bit_float()
            elif data_type == "INT16":
                regs = self.block.getValues(address, 1)
                decoder = BinaryPayloadDecoder.fromRegisters(
                    regs, byteorder=Endian.BIG, wordorder=Endian.LITTLE
                )
                return decoder.decode_16bit_int()
            elif data_type == "INT16U":
                regs = self.block.getValues(address, 1)
                decoder = BinaryPayloadDecoder.fromRegisters(
                    regs, byteorder=Endian.BIG, wordorder=Endian.LITTLE
                )
                return decoder.decode_16bit_uint()
            elif data_type == "INT64":
                regs = self.block.getValues(address, 4)
                decoder = BinaryPayloadDecoder.fromRegisters(
                    regs, byteorder=Endian.BIG, wordorder=Endian.LITTLE
                )
                return decoder.decode_64bit_int()
            elif data_type == "DATETIME":
                regs = self.block.getValues(address, 4)
                decoder = BinaryPayloadDecoder.fromRegisters(
                    regs, byteorder=Endian.BIG, wordorder=Endian.LITTLE
                )
                timestamp = decoder.decode_64bit_uint()
                return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            else:
                return "Tipo desconocido"
        except (ValueError, IndexError) as e:
            raise ValueError(f"Error decodificando {data_type} en dirección {address}: {e}")
        except Exception as e:
            raise Exception(f"Error inesperado: {e}")

    def print_all_registers(self) -> None:
        """Imprime los valores de todos los registros en formato legible."""
        print(
            f"[Device ID {self.device_id} - {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}] Valores de registros:"
        )
        print("=" * 80)

        for reg_info in self.register_definitions:
            address = reg_info["address"]
            data_type = reg_info["data_type"]
            description = reg_info["description"]

            try:
                value = self._decode_register_value(address, data_type)
                print(f"Registro {address:4d} ({data_type:8s}): {value} ({description})")
            except Exception as e:
                print(f"Registro {address:4d} ({data_type:8s}): Error leyendo registro - {e}")

        print("=" * 80)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del generador.

        Returns:
            Diccionario con estadísticas
        """
        return {
            "device_id": self.device_id,
            "total_registers": len(self.register_definitions),
            "last_update": self._last_update,
            "update_interval": self.update_interval,
        }
