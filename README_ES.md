<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/Language-English-blue?style=for-the-badge" alt="English"></a>
  <a href="README_ES.md"><img src="https://img.shields.io/badge/Idioma-Español-red?style=for-the-badge" alt="Español"></a>
</p>

# Ultimate Warriors

### Juego de Peleas 2D de Dragon Ball en PowerPoint

> VBA-Powered | Bot de Python | Windows | PowerPoint 2016+

Un juego de peleas 2D completo construido enteramente en PowerPoint usando VBA. Incluye transformaciones, combos, movimientos especiales y un bot inteligente de Python.

![Status](https://img.shields.io/badge/Estado-Activo-success?style=flat-square)
![Version](https://img.shields.io/badge/Versión-1.0.0-blue?style=flat-square)
![Genre](https://img.shields.io/badge/Género-Peleas-red?style=flat-square)

---

## Video de Lanzamiento

<p align="center">
  <a href="https://www.youtube.com/watch?v=_dMCui9MIOw">
    <img src="https://img.youtube.com/vi/_dMCui9MIOw/maxresdefault.jpg" alt="Ultimate Warriors - Video de Lanzamiento" width="720">
  </a>
</p>

<p align="center">
  <a href="https://www.youtube.com/watch?v=_dMCui9MIOw">Ver en YouTube</a>
</p>

> [!NOTE]
> Este es el video oficial de lanzamiento de Ultimate Warriors. Mira el gameplay completo y las características en [YouTube](https://www.youtube.com/watch?v=_dMCui9MIOw).

---

## Características

### Sistema de Combate
- Mecánicas de pelea 2D: movimiento, saltos, ataques, ráfagas de Ki
- Detección de colisiones con cajas y sistema preciso de hitbox/hurtbox
- Sistema de guardia, embestida y cobertura
- Calculadora de combos con seguimiento de daño y puntuación
- Dragon rush: finalizador de combo especial
- Time jump: mecánica de cámara lenta
- Sistema de retroceso con estados de golpe crítico

### Sistema de Transformaciones
- Transformaciones infinitas (no limitado a 6 fases)
- Escalado dinámico de estadísticas por fase (velocidad, daño, defensa)
- Modos Kaioken con multiplicador configurable y drenaje de vida
- Efectos visuales: auras, brillos y animaciones de transformación
- Sistema de teletransporte: intercambio de posición instantáneo
- 25+ trucos de personaje con habilidades únicas

### Características Avanzadas
- Sistema de animación de sprites con renderizado cuadro a cuadro y caché
- 22 escenarios definidos en JSON con propiedades únicas
- Sistema de puntuación por rondas con puntos, rangos y pantallas de victoria
- Sistema de buffer de entrada para detección de combos estilo juegos de pelea
- Sombras dinámicas de personajes
- Sistema de gravedad y física (JumpVelocity=-500, Gravity=1000)

### IA y Personalización
- Integración de bot de Python con oponente de IA en tiempo real
- Datos de personajes en JSON para fácil creación y modificación
- Controles personalizables con teclas reasignables para P1 y P2
- Sistema de sonido con música y efectos de sonido vía APIs de Windows
- Interfaz bilingüe: localización en español e inglés

---

## Aspectos Técnicos

### Motor del Juego (dbxwCore)
- Bucle de juego VBA con sincronización DeltaTime vía `GetTickCount`
- Gestión de estados para personajes y jugabilidad
- Física de colisiones con gravedad y límites de pantalla
- Arquitectura modular para código mantenible
- Integración con APIs de Windows para teclado (`GetAsyncKeyState`) y sonido (`winmm.dll`)

### Diseño Basado en Datos
- Configuración JSON para personajes, escenarios, controles y ajustes
- Sistema de sprites con carga dinámica y caché de cuadros
- Persistencia de ajustes con funcionalidad de guardado/carga
- Comunicación con bot vía intercambio de archivos JSON en tiempo real
- Parser JSON personalizado (PPTGames VBAJSON v1.13)

---

## Estructura del Proyecto

```
Ultimate-Warriors/
├── Game.ppsm                    # Juego principal de PowerPoint (con macros)
├── README.md
├── requirements.txt             # Dependencias de Python
│
├── chars/                       # 30 carpetas de personajes
│   ├── Goku/char.json
│   ├── Vegeta/char.json
│   └── ... (30 personajes)
│
├── stages/                      # 22 carpetas de escenarios
│   ├── World Tournament Stage/
│   ├── Planet Namek/
│   └── ... (22 escenarios)
│
├── sound/                       # 25 pistas de música MP3
├── font/                        # Fuentes personalizadas (display HUD)
│   ├── Great Fighter Demo.otf
│   ├── Great Fighter Demo.ttf
│   ├── PIZZADUDEPOINTERS.ttf
│   └── Super Squad.ttf
│
├── data/
│   ├── version.data             # Información de versión
│   ├── Changelog.txt            # Registro de cambios
│   ├── Controls.json            # Mapeo de controles
│   ├── Language.json            # Localización bilingüe (ES/EN)
│   ├── Settings.json            # Ajustes del juego
│   ├── style.css                # UI de galería de sprites
│   ├── index.js                 # Lógica de la galería
│   ├── index_credits.html       # Página de créditos
│   ├── icon.ico                 # Icono de la app
│   ├── icon.png                 # Icono de la app (PNG)
│   ├── sound_effects/           # 44 archivos WAV/MP3 de efectos
│   ├── resources/
│   │   ├── CharEffects/         # 106 sprites PNG de aura/efectos
│   │   ├── GameEffects/         # 46 sprites PNG de explosiones/ventisca
│   │   ├── menu/
│   │   │   ├── Anim/            # Animaciones del menú
│   │   │   ├── credits.png
│   │   │   ├── main.png
│   │   │   ├── selection.png
│   │   │   └── settings.png
│   │   ├── coconut.png
│   │   ├── ico_char_null.png
│   │   ├── null.png
│   │   └── pre_stage_null.png
│   └── bot/                     # Bot de IA en Python (modular)
│       ├── main.py
│       ├── config.py
│       ├── core/
│       │   ├── game_reader.py
│       │   ├── input_manager.py
│       │   └── state_manager.py
│       ├── strategies/
│       │   ├── adaptive.py
│       │   ├── aggressive.py
│       │   └── defensive.py
│       ├── ai/
│       │   ├── combat.py
│       │   ├── defense.py
│       │   ├── movement.py
│       │   ├── pattern_analyzer.py
│       │   └── prediction.py
│       ├── abilities/
│       │   ├── combo_breaker.py
│       │   ├── energy.py
│       │   ├── special_moves.py
│       │   ├── teleport.py
│       │   └── transformation.py
│       └── utils/
│           ├── constants.py
│           └── helpers.py
```

---

## Personajes (30)

| Personaje | Forma Base | Transformaciones | Habilidades Especiales |
|-----------|-----------|-----------------|-------------------|
| Goku | Normal | SSJ, SSJ2, SSJ3, God, Blue, UI (6 fases) | MUI, Kaioken x4, Teleport, Dodge |
| Vegeta | Normal | SSJ, SSJ2, God, Blue, Blue Evolution (5+ fases, decimal 6.5) | Ultra Ego, Teleport |
| Gohan | Base | SSJ, Ultimate, Beast (3 fases) | Fast Charge, Teleport |
| Gohan Niño | SSJ2 | - | Teleport, Fast Charge |
| Piccolo | Base | Super, Orange (2 fases) | Teleport, Updim (fase 7) |
| Vegetto | Blue | - | Teleport, Fast Charge |
| Gogeta | Blue | - | Teleport, Fast Charge |
| Gotenks | SSJ3 | - | Teleport, Fast Charge |
| Trunks | Base | SSJ, SSJ2 (2 fases) | FixK, Teleport |
| Bardock | Base | SSJ (1 fase) | Teleport |
| Broly | Rage | SSJ (fase 4) | Updim, SSFP, noformback, Teleport |
| Freezer | Normal | Golden (fase 5) | Black, Teleport |
| Cell | Perfect | - | Teleport |
| Cooler | Base | Final (fase 1) | Teleport, Updim (fase 1), Fast Charge |
| Android 17 | Base | - | Android, Teleport, Fast Charge |
| Android 18 | Base | - | Android, Teleport |
| Android 21 | Base | - | Teleport, RecoverLife=1 |
| Kid Buu | Base | - | Teleport, Fast Charge, FixK, RecoverLife=1 |
| Super Buu (Gohan) | Base | - | Teleport, Fast Charge, RecoverLife=1 |
| Hit | Base | - | Teleport, TimeJump |
| Jiren | Normal | Full Power (fase 2) | Teleport, noformback, Fast Charge |
| Kefla | LSSJ | - (deshabilitado) | Teleport, Fast Charge |
| Beerus | Base | - | Teleport, Fast Charge, Accuracy |
| Zamasu | Base | Corrupted (fase 1) | Teleport, Fast Charge, Updim (fase 1), noformback |
| Black | Normal | SSJ, Rose (2 fases) | Teleport |
| Janemba | Base | - | Teleport, Fast Charge |
| Moro | Base | - (deshabilitado) | Fast Charge, Teleport |
| Granola | Base | - | Teleport, Accuracy, Fast Charge |
| Videl | Base | - | Teleport |
| Alex | Normal | SSJ, God, Blue (3 fases) | Fast Charge, Teleport, Kaioken x4, Ultra Ego |

---

## Escenarios (22)

Archipelago, Cell Games Arena, Destroyed Planet Namek, Future in Ruins, Glacier, Hell, Hyperbolic Time Chamber, Kami Lookout, Open Field, Plains, Planet Namek, Power Tree, Rocky Site, Sky, Space (Earth), Space (Planet Vegeta), Supreme Kai World, The Nameless Planet, Tournament of Power Arena, Underground Lake, Westland, World Tournament Stage

---

## Mecánicas del Juego

### Estadísticas Base de Personajes

Cada personaje define sus estadísticas base en `char.json`:

```json
{
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
}
```

| Estadística | Descripción |
|------|-------------|
| `speed` | Velocidad de movimiento horizontal |
| `life` | Salud máxima |
| `damaged` | Poder de ataque base |
| `defence` | Reduce el daño recibido |
| `Attack Speed` | Velocidad de animación de ataque (menor = más rápido) |
| `Stand Speed` | Velocidad de animación en reposo |
| `Taunt Speed` | Velocidad de animación de burla |
| `Aura Speed` | Velocidad de animación de aura |

#### Ejemplos de Estadísticas de Personajes

| Personaje | Velocidad | Vida | Daño | Defensa | Vel. Ataque |
|-----------|-------|------|---------|---------|--------------|
| Goku | 420 | 100 | 97 | 17 | - |
| Vegeta | 420 | 100 | 97 | 17 | - |
| Broly | 500 | 100 | 110 | 18 | 7.5 |
| Beerus | 500 | 150 | 135 | 20 | 6 |

---

### Sistema de Transformaciones

Las transformaciones se activan con combinaciones de teclas y consumen niveles de energía Ki. El sistema usa un contador interno llamado `CapForm` que indica la fase actual.

#### Estructura de Fases

El motor soporta **transformaciones infinitas** — no limitado a 6 o 7 fases. La forma cheat (MUI, UE, BLACK, SSFP) se convierte en la forma final de la cadena de transformación.

```
Fase 0: Estado base
Fase 1: Primera transformación (ej. SSJ)
Fase 2: Segunda transformación (ej. SSJ2)
Fase N: Cualquier número de fase (incluyendo decimales como 6.5)
```

#### Ejemplo: Goku (6 fases)

```
Fase 0: normal
Fase 1: ssj
Fase 2: ssj2
Fase 3: ssj3
Fase 4: god
Fase 5: blue
Fase 6: ui
Fase 7: mui (truco/maxform)
```

#### Ejemplo: Vegeta (fases decimales)

```
Fase 0: normal
Fase 1: ssj
Fase 2: ssj2
Fase 4: god
Fase 5: blue
Fase 6.5: blue_ev
Fase 7.5: ue (truco/maxform)
```

> [!NOTE]
> Vegeta usa fases 6.5 y 7.5 porque salta la fase 3. El sistema soporta fases decimales y transformaciones infinitas.

#### Combinaciones de Teclas para Transformación

| Entrada | Acción | Ki Requerido |
|-------|--------|-------------|
| Abajo + Puñetazo | Siguiente fase (1 > 2 > 3 > 4...) | 1+ |
| Abajo + Patada | Saltar a fase 4 | 2+ |
| Abajo + Disparo | Forma de truco (fase máxima) | 3 (máx) |
| Abajo + (A o D) + Puñetazo | Saltar a fase 2 | 2+, 3+ formas |
| Abajo + (A o D) + Patada | Saltar a fase 4 | 3+, 3+ formas |
| Abajo + L + A + D | Saltar a fase de truco máxima | 3 (máx), 3+ formas |
| Abajo + L | Fase antes de la máxima | 3 (máx), 3+ formas |
| Abajo + Cargar (mantener 0.5s) | Volver a forma base | - |

#### Restricciones de Transformación

> [!WARNING]
> - No se puede transformar sin Ki suficiente
> - El Kaioken se cancela al transformarse
> - Si `noformback` está activo, no se puede volver al estado base
> - Las formas de truco (MUI, UE, BLACK, SSFP) son fase 7 (máxima)

---

### Fórmulas de Estadísticas por Fase

#### Transformaciones Normales (Fases 1-6)

Al transformarse, las estadísticas se calculan con estas fórmulas:

```
Velocidad    = speedTx + (25 * CapForm)
Daño  = damagedTx + (8 + (2 * CapForm))
Defensa  = defenceTx + (3 + (2 * CapForm))
```

Donde `speedTx`, `damagedTx` y `defenceTx` son las estadísticas base del personaje.

**Límites:**
- Velocidad máxima: 600
- Defensa máxima: 40

**Velocidad de ataque:**
```
attackAnim = AttackAnimTx - (0.0005 * CapForm)
```
Mínimo: 0.06

#### Ejemplo: Goku (base: speed=420, damaged=97, defence=17)

| Fase | Forma | Velocidad | Daño | Defensa |
|-------|------|-------|---------|---------|
| 0 | normal | 420 | 97 | 17 |
| 1 | ssj | 445 | 107 | 22 |
| 2 | ssj2 | 470 | 109 | 24 |
| 3 | ssj3 | 495 | 111 | 26 |
| 4 | god | 520 | 113 | 28 |
| 5 | blue | 545 | 115 | 30 |
| 6 | ui | 570 | 117 | 32 |
| 7 | mui | 570 | 121 | 34 |

#### Transformaciones de Truco (Fase 7)

Las formas de truco tienen bonificaciones adicionales sobre la fórmula base:

| Forma | Velocidad | Daño Extra | Defensa Extra | Efectos Adicionales |
|------|-------|---------------|---------------|---------------------|
| MUI | base + 175 | +25 + 4 | +24 + 2 | Teletransporte, Carga Rápida, Esquivar 30-80% |
| UE | base + 175 | +27 + 4 | +20 + 4 | Teletransporte, Carga Rápida, +10% daño al golpear |
| BLACK | base + 180 | +28 + 15 | +24 + 6 | Teletransporte, Carga Máxima, defensa superior |
| SSFP | base + 125 | +24 + 2 | +16 + 2 | Carga Rápida, Sin Retroceso, personaje más grande |

> [!IMPORTANT]
> Los valores de formas de truco se aplican directamente en el código para la fase 7, NO usan la fórmula normal de fase.

---

### Sistema de Daño

#### Fórmulas de Daño

**Daño normal (golpe sin bloquear):**

```
Dmg = (damaged * Normal_Multiplier / defence) / 5
```

**Daño bloqueado (cobertura):**

```
DmgCover = (damaged * CoveredDamaged / (defence * Defence_Multiplier)) / 5
```

Donde:
- `CoveredDamaged` = multiplicador de daño cubierto (típicamente 1.5)
- `Defence_Multiplier` = multiplicador de defensa (típicamente 6)

#### Multiplicadores de Ataque

| Ataque | Multiplicador |
|--------|------------|
| Puñetazo | 1.0 |
| Patada | 1.2 |
| Ráfaga de Ki (daño) | 3.2 |
| Ráfaga de Ki (cobertura) | 2.0 |
| Embestida | 1.5 |

#### Ejemplo de Daño

El Personaje A ataca al Personaje B:
- Personaje A: damaged=107, ataca con puñetazo (multiplicador 1.0)
- Personaje B: defence=22

```
Dmg = (107 * 1.0 / 22) / 5 = 4.86 / 5 = 0.97 por golpe
```

Si B bloquea (CoveredDamaged=1.5, Defence_Multiplier=6):

```
DmgCover = (107 * 1.5 / (22 * 6)) / 5 = 1.21 / 5 = 0.24 por golpe
```

#### Daño Normalizado (para puntuación)

```
NormalizedDamage = (Dmg / (MaxLife - 10)) * 100
```

#### Barra de Vida

```
Lifebar.Width = 373 * (LifeSave / MaxLife)
```

---

### Sistema de Ki (Carga)

#### Niveles de Ki

| Nivel | Ancho de Barra | Descripción |
|-------|-----------|-------------|
| 0 | < 93 | Carga insuficiente |
| 1 | 93 - 179 | Mínimo para transformación |
| 2 | 180 - 252 | Carga media |
| 3 | 280 - 282 | Carga máxima |

#### Velocidades de Carga

| Tipo | Velocidad (px/frame) | Efecto |
|------|-------------------|--------|
| Normal | 80 | Base |
| Carga Rápida | 85 | +15% más rápido |
| Carga Máxima | 95 | +31% más rápido |
| Carga Baja | 60 | -23% más lento |

#### Auto-Carga de Android

| Tipo | Velocidad |
|------|-------|
| Normal | 25 |
| Carga Rápida | 28 |
| Carga Máxima | 31 |
| Carga Baja | 22 |

#### Consumo de Ki

| Acción | Coste |
|--------|------|
| Transformación (Puñetazo) | -94 (1 nivel) |
| Transformación (Patada) | -186 (2 niveles) |
| Transformación (Disparo) | -373 (3 niveles) |
| Teletransporte básico | -30 |
| Teletransporte con Abajo | -94 |
| Ráfaga de Ki | -50 |
| Embestida | -186 |
| TimeJump | -186 |
| Esquivar MUI | -40 |
| Esquivar | -25 |

---

### Sistema Kaioken

#### Activación

```
Abajo + Disparo x2
```

Requisitos:
- Nivel de Ki >= 1
- No estar en forma MUI
- No haber superado la fase máxima + 1

#### Efectos

| Estadística | Fórmula |
|------|---------|
| Daño | damaged + Valor |
| Defensa | defence + (Valor * 0.35) si Valor > 2 |
| Velocidad | Speed + Valor + 10 (máx 700) |
| AttackAnim | attackAnim - (Valor * 0.0005, mín 0.06) |

#### Drenaje de Vida

El Kaioken drena vida por segundo:

**Fases 1-3 (CapForm <= 3):**

```
Drenaje = ((KaioMult / defence) * 2) + (CapForm * 0.15)
```

**Fases 4+ (CapForm > 3):**

```
Drenaje = ((KaioMult / defence) * 4) + (CapForm * 0.15)
```

Donde `KaioMult` es el valor acumulado de Kaioken (ej. kaiokenx4 activado 2 veces = 8).

#### Duración y Apilamiento

> [!TIP]
> - Dura 15 segundos
> - Se puede apilar activando múltiples veces
> - Al expirar, vuelve al estado base

#### Coste de Ki por Valor

| Valor | Coste |
|-------|------|
| <= 4 | -94 |
| 5 - 10 | -186 |
| > 10 | -373 |

---

### Sistema de Esquiva

#### MUI (Ultra Instinto Dominado)

| Salud | Sin Precisión | Con Precisión |
|--------|-----------------|---------------|
| > 50% | 70% | 30% |
| 25% - 50% | 80% | 50% |
| < 25% | 50% | Desactivado |

- Coste: -40 de carga por esquiva
- No funciona si la carga <= 40
- No funciona contra BLACK en forma máxima

#### Esquivar (Normal)

| Salud | Probabilidad |
|--------|-------------|
| > 25% | 25% |
| < 25% | 45% |

- Coste: -25 de carga por esquiva
- No funciona si el oponente tiene Precisión activa
- No funciona si la carga <= 25
- No funciona contra BLACK en forma máxima

#### MasterDodge

| Salud | Probabilidad |
|--------|-------------|
| > 25% | 100% |
| < 25% | 95% |

- Coste: Ninguno
- No funciona si la carga <= 13

#### Precisión (Limitador de Esquiva)

> [!CAUTION]
> Precisión es un truco que reduce la capacidad de esquiva del oponente:
> - Reduce las probabilidades de MUI y Esquivar
> - Desactiva la esquiva si la salud < 25%
> - No afecta a MasterDodge

---

### Sistema de Teletransporte

#### Activación

```
Izquierda x2 o Derecha x2 (doble toque)
```

Con Abajo presionado:

```
Abajo + Izquierda x2 o Abajo + Derecha x2
```

#### Requisitos

- Nivel de Ki >= 1
- Carga >= 30
- Una de estas condiciones:
  - Truco `teleport` activo
  - En forma máxima con MUI, UE, BLACK o SSFP
  - En fase >= 4

#### Efectos

| Modo | Distancia | Coste |
|------|----------|------|
| Sin Abajo | 45 * 3 = 135 | -30 |
| Con Abajo | hasta oponente + 50 | -94 |

#### Enfriamiento

0.3 segundos entre teletransportes

---

### Sistema de Embestida

#### Activación

```
Botón de Embestida (O)
```

#### Requisitos

- Nivel de Ki >= 2

#### Coste

-186 de carga

#### Embestida de Choque

> [!NOTE]
> Si ambos jugadores presionan Embestida dentro de 0.2 segundos:
> - Se activa la Embestida de Choque
> - Ambos se acercan a distancia 50 (55 con UpDim)
> - Intercambian golpes durante 5 segundos
> - El ganador inflige daño extra

**Golpes normales durante el choque:**

```
dmg1 = (Damaged1 * 0.5 / Defence2) / 5
dmg2 = (Damaged2 * 0.5 / Defence1) / 5
```

**Ganador del choque:**

```
dmgFinal = (DamagedGanador * 0.8 / DefencePerdedor)
```

---

### Sistema TimeJump

#### Activación

```
Abajo + Puñetazo x2
```

#### Requisitos

- Truco `TimeJump` activo
- Nivel de Ki >= 2

#### Efectos

- Congela al oponente durante 5 segundos
- El oponente no puede moverse ni atacar
- El oponente SÍ puede bloquear
- El fondo se vuelve escala de grises
- Brillo púrpura en el personaje activo
- La barra de carga del oponente se congela

#### Coste

-186 de carga

---

### Sistema de Combos

#### Contador de Combo

- Se incrementa con cada golpe exitoso
- Se reinicia después de 2 segundos sin golpes
- Se muestra en pantalla como "X Hits" o "X Golpes"

#### Golpe Crítico

Se activa cuando `comboCounter > 1`:
- Aplica retroceso al oponente
- Retroceso horizontal: `50 + sqrt(comboCounter) * 10`
- Retroceso vertical: `30 + sqrt(comboCounter) * 8`
- El oponente entra en estado crítico (no puede moverse)

#### Retroceso

```
dx = knockbackPowerX (en dirección del golpe)
dy = -knockbackPowerY * 1.2 (hacia arriba)
```

Desaceleración: -15 por cuadro hasta llegar a 0

#### Retroceso por Tipo

| Tipo | Retroceso X | Retroceso Y |
|------|-------------|-------------|
| Golpe normal (crítico) | 50 + sqrt(combo) * 10 | 30 + sqrt(combo) * 8 |
| Ráfaga de Ki | 350 | 160 |
| Ráfaga de Ki (cobertura) | 350 | 130 |

#### Anti-Retroceso

> [!TIP]
> Los trucos `Recoilless` y `SSFP` (en forma ssfp) anulan el retroceso.

---

### Puntuación y Rangos

#### Cálculo de Puntuación

```
NormalizedDamage = (Dmg / (MaxLife - 10)) * 100
ScoreAcum = ScoreAcum + NormalizedDamage * 1000
```

#### Bonificaciones

- Bono de Combo: ComboCount * 50
- Bono de Eficiencia: (1 - LifeSaveRatio) * 1000

#### Rangos

| Puntuación Promedio | Rango |
|---------------|------|
| >= 250,000 | GOD |
| >= 135,000 | Z+ |
| >= 115,000 | Z |
| >= 95,000 | S+ |
| >= 80,000 | S |
| >= 65,000 | A |
| >= 50,000 | B |
| >= 35,000 | C |
| < 35,000 | D |

---

### Colores de Barra de Carga por Transformación

| Forma | Color Frente | Color Fondo |
|------|-------------|------------|
| SSJ / Golden / Perfect | Blanco | Naranja |
| MUI | Blanco | Gris |
| UI / Definitivo | Blanco | Azul |
| UE / Ultra Ego | Rosa | Púrpura Oscuro |
| Full Power / Red | Rosa Claro | Rojo |
| God / SSJ God | Rosa Claro | Rojo Claro |
| Rose / SSJ Rose | Rosa Claro | Rosa |
| Blue / SSJ Blue | Azul Claro | Azul |
| Blue Evolution | Azul Medio | Azul Oscuro |
| Black | Púrpura Oscuro | Gris |
| SSJ Legendario / SSFP | Amarillo Claro | Verde Lima |
| Beast | Blanco | Púrpura |
| Orange | Naranja | Amarillo |
| Corrupted | Púrpura Claro | Púrpura Oscuro |

---

### Gravedad y Movimiento

#### Constantes

```
JumpVelocity = -500
Gravity = 1000
```

#### Límites de Pantalla

| Condición | Límite Y |
|-----------|---------|
| Normal | 301 |
| Con UpDim activo | 265 |
| Con SSFP (forma ssfp) | 260 |

#### Doble Salto

- Primer salto: dy = JumpVelocity
- Doble salto: dy = JumpVelocity (solo si dy > JumpVelocity * 0.5)

---

### Sistema de Rondas

| Ajuste | Predeterminado |
|---------|---------|
| Rondas | 2 |
| Tiempo de Juego | Ilimitado |
| Transformación Instantánea | true |
| Efecto de Flash | true |

---

## Referencia de Trucos

### Trucos de Forma

| Truco | Fase | Efecto |
|-------|-------|--------|
| MUI | 7 | +25 daño, +24 defensa, teletransporte, carga rápida, esquivar 30-80% |
| UE | 7 | +27 daño, +20 defensa, teletransporte, carga rápida, +10% daño al golpear, se destransforma al <15% salud |
| BLACK | 7 | +28 daño, +24 defensa, teletransporte, carga máxima, defensa superior |
| SSFP | 7 | +24 daño, +16 defensa, carga rápida, sin retroceso, personaje más grande (161x149) |

### Trucos de Movimiento

| Truco | Efecto |
|-------|--------|
| teleport | Permite teletransportarse en estado base con Ki >= 1 |
| fixK | Ajusta el sprite de patada si es muy ancho |
| updim | Aumenta las dimensiones del personaje (124x141). `updim:phase=X` solo en fase X |
| SSFP | Personaje más grande que updim (161x149), +20-30% daño/defensa |

### Trucos de Carga

| Truco | Efecto |
|-------|--------|
| fastcharge | +15% velocidad de carga (85 px/frame) |
| Maxcharge | +31% velocidad de carga (95 px/frame) |
| lowercharge | -23% velocidad de carga (60 px/frame) |
| Android | Auto-carga, no puede cargar manualmente |

### Trucos de Combate

| Truco | Efecto |
|-------|--------|
| KaiokenxN | Multiplicador N: +N daño, +(N*0.35) defensa (si N>2), +(N+10) velocidad |
| TimeJump | Congela oponente 5 segundos (Abajo + Puñetazo x2, 2 niveles) |
| Dodge | Esquivar 25-45% con coste de carga |
| MasterDodge | Esquivar 95-100% sin coste |
| Accuracy | Reduce la esquiva del oponente |
| Recoilless | Reduce daño al bloquear, anula retroceso |
| noformback | No puede volver a la forma base |
| NoShot | No puede lanzar ráfagas de Ki. `NoShot=phase:X` solo en fase X |
| RecoverLife | Regenera salud periódicamente. `RecoverLife=X` regenera X por tick |

---

## Controles

### Controles Básicos

| Acción | Teclas |
|--------|------|
| Movimiento | Flechas o WASD |
| Saltar | Flecha arriba / W |
| Puñetazo | Configurable |
| Patada | Configurable |
| Ráfaga de Ki | Ataque de proyectil de energía |
| Cargar | Mantener para llenar barra de energía |
| Guardar | Abajo + tecla de bloqueo |
| Cubrirse | Botón de cobertura (E) |
| Embestida | Botón de embestida (O) |

### Combinaciones de Habilidades

| Entrada | Acción | Ki Requerido |
|-------|--------|-------------|
| Abajo + Puñetazo | Transformar a siguiente fase | 1+ |
| Abajo + Patada | Saltar a fase 4 | 2+ |
| Abajo + Disparo | Transformar a forma de truco | 3 |
| Abajo + (A o D) + Puñetazo | Saltar a fase 2 | 2+, 3+ formas |
| Abajo + (A o D) + Patada | Saltar a fase 4 | 3+, 3+ formas |
| Abajo + L + A + D | Saltar a fase de truco máxima | 3, 3+ formas |
| Abajo + Cargar (mantener 0.5s) | Volver a forma base | - |
| Abajo + Disparo x2 | Activar Kaioken | 1+ |
| Abajo + Puñetazo x2 | Activar TimeJump | 2+ |
| Izquierda/Derecha x2 | Teletransporte | 1+ |
| Abajo + Izquierda/Derecha | Teletransportar al oponente | 1+ |
| Botón de Embestida (O) | Embestida | 2+ |
| Botón de Cobertura (E) | Cubrirse | - |

---

## Requisitos

### Software

- **Microsoft Office 2016 o superior** (PowerPoint con soporte de macros habilitado)
- **Sistema operativo Windows** (requerido para APIs del sistema: teclado, sonido, temporización)
- **Python 3.x** (para funcionalidad del bot)

### Dependencias de Python

```
keyboard>=0.13.5
psutil>=7.1.3
```

Bibliotecas integradas utilizadas: `os`, `json`, `threading`, `random`, `time`

### Configuración Adicional

> [!IMPORTANT]
> 1. Instala las fuentes de la carpeta `/font` para el display HUD correcto
> 2. Habilita las macros en la configuración de seguridad de PowerPoint

---

## Requisitos del Sistema

| Componente | Mínimo | Recomendado |
|-----------|---------|-------------|
| CPU | Dual-core 2.0 GHz | Quad-core 2.5 GHz+ |
| RAM | 4 GB | 8 GB |
| GPU | Gráficos integrados | Integrados/dedicados modernos |
| Almacenamiento | 1 GB libre | 2 GB+ |
| SO | Windows 7+ | Windows 10/11 |

---

## Cómo Jugar

### Instalación

```bash
git clone https://github.com/yourusername/ultimate-warriors.git
cd ultimate-warriors
pip install -r requirements.txt
```

Luego instala las fuentes (clic derecho en las fuentes de la carpeta `/font`, selecciona "Instalar para todos los usuarios").

### Ejecutar el Juego

1. Abre `Game.ppsm` en PowerPoint
2. Habilita las macros cuando se te solicite
3. Inicia la presentación (F5)
4. Selecciona tu personaje y escenario
5. ¡Pelea!

---

## Creación de Personajes

¿Quieres crear tu propio personaje personalizado? Consulta la guía completa:

- **[Character Creation Guide (English)](docs/Character_creation_guide.md)**
- **[Guía para Crear un Personaje (Español)](docs/Character_creation_guide_ES.md)**

---

## Licencia

Este proyecto es un juego fan de Dragon Ball hecho con amor para la comunidad.

---

*Hecho con PowerPoint VBA. Sí, en serio.*
