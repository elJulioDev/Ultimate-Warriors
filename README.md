<div align="center">
  
# ⚡ Ultimate Warriors

### Dragon Ball 2D Fighting Game in PowerPoint

<p align="center">
  <img src="https://img.shields.io/badge/VBA-Powered-217346?style=for-the-badge&logo=microsoft&logoColor=white" alt="VBA">
  <img src="https://img.shields.io/badge/Python-Bot_Support-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Platform">
  <img src="https://img.shields.io/badge/PowerPoint-2016+-D04423?style=for-the-badge&logo=microsoftpowerpoint&logoColor=white" alt="PowerPoint">
</p>

<p align="center">
  <strong>A full-featured 2D fighting game built entirely in PowerPoint using VBA</strong><br>
  Complete with transformations, combos, special moves, and an intelligent Python bot
</p>

<img src="https://img.shields.io/badge/Status-Active-success?style=flat-square" alt="Status">
<img src="https://img.shields.io/badge/Game_Engine-Custom_VBA-217346?style=flat-square" alt="Engine">
<img src="https://img.shields.io/badge/Genre-Fighting-red?style=flat-square" alt="Genre">

</div>

***

## ✨ Features

<table>
<tr>
<td width="50%">

### ⚔️ Combat System
- **2D Fighting Mechanics**: Movement, jumps, attacks, Ki blasts
- **Box Collision Detection**: Precise hitbox & hurtbox system
- **Guard & Tackle System**: Block attacks and crash into opponents
- **Combo Calculator**: Damage tracking with scoring system

</td>
<td width="50%">

### 🔥 Transformation System
- **Dynamic Phases**: SSJ, God forms, Ultra Instinct, and more
- **Stat Modifications**: Damage, defense, speed changes per form
- **Kaioken Modes**: Temporary power boosts with life drain
- **Visual Effects**: Auras, glows, and transformation animations

</td>
</tr>
<tr>
<td width="50%">

### 🎮 Advanced Features
- **Character Cheats**: Special abilities per character
- **Round-Based Scoring**: Points, ranks, and victory screens
- **Sprite Animation System**: Frame-by-frame character rendering
- **Custom Stages**: JSON-defined arenas with unique properties

</td>
<td width="50%">

### 🤖 AI & Customization
- **Python Bot Integration**: Real-time AI opponent
- **JSON Character Data**: Easy character creation
- **Custom Controls**: Remappable key bindings
- **Sound System**: Music and SFX via Windows APIs

</td>
</tr>
</table>

***

## 🧠 Technical Highlights

<table>
<tr>
<td width="50%">

### 🔧 Game Engine
- **VBA Game Loop** with DeltaTime synchronization
- **State Management** for characters and gameplay
- **Collision Physics** with gravity and boundaries
- **Module Architecture** for maintainable code

</td>
<td width="50%">

### 📊 Data-Driven Design
- **JSON Configuration** for characters, stages, controls
- **Sprite System** with dynamic loading and caching
- **Settings Persistence** with save/load functionality
- **Bot Communication** via real-time JSON file exchange

</td>
</tr>
</table>

***

## 📥 Requirements

### Software
- **Microsoft Office 2016 or higher** (PowerPoint with macro support enabled)
- **Windows OS** (required for system APIs: keyboard, sound, timing)
- **Python 3.x** (for bot functionality)

### Python Libraries (for bot)

Built-in libraries used: `os`, `json`, `threading`, `random`, `time`

### Additional Setup
- **Font Installation**: Install fonts from the `/font` folder for proper HUD display
- **Macro Permissions**: Enable macros in PowerPoint security settings

***

## 💻 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | Dual-core 2.0 GHz | Quad-core 2.5 GHz+ |
| **RAM** | 4 GB | 8 GB |
| **GPU** | Integrated graphics | Modern integrated/dedicated |
| **Storage** | 1 GB free space | 2 GB+ |
| **OS** | Windows 7+ | Windows 10/11 |

***

## 🎮 How to Play

### Basic Controls
- **Movement**: Arrow keys or WASD
- **Jump**: Up arrow/W
- **Punch/Kick**: Configurable attack keys
- **Ki Blast**: Energy projectile attack
- **Charge**: Hold to build energy bar
- **Guard**: Down + block key

### Transformations
- **S + J**: Transform to next phase
- **S + A + D + J**: Jump to max phase
- **S + K/L**: Access special forms
- Requires sufficient energy charge

### Installation

```bash
Clone the repository
git clone https://github.com/yourusername/ultimate-warriors.git

Navigate to directory
cd ultimate-warriors

Install Python dependencies (for bot)
pip install keyboard

Install fonts (Windows)
Right-click fonts in /font folder → Install for all users
