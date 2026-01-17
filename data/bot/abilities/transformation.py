"""
Sistema de transformaciones del bot
Gestiona todas las transformaciones y sus combinaciones de teclas
"""

import time
from config import Config
from utils.constants import nivel_carga


class TransformationManager:
    """Gestor de transformaciones estratégicas"""
    
    def __init__(self, input_manager):
        self.input_manager = input_manager
        self.last_transform_attempt = 0
        self.last_s_press = 0.0
    
    def transform_logic(self, bot, enemy):
        """
        Decide y ejecuta transformaciones basándose en el contexto del combate
        
        Args:
            bot: Estado del bot (PlayerState)
            enemy: Estado del enemigo (PlayerState)
        """
        # No transformar mientras ataca
        if bot.acciones.get("golpe") or bot.acciones.get("patada"):
            return
        
        ahora = time.time()
        
        # Calcular cooldown dinámico (más largo en transformaciones altas)
        cooldown_base = 2.0
        cooldown_extra = (bot.maxima_transformacion - bot.cap_form_actual) * 1.2
        cooldown_actual = min(12.0, cooldown_base + cooldown_extra)
        
        if ahora - self.last_transform_attempt < cooldown_actual:
            return
        
        # Validaciones básicas
        if not bot.puede_transformarse or bot.cantidad_transformaciones < 1:
            return
        
        if bot.cap_form_actual >= bot.maxima_transformacion:
            return  # Ya está en forma máxima
        
        # Calcular "score" de necesidad de transformación
        score = self._calculate_transformation_score(bot, enemy)
        
        # Umbral dinámico (más difícil transformar en formas altas)
        umbral = 3.5 + (bot.cap_form_actual * 0.5)
        
        if score < umbral:
            return  # No es necesario transformar aún
        
        # Seleccionar tipo de transformación
        tipo_trans = self._select_transformation_type(bot, score)
        
        if tipo_trans:
            self._execute_transformation(tipo_trans)
            self.last_transform_attempt = ahora
    
    def _calculate_transformation_score(self, bot, enemy):
        """
        Calcula un score de 0-10+ que indica cuán urgente es transformarse
        
        Returns:
            float: Score de necesidad de transformación
        """
        score = 0
        
        # Factor 1: Stats del enemigo superiores
        if enemy.damaged > bot.damaged: score += 1
        if enemy.defence > bot.defence: score += 1
        if enemy.speed > bot.speed: score += 1
        
        # Factor 2: HP bajo y enemigo con ventaja
        if bot.hp < 60 and enemy.hp > bot.hp: score += 2
        
        # Factor 3: Enemigo más transformado
        if enemy.cap_form_actual > bot.cap_form_actual: score += 1.5
        
        # Factor 4: Enemigo tiene forma cheat y nosotros no
        if enemy.forma_cheat and not bot.forma_cheat: score += 2
        
        # Factor 5: HP crítico
        if bot.hp < 30: score += 2
        
        # Factor 6: Gran diferencia de HP
        hp_diff = enemy.hp - bot.hp
        if hp_diff > 30: score += 1
        
        return score
    
    def _select_transformation_type(self, bot, score):
        """
        Selecciona el tipo de transformación apropiado
        
        Args:
            bot: Estado del bot
            score: Score de necesidad
            
        Returns:
            str: Tipo de transformación ("secuencial", "fase2", etc.) o None
        """
        nivel = nivel_carga(bot.carga)
        costos = Config.COSTO_TRANSFORMACION
        max_form = bot.maxima_transformacion
        
        # Si solo tiene 1-2 transformaciones, usar secuencial
        if bot.cantidad_transformaciones <= 2:
            if nivel >= costos["secuencial"]:
                return "secuencial"
            return None
        
        # Para personajes con múltiples transformaciones
        # Priorizar transformaciones más altas si el score es alto
        if score >= 6 and nivel >= costos["fase6"] and max_form >= 6:
            return "fase6"
        elif score >= 5 and nivel >= costos["fase5"] and max_form >= 5:
            return "fase5"
        elif score >= 4 and nivel >= costos["fase4"] and max_form >= 4:
            return "fase4"
        elif score >= 3 and nivel >= costos["fase3"] and max_form >= 3:
            return "fase3"
        elif score >= 2 and nivel >= costos["fase2"] and max_form >= 2:
            return "fase2"
        elif nivel >= costos["secuencial"]:
            return "secuencial"
        
        return None
    
    def _execute_transformation(self, tipo):
        """
        Ejecuta la secuencia de teclas para la transformación
        
        Args:
            tipo: Tipo de transformación a ejecutar
        """
        ahora = time.time()
        
        # Verificar cooldown de la tecla S (Cover)
        if ahora - self.last_s_press < Config.S_COOLDOWN:
            return
        
        # SECUENCIA: S (Hold) → Combo de teclas → S (Release)
        self.input_manager.press("cover")
        time.sleep(0.08)  # Esperar registro de cover
        
        # Ejecutar combo según tipo
        if tipo == "secuencial":  # S + J (Punch)
            self.input_manager.press("punch")
            time.sleep(0.25)
            self.input_manager.release("punch")
        
        elif tipo == "fase2":  # S + (A o D) + J
            self.input_manager.press("left")
            time.sleep(0.02)
            self.input_manager.press("punch")
            time.sleep(0.25)
            self.input_manager.release("punch")
            self.input_manager.release("left")
        
        elif tipo == "fase3":  # S + A + D + J
            self.input_manager.press("left")
            time.sleep(0.02)
            self.input_manager.press("right")
            time.sleep(0.02)
            self.input_manager.press("punch")
            time.sleep(0.25)
            self.input_manager.release("punch")
            self.input_manager.release("right")
            self.input_manager.release("left")
        
        elif tipo == "fase4":  # S + K (Kick)
            self.input_manager.press("kick")
            time.sleep(0.25)
            self.input_manager.release("kick")
        
        elif tipo == "fase5":  # S + (A o D) + K
            self.input_manager.press("left")
            time.sleep(0.02)
            self.input_manager.press("kick")
            time.sleep(0.25)
            self.input_manager.release("kick")
            self.input_manager.release("left")
        
        elif tipo == "fase6":  # S + (A o D) + Shot
            self.input_manager.press("left")
            time.sleep(0.02)
            self.input_manager.press("shot")
            time.sleep(0.25)
            self.input_manager.release("shot")
            self.input_manager.release("left")
        
        elif tipo == "cheat":  # S + A + D + Shot
            self.input_manager.press("left")
            time.sleep(0.02)
            self.input_manager.press("right")
            time.sleep(0.02)
            self.input_manager.press("shot")
            time.sleep(0.25)
            self.input_manager.release("shot")
            self.input_manager.release("right")
            self.input_manager.release("left")
        
        # Soltar S al final
        self.input_manager.release("cover")
        self.last_s_press = time.time()
    
    def force_transform(self, tipo):
        """
        Fuerza una transformación específica (para testing)
        
        Args:
            tipo: Tipo de transformación
        """
        self._execute_transformation(tipo)
        self.last_transform_attempt = time.time()