"""
Tests de integración para el simulador completo.
"""

import unittest
import tempfile
import json
import os
from unittest.mock import patch, MagicMock

from src.data_generation.meter_generator import MeterDataGenerator
from src.data_generation.register_loader import load_register_table, validate_register_definition
from src.config.cli_parser import parse_arguments


class TestRegisterLoader(unittest.TestCase):
    """Test cases para el cargador de registros."""

    def test_load_valid_register_table(self):
        """Test carga de tabla de registros válida."""
        test_data = [
            {
                "address": 1000,
                "data_type": "FLOAT32",
                "description": "Test Register",
                "generation": {"type": "fixed", "params": [42.0]},
            }
        ]

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            json.dump(test_data, f)
            temp_file = f.name

        try:
            registers = load_register_table(temp_file)
            self.assertEqual(len(registers), 1)
            self.assertEqual(registers[0]["address"], 1000)
            self.assertEqual(registers[0]["data_type"], "FLOAT32")
        finally:
            os.unlink(temp_file)

    def test_load_nonexistent_file(self):
        """Test carga de archivo inexistente."""
        with self.assertRaises(FileNotFoundError):
            load_register_table("nonexistent_file.json")

    def test_validate_register_definition(self):
        """Test validación de definiciones de registros."""
        # Registro válido
        valid_register = {"address": 1000, "data_type": "FLOAT32", "description": "Test Register"}
        self.assertTrue(validate_register_definition(valid_register))

        # Registro inválido - falta campo requerido
        invalid_register = {
            "address": 1000,
            "data_type": "FLOAT32",
            # Falta 'description'
        }
        self.assertFalse(validate_register_definition(invalid_register))

        # Registro inválido - tipo de dato no soportado
        invalid_type_register = {
            "address": 1000,
            "data_type": "INVALID_TYPE",
            "description": "Test Register",
        }
        self.assertFalse(validate_register_definition(invalid_type_register))


class TestMeterDataGenerator(unittest.TestCase):
    """Test cases para el generador de datos del medidor."""

    def setUp(self):
        """Configuración para los tests."""
        self.test_registers = [
            {
                "address": 1000,
                "data_type": "FLOAT32",
                "description": "Test Float",
                "generation": {"type": "fixed", "params": [42.0]},
            },
            {
                "address": 1002,
                "data_type": "INT16",
                "description": "Test Int",
                "generation": {"type": "fixed", "params": [100]},
            },
        ]

        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            json.dump(self.test_registers, f)
            self.temp_file = f.name

    def tearDown(self):
        """Limpieza después de los tests."""
        if os.path.exists(self.temp_file):
            os.unlink(self.temp_file)

    def test_generator_initialization(self):
        """Test inicialización del generador."""
        generator = MeterDataGenerator(
            device_id=1, register_file=self.temp_file, update_interval=60
        )

        self.assertEqual(generator.device_id, 1)
        self.assertEqual(generator.update_interval, 60)
        self.assertEqual(len(generator.register_definitions), 2)

    def test_generate_registers(self):
        """Test generación de registros."""
        generator = MeterDataGenerator(
            device_id=1, register_file=self.temp_file, update_interval=0  # Sin delay para testing
        )

        result = generator.generate_registers()
        self.assertTrue(result)

    def test_get_register_value(self):
        """Test obtención de valores de registros."""
        generator = MeterDataGenerator(device_id=1, register_file=self.temp_file, update_interval=0)

        generator.generate_registers()

        # Test float value
        value = generator.get_register_value(1000, "FLOAT32")
        self.assertAlmostEqual(value, 42.0, delta=0.01)

        # Test int value
        value = generator.get_register_value(1002, "INT16")
        self.assertEqual(value, 100)


class TestCLIParser(unittest.TestCase):
    """Test cases para el parser de argumentos CLI."""

    @patch("sys.argv", ["virtual_pm_CLI.py"])
    def test_default_arguments(self):
        """Test argumentos por defecto."""
        args = parse_arguments()
        self.assertEqual(args.devices, 1)
        self.assertEqual(args.protocol, "tcp")
        self.assertEqual(args.host, "0.0.0.0")
        self.assertEqual(args.port, 502)
        self.assertFalse(args.verbose)

    @patch("sys.argv", ["virtual_pm_CLI.py", "--devices", "2", "--verbose"])
    def test_custom_arguments(self):
        """Test argumentos personalizados."""
        args = parse_arguments()
        self.assertEqual(args.devices, 2)
        self.assertTrue(args.verbose)

    @patch("sys.argv", ["virtual_pm_CLI.py", "--protocol", "rtu"])
    def test_rtu_without_serial_port(self):
        """Test protocolo RTU sin puerto serial."""
        with self.assertRaises(ValueError):
            parse_arguments()


if __name__ == "__main__":
    unittest.main()
