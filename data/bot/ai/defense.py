import time
import random
from config import Config

class PatternAnalyzer:
    """Sub-sistema para analizar patrones del enemigo"""
    def __init__(self):
        self.attack_history = []
    
    def analyze(self, bot, enemy):
        # Registrar ataque si ocurre
        if enemy.acciones.get("golpe") or enemy.acciones.get("patada"):
            distancia = abs(enemy.x - bot.x)
            self.attack_history.append({
                'time': time.time(),
                'distance': distancia
            })
            # Mantener solo los últimos 20
            if len(self.attack_history) > 20:
                self.attack_history.pop(0)
    
    def predict_attack(self, current_distance):
        if len(self.attack_history) < 3:
            return False
        
        recent_attacks = self.attack_history[-5:]
        avg_dist = sum(a['distance'] for a in recent_attacks) / len(recent_attacks)
        
        # Si estamos cerca de la distancia promedio donde suele atacar
        return abs(current_distance - avg_dist) < 30

class DefenseAI:
    def __init__(self, input_manager, state_manager):
        self.input_manager = input_manager
        self.state_manager = state_manager
        self.analyzer = PatternAnalyzer()
        
        # Estado defensa
        self.covering = False
        self.cover_start_time = 0
        self.last_cover_time = 0
        
        # Estado teleport
        self.last_teleport_time = 0

    def intelligent_dodge(self, bot, enemy):
        """Sistema de esquiva predictiva y reactiva (Prioridad 1)"""
        ahora = time.time()
        
        # Actualizar análisis
        self.analyzer.analyze(bot, enemy)
        
        distancia = abs(bot.x - enemy.x)
        atacando_enemigo = enemy.acciones.get("golpe") or enemy.acciones.get("patada")
        disparando_enemigo = enemy.acciones.get("disparando")
        
        # 1. ESQUIVA PREDICTIVA
        if self.analyzer.predict_attack(distancia) and distancia < 70:
            if self._try_teleport(bot, enemy, ahora):
                return True
                
        # 2. ESQUIVA REACTIVA (Emergencia)
        if atacando_enemigo and distancia < 50:
            # Intentar teleport si el cooldown corto ha pasado
            if bot.puede_teletransportarse and bot.carga >= Config.TELEPORT_ENERGY:
                 if ahora - self.last_teleport_time > 0.2:
                    if self._try_teleport(bot, enemy, ahora):
                        return True

        # 3. ESQUIVA DE KI SHOTS
        if disparando_enemigo and distancia > 80:
            if random.random() < 0.6:
                # Salto simple
                self.input_manager.press("jump")
                time.sleep(0.1)
                self.input_manager.release("jump")
            else:
                # Dash agresivo hacia el enemigo
                direccion = "right" if enemy.x > bot.x else "left"
                self.input_manager.press(direccion)
                time.sleep(0.15)
                self.input_manager.release(direccion)
                
        return False

    def adaptive_strategy(self, bot, enemy):
        """Gestión de cobertura basada en HP"""
        # Si el bot está atacando, no defenderse
        if bot.acciones.get("golpe") or bot.acciones.get("patada"):
            return

        distancia = abs(enemy.x - bot.x)
        ahora = time.time()
        enemigo_atacando = enemy.acciones.get("golpe") or enemy.acciones.get("patada") or enemy.acciones.get("disparando")

        should_cover = False

        # Lógica según HP
        if bot.hp < 25: # CRITICO
            # Huir
            if distancia < 120:
                dir_huida = "left" if bot.x > enemy.x else "right"
                self.input_manager.press(dir_huida)
                time.sleep(0.1)
                self.input_manager.release(dir_huida)
            # Cubrir todo
            if distancia < 100 and enemigo_atacando:
                should_cover = True
                
        elif bot.hp < 50: # BAJO
            if distancia < Config.DEFENSE_RANGE and enemigo_atacando:
                should_cover = True
                
        else: # ALTO (Agresivo)
            # Solo cubrir si está muy cerca y cooldown largo pasado
            if distancia < Config.DEFENSE_RANGE and enemigo_atacando:
                if ahora - self.last_cover_time > Config.COVER_COOLDOWN * 1.5:
                    should_cover = True

        # Ejecutar cobertura
        if should_cover and not self.covering:
            if ahora - self.last_cover_time > Config.COVER_COOLDOWN:
                self.input_manager.press("cover")
                self.covering = True
                self.cover_start_time = ahora
        
        # Soltar cobertura
        if self.covering:
            # Si ya no atacan o pasó el tiempo máximo
            if not enemigo_atacando or ahora - self.cover_start_time > Config.COVER_DURATION * 0.8:
                self.input_manager.release("cover")
                self.covering = False
                self.last_cover_time = ahora

    def _try_teleport(self, bot, enemy, ahora):
        """Intenta ejecutar un teleport si hay recursos"""
        if bot.puede_teletransportarse and bot.carga >= Config.TELEPORT_ENERGY:
            if ahora - self.last_teleport_time > Config.TELEPORT_COOLDOWN:
                # Teleport hacia atrás o cruzado
                direccion = "left" if bot.x > enemy.x else "right"
                self.input_manager.press_and_release(direccion)
                time.sleep(0.05)
                self.input_manager.press_and_release(direccion)
                self.last_teleport_time = ahora
                return True
        return False