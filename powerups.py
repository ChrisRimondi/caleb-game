import math
import pygame
from constants import *

_font_cache = {}

def _font(size):
    if size not in _font_cache:
        _font_cache[size] = pygame.font.SysFont(None, size)
    return _font_cache[size]


class PowerupPickup:
    COLORS  = {'jetpack': CYAN,   'bomb': ORANGE}
    LABELS  = {'jetpack': 'JET',  'bomb': 'BOMB'}

    def __init__(self, pos, ptype):
        self.x, self.y = pos
        self.ptype     = ptype
        self.alive     = True
        self._pulse    = 0.0

    def update(self, dt):
        self._pulse += dt * 3.0

    def check_collect(self, player):
        if not self.alive or not player.alive:
            return
        d = math.sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2)
        if d < 1.2:
            player.add_powerup(self.ptype)
            self.alive = False

    def draw(self, surface):
        px, py = w2s(self.x, self.y)
        r   = int(SCALE * 0.55 + math.sin(self._pulse) * 2)
        col = self.COLORS.get(self.ptype, YELLOW)
        pygame.draw.circle(surface, col, (px, py), r)
        pygame.draw.circle(surface, WHITE, (px, py), r, 2)
        lbl = _font(16).render(self.LABELS.get(self.ptype, '?'), True, BLACK)
        surface.blit(lbl, (px - lbl.get_width() // 2, py - lbl.get_height() // 2))


class HealthPickup:
    def __init__(self, pos):
        self.x, self.y = pos
        self.alive     = True
        self._pulse    = 0.0

    def update(self, dt):
        self._pulse += dt * 3.0

    def check_collect(self, player):
        if not self.alive or not player.alive:
            return
        d = math.sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2)
        if d < 1.2:
            player.health = min(player.max_health, player.health + 5)
            self.alive = False

    def draw(self, surface):
        px, py = w2s(self.x, self.y)
        r = int(SCALE * 0.55 + math.sin(self._pulse) * 2)
        pygame.draw.circle(surface, LIME, (px, py), r)
        pygame.draw.circle(surface, WHITE, (px, py), r, 2)
        lbl = _font(20).render('+5', True, BLACK)
        surface.blit(lbl, (px - lbl.get_width() // 2, py - lbl.get_height() // 2))
