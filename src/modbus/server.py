"""
Servidor Modbus mejorado con mejor manejo de errores y logging.
"""

import os
import time
import threading
from typing import List, Dict, Any
from datetime import datetime

from pymodbus.server import StartTcpServer, StartSerialServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

from src.data_generation.meter_generator import MeterDataGenerator
from src.config.settings import REGISTER_FILES


class ModbusServerManager:
    """
    Manager para el servidor Modbus con soporte para múltiples dispositivos.
    """

    def __init__(self, args):
        """
        Inicializa el manager del servidor Modbus.

        Args:
            args: Argumentos parseados de línea de comandos
        """
        self.args = args
        self.generators: List[MeterDataGenerator] = []
        self._update_thread = None
        self._running = False

    def initialize_generators(self) -> None:
        """Inicializa los generadores de datos para los dispositivos."""
        if self.args.protocol == "tcp":
            base_device_id = self.args.unit_id
        else:
            base_device_id = self.args.slave_id

        from src.config.settings import DEFAULT_CONFIG

        config_dir = DEFAULT_CONFIG.register_tables_dir

        # Crear generador para el primer dispositivo
        try:
            register_filename = REGISTER_FILES.get(1, "register_table_PM21XX.json")
            register_file = os.path.join(config_dir, register_filename)
            generator1 = MeterDataGenerator(
                device_id=base_device_id,
                register_file=register_file,
                update_interval=self.args.update_interval,
            )
            self.generators.append(generator1)
            print(f"✓ Dispositivo {base_device_id} inicializado con {register_filename}")
        except Exception as e:
            print(f"✗ Error inicializando dispositivo {base_device_id}: {e}")

        # Crear generador para el segundo dispositivo si se solicita
        if self.args.devices == 2:
            try:
                register_filename = REGISTER_FILES.get(2, "register_table_generic.json")
                register_file = os.path.join(config_dir, register_filename)
                generator2 = MeterDataGenerator(
                    device_id=base_device_id + 1,
                    register_file=register_file,
                    update_interval=self.args.update_interval,
                )
                self.generators.append(generator2)
                print(f"✓ Dispositivo {base_device_id + 1} inicializado con {register_filename}")
            except Exception as e:
                print(f"✗ Error inicializando dispositivo {base_device_id + 1}: {e}")

    def _update_registers_thread(self) -> None:
        """Función que se ejecuta en un thread separado para actualizar los registros."""
        print(f"[INFO] Thread de actualización iniciado (intervalo: {self.args.update_interval}s)")

        while self._running:
            try:
                start_time = time.time()

                for generator in self.generators:
                    success = generator.generate_registers()

                    if self.args.verbose and success:
                        generator.print_all_registers()
                        print()  # Línea en blanco para separar dispositivos

                # Calcular tiempo de procesamiento
                processing_time = time.time() - start_time
                remaining_time = max(0, self.args.update_interval - processing_time)

                if remaining_time > 0:
                    time.sleep(remaining_time)
                else:
                    print(
                        f"[WARNING] Actualización tardó {processing_time:.2f}s (más que el intervalo de {self.args.update_interval}s)"
                    )

            except Exception as e:
                print(f"[ERROR] Error en thread de actualización: {e}")
                if self._running:  # Solo dormir si seguimos ejecutando
                    time.sleep(self.args.update_interval)

    def create_modbus_context(self) -> ModbusServerContext:
        """
        Crea el contexto del servidor Modbus.

        Returns:
            Contexto configurado del servidor Modbus
        """
        slaves = {}

        for generator in self.generators:
            slaves[generator.device_id] = ModbusSlaveContext(
                di=generator.block,  # Discrete Inputs
                co=generator.block,  # Coils
                hr=generator.block,  # Holding Registers
                ir=generator.block,  # Input Registers
            )

        context = ModbusServerContext(slaves=slaves, single=False)
        print(f"[INFO] Contexto Modbus creado con {len(slaves)} dispositivos")
        return context

    def print_startup_message(self) -> None:
        """Imprime el mensaje de inicio del servidor."""
        print("=" * 60)
        print("🔌 Virtual Power Meter - Servidor Modbus")
        print("=" * 60)
        print(f"📊 Número de dispositivos: {self.args.devices}")

        if self.args.protocol == "tcp":
            print(f"🌐 Host: {self.args.host}")
            print(f"🔌 Puerto: {self.args.port}")
            print(f"🏷️  Unit ID base: {self.args.unit_id}")
        else:
            print(f"📡 Puerto serial: {self.args.port_serial}")
            print(f"⚡ Baudrate: {self.args.baudrate}")
            print(f"🏷️  Slave ID base: {self.args.slave_id}")

        print(f"⏱️  Intervalo de actualización: {self.args.update_interval} segundos")

        if self.args.verbose:
            print("📢 Modo: Verbose (mostrando valores de registros)")
        else:
            print("🔇 Modo: Silencioso (sin salida de registros)")

        print("=" * 60)
        print(f"🕐 Servidor iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

    def start_server(self) -> None:
        """Inicia el servidor Modbus."""
        try:
            # Inicializar generadores
            self.initialize_generators()

            if not self.generators:
                print("❌ No se pudieron inicializar generadores de dispositivos")
                print(
                    "💡 Verificar que existen los archivos de configuración en el directorio 'config/'"
                )
                return

            # Verificar que al menos un generador tiene registros
            valid_generators = [g for g in self.generators if g.register_definitions]
            if not valid_generators:
                print("❌ Ningún generador tiene definiciones de registros válidas")
                print("💡 Verificar el contenido de los archivos JSON de configuración")
                return

            # Mostrar mensaje de inicio
            self.print_startup_message()

            # Iniciar thread de actualización
            self._running = True
            self._update_thread = threading.Thread(
                target=self._update_registers_thread, daemon=True
            )
            self._update_thread.start()

            # Crear contexto del servidor
            context = self.create_modbus_context()

            # Iniciar servidor según protocolo
            if self.args.protocol == "tcp":
                print(f"🚀 Iniciando servidor Modbus TCP en {self.args.host}:{self.args.port}")
                StartTcpServer(context=context, address=(self.args.host, self.args.port))
            else:
                if not self.args.port_serial:
                    raise ValueError("Para Modbus RTU se requiere especificar --port-serial")

                print(f"🚀 Iniciando servidor Modbus RTU en {self.args.port_serial}")
                StartSerialServer(
                    context=context,
                    port=self.args.port_serial,
                    baudrate=self.args.baudrate,
                    parity="N",
                    stopbits=1,
                    bytesize=8,
                    timeout=1,
                )

        except KeyboardInterrupt:
            print("\n🛑 Deteniendo servidor...")
            self.stop_server()
        except Exception as e:
            print(f"❌ Error iniciando servidor: {e}")
            raise

    def stop_server(self) -> None:
        """Detiene el servidor Modbus."""
        self._running = False
        if self._update_thread and self._update_thread.is_alive():
            self._update_thread.join(timeout=5)
        print("✅ Servidor detenido correctamente")

    def get_server_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del servidor.

        Returns:
            Diccionario con estadísticas del servidor
        """
        stats = {
            "protocol": self.args.protocol,
            "devices": self.args.devices,
            "update_interval": self.args.update_interval,
            "verbose": self.args.verbose,
            "generators": [],
        }

        for generator in self.generators:
            stats["generators"].append(generator.get_statistics())

        return stats
