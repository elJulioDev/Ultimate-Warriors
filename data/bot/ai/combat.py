import time
from config import Config

class CombatAI:
    def __init__(self, input_manager, state_manager):
        self.input_manager = input_manager
        self.state_manager = state_manager
        
        # Estado de combate
        self.attacking = False
        self.attack_start_time = 0
        self.current_attack_key = None
        self.last_attack_type = None # 'punch' o 'kick'

    def precise_attack(self, bot, enemy):
        """Lógica de ataque preciso basado en hitboxes"""
        
        # Si el enemigo se cubre, cancelar ataque o intentar romper guardia
        if enemy.cubriendose:
            if self.attacking:
                self._stop_attack()
            
            # Intentar Ki Shot ocasional para romper ritmo
            # (Nota: La lógica principal de Ki Shot está en EnergyManager, 
            # pero aquí se permite una pequeña interacción)
            return

        distancia_x = abs(bot.hit_x - enemy.hitbox_x)
        distancia_y = abs(bot.hit_y - enemy.hitbox_y)

        # SI NO ESTÁ ATACANDO: Iniciar ataque
        if not self.attacking:
            if distancia_x <= Config.RANGO_INICIO_X and distancia_y <= Config.RANGO_INICIO_Y:
                # Decidir tipo de ataque
                if distancia_y > 30:
                    self.current_attack_key = "kick"
                    self.last_attack_type = "kick"
                else:
                    # Alternar golpes para combos variados
                    self.current_attack_key = "punch" if self.last_attack_type != "punch" else "kick"
                    self.last_attack_type = "punch" if self.current_attack_key == "punch" else "kick"
                
                self.input_manager.press(self.current_attack_key)
                self.attacking = True
                self.attack_start_time = time.time()

        # SI YA ESTÁ ATACANDO: Mantener o Cancelar
        else:
            tiempo_atacando = time.time() - self.attack_start_time
            
            # Cancelar si el enemigo se alejó del rango de mantenimiento
            if distancia_x > Config.RANGO_MANTENER_X or distancia_y > Config.RANGO_MANTENER_Y:
                self._stop_attack()
                return
            
            # Cancelar si excedió la duración del ataque (evita quedarse pegado)
            if tiempo_atacando > Config.ATTACK_DURATION:
                self._stop_attack()
                time.sleep(0.04) # Pequeña pausa post-ataque
                return

    def _stop_attack(self):
        if self.current_attack_key:
            self.input_manager.release(self.current_attack_key)
        self.attacking = False
        self.current_attack_key = None