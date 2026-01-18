import time
from config import Config


class ComboBreaker:
    __slots__ = ('_input', '_teleport', '_hit_history', '_last_escape', 
                 '_in_combo', '_combo_start', '_escape_attempts')
    
    def __init__(self, input_manager, teleport_manager):
        self._input = input_manager
        self._teleport = teleport_manager
        self._hit_history = []
        self._last_escape = 0
        self._in_combo = False
        self._combo_start = 0
        self._escape_attempts = 0
    
    def register_hit(self):
        ahora = time.time()
        self._hit_history.append(ahora)
        
        if len(self._hit_history) > 10:
            self._hit_history.pop(0)
    
    def is_being_comboed(self):
        ahora = time.time()
        recent_time = ahora - Config.COMBO_DETECTION_TIME
        
        recent_hits = [t for t in self._hit_history if t > recent_time]
        
        if len(recent_hits) >= Config.COMBO_DETECTION_HITS:
            if not self._in_combo:
                self._in_combo = True
                self._combo_start = ahora
                self._escape_attempts = 0
            return True
        else:
            if self._in_combo and ahora - self._combo_start > 1.0:
                self._in_combo = False
            return False
    
    def try_escape(self, bot, enemy):
        ahora = time.time()
        
        if ahora - self._last_escape < 0.2:
            return False
        
        distancia = abs(bot.x - enemy.x)
        
        if bot.carga >= Config.COMBO_ESCAPE_ENERGY:
            if distancia < 60:
                self._input.press_and_release("shot")
                self._last_escape = ahora
                self._escape_attempts += 1
                return True
        
        if self._teleport.can_teleport(bot):
            if bot.carga >= Config.TELEPORT_ENERGY:
                direction = "left" if bot.x > enemy.x else "right"
                self._teleport.execute_teleport(bot, enemy, direction)
                self._last_escape = ahora
                self._escape_attempts += 1
                return True
        
        if bot.carga >= 15 and self._escape_attempts < 5:
            self._input.press_and_release("shot")
            self._last_escape = ahora
            self._escape_attempts += 1
            return True
        
        return False
    
    def emergency_escape(self, bot, enemy):
        ahora = time.time()
        
        if ahora - self._last_escape < 0.1:
            return False
        
        self._input.press_and_release("shot")
        time.sleep(0.05)
        
        if bot.carga >= Config.TELEPORT_ENERGY:
            direction = "left" if bot.x > enemy.x else "right"
            self._input.press_and_release(direction)
            time.sleep(0.03)
            self._input.press_and_release(direction)
        
        self._last_escape = ahora
        return True
    
    def reset(self):
        self._hit_history.clear()
        self._in_combo = False
        self._escape_attempts = 0