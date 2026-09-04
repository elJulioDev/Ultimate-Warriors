# Guía para Crear un Personaje - Ultimate Warriors

Guía completa paso a paso para crear un personaje personalizado e importarlo al juego.

---

## Requisitos Previos

- Sprites del personaje en **PNG con fondo transparente**
- Editor de texto para crear el `char.json` (VS Code, Notepad++, etc.)
- El juego **Game.ppsm** abierto en PowerPoint con macros habilitadas

---

## Paso 1: Crear la Estructura de Carpetas

Cada personaje vive dentro de la carpeta `chars/`. La estructura debe ser exactamente así:

```
chars/
└── MiPersonaje/              # Nombre de la carpeta del personaje
    ├── char.json             # Archivo de configuración (OBLIGATORIO)
    ├── ico.png               # Icono para la selección de personajes (recomendado)
    ├── normal/               # Forma base (carpeta OBLIGATORIA)
    │   ├── stand.png         # Sprite de idle/parado
    │   ├── punch_1.png       # Sprites de golpe (secuencia)
    │   ├── kick_1.png        # Sprites de patada (secuencia)
    │   ├── damaged_1.png     # Sprites de daño recibido
    │   ├── aura_1.png        # Sprites de aura
    │   ├── down.png          # Sprite agachado
    │   ├── up.png            # Sprite saltando
    │   ├── fly_left.png      # Sprite volando izquierda
    │   ├── fly_right.png     # Sprite volando derecha
    │   ├── power_1.png       # Sprites de carga de Ki
    │   ├── taunt_1.png       # Sprites de taunt/burla
    │   ├── coverup.png       # Sprite cubriéndose
    │   ├── win.png           # Sprite de victoria
    │   ├── lose.png          # Sprite de derrota
    │   └── blast.png         # Sprite del proyectil Ki
    └── [nombre_transformacion]/  # Carpetas por cada transformación
        ├── stand.png
        ├── punch_1.png
        └── ...
```

### Reglas de Carpetas

1. **El nombre de la carpeta** del personaje se usa como identificador único en todo el juego
2. **La carpeta base** (normalmente `normal/`) es obligatoria — es la forma inicial del personaje
3. **Las carpetas de transformación** llevan el mismo nombre que el valor definido en `char.json` → `"phase 1": "ssj"` = carpeta `ssj/`
4. **Si una transformación no tiene carpeta**, el juego no la cargará correctamente

---

## Paso 2: Preparar los Sprites

### Formato Requerido

- **Extensión:** `.png`
- **Fondo:** Transparente
- **Resolución:** Consistente entre todos los sprites del mismo personaje (ej: 200x200px)

### Nomenclatura de Sprites

Los sprites se nombran con un prefijo de categoría y un número de secuencia:

| Archivo | Descripción | Secuencia |
|---------|-------------|-----------|
| `stand.png` o `stand_1.png` | Idle / Parado | 1 o Animation (si hay más de 1, se anima) |
| `punch_1.png`, `punch_2.png`... | Golpes | Secuencia de animación |
| `kick_1.png`, `kick_2.png`... | Patadas | Secuencia de animación |
| `damaged_1.png`, `damaged_2.png`... | Daño recibido | Secuencia de animación |
| `aura_1.png`, `aura_2.png`... | Aura / Efecto visual | Secuencia de animación |
| `power_1.png`, `power_2.png`... | Carga de Ki | Secuencia de animación |
| `taunt_1.png`, `taunt_2.png`... | Taunt / Burla | Secuencia de animación |
| `dodge_1.png`, `dodge_2.png`... | Esquive (solo formas especiales) | Secuencia |
| `down.png` | Agachado | 1 sprite |
| `up.png` | Saltando | 1 sprite |
| `fly_left.png` | Volando izquierda | 1 sprite |
| `fly_right.png` | Volando derecha | 1 sprite |
| `coverup.png` | Cubriéndose | 1 sprite |
| `win.png` | Victoria | 1 sprite |
| `lose.png` | Derrota | 1 sprite |
| `blast.png` | Proyectil Ki | 1 sprite |

### Categorías de Sprites que el Juego Detecta

El sistema verifica automáticamente estos nombres de archivo al importar:

```
aura, damaged, kick, punch, taunt, power, blast, dodge, roll, 
stand, fly_left, fly_right, up, down, tackle
```

### Sprites Mínimos Recomendados

Para que el personaje funcione correctamente, como mínimo necesitas:

```
stand.png        ← Obligatorio (el juego busca este para la preview)
punch_1.png      ← Para atacar
kick_1.png       ← Para atacar
damaged_1.png    ← Para recibir daño
aura_1.png       ← Para el aura visual
down.png         ← Para agacharse
up.png           ← Para saltar
fly_left.png     ← Para moverse a la izquierda
fly_right.png    ← Para moverse a la derecha
coverup.png      ← Para cubrirse
win.png          ← Para pantalla de victoria
lose.png         ← Para pantalla de derrota
blast.png        ← Para el proyectil Ki
```

---

## Paso 3: Crear el `char.json`

Este es el archivo más importante. Define todas las propiedades del personaje.

### Estructura Básica (Mínima)

Un personaje sin transformaciones:

```json
{
    "folder": "MiPersonaje",
    "base": "normal",
    "name": "Nombre del Personaje",
    "statistics": {
        "speed": 420,
        "life": 100,
        "damaged": 97,
        "defence": 17
    },
    "cheats": {
        "slot 1": "teleport"
    }
}
```

### Estructura Completa (Con Transformaciones)

```json
{
    "folder": "MiPersonaje",
    "base": "normal",
    "name": "Nombre del Personaje",
    "statistics": {
        "speed": 420,
        "life": 100,
        "damaged": 97,
        "defence": 17,
        "Attack Speed": 7.5,
        "Stand Speed": 12,
        "Taunt Speed": 12,
        "Aura Speed": 1
    },
    "transformation": {
        "eneable": true,
        "phase 1": "ssj",
        "phase 2": "ssj2",
        "phase 3": "ssj3",
        "phase 4": "god",
        "phase 5": "blue",
        "phase 6": "ui"
    },
    "transformation color": {
        "eneable": true,
        "phase 1": {"color": "#ffff00", "radio": 4, "transparecy": 75},
        "phase 2": {"color": "#ffff00", "radio": 5, "transparecy": 60},
        "cheat phase": {"color": "#95A4D6", "radio": 3, "transparecy": 40}
    },
    "Char Effects": {
        "Phase 1": {"eneable": true, "effect": "yellow", "speed": 0.12, "transparecy": 70},
        "Phase 2": {"eneable": true, "effect": "cianray", "speed": 0.12, "transparecy": 20}
    },
    "cheats": {
        "slot 1": "mui",
        "slot 2": "kaiokenx4",
        "slot 3": "teleport",
        "slot 4": "dodge=phase:6"
    }
}
```

---

## Paso 4: Referencia Completa de `char.json`

### Campo `folder`

```json
"folder": "MiPersonaje"
```

- **Tipo:** String (obligatorio)
- **Descripción:** Nombre de la carpeta del personaje dentro de `chars/`
- **Debe coincidir** exactamente con el nombre de la carpeta

### Campo `base`

```json
"base": "normal"
```

- **Tipo:** String (obligatorio)
- **Descripción:** Nombre de la subcarpeta que contiene la forma base del personaje
- **Ejemplos:** `"normal"`, `"base"`, `"Perfect"`, `"rage"`

### Campo `name`

```json
"name": "Son Goku"
```

- **Tipo:** String (obligatorio)
- **Descripción:** Nombre que se muestra en la pantalla de selección
- **Puede estar vacío** — el juego usa `"El Pichula"` como fallback

### Campo `statistics`

```json
"statistics": {
    "speed": 420,
    "life": 100,
    "damaged": 97,
    "defence": 17,
    "Attack Speed": 7.5,
    "Stand Speed": 12,
    "Taunt Speed": 12,
    "Aura Speed": 1
}
```

| Estadística | Tipo | Obligatorio | Descripción | Valor por defecto |
|-------------|------|-------------|-------------|-------------------|
| `speed` | Number | Sí | Velocidad de movimiento horizontal | 420 |
| `life` | Number | Sí | Vida máxima del personaje | 100 |
| `damaged` | Number | Sí | Poder de ataque base | 97 |
| `defence` | Number | Sí | Defensa (reduce daño recibido) | 17 |
| `Attack Speed` | Number | No | Velocidad de animación de ataque (menor = más rápido). Se multiplica por 0.01. Mínimo: 0.06 | 0.08 (8) |
| `Stand Speed` | Number | No | Velocidad de animación idle | 0.08 (8) |
| `Taunt Speed` | Number | No | Velocidad de animación de taunt | 0.08 (8) |
| `Aura Speed` | Number | No | Velocidad de animación del aura | 0.08 (8) |

**Notas:**
- Los valores de speed van de ~350 (lento) a ~500 (rápido)
- Los valores de life van de 80 (frágil) a 200 (tanque)
- Los valores de damaged van de 80 (bajo) a 140 (alto)
- Los valores de defence van de 10 (baja) a 25 (alta)

### Campo `transformation`

```json
"transformation": {
    "eneable": true,
    "phase 1": "ssj",
    "phase 2": "ssj2",
    "phase 4": "god"
}
```

- **`eneable`** (Boolean, obligatorio): Activa/desactiva el sistema de transformaciones
- **`phase N`** (String): Nombre de la subcarpeta para cada fase de transformación
- **Las fases van de 1 a 7** (fase 7 = forma cheat)
- **Se pueden saltar fases** — Vegeta usa phase 1, 2, 4, 5, 6,5 (sin phase 3)
- **Soporta decimales** — `"phase 6,5": "blue_ev"` funciona

**Ejemplos de uso:**

| Personaje | Fases | Notas |
|-----------|-------|-------|
| Goku | 1-6 | Transformaciones secuenciales |
| Vegeta | 1, 2, 4, 5, 6,5 | Salta phase 3, usa decimales |
| Broly | 4 | Solo una transformación |
| Beerus | (ninguna) | Sin transformaciones |
| Cell | (ninguna) | Sin transformaciones |

### Campo `base color` (Opcional)

Para personajes que tienen un aura en su forma base:

```json
"base color": {
    "eneable": true,
    "color": "#ffff00",
    "radio": 3,
    "transparecy": 80
}
```

| Propiedad | Tipo | Descripción |
|-----------|------|-------------|
| `eneable` | Boolean | Activar aura en forma base |
| `color` | String | Color hexadecimal del aura |
| `radio` | Number | Tamaño del radio del aura (1-10) |
| `transparecy` | Number | Transparencia (0=sólido, 100=invisible) |

### Campo `transformation color`

Define el color del aura/glow durante cada transformación:

```json
"transformation color": {
    "eneable": true,
    "phase 1": {"color": "#ffff00", "radio": 4, "transparecy": 75},
    "phase 2": {"color": "#ffff00", "radio": 5, "transparecy": 60},
    "cheat phase": {"color": "#95A4D6", "radio": 3, "transparecy": 40}
}
```

- **`eneable`** (Boolean): Activa/desactiva los colores de transformación
- **`phase N`** (Object): Color para cada fase — `"phase 1"`, `"phase 2"`, etc.
- **`cheat phase`** (Object): Color para la fase cheat (phase 7)
- **`cheat phase 2`** (Object): Segundo color cheat (para personajes con doble cheat)

| Propiedad | Tipo | Descripción |
|-----------|------|-------------|
| `color` | String | Color hexadecimal |
| `radio` | Number | Tamaño del glow (1-10) |
| `transparecy` | Number | Transparencia (0-100) |

### Campo `Char Effects`

Define el efecto visual de aura que se superpone al personaje durante cada fase:

```json
"Char Effects": {
    "Phase 0": {"eneable": true, "effect": "cianray", "speed": 0.12, "transparecy": 20},
    "Phase 1": {"eneable": true, "effect": "yellow", "speed": 0.12, "transparecy": 70},
    "Phase 2": {"eneable": true, "effect": "cianray", "speed": 0.12, "transparecy": 20},
    "Phase 7": {"eneable": true, "effect": "cian", "speed": 0.08, "transparecy": 65}
}
```

**Efectos disponibles** (carpeta `data/resources/CharEffects/`):

| Efecto | Color |
|--------|-------|
| `yellow` | Amarillo (SSJ clásico) |
| `blue` | Azul (SSJ Blue) |
| `blueEv` | Azul oscuro (Blue Evolution) |
| `cian` | Cian |
| `cianray` | Cian con rayos |
| `god` | Rojo divino (SSJ God) |
| `golden` | Dorado (Freezer Golden) |
| `green` | Verde (Broly) |
| `orange` | Naranja (Piccolo Orange) |
| `purple` | Púrpura (Ultra Ego) |
| `purpleray` | Púrpura con rayos |
| `red` | Rojo |
| `redray` | Rojo con rayos |
| `beast` | Beast (Gohan Beast) |
| `divine` | Divino |
| `bright` | Brillante |
| `goldbright` | Dorado brillante |
| `stars` | Estrellas |

| Propiedad | Tipo | Descripción |
|-----------|------|-------------|
| `eneable` | Boolean | Activar/desactivar efecto |
| `effect` | String | Nombre del efecto (ver tabla) |
| `speed` | Number | Velocidad de animación (0.06-0.2) |
| `transparecy` | Number | Transparencia (0-100) |

### Campo `cheats`

Define las habilidades especiales del personaje:

```json
"cheats": {
    "slot 1": "teleport",
    "slot 2": "fastCharge",
    "slot 3": "kaiokenx4",
    "slot 4": "dodge=phase:6"
}
```

**Cheats disponibles:**

| Cheat | Efecto |
|-------|--------|
| `teleport` | Permite teletransportar en forma base con Ki >= 1 |
| `fastCharge` | +15% velocidad de carga (85 px/frame) |
| `Maxcharge` | +31% velocidad de carga (95 px/frame) |
| `lowercharge` | -23% velocidad de carga (60 px/frame) |
| `mui` | Ultra Instinto Maestrado (fase cheat) |
| `ue` | Ultra Ego (fase cheat) |
| `black` | Black (fase cheat, defensa superior) |
| `SSFP` | Super Saiyan Full Power (fase cheat) |
| `kaiokenxN` | Kaioken x N (ej: `kaiokenx4`, `kaiokenx20`) |
| `TimeJump` | Congela oponente 5 segundos |
| `Dodge` | Esquive 25-45% con costo de carga |
| `MasterDodge` | Esquive 95-100% sin costo |
| `Accuracy` | Reduce capacidad de esquive del oponente |
| `Recoilless` | Reduce daño bloqueado, anula knockback |
| `noformback` | No puede volver a forma base |
| `updim` | Aumenta dimensiones del personaje |
| `updim=phase:N` | updim solo en fase N específica |
| `fixK` | Ajusta sprite de patada si es muy ancho |
| `fixJ` | Ajusta sprite de golpe si es muy ancho |
| `Android` | Auto-carga, no puede cargar manualmente |
| `RecoverLife=X` | Regenera X de vida periódicamente |
| `NoShot` | No puede disparar Ki blasts |
| `NoShot=phase:N` | NoShot solo en fase N |
| `dodge=phase:N` | Dodge activo solo en fase N |

---

## Paso 5: El Icono (`ico.png`)

- **Tipo:** PNG con fondo transparente
- **Tamaño recomendado:** 36x36 píxeles
- **Nombre:** Exactamente `ico.png` en la raíz de la carpeta del personaje
- **Función:** Se muestra en la grilla de selección de personajes

Si no se encuentra `ico.png`, el juego usa `data/resources/ico_char_null.png` como placeholder.

---

## Paso 6: Importar al Juego

### Proceso de Verificación

1. Abre `Game.ppsm` en PowerPoint
2. Habilita macros cuando se pregunte
3. Inicia la presentación (F5)
4. Ve a **Juego Local** → **Selección de Personajes**
5. Haz clic en el botón **"Verificar"**

### Qué Hace el Botón "Verificar"

El botón ejecuta la macro `OrdenarCharsFolder` que:

1. **Escanea** la carpeta `chars/` buscando subcarpetas
2. **Detecta** todas las carpetas de personajes (nuevos y existentes)
3. **Carga** el `ico.png` de cada uno (o el placeholder si no existe)
4. **Crea** un botón en la grilla de selección para cada personaje
5. **Ordena** primero los personajes oficiales, luego los personalizados
6. **Elimina** personajes que ya no existen en la carpeta

### Límites

- **Máximo 66 personajes** importados simultáneamente
- Si hay más de 45, la grilla cambia a 22 columnas

### Orden de Aparición

Los personajes oficiales aparecen primero en este orden:
```
Goku, Vegeta, Gohan, Trunks, Piccolo, Android17, Android18, Videl, 
KidGohan, Freezer, Cell, KidBuu, Gotenks, SuperBuuGohan, Android21, 
Black, Hit, Jiren, Broly, Beerus, Gogeta, Vegetto, Zamasu, Kefla, 
Moro, Granola, Janemba
```

Los personajes personalizados aparecen después, en orden alfabético.

---

## Paso 7: Verificar que Funciona

Al seleccionar tu personaje en la pantalla de selección:

1. **Preview:** Se muestra el sprite `stand.png` (o `stand_1.png`) de la forma base
2. **Nombre:** Se muestra el campo `name` del `char.json`
3. **Icono de transformación:** Aparece si `"transformation" → "eneable": true`
4. **Al jugar:** El personaje carga con todos los sprites y estadísticas definidas

---

## Ejemplo Práctico: Crear un Personaje Paso a Paso

### 1. Crear carpetas

```
chars/
└── TrunksFuture/
    ├── char.json
    ├── ico.png
    ├── normal/
    │   ├── stand.png
    │   ├── punch_1.png ... punch_8.png
    │   ├── kick_1.png ... kick_6.png
    │   ├── damaged_1.png ... damaged_4.png
    │   ├── aura_1.png, aura_2.png
    │   ├── power_1.png, power_2.png
    │   ├── taunt_1.png ... taunt_8.png
    │   ├── down.png
    │   ├── up.png
    │   ├── fly_left.png
    │   ├── fly_right.png
    │   ├── coverup.png
    │   ├── win.png
    │   ├── lose.png
    │   └── blast.png
    └── super/
        ├── stand.png
        ├── punch_1.png ... punch_10.png
        ├── kick_1.png ... kick_8.png
        ├── damaged_1.png ... damaged_4.png
        ├── aura_1.png, aura_2.png
        ├── power_1.png, power_2.png
        ├── taunt_1.png ... taunt_10.png
        ├── down.png
        ├── up.png
        ├── fly_left.png
        ├── fly_right.png
        ├── coverup.png
        ├── win.png
        ├── lose.png
        └── blast.png
```

### 2. Crear `char.json`

```json
{
    "folder": "TrunksFuture",
    "base": "normal",
    "name": "Trunks (Future)",
    "statistics": {
        "speed": 430,
        "life": 105,
        "damaged": 100,
        "defence": 18,
        "Attack Speed": 7.5
    },
    "transformation": {
        "eneable": true,
        "phase 4": "super"
    },
    "transformation color": {
        "eneable": true,
        "phase 4": {"color": "#ffff00", "radio": 4, "transparecy": 70},
        "cheat phase": {"color": "#00aaff", "radio": 3, "transparecy": 40}
    },
    "Char Effects": {
        "Phase 4": {"eneable": true, "effect": "yellow", "speed": 0.12, "transparecy": 70},
        "Phase 5": {"eneable": true, "effect": "blue", "speed": 0.08, "transparecy": 65}
    },
    "cheats": {
        "slot 1": "teleport",
        "slot 2": "fastCharge"
    }
}
```

### 3. Importar

1. Guarda la carpeta `TrunksFuture` dentro de `chars/`
2. Abre el juego y ve a selección de personajes
3. Haz clic en **"Verificar"**
4. Tu personaje aparecerá en la grilla
5. Selecciona y ¡a pelear!

---

## Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Personaje no aparece | Falta `char.json` o JSON mal formateado | Verifica la sintaxis JSON |
| Preview no carga | Falta `stand.png` en la carpeta base | Asegúrate de que el archivo existe |
| Transformación no funciona | Nombre de carpeta no coincide con `char.json` | Verifica que `"phase N": "nombre"` = carpeta `nombre/` |
| Icono no aparece | Falta `ico.png` | Crea el icono o usa el placeholder |
| Error al importar | JSON con comas finales o comillas incorrectas | Usa un validador JSON |
| No hay aura | `"eneable": false` o efecto no existe | Verifica el campo y el nombre del efecto |
| Juego se cierra al jugar | Sprite faltante en alguna fase | Asegúrate de que cada fase tenga los sprites mínimos |

---

## Notas Importantes

- **NO uses tildes ni caracteres especiales** en nombres de carpetas o archivos
- **El campo `eneable`** (sin la "b") es intencional — el juego usa esta escritura. No lo corrijas
- **Las transformaciones se calculan** con fórmulas del motor — los stats suben automáticamente por fase
- **Los cheats se activan** con combinaciones de teclas en el juego (ver README para controles)
- **Prueba con un personaje existente** primero para entender la estructura antes de crear uno nuevo
