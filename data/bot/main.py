import threading, time, keyboard
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
                 '_combo_breaker', '_running', '_last_tick', '_thread')
    
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
    
    def update(self):
        game_data = self._game_reader.read()
        if not game_data:
            return
        
        self._state.update(game_data)
        bot = self._state.bot
        enemy = self._state.enemy

        self._prediction.update(enemy.x, enemy.y)
        self._pattern.analyze_attack_pattern(bot, enemy)

        if self._defense.intelligent_dodge(bot, enemy):
            return 

        self._combat.precise_attack(bot, enemy)
        
        is_attacking = self._combat.is_attacking()

        self._movement.strategic_movement(bot, enemy, is_attacking)

        self._defense.adaptive_strategy(bot, enemy, is_attacking)
        
        self._movement.jump_logic(bot, enemy)
        
        self._energy.charge_logic(bot, enemy, is_being_comboed=False)
        self._energy.ki_shot_logic(bot, enemy)
        
        self._transform.transform_logic(bot, enemy, is_attacking)
        self._special.tackle_logic(bot, enemy)
        self._special.timejump_logic(bot, enemy)
        self._special.kaioken_logic(bot, enemy)
        
        self._special.handle_clash_tackle(bot)

    def loop(self):
        print("Bot iniciado v2.0 (Lógica Original) - Presiona ESC para detener")
        pause_key = self._input.get_pause_key()
        
        while self._running:
            now = time.time()
            
            if now - self._last_tick < self._config.TICK_RATE:
                time.sleep(0.005)
                continue
            
            self._last_tick = now
            
            try:
                self.update()
            except Exception as e:
                print(f"Error en loop: {e}")
            
            try:
                if keyboard.is_pressed("esc") or keyboard.is_pressed(pause_key):
                    print("Deteniendo bot...")
                    self.stop()
                    break
            except:
                pass
            
            time.sleep(0.001)
    
    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self.loop, daemon=True)
        self._thread.start()
        
    def stop(self):
        self._running = False
        self._input.release_all_keys()
        print("Bot detenido")

def iniciar_bot():
    bot = DBXWBot()
    bot.start()
    
    try:
        while bot._running:
            time.sleep(1)
    except KeyboardInterrupt:
        bot.stop()

if __name__ == "__main__":
    iniciar_bot()