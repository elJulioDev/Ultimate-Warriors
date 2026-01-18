import time
from config import Config


class AdaptiveStrategy:
    __slots__ = ('_pattern_analyzer', '_prediction', '_teleport', '_last_switch',
                 '_current_mode', '_performance_score', '_decision_history')
    
    def __init__(self, pattern_analyzer, prediction_engine, teleport_manager):
        self._pattern_analyzer = pattern_analyzer
        self._prediction = prediction_engine
        self._teleport = teleport_manager
        self._last_switch = 0
        self._current_mode = 'balanced'
        self._performance_score = {
            'aggressive': 0,
            'defensive': 0,
            'balanced': 0
        }
        self._decision_history = []
    
    def decide_strategy(self, bot, enemy):
        ahora = time.time()
        
        if ahora - self._last_switch < 3:
            return self._current_mode
        
        danger_level = self._pattern_analyzer.calculate_danger_level(bot, enemy, abs(bot.x - enemy.x))
        hp_ratio = bot.hp / max(enemy.hp, 1)
        form_diff = enemy.cap_form_actual - bot.cap_form_actual
        
        if bot.hp < 25:
            new_mode = 'defensive'
        elif hp_ratio > 1.3 and bot.carga > 150:
            new_mode = 'aggressive'
        elif danger_level > 6:
            new_mode = 'defensive'
        elif form_diff > 1:
            new_mode = 'balanced'
        else:
            enemy_behavior = self._pattern_analyzer.get_dominant_behavior()
            
            if enemy_behavior == 'aggressive':
                new_mode = 'defensive'
            elif enemy_behavior == 'defensive':
                new_mode = 'aggressive'
            else:
                new_mode = 'balanced'
        
        if new_mode != self._current_mode:
            self._current_mode = new_mode
            self._last_switch = ahora
            self._record_decision(new_mode, danger_level, hp_ratio)
        
        return self._current_mode
    
    def should_attack(self, bot, enemy, current_distance):
        mode = self._current_mode
        
        if mode == 'aggressive':
            return current_distance < 60 and not enemy.cubriendose
        elif mode == 'defensive':
            return current_distance < 40 and self._pattern_analyzer.should_counter_attack(current_distance)
        else:
            return current_distance < 50 and not enemy.acciones.get("golpe")
    
    def should_defend(self, bot, enemy, current_distance):
        mode = self._current_mode
        danger = self._pattern_analyzer.calculate_danger_level(bot, enemy, current_distance)
        
        if mode == 'defensive':
            return danger > 3 or current_distance < 70
        elif mode == 'aggressive':
            return danger > 7 or bot.hp < 30
        else:
            return danger > 5
    
    def should_charge_energy(self, bot, enemy, current_distance):
        mode = self._current_mode
        
        if bot.carga >= Config.MAX_CARGA * 0.9:
            return False
        
        if mode == 'aggressive':
            return bot.carga < 100 and current_distance > 150
        elif mode == 'defensive':
            return bot.carga < 180 and current_distance > 120
        else:
            return bot.carga < 140 and current_distance > 130
    
    def should_use_ki_shot(self, bot, enemy, current_distance):
        mode = self._current_mode
        
        if bot.carga < Config.KI_SHOT_ENERGY_REQUIRED:
            return False
        
        if mode == 'aggressive':
            return current_distance > 60 or enemy.cubriendose
        elif mode == 'defensive':
            return current_distance > 100
        else:
            return current_distance > 80 and bot.carga > 80
    
    def should_transform(self, bot, enemy):
        if not bot.puede_transformarse:
            return False
        
        mode = self._current_mode
        form_diff = enemy.cap_form_actual - bot.cap_form_actual
        
        if mode == 'aggressive':
            return form_diff >= 0 and bot.carga > 140
        elif mode == 'defensive':
            return form_diff > 1 or bot.hp < 40
        else:
            return form_diff > 0 and bot.carga > 160
    
    def should_use_teleport(self, bot, enemy, current_distance):
        if not self._teleport.can_teleport(bot):
            return False
        
        mode = self._current_mode
        danger = self._pattern_analyzer.calculate_danger_level(bot, enemy, current_distance)
        
        if mode == 'defensive':
            return danger > 5 and current_distance < 60
        elif mode == 'aggressive':
            pred_x, _ = self._prediction.predict_position(enemy.x, enemy.y, 0.2)
            return abs(pred_x - bot.x) > current_distance and current_distance < 100
        else:
            return danger > 7
    
    def get_optimal_distance(self):
        mode = self._current_mode
        
        if mode == 'aggressive':
            return 45
        elif mode == 'defensive':
            return 100
        else:
            return 70
    
    def adapt_to_performance(self, hit_success_rate):
        if hit_success_rate > 0.7:
            self._performance_score[self._current_mode] += 2
        elif hit_success_rate < 0.3:
            self._performance_score[self._current_mode] -= 1
        
        worst_mode = min(self._performance_score, key=self._performance_score.get)
        if self._performance_score[worst_mode] < -5:
            self._performance_score[worst_mode] = 0
    
    def _record_decision(self, mode, danger, hp_ratio):
        self._decision_history.append({
            'time': time.time(),
            'mode': mode,
            'danger': danger,
            'hp_ratio': hp_ratio
        })
        
        if len(self._decision_history) > 20:
            self._decision_history.pop(0)
    
    def get_current_mode(self):
        return self._current_mode
    
    def reset(self):
        self._current_mode = 'balanced'
        self._performance_score = {'aggressive': 0, 'defensive': 0, 'balanced': 0}
        self._decision_history.clear()