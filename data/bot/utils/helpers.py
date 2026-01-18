import time

class Timer:
    __slots__ = ('_timers',)
    
    def __init__(self):
        self._timers = {}
    
    def set(self, name, cooldown):
        self._timers[name] = time.time() + cooldown
    
    def ready(self, name):
        if name not in self._timers:
            return True
        return time.time() >= self._timers[name]
    
    def reset(self, name):
        if name in self._timers:
            del self._timers[name]
    
    def get_remaining(self, name):
        if name not in self._timers:
            return 0
        remaining = self._timers[name] - time.time()
        return max(0, remaining)

def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def distance_x(x1, x2):
    return abs(x2 - x1)

def distance_y(y1, y2):
    return abs(y2 - y1)

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))