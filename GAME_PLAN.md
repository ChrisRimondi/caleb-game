# Caleb's FPS Game — Build Plan

## Overview
A first-person shooter game running locally on Mac, built in Python using the **Ursina** game engine.
Ursina is a beginner-friendly 3D Python game engine — no installer needed beyond `pip install ursina`.

---

## Tech Stack
- **Language:** Python 3
- **Engine:** Ursina (3D game engine for Python)
- **Platform:** macOS (runs from terminal with `python game.py`)

---

## Full Game Design (Finalized)

### The Arena
- 50x50 unit battlefield with a flat floor
- Border walls on all 4 sides (player cannot leave)
- 5–7 pillars randomly placed as cover
- Power-ups and health pickups spawn on the ground

### The Player
- 20 health points
- 2 units tall, first-person camera
- **Movement:** WASD + mouse look
- **Jump:** Space bar, 1 unit high
- **Shoot:** Left click (shotgun), Right click (machine gun)
- **Activate power-up:** R key

### Weapons
| Weapon | Button | Damage | Ammo Before Cooldown | Cooldown Duration |
|--------|--------|--------|----------------------|-------------------|
| Shotgun | Left click | 2 HP | 25 shots | 10 seconds |
| Machine Gun | Right click | 1 HP | 85 shots | 10 seconds |

### Enemies
| Type | HP | Damage to Player | Attack Cooldown | Movement | Notes |
|------|-----|-----------------|-----------------|----------|-------|
| Range Attacker | 2 | 1 | 1 second | Moves (slower than player) | Fires arrows |
| Melee Attacker | 3 | 2 | 2 seconds | Slow | Charges player |
| Spell Caster | 4 | 2 (blast) | 2 sec (blast) / 15 sec (summon) | Moves (slower than player) | Summons 2 melee attackers |

### Power-Ups
- Picked up by walking over them; stack in a queue
- **R** activates the next power-up in queue (one at a time)
- **Jetpack** — player can fly freely for 5 seconds
- **Bomb** — explodes in a 5-unit radius, damages ALL entities including the player

### Health Pickups
- 1 health pickup spawns somewhere on the map each wave
- Player walks over it to heal

### Waves (10 Total — Game Decides Composition)
| Wave | Enemies | Notes |
|------|---------|-------|
| 1 | 4 Range | Intro wave, easy |
| 2 | 5 Range, 2 Melee | First melee introduced |
| 3 | 5 Range, 4 Melee | More pressure |
| 4 | 6 Range, 4 Melee, 1 Caster | First spell caster |
| 5 | 6 Range, 6 Melee, 2 Casters | Midpoint spike |
| 6 | 8 Range, 6 Melee, 2 Casters | More ranged |
| 7 | 8 Range, 8 Melee, 3 Casters | Heavier summons |
| 8 | 10 Range, 8 Melee, 4 Casters | High pressure |
| 9 | 12 Range, 10 Melee, 4 Casters | Near-max difficulty |
| 10 | 15 Range, 12 Melee, 6 Casters | Final boss wave |

- Clearing all enemies advances to next wave
- On death: player respawns, loses all queued power-ups, wave restarts from beginning
- Completing wave 10 → **Victory Screen**

---

## Planned File Structure
```
caleb_game/
├── game.py              # Main entry point, game loop
├── arena.py             # Floor, border walls, pillars
├── player.py            # Player movement, health, weapons, power-up queue
├── enemies.py           # Enemy base class + Range, Melee, Caster types
├── weapons.py           # Shotgun and machine gun logic, cooldowns
├── powerups.py          # Jetpack, bomb, health pickup logic
├── waves.py             # Wave definitions and enemy spawning
├── ui.py                # HUD: health bar, wave counter, ammo, power-up queue
└── GAME_PLAN.md         # This file
```

---

## Build Order
1. Install Ursina, create arena (floor, walls, 5–7 pillars)
2. Add player: WASD movement, mouse look, jumping, first-person camera
3. Add weapons: shotgun + machine gun, ammo tracking, 10-sec cooldowns
4. Add enemy base class + all 3 enemy types with basic AI (move toward player, attack)
5. Add wave system: spawn enemies per wave table, detect wave clear, advance wave
6. Add power-ups and health pickup: spawn, pickup collision, R activation, queue display
7. Add HUD: health bar, wave number, ammo count, power-up queue
8. Add death/respawn: lose power-ups, restart current wave
9. Add victory screen (after wave 10) and game over screen
10. Final tuning: enemy speeds, spawn positions, pillar layout

---

## Notes
- Enemy AI: move toward player each frame, attack when in range, avoid re-pathing through walls using simple steering
- Spell Caster summon spawns 2 melee attackers near the caster's position
- Bomb damage applies to the player if within 5 units — use carefully!
- Power-up queue shows stacked icons on HUD; R pops the front item
