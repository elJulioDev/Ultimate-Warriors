import random
from config import Config


class AggressiveStrategy:
    __slots__ = ('_input', '_prediction', '_teleport', '_combo_count', '_last_combo')
    
    def __init__(self, input_manager, prediction_engine, teleport_manager):
        self._input = input_manager
        self._prediction = prediction_engine
        self._teleport = teleport_manager
        self._combo_count = 0
        self._last_combo = 0
    
    def execute(self, bot, enemy, combat_ai, movement_ai, energy_mgr):
        distancia = abs(bot.x - enemy.x)
        
        if distancia > 80:
            self._approach_aggressively(bot, enemy)
        
        if distancia < 50:
            self._pressure_attack(bot, enemy, combat_ai)
        
        if bot.carga > 100 and distancia > 60:
            self._ranged_pressure(bot, enemy, energy_mgr)
        
        if self._should_teleport_in(bot, enemy, distancia):
            self._offensive_teleport(bot, enemy)
    
    def _approach_aggressively(self, bot, enemy):
        pred_x, _ = self._prediction.predict_position(enemy.x, enemy.y, 0.3)
        
        if pred_x > bot.x:
            self._input.press("right")
        else:
            self._input.press("left")
    
    def _pressure_attack(self, bot, enemy, combat_ai):
        if not enemy.cubriendose:
            
            if random.random() < 0.3:
                self._input.press("kick")
            else:
                self._input.press("punch")
        else:
            if bot.carga >= 50:
                self._input.press_and_release("shot")
    
    def _ranged_pressure(self, bot, enemy, energy_mgr):
        if random.random() < 0.6:
            energy_mgr.ki_shot_logic(bot, enemy)
    
    def _should_teleport_in(self, bot, enemy, distancia):
        if not self._teleport.can_teleport(bot):
            return False
        
        if distancia > 100 and distancia < 150:
            pred_x, _ = self._prediction.predict_position(enemy.x, enemy.y, 0.2)
            pred_dist = abs(pred_x - bot.x)
            
            if pred_dist < distancia:
                return True
        
        return False
    
    def _offensive_teleport(self, bot, enemy):
        pred_x, _ = self._prediction.predict_position(enemy.x, enemy.y, 0.2)
        direction = "right" if pred_x > bot.x else "left"
        self._teleport.execute_teleport(bot, enemy, direction)
    
    def attempt_combo(self, bot, enemy):
        import time
        ahora = time.time()
        
        if ahora - self._last_combo < 2:
            return False
        
        distancia = abs(bot.x - enemy.x)
        
        if distancia < 45 and bot.carga > 50:
            self._input.press("punch")
            time.sleep(0.15)
            self._input.release("punch")
            time.sleep(0.05)
            self._input.press("kick")
            time.sleep(0.15)
            self._input.release("kick")
            time.sleep(0.05)
            self._input.press_and_release("shot")
            
            self._combo_count += 1
            self._last_combo = ahora
            return True
        
        return False
    
    def rush_down(self, bot, enemy):
        distancia = abs(bot.x - enemy.x)
        
        if distancia > 50:
            direction = "right" if enemy.x > bot.x else "left"
            self._input.press(direction)
            
            if bot.y > enemy.y + 30:
                self._input.press("jump")
    
    def mix_up_attack(self, bot, enemy):
        if random.random() < 0.4:
            return "kick"
        elif random.random() < 0.7:
            return "punch"
        else:
            if bot.carga > 40:
                return "shot"
            return "punch"