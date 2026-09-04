# Character Creation Guide - Ultimate Warriors

Complete step-by-step guide to create a custom character and import it into the game.

---

## Prerequisites

- Character sprites in **PNG with transparent background**
- Text editor to create the `char.json` (VS Code, Notepad++, etc.)
- The game **Game.ppsm** open in PowerPoint with macros enabled

---

## Step 1: Create the Folder Structure

Each character lives inside the `chars/` folder. The structure must be exactly like this:

```
chars/
└── MyCharacter/              # Character folder name
    ├── char.json             # Configuration file (REQUIRED)
    ├── ico.png               # Icon for character selection (recommended)
    ├── normal/               # Base form (REQUIRED folder)
    │   ├── stand.png         # Idle/standing sprite
    │   ├── punch_1.png       # Punch sprites (sequence)
    │   ├── kick_1.png        # Kick sprites (sequence)
    │   ├── damaged_1.png     # Damage received sprites
    │   ├── aura_1.png        # Aura sprites
    │   ├── down.png          # Crouching sprite
    │   ├── up.png            # Jumping sprite
    │   ├── fly_left.png      # Flying left sprite
    │   ├── fly_right.png     # Flying right sprite
    │   ├── power_1.png       # Ki charge sprites
    │   ├── taunt_1.png       # Taunt sprites
    │   ├── coverup.png       # Covering up sprite
    │   ├── win.png           # Victory sprite
    │   ├── lose.png          # Defeat sprite
    │   └── blast.png         # Ki projectile sprite
    └── [transformation_name]/  # Folders for each transformation
        ├── stand.png
        ├── punch_1.png
        └── ...
```

### Folder Rules

1. **The character folder name** is used as a unique identifier throughout the game
2. **The base folder** (usually `normal/`) is required — it's the character's initial form
3. **Transformation folders** use the same name as the value defined in `char.json` → `"phase 1": "ssj"` = folder `ssj/`
4. **If a transformation doesn't have a folder**, the game won't load it correctly

---

## Step 2: Prepare the Sprites

### Required Format

- **Extension:** `.png`
- **Background:** Transparent
- **Resolution:** Consistent across all sprites of the same character (e.g., 200x200px)

### Sprite Naming

Sprites are named with a category prefix and a sequence number:

| File | Description | Sequence |
|------|-------------|----------|
| `stand.png` or `stand_1.png` | Idle / Standing | 1 or Animation (if more than 1, it animates) |
| `punch_1.png`, `punch_2.png`... | Punches | Animation sequence |
| `kick_1.png`, `kick_2.png`... | Kicks | Animation sequence |
| `damaged_1.png`, `damaged_2.png`... | Damage received | Animation sequence |
| `aura_1.png`, `aura_2.png`... | Aura / Visual effect | Animation sequence |
| `power_1.png`, `power_2.png`... | Ki charge | Animation sequence |
| `taunt_1.png`, `taunt_2.png`... | Taunt | Animation sequence |
| `dodge_1.png`, `dodge_2.png`... | Dodge (special forms only) | Sequence |
| `down.png` | Crouching | 1 sprite |
| `up.png` | Jumping | 1 sprite |
| `fly_left.png` | Flying left | 1 sprite |
| `fly_right.png` | Flying right | 1 sprite |
| `coverup.png` | Covering up | 1 sprite |
| `win.png` | Victory | 1 sprite |
| `lose.png` | Defeat | 1 sprite |
| `blast.png` | Ki projectile | 1 sprite |

### Sprite Categories the Game Detects

The system automatically checks these filenames on import:

```
aura, damaged, kick, punch, taunt, power, blast, dodge, roll,
stand, fly_left, fly_right, up, down, tackle
```

### Minimum Recommended Sprites

For the character to work correctly, you need at minimum:

```
stand.png        ← Required (game looks for this for the preview)
punch_1.png      ← For attacking
kick_1.png       ← For attacking
damaged_1.png    ← For receiving damage
aura_1.png       ← For the visual aura
down.png         ← For crouching
up.png           ← For jumping
fly_left.png     ← For moving left
fly_right.png    ← For moving right
coverup.png      ← For covering up
win.png          ← For victory screen
lose.png         ← For defeat screen
blast.png        ← For Ki projectile
```

---

## Step 3: Create the `char.json`

This is the most important file. It defines all character properties.

### Basic Structure (Minimum)

A character without transformations:

```json
{
    "folder": "MyCharacter",
    "base": "normal",
    "name": "Character Name",
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

### Complete Structure (With Transformations)

```json
{
    "folder": "MyCharacter",
    "base": "normal",
    "name": "Character Name",
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

## Step 4: Complete `char.json` Reference

### `folder` Field

```json
"folder": "MyCharacter"
```

- **Type:** String (required)
- **Description:** Character folder name inside `chars/`
- **Must match** the folder name exactly

### `base` Field

```json
"base": "normal"
```

- **Type:** String (required)
- **Description:** Subfolder name containing the character's base form
- **Examples:** `"normal"`, `"base"`, `"Perfect"`, `"rage"`

### `name` Field

```json
"name": "Son Goku"
```

- **Type:** String (required)
- **Description:** Name displayed on the selection screen
- **Can be empty** — the game uses `"El Pichula"` as fallback

### `statistics` Field

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

| Statistic | Type | Required | Description | Default Value |
|-----------|------|----------|-------------|---------------|
| `speed` | Number | Yes | Horizontal movement speed | 420 |
| `life` | Number | Yes | Maximum health | 100 |
| `damaged` | Number | Yes | Base attack power | 97 |
| `defence` | Number | Yes | Defense (reduces incoming damage) | 17 |
| `Attack Speed` | Number | No | Attack animation speed (lower = faster). Multiplied by 0.01. Minimum: 0.06 | 0.08 (8) |
| `Stand Speed` | Number | No | Idle animation speed | 0.08 (8) |
| `Taunt Speed` | Number | No | Taunt animation speed | 0.08 (8) |
| `Aura Speed` | Number | No | Aura animation speed | 0.08 (8) |

**Notes:**
- Speed values range from ~350 (slow) to ~500 (fast)
- Life values range from 80 (fragile) to 200 (tank)
- Damaged values range from 80 (low) to 140 (high)
- Defence values range from 10 (low) to 25 (high)

### `transformation` Field

```json
"transformation": {
    "eneable": true,
    "phase 1": "ssj",
    "phase 2": "ssj2",
    "phase 4": "god"
}
```

- **`eneable`** (Boolean, required): Enables/disables the transformation system
- **`phase N`** (String): Subfolder name for each transformation phase
- **Phases go from 1 to 7** (phase 7 = cheat form)
- **You can skip phases** — Vegeta uses phase 1, 2, 4, 5, 6.5 (no phase 3)
- **Supports decimals** — `"phase 6.5": "blue_ev"` works

**Usage examples:**

| Character | Phases | Notes |
|-----------|--------|-------|
| Goku | 1-6 | Sequential transformations |
| Vegeta | 1, 2, 4, 5, 6.5 | Skips phase 3, uses decimals |
| Broly | 4 | Single transformation |
| Beerus | (none) | No transformations |
| Cell | (none) | No transformations |

### `base color` Field (Optional)

For characters that have an aura in their base form:

```json
"base color": {
    "eneable": true,
    "color": "#ffff00",
    "radio": 3,
    "transparecy": 80
}
```

| Property | Type | Description |
|----------|------|-------------|
| `eneable` | Boolean | Enable aura in base form |
| `color` | String | Hex color code |
| `radio` | Number | Aura radius size (1-10) |
| `transparecy` | Number | Transparency (0=solid, 100=invisible) |

### `transformation color` Field

Defines the aura/glow color during each transformation:

```json
"transformation color": {
    "eneable": true,
    "phase 1": {"color": "#ffff00", "radio": 4, "transparecy": 75},
    "phase 2": {"color": "#ffff00", "radio": 5, "transparecy": 60},
    "cheat phase": {"color": "#95A4D6", "radio": 3, "transparecy": 40}
}
```

- **`eneable`** (Boolean): Enables/disables transformation colors
- **`phase N`** (Object): Color for each phase — `"phase 1"`, `"phase 2"`, etc.
- **`cheat phase`** (Object): Color for the cheat phase (phase 7)
- **`cheat phase 2`** (Object): Second cheat color (for characters with double cheat)

| Property | Type | Description |
|----------|------|-------------|
| `color` | String | Hex color code |
| `radio` | Number | Glow size (1-10) |
| `transparecy` | Number | Transparency (0-100) |

### `Char Effects` Field

Defines the visual aura effect overlaid on the character during each phase:

```json
"Char Effects": {
    "Phase 0": {"eneable": true, "effect": "cianray", "speed": 0.12, "transparecy": 20},
    "Phase 1": {"eneable": true, "effect": "yellow", "speed": 0.12, "transparecy": 70},
    "Phase 2": {"eneable": true, "effect": "cianray", "speed": 0.12, "transparecy": 20},
    "Phase 7": {"eneable": true, "effect": "cian", "speed": 0.08, "transparecy": 65}
}
```

**Available effects** (folder `data/resources/CharEffects/`):

| Effect | Color |
|--------|-------|
| `yellow` | Yellow (classic SSJ) |
| `blue` | Blue (SSJ Blue) |
| `blueEv` | Dark blue (Blue Evolution) |
| `cian` | Cyan |
| `cianray` | Cyan with rays |
| `god` | Divine red (SSJ God) |
| `golden` | Golden (Freezer Golden) |
| `green` | Green (Broly) |
| `orange` | Orange (Piccolo Orange) |
| `purple` | Purple (Ultra Ego) |
| `purpleray` | Purple with rays |
| `red` | Red |
| `redray` | Red with rays |
| `beast` | Beast (Gohan Beast) |
| `divine` | Divine |
| `bright` | Bright |
| `goldbright` | Golden bright |
| `stars` | Stars |

| Property | Type | Description |
|----------|------|-------------|
| `eneable` | Boolean | Enable/disable effect |
| `effect` | String | Effect name (see table) |
| `speed` | Number | Animation speed (0.06-0.2) |
| `transparecy` | Number | Transparency (0-100) |

### `cheats` Field

Defines the character's special abilities:

```json
"cheats": {
    "slot 1": "teleport",
    "slot 2": "fastCharge",
    "slot 3": "kaiokenx4",
    "slot 4": "dodge=phase:6"
}
```

**Available cheats:**

| Cheat | Effect |
|-------|--------|
| `teleport` | Allows teleporting in base form with Ki >= 1 |
| `fastCharge` | +15% charge speed (85 px/frame) |
| `Maxcharge` | +31% charge speed (95 px/frame) |
| `lowercharge` | -23% charge speed (60 px/frame) |
| `mui` | Mastered Ultra Instinct (cheat phase) |
| `ue` | Ultra Ego (cheat phase) |
| `black` | Black (cheat phase, superior defense) |
| `SSFP` | Super Saiyan Full Power (cheat phase) |
| `kaiokenxN` | Kaioken x N (e.g., `kaiokenx4`, `kaiokenx20`) |
| `TimeJump` | Freezes opponent for 5 seconds |
| `Dodge` | 25-45% dodge with charge cost |
| `MasterDodge` | 95-100% dodge without cost |
| `Accuracy` | Reduces opponent's dodge capability |
| `Recoilless` | Reduces blocked damage, negates knockback |
| `noformback` | Cannot return to base form |
| `updim` | Increases character dimensions |
| `updim=phase:N` | updim only in specific phase N |
| `fixK` | Adjusts kick sprite if too wide |
| `fixJ` | Adjusts punch sprite if too wide |
| `Android` | Auto-charge, cannot charge manually |
| `RecoverLife=X` | Regenerates X health periodically |
| `NoShot` | Cannot fire Ki blasts |
| `NoShot=phase:N` | NoShot only in phase N |
| `dodge=phase:N` | Dodge active only in phase N |

---

## Step 5: The Icon (`ico.png`)

- **Type:** PNG with transparent background
- **Recommended size:** 36x36 pixels
- **Name:** Exactly `ico.png` in the character folder root
- **Function:** Displayed in the character selection grid

If `ico.png` is not found, the game uses `data/resources/ico_char_null.png` as placeholder.

---

## Step 6: Import into the Game

### Verification Process

1. Open `Game.ppsm` in PowerPoint
2. Enable macros when prompted
3. Start the slideshow (F5)
4. Go to **Local Game** → **Character Selection**
5. Click the **"Verify"** button

### What the "Verify" Button Does

The button runs the `OrdenarCharsFolder` macro which:

1. **Scans** the `chars/` folder for subfolders
2. **Detects** all character folders (new and existing)
3. **Loads** the `ico.png` from each (or placeholder if missing)
4. **Creates** a button in the selection grid for each character
5. **Sorts** official characters first, then custom ones
6. **Removes** characters that no longer exist in the folder

### Limits

- **Maximum 66 characters** imported simultaneously
- If more than 45, the grid changes to 22 columns

### Appearance Order

Official characters appear first in this order:
```
Goku, Vegeta, Gohan, Trunks, Piccolo, Android17, Android18, Videl,
KidGohan, Freezer, Cell, KidBuu, Gotenks, SuperBuuGohan, Android21,
Black, Hit, Jiren, Broly, Beerus, Gogeta, Vegetto, Zamasu, Kefla,
Moro, Granola, Janemba
```

Custom characters appear after, in alphabetical order.

---

## Step 7: Verify It Works

When selecting your character on the selection screen:

1. **Preview:** Shows the `stand.png` (or `stand_1.png`) sprite from the base form
2. **Name:** Displays the `name` field from `char.json`
3. **Transformation icon:** Appears if `"transformation" → "eneable": true`
4. **In-game:** The character loads with all defined sprites and statistics

---

## Practical Example: Create a Character Step by Step

### 1. Create folders

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

### 2. Create `char.json`

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

### 3. Import

1. Save the `TrunksFuture` folder inside `chars/`
2. Open the game and go to character selection
3. Click **"Verify"**
4. Your character will appear in the grid
5. Select it and fight!

---

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Character doesn't appear | Missing `char.json` or malformed JSON | Check JSON syntax |
| Preview doesn't load | Missing `stand.png` in base folder | Ensure the file exists |
| Transformation doesn't work | Folder name doesn't match `char.json` | Verify `"phase N": "name"` = folder `name/` |
| Icon doesn't appear | Missing `ico.png` | Create the icon or use the placeholder |
| Import error | Trailing commas or wrong quotes in JSON | Use a JSON validator |
| No aura | `"eneable": false` or effect doesn't exist | Check the field and effect name |
| Game crashes on play | Missing sprite in some phase | Ensure each phase has minimum sprites |

---

## Important Notes

- **DO NOT use accents or special characters** in folder or file names
- **The `eneable` field** (without the "b") is intentional — the game uses this spelling. Don't correct it
- **Transformations are calculated** with engine formulas — stats increase automatically per phase
- **Cheats are activated** with key combinations in the game (see README for controls)
- **Test with an existing character** first to understand the structure before creating a new one
