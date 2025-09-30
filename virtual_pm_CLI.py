import time
import random
import argparse
from pymodbus.server import StartTcpServer, StartSerialServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.constants import Endian
from datetime import datetime, timezone
import threading


def parse_arguments():
    """
    Parsea los argumentos de línea de comandos.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Virtual Power Meter - Modbus TCP/RTU Server Simulator\n"
            "Este programa simula un medidor de energía y expone sus registros vía Modbus TCP o RTU."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Opciones generales:
  -v, --verbose                 Muestra información detallada de los registros en la terminal
  -P, --protocol {tcp,rtu}      Protocolo Modbus
  -h, --help                    Muestra este mensaje de ayuda y termina
  -t, --update-interval {UPDATE_INTERVAL}
                                Intervalo de actualización en segundos (por defecto: 60)
  -d, --devices {1,2}           Number of devices to simulate (1 or 2)

Opciones TCP:
  -H, --host {HOST}             Dirección IP del servidor Modbus TCP (por defecto: 0.0.0.0)
  -p, --port {PORT}             Puerto del servidor Modbus TCP (por defecto: 502)
  -u, --unit-id {UNIT_ID}       ID del dispositivo Modbus TCP (por defecto: 1)

Opciones RTU:
  -s, --port-serial {PORT_SERIAL}
                                Puerto serial para Modbus RTU (ej: COM5, /dev/ttyUSB0)
  -b, --baudrate {BAUDRATE}     Velocidad de baudios para Modbus RTU (por defecto: 9600)
  -i, --slave-id {SLAVE_ID}     ID del dispositivo esclavo Modbus (por defecto: 1)

        """,
        add_help=False,
    )

    parser.add_argument("-v", "--verbose", action="store_true", help=argparse.SUPPRESS)

    parser.add_argument(
        "-P", "--protocol", choices=["tcp", "rtu"], default="tcp", help=argparse.SUPPRESS
    )

    parser.add_argument("-H", "--host", type=str, default="0.0.0.0", help=argparse.SUPPRESS)

    parser.add_argument("-p", "--port", type=int, default=502, help=argparse.SUPPRESS)

    parser.add_argument("-s", "--port-serial", type=str, help=argparse.SUPPRESS)

    parser.add_argument("-b", "--baudrate", type=int, default=9600, help=argparse.SUPPRESS)

    parser.add_argument("-u", "--unit-id", type=int, default=1, help=argparse.SUPPRESS)

    parser.add_argument("-i", "--slave-id", type=int, default=1, help=argparse.SUPPRESS)

    parser.add_argument("-t", "--update-interval", type=int, default=60, help=argparse.SUPPRESS)

    parser.add_argument("-h", "--help", action="help", help=argparse.SUPPRESS)

    parser.add_argument(
        "-d",
        "--devices",
        type=int,
        choices=[1, 2],
        default=1,
        help="Number of devices to simulate (1 or 2)",
    )

    # Parseamos los argumentos primero
    args = parser.parse_args()

    # Validamos que se especifique el ID correcto según el protocolo
    if args.protocol == "tcp" and args.unit_id is None:
        parser.error("TCP protocol requires --unit-id")
    elif args.protocol == "rtu" and args.slave_id is None:
        parser.error("RTU protocol requires --slave-id")

    return args


import json


def parse_json_register_table(file_path):
    """
    Parsea un archivo de tabla de registros en formato JSON.
    """
    with open(file_path, "r") as f:
        return json.load(f)


def decode_register_value(block, address, data_type):
    """
    Decodifica un valor de registro según su tipo de datos.
    """
    try:
        if data_type in ["FLOAT32", "4Q_FP_PF"]:
            regs = block.getValues(address, 2)
            decoder = BinaryPayloadDecoder.fromRegisters(
                regs, byteorder=Endian.BIG, wordorder=Endian.LITTLE
            )
            return decoder.decode_32bit_float()
        elif data_type == "INT16":
            regs = block.getValues(address, 1)
            decoder = BinaryPayloadDecoder.fromRegisters(
                regs, byteorder=Endian.BIG, wordorder=Endian.LITTLE
            )
            return decoder.decode_16bit_int()
        elif data_type == "INT16U":
            regs = block.getValues(address, 1)
            decoder = BinaryPayloadDecoder.fromRegisters(
                regs, byteorder=Endian.BIG, wordorder=Endian.LITTLE
            )
            return decoder.decode_16bit_uint()
        elif data_type == "INT64":
            regs = block.getValues(address, 4)
            decoder = BinaryPayloadDecoder.fromRegisters(
                regs, byteorder=Endian.BIG, wordorder=Endian.LITTLE
            )
            return decoder.decode_64bit_int()
        elif data_type == "DATETIME":
            regs = block.getValues(address, 4)
            decoder = BinaryPayloadDecoder.fromRegisters(
                regs, byteorder=Endian.BIG, wordorder=Endian.LITTLE
            )
            timestamp = decoder.decode_64bit_uint()
            return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        else:
            return "Unknown type"
    except (ValueError, IndexError) as e:
        return f"Decoding Error for type {data_type} at address {address}: {e}"
    except Exception as e:
        return f"Unexpected Error: {e}"


def print_all_registers(block, device_id, registers_info):
    """
    Imprime los valores de los registros especificados en formato legible.
    """
    print(
        f"[Device ID {device_id} - {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}] Register values:"
    )
    print("=" * 80)
    for reg_info in registers_info:
        address = reg_info["address"]
        data_type = reg_info["data_type"]
        description = reg_info["description"]
        try:
            value = decode_register_value(block, address, data_type)
            print(f"Register {address:4d} ({data_type:8s}): {value} ({description})")
        except Exception as e:
            print(f"Register {address:4d} ({data_type:8s}): Error reading register - {e}")
    print("=" * 80)


class MeterDataGenerator:
    """Generador de datos para un medidor específico con su propia configuración de registros"""

    def __init__(self, device_id, register_file, args):
        self.device_id = device_id
        self.args = args
        self.block = ModbusSequentialDataBlock(0x00, [0] * 5000)
        self.register_definitions = parse_json_register_table(register_file)

    def generate_registers(self):
        """Genera los datos simulados para el medidor de forma data-driven desde el JSON."""
        builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)

        for reg_def in self.register_definitions:
            address = reg_def["address"]

            gen_info = reg_def.get("generation")
            if not gen_info:
                continue

            value = 0
            gen_type = gen_info.get("type", "fixed")
            params = gen_info.get("params", [])

            if gen_type == "uniform":
                value = random.uniform(*params)
            elif gen_type == "randint":
                value = random.randint(*params)
            elif gen_type == "timestamp":
                value = int(time.time())
            elif gen_type == "fixed" and params:
                value = params[0]

            data_type = reg_def["data_type"]

            builder.reset()
            if data_type == "FLOAT32" or data_type == "4Q_FP_PF":
                builder.add_32bit_float(value)
            elif data_type == "INT16":
                builder.add_16bit_int(value)
            elif data_type == "INT16U":
                builder.add_16bit_uint(value)
            elif data_type == "INT64":
                builder.add_64bit_int(value)
            elif data_type == "DATETIME":
                builder.add_64bit_uint(int(value))

            built_regs = builder.to_registers()
            if built_regs:
                self.block.setValues(address, built_regs)


def print_startup_message(args):
    """Imprime el mensaje de inicio del servidor."""
    print("Starting Virtual Power Meter - Modbus Server")
    print(f"Number of devices: {args.devices}")
    if args.protocol == "tcp":
        print(f"Host: {args.host}")
        print(f"Port: {args.port}")
        print(f"Unit ID: {args.unit_id}")
    else:
        print(f"Serial Port: {args.port_serial}")
        print(f"Baudrate: {args.baudrate}")
        print(f"Slave ID: {args.slave_id}")

    print(f"Update interval: {args.update_interval} seconds")

    if args.verbose:
        print("Mode: Verbose (showing register values)")
    else:
        print("Mode: Silent (no register output)")
    print("-" * 60)


def run_modbus_server(args):
    """Ejecuta el servidor Modbus TCP o RTU que ofrece registros simulados de un medidor."""

    generators = []
    if args.protocol == "tcp":
        base_device_id = args.unit_id
    else:
        base_device_id = args.slave_id

    # Create generator for the first device
    generator1 = MeterDataGenerator(base_device_id, "register_table_PM21XX.json", args)
    generators.append(generator1)

    # Create generator for the second device if requested
    if args.devices == 2:
        generator2 = MeterDataGenerator(base_device_id + 1, "register_table_generic.json", args)
        generators.append(generator2)

    def update_registers():
        """Función que se ejecuta en un thread separado para actualizar los registros."""
        while True:
            try:
                for generator in generators:
                    # Actualiza los registros del medidor
                    generator.generate_registers()
                    if args.verbose:
                        print_all_registers(
                            generator.block, generator.device_id, generator.register_definitions
                        )

                time.sleep(args.update_interval)
            except Exception as e:
                if args.verbose:
                    print(f"Error in update thread: {e}")
                time.sleep(args.update_interval)

    # Imprime mensaje de inicio
    print_startup_message(args)

    # Lanza el thread que actualiza los datos
    update_thread = threading.Thread(target=update_registers, daemon=True)
    update_thread.start()

    # Crea el contexto para los dispositivos
    slaves = {
        g.device_id: ModbusSlaveContext(di=g.block, co=g.block, hr=g.block, ir=g.block)
        for g in generators
    }

    context = ModbusServerContext(slaves=slaves, single=False)

    # Ejecuta el servidor Modbus según el protocolo seleccionado
    if args.protocol == "tcp":
        StartTcpServer(context=context, address=(args.host, args.port))
    else:
        if not args.port_serial:
            raise ValueError("Para Modbus RTU se requiere especificar --port-serial")

        StartSerialServer(
            context=context,
            port=args.port_serial,
            baudrate=args.baudrate,
            parity="N",
            stopbits=1,
            bytesize=8,
            timeout=1,
        )


if __name__ == "__main__":
    # Parsea argumentos de línea de comandos
    args = parse_arguments()

    # Ejecuta el servidor Modbus
    run_modbus_server(args)
