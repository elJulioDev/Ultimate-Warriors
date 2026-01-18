import json
from config import Config

class GameReader:
    __slots__ = ('_data_file', '_last_valid_data', '_error_count')
    
    def __init__(self):
        self._data_file = Config.GAME_DATA_FILE
        self._last_valid_data = {}
        self._error_count = 0
    
    def read(self):
        if not self._data_file.exists():
            if self._error_count == 0:
                print(f"Archivo no encontrado: {self._data_file}")
            self._error_count += 1
            return self._last_valid_data
        
        try:
            with open(self._data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            if not self._validate_data(data):
                return self._last_valid_data
            
            self._last_valid_data = data
            self._error_count = 0
            return data
            
        except (json.JSONDecodeError, Exception):
            self._error_count += 1
            return self._last_valid_data
    
    def _validate_data(self, data):
        if not isinstance(data, dict):
            return False
        
        if "jugador1" not in data or "jugador2" not in data:
            return False
        
        required_fields = ["x", "y", "hp", "carga"]
        
        for player in ["jugador1", "jugador2"]:
            player_data = data.get(player, {})
            if not isinstance(player_data, dict):
                return False
            
            for field in required_fields:
                if field not in player_data:
                    return False
        
        return True