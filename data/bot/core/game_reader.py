import json
import os
from config import Config

class GameReader:
    __slots__ = ('_data_file', '_last_valid_data', '_error_count', 
                 '_file_handle', '_last_mtime', '_buffer_size')
    
    def __init__(self):
        self._data_file = Config.GAME_DATA_FILE
        self._last_valid_data = {}
        self._error_count = 0
        self._file_handle = None
        self._last_mtime = 0
        self._buffer_size = 8192
    
    def read(self):
        if not self._data_file.exists():
            if self._error_count == 0:
                print(f"Archivo no encontrado: {self._data_file}")
            self._error_count += 1
            return self._last_valid_data
        
        try:
            current_mtime = os.path.getmtime(self._data_file)
            
            if current_mtime == self._last_mtime and self._last_valid_data:
                return self._last_valid_data
            
            self._last_mtime = current_mtime
            
            with open(self._data_file, "r", encoding="utf-8", buffering=self._buffer_size) as f:
                data = json.load(f)
                
            if not self._validate_data(data):
                return self._last_valid_data
            
            self._last_valid_data = data
            self._error_count = 0
            return data
            
        except (json.JSONDecodeError, OSError):
            self._error_count += 1
            return self._last_valid_data
    
    def _validate_data(self, data):
        if not isinstance(data, dict):
            return False
        
        j1 = data.get("jugador1")
        j2 = data.get("jugador2")
        
        if not (j1 and j2):
            return False
        
        for player in (j1, j2):
            if not all(k in player for k in ("x", "y", "hp", "carga")):
                return False
        
        return True
    
    def close(self):
        if self._file_handle:
            self._file_handle.close()
            self._file_handle = None