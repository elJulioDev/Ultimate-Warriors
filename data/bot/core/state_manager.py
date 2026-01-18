class PlayerState:
    __slots__ = ('x', 'y', 'hit_x', 'hit_y', 'hitbox_x', 'hitbox_y', 
                 'hp', 'carga', 'ki', 'damaged', 'defence', 'speed',
                 'colision', 'cubriendose', 'transformado', 'estado_critico',
                 'fase_actual', 'cap_form_actual', 'cantidad_transformaciones',
                 'maxima_transformacion', 'forma_cheat', 'puede_transformarse',
                 'puede_kaioken', 'puede_timejump', 'puede_teletransportarse',
                 'clash_tackle', 'acciones')
    
    def __init__(self, data):
        self.update(data)

    def update(self, data):
        self.x = data.get("x", 0)
        self.y = data.get("y", 0)
        
        hit = data.get("hit", {})
        self.hit_x = hit.get("x", 0)
        self.hit_y = hit.get("y", 0)
        
        hitbox = data.get("hitbox", {})
        self.hitbox_x = hitbox.get("x", 0)
        self.hitbox_y = hitbox.get("y", 0)
        
        self.hp = data.get("hp", 100)
        self.carga = data.get("carga", 0)
        self.ki = data.get("ki", 0)
        self.damaged = data.get("damaged", 0)
        self.defence = data.get("defence", 0)
        self.speed = data.get("speed", 0)
        
        self.colision = data.get("colision", False)
        self.cubriendose = data.get("cubriendose", False)
        self.transformado = data.get("transformado", False)
        self.estado_critico = data.get("estado critico", False)
        
        self.fase_actual = str(data.get("fase actual", "base")).lower()
        self.cap_form_actual = data.get("cap form actual", 0)
        self.cantidad_transformaciones = data.get("cantidad de transformaciones", 0)
        self.maxima_transformacion = data.get("Maxima transformacion", 0)
        self.forma_cheat = str(data.get("Forma Cheat", "")).lower()
        
        self.puede_transformarse = data.get("puede transformarse", False)
        self.puede_kaioken = data.get("puede usar kaioken", "")
        self.puede_timejump = data.get("puede usar timejump", False)
        self.puede_teletransportarse = data.get("puede teletransportarse", False)
        self.clash_tackle = data.get("ClashTackle", False)
        
        self.acciones = data.get("acciones", {})
        if not self.acciones:
            self.acciones = {
                "golpe": False, "patada": False, 
                "cargando": False, "disparando": False, 
                "cubrirse": False
            }


class StateManager:
    __slots__ = ('bot', 'enemy', '_player_controlled')
    
    def __init__(self, player_controlled):
        self._player_controlled = player_controlled
        self.bot = None
        self.enemy = None
        
    def update(self, game_data):
        if not game_data:
            return

        if self._player_controlled == "Player 2":
            bot_data = game_data.get("jugador2", {})
            enemy_data = game_data.get("jugador1", {})
        else:
            bot_data = game_data.get("jugador1", {})
            enemy_data = game_data.get("jugador2", {})
            
        if self.bot is None:
            self.bot = PlayerState(bot_data)
        else:
            self.bot.update(bot_data)
            
        if self.enemy is None:
            self.enemy = PlayerState(enemy_data)
        else:
            self.enemy.update(enemy_data)