import time
import random
from config import Config

class SpecialMovesManager:
    def __init__(self, input_manager):
        self.input_manager = input_manager
        self.last_tackle = 0
        self.last_timejump = 0
        self.last_kaioken = 0

    def tackle_logic(self, bot, enemy):
        ahora = time.time()
        distancia = abs(bot.x - enemy.x)
        
        puede = (
            bot.carga >= Config.TACKLE_ENERGY_REQUIRED and
            not bot.cubriendose and
            not bot.acciones.get("golpe") and
            distancia < Config.TACKLE_DISTANCE
        )
        
        if puede and (ahora - self.last_tackle >= Config.TACKLE_COOLDOWN):
            self.input_manager.press("tackle")
            time.sleep(0.4)
            self.input_manager.release("tackle")
            self.last_tackle = ahora

    def timejump_logic(self, bot, enemy):
        ahora = time.time()
        distancia = abs(bot.x - enemy.x)
        
        if (bot.puede_timejump and 
            bot.ki >= 2 and 
            bot.cubriendose and 
            ahora - self.last_timejump >= Config.TIMEJUMP_COOLDOWN and
            (bot.hp < 60 or distancia < 100)):
            
            # Combo TimeJump: Cover + Punch + Punch
            self.input_manager.press("cover")
            time.sleep(0.05)
            self.input_manager.press_and_release("punch")
            time.sleep(0.05)
            self.input_manager.press_and_release("punch")
            self.input_manager.release("cover")
            
            self.last_timejump = ahora

    def kaioken_logic(self, bot, enemy):
        ahora = time.time()
        # Verificar estado fase para no activar si ya es UI/UE etc
        fases_prohibidas = ("ui", "mui", "ssfp", "black", "ue")
        
        if (bot.cubriendose and
            bot.puede_kaioken and
            bot.fase_actual not in fases_prohibidas and
            bot.ki >= 1 and
            ahora - self.last_kaioken >= Config.KAIOKEN_COOLDOWN):
            
            # Combo Kaioken: Cover + Shot + Shot
            self.input_manager.press("cover")
            time.sleep(0.05)
            self.input_manager.press_and_release("shot")
            time.sleep(0.05)
            self.input_manager.press_and_release("shot")
            self.input_manager.release("cover")
            
            self.last_kaioken = ahora

    def handle_clash_tackle(self, bot):
        """Mecánica de machacar botones en un choque"""
        if bot.clash_tackle:
            # Elegir aleatoriamente entre golpe y patada para simular spam
            btn = "punch" if random.random() > 0.5 else "kick"
            self.input_manager.press(btn)
            time.sleep(random.uniform(0.01, 0.02))
            self.input_manager.release(btn)