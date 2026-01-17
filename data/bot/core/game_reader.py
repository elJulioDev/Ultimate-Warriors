"""
Módulo de lectura de datos del juego
"""

import json
from pathlib import Path
from config import Config


class GameReader:
    """Lee y procesa los datos de game_data.json"""
    
    def __init__(self):
        self.data_file = Config.GAME_DATA_FILE
        self.last_data = {}
    
    def read(self):
        """Lee el archivo game_data.json y retorna los datos"""
        if not self.data_file.exists():
            return {}
        
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.last_data = data
                return data
        except json.JSONDecodeError:
            return self.last_data  # Retornar último dato válido
        except Exception:
            return {}


# ==================== core/input_manager.py ====================
"""
Gestor de entradas de teclado
"""

import json
import keyboard
from config import Config


class InputManager:
    """Gestiona las teclas y entrada del teclado"""
    
    def __init__(self):
        self.teclas = {}
        self.load_controls()
    
    def load_controls(self):
        """Carga las teclas desde controls.json"""
        if not Config.CONTROLS_FILE.exists():
            return
        
        try:
            with open(Config.CONTROLS_FILE, "r", encoding="utf-8") as f:
                controles = json.load(f)["Controls"][Config.JUGADOR_CONTROLADO]
            
            self.teclas = {
                "jump": controles["Movement"].get("Jump", "").lower(),
                "left": controles["Movement"].get("Left", "").lower(),
                "right": controles["Movement"].get("Right", "").lower(),
                "cover": controles["Movement"].get("Cover up", "").lower(),
                "punch": controles["Combat"].get("Punch", "").lower(),
                "kick": controles["Combat"].get("Kick", "").lower(),
                "charge": controles["Energy"].get("Charge", "").lower(),
                "shot": controles["Energy"].get("Ki shot", "").lower(),
                "tackle": controles["Energy"].get("Tackle", "").lower(),
                "emote": controles.get("Emote", "").lower()
            }
        except Exception:
            pass
    
    def get_pause_key(self):
        """Retorna la tecla de pausa"""
        if not Config.CONTROLS_FILE.exists():
            return "enter"
        
        try:
            with open(Config.CONTROLS_FILE, "r", encoding="utf-8") as f:
                datos = json.load(f)
                return datos.get("Controls", {}).get("Others", {}).get("Pause", "ENTER").lower()
        except:
            return "enter"
    
    def press(self, key_name):
        """Presiona una tecla"""
        key = self.teclas.get(key_name)
        if key:
            keyboard.press(key)
    
    def release(self, key_name):
        """Suelta una tecla"""
        key = self.teclas.get(key_name)
        if key:
            keyboard.release(key)
    
    def press_and_release(self, key_name):
        """Presiona y suelta una tecla"""
        key = self.teclas.get(key_name)
        if key:
            keyboard.press_and_release(key)
    
    def release_all_keys(self):
        """Suelta todas las teclas"""
        for key in self.teclas.values():
            keyboard.release(key)


# ==================== core/state_manager.py ====================
"""
Gestor de estado del bot y del enemigo
"""

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class PlayerState:
    """Estado de un jugador"""
    x: float = 0
    y: float = 0
    hit_x: float = 0
    hit_y: float = 0
    hitbox_x: float = 0
    hitbox_y: float = 0
    hp: float = 100
    carga: float = 0
    ki: int = 0
    damaged: int = 0
    defence: int = 0
    speed: int = 0
    transformado: bool = False
    cap_form_actual: int = 0
    cubriendose: bool = False
    colision: bool = False
    cantidad_transformaciones: int = 0
    puede_transformarse: bool = False
    maxima_transformacion: int = 0
    forma_cheat: str = ""
    puede_kaioken: str = ""
    puede_timejump: bool = False
    puede_teletransportarse: bool = False
    clash_tackle: bool = False
    estado_critico: bool = False
    fase_actual: str = "base"
    acciones: Dict[str, bool] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Crea un PlayerState desde un diccionario"""
        hit = data.get("hit", {})
        hitbox = data.get("hitbox", {})
        
        return cls(
            x=data.get("x", 0),
            y=data.get("y", 0),
            hit_x=hit.get("x", 0),
            hit_y=hit.get("y", 0),
            hitbox_x=hitbox.get("x", 0),
            hitbox_y=hitbox.get("y", 0),
            hp=data.get("hp", 100),
            carga=data.get("carga", 0),
            ki=data.get("ki", 0),
            damaged=data.get("damaged", 0),
            defence=data.get("defence", 0),
            speed=data.get("speed", 0),
            transformado=data.get("transformado", False),
            cap_form_actual=data.get("cap form actual", 0),
            cubriendose=data.get("cubriendose", False),
            colision=data.get("colision", False),
            cantidad_transformaciones=data.get("cantidad de transformaciones", 0),
            puede_transformarse=data.get("puede transformarse", False),
            maxima_transformacion=data.get("Maxima transformacion", 0),
            forma_cheat=data.get("Forma Cheat", ""),
            puede_kaioken=data.get("puede usar kaioken", ""),
            puede_timejump=data.get("puede usar timejump", False),
            puede_teletransportarse=data.get("puede teletransportarse", False),
            clash_tackle=data.get("ClashTackle", False),
            estado_critico=data.get("estado critico", False),
            fase_actual=data.get("fase actual", "base"),
            acciones=data.get("acciones", {})
        )


class StateManager:
    """Gestiona el estado del bot y del enemigo"""
    
    def __init__(self):
        self.bot = PlayerState()
        self.enemy = PlayerState()
    
    def update(self, game_data: Dict[str, Any], controlled_player: str):
        """Actualiza el estado basado en los datos del juego"""
        if controlled_player == "Player 2":
            self.bot = PlayerState.from_dict(game_data.get("jugador2", {}))
            self.enemy = PlayerState.from_dict(game_data.get("jugador1", {}))
        else:
            self.bot = PlayerState.from_dict(game_data.get("jugador1", {}))
            self.enemy = PlayerState.from_dict(game_data.get("jugador2", {}))