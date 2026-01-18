import time
from config import Config


class CombatAI:
    __slots__ = ('_input', '_attacking', '_attack_start', '_current_key', '_last_type')
    
    def __init__(self, input_manager):
        self._input = input_manager
        self._attacking = False
        self._attack_start = 0
        self._current_key = None
        self._last_type = None

    def precise_attack(self, bot, enemy):
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

    def _stop_attack(self):
        if self._current_key:
            self._input.release(self._current_key)
        self._attacking = False
        self._current_key = None
    
    def is_attacking(self):
        return self._attacking