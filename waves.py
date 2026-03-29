import random
from enemies import RangeEnemy, MeleeEnemy, CasterEnemy
from powerups import PowerupPickup, HealthPickup

WAVE_DEFS = [
    {'range': 4,  'melee': 0,  'caster': 0},   # Wave 1
    {'range': 5,  'melee': 2,  'caster': 0},   # Wave 2
    {'range': 5,  'melee': 4,  'caster': 0},   # Wave 3
    {'range': 6,  'melee': 4,  'caster': 1},   # Wave 4
    {'range': 6,  'melee': 6,  'caster': 2},   # Wave 5
    {'range': 8,  'melee': 6,  'caster': 2},   # Wave 6
    {'range': 8,  'melee': 8,  'caster': 3},   # Wave 7
    {'range': 10, 'melee': 8,  'caster': 4},   # Wave 8
    {'range': 12, 'melee': 10, 'caster': 4},   # Wave 9
    {'range': 15, 'melee': 12, 'caster': 6},   # Wave 10
]

POWERUP_TYPES = ['jetpack', 'bomb']


class WaveManager:
    def __init__(self, player, arena):
        self.player  = player
        self.arena   = arena
        self.enemies = []
        self.pickups = []

        self.current_wave  = 0
        self.wave_active   = False
        self.between_waves = False
        self.between_timer = 0.0
        self._next_wave    = 0

    # ------------------------------------------------------------------
    def reset(self):
        self._clear_enemies()
        self._clear_pickups()
        self.current_wave  = 0
        self.wave_active   = False
        self.between_waves = False

    def start_wave(self, wave_index):
        self.current_wave  = wave_index
        self.between_waves = False
        self._clear_enemies()
        self._clear_pickups()
        self._spawn_enemies(wave_index)
        self._spawn_pickups()
        self.wave_active = True

    # ------------------------------------------------------------------
    def update(self, dt):
        """Returns 'victory', 'wave_cleared', or None."""
        if self.between_waves:
            self.between_timer -= dt
            if self.between_timer <= 0:
                self.start_wave(self._next_wave)
            return None

        if not self.wave_active:
            return None

        if not any(e.alive for e in self.enemies):
            self.wave_active = False
            if self.current_wave >= 9:
                return 'victory'
            self.between_waves = True
            self.between_timer = 3.0
            self._next_wave    = self.current_wave + 1
            return 'wave_cleared'

        return None

    # ------------------------------------------------------------------
    def _spawn_enemies(self, wave_index):
        wave = WAVE_DEFS[wave_index]
        for _ in range(wave['range']):
            pos = self.arena.random_open_position(min_dist_from_center=10)
            self.enemies.append(RangeEnemy(pos[0], pos[1], self.player))
        for _ in range(wave['melee']):
            pos = self.arena.random_open_position(min_dist_from_center=10)
            self.enemies.append(MeleeEnemy(pos[0], pos[1], self.player))
        for _ in range(wave['caster']):
            pos = self.arena.random_open_position(min_dist_from_center=12)
            self.enemies.append(CasterEnemy(pos[0], pos[1], self.player))

    def _spawn_pickups(self):
        for _ in range(random.randint(1, 2)):
            ptype = random.choice(POWERUP_TYPES)
            pos   = self.arena.random_open_position(min_dist_from_center=5)
            self.pickups.append(PowerupPickup(pos, ptype))
        pos = self.arena.random_open_position(min_dist_from_center=5)
        self.pickups.append(HealthPickup(pos))

    def _clear_enemies(self):
        self.enemies.clear()

    def _clear_pickups(self):
        self.pickups.clear()
