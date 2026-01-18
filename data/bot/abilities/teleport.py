import time
from config import Config


class TeleportManager:
    __slots__ = ('_input', '_last_teleport', '_teleport_history', '_escape_mode')
    
    def __init__(self, input_manager):
        self._input = input_manager
        self._last_teleport = 0
        self._teleport_history = []
        self._escape_mode = False
    
    def execute_teleport(self, bot, enemy, direction=None):
        ahora = time.time()
        
        if not bot.puede_teletransportarse:
            return False
        
        if bot.carga < Config.TELEPORT_ENERGY:
            return False
        
        if ahora - self._last_teleport < Config.TELEPORT_COOLDOWN:
            return False
        
        if direction is None:
            direction = "left" if bot.x > enemy.x else "right"
        
        self._input.press_and_release(direction)
        time.sleep(0.05)
        self._input.press_and_release(direction)
        
        self._last_teleport = ahora
        self._teleport_history.append({
            'time': ahora,
            'direction': direction,
            'bot_x': bot.x,
            'enemy_x': enemy.x
        })
        
        if len(self._teleport_history) > 10:
            self._teleport_history.pop(0)
        
        return True
    
    def offensive_teleport(self, bot, enemy, prediction_x):
        ahora = time.time()
        
        if ahora - self._last_teleport < Config.TELEPORT_COOLDOWN * 0.7:
            return False
        
        bot_to_enemy = enemy.x - bot.x
        bot_to_prediction = prediction_x - bot.x
        
        if abs(bot_to_prediction) < abs(bot_to_enemy):
            direction = "right" if bot_to_prediction > 0 else "left"
            return self.execute_teleport(bot, enemy, direction)
        
        return False
    
    def defensive_teleport(self, bot, enemy):
        self._escape_mode = True
        
        safe_distance = 150
        current_distance = abs(bot.x - enemy.x)
        
        if current_distance < safe_distance:
            direction = "left" if bot.x > enemy.x else "right"
            result = self.execute_teleport(bot, enemy, direction)
            
            if result:
                time.sleep(0.1)
            
            return result
        
        self._escape_mode = False
        return False
    
    def cross_teleport(self, bot, enemy):
        ahora = time.time()
        
        if ahora - self._last_teleport < Config.TELEPORT_COOLDOWN * 1.5:
            return False
        
        direction = "right" if bot.x < enemy.x else "left"
        return self.execute_teleport(bot, enemy, direction)
    
    def can_teleport(self, bot):
        ahora = time.time()
        return (bot.puede_teletransportarse and 
                bot.carga >= Config.TELEPORT_ENERGY and
                ahora - self._last_teleport >= Config.TELEPORT_COOLDOWN)
    
    def reset_escape_mode(self):
        self._escape_mode = False
    
    def is_escape_mode(self):
        return self._escape_mode