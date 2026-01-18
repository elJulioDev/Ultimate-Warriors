import time
import random
from config import Config

class SpecialMovesManager:
    __slots__ = ('_input', '_last_tackle', '_last_timejump', '_last_kaioken')
    
    def __init__(self, input_manager):
        self._input = input_manager
        self._last_tackle = 0
        self._last_timejump = 0
        self._last_kaioken = 0

    def tackle_logic(self, bot, enemy):
        ahora = time.time()
        distancia = abs(bot.x - enemy.x)
        
        puede = (
            bot.carga >= Config.TACKLE_ENERGY_REQUIRED and
            not bot.cubriendose and
            not bot.acciones.get("golpe") and
            distancia < Config.TACKLE_DISTANCE
        )
        
        if puede and (ahora - self._last_tackle >= Config.TACKLE_COOLDOWN):
            self._input.press("tackle")
            time.sleep(0.4)
            self._input.release("tackle")
            self._last_tackle = ahora

    def timejump_logic(self, bot, enemy):
        ahora = time.time()
        distancia = abs(bot.x - enemy.x)
        
        if (bot.puede_timejump and 
            bot.ki >= 2 and 
            bot.cubriendose and 
            ahora - self._last_timejump >= Config.TIMEJUMP_COOLDOWN and
            (bot.hp < 60 or distancia < 100)):
            
            self._input.press("cover")
            time.sleep(0.05)
            self._input.press_and_release("punch")
            time.sleep(0.05)
            self._input.press_and_release("punch")
            self._input.release("cover")
            
            self._last_timejump = ahora

    def kaioken_logic(self, bot, enemy):
        ahora = time.time()
        fases_prohibidas = ("ui", "mui", "ssfp", "black", "ue")
        
        if (bot.cubriendose and
            bot.puede_kaioken and
            bot.fase_actual not in fases_prohibidas and
            bot.ki >= 1 and
            ahora - self._last_kaioken >= Config.KAIOKEN_COOLDOWN):
            
            self._input.press("cover")
            time.sleep(0.05)
            self._input.press_and_release("shot")
            time.sleep(0.05)
            self._input.press_and_release("shot")
            self._input.release("cover")
            
            self._last_kaioken = ahora

    def handle_clash_tackle(self, bot):
        if bot.clash_tackle:
            btn = "punch" if random.random() > 0.5 else "kick"
            self._input.press(btn)
            time.sleep(random.uniform(0.01, 0.02))
            self._input.release(btn)