import time, random
from config import Config

class DefenseAI:
    __slots__ = ('_input', '_pattern', '_prediction', '_teleport', '_combo_breaker',
                 '_covering', '_cover_start', '_last_cover', '_last_teleport',
                 '_last_hp', '_hp_drop_counter')
    
    def __init__(self, input_manager, pattern_analyzer, prediction_engine, 
                 teleport_manager, combo_breaker):
        self._input = input_manager
        self._pattern = pattern_analyzer
        self._prediction = prediction_engine
        self._teleport = teleport_manager
        self._combo_breaker = combo_breaker
        self._covering = False
        self._cover_start = 0
        self._last_cover = 0
        self._last_teleport = 0
        self._last_hp = 100
        self._hp_drop_counter = 0

    def intelligent_dodge(self, bot, enemy):
        ahora = time.time()
        
        current_hp = bot.hp
        if current_hp < self._last_hp:
            self._combo_breaker.register_hit()
            self._hp_drop_counter += 1
        else:
            if ahora - self._last_cover > 0.5:
                self._hp_drop_counter = 0
        
        self._last_hp = current_hp
        
        if self._combo_breaker.is_being_comboed():
            if self._combo_breaker.try_escape(bot, enemy):
                return True
            
            if self._hp_drop_counter > 3:
                if self._combo_breaker.emergency_escape(bot, enemy):
                    self._hp_drop_counter = 0
                    return True
        
        self._pattern.analyze_attack_pattern(bot, enemy)
        self._prediction.update(enemy.x, enemy.y)
        
        distancia = abs(bot.x - enemy.x)
        atacando = enemy.acciones.get("golpe") or enemy.acciones.get("patada")
        disparando = enemy.acciones.get("disparando")
        
        next_action = self._pattern.predict_next_action(distancia, enemy.hp, enemy.carga)
        
        if next_action == 'attack' and distancia < 70:
            if self._teleport.can_teleport(bot):
                pred_x, _ = self._prediction.predict_position(enemy.x, enemy.y, 0.15)
                
                if abs(pred_x - bot.x) < distancia:
                    if self._teleport.defensive_teleport(bot, enemy):
                        return True
        
        if atacando and distancia < 50:
            if self._teleport.can_teleport(bot):
                if ahora - self._last_teleport > Config.TELEPORT_EMERGENCY_COOLDOWN:
                    if self._teleport.execute_teleport(bot, enemy):
                        self._last_teleport = ahora
                        return True
        
        if disparando and distancia > 80:
            if random.random() < 0.6:
                self._input.press("jump")
                time.sleep(0.1)
                self._input.release("jump")
            else:
                direction = "right" if enemy.x > bot.x else "left"
                self._input.press(direction)
                time.sleep(0.15)
                self._input.release(direction)
        
        if self._prediction.was_teleport_detected():
            pred_x, _ = self._prediction.predict_position(enemy.x, enemy.y, 0.1)
            
            if abs(pred_x - bot.x) < 40:
                if not self._covering:
                    self._input.press("cover")
                    self._covering = True
                    self._cover_start = ahora
                return True
        
        return False

    def adaptive_strategy(self, bot, enemy, is_attacking):
        if is_attacking:
            return

        distancia = abs(enemy.x - bot.x)
        ahora = time.time()
        enemigo_atacando = (enemy.acciones.get("golpe") or 
                           enemy.acciones.get("patada") or 
                           enemy.acciones.get("disparando"))

        danger_level = self._pattern.calculate_danger_level(bot, enemy, distancia)
        should_cover = False

        if bot.hp < 25:
            if distancia < 120:
                dir_huida = "left" if bot.x > enemy.x else "right"
                self._input.press(dir_huida)
                time.sleep(0.1)
                self._input.release(dir_huida)
            
            if distancia < 100 and enemigo_atacando:
                should_cover = True
        
        elif bot.hp < 50:
            if danger_level > 5:
                should_cover = True
            elif distancia < Config.DEFENSE_RANGE and enemigo_atacando:
                should_cover = True
        
        else:
            if danger_level > 7:
                should_cover = True
            elif distancia < Config.DEFENSE_RANGE and enemigo_atacando:
                if ahora - self._last_cover > Config.COVER_COOLDOWN * 1.5:
                    should_cover = True

        if should_cover and not self._covering:
            if ahora - self._last_cover > Config.COVER_COOLDOWN:
                self._input.press("cover")
                self._covering = True
                self._cover_start = ahora
        
        if self._covering:
            max_cover_time = Config.COVER_DURATION * (1.2 if bot.hp < 30 else 0.8)
            
            if not enemigo_atacando or ahora - self._cover_start > max_cover_time:
                self._input.release("cover")
                self._covering = False
                self._last_cover = ahora
    
    def is_covering(self):
        return self._covering
    
    def is_being_comboed(self):
        return self._combo_breaker.is_being_comboed()