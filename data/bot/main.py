import threading, time, keyboard, random
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
from strategies.adaptive import AdaptiveStrategy
from strategies.aggressive import AggressiveStrategy
from strategies.defensive import DefensiveStrategy


class DBXWBot:
    __slots__ = ('_config', '_game_reader', '_input', '_state', 
                 '_combat', '_movement', '_defense', '_transform', 
                 '_energy', '_special', '_teleport', '_pattern', '_prediction',
                 '_adaptive', '_aggressive', '_defensive_strat',
                 '_running', '_last_tick', '_thread', '_enemy_prev_x')
    
    def __init__(self):
        self._config = Config()
        self._game_reader = GameReader()
        self._input = InputManager()
        self._state = StateManager(self._config.JUGADOR_CONTROLADO)
        
        self._pattern = PatternAnalyzer()
        self._prediction = PredictionEngine()
        self._teleport = TeleportManager(self._input)
        
        self._combat = CombatAI(self._input)
        self._movement = MovementAI(self._input)
        self._defense = DefenseAI(self._input, self._pattern, self._prediction, self._teleport)
        
        self._transform = TransformationManager(self._input)
        self._energy = EnergyManager(self._input)
        self._special = SpecialMovesManager(self._input)
        
        self._adaptive = AdaptiveStrategy(self._pattern, self._prediction, self._teleport)
        self._aggressive = AggressiveStrategy(self._input, self._prediction, self._teleport)
        self._defensive_strat = DefensiveStrategy(self._input, self._pattern, self._teleport)
        
        self._running = False
        self._last_tick = 0
        self._thread = None
        self._enemy_prev_x = None
    
    def update(self):
        game_data = self._game_reader.read()
        if not game_data:
            return
        
        self._state.update(game_data)
        
        bot = self._state.bot
        enemy = self._state.enemy
        
        self._pattern.analyze_movement_pattern(enemy, self._enemy_prev_x)
        self._pattern.analyze_transformation(enemy)
        self._pattern.analyze_charge_behavior(enemy)
        self._pattern.update_behavior_score()
        
        self._enemy_prev_x = enemy.x
        
        strategy_mode = self._adaptive.decide_strategy(bot, enemy)
        
        if self._defense.intelligent_dodge(bot, enemy):
            return
        
        if strategy_mode == 'aggressive':
            self._execute_aggressive_mode(bot, enemy)
        elif strategy_mode == 'defensive':
            self._execute_defensive_mode(bot, enemy)
        else:
            self._execute_balanced_mode(bot, enemy)
        
        self._special.handle_clash_tackle(bot)
    
    def _execute_aggressive_mode(self, bot, enemy):
        is_attacking = self._combat.is_attacking()
        
        if self._adaptive.should_attack(bot, enemy, abs(bot.x - enemy.x)):
            self._combat.precise_attack(bot, enemy)
        
        self._movement.strategic_movement(bot, enemy, is_attacking)
        
        if self._adaptive.should_use_ki_shot(bot, enemy, abs(bot.x - enemy.x)):
            self._energy.ki_shot_logic(bot, enemy)
        
        if random.random() < 0.1:
            self._aggressive.attempt_combo(bot, enemy)
        
        self._movement.jump_logic(bot, enemy)
        
        if self._adaptive.should_transform(bot, enemy):
            self._transform.transform_logic(bot, enemy, is_attacking)
        
        if self._adaptive.should_charge_energy(bot, enemy, abs(bot.x - enemy.x)):
            self._energy.charge_logic(bot, enemy)
        
        self._special.tackle_logic(bot, enemy)
        self._special.timejump_logic(bot, enemy)
        self._special.kaioken_logic(bot, enemy)
    
    def _execute_defensive_mode(self, bot, enemy):
        is_attacking = self._combat.is_attacking()
        
        self._defense.adaptive_strategy(bot, enemy, is_attacking)
        
        if self._defensive_strat.should_heal_opportunity(bot, enemy):
            self._defensive_strat.execute_heal(bot)
        
        if self._defensive_strat.can_counter_safely(bot, enemy, abs(bot.x - enemy.x)):
            self._defensive_strat.counter_attack(bot, enemy)
        
        self._defensive_strat.adaptive_defense(bot, enemy)
        
        self._movement.strategic_movement(bot, enemy, is_attacking)
        self._movement.jump_logic(bot, enemy)
        
        if self._adaptive.should_charge_energy(bot, enemy, abs(bot.x - enemy.x)):
            self._energy.charge_logic(bot, enemy)
        
        if self._adaptive.should_transform(bot, enemy):
            self._transform.transform_logic(bot, enemy, is_attacking)
        
        if random.random() < 0.05:
            self._defensive_strat.bait_and_punish(bot, enemy)
    
    def _execute_balanced_mode(self, bot, enemy):
        is_attacking = self._combat.is_attacking()
        
        self._combat.precise_attack(bot, enemy)
        
        self._movement.strategic_movement(bot, enemy, is_attacking)
        
        self._defense.adaptive_strategy(bot, enemy, is_attacking)
        
        self._movement.jump_logic(bot, enemy)
        
        self._energy.charge_logic(bot, enemy)
        self._energy.ki_shot_logic(bot, enemy)
        
        self._transform.transform_logic(bot, enemy, is_attacking)
        self._special.tackle_logic(bot, enemy)
        self._special.timejump_logic(bot, enemy)
        self._special.kaioken_logic(bot, enemy)
    
    def loop(self):
        print("Bot iniciado - Presiona ESC para detener")
        print(f"Modo inicial: {self._adaptive.get_current_mode()}")
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
                print(f"Error en update: {e}")
            
            try:
                if keyboard.is_pressed("esc") or keyboard.is_pressed(pause_key):
                    print("Deteniendo bot...")
                    self.stop()
                    break
            except:
                pass
            
            time.sleep(0.02)
    
    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self.loop, daemon=True)
        self._thread.start()
        
    def stop(self):
        self._running = False
        self._input.release_all_keys()
        print("Bot detenido")


def mostrar_banner():
    print("""
╔══════════════════════════════════════════════════════════╗
║               UW - AI Combat Bot v2.1.0                  ║
╠══════════════════════════════════════════════════════════╣
║ Proyect: Ultimate Warriors                               ║
║ Autor: elJulioDev                                        ║
║                                                          ║
║ - Advanced Pattern Recognition System                    ║
║ - Predictive Movement Analysis                           ║
║ - Adaptive Strategy Selection                            ║
║ - Enhanced Combat Intelligence                           ║
║                                                          ║
║  Press ESC or ENTER to stop the bot                      ║
║                                                          ║
║ © 2026 elJulioDev | Exclusive use for UW                 ║
╚══════════════════════════════════════════════════════════╝
""")


def iniciar_bot():
    mostrar_banner()
    
    bot = DBXWBot()
    bot.start()
    
    try:
        while bot._running:
            time.sleep(1)
    except KeyboardInterrupt:
        bot.stop()


if __name__ == "__main__":
    iniciar_bot()