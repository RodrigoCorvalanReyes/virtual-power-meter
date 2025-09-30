"""
Generadores de datos para valores de registros simulados.
"""

import random
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class DataGenerator(ABC):
    """Clase base abstracta para generadores de datos."""

    @abstractmethod
    def generate(self, params: List[Any]) -> Any:
        """Genera un valor basado en parámetros."""
        pass


class UniformGenerator(DataGenerator):
    """Generador de números aleatorios con distribución uniforme."""

    def generate(self, params: List[Any]) -> float:
        if len(params) < 2:
            raise ValueError("UniformGenerator requiere al menos 2 parámetros [min, max]")
        return random.uniform(params[0], params[1])


class RandintGenerator(DataGenerator):
    """Generador de números enteros aleatorios."""

    def generate(self, params: List[Any]) -> int:
        if len(params) < 2:
            raise ValueError("RandintGenerator requiere al menos 2 parámetros [min, max]")
        return random.randint(params[0], params[1])


class TimestampGenerator(DataGenerator):
    """Generador de timestamps."""

    def generate(self, params: List[Any]) -> int:
        return int(time.time())


class FixedGenerator(DataGenerator):
    """Generador de valores fijos."""

    def generate(self, params: List[Any]) -> Any:
        if not params:
            raise ValueError("FixedGenerator requiere al menos 1 parámetro")
        return params[0]


class SineWaveGenerator(DataGenerator):
    """Generador de ondas senoidales para simular valores más realistas."""

    def __init__(self):
        self._time_offset = time.time()

    def generate(self, params: List[Any]) -> float:
        """
        Genera valor senoidal: amplitude * sin(2π * frequency * time + phase) + offset
        params: [amplitude, frequency, phase_offset, dc_offset]
        """
        if len(params) < 4:
            raise ValueError(
                "SineWaveGenerator requiere 4 parámetros [amplitude, frequency, phase, dc_offset]"
            )

        amplitude, frequency, phase, dc_offset = params
        current_time = time.time() - self._time_offset

        import math

        value = amplitude * math.sin(2 * math.pi * frequency * current_time + phase) + dc_offset
        return value


class NoiseGenerator(DataGenerator):
    """Generador que añade ruido a un valor base."""

    def generate(self, params: List[Any]) -> float:
        """
        params: [base_value, noise_amplitude]
        """
        if len(params) < 2:
            raise ValueError("NoiseGenerator requiere 2 parámetros [base_value, noise_amplitude]")

        base_value, noise_amplitude = params
        noise = random.uniform(-noise_amplitude, noise_amplitude)
        return base_value + noise


# Registry de generadores disponibles
GENERATOR_REGISTRY = {
    "uniform": UniformGenerator(),
    "randint": RandintGenerator(),
    "timestamp": TimestampGenerator(),
    "fixed": FixedGenerator(),
    "sine": SineWaveGenerator(),
    "noise": NoiseGenerator(),
}


def get_generator(generator_type: str) -> DataGenerator:
    """
    Obtiene un generador por su tipo.

    Args:
        generator_type: Tipo de generador

    Returns:
        Instancia del generador

    Raises:
        ValueError: Si el tipo de generador no existe
    """
    if generator_type not in GENERATOR_REGISTRY:
        available = ", ".join(GENERATOR_REGISTRY.keys())
        raise ValueError(f"Generador '{generator_type}' no disponible. Disponibles: {available}")

    return GENERATOR_REGISTRY[generator_type]
