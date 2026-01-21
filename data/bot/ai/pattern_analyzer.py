import time
from collections import deque

class PatternAnalyzer:
    __slots__ = ('_attack_patterns', '_movement_patterns', '_transform_patterns',
                 '_charge_patterns', '_last_analysis', '_behavior_score',
                 '_cached_aggressive', '_cached_defensive', '_cache_time',
                 '_cache_duration')
    
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
        
        self._cached_aggressive = False
        self._cached_defensive = False
        self._cache_time = 0
        self._cache_duration = 0.5
    
    def analyze_attack_pattern(self, bot, enemy):
        acciones = enemy.acciones
        
        if not (acciones.get("golpe") or acciones.get("patada")):
            return
        
        now = time.time()
        distancia = abs(enemy.x - bot.x)
        
        self._attack_patterns.append({
            'time': now,
            'type': 'punch' if acciones.get("golpe") else 'kick',
            'distance': distancia,
            'enemy_hp': enemy.hp,
            'enemy_carga': enemy.carga
        })
        
        self._cache_time = 0
    
    def analyze_movement_pattern(self, enemy, previous_x):
        if previous_x is None:
            return
        
        movement = enemy.x - previous_x
        
        if abs(movement) > 5:
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
        length = len(self._attack_patterns)
        
        if length < 3:
            return 50
        
        recent = list(self._attack_patterns)[-5:]
        total = sum(a['distance'] for a in recent)
        return total / len(recent)
    
    def predict_attack_timing(self):
        length = len(self._attack_patterns)
        
        if length < 2:
            return None
        
        recent = list(self._attack_patterns)[-3:]

        if len(recent) < 2:
            return None
        
        intervals = [recent[i]['time'] - recent[i-1]['time'] 
                    for i in range(1, len(recent))]
        
        return sum(intervals) / len(intervals) if intervals else None
    
    def is_aggressive_player(self):
        now = time.time()
        
        if now - self._cache_time < self._cache_duration:
            return self._cached_aggressive
        
        if len(self._attack_patterns) < 5:
            self._cached_aggressive = False
            self._cache_time = now
            return False
        
        recent_time = now - 5
        
        recent_count = sum(1 for p in self._attack_patterns if p['time'] > recent_time)
        
        self._cached_aggressive = recent_count >= 3
        self._cache_time = now
        return self._cached_aggressive
    
    def is_defensive_player(self):
        now = time.time()
        
        if now - self._cache_time < self._cache_duration:
            return self._cached_defensive
        
        if len(self._charge_patterns) < 3:
            self._cached_defensive = False
            self._cache_time = now
            return False
        
        recent_time = now - 5
        
        recent_count = sum(1 for p in self._charge_patterns if p['time'] > recent_time)
        
        self._cached_defensive = recent_count >= 2
        self._cache_time = now
        return self._cached_defensive
    
    def predict_next_action(self, current_distance, enemy_hp, enemy_carga):
        if self.is_aggressive_player():
            if current_distance < self.predict_attack_distance() + 15:
                return 'attack'
        
        if self.is_defensive_player():
            if enemy_carga < 100 and current_distance > 100:
                return 'charge'
        
        if enemy_hp < 30 and len(self._transform_patterns) < enemy_hp // 15:
            return 'transform'
        
        return 'neutral'
    
    def get_movement_tendency(self):
        length = len(self._movement_patterns)
        
        if length < 5:
            return 'neutral'
        
        recent = list(self._movement_patterns)[-10:]
        right_moves = sum(1 for m in recent if m['direction'] == 'right')
        left_moves = length - right_moves
        
        if right_moves > left_moves * 1.5:
            return 'right'
        elif left_moves > right_moves * 1.5:
            return 'left'
        return 'neutral'
    
    def calculate_danger_level(self, bot, enemy, current_distance):
        danger = 0

        if current_distance < self.predict_attack_distance():
            danger += 2
        
        if self.is_aggressive_player():
            danger += 3
        
        form_diff = enemy.cap_form_actual - bot.cap_form_actual
        if form_diff > 0:
            danger += min(form_diff, 2)
        
        hp_diff = enemy.hp - bot.hp
        if hp_diff > 20:
            danger += 1
        
        if enemy.acciones.get("disparando"):
            danger += 1
        
        return min(danger, 10)
    
    def update_behavior_score(self):
        now = time.time()
        
        if now - self._last_analysis < 2:
            return
        
        self._last_analysis = now
        recent_time = now - 10
        
        attack_count = sum(1 for p in self._attack_patterns if p['time'] > recent_time)
        charge_count = sum(1 for p in self._charge_patterns if p['time'] > recent_time)
        
        if attack_count > 5:
            self._behavior_score['aggressive'] += 1
        elif charge_count > 3:
            self._behavior_score['defensive'] += 1
        else:
            self._behavior_score['balanced'] += 1
    
    def get_dominant_behavior(self):
        return max(self._behavior_score, key=self._behavior_score.get)
    
    def should_counter_attack(self, current_distance):
        if len(self._attack_patterns) < 3:
            return False
        
        last_attack = self._attack_patterns[-1]
        time_since = time.time() - last_attack['time']
        
        return time_since < 0.5 and current_distance < 60
    
    def reset(self):
        self._attack_patterns.clear()
        self._movement_patterns.clear()
        self._transform_patterns.clear()
        self._charge_patterns.clear()
        self._behavior_score = {'aggressive': 0, 'defensive': 0, 'balanced': 0}
        self._cache_time = 0