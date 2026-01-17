
"""
Funciones auxiliares útiles
"""

import time

class Timer:
    """Clase para manejar cooldowns de forma elegante"""
    
    def __init__(self):
        self._timers = {}
    
    def set(self, name, cooldown):
        """Establece un timer"""
        self._timers[name] = time.time() + cooldown
    
    def ready(self, name):
        """Verifica si un timer está listo"""
        if name not in self._timers:
            return True
        return time.time() >= self._timers[name]
    
    def reset(self, name):
        """Resetea un timer"""
        if name in self._timers:
            del self._timers[name]
    
    def get_remaining(self, name):
        """Obtiene el tiempo restante de un timer"""
        if name not in self._timers:
            return 0
        remaining = self._timers[name] - time.time()
        return max(0, remaining)


def distance(x1, y1, x2, y2):
    """Calcula la distancia euclidiana entre dos puntos"""
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def distance_x(x1, x2):
    """Calcula la distancia en X"""
    return abs(x2 - x1)


def distance_y(y1, y2):
    """Calcula la distancia en Y"""
    return abs(y2 - y1)


def clamp(value, min_value, max_value):
    """Limita un valor entre un mínimo y un máximo"""
    return max(min_value, min(value, max_value))