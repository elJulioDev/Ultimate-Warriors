import time
from config import Config
from utils.constants import nivel_carga


class TransformationManager:
    __slots__ = ('_input', '_last_transform', '_last_s_press')
    
    def __init__(self, input_manager):
        self._input = input_manager
        self._last_transform = 0
        self._last_s_press = 0.0
    
    def transform_logic(self, bot, enemy, is_attacking):
        if is_attacking:
            return
        
        ahora = time.time()
        
        cooldown_base = 2.0
        cooldown_extra = (bot.maxima_transformacion - bot.cap_form_actual) * 1.2
        cooldown_actual = min(12.0, cooldown_base + cooldown_extra)
        
        if ahora - self._last_transform < cooldown_actual:
            return
        
        if not bot.puede_transformarse or bot.cantidad_transformaciones < 1:
            return
        
        if bot.cap_form_actual >= bot.maxima_transformacion:
            return
        
        score = self._calculate_score(bot, enemy)
        umbral = 3.5 + (bot.cap_form_actual * 0.5)
        
        if score < umbral:
            return
        
        tipo_trans = self._select_type(bot, score)
        
        if tipo_trans:
            self._execute(tipo_trans)
            self._last_transform = ahora
    
    def _calculate_score(self, bot, enemy):
        score = 0
        
        if enemy.damaged > bot.damaged: score += 1
        if enemy.defence > bot.defence: score += 1
        if enemy.speed > bot.speed: score += 1
        
        if bot.hp < 60 and enemy.hp > bot.hp: score += 2
        
        if enemy.cap_form_actual > bot.cap_form_actual: score += 1.5
        
        if enemy.forma_cheat and not bot.forma_cheat: score += 2
        
        if bot.hp < 30: score += 2
        
        hp_diff = enemy.hp - bot.hp
        if hp_diff > 30: score += 1
        
        return score
    
    def _select_type(self, bot, score):
        nivel = nivel_carga(bot.carga)
        costos = Config.COSTO_TRANSFORMACION
        max_form = bot.maxima_transformacion
        
        if bot.cantidad_transformaciones <= 2:
            if nivel >= costos["secuencial"]:
                return "secuencial"
            return None
        
        if score >= 6 and nivel >= costos["fase6"] and max_form >= 6:
            return "fase6"
        elif score >= 5 and nivel >= costos["fase5"] and max_form >= 5:
            return "fase5"
        elif score >= 4 and nivel >= costos["fase4"] and max_form >= 4:
            return "fase4"
        elif score >= 3 and nivel >= costos["fase3"] and max_form >= 3:
            return "fase3"
        elif score >= 2 and nivel >= costos["fase2"] and max_form >= 2:
            return "fase2"
        elif nivel >= costos["secuencial"]:
            return "secuencial"
        
        return None
    
    def _execute(self, tipo):
        ahora = time.time()
        
        if ahora - self._last_s_press < Config.S_COOLDOWN:
            return
        
        self._input.press("cover")
        time.sleep(0.08)
        
        if tipo == "secuencial":
            self._input.press("punch")
            time.sleep(0.25)
            self._input.release("punch")
        
        elif tipo == "fase2":
            self._input.press("left")
            time.sleep(0.02)
            self._input.press("punch")
            time.sleep(0.25)
            self._input.release("punch")
            self._input.release("left")
        
        elif tipo == "fase3":
            self._input.press("left")
            time.sleep(0.02)
            self._input.press("right")
            time.sleep(0.02)
            self._input.press("punch")
            time.sleep(0.25)
            self._input.release("punch")
            self._input.release("right")
            self._input.release("left")
        
        elif tipo == "fase4":
            self._input.press("kick")
            time.sleep(0.25)
            self._input.release("kick")
        
        elif tipo == "fase5":
            self._input.press("left")
            time.sleep(0.02)
            self._input.press("kick")
            time.sleep(0.25)
            self._input.release("kick")
            self._input.release("left")
        
        elif tipo == "fase6":
            self._input.press("left")
            time.sleep(0.02)
            self._input.press("shot")
            time.sleep(0.25)
            self._input.release("shot")
            self._input.release("left")
        
        elif tipo == "cheat":
            self._input.press("left")
            time.sleep(0.02)
            self._input.press("right")
            time.sleep(0.02)
            self._input.press("shot")
            time.sleep(0.25)
            self._input.release("shot")
            self._input.release("right")
            self._input.release("left")
        
        self._input.release("cover")
        self._last_s_press = time.time()