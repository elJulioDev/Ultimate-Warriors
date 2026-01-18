import time
import random
from config import Config


class EnergyManager:
    __slots__ = ('_input', '_charging', '_last_ki_shot')
    
    def __init__(self, input_manager):
        self._input = input_manager
        self._charging = False
        self._last_ki_shot = 0

    def charge_logic(self, bot, enemy):
        distancia = abs(bot.x - enemy.x)
        
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

        if puede_cargar and enemy_charging and distancia > Config.CHARGE_DISTANCE + 20:
            if not self._charging:
                self._input.press("charge")
                self._charging = True
            return

        if puede_cargar and bot.carga < 60:
            if random.random() < 0.05:
                self._input.press("charge")
                self._charging = True
            return

        if self._charging and (not puede_cargar or bot.carga >= Config.MAX_CARGA):
            self._input.release("charge")
            self._charging = False

    def ki_shot_logic(self, bot, enemy):
        ahora = time.time()
        
        puede_disparar = (
            bot.carga >= Config.KI_SHOT_ENERGY_REQUIRED and
            not bot.cubriendose and
            not bot.acciones.get("golpe") and
            not bot.acciones.get("patada")
        )

        if puede_disparar and (ahora - self._last_ki_shot > Config.KI_SHOT_COOLDOWN):
            if random.random() < 0.8:
                self._input.press_and_release("shot")
                self._last_ki_shot = ahora