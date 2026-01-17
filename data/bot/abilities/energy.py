import time
import random
from config import Config

class EnergyManager:
    def __init__(self, input_manager):
        self.input_manager = input_manager
        self.charging = False
        self.last_ki_shot_time = 0

    def charge_logic(self, bot, enemy):
        """Gestión de carga de Ki"""
        distancia = abs(bot.x - enemy.x)
        
        # Verificar si es seguro cargar
        puede_cargar = (
            not bot.cubriendose and
            not bot.acciones.get("golpe") and
            not bot.acciones.get("patada") and
            not bot.colision and
            bot.carga < Config.MAX_CARGA and
            distancia > Config.CHARGE_DISTANCE and
            not enemy.acciones.get("disparando")
        )

        enemy_charging = enemy.acciones.get("cargando")

        # 1. Carga espejo: Si el enemigo carga lejos, nosotros también
        if puede_cargar and enemy_charging and distancia > Config.CHARGE_DISTANCE + 20:
            if not self.charging:
                self.input_manager.press("charge")
                self.charging = True
            return

        # 2. Carga oportunista: Poca carga y lejos
        if puede_cargar and bot.carga < 60:
            # Probabilidad baja por frame para no spamear
            if random.random() < 0.05:
                self.input_manager.press("charge")
                self.charging = True
            return

        # Detener carga
        if self.charging and (not puede_cargar or bot.carga >= Config.MAX_CARGA):
            self.input_manager.release("charge")
            self.charging = False

    def ki_shot_logic(self, bot, enemy):
        """Lógica de disparo de Ki"""
        ahora = time.time()
        
        puede_disparar = (
            bot.carga >= Config.KI_SHOT_ENERGY_REQUIRED and
            not bot.cubriendose and
            not bot.acciones.get("golpe") and
            not bot.acciones.get("patada")
        )

        if puede_disparar and (ahora - self.last_ki_shot_time > Config.KI_SHOT_COOLDOWN):
            # 80% probabilidad de disparo si las condiciones se cumplen
            if random.random() < 0.8:
                self.input_manager.press_and_release("shot")
                self.last_ki_shot_time = ahora