import time
from config import Config

class PredictionEngine:
    __slots__ = ('_position_history', '_velocity_history', '_last_prediction',
                 '_teleport_detected', '_last_teleport_check')
    
    def __init__(self):
        self._position_history = []
        self._velocity_history = []
        self._last_prediction = (0, 0)
        self._teleport_detected = False
        self._last_teleport_check = 0
    
    def update(self, enemy_x, enemy_y):
        ahora = time.time()
        self._add_position(enemy_x, enemy_y, ahora)
        self._detect_teleport()
    
    def predict_position(self, current_x, current_y, time_ahead=None):
        if time_ahead is None:
            time_ahead = Config.PREDICT_TIME
        
        ahora = time.time()
        self._add_position(current_x, current_y, ahora)
        
        vx, vy = self._estimate_velocity()
        
        x_pred = current_x + vx * time_ahead
        y_pred = current_y + vy * time_ahead
        
        dx = x_pred - current_x
        dy = y_pred - current_y
        
        max_move = Config.MAX_PRED_MOVE
        
        if abs(dx) > max_move:
            x_pred = current_x + (max_move if dx > 0 else -max_move)
        
        if abs(dy) > max_move:
            y_pred = current_y + (max_move if dy > 0 else -max_move)
        
        self._last_prediction = (x_pred, y_pred)
        return x_pred, y_pred
    
    def predict_attack_point(self, bot_x, bot_y, enemy_x, enemy_y):
        vx, vy = self._estimate_velocity()
        
        speed_magnitude = (vx**2 + vy**2)**0.5
        
        if speed_magnitude < 10:
            return enemy_x, enemy_y
        
        intercept_time = self._calculate_intercept_time(
            bot_x, bot_y, enemy_x, enemy_y, vx, vy
        )
        
        if intercept_time is None:
            return enemy_x, enemy_y
        
        pred_x = enemy_x + vx * intercept_time
        pred_y = enemy_y + vy * intercept_time
        
        return pred_x, pred_y
    
    def get_velocity(self):
        return self._estimate_velocity()
    
    def is_moving_towards(self, bot_x, enemy_x):
        if len(self._position_history) < 2:
            return False
        
        vx, _ = self._estimate_velocity()
        
        if enemy_x < bot_x:
            return vx > 0
        else:
            return vx < 0
    
    def is_retreating(self, bot_x, enemy_x):
        return not self.is_moving_towards(bot_x, enemy_x) and self._is_moving()
    
    def predict_landing_position(self, current_x, current_y, current_vy):
        if current_vy >= 0:
            return current_x, current_y
        
        vx, _ = self._estimate_velocity()
        
        fall_time = abs(current_vy) / 500
        
        landing_x = current_x + vx * fall_time
        
        return landing_x, current_y
    
    def _add_position(self, x, y, t):
        self._position_history.append({'t': t, 'x': x, 'y': y})
        
        if len(self._position_history) > Config.MAX_HISTORY:
            self._position_history.pop(0)
    
    def _estimate_velocity(self):
        if len(self._position_history) < 2:
            return 0.0, 0.0
        
        vx_list = []
        vy_list = []
        
        for i in range(1, len(self._position_history)):
            p0 = self._position_history[i-1]
            p1 = self._position_history[i]
            dt = p1['t'] - p0['t']
            
            if dt <= 0:
                continue
            
            vx = (p1['x'] - p0['x']) / dt
            vy = (p1['y'] - p0['y']) / dt
            
            if abs(vx) < Config.MAX_VEL and abs(vy) < Config.MAX_VEL:
                vx_list.append(vx)
                vy_list.append(vy)
        
        if not vx_list:
            return 0.0, 0.0
        
        vx_avg = sum(vx_list) / len(vx_list)
        vy_avg = sum(vy_list) / len(vy_list)
        
        vx_ema = vx_list[0]
        vy_ema = vy_list[0]
        alpha = Config.VEL_EMA_ALPHA
        
        for i in range(1, len(vx_list)):
            vx_ema = alpha * vx_list[i] + (1 - alpha) * vx_ema
            vy_ema = alpha * vy_list[i] + (1 - alpha) * vy_ema
        
        vx = 0.5 * vx_avg + 0.5 * vx_ema
        vy = 0.5 * vy_avg + 0.5 * vy_ema
        
        return vx, vy
    
    def _detect_teleport(self):
        if len(self._position_history) < 2:
            return
        
        p1 = self._position_history[-2]
        p2 = self._position_history[-1]
        
        dx = abs(p2['x'] - p1['x'])
        dt = p2['t'] - p1['t']
        
        if dt > 0:
            speed = dx / dt
            if speed > Config.MAX_VEL * 0.8:
                self._teleport_detected = True
                self._last_teleport_check = time.time()
    
    def _calculate_intercept_time(self, bot_x, bot_y, enemy_x, enemy_y, vx, vy):
        dx = enemy_x - bot_x
        dy = enemy_y - bot_y
        
        relative_speed = (vx**2 + vy**2)**0.5
        
        if relative_speed < 1:
            return None
        
        distance = (dx**2 + dy**2)**0.5
        
        intercept_time = distance / (relative_speed * 2)
        
        if intercept_time > 2.0:
            return None
        
        return intercept_time
    
    def _is_moving(self):
        vx, vy = self._estimate_velocity()
        return abs(vx) > 5 or abs(vy) > 5
    
    def was_teleport_detected(self):
        if self._teleport_detected:
            if time.time() - self._last_teleport_check > 0.3:
                self._teleport_detected = False
            return True
        return False
    
    def reset(self):
        self._position_history.clear()
        self._velocity_history.clear()
        self._last_prediction = (0, 0)
        self._teleport_detected = False