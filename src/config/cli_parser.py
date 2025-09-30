"""
Validación y parsing de argumentos de línea de comandos.
"""

import argparse
from src.config.settings import DEFAULT_CONFIG, DEFAULT_MODBUS_CONFIG


def create_argument_parser():
    """Crea el parser de argumentos de línea de comandos."""
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
  -t, --update-interval         Intervalo de actualización en segundos (por defecto: 60)
  -d, --devices {1,2}           Number of devices to simulate (1 or 2)

Opciones TCP:
  -H, --host                    Dirección IP del servidor Modbus TCP (por defecto: 0.0.0.0)
  -p, --port                    Puerto del servidor Modbus TCP (por defecto: 502)
  -u, --unit-id                 ID del dispositivo Modbus TCP (por defecto: 1)

Opciones RTU:
  -s, --port-serial             Puerto serial para Modbus RTU (ej: COM5, /dev/ttyUSB0)
  -b, --baudrate                Velocidad de baudios para Modbus RTU (por defecto: 9600)
  -i, --slave-id                ID del dispositivo esclavo Modbus (por defecto: 1)

        """,
        add_help=False,
    )

    # Argumentos generales
    parser.add_argument("-v", "--verbose", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument(
        "-P",
        "--protocol",
        choices=["tcp", "rtu"],
        default=DEFAULT_MODBUS_CONFIG.protocol,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-t",
        "--update-interval",
        type=int,
        default=DEFAULT_CONFIG.update_interval,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-d",
        "--devices",
        type=int,
        choices=[1, 2],
        default=DEFAULT_CONFIG.devices,
        help="Number of devices to simulate (1 or 2)",
    )
    parser.add_argument("-h", "--help", action="help", help=argparse.SUPPRESS)

    # Argumentos TCP
    parser.add_argument(
        "-H", "--host", type=str, default=DEFAULT_MODBUS_CONFIG.host, help=argparse.SUPPRESS
    )
    parser.add_argument(
        "-p", "--port", type=int, default=DEFAULT_MODBUS_CONFIG.port, help=argparse.SUPPRESS
    )
    parser.add_argument(
        "-u", "--unit-id", type=int, default=DEFAULT_MODBUS_CONFIG.unit_id, help=argparse.SUPPRESS
    )

    # Argumentos RTU
    parser.add_argument("-s", "--port-serial", type=str, help=argparse.SUPPRESS)
    parser.add_argument(
        "-b", "--baudrate", type=int, default=DEFAULT_MODBUS_CONFIG.baudrate, help=argparse.SUPPRESS
    )
    parser.add_argument(
        "-i", "--slave-id", type=int, default=DEFAULT_MODBUS_CONFIG.slave_id, help=argparse.SUPPRESS
    )

    return parser


def validate_arguments(args):
    """Valida los argumentos parseados."""
    if args.protocol == "rtu" and not args.port_serial:
        raise ValueError("Para Modbus RTU se requiere especificar --port-serial")

    return args


def parse_arguments():
    """Parsea y valida los argumentos de línea de comandos."""
    parser = create_argument_parser()
    args = parser.parse_args()
    return validate_arguments(args)
