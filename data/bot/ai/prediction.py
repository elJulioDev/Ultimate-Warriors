"""
Sistema de predicción de movimiento del oponente
Usa historial de posiciones y velocidad para anticipar movimientos
"""

import time
from config import Config


class PredictionEngine:
    """
    Motor de predicción que estima la posición futura del oponente
    basándose en su historial de movimiento
    """
    
    def __init__(self):
        self.opponent_history = []  # Lista de {'t': timestamp, 'x': x, 'y': y}
        self.last_prediction = (0, 0)
    
    def update(self, enemy_x, enemy_y):
        """
        Actualiza el historial con la posición actual del enemigo
        
        Args:
            enemy_x: Posición X del enemigo
            enemy_y: Posición Y del enemigo
        """
        ahora = time.time()
        self._push_position(enemy_x, enemy_y, ahora)
    
    def predict_position(self, current_x, current_y):
        """
        Predice la posición futura del oponente
        
        Args:
            current_x: Posición X actual
            current_y: Posición Y actual
            
        Returns:
            tuple: (x_pred, y_pred) posición predicha
        """
        ahora = time.time()
        self._push_position(current_x, current_y, ahora)
        
        # Estimar velocidad
        vx, vy = self._estimate_velocity()
        
        # Extrapolar posición futura
        x_pred = current_x + vx * Config.PREDICT_TIME
        y_pred = current_y + vy * Config.PREDICT_TIME
        
        # Limitar predicción a movimiento razonable
        dx = x_pred - current_x
        dy = y_pred - current_y
        
        if abs(dx) > Config.MAX_PRED_MOVE:
            x_pred = current_x + (Config.MAX_PRED_MOVE * (1 if dx > 0 else -1))
        
        if abs(dy) > Config.MAX_PRED_MOVE:
            y_pred = current_y + (Config.MAX_PRED_MOVE * (1 if dy > 0 else -1))
        
        self.last_prediction = (x_pred, y_pred)
        return x_pred, y_pred
    
    def get_velocity(self):
        """
        Obtiene la velocidad estimada actual del oponente
        
        Returns:
            tuple: (vx, vy) velocidad en px/s
        """
        return self._estimate_velocity()
    
    def is_moving_towards(self, bot_x):
        """
        Determina si el oponente se está moviendo hacia el bot
        
        Args:
            bot_x: Posición X del bot
            
        Returns:
            bool: True si se mueve hacia el bot
        """
        if len(self.opponent_history) < 2:
            return False
        
        vx, _ = self._estimate_velocity()
        
        # Obtener última posición conocida
        last_pos = self.opponent_history[-1]
        enemy_x = last_pos['x']
        
        # Si el enemigo está a la izquierda y velocidad es positiva → acercándose
        # Si el enemigo está a la derecha y velocidad es negativa → acercándose
        if enemy_x < bot_x:
            return vx > 0
        else:
            return vx < 0
    
    def _push_position(self, x, y, t):
        """Añade una observación al historial"""
        self.opponent_history.append({'t': t, 'x': x, 'y': y})
        
        # Mantener solo las últimas N observaciones
        if len(self.opponent_history) > Config.MAX_HISTORY:
            self.opponent_history.pop(0)
    
    def _estimate_velocity(self):
        """
        Estima la velocidad usando EMA (Exponential Moving Average)
        
        Returns:
            tuple: (vx, vy) en px/s
        """
        if len(self.opponent_history) < 2:
            return 0.0, 0.0
        
        # Calcular velocidades instantáneas entre pares consecutivos
        vx_list = []
        vy_list = []
        
        for i in range(1, len(self.opponent_history)):
            p0 = self.opponent_history[i-1]
            p1 = self.opponent_history[i]
            dt = p1['t'] - p0['t']
            
            if dt <= 0:
                continue
            
            vx_list.append((p1['x'] - p0['x']) / dt)
            vy_list.append((p1['y'] - p0['y']) / dt)
        
        if not vx_list:
            return 0.0, 0.0
        
        # Promedio simple
        vx_avg = sum(vx_list) / len(vx_list)
        vy_avg = sum(vy_list) / len(vy_list)
        
        # Aplicar EMA para dar más peso a lo reciente
        vx_ema = vx_list[0]
        vy_ema = vy_list[0]
        
        alpha = Config.VEL_EMA_ALPHA
        
        for i in range(1, len(vx_list)):
            vx_ema = alpha * vx_list[i] + (1 - alpha) * vx_ema
            vy_ema = alpha * vy_list[i] + (1 - alpha) * vy_ema
        
        # Combinar promedio y EMA
        vx = 0.5 * vx_avg + 0.5 * vx_ema
        vy = 0.5 * vy_avg + 0.5 * vy_ema
        
        # Clampar a velocidad máxima razonable (filtrar teleports)
        if abs(vx) > Config.MAX_VEL:
            vx = Config.MAX_VEL * (1 if vx > 0 else -1)
        
        if abs(vy) > Config.MAX_VEL:
            vy = Config.MAX_VEL * (1 if vy > 0 else -1)
        
        return vx, vy
    
    def reset(self):
        """Reinicia el historial de predicción"""
        self.opponent_history.clear()
        self.last_prediction = (0, 0)
    
    def get_stats(self):
        """Retorna estadísticas del predictor"""
        return {
            "history_size": len(self.opponent_history),
            "last_prediction": self.last_prediction,
            "current_velocity": self._estimate_velocity()
        }