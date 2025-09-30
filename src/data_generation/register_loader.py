"""
Módulo para la carga y parsing de tablas de registros en formato JSON.
"""

import json
import os
from typing import List, Dict, Any


def load_register_table(file_path: str) -> List[Dict[str, Any]]:
    """
    Carga una tabla de registros desde un archivo JSON.

    Args:
        file_path: Ruta al archivo JSON de registros

    Returns:
        Lista de definiciones de registros

    Raises:
        FileNotFoundError: Si el archivo no existe
        json.JSONDecodeError: Si el archivo JSON es inválido
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Archivo de registros no encontrado: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            registers = json.load(f)

        # Validación básica de la estructura
        if not isinstance(registers, list):
            raise ValueError("El archivo de registros debe contener una lista")

        for register in registers:
            required_fields = ["address", "data_type", "description"]
            for field in required_fields:
                if field not in register:
                    raise ValueError(f"Campo requerido '{field}' faltante en registro")

        return registers

    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error parsing JSON en {file_path}: {e}")


def validate_register_definition(register: Dict[str, Any]) -> bool:
    """
    Valida si una definición de registro tiene la estructura correcta.

    Args:
        register: Diccionario con la definición del registro

    Returns:
        True si es válida, False en caso contrario
    """
    required_fields = ["address", "data_type", "description"]

    # Verificar campos requeridos
    for field in required_fields:
        if field not in register:
            return False

    # Validar tipos de datos soportados
    supported_types = ["FLOAT32", "4Q_FP_PF", "INT16", "INT16U", "INT64", "DATETIME"]
    if register["data_type"] not in supported_types:
        return False

    # Validar dirección
    if not isinstance(register["address"], int) or register["address"] < 0:
        return False

    return True
