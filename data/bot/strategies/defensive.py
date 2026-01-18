import time
import random
from config import Config


class DefensiveStrategy:
    __slots__ = ('_input', '_pattern', '_teleport', '_last_retreat', '_safe_distance',
                 '_last_counter', '_heal_attempts')
    
    def __init__(self, input_manager, pattern_analyzer, teleport_manager):
        self._input = input_manager
        self._pattern = pattern_analyzer
        self._teleport = teleport_manager
        self._last_retreat = 0
        self._safe_distance = 120
        self._last_counter = 0
        self._heal_attempts = 0
    
    def execute(self, bot, enemy, defense_ai):
        distancia = abs(bot.x - enemy.x)
        
        if distancia < self._safe_distance:
            self._maintain_distance(bot, enemy, distancia)
        
        if self._should_escape(bot, enemy, distancia):
            self._execute_escape(bot, enemy)
        
        if self._can_counter_safely(bot, enemy, distancia):
            self._counter_attack(bot, enemy)
        
        self._defensive_positioning(bot, enemy)
    
    def _maintain_distance(self, bot, enemy, current_distance):
        if current_distance < self._safe_distance * 0.7:
            self._retreat(bot, enemy)
        elif current_distance < self._safe_distance:
            if enemy.acciones.get("golpe") or enemy.acciones.get("patada"):
                self._input.press("cover")
    
    def _retreat(self, bot, enemy):
        ahora = time.time()
        
        if ahora - self._last_retreat < 0.5:
            return
        
        retreat_dir = "left" if bot.x > enemy.x else "right"
        self._input.press(retreat_dir)
        
        if random.random() < 0.3 and bot.y - enemy.y < 40:
            self._input.press("jump")
        
        self._last_retreat = ahora
    
    def _should_escape(self, bot, enemy, distancia):
        if bot.hp < 20:
            return True
        
        danger = self._pattern.calculate_danger_level(bot, enemy, distancia)
        
        if danger > 7 and distancia < 60:
            return True
        
        if enemy.cap_form_actual > bot.cap_form_actual + 2:
            return True
        
        return False
    
    def _execute_escape(self, bot, enemy):
        if self._teleport.can_teleport(bot):
            self._teleport.defensive_teleport(bot, enemy)
        else:
            self._retreat(bot, enemy)
            
            if bot.carga > 30 and random.random() < 0.5:
                self._input.press_and_release("shot")
    
    def _can_counter_safely(self, bot, enemy, distancia):
        ahora = time.time()
        
        if ahora - self._last_counter < 1.5:
            return False
        
        if distancia > 80:
            return False
        
        if self._pattern.should_counter_attack(distancia):
            if bot.hp > 35 and bot.carga > 50:
                return True
        
        return False
    
    def _counter_attack(self, bot, enemy):
        ahora = time.time()
        
        attack_dist = self._pattern.predict_attack_distance()
        current_dist = abs(bot.x - enemy.x)
        
        if current_dist <= attack_dist + 10:
            if random.random() < 0.6:
                self._input.press("punch")
                time.sleep(0.1)
                self._input.release("punch")
            else:
                self._input.press_and_release("shot")
            
            self._last_counter = ahora
    
    def _defensive_positioning(self, bot, enemy):
        optimal_y_diff = 40
        current_y_diff = bot.y - enemy.y
        
        if abs(current_y_diff) < optimal_y_diff / 2:
            if random.random() < 0.2:
                self._input.press("jump")
    
    def should_heal_opportunity(self, bot, enemy):
        distancia = abs(bot.x - enemy.x)
        
        if bot.hp < 30 and distancia > 150:
            if not enemy.acciones.get("disparando"):
                return True
        
        return False
    
    def execute_heal(self, bot):
        if bot.carga < Config.MAX_CARGA * 0.7:
            self._input.press("charge")
            self._heal_attempts += 1
    
    def punish_whiff(self, bot, enemy):
        if enemy.acciones.get("golpe") or enemy.acciones.get("patada"):
            distancia = abs(bot.x - enemy.x)
            
            if distancia > 60 and distancia < 100:
                if bot.carga > 40:
                    self._input.press_and_release("shot")
                    return True
        
        return False
    
    def adaptive_defense(self, bot, enemy):
        if self._pattern.is_aggressive_player():
            self._safe_distance = 140
        else:
            self._safe_distance = 100
    
    def bait_and_punish(self, bot, enemy):
        distancia = abs(bot.x - enemy.x)
        
        if distancia > 70 and distancia < 90:
            if random.random() < 0.3:
                forward_dir = "right" if enemy.x > bot.x else "left"
                self._input.press(forward_dir)
                time.sleep(0.05)
                self._input.release(forward_dir)
                
                backward_dir = "left" if enemy.x > bot.x else "right"
                self._input.press(backward_dir)
                time.sleep(0.1)
                self._input.release(backward_dir)
    
    def reset(self):
        self._safe_distance = 120
        self._heal_attempts = 0