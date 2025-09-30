"""
Tests unitarios para los generadores de datos.
"""

import unittest
import time
from src.data_generation.generators import (
    UniformGenerator,
    RandintGenerator,
    TimestampGenerator,
    FixedGenerator,
    SineWaveGenerator,
    NoiseGenerator,
    get_generator,
)


class TestDataGenerators(unittest.TestCase):
    """Test cases para los generadores de datos."""

    def test_uniform_generator(self):
        """Test para el generador uniforme."""
        generator = UniformGenerator()

        # Test básico
        value = generator.generate([10.0, 20.0])
        self.assertGreaterEqual(value, 10.0)
        self.assertLessEqual(value, 20.0)

        # Test con parámetros insuficientes
        with self.assertRaises(ValueError):
            generator.generate([10.0])

    def test_randint_generator(self):
        """Test para el generador de enteros aleatorios."""
        generator = RandintGenerator()

        # Test básico
        value = generator.generate([1, 10])
        self.assertGreaterEqual(value, 1)
        self.assertLessEqual(value, 10)
        self.assertIsInstance(value, int)

        # Test con parámetros insuficientes
        with self.assertRaises(ValueError):
            generator.generate([5])

    def test_timestamp_generator(self):
        """Test para el generador de timestamps."""
        generator = TimestampGenerator()

        current_time = int(time.time())
        value = generator.generate([])

        # Verificar que el timestamp está cerca del tiempo actual
        self.assertAlmostEqual(value, current_time, delta=2)
        self.assertIsInstance(value, int)

    def test_fixed_generator(self):
        """Test para el generador de valores fijos."""
        generator = FixedGenerator()

        # Test con diferentes tipos de valores
        self.assertEqual(generator.generate([42]), 42)
        self.assertEqual(generator.generate([3.14]), 3.14)
        self.assertEqual(generator.generate(["test"]), "test")

        # Test sin parámetros
        with self.assertRaises(ValueError):
            generator.generate([])

    def test_sine_wave_generator(self):
        """Test para el generador de ondas senoidales."""
        generator = SineWaveGenerator()

        # Test básico
        value = generator.generate([10.0, 1.0, 0.0, 50.0])
        self.assertIsInstance(value, float)

        # Test con parámetros insuficientes
        with self.assertRaises(ValueError):
            generator.generate([10.0, 1.0])

        # Test funcionalidad senoidal
        # Con frecuencia 0, debería dar el valor DC offset (sin amplitude porque sin(0) = 0)
        value = generator.generate([10.0, 0.0, 0.0, 50.0])
        self.assertAlmostEqual(value, 50.0, delta=0.1)

    def test_noise_generator(self):
        """Test para el generador con ruido."""
        generator = NoiseGenerator()

        # Test básico
        base_value = 100.0
        noise_amplitude = 5.0
        value = generator.generate([base_value, noise_amplitude])

        self.assertGreaterEqual(value, base_value - noise_amplitude)
        self.assertLessEqual(value, base_value + noise_amplitude)

        # Test con parámetros insuficientes
        with self.assertRaises(ValueError):
            generator.generate([100.0])

    def test_get_generator(self):
        """Test para la función get_generator."""
        # Test generadores válidos
        self.assertIsInstance(get_generator("uniform"), UniformGenerator)
        self.assertIsInstance(get_generator("randint"), RandintGenerator)
        self.assertIsInstance(get_generator("timestamp"), TimestampGenerator)
        self.assertIsInstance(get_generator("fixed"), FixedGenerator)
        self.assertIsInstance(get_generator("sine"), SineWaveGenerator)
        self.assertIsInstance(get_generator("noise"), NoiseGenerator)

        # Test generador inválido
        with self.assertRaises(ValueError):
            get_generator("invalid_generator")


if __name__ == "__main__":
    unittest.main()
