import time
from collections import deque


class PatternAnalyzer:
    __slots__ = ('_attack_patterns', '_movement_patterns', '_transform_patterns',
                 '_charge_patterns', '_last_analysis', '_behavior_score')
    
    def __init__(self):
        self._attack_patterns = deque(maxlen=30)
        self._movement_patterns = deque(maxlen=20)
        self._transform_patterns = deque(maxlen=10)
        self._charge_patterns = deque(maxlen=15)
        self._last_analysis = 0
        self._behavior_score = {
            'aggressive': 0,
            'defensive': 0,
            'balanced': 0
        }
    
    def analyze_attack_pattern(self, bot, enemy):
        acciones = enemy.acciones
        
        if acciones.get("golpe") or acciones.get("patada"):
            distancia = abs(enemy.x - bot.x)
            self._attack_patterns.append({
                'time': time.time(),
                'type': 'punch' if acciones.get("golpe") else 'kick',
                'distance': distancia,
                'enemy_hp': enemy.hp,
                'enemy_carga': enemy.carga
            })
    
    def analyze_movement_pattern(self, enemy, previous_x):
        if previous_x is not None:
            movement = enemy.x - previous_x
            if abs(movement) > 2:
                self._movement_patterns.append({
                    'time': time.time(),
                    'direction': 'right' if movement > 0 else 'left',
                    'speed': abs(movement)
                })
    
    def analyze_transformation(self, enemy):
        if enemy.transformado:
            self._transform_patterns.append({
                'time': time.time(),
                'form': enemy.cap_form_actual,
                'hp_at_transform': enemy.hp
            })
    
    def analyze_charge_behavior(self, enemy):
        if enemy.acciones.get("cargando"):
            self._charge_patterns.append({
                'time': time.time(),
                'carga': enemy.carga,
                'distance': 0
            })
    
    def predict_attack_distance(self):
        if len(self._attack_patterns) < 3:
            return 50
        
        recent = list(self._attack_patterns)[-5:]
        avg_distance = sum(a['distance'] for a in recent) / len(recent)
        return avg_distance
    
    def predict_attack_timing(self):
        if len(self._attack_patterns) < 2:
            return None
        
        recent = list(self._attack_patterns)[-3:]
        intervals = []
        for i in range(1, len(recent)):
            intervals.append(recent[i]['time'] - recent[i-1]['time'])
        
        if intervals:
            return sum(intervals) / len(intervals)
        return None
    
    def is_aggressive_player(self):
        if len(self._attack_patterns) < 5:
            return False
        
        recent_time = time.time() - 5
        recent_attacks = [p for p in self._attack_patterns if p['time'] > recent_time]
        
        return len(recent_attacks) >= 3
    
    def is_defensive_player(self):
        if len(self._charge_patterns) < 3:
            return False
        
        recent_time = time.time() - 5
        recent_charges = [p for p in self._charge_patterns if p['time'] > recent_time]
        
        return len(recent_charges) >= 2
    
    def predict_next_action(self, current_distance, enemy_hp, enemy_carga):
        if self.is_aggressive_player():
            if current_distance < self.predict_attack_distance() + 15:
                return 'attack'
        
        if self.is_defensive_player():
            if enemy_carga < 100 and current_distance > 100:
                return 'charge'
        
        if enemy_hp < 30 and len(self._transform_patterns) < enemy_hp / 15:
            return 'transform'
        
        return 'neutral'
    
    def get_movement_tendency(self):
        if len(self._movement_patterns) < 5:
            return 'neutral'
        
        recent = list(self._movement_patterns)[-10:]
        right_moves = sum(1 for m in recent if m['direction'] == 'right')
        left_moves = len(recent) - right_moves
        
        if right_moves > left_moves * 1.5:
            return 'right'
        elif left_moves > right_moves * 1.5:
            return 'left'
        return 'neutral'
    
    def calculate_danger_level(self, bot, enemy, current_distance):
        danger = 0
        
        if self.is_aggressive_player():
            danger += 3
        
        if current_distance < self.predict_attack_distance():
            danger += 2
        
        if enemy.cap_form_actual > bot.cap_form_actual:
            danger += 2
        
        if enemy.hp > bot.hp + 20:
            danger += 1
        
        if enemy.acciones.get("disparando"):
            danger += 1
        
        return min(danger, 10)
    
    def update_behavior_score(self):
        ahora = time.time()
        
        if ahora - self._last_analysis < 2:
            return
        
        self._last_analysis = ahora
        
        recent_time = ahora - 10
        recent_attacks = [p for p in self._attack_patterns if p['time'] > recent_time]
        recent_charges = [p for p in self._charge_patterns if p['time'] > recent_time]
        
        if len(recent_attacks) > 5:
            self._behavior_score['aggressive'] += 1
        elif len(recent_charges) > 3:
            self._behavior_score['defensive'] += 1
        else:
            self._behavior_score['balanced'] += 1
    
    def get_dominant_behavior(self):
        return max(self._behavior_score, key=self._behavior_score.get)
    
    def should_counter_attack(self, current_distance):
        if len(self._attack_patterns) < 3:
            return False
        
        last_attack = self._attack_patterns[-1]
        time_since_attack = time.time() - last_attack['time']
        
        if time_since_attack < 0.5 and current_distance < 60:
            return True
        
        return False
    
    def reset(self):
        self._attack_patterns.clear()
        self._movement_patterns.clear()
        self._transform_patterns.clear()
        self._charge_patterns.clear()
        self._behavior_score = {'aggressive': 0, 'defensive': 0, 'balanced': 0}