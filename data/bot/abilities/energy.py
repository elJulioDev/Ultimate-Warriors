import time, random
from config import Config

class EnergyManager:
    __slots__ = ('_input', '_charging', '_last_ki_shot', '_ki_spam_mode', 
                 '_charge_interrupted', '_last_charge_time')
    
    def __init__(self, input_manager):
        self._input = input_manager
        self._charging = False
        self._last_ki_shot = 0
        self._ki_spam_mode = False
        self._charge_interrupted = False
        self._last_charge_time = 0

    def charge_logic(self, bot, enemy, is_being_comboed=False):
        if is_being_comboed:
            if self._charging:
                self._input.release("charge")
                self._charging = False
            return

        distancia = abs(bot.x - enemy.x)
        ahora = time.time()
        
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

        if puede_cargar and bot.carga < 60 and not enemy_charging:
            if random.random() < 0.05:
                self._input.press("charge")
                self._charging = True
            return

        if self._charging:
            if not puede_cargar or bot.carga >= Config.MAX_CARGA:
                self._input.release("charge")
                self._charging = False

    def ki_shot_logic(self, bot, enemy, force_shot=False, is_being_comboed=False):
        ahora = time.time()
        distancia = abs(bot.x - enemy.x)
        
        if is_being_comboed:
            if bot.carga >= 15:
                self._input.press_and_release("shot")
                self._last_ki_shot = ahora
                return True
            return False
        
        teleport_activo = (ahora - bot.last_teleport_time < Config.TELEPORT_COOLDOWN) if hasattr(bot, 'last_teleport_time') else False

        puede_disparar = (
            bot.carga >= Config.KI_SHOT_ENERGY_REQUIRED and
            not bot.cubriendose and
            not bot.acciones.get("golpe") and
            not bot.acciones.get("patada") and
            not teleport_activo
        )
        
        if force_shot:
            puede_disparar = True

        if puede_disparar and (ahora - self._last_ki_shot > Config.KI_SHOT_COOLDOWN):
            if random.random() < 0.8:
                self._input.press_and_release("shot")
                self._last_ki_shot = ahora
                return True
        
        return False