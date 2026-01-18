import time
from config import Config

class MovementAI:
    __slots__ = ('_input', '_moving_left', '_moving_right', '_last_jump', '_jumping')
    
    def __init__(self, input_manager):
        self._input = input_manager
        self._moving_left = False
        self._moving_right = False
        self._last_jump = 0
        self._jumping = False

    def strategic_movement(self, bot, enemy, is_attacking):
        hit_bot_x = bot.hit_x
        hit_enemy_x = enemy.hitbox_x
        colision = bot.colision
        distancia_x = abs(hit_bot_x - hit_enemy_x)
        
        if colision and is_attacking:
            self._stop_movement()
            return

        if distancia_x <= Config.RANGO_CORRECCION_MIN_X:
            if hit_bot_x < hit_enemy_x:
                self._move_left()
            else:
                self._move_right()
            return
        
        if not colision and distancia_x <= Config.RANGO_GOLPE_EFECTIVO_X:
            if hit_bot_x < hit_enemy_x:
                self._move_right()
            else:
                self._move_left()
            return
        
        if colision and distancia_x <= Config.RANGO_GOLPE_EFECTIVO_X:
            self._stop_movement()
            return

        if hit_enemy_x < hit_bot_x:
            self._move_left()
        else:
            self._move_right()

    def jump_logic(self, bot, enemy):
        diff_y = bot.y - enemy.y
        ahora = time.time()

        if self._jumping and ahora - self._last_jump > 1:
            self._jumping = False

        if not self._jumping and diff_y > Config.JUMP_DIFF:
            self._input.press("jump")
            
            if bot.carga < Config.MAX_CARGA and abs(enemy.x - bot.x) > Config.CHARGE_DISTANCE:
                self._input.press("charge")
                time.sleep(0.25)
                self._input.release("charge")
            
            time.sleep(0.3)
            self._input.release("jump")
            
            self._jumping = True
            self._last_jump = ahora

    def _move_left(self):
        self._input.press("left")
        if self._moving_right:
            self._input.release("right")
            self._moving_right = False
        self._moving_left = True

    def _move_right(self):
        self._input.press("right")
        if self._moving_left:
            self._input.release("left")
            self._moving_left = False
        self._moving_right = True

    def _stop_movement(self):
        if self._moving_left:
            self._input.release("left")
            self._moving_left = False
        if self._moving_right:
            self._input.release("right")
            self._moving_right = False