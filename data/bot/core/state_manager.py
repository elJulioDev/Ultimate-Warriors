"""
Maneja el estado del juego y normaliza los datos para la IA
"""
from utils.helpers import distance

class PlayerState:
    """Representación limpia de un jugador"""
    def __init__(self, data):
        self.update(data)

    def update(self, data):
        # Datos posicionales básicos
        self.x = data.get("x", 0)
        self.y = data.get("y", 0)
        
        # Hitbox (lectura anidada segura)
        hit = data.get("hit", {})
        self.hit_x = hit.get("x", 0)
        self.hit_y = hit.get("y", 0)
        
        hitbox = data.get("hitbox", {})
        self.hitbox_x = hitbox.get("x", 0)
        self.hitbox_y = hitbox.get("y", 0)
        
        # Stats
        self.hp = data.get("hp", 100)
        self.carga = data.get("carga", 0)
        self.ki = data.get("ki", 0)
        self.damaged = data.get("damaged", 0)
        self.defence = data.get("defence", 0)
        self.speed = data.get("speed", 0)
        
        # Estados booleanos y flags
        self.colision = data.get("colision", False)
        self.cubriendose = data.get("cubriendose", False)
        self.transformado = data.get("transformado", False)
        self.estado_critico = data.get("estado critico", False)
        
        # Transformaciones y Habilidades
        self.fase_actual = str(data.get("fase actual", "base")).lower()
        self.cap_form_actual = data.get("cap form actual", 0)
        self.cantidad_transformaciones = data.get("cantidad de transformaciones", 0)
        self.maxima_transformacion = data.get("Maxima transformacion", 0)
        self.forma_cheat = str(data.get("Forma Cheat", "")).lower()
        
        # Habilidades especiales
        self.puede_transformarse = data.get("puede transformarse", False)
        self.puede_kaioken = data.get("puede usar kaioken", "") # Puede venir como string o bool
        self.puede_timejump = data.get("puede usar timejump", False)
        self.puede_teletransportarse = data.get("puede teletransportarse", False)
        self.clash_tackle = data.get("ClashTackle", False)
        
        # Acciones actuales (Input del momento)
        self.acciones = data.get("acciones", {})
        # Normalizar claves de acciones para acceso seguro
        if not self.acciones:
            self.acciones = {
                "golpe": False, "patada": False, 
                "cargando": False, "disparando": False, 
                "cubrirse": False
            }

class StateManager:
    """Coordina el estado global del juego"""
    def __init__(self):
        self.bot = None
        self.enemy = None
        
    def update(self, game_data, player_controlled):
        """
        Actualiza el estado basado en el game_data.json
        player_controlled: "Player 1" o "Player 2"
        """
        if not game_data:
            return

        # Determinar quién es quién
        if player_controlled == "Player 2":
            bot_data = game_data.get("jugador2", {})
            enemy_data = game_data.get("jugador1", {})
        else:
            bot_data = game_data.get("jugador1", {})
            enemy_data = game_data.get("jugador2", {})
            
        # Crear o actualizar objetos de estado
        if self.bot is None:
            self.bot = PlayerState(bot_data)
        else:
            self.bot.update(bot_data)
            
        if self.enemy is None:
            self.enemy = PlayerState(enemy_data)
        else:
            self.enemy.update(enemy_data)