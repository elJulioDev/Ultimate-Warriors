import os, json, keyboard, threading, random, time

# ---------------------- CONFIGURACIÓN INICIAL -----------v-----------
print("""
╔══════════════════════════════════════════════════════════╗
║               DBXW - AI Combat Bot v1.0.0                ║
╠══════════════════════════════════════════════════════════╣
║ Proyecto: Dragon Ball Xeno Warriors                      ║
║ Autor: elJulioQlo                                        ║
║                                                          ║
║ Este script controla automáticamente a un personaje      ║
║ del juego usando inteligencia artificial basada en       ║
║ reglas y condiciones extraídas del juego.                ║
║                                                          ║
║ Funciones principales:                                   ║
║  - Ataque automático inteligente                         ║
║  - Defensa reactiva y lógica de cobertura                ║
║  - Transformaciones estratégicas                         ║
║  - Evasión mediante teletransporte                       ║
║  - Soporte para clash, ki shots, tackles, etc.           ║
║                                                          ║
║ Requiere:                                                ║
║  - Archivos: game_data.json, controls.json               ║
║  - Configurar correctamente 'JUGADOR_CONTROLADO'         ║
║                                                          ║
║  Presiona ESC o la tecla de pausa para detener el bot    ║
║                                                          ║
║ © 2025 elJulioQlo | Uso exclusivo para DBXW              ║
╚══════════════════════════════════════════════════════════╝
""")

# Carpeta donde están los archivos de datos
DATA_FOLDER = os.path.dirname(__file__)

# Archivos
GAME_DATA_FILE = os.path.join(DATA_FOLDER, "game_data.json")
CONTROLS_FILE = os.path.join(DATA_FOLDER, "controls.json")

# Indica qué jugador será controlado por este script: "Player 1" o "Player 2"
JUGADOR_CONTROLADO = "Player 2"

# Diccionario para almacenar las teclas configuradas dinámicamente
teclas = {}

# ---------------------- CARGA DE CONTROLES ----------------------

def cargar_controles():
    """Carga las teclas desde controls.json y las adapta para uso con keyboard."""
    global teclas

    if not os.path.exists(CONTROLS_FILE):
        #print("❌ No se encontró el archivo controls.json")
        return

    try:
        with open(CONTROLS_FILE, "r", encoding="utf-8") as f:
            controles = json.load(f)["Controls"][JUGADOR_CONTROLADO]
    except Exception as e:
        #print(f"❌ Error al leer controls.json: {e}")
        return

    teclas = {
        "jump": controles["Movement"].get("Jump", "").lower(),
        "left": controles["Movement"].get("Left", "").lower(),
        "right": controles["Movement"].get("Right", "").lower(),
        "cover": controles["Movement"].get("Cover up", "").lower(),
        "punch": controles["Combat"].get("Punch", "").lower(),
        "kick": controles["Combat"].get("Kick", "").lower(),
        "charge": controles["Energy"].get("Charge", "").lower(),
        "shot": controles["Energy"].get("Ki shot", "").lower(),
        "tackle": controles["Energy"].get("Tackle", "").lower(),
        "emote": controles.get("Emote", "").lower()
    }

def obtener_tecla_pausa():
    """Devuelve la tecla configurada para pausar desde controls.json"""
    if not os.path.exists(CONTROLS_FILE):
        return "enter"  # por defecto

    try:
        with open(CONTROLS_FILE, "r", encoding="utf-8") as f:
            datos = json.load(f)
            return datos.get("Controls", {}).get("Others", {}).get("Pause", "ENTER").lower()
    except:
        return "enter"
    
def liberar_todas_las_teclas():
    for tecla in teclas.values():
        keyboard.release(tecla)


# ---------------------- LECTURA DE DATOS ----------------------

def leer_datos_juego():
    """Lee y retorna el contenido actual del archivo game_data.json."""
    if not os.path.exists(GAME_DATA_FILE):
        #print("❌ No se encontró el archivo game_data.json")
        return {}

    try:
        with open(GAME_DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        #print("⚠️ Error de formato JSON en game_data.json")
        return {}
    except Exception as e:
        #print(f"❌ Error al leer game_data.json: {e}")
        return {}

# ---------------------- BASE PARA FUNCIONES DEL BOT ----------------------


# Variables de estado del movimiento
last_move_time = 0
moving_left = False
moving_right = False

# Variables de salto
last_jump_time = 0
jumping = False
JUMP_DIFF = 65  # Diferencia de altura mínima para saltar

attacking = False
attack_start_time = 0
current_attack_key = None
last_attack_type = None  # 'punch' o 'kick'

covering = False
cover_start_time = 0
last_cover_time = 0

COVER_DURATION = 1.5  # segundos máximos cubriéndose
COVER_COOLDOWN = 1.0  # tiempo antes de poder cubrirse otra vez
LOW_HP_THRESHOLD = 35
DEFENSE_RANGE = 80  # distancia máxima para reaccionar a un ataque

last_transform_attempt = 0
TRANSFORM_COOLDOWN = 2.0  # segundos entre intentos

last_teleport_time = 0
TELEPORT_COOLDOWN = 0.3  # segundos
TELEPORT_ENERGY = 30     # mínimo de carga necesaria

charging = False
MAX_CARGA = 282
CHARGE_DISTANCE = 140  # distancia mínima para decidir cargar

last_ki_shot_time = 0
KI_SHOT_COOLDOWN = 0.1  # reducido para mayor frecuencia
KI_SHOT_ENERGY_REQUIRED = 25  # menor energía requerida
KI_SHOT_MIN_DISTANCE = 0  # puede disparar incluso más cerca

last_tackle_time = 0
TACKLE_COOLDOWN = 4.0  # segundos para evitar spam
TACKLE_ENERGY_REQUIRED = 188  # nivel 2
TACKLE_DISTANCE = 90  # se puede usar si está cerca

last_timejump = 0
TIMEJUMP_COOLDOWN = 10  # segundos para no abusar

last_kaioken_time = 0
KAIOKEN_COOLDOWN = 15  # segundos

# Cooldown especial para tecla S (cover)
S_COOLDOWN = 0.25  # segundos (igual que en VBA)
last_s_press = 0.0

last_tick = 0
TICK_RATE = 0.05  # 50ms → 20 ciclos por segundo

# ---------------------- PREDICCIÓN DEL OPONENTE (HISTORIAL + VELOCIDAD) ----------------------

# buffer para historial de hitbox del oponente: lista de dicts {'t': timestamp, 'x':..., 'y':...}
_opponent_history = []
MAX_HISTORY = 16        # cuántos puntos guardar (16 * 0.02 loop ~ suficiente)
PREDICT_TIME = 0.2     # segundos a predecir (tu requisito)
MAX_VEL = 1500         # px/s máximo plausible (para filtrar teleports), ajustar si es necesario
VEL_EMA_ALPHA = 0.4    # suavizado exponencial para la velocidad — 0 = muy suave, 1 = sin suavizado


# Mejora para la predicción con análisis de patrones
class PatternAnalyzer:
    def __init__(self):
        self.attack_history = []  # Historial de ataques del oponente
        self.movement_patterns = []  # Patrones de movimiento
        self.last_positions = []  # Últimas 10 posiciones
        
    def analyze_opponent_behavior(self, datos):
        """Analiza patrones del oponente para predecir acciones"""
        enemigo = datos.get("jugador1", {})
        acciones = enemigo.get("acciones", {})
        
        # Registrar patrón de ataque
        if acciones.get("golpe") or acciones.get("patada"):
            self.attack_history.append({
                'time': time.time(),
                'type': 'punch' if acciones.get("golpe") else 'kick',
                'distance': abs(enemigo.get("x", 0) - datos.get("jugador2", {}).get("x", 0))
            })
            
        # Mantener solo los últimos 20 ataques
        if len(self.attack_history) > 20:
            self.attack_history.pop(0)
            
    def predict_next_attack(self, current_distance):
        """Predice si el oponente va a atacar basándose en patrones"""
        if len(self.attack_history) < 3:
            return False
            
        # Analizar distancias de ataque previas
        recent_attacks = self.attack_history[-5:]
        avg_attack_distance = sum(a['distance'] for a in recent_attacks) / len(recent_attacks)
        
        # Si la distancia actual es similar a la distancia promedio de ataque
        if abs(current_distance - avg_attack_distance) < 30:
            return True
        return False

# Variable global
pattern_analyzer = PatternAnalyzer()

def _push_opponent_hitbox(x, y, t):
    """Añade la observación al historial y lo recorta."""
    global _opponent_history
    _opponent_history.append({'t': t, 'x': x, 'y': y})
    if len(_opponent_history) > MAX_HISTORY:
        _opponent_history.pop(0)

def _estimate_velocity():
    """Estima vx, vy usando diferencias entre puntos y aplica EMA para suavizar.
       Devuelve (vx, vy) en px/s. Si no hay suficiente info devuelve (0,0)."""
    if len(_opponent_history) < 2:
        return 0.0, 0.0

    # calcular velocidades instantáneas entre pares consecutivos
    vx_list = []
    vy_list = []
    for i in range(1, len(_opponent_history)):
        p0 = _opponent_history[i-1]
        p1 = _opponent_history[i]
        dt = p1['t'] - p0['t']
        if dt <= 0:
            continue
        vx_list.append((p1['x'] - p0['x']) / dt)
        vy_list.append((p1['y'] - p0['y']) / dt)

    if not vx_list:
        return 0.0, 0.0

    # promedio simple primero
    vx_avg = sum(vx_list) / len(vx_list)
    vy_avg = sum(vy_list) / len(vy_list)

    # aplicar EMA sobre la lista para darle más peso a lo reciente
    vx_ema = vx_list[0]
    vy_ema = vy_list[0]
    for i in range(1, len(vx_list)):
        vx_ema = VEL_EMA_ALPHA * vx_list[i] + (1 - VEL_EMA_ALPHA) * vx_ema
        vy_ema = VEL_EMA_ALPHA * vy_list[i] + (1 - VEL_EMA_ALPHA) * vy_ema

    # combinación entre promedio y EMA para estabilidad
    vx = 0.5 * vx_avg + 0.5 * vx_ema
    vy = 0.5 * vy_avg + 0.5 * vy_ema

    # clampar velocidad a un máximo razonable para evitar teleports locos
    if abs(vx) > MAX_VEL:
        vx = MAX_VEL * (1 if vx > 0 else -1)
    if abs(vy) > MAX_VEL:
        vy = MAX_VEL * (1 if vy > 0 else -1)

    return vx, vy

def _predict_opponent_position(current_x, current_y):
    """Devuelve (x_pred, y_pred) extrapolando PREDICT_TIME hacia adelante.
       Usa historial actual (si existe)."""
    ahora = time.time()
    # push la observación actual también (mantiene el buffer actualizado)
    _push_opponent_hitbox(current_x, current_y, ahora)

    vx, vy = _estimate_velocity()
    x_pred = current_x + vx * PREDICT_TIME
    y_pred = current_y + vy * PREDICT_TIME

    # seguridad: si predicción se aleja demasiado de la posición actual, limitar el desplazamiento
    MAX_PRED_MOVE = 200  # px máximo que puede moverse en PREDICT_TIME (ajustable)
    dx = x_pred - current_x
    dy = y_pred - current_y
    if abs(dx) > MAX_PRED_MOVE:
        x_pred = current_x + (MAX_PRED_MOVE * (1 if dx > 0 else -1))
    if abs(dy) > MAX_PRED_MOVE:
        y_pred = current_y + (MAX_PRED_MOVE * (1 if dy > 0 else -1))

    return x_pred, y_pred

def intelligent_dodge():
    """Sistema de esquiva predictivo mejorado"""
    global last_teleport_time
    datos = leer_datos_juego()
    if not datos:
        return
    
    if JUGADOR_CONTROLADO == "Player 2":
        bot = datos.get("jugador2", {})
        enemigo = datos.get("jugador1", {})
    else:
        bot = datos.get("jugador1", {})
        enemigo = datos.get("jugador2", {})
    
    hp_bot = bot.get("hp", 100)
    carga = bot.get("carga", 0)
    puede_tp = bot.get("puede teletransportarse", False)
    
    # Analizar comportamiento del enemigo
    pattern_analyzer.analyze_opponent_behavior(datos)
    
    x_bot = bot.get("x", 0)
    x_enemigo = enemigo.get("x", 0)
    distancia = abs(x_bot - x_enemigo)
    
    acciones_enemigo = enemigo.get("acciones", {})
    atacando_enemigo = acciones_enemigo.get("golpe") or acciones_enemigo.get("patada")
    disparando_enemigo = acciones_enemigo.get("disparando")
    
    ahora = time.time()
    
    # ESQUIVA PREDICTIVA: Si detecta que el enemigo va a atacar
    if pattern_analyzer.predict_next_attack(distancia) and distancia < 70:
        if puede_tp and carga >= TELEPORT_ENERGY and ahora - last_teleport_time > TELEPORT_COOLDOWN:
            # Teleport hacia atrás para esquivar
            direccion = teclas["left"] if x_bot > x_enemigo else teclas["right"]
            keyboard.press_and_release(direccion)
            time.sleep(0.05)
            keyboard.press_and_release(direccion)
            last_teleport_time = ahora
            return True
    
    # ESQUIVA REACTIVA: Si ya está siendo atacado
    if atacando_enemigo and distancia < 50:
        if puede_tp and carga >= TELEPORT_ENERGY and ahora - last_teleport_time > 0.2:
            # Teleport de emergencia
            direccion = teclas["left"] if x_bot > x_enemigo else teclas["right"]
            keyboard.press_and_release(direccion)
            time.sleep(0.05)
            keyboard.press_and_release(direccion)
            last_teleport_time = ahora
            return True
            
    # ESQUIVA DE KI SHOTS
    if disparando_enemigo and distancia > 80:
        # Saltar o moverse lateralmente
        if random.random() < 0.6:
            keyboard.press(teclas["jump"])
            time.sleep(0.1)
            keyboard.release(teclas["jump"])
        else:
            # Moverse hacia el oponente (agresivo)
            direccion = teclas["right"] if x_enemigo > x_bot else teclas["left"]
            keyboard.press(direccion)
            time.sleep(0.15)
            keyboard.release(direccion)
    
    return False

def precise_attack_logic():
    """Sistema de ataque con timing preciso y combos"""
    global attacking, attack_start_time, current_attack_key, last_attack_type, combo_counter
    
    datos = leer_datos_juego()
    if not datos:
        return
    
    if JUGADOR_CONTROLADO == "Player 2":
        jugador1 = datos.get("jugador1", {})
        jugador2 = datos.get("jugador2", {})
    else:
        jugador2 = datos.get("jugador1", {})
        jugador1 = datos.get("jugador2", {})
    
    cubriendose = jugador2.get("cubriendose", False)
    colision = jugador2.get("colision", False)
    hit2 = jugador2.get("hit", {})
    hitbox1 = jugador1.get("hitbox", {})
    
    hit2_x = hit2.get("x", 0)
    hit2_y = hit2.get("y", 0)
    hitbox1_x = hitbox1.get("x", 0)
    hitbox1_y = hitbox1.get("y", 0)
    
    # Predicción mejorada
    pred_hitbox1_x, pred_hitbox1_y = _predict_opponent_position(hitbox1_x, hitbox1_y)
    
    distancia_x = abs(hit2_x - pred_hitbox1_x)
    distancia_y = abs(hit2_y - pred_hitbox1_y)
    
    # Si el enemigo se cubre, cancelar ataque y preparar ki shot o grab
    if cubriendose:
        if attacking and current_attack_key:
            keyboard.release(current_attack_key)
            attacking = False
            current_attack_key = None
        
        # Intentar ki shot si está cubierto
        if jugador2.get("carga", 0) >= 50 and random.random() < 0.4:
            keyboard.press_and_release(teclas["shot"])
        return
    
    # ATAQUE ANTICIPADO: Golpear donde estará el enemigo
    rango_anticipacion_x = 70
    rango_anticipacion_y = 80
    
    # Si está en rango de predicción, comenzar ataque
    if distancia_x < rango_anticipacion_x and distancia_y < rango_anticipacion_y:
        if not attacking:
            # Alternar entre punch y kick inteligentemente
            # Preferir kick si el enemigo está más alto
            if distancia_y > 30:
                current_attack_key = teclas["kick"]
                last_attack_type = "kick"
            else:
                # Alternar normalmente
                current_attack_key = teclas["punch"] if last_attack_type != "punch" else teclas["kick"]
                last_attack_type = "punch" if current_attack_key == teclas["punch"] else "kick"
            
            keyboard.press(current_attack_key)
            attacking = True
            attack_start_time = time.time()
            
    # SISTEMA DE COMBOS: Mantener presión con timing
    elif attacking:
        # Si no hay colisión después de 0.15s, soltar y reintentar
        if not colision and time.time() - attack_start_time > 0.15:
            keyboard.release(current_attack_key)
            attacking = False
            current_attack_key = None
        # Si hay colisión, mantener presionado brevemente para combo
        elif colision:
            # Soltar después de 0.1s para permitir siguiente golpe
            if time.time() - attack_start_time > 0.1:
                keyboard.release(current_attack_key)
                attacking = False
                current_attack_key = None
                # Pequeña pausa antes del siguiente ataque
                time.sleep(0.05)

# Variable global para contador de combos
combo_counter = 0

def adaptive_defense_strategy():
    """Estrategia defensiva adaptativa según HP"""
    global covering, cover_start_time, last_cover_time, charging
    
    datos = leer_datos_juego()
    if not datos:
        return
    
    if JUGADOR_CONTROLADO == "Player 2":
        jugador1 = datos.get("jugador1", {})
        jugador2 = datos.get("jugador2", {})
    else:
        jugador2 = datos.get("jugador1", {})
        jugador1 = datos.get("jugador2", {})
    
    x1 = jugador1.get("x", 0)
    x2 = jugador2.get("x", 0)
    hp2 = jugador2.get("hp", 100)
    hp1 = jugador1.get("hp", 100)
    carga2 = jugador2.get("carga", 0)
    
    acciones_p1 = jugador1.get("acciones", {})
    golpe = acciones_p1.get("golpe", False)
    patada = acciones_p1.get("patada", False)
    disparando = acciones_p1.get("disparando", False)
    
    distancia = abs(x1 - x2)
    ahora = time.time()
    atacando = golpe or patada or disparando
    
    # ESTRATEGIA SEGÚN HP
    
    # HP CRÍTICO (< 25%): Modo supervivencia
    if hp2 < 25:
        # Mantener distancia
        if distancia < 120:
            # Retroceder
            direccion_huida = teclas["left"] if x2 > x1 else teclas["right"]
            keyboard.press(direccion_huida)
            time.sleep(0.1)
            keyboard.release(direccion_huida)
        
        # Cubrir ante cualquier ataque cercano
        if distancia < 100 and atacando:
            if not covering and ahora - last_cover_time > COVER_COOLDOWN:
                keyboard.press(teclas["cover"])
                covering = True
                cover_start_time = ahora
        
        # Cargar energía a distancia segura
        if distancia > 150 and carga2 < 200 and not charging:
            keyboard.press(teclas["charge"])
            charging = True
            
    # HP BAJO (25-50%): Modo cauteloso
    elif hp2 < 50:
        # Cubrir solo ataques cercanos
        if distancia < DEFENSE_RANGE and atacando:
            if not covering and ahora - last_cover_time > COVER_COOLDOWN:
                keyboard.press(teclas["cover"])
                covering = True
                cover_start_time = ahora
        
        # Preferir ataques a distancia
        if distancia > 80 and carga2 >= 50:
            if random.random() < 0.3:
                keyboard.press_and_release(teclas["shot"])
    
    # HP MEDIO-ALTO (> 50%): Modo agresivo
    else:
        # Solo cubrir ataques directos
        if distancia < DEFENSE_RANGE and atacando:
            if not covering and ahora - last_cover_time > COVER_COOLDOWN * 1.5:
                keyboard.press(teclas["cover"])
                covering = True
                cover_start_time = ahora
    
    # Dejar de cubrirse
    if covering:
        if not atacando or ahora - cover_start_time > COVER_DURATION * 0.8:  # Cubrir menos tiempo
            keyboard.release(teclas["cover"])
            covering = False
            last_cover_time = ahora

def strategic_movement():
    """Movimiento estratégico con spacing y footsies"""
    global last_move_time, moving_left, moving_right
    
    datos = leer_datos_juego()
    if not datos:
        return
    
    if JUGADOR_CONTROLADO == "Player 2":
        enemigo = datos.get("jugador1", {})
        bot = datos.get("jugador2", {})
    else:
        bot = datos.get("jugador1", {})
        enemigo = datos.get("jugador2", {})
    
    hit_bot = bot.get("hit", {})
    hitbox_enemy = enemigo.get("hitbox", {})
    
    x_hit_bot = hit_bot.get("x", 0)
    x_hitbox_enemy = hitbox_enemy.get("x", 0)
    
    hp_bot = bot.get("hp", 100)
    hp_enemy = enemigo.get("hp", 100)
    colision = bot.get("colision", False)
    
    ahora = time.time()
    
    distancia_x = abs(x_hit_bot - x_hitbox_enemy)
    
    # RANGO ÓPTIMO DE ATAQUE (footsies)
    OPTIMAL_RANGE_MIN = 35
    OPTIMAL_RANGE_MAX = 55
    
    # Si tiene poca vida, mantener distancia segura
    if hp_bot < 30:
        SAFE_DISTANCE = 120
        if distancia_x < SAFE_DISTANCE:
            # Retroceder
            if x_hit_bot < x_hitbox_enemy:
                keyboard.press(teclas["left"])
                moving_left = True
                if moving_right:
                    keyboard.release(teclas["right"])
                    moving_right = False
            else:
                keyboard.press(teclas["right"])
                moving_right = True
                if moving_left:
                    keyboard.release(teclas["left"])
                    moving_left = False
            last_move_time = ahora
            return
    
    # Si tiene ventaja de HP, ser más agresivo
    if hp_bot > hp_enemy + 20:
        OPTIMAL_RANGE_MIN = 30
        OPTIMAL_RANGE_MAX = 45
    
    # FOOTSIES: Mantener rango óptimo
    if distancia_x > OPTIMAL_RANGE_MAX:
        # Acercarse
        if x_hitbox_enemy < x_hit_bot:
            keyboard.press(teclas["left"])
            moving_left = True
            if moving_right:
                keyboard.release(teclas["right"])
                moving_right = False
        else:
            keyboard.press(teclas["right"])
            moving_right = True
            if moving_left:
                keyboard.release(teclas["left"])
                moving_left = False
                
    elif distancia_x < OPTIMAL_RANGE_MIN and not attacking:
        # Alejarse ligeramente para baiting
        if x_hit_bot < x_hitbox_enemy:
            keyboard.press(teclas["left"])
            moving_left = True
            if moving_right:
                keyboard.release(teclas["right"])
                moving_right = False
        else:
            keyboard.press(teclas["right"])
            moving_right = True
            if moving_left:
                keyboard.release(teclas["left"])
                moving_left = False
    else:
        # En rango óptimo: detener movimiento para atacar
        if moving_left:
            keyboard.release(teclas["left"])
            moving_left = False
        if moving_right:
            keyboard.release(teclas["right"])
            moving_right = False
    
    last_move_time = ahora


def follow_opponent():
    global last_move_time, moving_left, moving_right

    datos = leer_datos_juego()
    if not datos:
        return

    if JUGADOR_CONTROLADO == "Player 2":
        enemigo = datos.get("jugador1", {})
        bot = datos.get("jugador2", {})
    else:
        bot = datos.get("jugador1", {})
        enemigo = datos.get("jugador2", {})

    # Usar centro de hit y hitbox para ambos ejes
    hit_bot = bot.get("hit", {})
    hitbox_enemy = enemigo.get("hitbox", {})
    x_hit_bot = hit_bot.get("x", 0)
    y_hit_bot = hit_bot.get("y", 0)
    x_hitbox_enemy = hitbox_enemy.get("x", 0)
    y_hitbox_enemy = hitbox_enemy.get("y", 0)
    colision = bot.get("colision", False)
    hp_bot = bot.get("hp", 100)

    ahora = time.time()
    if ahora - last_move_time < random.uniform(0.1, 0.25):
        return

    distancia_x = abs(x_hit_bot - x_hitbox_enemy)
    distancia_y = abs(y_hit_bot - y_hitbox_enemy)

    RANGO_GOLPE_EFECTIVO_X = 40
    RANGO_GOLPE_EFECTIVO_Y = 50
    RANGO_CORRECCION_MIN_X = 5
    RANGO_CORRECCION_MIN_Y = 5

    # Detener movimiento si ya colisiona y está atacando
    if colision and attacking:
        if moving_left:
            keyboard.release(teclas["left"])
            moving_left = False
        if moving_right:
            keyboard.release(teclas["right"])
            moving_right = False
        last_move_time = ahora
        return

    # Corregir si está demasiado encima (ambos ejes)
    if distancia_x <= RANGO_CORRECCION_MIN_X and distancia_y <= RANGO_CORRECCION_MIN_Y:
        if x_hit_bot < x_hitbox_enemy:
            keyboard.press(teclas["left"])
            if moving_right:
                keyboard.release(teclas["right"])
                moving_right = False
            moving_left = True
        else:
            keyboard.press(teclas["right"])
            if moving_left:
                keyboard.release(teclas["left"])
                moving_left = False
            moving_right = True
        last_move_time = ahora
        return

    # Si está cerca pero no hay colisión, ajusta con precisión (ambos ejes)
    if not colision and distancia_x <= RANGO_GOLPE_EFECTIVO_X and distancia_y <= RANGO_GOLPE_EFECTIVO_Y:
        if x_hit_bot < x_hitbox_enemy:
            keyboard.press(teclas["right"])
            keyboard.release(teclas["left"])
            moving_right = True
            moving_left = False
        else:
            keyboard.press(teclas["left"])
            keyboard.release(teclas["right"])
            moving_left = True
            moving_right = False
        last_move_time = ahora
        return

    # Si ya colisiona y está en rango, detener
    if colision and distancia_x <= RANGO_GOLPE_EFECTIVO_X and distancia_y <= RANGO_GOLPE_EFECTIVO_Y:
        if moving_left:
            keyboard.release(teclas["left"])
            moving_left = False
        if moving_right:
            keyboard.release(teclas["right"])
            moving_right = False
        last_move_time = ahora
        return

    # Mover para acercarse si no está en posición (prioridad eje X)
    if x_hitbox_enemy < x_hit_bot:
        keyboard.press(teclas["left"])
        if moving_right:
            keyboard.release(teclas["right"])
            moving_right = False
        moving_left = True
    else:
        keyboard.press(teclas["right"])
        if moving_left:
            keyboard.release(teclas["left"])
            moving_left = False
        moving_right = True

    last_move_time = ahora

def attack_logic():
    global attacking, attack_start_time, current_attack_key, last_attack_type

    datos = leer_datos_juego()
    if not datos:
        return

    if JUGADOR_CONTROLADO == "Player 2":
        jugador1 = datos.get("jugador1", {})
        jugador2 = datos.get("jugador2", {})
    else:
        jugador2 = datos.get("jugador1", {})
        jugador1 = datos.get("jugador2", {})

    cubriendose = jugador2.get("cubriendose", False)
    colision = jugador2.get("colision", False)

    hit2 = jugador2.get("hit", {})
    hitbox1 = jugador1.get("hitbox", {})
    hit2_x = hit2.get("x", 0)
    hit2_y = hit2.get("y", 0)
    hitbox1_x = hitbox1.get("x", 0)
    hitbox1_y = hitbox1.get("y", 0)

    # --- PREDICCIÓN: usamos la posición predicha del oponente ---
    pred_hitbox1_x, pred_hitbox1_y = _predict_opponent_position(hitbox1_x, hitbox1_y)

    distancia_x = abs(hit2_x - pred_hitbox1_x)
    distancia_y = abs(hit2_y - pred_hitbox1_y)

    # Rango base (ajustado para compensar latencia)
    max_rango_x = 60
    max_rango_y = 70
    tolerancia_extra = 15

    # Rango dinámico: solo agrega tolerancia si hay colisión
    rango_x = max_rango_x + (tolerancia_extra if colision else 0)
    rango_y = max_rango_y + (tolerancia_extra if colision else 0)

    # Si el enemigo se cubre → soltar ataque
    if cubriendose:
        if attacking and current_attack_key:
            keyboard.release(current_attack_key)
            attacking = False
            current_attack_key = None
        return

    # Seguridad extra: si lleva atacando pero sin colisión por más de 0.25s → soltar
    if attacking and not colision:
        if time.time() - attack_start_time > 0.1:
            keyboard.release(current_attack_key)
            attacking = False
            current_attack_key = None

    # Si no hay colisión y está lejos del rango efectivo → soltar ataque
    if not colision and (distancia_x > max_rango_x or distancia_y > max_rango_y):
        if attacking and current_attack_key:
            keyboard.release(current_attack_key)
            attacking = False
            current_attack_key = None
        return

    # Atacar incluso sin colisión si está dentro de rango medio (usando predicción)
    if not colision and distancia_x < 80 and distancia_y < 90:
        if not attacking:
            current_attack_key = teclas["punch"] if last_attack_type != "punch" else teclas["kick"]
            last_attack_type = "punch" if current_attack_key == teclas["punch"] else "kick"
            keyboard.press(current_attack_key)
            attacking = True
            attack_start_time = time.time()
        return

    # Mantener la tecla presionada mientras esté en rango (usando predicción)
    if distancia_x < rango_x and distancia_y < rango_y:
        if not attacking:
            if last_attack_type == "punch":
                current_attack_key = teclas["kick"]
                last_attack_type = "kick"
            else:
                current_attack_key = teclas["punch"]
                last_attack_type = "punch"
            keyboard.press(current_attack_key)
            attacking = True
            attack_start_time = time.time()
    else:
        # Salió de rango → soltar
        if attacking and current_attack_key:
            keyboard.release(current_attack_key)
            attacking = False
            current_attack_key = None

def defense_logic():
    global covering, cover_start_time, last_cover_time

    datos = leer_datos_juego()
    if not datos:
        return

    if JUGADOR_CONTROLADO == "Player 2":
        jugador1 = datos.get("jugador1", {})
        jugador2 = datos.get("jugador2", {})
    else:
        jugador2 = datos.get("jugador1", {})
        jugador1 = datos.get("jugador2", {})

    x1 = jugador1.get("x", 0)
    x2 = jugador2.get("x", 0)
    hp2 = jugador2.get("hp", 100)

    acciones_p1 = jugador1.get("acciones", {})
    golpe = acciones_p1.get("golpe", False)
    patada = acciones_p1.get("patada", False)
    disparando = acciones_p1.get("disparando", False)

    distancia = abs(x1 - x2)
    ahora = time.time()

    atacando = golpe or patada or disparando

    # ❌ No cubrirse si el bot está atacando (previene transformación)
    if attacking:
        return

    # ✅ Si está en peligro y no se está cubriendo, empezar a cubrirse
    if distancia < DEFENSE_RANGE and atacando and not covering and ahora - last_cover_time > COVER_COOLDOWN:
        keyboard.press(teclas["cover"])
        covering = True
        cover_start_time = ahora
        #print("🛡️ Bot se cubre.")

    # ⏹️ Dejar de cubrirse si ya no hay ataque o lleva mucho tiempo cubriéndose
    if covering:
        if not atacando or ahora - cover_start_time > COVER_DURATION:
            keyboard.release(teclas["cover"])
            covering = False
            last_cover_time = ahora
            #print("🛡️ Bot deja de cubrirse.")

def jump_logic():
    global last_jump_time, jumping

    datos = leer_datos_juego()
    if not datos:
        return

    if JUGADOR_CONTROLADO == "Player 2":
        jugador1 = datos.get("jugador1", {})
        jugador2 = datos.get("jugador2", {})
    else:
        jugador2 = datos.get("jugador1", {})
        jugador1 = datos.get("jugador2", {})

    y1 = jugador1.get("y", 0)
    y2 = jugador2.get("y", 0)

    diff_y = y2 - y1
    ahora = time.time()

    if jumping and ahora - last_jump_time > 1:
        jumping = False

    # Salto + pequeña carga si está lejos
    if not jumping and diff_y > JUMP_DIFF:
        keyboard.press(teclas["jump"])
        if jugador2.get("carga", 0) < MAX_CARGA and abs(jugador1.get("x", 0) - jugador2.get("x", 0)) > CHARGE_DISTANCE:
            keyboard.press(teclas["charge"])
            time.sleep(0.25)
            keyboard.release(teclas["charge"])
        time.sleep(0.3)
        keyboard.release(teclas["jump"])
        jumping = True
        last_jump_time = ahora

def calcular_stats(i):
    return {
        "daño": 8 + 2 * i,
        "defensa": 3 + 2 * i,
        "velocidad": 25 * i
    }

def ejecutar_transformacion(tipo):
    """
    tipo: "secuencial", "fase2", "fase3", "fase4", "fase5", "fase6", "cheat"
    """
    tecla_cover = teclas["cover"]
    keyboard.press(tecla_cover)   # Mantener S presionada

    # ✅ Mantener un pequeño tiempo antes de las demás teclas
    time.sleep(0.08)

    if tipo == "secuencial":  # S + J (punch)
        keyboard.press(teclas["punch"])
        time.sleep(0.25)
        keyboard.release(teclas["punch"])

    elif tipo == "fase2":  # S + (A o D) + J
        keyboard.press(teclas["left"])
        keyboard.press(teclas["punch"])
        time.sleep(0.25)
        keyboard.release(teclas["punch"])
        keyboard.release(teclas["left"])

    elif tipo == "fase3":  # S + A + D + J
        keyboard.press(teclas["left"])
        keyboard.press(teclas["right"])
        keyboard.press(teclas["punch"])
        time.sleep(0.25)
        keyboard.release(teclas["punch"])
        keyboard.release(teclas["left"])
        keyboard.release(teclas["right"])

    elif tipo == "fase4":  # S + K (kick)
        keyboard.press(teclas["kick"])
        time.sleep(0.25)
        keyboard.release(teclas["kick"])

    elif tipo == "fase5":  # S + (A o D) + K
        keyboard.press(teclas["left"])
        keyboard.press(teclas["kick"])
        time.sleep(0.25)
        keyboard.release(teclas["kick"])
        keyboard.release(teclas["left"])

    elif tipo == "fase6":  # S + (A o D) + Shot
        keyboard.press(teclas["left"])
        keyboard.press(teclas["shot"])
        time.sleep(0.25)
        keyboard.release(teclas["shot"])
        keyboard.release(teclas["left"])

    elif tipo == "cheat":  # S + A + D + Shot
        keyboard.press(teclas["left"])
        keyboard.press(teclas["right"])
        keyboard.press(teclas["shot"])
        time.sleep(0.25)
        keyboard.release(teclas["shot"])
        keyboard.release(teclas["left"])
        keyboard.release(teclas["right"])

    # ✅ Soltar S solo al final de toda la combinación
    keyboard.release(tecla_cover)

def nivel_carga(carga):
    if carga < 93:
        return 0
    elif carga < 180:
        return 1
    elif carga <= 252:
        return 2
    elif carga >= 280:
        return 3
    return 0

COSTO_TRANSFORMACION = {
    "secuencial": 1,
    "fase2": 2,
    "fase3": 3,
    "fase4": 2,
    "fase5": 3,
    "fase6": 3,
    "cheat": 3
}

def transform_logic():
    global last_transform_attempt, last_s_press

    datos = leer_datos_juego()
    if not datos:
        return

    # ✅ Bot = Player 2
    if JUGADOR_CONTROLADO == "Player 2":
        jugador = datos.get("jugador2", {})
        oponente = datos.get("jugador1", {})
    else:
        jugador = datos.get("jugador1", {})
        oponente = datos.get("jugador2", {})

    ahora = time.time()

    # Datos del jugador
    hp = jugador.get("hp", 100)
    carga = jugador.get("carga", 0)
    puede_transformarse = jugador.get("puede transformarse", False)
    cap_form = jugador.get("cap form actual", 0)
    cantidad_fases = jugador.get("cantidad de transformaciones", 0)
    max_form = jugador.get("Maxima transformacion", cantidad_fases)
    forma_cheat = jugador.get("Forma Cheat", "").lower()

    # Datos del oponente
    hp_oponente = oponente.get("hp", 100)
    cap_form_oponente = oponente.get("cap form actual", 0)
    forma_cheat_op = oponente.get("Forma Cheat", "").lower()
    daño = jugador.get("damaged", 0)
    defensa = jugador.get("defence", 0)
    velocidad = jugador.get("speed", 0)
    daño_op = oponente.get("damaged", 0)
    defensa_op = oponente.get("defence", 0)
    velocidad_op = oponente.get("speed", 0)

    # --- Cooldown general de transformación ---
    cooldown_base = 2.0
    cooldown_extra = (max_form - cap_form) * 1.2
    cooldown_actual = min(12.0, cooldown_base + cooldown_extra)
    if ahora - last_transform_attempt < cooldown_actual:
        return

    if not puede_transformarse or cantidad_fases < 1:
        return
    if cap_form >= max_form:
        return

    # --- Score ---
    score = 0
    if daño_op > daño: score += 1
    if defensa_op > defensa: score += 1
    if velocidad_op > velocidad: score += 1
    if hp < 60 and hp_oponente > hp: score += 2
    if cap_form_oponente > cap_form: score += 1.5
    if forma_cheat_op and not forma_cheat: score += 2
    if hp < 30: score += 2

    umbral = 3.5 + (cap_form * 0.5)
    if score < umbral:
        return

    # --- Decisión según fases disponibles ---
    tipo = None
    nivel = nivel_carga(carga)

    if cantidad_fases <= 2:
        if nivel >= COSTO_TRANSFORMACION["secuencial"]:
            tipo = "secuencial"
    else:
        if score >= 6 and nivel >= COSTO_TRANSFORMACION["fase6"] and max_form >= 6:
            tipo = "fase6"
        elif score >= 5 and nivel >= COSTO_TRANSFORMACION["fase5"] and max_form >= 5:
            tipo = "fase5"
        elif score >= 4 and nivel >= COSTO_TRANSFORMACION["fase4"] and max_form >= 4:
            tipo = "fase4"
        elif score >= 3 and nivel >= COSTO_TRANSFORMACION["fase3"] and max_form >= 3:
            tipo = "fase3"
        elif score >= 2 and nivel >= COSTO_TRANSFORMACION["fase2"] and max_form >= 2:
            tipo = "fase2"
        elif nivel >= COSTO_TRANSFORMACION["secuencial"]:
            tipo = "secuencial"

    # --- Ejecutar con cooldown de tecla S ---
    if tipo:
        # Verificar cooldown de S
        if ahora - last_s_press < S_COOLDOWN:
            return

        # Presionar la tecla S (cover) antes de la combinación
        tecla_cover = teclas.get("cover", "s")
        keyboard.press(tecla_cover)
        time.sleep(S_COOLDOWN)  # mantenerla presionada para validar

        ejecutar_transformacion(tipo)

        keyboard.release(tecla_cover)  # soltar después

        last_s_press = time.time()
        last_transform_attempt = ahora

def teleport_logic():
    global last_teleport_time

    datos = leer_datos_juego()
    if not datos:
        return

    if JUGADOR_CONTROLADO == "Player 2":
        jugador1 = datos.get("jugador1", {})
        jugador2 = datos.get("jugador2", {})
    else:
        jugador2 = datos.get("jugador1", {})
        jugador1 = datos.get("jugador2", {})

    ahora = time.time()
    if ahora - last_teleport_time < TELEPORT_COOLDOWN:
        return

    x1 = jugador1.get("x", 0)
    x2 = jugador2.get("x", 0)
    distancia = abs(x1 - x2)

    carga = jugador2.get("carga", 0)
    puede_tp = jugador2.get("puede teletransportarse", False)
    hp2 = jugador2.get("hp", 100)
    hp1 = jugador1.get("hp", 100)
    acciones = jugador2.get("acciones", {})
    esta_cargando = acciones.get("cargando", False)

    if not puede_tp or carga < TELEPORT_ENERGY or esta_cargando:
        return

    # Nueva lógica mejorada
    debe_teletransportarse = False

    if hp2 < 35 and distancia < 100:
        # Evasión
        debe_teletransportarse = True
    elif distancia > 160 and hp2 > 40:
        # Perseguir al oponente
        debe_teletransportarse = True

    if not debe_teletransportarse:
        return

    # Dirección hacia el enemigo
    if x2 < x1:
        direccion = teclas["right"]
    else:
        direccion = teclas["left"]

    # Simula doble pulsación rápida
    keyboard.press_and_release(direccion)
    time.sleep(0.05)
    keyboard.press_and_release(direccion)

    last_teleport_time = ahora
    #print("⚡ Bot usa teletransporte hacia", "➡️" if direccion == teclas["right"] else "⬅️")

def charge_logic():
    global charging

    datos = leer_datos_juego()
    if not datos:
        return

    if JUGADOR_CONTROLADO == "Player 2":
        jugador1 = datos.get("jugador1", {})
        jugador2 = datos.get("jugador2", {})
    else:
        jugador2 = datos.get("jugador1", {})
        jugador1 = datos.get("jugador2", {})

    x1 = jugador1.get("x", 0)
    x2 = jugador2.get("x", 0)
    distancia = abs(x1 - x2)

    carga = jugador2.get("carga", 0)
    carga_enemigo = jugador1.get("carga", 0)

    colision = jugador2.get("colision", False)
    cubriendose = jugador2.get("cubriendose", False)

    acciones_p1 = jugador1.get("acciones", {})
    acciones_p2 = jugador2.get("acciones", {})

    p1_cargando = acciones_p1.get("cargando", False)
    p1_disparando = acciones_p1.get("disparando", False)

    golpeando = acciones_p2.get("golpe", False)
    pateando = acciones_p2.get("patada", False)

    ahora = time.time()

    # Condición estratégica para comenzar a cargar
    puede_cargar = (
        not cubriendose and
        not golpeando and
        not pateando and
        not colision and
        carga < MAX_CARGA and
        distancia > CHARGE_DISTANCE and
        not p1_disparando
    )

    # Caso 1: el enemigo también está cargando
    if puede_cargar and p1_cargando and distancia > CHARGE_DISTANCE + 20:
        if not charging:
            keyboard.press(teclas["charge"])
            charging = True
            #print("🔋 Ambos cargando: bot empieza a cargar energía.")
        return

    # Caso 2: el bot está lejos, tiene poca carga, y el enemigo no ataca
    if puede_cargar and carga < 60 and not p1_cargando and not p1_disparando:
        if random.random() < 0.05:  # 5% de probabilidad por frame (~1 intento cada segundo)
            keyboard.press(teclas["charge"])
            charging = True
            #print("🔋 Bot decide cargar porque está seguro.")
        return

    # Detener carga si se rompe la condición
    if charging and (not puede_cargar or carga >= MAX_CARGA):
        keyboard.release(teclas["charge"])
        charging = False
        #print("🔋 Bot deja de cargar.")


def ki_shot_logic():
    global last_ki_shot_time

    datos = leer_datos_juego()
    if not datos:
        return

    if JUGADOR_CONTROLADO == "Player 2":
        jugador1 = datos.get("jugador1", {})
        jugador2 = datos.get("jugador2", {})
    else:
        jugador2 = datos.get("jugador1", {})
        jugador1 = datos.get("jugador2", {})

    ahora = time.time()

    x1 = jugador1.get("x", 0)
    x2 = jugador2.get("x", 0)
    distancia = abs(x1 - x2)

    carga = jugador2.get("carga", 0)
    cubriendose = jugador2.get("cubriendose", False)
    acciones = jugador2.get("acciones", {})
    golpeando = acciones.get("golpe", False)
    pateando = acciones.get("patada", False)
    teleport_activo = ahora - last_teleport_time < TELEPORT_COOLDOWN

    # Condiciones para disparar
    puede_disparar = (
        carga >= KI_SHOT_ENERGY_REQUIRED and
        not cubriendose and
        not golpeando and
        not pateando and
        not teleport_activo
    )

    if puede_disparar and (ahora - last_ki_shot_time > KI_SHOT_COOLDOWN):
        if random.random() < 0.8:  # 80% de chance por frame válido
            keyboard.press_and_release(teclas["shot"])
            last_ki_shot_time = ahora
            #print("💥 Bot dispara un Ki Shot.")


def tackle_logic():
    global last_tackle_time

    datos = leer_datos_juego()
    if not datos:
        return

    if JUGADOR_CONTROLADO == "Player 2":
        jugador1 = datos.get("jugador1", {})
        jugador2 = datos.get("jugador2", {})
    else:
        jugador2 = datos.get("jugador1", {})
        jugador1 = datos.get("jugador2", {})

    ahora = time.time()

    x1 = jugador1.get("x", 0)
    x2 = jugador2.get("x", 0)
    distancia = abs(x1 - x2)

    carga = jugador2.get("carga", 0)
    cubriendose = jugador2.get("cubriendose", False)

    acciones = jugador2.get("acciones", {})
    golpeando = acciones.get("golpe", False)
    pateando = acciones.get("patada", False)

    # Condiciones para ejecutar el tackle
    puede_tacleo = (
        carga >= TACKLE_ENERGY_REQUIRED and
        not cubriendose and
        not golpeando and
        not pateando and
        distancia < TACKLE_DISTANCE
    )

    if puede_tacleo and (ahora - last_tackle_time >= TACKLE_COOLDOWN):
        keyboard.press(teclas["tackle"])
        time.sleep(0.4)  # duración del tacleo
        keyboard.release(teclas["tackle"])
        last_tackle_time = ahora
        #print("💥 Bot ejecuta TACKLE")

def timejump_logic():
    global last_timejump

    datos = leer_datos_juego()
    if not datos:
        return

    if JUGADOR_CONTROLADO == "Player 2":
        jugador = datos.get("jugador2", {})
        enemigo = datos.get("jugador1", {})
    else:
        jugador = datos.get("jugador1", {})
        enemigo = datos.get("jugador2", {})

    ahora = time.time()
    puede_timejump = jugador.get("puede usar timejump", False)
    ki = jugador.get("ki", 0)
    hp = jugador.get("hp", 100)
    cubriendose = jugador.get("cubriendose", False)
    distancia = abs(jugador.get("x", 0) - enemigo.get("x", 0))

    # Condiciones para usar TimeJump
    if (
        puede_timejump and
        ki >= 2 and
        cubriendose and
        ahora - last_timejump >= TIMEJUMP_COOLDOWN and
        (hp < 60 or distancia < 100)
    ):
        # Ejecutar la combinación: Cover + doble golpe rápido
        keyboard.press(teclas["cover"])
        time.sleep(0.05)
        keyboard.press_and_release(teclas["punch"])
        time.sleep(0.05)
        keyboard.press_and_release(teclas["punch"])
        time.sleep(0.05)
        keyboard.release(teclas["cover"])

        last_timejump = ahora
        #print("⏳ Bot usa TimeJump")

def kaioken_logic():
    global last_kaioken_time

    datos = leer_datos_juego()
    if not datos:
        return

    if JUGADOR_CONTROLADO == "Player 2":
        jugador = datos.get("jugador2", {})
    else:
        jugador = datos.get("jugador1", {})

    ahora = time.time()

    cubriendose = jugador.get("cubriendose", False)
    puede_kaioken = jugador.get("puede usar kaioken", "")
    fase_actual = str(jugador.get("fase actual", "")).lower()
    cap_form = jugador.get("cap form actual", 0)
    cantidad_fases = jugador.get("cantidad de transformaciones", 0)
    ki = jugador.get("ki", 0)

    # Condiciones de activación
    if (
        cubriendose and
        puede_kaioken and
        fase_actual not in ("ui", "mui", "ssfp", "black", "ue") and
        ki >= 1 and
        cap_form < (cantidad_fases + 1) and
        ahora - last_kaioken_time >= KAIOKEN_COOLDOWN
    ):
        # Ejecutar: cubrirse + doble disparo
        keyboard.press(teclas["cover"])
        time.sleep(0.05)
        keyboard.press_and_release(teclas["shot"])
        time.sleep(0.05)
        keyboard.press_and_release(teclas["shot"])
        time.sleep(0.05)
        keyboard.release(teclas["cover"])

        last_kaioken_time = ahora
        #print(f"🔥 Bot activa Kaioken ({puede_kaioken})")

def manejar_clash_tackle():
    datos = leer_datos_juego()
    if not datos:
        return

    if JUGADOR_CONTROLADO == "Player 2":
        bot = datos.get("jugador2", {})
    else:
        bot = datos.get("jugador1", {})

    if bot.get("ClashTackle", False):
        tecla_golpe = teclas.get("punch")
        tecla_patada = teclas.get("kick")

        if not tecla_golpe or not tecla_patada:
            return True  # sigue en clash pero no puede actuar

        tecla = random.choice([tecla_golpe, tecla_patada])
        keyboard.press(tecla)
        time.sleep(random.uniform(0.01, 0.02))
        keyboard.release(tecla)

        return True  # sigue en clash

def escape_logic():
    datos = leer_datos_juego()
    if not datos:
        return

    if JUGADOR_CONTROLADO == "Player 2":
        bot = datos.get("jugador2", {})
        enemigo = datos.get("jugador1", {})
    else:
        bot = datos.get("jugador1", {})
        enemigo = datos.get("jugador2", {})

    critico = bot.get("estado critico", False)
    carga = bot.get("carga", 0)
    puede_tp = bot.get("puede teletransportarse", False)
    acciones = bot.get("acciones", {})
    disparando = acciones.get("disparando", False)
    ahora = time.time()

    # Si está en estado crítico y puede teletransportarse
    if critico and puede_tp and carga >= TELEPORT_ENERGY:
        direccion = teclas["right"] if bot.get("x", 0) < enemigo.get("x", 0) else teclas["left"]
        keyboard.press_and_release(direccion)
        time.sleep(0.05)
        keyboard.press_and_release(direccion)
        #print("🌀 Escape por TELEPORT")
        return

    # Si no puede teleport, dispara ki para alejar
    if critico and carga >= KI_SHOT_ENERGY_REQUIRED and not disparando:
        if random.random() < 0.7:
            keyboard.press_and_release(teclas["shot"])
            #print("💥 Escape por KI SHOT")


# ---------------------- EJECUCIÓN DEL BOT EN HILO ----------------------

def loop_bot():
    global last_tick
    tecla_pausa = obtener_tecla_pausa()
    
    while True:
        ahora = time.time()
        if ahora - last_tick < TICK_RATE:
            time.sleep(0.005)
            continue
        last_tick = ahora
        
        datos = leer_datos_juego()
        if not datos:
            continue
        
        # PRIORIDAD 1: Esquiva inteligente
        if intelligent_dodge():
            continue  # Si esquivó, skip otras acciones este frame
        
        # PRIORIDAD 2: Estrategia defensiva adaptativa
        adaptive_defense_strategy()
        
        # PRIORIDAD 3: Movimiento estratégico
        strategic_movement()
        
        # PRIORIDAD 4: Ataque preciso
        precise_attack_logic()
        
        # PRIORIDAD 5: Salto táctico
        jump_logic()
        
        # PRIORIDAD 6: Gestión de energía
        charge_logic()
        ki_shot_logic()
        
        # PRIORIDAD 7: Habilidades especiales
        transform_logic()
        tackle_logic()
        timejump_logic()
        kaioken_logic()
        
        # PRIORIDAD 8: Clash management
        manejar_clash_tackle()
        
        try:
            if keyboard.is_pressed("esc") or keyboard.is_pressed(tecla_pausa):
                break
        except:
            print("❌ Error al detectar la tecla.")
        
        time.sleep(0.02)


# ---------------------- INICIO ----------------------

def iniciar_bot():
    cargar_controles()
    hilo = threading.Thread(target=loop_bot)
    hilo.start()

iniciar_bot()