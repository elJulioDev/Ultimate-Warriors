import time
import random
from config import Config

class MovementAI:
    def __init__(self, input_manager, state_manager):
        self.input_manager = input_manager
        self.state_manager = state_manager
        
        # Estados internos
        self.moving_left = False
        self.moving_right = False
        self.last_jump_time = 0
        self.jumping = False

    def strategic_movement(self, bot, enemy):
        """Maneja el movimiento horizontal estratégico"""
        # Si está atacando y colisionando, detener movimiento
        if bot.colision and (bot.acciones.get("golpe") or bot.acciones.get("patada")):
            self._stop_movement()
            return

        distancia_x = abs(bot.hit_x - enemy.hitbox_x)

        # Corregir si está demasiado encima (superposición)
        if distancia_x <= Config.RANGO_CORRECCION_MIN_X:
            if bot.hit_x < enemy.hitbox_x:
                self._move_left()
            else:
                self._move_right()
            return

        # Ajuste fino si está cerca pero sin colisión (Rango de golpe)
        if not bot.colision and distancia_x <= Config.RANGO_GOLPE_EFECTIVO_X:
            if bot.hit_x < enemy.hitbox_x:
                self._move_right() # Acercarse un poco más
            else:
                self._move_left()
            return

        # Detener si ya colisiona y está en rango óptimo
        if bot.colision and distancia_x <= Config.RANGO_GOLPE_EFECTIVO_X:
            self._stop_movement()
            return

        # Perseguir al oponente
        if enemy.hitbox_x < bot.hit_x:
            self._move_left()
        else:
            self._move_right()

    def jump_logic(self, bot, enemy):
        """Lógica de salto y vuelo"""
        diff_y = bot.y - enemy.y
        ahora = time.time()

        # Resetear estado de salto tras 1 segundo
        if self.jumping and ahora - self.last_jump_time > 1:
            self.jumping = False

        # Condición para saltar
        if not self.jumping and diff_y > Config.JUMP_DIFF:
            self.input_manager.press("jump")
            
            # Pequeña carga aérea si está lejos (optimización de tiempo)
            if bot.carga < Config.MAX_CARGA and abs(enemy.x - bot.x) > Config.CHARGE_DISTANCE:
                self.input_manager.press("charge")
                time.sleep(0.25)
                self.input_manager.release("charge")
            
            time.sleep(0.3)
            self.input_manager.release("jump")
            
            self.jumping = True
            self.last_jump_time = ahora

    # --- Helpers privados para evitar redundancia ---
    def _move_left(self):
        self.input_manager.press("left")
        if self.moving_right:
            self.input_manager.release("right")
            self.moving_right = False
        self.moving_left = True

    def _move_right(self):
        self.input_manager.press("right")
        if self.moving_left:
            self.input_manager.release("left")
            self.moving_left = False
        self.moving_right = True

    def _stop_movement(self):
        if self.moving_left:
            self.input_manager.release("left")
            self.moving_left = False
        if self.moving_right:
            self.input_manager.release("right")
            self.moving_right = False