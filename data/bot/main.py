import threading, time, keyboard, os
from config import Config
from core.game_reader import GameReader
from core.input_manager import InputManager
from core.state_manager import StateManager
from ai.combat import CombatAI
from ai.movement import MovementAI
from ai.defense import DefenseAI
from ai.pattern_analyzer import PatternAnalyzer
from ai.prediction import PredictionEngine
from abilities.transformation import TransformationManager
from abilities.energy import EnergyManager
from abilities.special_moves import SpecialMovesManager
from abilities.teleport import TeleportManager
from abilities.combo_breaker import ComboBreaker

class DBXWBot:
    __slots__ = ('_config', '_game_reader', '_input', '_state', 
                 '_combat', '_movement', '_defense', '_transform', 
                 '_energy', '_special', '_teleport', '_pattern', '_prediction',
                 '_combo_breaker', '_running', '_last_tick', '_thread',
                 '_update_counter', '_pattern_update_interval', '_pause_key_pressed')
    
    def __init__(self):
        self._config = Config()
        self._game_reader = GameReader()
        self._input = InputManager()
        self._state = StateManager(self._config.JUGADOR_CONTROLADO)
        
        self._pattern = PatternAnalyzer()
        self._prediction = PredictionEngine()
        self._teleport = TeleportManager(self._input)
        self._combo_breaker = ComboBreaker(self._input, self._teleport)
        
        self._combat = CombatAI(self._input)
        self._movement = MovementAI(self._input)
        
        self._defense = DefenseAI(self._input, self._pattern, self._prediction, 
                                   self._teleport, self._combo_breaker)
        
        self._transform = TransformationManager(self._input)
        self._energy = EnergyManager(self._input)
        self._special = SpecialMovesManager(self._input)
        
        self._running = False
        self._last_tick = 0
        self._thread = None
        
        self._update_counter = 0
        self._pattern_update_interval = 5
        self._pause_key_pressed = False
    
    def update(self):
        game_data = self._game_reader.read()
        if not game_data:
            return
        
        self._state.update(game_data)
        bot = self._state.bot
        enemy = self._state.enemy

        self._prediction.update(enemy.x, enemy.y)
        self._update_counter += 1
        if self._update_counter >= self._pattern_update_interval:
            self._pattern.analyze_attack_pattern(bot, enemy)
            self._update_counter = 0

        if self._defense.intelligent_dodge(bot, enemy):
            return 

        self._combat.precise_attack(bot, enemy)
        
        is_attacking = self._combat.is_attacking()

        self._movement.strategic_movement(bot, enemy, is_attacking)

        self._defense.adaptive_strategy(bot, enemy, is_attacking)
        
        self._movement.jump_logic(bot, enemy)
        
        is_being_comboed = self._defense.is_being_comboed()
        self._energy.charge_logic(bot, enemy, is_being_comboed)
        self._energy.ki_shot_logic(bot, enemy, is_being_comboed=is_being_comboed)
        if not self._transform.is_busy():
            self._transform.transform_logic(bot, enemy, is_attacking)
        self._special.tackle_logic(bot, enemy)
        self._special.timejump_logic(bot, enemy)
        self._special.kaioken_logic(bot, enemy)
        
        self._special.handle_clash_tackle(bot)

    def loop(self):
        pause_key = self._input.get_pause_key()
        sleep_time = self._config.TICK_RATE
        
        stop_keys = {'esc', pause_key}
        
        while self._running:
            frame_start = time.perf_counter()
            
            try:
                self.update()
            except Exception as e:
                print(f"Error en loop: {e}")
            
            try:
                for key in stop_keys:
                    if keyboard.is_pressed(key):
                        if not self._pause_key_pressed:
                            self._pause_key_pressed = True
                            self.stop()
                            return
                    else:
                        self._pause_key_pressed = False
            except:
                pass
            
            elapsed = time.perf_counter() - frame_start
            remaining = sleep_time - elapsed
            
            if remaining > 0:
                time.sleep(remaining * 0.9)
                
                while time.perf_counter() - frame_start < sleep_time:
                    pass
    
    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self.loop, daemon=True)
        self._thread.start()
        
    def stop(self):
        self._running = False
        self._input.release_all_keys()
        self._game_reader.close()

def iniciar_bot():
    bot = DBXWBot()
    
    try:
        import sys
        if sys.platform == 'win32':
            import psutil
            p = psutil.Process(os.getpid())
            p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    except:
        pass
    
    bot.start()
    
    signal_file = "stop.signal"
    check_interval = 0.5
    
    try:
        while bot._running:
            if os.path.exists(signal_file):
                os.remove(signal_file)
                bot.stop()
                break
            time.sleep(check_interval)
    except KeyboardInterrupt:
        bot.stop()
    finally:
        bot.stop()

if __name__ == "__main__":
    iniciar_bot()