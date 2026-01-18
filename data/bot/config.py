import os
from pathlib import Path


class Config:
    BASE_DIR = Path(__file__).parent.parent
    BOT_DIR = Path(__file__).parent
    
    GAME_DATA_FILE = BASE_DIR / "game_data.json"
    CONTROLS_FILE = BASE_DIR / "controls.json"
    
    JUGADOR_CONTROLADO = "Player 2"
    
    TICK_RATE = 0.05
    
    RANGO_INICIO_X = 38
    RANGO_INICIO_Y = 45
    RANGO_MANTENER_X = 42
    RANGO_MANTENER_Y = 50
    ATTACK_DURATION = 0.4
    
    RANGO_GOLPE_EFECTIVO_X = 40
    RANGO_CORRECCION_MIN_X = 5
    JUMP_DIFF = 65
    JUMP_COOLDOWN = 1.0
    
    LOW_HP_THRESHOLD = 35
    DEFENSE_RANGE = 80
    COVER_DURATION = 1.5
    COVER_COOLDOWN = 1.0
    S_COOLDOWN = 0.25
    
    MAX_CARGA = 282
    CHARGE_DISTANCE = 140
    
    KI_SHOT_COOLDOWN = 0.1
    KI_SHOT_ENERGY_REQUIRED = 25
    KI_SHOT_MIN_DISTANCE = 0
    
    TACKLE_COOLDOWN = 4.0
    TACKLE_ENERGY_REQUIRED = 188
    TACKLE_DISTANCE = 90
    
    TELEPORT_COOLDOWN = 0.3
    TELEPORT_ENERGY = 30
    
    TRANSFORM_COOLDOWN = 2.0
    
    COSTO_TRANSFORMACION = {
        "secuencial": 1,
        "fase2": 2,
        "fase3": 3,
        "fase4": 2,
        "fase5": 3,
        "fase6": 3,
        "cheat": 3
    }
    
    TIMEJUMP_COOLDOWN = 10
    KAIOKEN_COOLDOWN = 15
    
    MAX_HISTORY = 16
    PREDICT_TIME = 0.2
    MAX_VEL = 1500
    VEL_EMA_ALPHA = 0.4
    MAX_PRED_MOVE = 200