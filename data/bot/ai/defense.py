import time
import random
from config import Config


class PatternAnalyzer:
    __slots__ = ('_attack_history',)
    
    def __init__(self):
        self._attack_history = []
    
    def analyze(self, bot, enemy):
        if enemy.acciones.get("golpe") or enemy.acciones.get("patada"):
            distancia = abs(enemy.x - bot.x)
            self._attack_history.append({
                'time': time.time(),
                'distance': distancia
            })
            
            if len(self._attack_history) > 20:
                self._attack_history.pop(0)
    
    def predict_attack(self, current_distance):
        if len(self._attack_history) < 3:
            return False
        
        recent = self._attack_history[-5:]
        avg_dist = sum(a['distance'] for a in recent) / len(recent)
        
        return abs(current_distance - avg_dist) < 30


class DefenseAI:
    __slots__ = ('_input', '_analyzer', '_covering', '_cover_start', 
                 '_last_cover', '_last_teleport')
    
    def __init__(self, input_manager):
        self._input = input_manager
        self._analyzer = PatternAnalyzer()
        self._covering = False
        self._cover_start = 0
        self._last_cover = 0
        self._last_teleport = 0

    def intelligent_dodge(self, bot, enemy):
        ahora = time.time()
        self._analyzer.analyze(bot, enemy)
        
        distancia = abs(bot.x - enemy.x)
        atacando = enemy.acciones.get("golpe") or enemy.acciones.get("patada")
        disparando = enemy.acciones.get("disparando")
        
        if self._analyzer.predict_attack(distancia) and distancia < 70:
            if self._try_teleport(bot, enemy, ahora):
                return True
                
        if atacando and distancia < 50:
            if bot.puede_teletransportarse and bot.carga >= Config.TELEPORT_ENERGY:
                if ahora - self._last_teleport > 0.2:
                    if self._try_teleport(bot, enemy, ahora):
                        return True

        if disparando and distancia > 80:
            if random.random() < 0.6:
                self._input.press("jump")
                time.sleep(0.1)
                self._input.release("jump")
            else:
                direccion = "right" if enemy.x > bot.x else "left"
                self._input.press(direccion)
                time.sleep(0.15)
                self._input.release(direccion)
                
        return False

    def adaptive_strategy(self, bot, enemy, is_attacking):
        if is_attacking:
            return

        distancia = abs(enemy.x - bot.x)
        ahora = time.time()
        enemigo_atacando = (enemy.acciones.get("golpe") or 
                           enemy.acciones.get("patada") or 
                           enemy.acciones.get("disparando"))

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
            if distancia < Config.DEFENSE_RANGE and enemigo_atacando:
                should_cover = True
        else:
            if distancia < Config.DEFENSE_RANGE and enemigo_atacando:
                if ahora - self._last_cover > Config.COVER_COOLDOWN * 1.5:
                    should_cover = True

        if should_cover and not self._covering:
            if ahora - self._last_cover > Config.COVER_COOLDOWN:
                self._input.press("cover")
                self._covering = True
                self._cover_start = ahora
        
        if self._covering:
            if not enemigo_atacando or ahora - self._cover_start > Config.COVER_DURATION * 0.8:
                self._input.release("cover")
                self._covering = False
                self._last_cover = ahora

    def _try_teleport(self, bot, enemy, ahora):
        if bot.puede_teletransportarse and bot.carga >= Config.TELEPORT_ENERGY:
            if ahora - self._last_teleport > Config.TELEPORT_COOLDOWN:
                direccion = "left" if bot.x > enemy.x else "right"
                self._input.press_and_release(direccion)
                time.sleep(0.05)
                self._input.press_and_release(direccion)
                self._last_teleport = ahora
                return True
        return False