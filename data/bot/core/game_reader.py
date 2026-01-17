"""
Módulo de lectura de datos del juego
Lee y valida el archivo game_data.json generado por VBA
"""

import json
from pathlib import Path
from config import Config


class GameReader:
    """Lee y procesa los datos de game_data.json"""
    
    def __init__(self):
        self.data_file = Config.GAME_DATA_FILE
        self.last_valid_data = {}
        self.read_count = 0
        self.error_count = 0
    
    def read(self):
        """
        Lee el archivo game_data.json y retorna los datos
        
        Returns:
            dict: Datos del juego con estructura {jugador1: {...}, jugador2: {...}}
            Si hay error, retorna el último dato válido o {}
        """
        # Verificar que el archivo existe
        if not self.data_file.exists():
            if self.error_count == 0:  # Solo mostrar una vez
                print(f"⚠️ Archivo no encontrado: {self.data_file}")
            self.error_count += 1
            return self.last_valid_data
        
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            # Validar estructura básica
            if not self._validate_data(data):
                print("⚠️ Estructura de datos inválida en game_data.json")
                return self.last_valid_data
            
            # Datos válidos
            self.last_valid_data = data
            self.read_count += 1
            self.error_count = 0  # Reset error counter
            
            return data
            
        except json.JSONDecodeError as e:
            if self.error_count < 3:  # Evitar spam de errores
                print(f"⚠️ Error de formato JSON: {e}")
            self.error_count += 1
            return self.last_valid_data
            
        except Exception as e:
            if self.error_count < 3:
                print(f"⚠️ Error al leer game_data.json: {e}")
            self.error_count += 1
            return self.last_valid_data
    
    def _validate_data(self, data):
        """
        Valida que los datos tengan la estructura esperada
        
        Args:
            data: Diccionario con los datos del juego
            
        Returns:
            bool: True si la estructura es válida
        """
        if not isinstance(data, dict):
            return False
        
        # Verificar que existan jugador1 y jugador2
        if "jugador1" not in data or "jugador2" not in data:
            return False
        
        # Verificar campos mínimos necesarios
        required_fields = ["x", "y", "hp", "carga"]
        
        for player in ["jugador1", "jugador2"]:
            player_data = data.get(player, {})
            if not isinstance(player_data, dict):
                return False
            
            # Verificar campos requeridos
            for field in required_fields:
                if field not in player_data:
                    return False
        
        return True
    
    def get_stats(self):
        """Retorna estadísticas de lectura"""
        return {
            "reads": self.read_count,
            "errors": self.error_count,
            "has_valid_data": bool(self.last_valid_data)
        }
    
    def reset_stats(self):
        """Reinicia los contadores de estadísticas"""
        self.read_count = 0
        self.error_count = 0