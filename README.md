<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/Language-English-blue?style=for-the-badge" alt="English"></a>
  <a href="README_ES.md"><img src="https://img.shields.io/badge/Idioma-Español-red?style=for-the-badge" alt="Español"></a>
</p>

# Ultimate Warriors

### Dragon Ball 2D Fighting Game in PowerPoint

> VBA-Powered | Python Bot Support | Windows | PowerPoint 2016+

A full-featured 2D fighting game built entirely in PowerPoint using VBA. Complete with transformations, combos, special moves, and an intelligent Python bot.

![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)
![Version](https://img.shields.io/badge/Version-1.0.0-blue?style=flat-square)
![Genre](https://img.shields.io/badge/Genre-Fighting-red?style=flat-square)

---

## Launch Video

<p align="center">
  <a href="https://www.youtube.com/watch?v=_dMCui9MIOw">
    <img src="https://img.youtube.com/vi/_dMCui9MIOw/maxresdefault.jpg" alt="Ultimate Warriors - Launch Video" width="720">
  </a>
</p>

<p align="center">
  <a href="https://www.youtube.com/watch?v=_dMCui9MIOw">Watch on YouTube</a>
</p>

> [!NOTE]
> This is the official launch video for Ultimate Warriors. Watch the full gameplay and features on [YouTube](https://www.youtube.com/watch?v=_dMCui9MIOw).

---

## Features

### Combat System
- 2D fighting mechanics: movement, jumps, attacks, Ki blasts
- Box collision detection with precise hitbox & hurtbox system
- Guard, tackle, and cover system
- Combo calculator with damage tracking and scoring
- Dragon rush: special combo finisher
- Time jump: slow-motion mechanic
- Knockback system with critical hit states

### Transformation System
- Up to 6 normal phases + 1 cheat phase per character
- Dynamic stat scaling per phase (speed, damage, defense)
- Kaioken modes with configurable multiplier and life drain
- Visual effects: auras, glows, and transformation animations
- Teleport system: instant position swap
- 25+ character cheats with unique abilities

### Advanced Features
- Sprite animation system with frame-by-frame rendering and caching
- 22 JSON-defined stages with unique properties
- Round-based scoring with points, ranks, and victory screens
- Input buffer system for fighting game-style combo detection
- Dynamic character shadows
- Gravity and physics system (JumpVelocity=-500, Gravity=1000)

### AI & Customization
- Python bot integration with real-time AI opponent
- JSON character data for easy creation and modification
- Custom controls with remappable key bindings for P1 and P2
- Sound system with music and SFX via Windows APIs
- Bilingual UI: Spanish and English localization

---

## Technical Highlights

### Game Engine (dbxwCore)
- VBA game loop with DeltaTime synchronization via `GetTickCount`
- State management for characters and gameplay
- Collision physics with gravity and screen boundaries
- Module architecture for maintainable code
- Windows API integration for keyboard (`GetAsyncKeyState`) and sound (`winmm.dll`)

### Data-Driven Design
- JSON configuration for characters, stages, controls, settings
- Sprite system with dynamic loading and frame caching
- Settings persistence with save/load functionality
- Bot communication via real-time JSON file exchange
- Custom JSON parser (PPTGames VBAJSON v1.13)

---

## Project Structure

```
Ultimate-Warriors/
├── Game.ppsm                    # Main PowerPoint game (macro-enabled)
├── README.md
├── requirements.txt             # Python dependencies
│
├── chars/                       # 30 character folders
│   ├── Goku/char.json
│   ├── Vegeta/char.json
│   └── ... (30 characters)
│
├── stages/                      # 22 stage folders
│   ├── World Tournament Stage/
│   ├── Planet Namek/
│   └── ... (22 stages)
│
├── sound/                       # 25 MP3 music tracks
├── font/                        # Custom fonts (HUD display)
│   ├── Great Fighter Demo.otf
│   ├── Great Fighter Demo.ttf
│   ├── PIZZADUDEPOINTERS.ttf
│   └── Super Squad.ttf
│
├── data/
│   ├── version.data             # Version info
│   ├── Changelog.txt            # Changelog
│   ├── Controls.json            # Control mappings
│   ├── Language.json            # Bilingual localization (ES/EN)
│   ├── Settings.json            # Game settings
│   ├── style.css                # Sprite gallery UI
│   ├── index.js                 # Gallery logic
│   ├── index_credits.html       # Credits page
│   ├── icon.ico                 # App icon
│   ├── icon.png                 # App icon (PNG)
│   ├── sound_effects/           # 44 WAV/MP3 SFX files
│   ├── resources/
│   │   ├── CharEffects/         # 106 aura/effect PNG sprites
│   │   ├── GameEffects/         # 46 explosion/blizzard PNG sprites
│   │   ├── menu/
│   │   │   ├── Anim/            # Menu animations
│   │   │   ├── credits.png
│   │   │   ├── main.png
│   │   │   ├── selection.png
│   │   │   └── settings.png
│   │   ├── coconut.png
│   │   ├── ico_char_null.png
│   │   ├── null.png
│   │   └── pre_stage_null.png
│   └── bot/                     # Python AI bot (modular)
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

## Characters (30)

| Character | Base Form | Transformations | Special Abilities |
|-----------|-----------|-----------------|-------------------|
| Goku | Normal | SSJ, SSJ2, SSJ3, God, Blue, UI (6 phases) | MUI, Kaioken x4, Teleport, Dodge |
| Vegeta | Normal | SSJ, SSJ2, God, Blue, Blue Evolution (5+ phases) | Ultra Ego, Teleport |
| Gohan | - | - | - |
| Kid Gohan | - | - | - |
| Piccolo | - | - | - |
| Vegetto | - | - | - |
| Gogeta | - | - | - |
| Gotenks | - | - | - |
| Trunks | - | - | - |
| Bardock | - | - | - |
| Broly | Rage | SSJ (phase 4) | Updim, SSFP, No Form Back, Teleport |
| Freezer | Normal | Golden (phase 5) | Black, Teleport |
| Cell | Perfect | - | Teleport |
| Cooler | - | - | - |
| Android 17 | - | - | - |
| Android 18 | - | - | - |
| Android 21 | - | - | - |
| Kid Buu | - | - | - |
| Super Buu (Gohan) | - | - | - |
| Hit | - | - | - |
| Jiren | Normal | Full Power (phase 2) | Teleport, No Form Back, Fast Charge |
| Kefla | - | - | - |
| Beerus | Base | - | Teleport, Fast Charge, Accuracy |
| Zamasu | - | - | - |
| Black | - | - | - |
| Janemba | - | - | - |
| Moro | - | - | - |
| Granola | - | - | - |
| Videl | - | - | - |
| Alex | Normal | SSJ, God, Blue | Fast Charge, Teleport, Kaioken x4, Ultra Ego |

---

## Stages (22)

Archipelago, Cell Games Arena, Destroyed Planet Namek, Future in Ruins, Glacier, Hell, Hyperbolic Time Chamber, Kami Lookout, Open Field, Plains, Planet Namek, Power Tree, Rocky Site, Sky, Space (Earth), Space (Planet Vegeta), Supreme Kai World, The Nameless Planet, Tournament of Power Arena, Underground Lake, Westland, World Tournament Stage

---

## Game Mechanics

### Base Character Stats

Each character defines its base stats in `char.json`:

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

| Stat | Description |
|------|-------------|
| `speed` | Horizontal movement speed |
| `life` | Maximum health |
| `damaged` | Base attack power |
| `defence` | Reduces incoming damage |
| `Attack Speed` | Attack animation speed (lower = faster) |
| `Stand Speed` | Idle animation speed |
| `Taunt Speed` | Taunt animation speed |
| `Aura Speed` | Aura animation speed |

#### Character Stat Examples

| Character | Speed | Life | Damaged | Defence | Attack Speed |
|-----------|-------|------|---------|---------|--------------|
| Goku | 420 | 100 | 97 | 17 | - |
| Vegeta | 420 | 100 | 97 | 17 | - |
| Broly | 500 | 100 | 110 | 18 | 7.5 |
| Beerus | 500 | 150 | 135 | 20 | 6 |

---

### Transformation System

Transformations are activated with key combinations and consume Ki energy levels. The system uses an internal counter called `CapForm` that indicates the current phase.

#### Phase Structure

Each character can have up to 6 normal phases + 1 cheat phase:

```
Phase 0: Base state
Phase 1: First transformation (e.g. SSJ)
Phase 2: Second transformation (e.g. SSJ2)
Phase 3: Third transformation (e.g. SSJ3)
Phase 4: Fourth transformation (e.g. God)
Phase 5: Fifth transformation (e.g. Blue)
Phase 6: Sixth transformation (e.g. UI)
Phase 7: Cheat form (MUI, UE, BLACK, or SSFP)
```

#### Example: Goku

```
Phase 0: normal
Phase 1: ssj
Phase 2: ssj2
Phase 3: ssj3
Phase 4: god
Phase 5: blue
Phase 6: ui
Phase 7: mui (cheat)
```

#### Example: Vegeta

```
Phase 0: normal
Phase 1: ssj
Phase 2: ssj2
Phase 4: god
Phase 5: blue
Phase 6.5: blue_ev
Phase 7.5: ue (cheat)
```

> [!NOTE]
> Vegeta uses phase 6.5 and 7.5 because it skips phase 3. The system supports decimal phases.

#### Transformation Key Combinations

| Input | Action | Ki Required |
|-------|--------|-------------|
| Down + Punch | Next phase (1 > 2 > 3 > 4...) | 1+ |
| Down + Kick | Jump to phase 4 | 2+ |
| Down + Shot | Cheat form (max phase) | 3 (max) |
| Down + (A or D) + Punch | Jump to phase 2 | 2+, 3+ forms |
| Down + (A or D) + Kick | Jump to phase 4 | 3+, 3+ forms |
| Down + L + A + D | Jump to max cheat phase | 3 (max), 3+ forms |
| Down + L | Phase before max | 3 (max), 3+ forms |
| Down + Charge (hold 0.5s) | Return to base form | - |

#### Transformation Restrictions

> [!WARNING]
> - Cannot transform without sufficient Ki
> - Kaioken cancels on transformation
> - If `noformback` is active, cannot return to base state
> - Cheat forms (MUI, UE, BLACK, SSFP) are phase 7 (maximum)

---

### Stat Formulas Per Phase

#### Normal Transformations (Phases 1-6)

On transformation, stats are calculated with these formulas:

```
Speed    = speedTx + (25 * CapForm)
Damaged  = damagedTx + (8 + (2 * CapForm))
Defence  = defenceTx + (3 + (2 * CapForm))
```

Where `speedTx`, `damagedTx`, and `defenceTx` are the character's base stats.

**Caps:**
- Speed maximum: 600
- Defence maximum: 40

**Attack speed:**
```
attackAnim = AttackAnimTx - (0.0005 * CapForm)
```
Minimum: 0.06

#### Example: Goku (base: speed=420, damaged=97, defence=17)

| Phase | Form | Speed | Damaged | Defence |
|-------|------|-------|---------|---------|
| 0 | normal | 420 | 97 | 17 |
| 1 | ssj | 445 | 107 | 22 |
| 2 | ssj2 | 470 | 109 | 24 |
| 3 | ssj3 | 495 | 111 | 26 |
| 4 | god | 520 | 113 | 28 |
| 5 | blue | 545 | 115 | 30 |
| 6 | ui | 570 | 117 | 32 |
| 7 | mui | 570 | 121 | 34 |

#### Cheat Transformations (Phase 7)

Cheat forms have additional bonuses over the base formula:

| Form | Speed | Damaged Extra | Defence Extra | Additional Effects |
|------|-------|---------------|---------------|---------------------|
| MUI | base + 175 | +25 + 4 | +24 + 2 | Teleport, Fast Charge, Dodge 30-80% |
| UE | base + 175 | +27 + 4 | +20 + 4 | Teleport, Fast Charge, +10% damage on hit |
| BLACK | base + 180 | +28 + 15 | +24 + 6 | Teleport, Max Charge, superior defence |
| SSFP | base + 125 | +24 + 2 | +16 + 2 | Fast Charge, Recoilless, larger character |

> [!IMPORTANT]
> Cheat form values are applied directly in code for phase 7, they do NOT use the normal phase formula.

---

### Damage System

#### Damage Formulas

**Normal damage (hit without block):**

```
Dmg = (damaged * Normal_Multiplier / defence) / 5
```

**Blocked damage (cover up):**

```
DmgCover = (damaged * CoveredDamaged / (defence * Defence_Multiplier)) / 5
```

Where:
- `CoveredDamaged` = covered damage multiplier (typically 1.5)
- `Defence_Multiplier` = defense multiplier (typically 6)

#### Attack Multipliers

| Attack | Multiplier |
|--------|------------|
| Punch | 1.0 |
| Kick | 1.2 |
| Ki Blast (damage) | 3.2 |
| Ki Blast (cover) | 2.0 |
| Tackle | 1.5 |

#### Damage Example

Character A attacks Character B:
- Character A: damaged=107, attacks with punch (multiplier 1.0)
- Character B: defence=22

```
Dmg = (107 * 1.0 / 22) / 5 = 4.86 / 5 = 0.97 per hit
```

If B blocks (CoveredDamaged=1.5, Defence_Multiplier=6):

```
DmgCover = (107 * 1.5 / (22 * 6)) / 5 = 1.21 / 5 = 0.24 per hit
```

#### Normalized Damage (for scoring)

```
NormalizedDamage = (Dmg / (MaxLife - 10)) * 100
```

#### Life Bar

```
Lifebar.Width = 373 * (LifeSave / MaxLife)
```

---

### Ki (Charge) System

#### Ki Levels

| Level | Bar Width | Description |
|-------|-----------|-------------|
| 0 | < 93 | Insufficient charge |
| 1 | 93 - 179 | Minimum for transformation |
| 2 | 180 - 252 | Medium charge |
| 3 | 280 - 282 | Maximum charge |

#### Charge Speeds

| Type | Speed (px/frame) | Effect |
|------|-------------------|--------|
| Normal | 80 | Base |
| Fast Charge | 85 | +15% faster |
| Max Charge | 95 | +31% faster |
| Lower Charge | 60 | -23% slower |

#### Android Auto-Charge

| Type | Speed |
|------|-------|
| Normal | 25 |
| Fast Charge | 28 |
| Max Charge | 31 |
| Lower Charge | 22 |

#### Ki Consumption

| Action | Cost |
|--------|------|
| Transformation (Punch) | -94 (1 level) |
| Transformation (Kick) | -186 (2 levels) |
| Transformation (Shot) | -373 (3 levels) |
| Basic teleport | -30 |
| Down teleport | -94 |
| Ki Blast | -50 |
| Tackle | -186 |
| TimeJump | -186 |
| MUI dodge | -40 |
| Dodge | -25 |

---

### Kaioken System

#### Activation

```
Down + Shot x2
```

Requirements:
- Ki level >= 1
- Not in MUI form
- Has not exceeded max phase + 1

#### Effects

| Stat | Formula |
|------|---------|
| Damaged | damaged + Valor |
| Defence | defence + (Valor * 0.35) if Valor > 2 |
| Speed | Speed + Valor + 10 (max 700) |
| AttackAnim | attackAnim - (Valor * 0.0005, min 0.06) |

#### Life Drain

The Kaioken drains life per second:

**Phases 1-3 (CapForm <= 3):**

```
Drain = ((KaioMult / defence) * 2) + (CapForm * 0.15)
```

**Phases 4+ (CapForm > 3):**

```
Drain = ((KaioMult / defence) * 4) + (CapForm * 0.15)
```

Where `KaioMult` is the accumulated Kaioken value (e.g. kaiokenx4 activated 2 times = 8).

#### Duration and Stacking

> [!TIP]
> - Lasts 15 seconds
> - Can be stacked by activating multiple times
> - On expiry, returns to base state

#### Ki Cost by Value

| Value | Cost |
|-------|------|
| <= 4 | -94 |
| 5 - 10 | -186 |
| > 10 | -373 |

---

### Dodge System

#### MUI (Mastered Ultra Instinct)

| Health | Without Accuracy | With Accuracy |
|--------|-----------------|---------------|
| > 50% | 70% | 30% |
| 25% - 50% | 80% | 50% |
| < 25% | 50% | Disabled |

- Cost: -40 charge per dodge
- Does not work if charge <= 40
- Does not work against BLACK in max form

#### Dodge (Normal)

| Health | Probability |
|--------|-------------|
| > 25% | 25% |
| < 25% | 45% |

- Cost: -25 charge per dodge
- Does not work if opponent has Accuracy active
- Does not work if charge <= 25
- Does not work against BLACK in max form

#### MasterDodge

| Health | Probability |
|--------|-------------|
| > 25% | 100% |
| < 25% | 95% |

- Cost: None
- Does not work if charge <= 13

#### Accuracy (Dodge Limiter)

> [!CAUTION]
> Accuracy is a cheat that reduces the opponent's dodge capability:
> - Reduces MUI and Dodge probabilities
> - Disables dodge if health < 25%
> - Does not affect MasterDodge

---

### Teleport System

#### Activation

```
Left x2 or Right x2 (double tap)
```

With Down pressed:

```
Down + Left x2 or Down + Right x2
```

#### Requirements

- Ki level >= 1
- Charge >= 30
- One of these conditions:
  - Cheat `teleport` active
  - In max form with MUI, UE, BLACK, or SSFP
  - In phase >= 4

#### Effects

| Mode | Distance | Cost |
|------|----------|------|
| Without Down | 45 * 3 = 135 | -30 |
| With Down | up to opponent + 50 | -94 |

#### Cooldown

0.3 seconds between teleports

---

### Tackle System

#### Activation

```
Tackle Button (O)
```

#### Requirements

- Ki level >= 2

#### Cost

-186 charge

#### Clash Tackle

> [!NOTE]
> If both players press Tackle within 0.2 seconds:
> - Clash Tackle activates
> - Both approach to distance 50 (55 with UpDim)
> - They exchange hits for 5 seconds
> - The winner deals extra damage

**Normal hits during clash:**

```
dmg1 = (Damaged1 * 0.5 / Defence2) / 5
dmg2 = (Damaged2 * 0.5 / Defence1) / 5
```

**Clash winner:**

```
dmgFinal = (DamagedGanador * 0.8 / DefencePerdedor)
```

---

### TimeJump System

#### Activation

```
Down + Punch x2
```

#### Requirements

- Cheat `TimeJump` active
- Ki level >= 2

#### Effects

- Freezes opponent for 5 seconds
- Opponent cannot move or attack
- Opponent CAN block
- Background turns grayscale
- Purple glow on active character
- Opponent's charge bar freezes

#### Cost

-186 charge

---

### Combo System

#### Combo Counter

- Increments with each successful hit
- Resets after 2 seconds without hits
- Displayed on screen as "X Hits" or "X Golpes"

#### Critical Hit

Activates when `comboCounter > 1`:
- Applies knockback to opponent
- Horizontal knockback: `50 + sqrt(comboCounter) * 10`
- Vertical knockback: `30 + sqrt(comboCounter) * 8`
- Opponent enters critical state (cannot move)

#### Knockback

```
dx = knockbackPowerX (in hit direction)
dy = -knockbackPowerY * 1.2 (upward)
```

Deceleration: -15 per frame until reaching 0

#### Knockback by Type

| Type | Knockback X | Knockback Y |
|------|-------------|-------------|
| Normal hit (critical) | 50 + sqrt(combo) * 10 | 30 + sqrt(combo) * 8 |
| Ki Blast | 350 | 160 |
| Ki Blast (cover) | 350 | 130 |

#### Anti-Knockback

> [!TIP]
> Cheats `Recoilless` and `SSFP` (in ssfp form) negate knockback.

---

### Scoring and Ranking

#### Score Calculation

```
NormalizedDamage = (Dmg / (MaxLife - 10)) * 100
ScoreAcum = ScoreAcum + NormalizedDamage * 1000
```

#### Bonifications

- Combo Bonus: ComboCount * 50
- Efficiency Bonus: (1 - LifeSaveRatio) * 1000

#### Ranks

| Average Score | Rank |
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

### Charge Bar Colors Per Transformation

| Form | Front Color | Back Color |
|------|-------------|------------|
| SSJ / Golden / Perfect | White | Orange |
| MUI | White | Gray |
| UI / Definitivo | White | Blue |
| UE / Ultra Ego | Pink | Dark Purple |
| Full Power / Red | Light Pink | Red |
| God / SSJ God | Light Pink | Light Red |
| Rose / SSJ Rose | Light Pink | Pink |
| Blue / SSJ Blue | Light Blue | Blue |
| Blue Evolution | Medium Blue | Dark Blue |
| Black | Dark Purple | Gray |
| SSJ Legendario / SSFP | Light Yellow | Lime Green |
| Beast | White | Purple |
| Orange | Orange | Yellow |
| Corrupted | Light Purple | Dark Purple |

---

### Gravity and Movement

#### Constants

```
JumpVelocity = -500
Gravity = 1000
```

#### Screen Limits

| Condition | Limit Y |
|-----------|---------|
| Normal | 301 |
| With UpDim active | 265 |
| With SSFP (ssfp form) | 260 |

#### Double Jump

- First jump: dy = JumpVelocity
- Double jump: dy = JumpVelocity (only if dy > JumpVelocity * 0.5)

---

### Round System

| Setting | Default |
|---------|---------|
| Rounds | 2 |
| Game Time | Unlimited |
| Instant Transformation | true |
| Flash Effect | true |

---

## Cheats Reference

### Form Cheats

| Cheat | Phase | Effect |
|-------|-------|--------|
| MUI | 7 | +25 damaged, +24 defence, teleport, fast charge, dodge 30-80% |
| UE | 7 | +27 damaged, +20 defence, teleport, fast charge, +10% damage on hit, de-transforms at <15% health |
| BLACK | 7 | +28 damaged, +24 defence, teleport, max charge, superior defence |
| SSFP | 7 | +24 damaged, +16 defence, fast charge, recoilless, larger character (161x149) |

### Movement Cheats

| Cheat | Effect |
|-------|--------|
| teleport | Allows teleporting in base state with Ki >= 1 |
| fixJ | Adjusts punch sprite if too wide |
| fixK | Adjusts kick sprite if too wide |
| updim | Increases character dimensions (124x141). `updim:phase=X` only in phase X |
| SSFP | Larger character than updim (161x149), +20-30% damaged/defence |

### Charge Cheats

| Cheat | Effect |
|-------|--------|
| fastcharge | +15% charge speed (85 px/frame) |
| Maxcharge | +31% charge speed (95 px/frame) |
| lowercharge | -23% charge speed (60 px/frame) |
| Android | Auto-charge, cannot charge manually |

### Combat Cheats

| Cheat | Effect |
|-------|--------|
| KaiokenxN | Multiplier N: +N damaged, +(N*0.35) defence (if N>2), +(N+10) speed |
| TimeJump | Freezes opponent 5 seconds (Down + Punch x2, 2 levels) |
| Dodge | Dodge 25-45% with charge cost |
| MasterDodge | Dodge 95-100% without cost |
| Accuracy | Reduces opponent's dodge |
| Recoilless | Reduces damage on block, negates knockback |
| noformback | Cannot return to base state |
| NoShot | Cannot fire Ki blasts. `NoShot=phase:X` only in phase X |
| RecoverLife | Regenerates health periodically. `RecoverLife=X` regenerates X per tick |

---

## Controls

### Basic Controls

| Action | Keys |
|--------|------|
| Movement | Arrow keys or WASD |
| Jump | Up arrow / W |
| Punch | Configurable |
| Kick | Configurable |
| Ki Blast | Energy projectile attack |
| Charge | Hold to build energy bar |
| Guard | Down + block key |
| Cover Up | Cover button (E) |
| Tackle | Tackle button (O) |

### Ability Combinations

| Input | Action | Ki Required |
|-------|--------|-------------|
| Down + Punch | Transform to next phase | 1+ |
| Down + Kick | Jump to phase 4 | 2+ |
| Down + Shot | Transform to cheat form | 3 |
| Down + (A or D) + Punch | Jump to phase 2 | 2+, 3+ forms |
| Down + (A or D) + Kick | Jump to phase 4 | 3+, 3+ forms |
| Down + L + A + D | Jump to max cheat phase | 3, 3+ forms |
| Down + Charge (hold 0.5s) | Return to base form | - |
| Down + Shot x2 | Activate Kaioken | 1+ |
| Down + Punch x2 | Activate TimeJump | 2+ |
| Left/Right x2 | Teleport | 1+ |
| Down + Left/Right | Teleport to opponent | 1+ |
| Tackle button (O) | Tackle | 2+ |
| Cover button (E) | Cover up | - |

---

## Requirements

### Software

- **Microsoft Office 2016 or higher** (PowerPoint with macro support enabled)
- **Windows OS** (required for system APIs: keyboard, sound, timing)
- **Python 3.x** (for bot functionality)

### Python Dependencies

```
keyboard>=0.13.5
psutil>=7.1.3
```

Built-in libraries used: `os`, `json`, `threading`, `random`, `time`

### Additional Setup

> [!IMPORTANT]
> 1. Install fonts from the `/font` folder for proper HUD display
> 2. Enable macros in PowerPoint security settings

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | Dual-core 2.0 GHz | Quad-core 2.5 GHz+ |
| RAM | 4 GB | 8 GB |
| GPU | Integrated graphics | Modern integrated/dedicated |
| Storage | 1 GB free space | 2 GB+ |
| OS | Windows 7+ | Windows 10/11 |

---

## How to Play

### Installation

```bash
git clone https://github.com/yourusername/ultimate-warriors.git
cd ultimate-warriors
pip install -r requirements.txt
```

Then install fonts (right-click fonts in `/font` folder, select "Install for all users").

### Running the Game

1. Open `Game.ppsm` in PowerPoint
2. Enable macros when prompted
3. Start the slideshow (F5)
4. Select your character and stage
5. Fight!

---

## Character Creation

Want to create your own custom character? See the full guide:

- **[Character Creation Guide (English)](Character_creation_guide.md)**
- **[Guía para Crear un Personaje (Español)](Character_creation_guide_ES.md)**

---

## License

This project is a Dragon Ball fan game made with love for the community.

---

*Built with PowerPoint VBA. Yes, really.*
