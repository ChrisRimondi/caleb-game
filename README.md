# Caleb's Epic Shooter

A top-down wave survival shooter built with Python and pygame. Survive 10 waves of increasingly difficult enemies — and unlock the Sabre after wave 5!

---

## Installation (Mac)

**Requirements:** Python 3.8 or higher. Check your version with:

```bash
python3 --version
```

### 1. Clone the repository

```bash
git clone https://github.com/ChrisRimondi/caleb-game.git
cd caleb-game
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

```bash
source venv/bin/activate
```

You should see `(venv)` appear at the start of your terminal prompt.

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the game

```bash
python game.py
```

To quit the game at any time, press `Q` or close the window.

---

## How to Play

### Controls

| Input | Action |
|---|---|
| `W A S D` | Move |
| Mouse | Aim |
| Left Click | Fire Shotgun |
| Hold Right Click | Fire Machine Gun |
| `E` | Swing Sabre *(unlocks after wave 5)* |
| `R` | Use next power-up from queue |
| `Q` | Quit |

### Weapons

| Weapon | Damage | Ammo | Reload |
|---|---|---|---|
| Shotgun | 2 | 25 shots | 10 s |
| Machine Gun | 1 | 85 shots | 10 s |
| Sabre *(unlocked wave 5)* | 3 | — | 0.5 s cooldown |

The Sabre is a melee weapon. It swings in a 180° arc toward your mouse and hits any enemy within close range. You earn it automatically when you clear wave 5.

### Enemies

| Enemy | Color | HP | Attack |
|---|---|---|---|
| Ranger | Green | 2 | Ranged shot — 1 damage, 1 s cooldown |
| Melee | Red | 3 | Melee strike — 2 damage, 2 s cooldown |
| Caster | Purple | 4 | Blast — 2 damage, 2 s cooldown; also summons 2 Melee enemies every 15 s |

### Power-ups

Walk over a power-up to collect it, then press `R` to activate it.

| Pickup | Color | Effect |
|---|---|---|
| Jetpack | Cyan | Fly through pillars and move faster for 5 seconds |
| Bomb | Orange | Destroys all enemies within 5 units — **also deals 5 damage to you!** |
| Health | Green | Restores +5 HP immediately on pickup |

### Waves

There are 10 waves, each with more enemies than the last. A 3-second break is given between waves. If you die, you respawn at the start of the current wave and lose all queued power-ups.

---

## Deactivating the virtual environment

When you are done playing, deactivate the virtual environment with:

```bash
deactivate
```
