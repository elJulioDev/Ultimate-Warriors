"""
Archivo de configuración global del bot
Centraliza todas las constantes y configuraciones
"""

import os
from pathlib import Path


class Config:
    """Configuración global del bot"""
    
    # ==================== RUTAS ====================
    BASE_DIR = Path(__file__).parent.parent  # Carpeta /data
    BOT_DIR = Path(__file__).parent  # Carpeta /data/bot
    
    GAME_DATA_FILE = BASE_DIR / "game_data.json"
    CONTROLS_FILE = BASE_DIR / "controls.json"
    LOGS_DIR = BOT_DIR / "logs"
    
    # Crear carpeta de logs si no existe
    LOGS_DIR.mkdir(exist_ok=True)
    
    # ==================== JUGADOR ====================
    JUGADOR_CONTROLADO = "Player 2"  # "Player 1" o "Player 2"
    
    # ==================== RENDIMIENTO ====================
    TICK_RATE = 0.05  # 50ms → 20 ciclos por segundo
    
    # ==================== COMBATE ====================
    # Rangos de ataque
    RANGO_INICIO_X = 38
    RANGO_INICIO_Y = 45
    RANGO_MANTENER_X = 42
    RANGO_MANTENER_Y = 50
    
    # Duración de ataques
    ATTACK_DURATION = 0.4  # segundos
    
    # ==================== MOVIMIENTO ====================
    RANGO_GOLPE_EFECTIVO_X = 40
    RANGO_CORRECCION_MIN_X = 5
    
    # Salto
    JUMP_DIFF = 65  # Diferencia de altura mínima para saltar
    JUMP_COOLDOWN = 1.0  # segundos entre saltos
    
    # ==================== DEFENSA ====================
    LOW_HP_THRESHOLD = 35
    DEFENSE_RANGE = 80  # distancia máxima para reaccionar
    COVER_DURATION = 1.5  # segundos máximos cubriéndose
    COVER_COOLDOWN = 1.0  # tiempo antes de poder cubrirse otra vez
    S_COOLDOWN = 0.25  # Cooldown especial para tecla S
    
    # ==================== ENERGÍA ====================
    MAX_CARGA = 282
    CHARGE_DISTANCE = 140  # distancia mínima para decidir cargar
    
    # Ki Shot
    KI_SHOT_COOLDOWN = 0.1
    KI_SHOT_ENERGY_REQUIRED = 25
    KI_SHOT_MIN_DISTANCE = 0
    
    # Tackle
    TACKLE_COOLDOWN = 4.0
    TACKLE_ENERGY_REQUIRED = 188  # nivel 2
    TACKLE_DISTANCE = 90
    
    # ==================== TELETRANSPORTE ====================
    TELEPORT_COOLDOWN = 0.3  # segundos
    TELEPORT_ENERGY = 30  # mínimo de carga necesaria
    
    # ==================== TRANSFORMACIONES ====================
    TRANSFORM_COOLDOWN = 2.0  # segundos entre intentos
    
    COSTO_TRANSFORMACION = {
        "secuencial": 1,
        "fase2": 2,
        "fase3": 3,
        "fase4": 2,
        "fase5": 3,
        "fase6": 3,
        "cheat": 3
    }
    
    # ==================== HABILIDADES ESPECIALES ====================
    # TimeJump
    TIMEJUMP_COOLDOWN = 10  # segundos
    
    # Kaioken
    KAIOKEN_COOLDOWN = 15  # segundos
    
    # ==================== PREDICCIÓN ====================
    MAX_HISTORY = 16  # cuántos puntos guardar para predicción
    PREDICT_TIME = 0.2  # segundos a predecir
    MAX_VEL = 1500  # px/s máximo plausible
    VEL_EMA_ALPHA = 0.4  # suavizado exponencial
    MAX_PRED_MOVE = 200  # px máximo en predicción
    
    # ==================== LOGGING ====================
    LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
    LOG_TO_FILE = True
    LOG_TO_CONSOLE = True
    
    @classmethod
    def get_config_dict(cls):
        """Retorna un diccionario con toda la configuración"""
        return {
            key: value 
            for key, value in cls.__dict__.items() 
            if not key.startswith('_') and key.isupper()
        }
    
    @classmethod
    def print_config(cls):
        """Imprime la configuración actual"""
        print("\n" + "="*60)
        print("CONFIGURACIÓN ACTUAL DEL BOT")
        print("="*60)
        
        config = cls.get_config_dict()
        for key, value in config.items():
            if isinstance(value, Path):
                print(f"{key:30} = {value}")
            elif isinstance(value, dict):
                print(f"{key:30} = ")
                for k, v in value.items():
                    print(f"  {k:28} = {v}")
            else:
                print(f"{key:30} = {value}")
        
        print("="*60 + "\n")


if __name__ == "__main__":
    # Test de configuración
    Config.print_config()