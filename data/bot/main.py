"""
DBXW - AI Combat Bot v2.0.0
Punto de entrada principal del bot
Autor: elJulioQlo
"""

import threading, time, keyboard
from config import Config
from core.game_reader import GameReader
from core.input_manager import InputManager
from core.state_manager import StateManager
from ai.combat import CombatAI
from ai.movement import MovementAI
from ai.defense import DefenseAI
from abilities.transformation import TransformationManager
from abilities.energy import EnergyManager
from abilities.special_moves import SpecialMovesManager
from utils.logger import Logger

class DBXWBot:
    """Clase principal del bot que coordina todos los sistemas"""
    
    def __init__(self):
        self.logger = Logger()
        self.config = Config()
        self.game_reader = GameReader()
        self.input_manager = InputManager()
        self.state_manager = StateManager()
        
        # Sistemas de IA
        self.combat_ai = CombatAI(self.input_manager, self.state_manager)
        self.movement_ai = MovementAI(self.input_manager, self.state_manager)
        self.defense_ai = DefenseAI(self.input_manager, self.state_manager)
        
        # Gestores de habilidades
        self.transformation_mgr = TransformationManager(self.input_manager)
        self.energy_mgr = EnergyManager(self.input_manager)
        self.special_moves_mgr = SpecialMovesManager(self.input_manager)
        
        self.running = False
        self.last_tick = 0
        
        self.logger.info("🤖 Bot inicializado correctamente")
    
    def update(self):
        """Actualización principal del bot (llamada cada tick)"""
        # Leer datos del juego
        game_data = self.game_reader.read()
        if not game_data:
            return
        
        # Actualizar estado
        self.state_manager.update(game_data, self.config.JUGADOR_CONTROLADO)
        
        # Obtener estado actual
        bot_state = self.state_manager.bot
        enemy_state = self.state_manager.enemy
        
        # PRIORIDAD 1: Esquiva inteligente
        if self.defense_ai.intelligent_dodge(bot_state, enemy_state):
            return  # Si esquivó, skip otras acciones
        
        # PRIORIDAD 2: Ataque preciso
        self.combat_ai.precise_attack(bot_state, enemy_state)
        
        # PRIORIDAD 3: Movimiento estratégico
        self.movement_ai.strategic_movement(bot_state, enemy_state)
        
        # PRIORIDAD 4: Defensa adaptativa
        self.defense_ai.adaptive_strategy(bot_state, enemy_state)
        
        # PRIORIDAD 5: Salto táctico
        self.movement_ai.jump_logic(bot_state, enemy_state)
        
        # PRIORIDAD 6: Gestión de energía
        self.energy_mgr.charge_logic(bot_state, enemy_state)
        self.energy_mgr.ki_shot_logic(bot_state, enemy_state)
        
        # PRIORIDAD 7: Habilidades especiales
        self.transformation_mgr.transform_logic(bot_state, enemy_state)
        self.special_moves_mgr.tackle_logic(bot_state, enemy_state)
        self.special_moves_mgr.timejump_logic(bot_state, enemy_state)
        self.special_moves_mgr.kaioken_logic(bot_state, enemy_state)
        
        # PRIORIDAD 8: Clash management
        self.special_moves_mgr.handle_clash_tackle(bot_state)
    
    def loop(self):
        """Loop principal del bot"""
        self.logger.info("🎮 Bot iniciado - Presiona ESC para detener")
        pause_key = self.input_manager.get_pause_key()
        
        while self.running:
            now = time.time()
            
            # Control de tick rate
            if now - self.last_tick < self.config.TICK_RATE:
                time.sleep(0.005)
                continue
            
            self.last_tick = now
            
            # Actualizar bot
            try:
                self.update()
            except Exception as e:
                self.logger.error(f"Error en update: {e}")
            
            # Verificar tecla de salida
            try:
                if keyboard.is_pressed("esc") or keyboard.is_pressed(pause_key):
                    self.logger.info("⏹️ Deteniendo bot...")
                    self.stop()
                    break
            except:
                pass
            
            time.sleep(0.02)
    
    def start(self):
        """Inicia el bot en un hilo separado"""
        self.running = True
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()
        
    def stop(self):
        """Detiene el bot"""
        self.running = False
        self.input_manager.release_all_keys()
        self.logger.info("✅ Bot detenido correctamente")


def mostrar_banner():
    """Muestra el banner de inicio"""
    print("""
╔══════════════════════════════════════════════════════════╗
║               UW - AI Combat Bot v2.0.0                  ║
╠══════════════════════════════════════════════════════════╣
║ Proyect: Ultimate Warriors                               ║
║ Autor: elJulioDev                                        ║
║                                                          ║
║ - New modular and scalable architecture                  ║
║ - Improved performance and maintainability               ║
║ - Integrated logging system                              ║
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
    
    # Mantener el programa vivo
    try:
        while bot.running:
            time.sleep(1)
    except KeyboardInterrupt:
        bot.stop()


if __name__ == "__main__":
    iniciar_bot()