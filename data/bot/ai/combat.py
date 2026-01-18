import time
from config import Config

class CombatAI:
    __slots__ = ('_input', '_attacking', '_attack_start', '_current_key', '_last_type',
                 '_aerial_combo', '_combo_hits', '_last_combo_time')
    
    def __init__(self, input_manager):
        self._input = input_manager
        self._attacking = False
        self._attack_start = 0
        self._current_key = None
        self._last_type = None
        self._aerial_combo = False
        self._combo_hits = 0
        self._last_combo_time = 0

    def precise_attack(self, bot, enemy):
        if bot.cubriendose:
            if self._attacking:
                self._stop_attack()
            return

        if bot.damaged > 0:
            if self._attacking:
                self._stop_attack()
            return
            
        if bot.acciones.get("cargando"):
             if self._attacking:
                self._stop_attack()
             return
        
        if enemy.cubriendose:
            if self._attacking:
                self._stop_attack()
            return

        distancia_x = abs(bot.hit_x - enemy.hitbox_x)
        distancia_y = abs(bot.hit_y - enemy.hitbox_y)

        if not self._attacking:
            if distancia_x <= Config.RANGO_INICIO_X and distancia_y <= Config.RANGO_INICIO_Y:
                if distancia_y > 30:
                    self._current_key = "kick"
                    self._last_type = "kick"
                else:
                    self._current_key = "punch" if self._last_type != "punch" else "kick"
                    self._last_type = "punch" if self._current_key == "punch" else "kick"
                
                self._input.press(self._current_key)
                self._attacking = True
                self._attack_start = time.time()
        else:
            tiempo_atacando = time.time() - self._attack_start
            
            if distancia_x > Config.RANGO_MANTENER_X or distancia_y > Config.RANGO_MANTENER_Y:
                self._stop_attack()
                return
            
            if tiempo_atacando > Config.ATTACK_DURATION:
                self._stop_attack()
                time.sleep(0.04)
                return

    def aerial_combo(self, bot, enemy):
        ahora = time.time()
        
        if ahora - self._last_combo_time < 3:
            return False
        
        distancia_x = abs(bot.hit_x - enemy.hitbox_x)
        distancia_y = abs(bot.hit_y - enemy.hitbox_y)
        
        if distancia_x < 50 and distancia_y < 60:
            self._input.press("jump")
            time.sleep(0.1)
            
            self._input.press("punch")
            time.sleep(0.15)
            self._input.release("punch")
            time.sleep(0.05)
            
            self._input.press("kick")
            time.sleep(0.15)
            self._input.release("kick")
            time.sleep(0.05)
            
            self._input.press("punch")
            time.sleep(0.15)
            self._input.release("punch")
            
            self._input.release("jump")
            
            self._last_combo_time = ahora
            self._combo_hits += 3
            return True
        
        return False
    
    def pre_emptive_attack(self, bot, enemy, prediction_x, prediction_y):
        distancia_pred = abs(prediction_x - bot.hit_x)
        
        if distancia_pred < 60:
            direction = "right" if prediction_x > bot.x else "left"
            
            self._input.press(direction)
            time.sleep(0.05)
            
            self._input.press("punch")
            time.sleep(0.12)
            self._input.release("punch")
            time.sleep(0.03)
            
            self._input.press("kick")
            time.sleep(0.12)
            self._input.release("kick")
            
            self._input.release(direction)
            
            return True
        
        return False
    
    def juggle_combo(self, bot, enemy):
        distancia_x = abs(bot.hit_x - enemy.hitbox_x)
        distancia_y = abs(bot.hit_y - enemy.hitbox_y)
        
        if distancia_x < 45 and distancia_y > 20 and distancia_y < 70:
            self._input.press("kick")
            time.sleep(0.12)
            self._input.release("kick")
            time.sleep(0.04)
            
            self._input.press("punch")
            time.sleep(0.12)
            self._input.release("punch")
            time.sleep(0.04)
            
            self._input.press("kick")
            time.sleep(0.12)
            self._input.release("kick")
            
            if bot.carga >= 50:
                time.sleep(0.05)
                self._input.press_and_release("shot")
            
            return True
        
        return False

    def _stop_attack(self):
        if self._current_key:
            self._input.release(self._current_key)
        self._attacking = False
        self._current_key = None
    
    def is_attacking(self):
        return self._attacking
    
    def get_combo_hits(self):
        return self._combo_hits
    
    def reset_combo_counter(self):
        self._combo_hits = 0