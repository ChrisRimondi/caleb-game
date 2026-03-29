import math
import random
import pygame
from constants import *  # includes get_font


# ---------------------------------------------------------------------------
# Projectile fired by enemies
# ---------------------------------------------------------------------------
class EnemyBullet:
    def __init__(self, x, y, vx, vy, damage, col):
        self.x, self.y   = x, y
        self.vx, self.vy = vx, vy
        self.damage      = damage
        self.col         = col
        self.owner       = 'enemy'
        self.alive       = True

    def update(self, dt, arena):
        self.x += self.vx * dt
        self.y += self.vy * dt
        if abs(self.x) > 25.5 or abs(self.y) > 25.5:
            self.alive = False
        elif arena.bullet_hits_pillar(self.x, self.y):
            self.alive = False

    def draw(self, surface):
        px, py = w2s(self.x, self.y)
        pygame.draw.circle(surface, self.col, (px, py), 5)
        pygame.draw.circle(surface, WHITE, (px, py), 5, 1)


# ---------------------------------------------------------------------------
# Base enemy
# ---------------------------------------------------------------------------
class BaseEnemy:
    COLOR  = WHITE
    RADIUS = 0.65
    LABEL  = 'Enemy'

    def __init__(self, x, y, player):
        self.x, self.y  = float(x), float(y)
        self.player     = player
        self.max_health = 1
        self.health     = 1
        self.alive      = True
        self.speed      = 2.0
        self.pref_dist  = 1.5   # preferred distance to player
        self.atk_dmg    = 1
        self.atk_cd     = 1.0
        self.atk_timer  = random.uniform(0, 1.0)
        self.hit_flash  = 0.0

    def _dist(self):
        return math.sqrt((self.x - self.player.x) ** 2 +
                         (self.y - self.player.y) ** 2)

    def _move(self, dt):
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        d  = math.sqrt(dx * dx + dy * dy)
        if d > self.pref_dist:
            self.x += (dx / d) * self.speed * dt
            self.y += (dy / d) * self.speed * dt

    def update(self, dt, player, enemies, bullets):
        if not self.alive or not player.alive:
            return
        self._move(dt)
        self.atk_timer -= dt
        if self.atk_timer <= 0:
            self._attack(bullets, enemies)
            self.atk_timer = self.atk_cd
        if self.hit_flash > 0:
            self.hit_flash -= dt

    def _attack(self, bullets, enemies):
        pass

    def take_damage(self, amount):
        if not self.alive:
            return
        self.health -= amount
        self.hit_flash = 0.15
        if self.health <= 0:
            self.alive = False

    def draw(self, surface):
        px, py = w2s(self.x, self.y)
        r      = int(self.RADIUS * SCALE)
        col    = WHITE if self.hit_flash > 0 else self.COLOR
        pygame.draw.circle(surface, col, (px, py), r)
        pygame.draw.circle(surface, WHITE, (px, py), r, 2)
        self._draw_hp_bar(surface, px, py, r)
        self._draw_label(surface, px, py, r)

    def _draw_label(self, surface, px, py, r):
        font = get_font(16)
        tag  = font.render(self.LABEL, True, WHITE)
        tx   = px - tag.get_width() // 2
        ty   = py - r - 18
        surface.blit(tag, (tx, ty))

    def _draw_hp_bar(self, surface, px, py, r):
        bw = r * 2 + 4
        bh = 5
        bx = px - r - 2
        by = py - r - 10
        pygame.draw.rect(surface, (80, 0, 0), (bx, by, bw, bh))
        ratio = max(0.0, self.health / self.max_health)
        pygame.draw.rect(surface, RED, (bx, by, int(bw * ratio), bh))
        pygame.draw.rect(surface, WHITE, (bx, by, bw, bh), 1)


# ---------------------------------------------------------------------------
# Range Attacker  (green) — bow, 2 HP, 1 s attack CD
# ---------------------------------------------------------------------------
class RangeEnemy(BaseEnemy):
    COLOR = (50, 190, 60)
    LABEL = 'Ranger'

    def __init__(self, x, y, player):
        super().__init__(x, y, player)
        self.max_health = 2
        self.health     = 2
        self.speed      = 4.0
        self.pref_dist  = 12.0
        self.atk_dmg    = 1
        self.atk_cd     = 1.0
        self.atk_timer  = random.uniform(0, 1.0)

    def _attack(self, bullets, enemies):
        if self._dist() > 22:
            return
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        d  = math.sqrt(dx * dx + dy * dy)
        if d > 0:
            spd = 14.0
            bullets.append(EnemyBullet(self.x, self.y,
                                        dx / d * spd, dy / d * spd,
                                        self.atk_dmg, (120, 230, 120)))


# ---------------------------------------------------------------------------
# Melee Attacker  (red) — sword, 3 HP, 2 s attack CD, slow
# ---------------------------------------------------------------------------
class MeleeEnemy(BaseEnemy):
    COLOR = (210, 55, 55)
    LABEL = 'Melee'

    def __init__(self, x, y, player):
        super().__init__(x, y, player)
        self.max_health = 3
        self.health     = 3
        self.speed      = 2.5
        self.pref_dist  = 0.8
        self.atk_dmg    = 2
        self.atk_cd     = 2.0
        self.atk_timer  = random.uniform(0, 2.0)

    def _attack(self, bullets, enemies):
        if self._dist() <= 1.5:
            self.player.take_damage(self.atk_dmg)


# ---------------------------------------------------------------------------
# Spell Caster    (purple) — blast 2 dmg + summon, 4 HP
# ---------------------------------------------------------------------------
class CasterEnemy(BaseEnemy):
    COLOR = (165, 55, 225)
    LABEL = 'Caster'

    def __init__(self, x, y, player):
        super().__init__(x, y, player)
        self.max_health   = 4
        self.health       = 4
        self.speed        = 3.0
        self.pref_dist    = 15.0
        self.atk_dmg      = 2
        self.atk_cd       = 2.0
        self.atk_timer    = random.uniform(0, 2.0)
        self.summon_cd    = 15.0
        self.summon_timer = self.summon_cd

    def update(self, dt, player, enemies, bullets):
        super().update(dt, player, enemies, bullets)
        if not self.alive:
            return
        self.summon_timer -= dt
        if self.summon_timer <= 0:
            self.summon_timer = self.summon_cd
            self._summon(enemies)

    def _attack(self, bullets, enemies):
        if self._dist() > 22:
            return
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        d  = math.sqrt(dx * dx + dy * dy)
        if d > 0:
            spd = 10.0
            bullets.append(EnemyBullet(self.x, self.y,
                                        dx / d * spd, dy / d * spd,
                                        self.atk_dmg, (220, 100, 255)))

    def _summon(self, enemies):
        for _ in range(2):
            sx = max(-24, min(24, self.x + random.uniform(-3, 3)))
            sy = max(-24, min(24, self.y + random.uniform(-3, 3)))
            enemies.append(MeleeEnemy(sx, sy, self.player))
